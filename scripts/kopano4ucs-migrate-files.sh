#!/bin/bash

# clean up files not removed by uninstalling zarafa app
if [ -e /etc/mapi/zarafa.inf ]; then
	rm /etc/mapi/zarafa.inf
fi

# check if /var/lib/zarafa is a mount. if so keep everything there
if [ ! -z $(mount | grep /var/lib/zarafa) ]; then
	echo "/var/lib/zarafa is a mount, going to reuse it"
	basedirectory=/var/lib/zarafa
	olddir=true
else
	basedirectory=/var/lib/kopano
	olddir=false
fi

# helper function to set variable, rsync & chown contents
function migratedir() {
	registry="$1"
	directory="$2"
	olddir="$3"

	# if not already defined as a variable store location now
	# (assuming that the default location is used otherwise)
	if [ -z $(ucr get "$registry") ]; then
		ucr set "$registry"="$directory"
	fi

	if [ $olddir == "false" ]; then
		rsync -avP $(basename $directory) "$directory"
	fi
	chown -R kopano:kopano "$directory"
}


migratedir kopano/cfg/server/attachment_path $basedirectory/attachments $olddir
migratedir kopano/cfg/server/client_update_path $basedirectory/client $olddir

# deleting old search index
rm -r $basedirectory/search/
migratedir kopano/cfg/search/index_path $basedirectory/search/
