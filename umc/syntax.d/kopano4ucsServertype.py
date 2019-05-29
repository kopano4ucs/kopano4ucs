# kopano4ucsRole UDM syntax
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

import univention.admin.localization
import univention.admin.syntax

translation = univention.admin.localization.translation('kopano4ucs')
_ = translation.translate

class kopano4ucsServertype (select):
    choices=[
        ('none', _('None')),
        ('home', _('Kopano Home Server')),
        ('archive', _('Kopano Archive Server')),
        ('homearchive', _('Kopano Home and Archive Server')),
    ]

