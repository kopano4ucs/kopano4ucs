#!/bin/sh

kopanoversion=$(dpkg-query --showformat='${Version}' --show kopano-server)

if $(dpkg --compare-versions $kopanoversion "gt" "8.6.81"); then
	echo "Installation with Kopano Groupware Core 8.7 detected"

	echo "configuring kopano-gateway"
	univention-config-registry set \
		kopano/cfg/gateway/pop3s_listen?'*:995' \
		kopano/cfg/gateway/imaps_listen?'*:993' \
		kopano/cfg/gateway/ssl_private_key_file?'/etc/kopano/ssl/private.key' \
		kopano/cfg/gateway/ssl_certificate_file?'/etc/kopano/ssl/cert.pem'

	echo "removing obsolete options from kopano-gateway configuration"
	univention-config-registry unset \
		kopano/cfg/gateway/imap_enable \
		kopano/cfg/gateway/imaps_enable \
		kopano/cfg/gateway/imap_generate_utf8 \
		kopano/cfg/gateway/imap_port \
		kopano/cfg/gateway/imap_store_rfc822 \
		kopano/cfg/gateway/imaps_port \
		kopano/cfg/gateway/pop3_enable \
		kopano/cfg/gateway/pop3s_enable \
		kopano/cfg/gateway/pop3_port \
		kopano/cfg/gateway/pop3s_port

	sed \
	        -e '/imap_enable/s/^#*/#/g' \
	        -e '/imaps_enable/s/^#*/#/g' \
	        -e '/imap_generate_utf8/s/^#*/#/g' \
	        -e '/imap_port/s/^#*/#/g' \
	        -e '/imap_store_rfc822/s/^#*/#/g' \
	        -e '/imaps_port/s/^#*/#/g' \
	        -e '/pop3_enable/s/^#*/#/g' \
	        -e '/pop3s_enable/s/^#*/#/g' \
	        -e '/pop3_port/s/^#*/#/g' \
	        -e '/pop3s_port/s/^#*/#/g' \
	        -i /etc/kopano/gateway.cfg

	echo "configuring kopano-ical"
	univention-config-registry set \
		kopano/cfg/ical/icals_listen?'*:8443' \
		kopano/cfg/ical/server_timezone?'@&@/etc/timezone@&@' \
		kopano/cfg/ical/ssl_private_key_file?'/etc/kopano/ssl/private.key' \
		kopano/cfg/ical/ssl_certificate_file?'/etc/kopano/ssl/cert.pem'

	echo "removing obsolete options from kopano-ical configuration"
	univention-config-registry unset \
		kopano/cfg/ical/icals_enable \
		kopano/cfg/ical/ical_enable \
		kopano/cfg/ical/ical_port \
		kopano/cfg/ical/icals_port

	sed \
		-e '/ical_enable/s/^#*/#/g' \
		-e '/ical_port/s/^#*/#/g' \
		-e '/icals_enable/s/^#*/#/g' \
		-e '/icals_port/s/^#*/#/g' \
		-i /etc/kopano/ical.cfg

else
	echo "Previous version to Kopano Groupware Core 8.7 detected"
	echo "not updating configuration"
	exit 1
fi
