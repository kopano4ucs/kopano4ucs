#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# Copyright 2013-2019 Univention GmbH
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

from univention.admin.layout import Tab, Group
import univention.admin.filter
import univention.admin.handlers
import univention.admin.syntax

translation = univention.admin.localization.translation('univention-admin-handlers-kopano-contact')
_ = translation.translate

module = 'kopano/contact'
childs = 0
short_description = _('Kopano Contact')
long_description = _('Management of Kopano Contact accounts.')
operations = ['add', 'edit', 'remove', 'search', 'move']
default_containers = ["cn=contacts,cn=kopano"]

options = {}

property_descriptions = {
	'kopanoAccount': univention.admin.property(
		short_description=_('Recognized by Kopano'),
		long_description=_('If set to 1, the account is recognized by kopano'),
		syntax=univention.admin.syntax.string,
		required=True,
		default='1',
	),
	'firstname': univention.admin.property(
		short_description=_('First name'),
		long_description='',
		syntax=univention.admin.syntax.TwoThirdsString,
		include_in_default_search=True,
	),
	'lastname': univention.admin.property(
		short_description=_('Last name'),
		long_description='',
		syntax=univention.admin.syntax.string,
		include_in_default_search=True,
		required=True,
	),
	'displayName': univention.admin.property(
		short_description=_('Display name'),
		long_description='',
		syntax=univention.admin.syntax.string,
		required=True,
		default='<firstname> <lastname><:strip>',
		identifies=True
	),
	'title': univention.admin.property(
		short_description=_('Title'),
		long_description='',
		syntax=univention.admin.syntax.OneThirdString,
	),
	'organisation': univention.admin.property(
		short_description=_('Organisation'),
		long_description='',
		syntax=univention.admin.syntax.string64,
	),
	'street': univention.admin.property(
		short_description=_('Street'),
		long_description='',
		syntax=univention.admin.syntax.string,
	),
	'e-mail': univention.admin.property(
		short_description=_('E-mail address'),
		long_description='',
		syntax=univention.admin.syntax.emailAddress,
		include_in_default_search=True,
	),
	'postcode': univention.admin.property(
		short_description=_('Postal code'),
		long_description='',
		syntax=univention.admin.syntax.OneThirdString,
	),
	'city': univention.admin.property(
		short_description=_('City'),
		long_description='',
		syntax=univention.admin.syntax.TwoThirdsString,
	),
	'phone': univention.admin.property(
		short_description=_('Telephone number'),
		long_description='',
		syntax=univention.admin.syntax.phone,
	),
	'mobileTelephoneNumber': univention.admin.property(
		short_description=_('Mobile phone number'),
		long_description='',
		syntax=univention.admin.syntax.phone,
	),
	'pagerTelephoneNumber': univention.admin.property(
		short_description=_('Pager telephone number'),
		long_description='',
		syntax=univention.admin.syntax.phone,
	),
	'homeTelephoneNumber': univention.admin.property(
		short_description=_('Private telephone number'),
		long_description='',
		syntax=univention.admin.syntax.phone,
	),
	'roomNumber': univention.admin.property(
		short_description=_('Room number'),
		long_description='',
		syntax=univention.admin.syntax.OneThirdString,
	),
	'departmentNumber': univention.admin.property(
		short_description=_('Department number'),
		long_description='',
		syntax=univention.admin.syntax.OneThirdString,
	),
	'kopanoHidden': univention.admin.property(
		short_description=_('Hide entry from Kopano addressbook'),
		long_description=_('Hide this entry from the global Kopano addressbook'),
		syntax=univention.admin.syntax.boolean,
		default=False,
	),
}

layout = [
	Tab(_('General'), _('Kopano Contact'), layout=[
		Group(_('General Contact information'), layout=[
			['kopanoHidden', ],
			['title', 'firstname', 'lastname'],
			['displayName', ],
			['phone', ],
			['e-mail', ],
		]),
		Group(_('Further Contact information'), layout=[
			['organisation', 'roomNumber', 'departmentNumber', ],
			['street', 'postcode', 'city', ],
			['mobileTelephoneNumber', ],
			['homeTelephoneNumber', ],
			['pagerTelephoneNumber', ],
		]),
	]),
]

mapping = univention.admin.mapping.mapping()
mapping.register('kopanoAccount', 'kopanoAccount', None, univention.admin.mapping.ListToString)
mapping.register('title', 'title', None, univention.admin.mapping.ListToString)
mapping.register('firstname', 'givenName', None, univention.admin.mapping.ListToString)
mapping.register('lastname', 'sn', None, univention.admin.mapping.ListToString)
mapping.register('organisation', 'o', None, univention.admin.mapping.ListToString)
mapping.register('street', 'street', None, univention.admin.mapping.ListToString)
mapping.register('e-mail', 'mailPrimaryAddress', None, univention.admin.mapping.ListToLowerString)
mapping.register('postcode', 'postalCode', None, univention.admin.mapping.ListToString)
mapping.register('city', 'l', None, univention.admin.mapping.ListToString)
mapping.register('phone', 'telephoneNumber', None, univention.admin.mapping.ListToString)
mapping.register('mobileTelephoneNumber', 'mobile', None, univention.admin.mapping.ListToString)
mapping.register('pagerTelephoneNumber', 'pager', None, univention.admin.mapping.ListToString)
mapping.register('homeTelephoneNumber', 'homePhone', None, univention.admin.mapping.ListToString)
mapping.register('displayName', 'cn', None, univention.admin.mapping.ListToString)
mapping.register('departmentNumber', 'departmentNumber', None, univention.admin.mapping.ListToString)
mapping.register('roomNumber', 'roomNumber', None, univention.admin.mapping.ListToString)
mapping.register('kopanoHidden', 'kopanoHidden', None, univention.admin.mapping.ListToString)


class object(univention.admin.handlers.simpleLdap):
	module = module

	def _update_policies(self):
		pass  # TODO: is there a reason why this doesn't do the inherited things?

	def _ldap_addlist(self):
		return [('objectClass', ['top', 'kopano-contact', 'person', 'inetOrgPerson', 'univentionObject', 'kopano4ucsObject']), ('univentionObjectFlag', ['functional'])]


def lookup(co, lo, filter_s, base='', superordinate=None, scope='sub', unique=0, required=0, timeout=-1, sizelimit=0):
	searchfilter = univention.admin.filter.conjunction('&', [
		univention.admin.filter.expression('objectClass', 'kopano-contact'),
		univention.admin.filter.expression('univentionObjectFlag', 'functional')
	])

	if filter_s:
		filter_p = univention.admin.filter.parse(filter_s)
		univention.admin.filter.walk(filter_p, univention.admin.mapping.mapRewrite, arg=mapping)
		searchfilter.expressions.append(filter_p)

	res = []
	for dn in lo.searchDn(str(searchfilter), base, scope, unique, required, timeout, sizelimit):
		res.append(object(co, lo, None, dn))
	return res


def identify(distinguished_name, attributes, canonical=False):
	return 'kopano-contact' in attributes.get('objectClass', []) and 'functional' in attributes.get('univentionObjectFlag', [])
