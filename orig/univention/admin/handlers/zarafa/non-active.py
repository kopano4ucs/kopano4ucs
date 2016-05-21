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
import univention.admin.password

import univention.password

translation = univention.admin.localization.translation('zarafa4ucs')
_ = translation.translate

module = 'zarafa/non-active'
childs = 0
short_description = _(u'Zarafa non-active and shared store account')
long_description = _(u'Management of Zarafa non-active user accounts, shared stores and resources.')
operations = ['add', 'edit', 'remove', 'search', 'move']
default_containers=["cn=non-active,cn=zarafa"]

options = {}

property_descriptions = {
	'zarafaAccount': univention.admin.property(
		short_description = _(u'Recognized by Zarafa'),
		long_description = _(u'If set to 1, the account is synced to Zarafa'),
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
		required=0,
		may_change=1,
		identifies=0,
		default=' '
	),
	'displayName': univention.admin.property(
		short_description=_('Display name'),
		long_description='',
		syntax=univention.admin.syntax.string,
		options=[],
		multivalue=0,
		required=0,
		may_change=1,
		default = '<username><:strip>',
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
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0,
		default=False,
	),
	'mailPrimaryAddress': univention.admin.property(
		short_description=_('E-mail address'),
		long_description='',
		syntax=univention.admin.syntax.primaryEmailAddressValidDomain,
		multivalue=0,
		include_in_default_search=1,
		required=1,
		dontsearch=0,
		may_change=1,
		identifies=0,
	),
	'mailAlternativeAddress': univention.admin.property(
		short_description=_('Alternative E-mail address'),
		long_description='',
		syntax=univention.admin.syntax.emailAddressValidDomain,
		multivalue=1,
		include_in_default_search=1,
		required=0,
		dontsearch=0,
		may_change=1,
		identifies=0,
	),
	'logindenied': univention.admin.property(
		short_description=_('Deny zarafa login for this account. Login is only required for configuration. If not denied, this account counts against the total zarafa user count'),
		long_description='',
		syntax=univention.admin.syntax.boolean,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0,
		default='1',
	),
	'username': univention.admin.property(
		short_description=_('User name'),
		long_description='',
		syntax=univention.admin.syntax.uid_umlauts,
		multivalue=0,
		include_in_default_search=1,
		required=1,
		may_change=1,
		identifies=1
	),
	'password': univention.admin.property(
		short_description=_('Password'),
		long_description='',
		syntax=univention.admin.syntax.userPasswd,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0,
		dontsearch=1
	),
	# zarafa attributes start here
	'SendAsPrivilege': univention.admin.property(
		short_description=_('Delegates'),
		long_description=_('List of users that may send emails with the identity of the current account'),
		syntax=univention.admin.syntax.zarafa4ucsSendAsPrivilege,
		multivalue=1,
		required=0,
		may_change=1,
		identifies=0,
	),
	'MRaccept': univention.admin.property(
		short_description=_('Auto accept meeting requests'),
		long_description=_('Accept meeting request (ressource) automatically'),
		syntax=univention.admin.syntax.boolean,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0,
		default=False
	),
	'MRDeclineConflictingTimes': univention.admin.property(
		short_description=_('Auto decline meetings requests with conflicting times'),
		long_description=_('Decline meeting requests with conflicting times (ressource) automatically'),
		syntax=univention.admin.syntax.boolean,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0,
		default=False
	),
	'MRDeclineRecurringItems': univention.admin.property(
		short_description=_('Auto decline recurring meeting requests'),
		long_description=_('Decline recurring items (ressource) automatically'),
		syntax=univention.admin.syntax.boolean,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0,
		default=False
	),
	'quotaOverride': univention.admin.property(
		short_description=_('Override global quota settings'),
		long_description=_('Override global quota settings with users warning, soft and hard quota size'),
		syntax=univention.admin.syntax.boolean,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0,
		default=False
	),
	'quotaWarn': univention.admin.property(
		short_description=_('Warning quota size in MB'),
		long_description=_('Warning quota size in MB'),
		syntax=univention.admin.syntax.integer,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0,
	),
	'quotaSoft': univention.admin.property(
		short_description=_('Soft quota size in MB'),
		long_description=_('Soft quota size in MB'),
		syntax=univention.admin.syntax.integer,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0,
	),
	'quotaHard': univention.admin.property(
		short_description=_('Hard quota size in MB'),
		long_description=_('Hard quota size in MB'),
		syntax=univention.admin.syntax.integer,
		multivalue=0,
		required=0,
		may_change=1,
		identifies=0,
	),
}

layout = [
	Tab(_(u'General'), _(u'Zarafa non-active account'), layout=[
		Group( _('Zarafa account settings'), layout = [
			[ 'logindenied', ],
			[ 'username', 'mailPrimaryAddress', ],
			[ 'password', ],
			[ 'mailAlternativeAddress', ],
			[ 'SendAsPrivilege', ],
			[ 'MRaccept', ],
			[ 'MRDeclineConflictingTimes', ],
			[ 'MRDeclineRecurringItems', ],
			[ 'quotaOverride', ],
			[ 'quotaWarn', ],
			[ 'quotaSoft', ],
			[ 'quotaHard', ],
		]),
	]),
	Tab(_(u'Contact information'), _(u'Zarafa non-active account'), layout=[
		Group( _( 'General Contact information' ), layout = [
			[ 'zarafaHidden', ],
			[ 'title', 'firstname', 'lastname'],
			[ 'displayName', ],
			[ 'phone', ],
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
mapping.register('mailPrimaryAddress', 'mailPrimaryAddress', None, univention.admin.mapping.ListToLowerString)
mapping.register('mailAlternativeAddress', 'mailAlternativeAddress', None, None)
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

mapping.register('logindenied', 'zarafaSharedStoreOnly', None, univention.admin.mapping.ListToString)
mapping.register('username', 'uid', None, univention.admin.mapping.ListToString)
mapping.register('SendAsPrivilege', 'zarafaSendAsPrivilege')
mapping.register('MRaccept', 'zarafaMrAccept', None, univention.admin.mapping.ListToString)
mapping.register('MRDeclineConflictingTimes', 'zarafaMrDeclineConflict', None, univention.admin.mapping.ListToString)
mapping.register('MRDeclineRecurringItems', 'zarafaMrDeclineRecurring', None, univention.admin.mapping.ListToString)
mapping.register('quotaOverride', 'zarafaQuotaOverride', None, univention.admin.mapping.ListToString)
mapping.register('quotaWarn', 'zarafaQuotaWarn', None, univention.admin.mapping.ListToString)
mapping.register('quotaSoft', 'zarafaQuotaSoft', None, univention.admin.mapping.ListToString)
mapping.register('quotaHard', 'zarafaQuotaHard', None, univention.admin.mapping.ListToString)

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
		self.allocation_locks = []

	def cancel(self):
		for type, value in self.allocation_locks:
			univention.admin.allocators.release(self.lo, self.position, type, value)
	def open(self):
		univention.admin.handlers.simpleLdap.open(self)
		self.save()

	def _ldap_pre_create(self):
		self.dn = '%s=%s,%s' % (mapping.mapName('username'), mapping.mapValue('username', self.info['username']), self.position.getDn())

	def _ldap_post_create(self):
		if self[ 'mailPrimaryAddress' ]:
			univention.admin.allocators.confirm( self.lo, self.position, 'mailPrimaryAddress', self[ 'mailPrimaryAddress' ] )
		univention.admin.allocators.confirm(self.lo, self.position, 'uid', self['username'])

	def _ldap_pre_modify(self):
		if self.hasChanged('mailPrimaryAddress'):
			if self['mailPrimaryAddress']:
				self['mailPrimaryAddress']=self['mailPrimaryAddress'].lower()

		if self.hasChanged('username'):
			try:
				univention.admin.allocators.request(self.lo, self.position, 'uid', value=self['username'])
			except univention.admin.uexceptions.noLock, e:
				username=self['username']
				del(self.info['username'])
				self.oldinfo={}
				self.dn=None
				self._exists=0
				self.old_username = username
				univention.admin.allocators.release(self.lo, self.position, 'uid', username)
				raise univention.admin.uexceptions.uidAlreadyUsed, ': %s' % username


	def _ldap_post_modify(self):
		if self.hasChanged( 'mailPrimaryAddress' ):
			if self[ 'mailPrimaryAddress' ]:
				univention.admin.allocators.confirm( self.lo, self.position, 'mailPrimaryAddress', self[ 'mailPrimaryAddress' ] )
			else:
				univention.admin.allocators.release( self.lo, self.position, 'mailPrimaryAddress', self.oldinfo[ 'mailPrimaryAddress' ] )

	def _ldap_pre_remove(self):
		pass

	def _ldap_post_remove(self):
		univention.admin.allocators.release(self.lo, self.position, 'mailPrimaryAddress', self[ 'mailPrimaryAddress' ] ) 
		univention.admin.allocators.release(self.lo, self.position, 'uid', self['username'])

	def _update_policies(self):
		pass

	def _ldap_addlist(self):
		# Try to set username
		try:    
			uid=univention.admin.allocators.request(self.lo, self.position, 'uid', value=self['username'])
			self.allocation_locks.append(('uid', uid))
		except univention.admin.uexceptions.noLock:
			username=self['username']
			del(self.info['username'])
			self.oldinfo={}
			self.dn=None
			self._exists=0
			self.old_username = username
			univention.admin.allocators.release(self.lo, self.position, 'uid', username)
			raise univention.admin.uexceptions.uidAlreadyUsed, ': %s' % username	

		al = [('uid', [uid])]

		# check if mailprimaryaddress is not in use
		if self[ 'mailPrimaryAddress' ]:
			try:
				univention.admin.allocators.request( self.lo, self.position, 'mailPrimaryAddress', value = self[ 'mailPrimaryAddress' ] )
				self.allocation_locks.append( ( 'mailPrimaryAddress', self[ 'mailPrimaryAddress' ] ) )
			except univention.admin.uexceptions.noLock:
				self.cancel()
				raise univention.admin.uexceptions.mailAddressUsed

		al.append(('univentionObjectFlag', ['functional']))

		ocs = ('objectClass', ['top', 'zarafa-user', 'person', 'inetOrgPerson', 'univentionObject', 'zarafa4ucsObject', 'univentionMail'])
		al.insert(0, ocs)

		return al

	def _ldap_modlist(self):
		ml=univention.admin.handlers.simpleLdap._ldap_modlist(self)
		if self.hasChanged('password'):
			pwdCheck = univention.password.Check(self.lo)
			pwdCheck.enableQualityCheck = True
			try:
				pwdCheck.check(self['password'])
			except ValueError, e:
				raise univention.admin.uexceptions.pwQuality, str(e).replace('W?rterbucheintrag','Wörterbucheintrag').replace('enth?lt', 'enthält')

			password_crypt = "{crypt}%s" % univention.admin.password.crypt(self['password'])
			ml.append(('userPassword', self.oldattr.get('userPassword', [''])[0], password_crypt))

		if self.hasChanged('mailPrimaryAddress') and self['mailPrimaryAddress']:
			for type, value in self.allocation_locks:
				if type == 'mailPrimaryAddress': break
			else:           
				try:    
					univention.admin.allocators.request( self.lo, self.position, 'mailPrimaryAddress', value = self[ 'mailPrimaryAddress' ] )
					self.allocation_locks.append( ( 'mailPrimaryAddress', self[ 'mailPrimaryAddress' ] ) )
				except univention.admin.uexceptions.noLock:
					self.cancel()
					raise univention.admin.uexceptions.mailAddressUsed

		return ml

def lookup(co, lo, filter_s, base='', superordinate=None, scope='sub', unique=0, required=0, timeout=-1, sizelimit=0):
	searchfilter = univention.admin.filter.conjunction('&', [
				univention.admin.filter.expression('objectClass', 'zarafa-user'),
				univention.admin.filter.expression('objectClass', 'zarafa4ucsObject'),
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
	return 'zarafa-user' in attributes.get('objectClass', []) and 'zarafa4ucsObject' in attributes.get('objectClass', [])
