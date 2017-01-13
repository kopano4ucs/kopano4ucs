#!/bin/bash

. /usr/share/univention-lib/all.sh

echo "Please make sure that you have entirely read https://wiki.z-hub.io/x/OIAo and"
echo "that all modification you made to your Zarafa configuration files are stored in the Univention Configuration Registry."
read -p 'Do you want to continue? (y/n) ' -n 1 confirmation
echo
if [[ $confirmation != 'y' && $confirmation != 'Y' ]]; then
        exit 3
fi

echo "enabling user_safe_mode for Kopano prior to installation"
ucr set kopano/cfg/server/user_safe_mode=yes

echo "stopping all kopano server processes"
service fetchmail stop
service postfix stop
for kop in /etc/init.d/kopano-*; do
	$kop stop
done

migrationlog=/var/log/kopano/kopano4ucs-migrate.log

echo "All actions done by the next steps are logged to $migrationlog"

echo "------ldap-----" >> $migrationlog
bash -x /usr/share/kopano4ucs/kopano4ucs-migrate-ldap.sh 2>&1 | tee -a $migrationlog ; test ${PIPESTATUS[0]} -eq 0 || { echo "Something went wrong, please check your logs.";  exit 1; }
echo "-----ucr-----" >> $migrationlog
bash -x /usr/share/kopano4ucs/kopano4ucs-migrate-ucr.sh 2>&1 | tee -a $migrationlog
echo "-----files-----" >> $migrationlog
bash -x /usr/share/kopano4ucs/kopano4ucs-migrate-files.sh 2>&1 | tee -a $migrationlog

service kopano-server start

echo "Kopano-server has been automatically started, please check if all data has been succesfully migrated."
echo "Once the migration has been verified please remember to deactivate user_safe_mode and start the remaining services:"
echo "ucr set kopano/cfg/server/user_safe_mode=no"
echo "for kop in /etc/init.d/kopano-*; do
	'$kop' start
done"
echo "service postfix start"
echo "service fetchmail start"
