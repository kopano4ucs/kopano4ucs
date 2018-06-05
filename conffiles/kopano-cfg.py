# -*- coding: utf-8 -*-
#
# kopano4ucs
#  config registry module to update kopano configuration
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

import os
import re
import subprocess

OPTIONS_CFG = {
		'DIR_CONFIG': '/etc/kopano',
		'FN_SUFFIX': '.cfg',
		'UCR_PREFIX': 'kopano/cfg/',
		'LINEFORMAT': '%s = %s\n',
		'RE_CFGOPTION': '^#?\s*%s\s*='
		}
OPTIONS_PHP = {
		'DIR_CONFIG': '/etc/kopano/webapp',
		'FN_SUFFIX': '.php',
		'UCR_PREFIX': 'kopano/webapp/',
		'LINEFORMAT': 'define("%s",%s);\n',
		'RE_CFGOPTION': '^\s*define\(\"%s\",\s*'
		}
RE_WARNING = re.compile('^# Warning: the value .*? has been set via UCR variable')
MSG_WARNING = '# Warning: the value "%s" has been set via UCR variable "%s"\n'
RE_UCRVAR = re.compile('@%@(.*?)@%@')
RE_FILENAME = re.compile('@&@(.*?)@&@')

KEY = 0
VALUE = 1
REPLACED = 2


def get_line(option, ucrkey, configRegistry, lineformat):
	"""
	this function loads the UCR value for the specified option
	and replaces UCR placeholders with its current value.
	"""
	value = lineformat % (option, configRegistry.get(ucrkey))
	matches = RE_UCRVAR.findall(value)
	for key in matches:
		value = value.replace('@%%@%s@%%@' % key, configRegistry.get(key, ''))
	matches = RE_FILENAME.findall(value)
	for key in matches:
		try:
			content = open(key, 'r').read()
		except IOError, e:
			content = ''
		value = value.replace('@&@%s@&@' % key, content)
	return value


def find_last(list, element):
	for index, el in enumerate(reversed(list)):
		if el.strip() == element:
			return len(list) - 1 - index
	return None


def handler(configRegistry, changes):
	"""
	main handler
	"""
	handle_files_etc_kopano(configRegistry, changes, OPTIONS_CFG)
	handle_files_etc_kopano(configRegistry, changes, OPTIONS_PHP)
	handle_files_etc_default(configRegistry, changes)


def handle_files_etc_kopano(configRegistry, changes, OPTIONS):
	"""
	handle UCR variable changes with prefix ucr_prefix and alter kopano
	config files in DIR_CONFIG if neccessary.
	UCR config option style:  <ucr_prefix>/server/quota_warn=12345
       	                      <-PREFIX-><-FILE-><-Option->=<-Value->
	The UCR variable value may contain UCR placeholders (@%@variable/name@%@).
	The UCR variable value may contain placeholders for files (@&@/etc/fstab@&@).
	"""
	UCR_PREFIX = OPTIONS['UCR_PREFIX']
	DIR_CONFIG = OPTIONS['DIR_CONFIG']
	FN_SUFFIX = OPTIONS['FN_SUFFIX']
	LINEFORMAT = OPTIONS['LINEFORMAT']
	RE_CFGOPTION = OPTIONS['RE_CFGOPTION']

	changed_options = {}
	# check all kopano UCR variables
	for key in [ x for x in configRegistry.keys() if x.startswith(UCR_PREFIX) ]:
		# find UCR placeholder in variable values (==> e.g. @%@ldap/server/name@%@)
		matches = RE_UCRVAR.findall( configRegistry.get(key) )
		# if key is in list of changed UCR variables or
		# the UCR variable value contains a UCR placeholder that is listed in changed UCR variables list then...
		if key in changes or filter(lambda x: x in changes, matches):
			# ...prepare UCR variable and remember filename, key and value
			items = key.split('/')
			if len(items) == 4:
				filename = os.path.join(DIR_CONFIG, '%s%s' % (items[2], FN_SUFFIX))
				if not filename in changed_options:
					changed_options[filename] = {}
				changed_options[filename][items[3]] = [ key, configRegistry.get(key), False ]  # key, value, replaced

	# check for removed UCR variables
	for key in [ x for x in changes.keys() if x.startswith(UCR_PREFIX) and x not in configRegistry ]:
		items = key.split('/')
		if len(items) == 4:
			filename = os.path.join(DIR_CONFIG, '%s%s' % (items[2], FN_SUFFIX))
			if not filename in changed_options:
				changed_options[filename] = {}
			changed_options[filename][items[3]] = [ key, None, False ]  # key, value, replaced

	if changed_options:
		handle_files(configRegistry, changed_options, LINEFORMAT, RE_CFGOPTION)


def handle_files_etc_default(configRegistry, changes):
	"""
	handle UCR variable changes with prefix "kopano/default/" and alter config file /etc/default/kopano.
	UCR config option style:  kopano/default/quota_warn=12345
       	                      <----PREFIX----><-Option->=<-Value->
	The UCR variable value may contain UCR placeholders (@%@variable/name@%@).
	The UCR variable value may contain placeholders for files (@&@/etc/fstab@&@).
	"""

	filename = '/etc/default/kopano'
	changed_options = { filename: {} }

	# check all kopano UCR variables
	for key in [ x for x in configRegistry.keys() if x.startswith('kopano/default/') ]:
		# find UCR placeholder in variable values (==> e.g. @%@ldap/server/name@%@)
		matches = RE_UCRVAR.findall( configRegistry.get(key) )
		# if key is in list of changed UCR variables or
		# the UCR variable value contains a UCR placeholder that is listed in changed UCR variables list then...
		if key in changes or filter(lambda x: x in changes, matches):
			# ...prepare UCR variable and remember filename, key and value
			items = key.split('/')
			if len(items) == 3:
				changed_options[filename][items[2]] = [ key, configRegistry.get(key), False ]  # key, value, replaced

	# check for removed UCR variables
	for key in [ x for x in changes.keys() if x.startswith('kopano/default/') and x not in configRegistry ]:
		items = key.split('/')
		if len(items) == 3:
			changed_options[filename][items[2]] = [ key, None, False ]  # key, value, replaced

	if changed_options:
		handle_files(configRegistry, changed_options, '%s="%s"\n', OPTIONS_CFG['RE_CFGOPTION'])


def handle_files(configRegistry, changed_options, lineformat, RE_CFGOPTION):
	"""
    Update specified files based on data structure "changed_options":

	changed_options = { '/etc/kopano/ldap.cfg': { 'mykey':  [ 'kopano/cfg/ldap/mykey', 'the_value', False ],
												  'thekey': [ 'kopano/cfg/ldap/thekey', 'some_value', False ],
												  },
												  ....
					  }
	"""

	# iterate over all filenames specified in UCR variables
	for fn in changed_options.keys():
		# ignore UCR variable if file does not exist
		if not os.path.exists(fn):
			continue

		# read content of file; on error, print msg and ignore file
		try:
			lines = open(fn, 'r').readlines()
		except IOError, e:
			subprocess.call(['/usr/bin/logger', '-t', 'UCR', 'module kopano-cfg.py: cannot read %s: %s' % (fn, e)])
			continue

		file_changed = False
		# iterate over all files and replace line if matching UCR variable does exist
		i = 0
		while i < len(lines):
			for cfgitem in changed_options[fn]:
				if re.match(RE_CFGOPTION % cfgitem, lines[i]):
					# matching line found...
					# ...mark option as found...
					changed_options[fn][cfgitem][REPLACED] = True

					if changed_options[fn][cfgitem][VALUE] is not None:
						# ...and UCR variable does still exist, so current line will be replaced
						lines[i] = get_line(cfgitem, changed_options[fn][cfgitem][KEY], configRegistry, lineformat)
						# check if warning text is missing...
						if (i == 0) or (i > 0 and not RE_WARNING.match(lines[i-1])):
							lines.insert(i, MSG_WARNING % (cfgitem, changed_options[fn][cfgitem][KEY]))
							i += 1
						file_changed = True
					else:
						# ...and UCR variable has been removed, so warning will be removed
						if (i > 0) and RE_WARNING.match(lines[i-1]):
							del lines[i-1]
							i -= 1
							lines[i] = "#%s" % lines[i]
							file_changed = True
			i += 1

		# check for unmatched options
		for cfgitem in changed_options[fn]:
			if not(changed_options[fn][cfgitem][REPLACED]):
				# add them at the bottom of the file as new entry
				# Check for and handle .cfg files differently than .php files
				if lines and lines[0].startswith("<?php"):
					php_closing_tag_line = find_last(lines, "?>")
					if php_closing_tag_line:
						file_changed = True
						lines.insert(php_closing_tag_line - 1, get_line(cfgitem, changed_options[fn][cfgitem][KEY], configRegistry, lineformat))
						lines.insert(php_closing_tag_line - 1, MSG_WARNING % (cfgitem, changed_options[fn][cfgitem][KEY]))
						lines.insert(php_closing_tag_line - 1, '\n')
					else:
						print "Error: no closing php tag found in %s, ucr option not added" % fn
				else:
					file_changed = True
					lines.extend( [ '\n',
								MSG_WARNING % (cfgitem, changed_options[fn][cfgitem][KEY]),
								get_line(cfgitem, changed_options[fn][cfgitem][KEY], configRegistry, lineformat),
								] )

		# update file only if changes have been made
		if file_changed:
			new_fn = '%s.NEW' % fn
			try:
				# write to temporary file and perform an atomic rename
				old_mode = os.stat(fn)
				fd = open(new_fn, 'w', old_mode.st_mode)
				# force old permissions
				os.chmod(new_fn, old_mode.st_mode)
				os.chown(new_fn, old_mode.st_uid, old_mode.st_gid)
				fd.write(''.join(lines))
				fd.close()
				os.rename(new_fn, fn)
			# except IOError, e:
			except Exception, e:
				subprocess.call(['/usr/bin/logger', '-t', 'UCR', 'module kopano-cfg.py: cannot write %s: %s' % (fn, e)])
