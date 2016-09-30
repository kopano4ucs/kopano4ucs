#!/bin/bash
set -x

LDAP_HOST="localhost"
LDAP_PORT="$(ucr get ldap/server/port)"
LDAP_USER="cn=admin,$(ucr get ldap/base)"
LDAP_PASSWORD="$(cat /etc/ldap.secret)"
LDAP_LDIF="/tmp/zarafa2kopano.ldif"

grep ^attributetype /usr/share/zarafa4ucs-schema/zarafa4ucs.schema -A1 | grep NAME | sed -e 's#.*NAME..##g' -e 's#.$##' | while read line; do
	new_attrib="`echo $line | sed 's#zarafa#kopano#'`"
	ldapsearch -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -b "cn=users,$(ucr get ldap/base)" -w "$LDAP_PASSWORD" -o ldif-wrap=no -LLL -x $line=* dn $line | \
	sed "s#$line: \(.*\)#changetype: modify\nadd: $new_attrib\n$new_attrib: \1\n-\ndelete: $line\n$line: \1\n-#" >> "$LDAP_LDIF".step2_attribute_data
done


# We now have the LDIF, we now need to extend the objects with the new objectClass.
grep ^dn "$LDAP_LDIF".step2_attribute_data | sort | uniq | sed 's#dn: ##' | while read dn; do
	ldapsearch -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -b "cn=users,$(ucr get ldap/base)" -w "$LDAP_PASSWORD" -o ldif-wrap=no -LLL -x -s base -b "$dn" objectclass | \
	egrep '(^dn|zarafa)' | sed -e '/^objectClass/ s#zarafa#kopano#' | sed 's#objectClass:\(.*\)#changetype: modify\nadd: objectClass\nobjectClass:\1\n#'
done >> "$LDAP_LDIF".step1_objectclass_extend
ldapmodify -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -w "$LDAP_PASSWORD" -f "$LDAP_LDIF".step1_objectclass_extend

# We are done with the LDIF, now lets do it.
ldapmodify -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -w "$LDAP_PASSWORD" -f "$LDAP_LDIF".step2_attribute_data

grep ^dn "$LDAP_LDIF".step2_attribute_data | sort | uniq | sed 's#dn: ##' | while read dn; do
	ldapsearch -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -b "cn=users,$(ucr get ldap/base)" -w "$LDAP_PASSWORD" -o ldif-wrap=no -LLL -x -s base -b "$dn" objectclass | \
	egrep '(^dn|zarafa)' | sed 's#objectClass:\(.*\)#changetype: modify\ndelete: objectClass\nobjectClass:\1\n#'
done >> "$LDAP_LDIF".step3_objectclass_remove
ldapmodify -h "$LDAP_HOST" -p "$LDAP_PORT" -D "$LDAP_USER" -w "$LDAP_PASSWORD" -f "$LDAP_LDIF".step3_objectclass_remove

# Clean up
rm -f "$LDAP_LDIF.step1_objectclass_extend"
rm -f "$LDAP_LDIF.step2_attribute_data"
rm -f "$LDAP_LDIF.step3_objectclass_remove"
