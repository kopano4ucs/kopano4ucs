#!/bin/bash

WORKDIR=$(mktemp -d)

# get full dump of univention registry
ucr dump > $WORKDIR/UCR_DUMP

# extract migration relevant ucr variables
grep 'zarafa/cfg\|zarafa/default\|zarafa/webapp' $WORKDIR/UCR_DUMP > $WORKDIR/ZARAFA-values

# remove ucr variables that should not be migrated
sed -i '/ldap_bind_/d' $WORKDIR/ZARAFA-values
sed -i '/license_socket/d' $WORKDIR/ZARAFA-values
sed -i '/local_admin_users/d' $WORKDIR/ZARAFA-values
sed -i '/pid_file/d' $WORKDIR/ZARAFA-values
sed -i '/run_as_group/d' $WORKDIR/ZARAFA-values
sed -i '/run_as_user/d' $WORKDIR/ZARAFA-values
sed -i '/search_socket/d' $WORKDIR/ZARAFA-values
sed -i '/server_bind_name/d' $WORKDIR/ZARAFA-values
sed -i '/server_pipe_name/d' $WORKDIR/ZARAFA-values
sed -i '/server_pipe_priority/d' $WORKDIR/ZARAFA-values
sed -i '/server_socket/d' $WORKDIR/ZARAFA-values
# remove default value for mysql_password
sed -i '\:/etc/zarafa-mysql.secret:d' $WORKDIR/ZARAFA-values

# delete ucr for default certificates (new default ones are already generated for kopano)
# if admin has set custom certificates over ucr this value will be migrated
sed -i '\:/etc/zarafa/ssl/cert.pem:d' $WORKDIR/ZARAFA-values
sed -i '\:/etc/zarafa/ssl/private.key:d' $WORKDIR/ZARAFA-values
sed -i '\:/etc/zarafa/ssl/server.pem:d' $WORKDIR/ZARAFA-values

# replace occurence of zarafa with sed (because of changed ldap objectclasses and attributes
sed -i 's/zarafaAccount/kopanoAccount/' $WORKDIR/ZARAFA-values
sed -i 's/zarafa-group/kopano-group/' $WORKDIR/ZARAFA-values
sed -i 's/zarafaSharedStoreOnly/kopanoSharedStoreOnly/' $WORKDIR/ZARAFA-values
sed -i 's/zarafa-user/kopano-user/' $WORKDIR/ZARAFA-values
sed -i 's/ZARAFA_LOCALE/KOPANO_LOCALE/' $WORKDIR/ZARAFA-values
sed -i 's/ZARAFA_USERSCRIPT_LOCALE/KOPANO_USERSCRIPT_LOCALE/' $WORKDIR/ZARAFA-values

# replace zarafa in ucr path with kopano for all that remains
sed -i 's/^zarafa/kopano/' $WORKDIR/ZARAFA-values

# set all migrated ucr values
while read line; do
	key=${line%%:*}
	value=${line#*:}
	# $value comes with a leading space, so we still have to remove it
	ucr set $key="${value#"${value%%[![:space:]]*}"}"
done < $WORKDIR/ZARAFA-values

rm -rf $WORKDIR
