# -*- coding: utf-8 -*-
#
# Zarafa4UCS
#  listener module
#
# Copyright 2012-2016 Univention GmbH
#
# http://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <http://www.gnu.org/licenses/>.

__package__='' 	# workaround for PEP 366
import listener
import subprocess
import univention.debug

name='zarafa'
description='update database of zarafa on changes in UCS LDAP'
filter='(|(zarafaAccount=1)(objectClass=zarafa-group))'
attributes=[]
modrdn="1"

# dn --> new_attributes
changed_objects = {}
event_counter = 0

def handler(dn, new, old, command):

	global changed_objects, event_counter

	# ignore modrdn changes
	if command == "r":
		return

	# call postrun() at least every 20 changes directly
	if event_counter > 20:
		postrun()

	# remove obj from list if object gets removed in LDAP
	if not new and dn in changed_objects:
		del changed_objects[dn]
		event_counter += 1

	# add object to list if it is a zarafa user object
	if new and new.get('uid') and not 'zarafa-contact' in new.get('objectClass'):
		if new.get('zarafaAccount', [''])[0] == '1' and not 'zarafa-group' in new.get('objectClass'):
			changed_objects[dn] = new
			event_counter += 1

def postrun():
	"""
	set zarafa options 15 seconds after last sync in a bulk action
	"""

	global changed_objects, event_counter

	univention.debug.debug(univention.debug.LISTENER, univention.debug.PROCESS, 'zarafa: initiating sync')

	listener.setuid(0)
	try:
		# initiate another sync
		subprocess.call(['/usr/sbin/zarafa-admin', '--sync'])
		# do a mass change for all cached objects
		for dn, new in changed_objects.items():
			univention.debug.debug(univention.debug.LISTENER, univention.debug.PROCESS, 'zarafa: updating %s' % dn)
			# set some options for automatic meeting request handling
			for attr, option in [('zarafaMrAccept', '--mr-accept'),
								 ('zarafaMrDeclineConflict', '--mr-decline-conflict'),
								 ('zarafaMrDeclineRecurring', '--mr-decline-recurring'),
								 ]:
				value = 'no'
				if new.get(attr) and ('1' in new.get(attr)):
					value = 'yes'
				cmd = ['/usr/sbin/zarafa-admin', '-u', new['uid'][0], option, value]
				univention.debug.debug(univention.debug.LISTENER, univention.debug.INFO, 'zarafa: calling %s' % str(cmd))
				subprocess.call(cmd)
	finally:
		listener.unsetuid()
		changed_objects = {}
		event_counter = 0
