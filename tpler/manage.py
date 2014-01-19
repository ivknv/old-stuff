#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
from xml.dom import minidom
from manage.dependencies import add, remove
from manage.change_lang import change_lang
from manage.change_name import rename
from manage.change_authors import change_author
from manage.change_description import change_description
from manage.change_version import change_version
from manage.change_date import update_date
import config
name=minidom.parse("project.xml").getElementsByTagName("name")[0].childNodes[0].nodeValue.strip()
full_path=os.path.realpath(__file__)
full_path=full_path[0:full_path.rindex(os.path.sep)]
try:
	arg1 = sys.argv[1].lower()
except IndexError:
	exit(0)
if arg1 in ["rename"]:
	rename(full_path, sys.argv[2])
elif arg1 in ["change_lang", "change_language"]:
	change_lang(full_path, sys.argv[2])
elif arg1 in ["change_authors", "change_auth"]:
	change_author(full_path, sys.argv[2])
elif arg1 in ["change_descr", "change_description"]:
	change_description(full_path , sys.argv[2])
elif arg1 in ["change_ver", "change_version"]:
	change_version(full_path, sys.argv[3])
elif arg1 in ["update_date"]:
	update_date(full_path)
elif arg1 in ["dependencies"]:
	if sys.argv[2].lower() in ["add"]:
		add(full_path, sys.argv[3])
	elif sys.argv[2].lower() in ["remove", "rm"]:
		remove(full_path, sys.argv[3])
elif arg1 in ["compile"]:
	import py_compile, distutils.core

	py_files = os.listdir(full_path)
	for py_file in py_files:
		if py_file.endswith(".py") and py_file not in ["manage.py"]:
			py_compile.compile(full_path+os.path.sep+py_file)
	if os.path.exists(full_path+os.path.sep+"__pycache__"):
		distutils.dir_util.copy_tree(full_path+os.path.sep+"__pycache__", full_path+os.path.sep+"bin")
	else:
		pyc_files = os.listdir(full_path)
		for pyc_file in pyc_files:
			if pyc_file.endswith(".pyc"):
				os.rename(full_path+os.path.sep+pyc_file, full_path+os.path.sep+"bin"+os.path.sep+pyc_file)
	if os.path.exists(full_path+os.path.sep+"bin"+os.path.sep+"config.pyc"):
		os.remove(full_path+os.path.sep+"bin"+os.path.sep+"config.pyc")