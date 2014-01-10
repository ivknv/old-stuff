#!python
# -*- coding: utf-8 -*-
import sys, os
from manage.change_lang import change_lang
from manage.change_name import rename
from manage.change_authors import change_author
from manage.change_description import change_description
from manage.change_version import change_version
from manage.change_date import update_date
name="PythonProject"
full_path="C:\\my98\\pro_\\TestProjects"
try:
	arg1 = sys.argv[1].lower()
except IndexError:
	exit(0)
if arg1 in ["rename"]:
	rename(full_path+"/"+name, sys.argv[2])
elif arg1 in ["change_lang", "change_language"]:
	change_lang(full_path+"/"+name, sys.argv[2])
elif arg1 in ["change_authors", "change_auth"]:
	change_author(full_path+"/"+name, sys.argv[2])
elif arg1 in ["change_descr", "change_description"]:
	change_description(full_path+"/"+name , sys.argv[2])
elif arg1 in ["change_ver", "change_version"]:
	change_version(full_path+"/"+name, sys.argv[3])
elif arg1 in ["update_date"]:
	update_date(full_path+"/"+name)
elif arg1 in ["compile"]:
	import py_compile, distutils.core
	directory=full_path+"/"+name+"/"+name

	py_files = os.listdir(directory)
	for py_file in py_files:
		if py_file.endswith(".py"):
			py_compile.compile(directory+"/"+py_file)
	distutils.dir_util.copy_tree(directory+"/__pycache__", full_path+"/"+name+"/bin")