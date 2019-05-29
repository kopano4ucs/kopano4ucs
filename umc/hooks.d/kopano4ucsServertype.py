# kopano4ucsRole UDM hook
#
# Copyright 2018-2019 linudata GmbH
#
# https://linudata.de
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

translation = univention.admin.localization.translation('kopano4ucs')
_ = translation.translate


class kopano4ucsServertype (simpleHook):
    type = 'kopano4ucsServertype'

    def __kopanoServertype(self, module, servertype):
        univention.debug.debug(univention.debug.ADMIN, univention.debug.INFO,
                                   'kopano4ucsServertype: called %s' % module["kopano-servertype"])        
        # if role has changed
        if module.hasChanged("kopano-servertype"):
            univention.debug.debug(univention.debug.ADMIN, univention.debug.INFO,
                                       'kopano4ucsServertype: original servertype %d' % servertype)

            if module["kopano-servertype"] == "none":
                servertype = 0
            if module["kopano-servertype"] == "home":
                servertype = 1
            elif module["kopano-servertype"] == "archive":
                servertype = 2
            elif module["kopano-servertype"] == "homearchive":
                servertype = 3
            else:
                servertype = 0

            # Muesste man jetzt die Accounts durchgehen und pruefen,
            # wo die Server alle noch in Verwendund sind?
            # Vielleicht wenigstens im Log als Warning ausgeben?


        else:
            univention.debug.debug(univention.debug.ADMIN, univention.debug.INFO,
                                       'kopano4ucsServertype: not changed')

        return servertype
    

    def hook_ldap_post_modify(self, module):
        pass

    def hook_open(self, module):
        pass

    def hook_ldap_pre_create(self, module):
        pass

    def hook_ldap_post_create(self, module):
        pass

    def hook_ldap_pre_modify(self, module):
        pass

    def hook_ldap_modlist(self, module, servertype):
        ucr.load()
        return servertype

    def hook_ldap_pre_remove(self, module):
        pass

    def hook_ldap_post_remove(self, module):
        pass


    
