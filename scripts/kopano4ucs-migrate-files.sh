#!/bin/bash

# clean up files not removed by uninstalling zarafa app
if [ -e /etc/mapi/zarafa.inf ]; then
	rm /etc/mapi/zarafa.inf
fi

# check if /var/lib/zarafa is a mount. if so keep everything there
if [ ! -z "$(mount | grep /var/lib/zarafa)" ]; then
	echo "/var/lib/zarafa is a mount, going to reuse it"
	basedirectory=/var/lib/zarafa
	olddir=true
else
	basedirectory=/var/lib/kopano
	olddir=false
fi

# helper function to set variable, rsync & chown contents
function migratedir() {
	local registry="$1"
	local directory="$2"
	local olddir="$3"

	# if not already defined as a variable store location now
	# (assuming that the default location is used otherwise)
	if [ -z $(ucr get "$registry") ]; then
		ucr set "$registry"="$directory"
	fi

	if [ "$olddir" == "false" ]; then
		if [ -d /var/lib/zarafa/$(basename $directory) ]; then
			rsync -avP --remove-source-files /var/lib/zarafa/$(basename $directory)/ "$directory"
		fi
	fi
	if [ -d "$directory" ]; then
		chown -R kopano:kopano "$directory"
	fi
}

# deleting old search index and setting ucr (no moving files)
rm -r $basedirectory/search/
migratedir kopano/cfg/search/index_path $basedirectory/search/

# migrating client msi stored for auto updater
migratedir kopano/cfg/server/client_update_path $basedirectory/client $olddir

# migration attachments
migratedir kopano/cfg/server/attachment_path $basedirectory/attachments $olddir
