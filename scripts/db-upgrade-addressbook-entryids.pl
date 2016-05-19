#!/usr/bin/perl -w
use strict;
use DBI;
use MIME::Base64;
use XML::DOM;

use constant {
	SYSTEM		=> 1,
	EVERYONE	=> 2,
};

sub readconfig($) {
	my ($fn) = @_;
	my %options;

	open(CFG, $fn) or die("unable to open ".$fn." config file");
	while (<CFG>) {
		if ($_ =~ /^\s*[#!]/) {
			next;
		}
		if ($_ =~ /^\s*(\S+)\s*=\s*([^\r]+)\r?$/) {
			my $idx = $1;
			my $val = $2;
			chomp($val);
			$val =~ s/\s+$//;
			$options{$idx} = $val;
		}
	}
	close(CFG);
	return %options;
}

sub decode_contact_entryid($) {
	my ($entryid) = @_;
	return unpack("LB128LLL", $entryid); # padding is lost
}

sub encode_contact_entryid(@) {
	my (@values) = @_;
	return pack("LB128LLLZ*CCC", @values, 0, 0, 0); # re-add padding!
}

sub getexternid(@) {
	my ($dbh, $id) = @_;
	my ($query, $sth, $externid);
	my @row;
	
	$query = "SELECT externid FROM users WHERE id=?";
	$sth = $dbh->prepare($query)
		or die $DBI::errstr;
	
	$sth->execute($id);
	@row = $sth->fetchrow_array();
	if (scalar(@row) > 0) {
		$externid = encode_base64($row[0]);
		
		# perl base64 adds \n at the end of the base64 data
		chomp($externid);
	}
	
	return $externid;
}

sub upgradeentryid(@) {
	my ($dbh, $cache, $entryid) = @_;
	my @values = decode_contact_entryid($entryid);
		
	if ($values[4] == SYSTEM || $values[4] == EVERYONE) {
		return undef;
	}

	my $externid;
	if (defined($cache->{$values[4]})) {
		$externid = $cache->{$values[4]};
		
	} else {
		$externid = getexternid($dbh, $values[4]);
		
		# if no externid is found, the user is most likely deleted. We could leave the
		# entryid a V0, but that could cause other servers to mistakenly interpret the
		# entryid as a valid (but wrong) user if that has the local id. So we want to
		# make an V1 entryid with an externid that will most likely not match an actual
		# user on any server.
		if (!$externid) {
			$externid=encode_base64("<DELETED>");
			chomp($externid);
		}
		
		$cache->{$values[4]} = $externid;
	}

	die "Id=$values[4], ExternId=Not Found\n" if (!$externid);
			
	# set version to 1
	$values[2] = 1;
	
	# add the encoded extern id
	push(@values, $externid);
	return encode_contact_entryid(@values);
}

sub upgrade_rules {
	my ($dbh, $cache, $doc) = @_;
	my ($nodes, $n, $i, $node);
	my ($entryid, $newentryid, $data, $newdata);
	
	$nodes = $doc->getElementsByTagName ("bin");
	$n = $nodes->getLength;
	for ($i = 0; $i < $n; $i++) {
		$node = $nodes->item($i)->getFirstChild();
		if (defined($node) && $node->getNodeType() == TEXT_NODE) {
			$data = $node->getData();
			#print $data."\n";
			$entryid = decode_base64($data);
			if (substr($entryid, 0, 20) eq pack('H40', '00000000AC21A95040D3EE48B319FBA753304425')) {
				$newentryid = upgradeentryid($dbh, $cache, $entryid);
				if (defined($newentryid)) {
					$newdata = encode_base64($newentryid);
					chomp($newdata);
					
					#print "$data -> $newdata\n";
					$node->setData($newdata);
				}
			}				
		}
	}
}


my $servercfg = $ARGV[0];
$servercfg = "/etc/zarafa/server.cfg" if (!defined($servercfg));

my %serveropt = readconfig($servercfg);

my ($dbh, $query, $sth, $upd, $udh);
my @row;
$dbh = DBI->connect("dbi:mysql:database=".$serveropt{mysql_database}.";host=".$serveropt{mysql_host}, $serveropt{mysql_user}, $serveropt{mysql_password})
	or die $DBI::errstr;
	
# check if the database is 6.30+
@row = $dbh->selectrow_array("SELECT major,minor FROM versions ORDER BY databaserevision DESC LIMIT 1")
	or die $DBI::errstr;

if (scalar(@row) == 0 || ($row[0] != 7 && !($row[0] == 6 && $row[1] >= 30))) {
	print "Database $serveropt{mysql_database} can not be upgraded\n";
#	exit(1);
}
my $dbversion = $row[0];

# join store so we use the index, only return addressbook entries V0
if ($dbversion == 7) {
	# possibly no storeid anymore in properties table
	$query = "SELECT 0,hierarchyid,val_binary FROM properties WHERE type=0x0102 AND tag=? AND substr(val_binary,1,20) = 0x00000000AC21A95040D3EE48B319FBA753304425";
	$upd = "UPDATE properties SET val_binary=? WHERE hierarchyid=? AND type=0x0102 AND tag=?";
} else {
	$query = "SELECT storeid,hierarchyid,val_binary FROM properties JOIN stores on properties.storeid=stores.hierarchy_id WHERE type=0x0102 AND tag=? AND substr(val_binary,1,20) = 0x00000000AC21A95040D3EE48B319FBA753304425";
	$upd = "UPDATE properties SET val_binary=? WHERE hierarchyid=? AND type=0x0102 AND tag=? AND storeid=?";
}
$sth = $dbh->prepare($query)
	or die $DBI::errstr;

$udh = $dbh->prepare($upd)
	or die $DBI::errstr;


# upgrade most recipient entry id's in database
my ($tag, $i);
my %cache;
# tags:
# PR_RECEIVED_BY_ENTRYID, PR_SENT_REPRESENTING_ENTRYID, PR_RCVD_REPRESENTING_ENTRYID, PR_READ_RECEIPT_ENTRYID,
# PR_ORIGINAL_AUTHOR_ENTRYID, PR_ORIGINAL_SENDER_ENTRYID, PR_ORIGINAL_SENT_REPRESENTING_ENTRYID, PR_SENDER_ENTRYID,
# PR_LAST_MODIFIER_ENTRYID, PR_RECIPIENT_ENTRYID, PR_EC_CONTACT_ENTRYID
my @tags = (0x003F, 0x0041, 0x0043, 0x0046,
			0x004C, 0x005B, 0x005E, 0x0C19,
			0x3FFB, 0x5FF7, 0x6710);
$i = 1;
$dbh->begin_work();
foreach $tag (@tags) {
	print "Converting properties table step $i of ".scalar(@tags)."\n";

	$sth->execute($tag);
	while(@row = $sth->fetchrow_array()) {
		my $entryid = upgradeentryid($dbh, \%cache, $row[2]);
		
		if (defined($entryid)) {
                      if ($dbversion == 7) {
                          $udh->execute($entryid, $row[1], $tag)
                                  or die $DBI::errstr;
                      } else {
                          $udh->execute($entryid, $row[1], $tag, $row[0])
                                  or die $DBI::errstr;
                      }
		}
	}

	$i++;
}


# See if the rules contain any addressbook entryids. If so upgrade them.
print "Converting rules...\n";
my $parser = new XML::DOM::Parser;

if ($dbversion == 7) {
	$query = 'SELECT r.objid,0,p.val_binary FROM receivefolder AS r JOIN properties AS p ON r.objid = p.hierarchyid WHERE r.messageclass="IPM" AND p.tag=0x3FE1 AND p.type=0x0102';
	$upd = 'UPDATE properties SET val_binary=? WHERE hierarchyid=? AND type=0x0102 AND tag=0x3FE1';
} else {
	$query = 'SELECT r.objid,r.storeid,p.val_binary FROM receivefolder AS r JOIN properties AS p ON r.storeid=p.storeid AND r.objid = p.hierarchyid WHERE r.messageclass="IPM" AND p.tag=0x3FE1 AND p.type=0x0102';
	$upd = 'UPDATE properties SET val_binary=? WHERE hierarchyid=? AND type=0x0102 AND tag=0x3FE1 AND storeid=?';
}

$sth = $dbh->prepare($query)
	or die $DBI::errstr;
	
$udh = $dbh->prepare($upd)
	or die $DBI::errstr;

$i = 1;
$sth->execute();
while(@row = $sth->fetchrow_array()) {
	print "Converting ruleset $i\n";

	my $doc = $parser->parse($row[2]);
	upgrade_rules($dbh, \%cache, $doc);
	
        if ($dbversion == 7) {
                $udh->execute($doc->toString(), $row[0])
                        or die DBI::errstr;
        } else {
                $udh->execute($doc->toString(), $row[0], $row[1])
                        or die DBI::errstr;
        }

	$doc->dispose();
		
	$i++;
}

# Enable multi server operation
$dbh->do("DELETE FROM settings WHERE name='lock_distributed_zarafa' AND value='upgrade'")
	or die $DBI::errstr;
	
print "Committing changes to database\n";
$dbh->commit();
exit(0);
