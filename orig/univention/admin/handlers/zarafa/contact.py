#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# Copyright 2013-2016 Univention GmbH
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

translation = univention.admin.localization.translation('zarafa4ucs')
_ = translation.translate

module = 'zarafa/contact'
childs = 0
short_description = _(u'Zarafa Contact')
long_description = _(u'Management of Zarafa Contact accounts.')
operations = ['add', 'edit', 'remove', 'search', 'move']
default_containers=["cn=contacts,cn=zarafa"]

options = {}

property_descriptions = {
	'zarafaAccount': univention.admin.property(
		short_description = _(u'Recognized by Zarafa'),
		long_description = _(u'If set to 1, the account is recognized by zarafa'),
		syntax = univention.admin.syntax.string,
		multivalue = False,
		options = [],
		required = True,
		may_change = True,
		identifies = False,
		default = '1',
	),
	'firstname': univention.admin.property(
		short_description=_('First name'),
		long_description='',
		syntax=univention.admin.syntax.TwoThirdsString,
		multivalue=0,
		include_in_default_search=1,
		options=[],
		required=0,
		may_change=1,
		identifies=0
	),
	'lastname': univention.admin.property(
		short_description=_('Last name'),
		long_description='',
		syntax=univention.admin.syntax.string,
		multivalue=0,
		include_in_default_search=1,
		required=1,
		may_change=1,
		identifies=0
	),
	'displayName': univention.admin.property(
		short_description=_('Display name'),
		long_description='',
		syntax=univention.admin.syntax.string,
		options=[],
		multivalue=0,
		required=1,
		may_change=1,
		default = '<firstname> <lastname><:strip>',
		identifies=0
	),
	'title': univention.admin.property(
		short_description=_('Title'),
		long_description='',
		syntax=univention.admin.syntax.OneThirdString,
		multivalue=0,
		options=[],
		required=0,
		may_change=1,
		identifies=0
	),
	'organisation': univention.admin.property(
		short_description=_('Organisation'),
		long_description='',
		syntax=univention.admin.syntax.string64,
		multivalue=0,
		options=[],
		required=0,
		may_change=1,
		identifies=0
	),
	'street': univention.admin.property(
		short_description=_('Street'),
		long_description='',
		syntax=univention.admin.syntax.string,
		multivalue=0,
		options=[],
		required=0,
		may_change=1,
		identifies=0
	),
	'e-mail': univention.admin.property(
		short_description=_('E-mail address'),
		long_description='',
		syntax=univention.admin.syntax.emailAddress,
		multivalue=0,
		include_in_default_search=1,
		required=0,
		dontsearch=0,
		may_change=1,
		identifies=0,
	),
	'postcode': univention.admin.property(
		short_description=_('Postal code'),
		long_description='',
		syntax=univention.admin.syntax.OneThirdString,
		multivalue=0,
		options=[],
		required=0,
		may_change=1,
		identifies=0
	),
	'city': univention.admin.property(
		short_description=_('City'),
		long_description='',
		syntax=univention.admin.syntax.TwoThirdsString,
		multivalue=0,
		options=[],
		required=0,
		may_change=1,
		identifies=0
	),
	'phone': univention.admin.property(
		short_description=_('Telephone number'),
		long_description='',
		syntax=univention.admin.syntax.phone,
		multivalue=0,
		options=[],
		required=0,
		may_change=1,
		identifies=0
	),
	'mobileTelephoneNumber': univention.admin.property(
		short_description=_('Mobile phone number'),
		long_description='',
		syntax=univention.admin.syntax.phone,
		multivalue=0,
		options=[],
		required=0,
		may_change=1,
		identifies=0
	),
	'pagerTelephoneNumber': univention.admin.property(
		short_description=_('Pager telephone number'),
		long_description='',
		syntax=univention.admin.syntax.phone,
		multivalue=0,
		options=[],
		required=0,
		may_change=1,
		identifies=0
	),
	'homeTelephoneNumber': univention.admin.property(
		short_description=_('Private telephone number'),
		long_description='',
		syntax=univention.admin.syntax.phone,
		multivalue=0,
		options=[],
		required=0,
		may_change=1,
		identifies=0
	),
	'roomNumber': univention.admin.property(
		short_description=_('Room number'),
		long_description='',
		syntax=univention.admin.syntax.OneThirdString,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0
	),
	'departmentNumber': univention.admin.property(
		short_description=_('Department number'),
		long_description='',
		syntax=univention.admin.syntax.OneThirdString,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0
	),
	'zarafaHidden': univention.admin.property(
		short_description=_('Hide entry from Zarafa addressbook'),
		long_description=_('Hide this entry from the global Zarafa addressbook'),
		syntax=univention.admin.syntax.boolean,
		default=False,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0
	),
}

layout = [
	Tab(_(u'General'), _(u'Zarafa Contact'), layout=[
		Group( _( 'General Contact information' ), layout = [
			[ 'zarafaHidden', ],
			[ 'title', 'firstname', 'lastname'],
			[ 'displayName', ],
			[ 'phone', ],
			[ 'e-mail', ],
		]),
		Group( _( 'Further Contact information' ), layout = [
			[ 'organisation', 'roomNumber', 'departmentNumber', ], 
			[ 'street', 'postcode', 'city', ],
			[ 'mobileTelephoneNumber', ],
			[ 'homeTelephoneNumber', ], 
			[ 'pagerTelephoneNumber', ],
		]),
	]),
]

mapping = univention.admin.mapping.mapping()
mapping.register('zarafaAccount', 'zarafaAccount', None, univention.admin.mapping.ListToString)
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
mapping.register('zarafaHidden', 'zarafaHidden', None, univention.admin.mapping.ListToString)

class object(univention.admin.handlers.simpleLdap):
	module = module

	def __init__(self, co, lo, position, dn='', superordinate=None, attributes=None):
		self.co = co
		self.lo = lo
		self.dn = dn
		self.position = position
		self.mapping = mapping
		self.descriptions = property_descriptions
		univention.admin.handlers.simpleLdap.__init__(self, co, lo, position, dn, superordinate)
		self.options = []

	def open(self):
		univention.admin.handlers.simpleLdap.open(self)
		self.save()

	def _ldap_pre_create(self):
		self.dn = '%s=%s,%s' % (mapping.mapName('displayName'), mapping.mapValue('displayName', self.info['displayName']), self.position.getDn())

	def _ldap_post_create(self):
		pass

	def _ldap_pre_modify(self):
		pass

	def _ldap_post_modify(self):
		pass

	def _ldap_pre_remove(self):
		pass

	def _ldap_post_remove(self):
		pass

	def _update_policies(self):
		pass

	def _ldap_addlist(self):
		return [('objectClass', ['top', 'zarafa-contact', 'person', 'inetOrgPerson', 'univentionObject', 'zarafa4ucsObject']),('univentionObjectFlag', ['functional'])]

def lookup(co, lo, filter_s, base='', superordinate=None, scope='sub', unique=0, required=0, timeout=-1, sizelimit=0):
	searchfilter = univention.admin.filter.conjunction('&', [
				univention.admin.filter.expression('objectClass', 'zarafa-contact'),
				univention.admin.filter.expression('univentionObjectFlag', 'functional')
				])

	if filter_s:
		filter_p = univention.admin.filter.parse(filter_s)
		univention.admin.filter.walk(filter_p, univention.admin.mapping.mapRewrite, arg=mapping)
		searchfilter.expressions.append(filter_p)

	res = []
	for dn in lo.searchDn(unicode(searchfilter), base, scope, unique, required, timeout, sizelimit):
		res.append(object(co, lo, None, dn))
	return res

def identify(distinguished_name, attributes, canonical=False):
	return 'zarafa-contact' in attributes.get('objectClass', []) and 'functional' in attributes.get('univentionObjectFlag', [])
