# zarafa4ucsRole UDM hook
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

from univention.admin.hook import simpleHook
from univention.admin.localization import translation
from univention.config_registry import ConfigRegistry
ucr = ConfigRegistry()

translation = univention.admin.localization.translation('zarafa4ucs')
_ = translation.translate


class zarafa4ucsRole(simpleHook):

	type = 'zarafa4ucsRole'

	def __isUsersUser(self, module):
		return 'username' in module.descriptions

	def __zarafaRoles(self, module, ml):
		# if role has changed and module is not "settings/usertemplate"
		if self.__isUsersUser(module) and module.hasChanged("zarafa-role"):

			univention.debug.debug(univention.debug.ADMIN, univention.debug.INFO,
				'zarafa4ucsRole: role has changed %s' % module["zarafa-role"])

			univention.debug.debug(univention.debug.ADMIN, univention.debug.INFO,
				'zarafa4ucsRole: original modlist %s' % ml)

			univention.debug.debug(univention.debug.ADMIN, univention.debug.INFO,
				'zarafa4ucsRole: oldattr %s' % module.oldattr)

			zarafaAccount = 0
			zarafaAdmin = 0
			zarafaSharedStoreOnly = 0
			zarafaContact = 0

			if module["zarafa-role"] == "user":
				zarafaAccount = 1
			elif module["zarafa-role"] == "admin":
				zarafaAccount = 1
				zarafaAdmin = 1
			elif module["zarafa-role"] == "store":
				zarafaSharedStoreOnly = 1
				zarafaAccount = 1
			elif module["zarafa-role"] == "contact":
				zarafaContact = 1
				zarafaAccount = 1
			else:
				pass

			# add/remove zarafa role
			ml.append((
				"zarafaAccount",
				module.oldattr.get("zarafaAccount", [""])[0],
				"%s" % zarafaAccount))
			ml.append((
				"zarafaAdmin",
				module.oldattr.get("zarafaAdmin", [""])[0],
				"%s" % zarafaAdmin))
			ml.append((
				"zarafaSharedStoreOnly",
				module.oldattr.get("zarafaSharedStoreOnly", [""])[0],
				"%s" % zarafaSharedStoreOnly))

			# add/remove objectClass zarafa-contact
			if zarafaContact:
				if not "zarafa-contact" in module.oldattr.get("objectClass", []):
					ml.append(("objectClass", "", "zarafa-contact"))
			else:
				if "zarafa-contact" in module.oldattr.get("objectClass", []):
					ml.append(("objectClass", "zarafa-contact", ""))

			univention.debug.debug(univention.debug.ADMIN, univention.debug.INFO,
				'zarafa4ucsRole: changed modlist %s' % ml)

		return ml

	def hook_ldap_post_modify(self, module):
		pass

	def hook_open(self, module):
		pass

	def hook_ldap_pre_create(self, module):
		if "mailPrimaryAddress" in module and not module.get("mailPrimaryAddress"):
			module["zarafa-role"] = "none"

		if "mailPrimaryAddress" in module and module.get("mailPrimaryAddress") and module["zarafa-role"] == "none":
			module["zarafa-role"] = "user"
		pass

	def hook_ldap_addlist(self, module, al=[]):
		al = self.__zarafaRoles(module, al)
		return al

	def hook_ldap_post_create(self, module):
		pass

	def hook_ldap_pre_modify(self, module):
		# zarafa-role not 'none' and no mailPrimaryAddress specified
		if "mailPrimaryAddress" in module and not module.get("mailPrimaryAddress") and module["zarafa-role"] and not module["zarafa-role"] in ["none", "contact"]:
			raise univention.admin.uexceptions.valueError, _("Zarafa users must have a primary e-mail address specified.")
		pass

	def hook_ldap_modlist(self, module, ml=[]):
		ucr.load()
		univention.debug.debug(univention.debug.ADMIN, univention.debug.INFO, "hook_ldap_modlist: ml: %s" % ml)

		# email address added, but zarafa-role unchanged and "none": user probably wants that user to be a zarafa-user
		if module.hasChanged('mailPrimaryAddress') and not module.oldattr.get("mailPrimaryAddress", [""])[0] and not module.hasChanged('zarafa-role') and module.get("zarafa-role") == "none" and ucr.is_true('zarafa/createzarafauserswithvalidemail', True):
			module["zarafa-role"] = "user"
			ml.append(("zarafa4ucsRole", "none", "user"))

		# set zarafa role flags
		ml = self.__zarafaRoles(module, ml)

		univention.debug.debug(univention.debug.ADMIN, univention.debug.INFO, "hook_ldap_modlist: ml after modification: %s" % ml)
		return ml

	def hook_ldap_pre_remove(self, module):
		pass

	def hook_ldap_post_remove(self, module):
		pass
