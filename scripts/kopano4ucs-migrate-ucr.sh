#!/bin/bash

WORKDIR=$(mktemp -d)

# extract migration relevant ucr variables
ucr dump | grep 'zarafa/cfg\|zarafa/default\|zarafa/webapp' > $WORKDIR/ZARAFA-values

# remove ucr variables that should not be migrated
sed -i -e '/ldap_bind_/d' \
    -e '/license_socket/d' \
    -e '/local_admin_users/d' \
    -e '/pid_file/d' \
    -e '/run_as_group/d' \
    -e '/run_as_user/d' \
    -e '/search_socket/d' \
    -e '/server_bind_name/d' \
    -e '/server_pipe_name/d' \
    -e '/server_pipe_priority/d' \
    -e '/server_socket/d' $WORKDIR/ZARAFA-values
# remove default value for mysql_password
sed -i '\:/etc/zarafa-mysql.secret:d' $WORKDIR/ZARAFA-values

# delete ucr for default certificates (new default ones are already generated for kopano)
# if admin has set custom certificates over ucr this value will be migrated
sed -i -e '\:/etc/zarafa/ssl/cert.pem:d' \
    -e '\:/etc/zarafa/ssl/private.key:d' \
    -e '\:/etc/zarafa/ssl/server.pem:d' $WORKDIR/ZARAFA-values

# replace occurence of zarafa with     (because of changed ldap objectclasses and attributes
sed -i -e 's/zarafaAccount/kopanoAccount/' \
    -e 's/zarafa-group/kopano-group/' \
    -e 's/zarafaSharedStoreOnly/kopanoSharedStoreOnly/' \
    -e 's/zarafa-user/kopano-user/' \
    -e 's/ZARAFA_LOCALE/KOPANO_LOCALE/' \
    -e 's/ZARAFA_USERSCRIPT_LOCALE/KOPANO_USERSCRIPT_LOCALE/' $WORKDIR/ZARAFA-values

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
