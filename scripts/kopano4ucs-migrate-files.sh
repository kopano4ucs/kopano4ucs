#!/bin/bash

# clean up files not removed by uninstalling zarafa app
if [ -e /etc/mapi/zarafa.inf ]; then
	rm /etc/mapi/zarafa.inf
fi

# check if attachment_path or index_path are defined as an ucr variable
# if not defined set variable with /var/lib/zarafa/$
# chown in both cases
