#!/bin/bash

LDAP_HOST="$(ucr get ldap/master)"
LDAP_PORT="$(ucr get ldap/master/port)"
LDAP_USER="cn=admin,$(ucr get ldap/base)"
LDAP_PASSWD_FILE="/etc/ldap.secret"
LDAP_LDIF="/tmp/zarafa2kopano.ldif"

cleanup (){
	if [ -e /tmp/zarafa2kopano.passwd ]; then
		rm /tmp/zarafa2kopano.passwd
	fi
}

if [ ! -e $LDAP_PASSWD_FILE ]; then
	echo "It seems you are running this script on an Univention Slave installation."
	read -e -p "Please enter password of your domain Administrator: " LDAP_PASSWD_TEMP
	LDAP_USER="uid=Administrator,cn=users,$(ucr get ldap/base)"
	echo -n $LDAP_PASSWD_TEMP > /tmp/zarafa2kopano.passwd
	LDAP_PASSWD_FILE="/tmp/zarafa2kopano.passwd"
	chmod go-rw $LDAP_PASSWD_FILE
fi

# connection test
ldapsearch -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -b "$(ucr get ldap/base)" -y "$LDAP_PASSWD_FILE" cn=admin > /dev/null || { cleanup; exit 1; }

grep ^attributetype /usr/share/kopano4ucs-schema/zarafa4ucs.schema -A1 | grep NAME | sed -e 's#.*NAME..##g' -e 's#.$##' | while read line; do
	new_attrib="`echo $line | sed 's#zarafa#kopano#'`"
	ldapsearch -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -b "$(ucr get ldap/base)" -y "$LDAP_PASSWD_FILE" -o ldif-wrap=no -LLL -x "$line=*" dn "$line" | \
	sed "s#$line: \(.*\)#changetype: modify\nadd: $new_attrib\n$new_attrib: \1\n-\ndelete: $line\n$line: \1\n-#" >> "$LDAP_LDIF".step2_attribute_data
done


# We now have the LDIF, we now need to extend the objects with the new objectClass.
grep ^dn "$LDAP_LDIF".step2_attribute_data | sort | uniq | sed 's#dn: ##' | while read dn; do
	ldapsearch -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -b "$(ucr get ldap/base)" -y "$LDAP_PASSWD_FILE" -o ldif-wrap=no -LLL -x -s base -b "$dn" objectclass | \
	egrep '(^dn|zarafa)' | sed -e '/^objectClass/ s#zarafa#kopano#' | sed 's#objectClass:\(.*\)#changetype: modify\nadd: objectClass\nobjectClass:\1\n#'
done >> "$LDAP_LDIF".step1_objectclass_extend
ldapmodify -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -y "$LDAP_PASSWD_FILE" -f "$LDAP_LDIF".step1_objectclass_extend

# We are done with the LDIF, now lets do it.
ldapmodify -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -y "$LDAP_PASSWD_FILE" -f "$LDAP_LDIF".step2_attribute_data

grep ^dn "$LDAP_LDIF".step2_attribute_data | sort | uniq | sed 's#dn: ##' | while read dn; do
	ldapsearch -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -b "$(ucr get ldap/base)" -y "$LDAP_PASSWD_FILE" -o ldif-wrap=no -LLL -x -s base -b "$dn" objectclass | \
	egrep '(^dn|zarafa)' | sed 's#objectClass:\(.*\)#changetype: modify\ndelete: objectClass\nobjectClass:\1\n#'
done >> "$LDAP_LDIF".step3_objectclass_remove
ldapmodify -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -y "$LDAP_PASSWD_FILE" -f "$LDAP_LDIF".step3_objectclass_remove

# Clean up
cleanup
