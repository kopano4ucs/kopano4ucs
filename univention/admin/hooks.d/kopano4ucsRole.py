# kopano4ucsRole UDM hook
#
# Copyright 2012-2019 Univention GmbH
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

import univention.debug as ud

import univention.admin.uexceptions
from univention.admin.hook import simpleHook
from univention.admin.localization import translation
from univention.config_registry import ConfigRegistry

ucr = ConfigRegistry()

translation = translation('univention-admin-handlers-kopano-contact')
_ = translation.translate


class kopano4ucsRole(simpleHook):

	type = 'kopano4ucsRole'

	def __isUsersUser(self, module):
		return 'username' in module.descriptions  # FIXME: this check is wrong and also detects since UCS 4.3 user/contact objects

	def __kopanoRoles(self, module, ml):
		# if role has changed and module is not "settings/usertemplate"
		if self.__isUsersUser(module) and module.hasChanged("kopano-role"):
			ud.debug(ud.ADMIN, ud.INFO, 'kopano4ucsRole: role has changed %r' % (module["kopano-role"],))
			ud.debug(ud.ADMIN, ud.INFO, 'kopano4ucsRole: original modlist %r' % (ml,))  # FIXME: this logs password hashes!
			ud.debug(ud.ADMIN, ud.INFO, 'kopano4ucsRole: oldattr %r' % (module.oldattr,))  # FIXME: this logs password hashes!

			kopanoAccount = 0
			kopanoAdmin = 0
			kopanoSharedStoreOnly = 0
			kopanoContact = 0

			if module["kopano-role"] == "user":
				kopanoAccount = 1
			elif module["kopano-role"] == "admin":
				kopanoAccount = 1
				kopanoAdmin = 1
			elif module["kopano-role"] == "super":
				kopanoAccount = 1
				kopanoAdmin = 2
			elif module["kopano-role"] == "store":
				kopanoSharedStoreOnly = 1
				kopanoAccount = 1
			elif module["kopano-role"] == "contact":
				kopanoContact = 1
				kopanoAccount = 1

			# add/remove kopano role
			ml.append((
				"kopanoAccount",
				module.oldattr.get("kopanoAccount", [b""])[0],
				b"%d" % kopanoAccount))
			ml.append((
				"kopanoAdmin",
				module.oldattr.get("kopanoAdmin", [b""])[0],
				b"%d" % kopanoAdmin))
			ml.append((
				"kopanoSharedStoreOnly",
				module.oldattr.get("kopanoSharedStoreOnly", [b""])[0],
				b"%d" % kopanoSharedStoreOnly))

			# add/remove objectClass kopano-contact
			if kopanoContact:
				if "kopano-contact" not in module.oldattr.get("objectClass", []):
					ml.append(("objectClass", b"", b"kopano-contact"))
			else:
				if "kopano-contact" in module.oldattr.get("objectClass", []):
					ml.append(("objectClass", b"kopano-contact", b""))

			ud.debug(ud.ADMIN, ud.INFO, 'kopano4ucsRole: changed modlist %r' % (ml,))  # FIXME: this logs password hashes

		return ml

	def hook_ldap_pre_create(self, module):
		if "mailPrimaryAddress" in module and not module.get("mailPrimaryAddress"):
			module["kopano-role"] = "none"

		if "mailPrimaryAddress" in module and module.get("mailPrimaryAddress") and module["kopano-role"] == "none":
			module["kopano-role"] = "user"

	def hook_ldap_addlist(self, module, al=[]):
		al = self.__kopanoRoles(module, al)
		return al

	def hook_ldap_pre_modify(self, module):
		# kopano-role not 'none' and no mailPrimaryAddress specified
		if "mailPrimaryAddress" in module and not module.get("mailPrimaryAddress") and module["kopano-role"] and module["kopano-role"] not in ("none", "contact"):
			raise univention.admin.uexceptions.valueError(_("Kopano users must have a primary e-mail address specified."))

	def hook_ldap_modlist(self, module, ml=[]):
		ucr.load()
		ud.debug(ud.ADMIN, ud.INFO, "hook_ldap_modlist: ml: %r" % (ml,))  # FIXME: logs password hashes

		# email address added, but kopano-role unchanged and "none": user probably wants that user to be a kopano-user
		if module.hasChanged('mailPrimaryAddress') and not module.oldattr.get("mailPrimaryAddress", [b""])[0] and not module.hasChanged('kopano-role') and module.get("kopano-role") == "none" and ucr.is_true('kopano/createkopanouserswithvalidemail', True):
			module["kopano-role"] = "user"
			ml.append(("kopano4ucsRole", b"none", b"user"))

		# set kopano role flags
		ml = self.__kopanoRoles(module, ml)

		ud.debug(ud.ADMIN, ud.INFO, "hook_ldap_modlist: ml after modification: %s" % (ml,))  # FIXME: logs password hashes
		return ml
