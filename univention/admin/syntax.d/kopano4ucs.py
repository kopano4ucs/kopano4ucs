# kopano4ucsRole UDM syntax
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

import univention.admin.localization
from univention.admin.syntax import select, UDM_Objects

translation = univention.admin.localization.translation('univention-admin-handlers-kopano-contact')
_ = translation.translate


class kopano4ucsRole(select):
	choices = [
		('none', _('None')),
		('user', _('Kopano User')),
		('admin', _('Kopano Admin')),
		('super', _('Kopano Super Admin')),
		('store', _('Kopano Shared Store/Non-active')),
		('contact', _('Kopano Contact')),
	]

class kopano4ucsResource(select):
     choices= [
         ('none', _('None')),
         ('room', _('Kopano Room')),
         ('equipment', _('Kopano Equipment')),
     ]

class kopano4ucsSendAsPrivilege(UDM_Objects):
	udm_modules = ('users/user', )
	key = '%(uidNumber)s'
	label = '%(username)s'
	udm_filter = '(&(kopanoAccount=1)(!(univentionObjectFlag=functional)))'
	simple = True
	regex = None


class kopano4ucsFeature(select):
	choices = [
		('pop3', 'POP3 access'),
		('imap', 'IMAP access'),
		('mobile', 'ActiveSync access'),
		('outlook', 'Outlook over ActiveSync access'),
	]
