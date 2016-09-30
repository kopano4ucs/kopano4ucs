#!/bin/sh

. /usr/share/univention-lib/all.sh

echo "enabling user_safe_mode for Kopano prior to installation"
ucr set kopano/cfg/server/user_safe_mode=yes

echo "stopping all kopano server processes"
/etc/init.d/postfix stop
for kop in /etc/init.d/kopano-*; do
	$kop stop
done

/usr/share/kopano4ucs/kopano4ucs-migrate-ldap.sh
/usr/share/kopano4ucs/kopano4ucs-migrate-ucr.sh
/usr/share/kopano4ucs/kopano4ucs-migrate-files.sh

/etc/init.d/kopano-server start

echo "Kopano-server has been automatically started, please check if all data has been succesfully migrated."
echo "Once the migration has been verified please remember to deactivate user_safe_mode and start the remaining services".
echo "ucr set kopano/cfg/server/user_safe_mode=no"
