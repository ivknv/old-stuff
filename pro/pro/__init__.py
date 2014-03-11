#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
from manage_project.wrtr import wrtr
from manage_project.proconfig import config

def pro(name, lang, description, authors, referenced=""):
		script_directory=os.path.realpath(__file__)
		script_directory=script_directory[0:script_directory.rindex(os.path.sep)]
		now = datetime.now()
		weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		if name == "":
			print ("Error: empty project name.")
			return False
		else:
			os.mkdir(name);
			project_xml=open(name+os.path.sep+"project.xml", "w+")
			ref=""
			if referenced:
				if isinstance(referenced, list):
					ref=referenced[0]
					if len(referenced) > 1:
						for line in referenced[1:]:
							ref+="\n{}".format(line)
			text1="""\
<?xml version='1.0' encoding='utf-8'?>
<project>
<version>
1.0
</version>
<name>
%s
</name>
<language>
%s
</language>
<authors>
%s
</authors>
<description>
%s
</description>
<date>
<day>
%s
</day>
<month>
%s
</month>
<year>
%s
</year>
<weekday>
%s
</weekday>
<hour>
%s
</hour>
<minute>
%s
</minute>
<second>
%s
</second>
</date>
<referenced>
%s
</referenced>
</project>""" %(name, lang, authors, description, now.day, now.month, now.year, weekdays[now.isoweekday()-1], now.hour, now.minute, now.second, ref)
			project_xml.write(text1)
			project_xml.close()
			dependencies=open(name+os.path.sep+"dependencies", "w+")
			dependencies.close()
			if isinstance(referenced, list):
				import distutils.core
				for r in referenced:
					if os.path.exists(r):
						distutils.dir_util.copy_tree(r, name+os.path.sep+r)
			else:
				import distutils.core
				if os.path.exists(referenced):
					distutils.dir_util.copy_tree(referenced, name+os.path.sep+referenced)
			manage_py=open(name+os.path.sep+"manage.py", "w+")
			os.mkdir(name+os.path.sep+"doc")
			doc_xhtml=open(name+os.path.sep+"doc"+os.path.sep+"doc.xhtml", "w+")
			text2="""\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xhtml>
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<meta charset="utf-8" />
<title>%s</title>
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
<project lang="%s" project_name="%s">
<h1>%s</h1>
<description>
<h3>Description</h3>
<p>
%s
</p>
</description>
</project>
</body>
</html>""" %(name, lang, name, name, description)
			doc_xhtml.write(text2)
			doc_xhtml.close()
			style_css=open(name+os.path.sep+"doc"+os.path.sep+"style.css", "w+")
			css_text="""\
project {
	font-family: Arial;
}
project description {
	text-align: justify;
}"""
			style_css.write(css_text)
			style_css.close()
			config_py=open(name+os.path.sep+"config.py", "w+")
			config_py.write(config.replace("%name%", ""))
			config_py.close()
			text3 = """\
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from xml.dom import minidom
from manage_project.dependencies import add, remove
from manage_project.change_lang import change_lang
from manage_project.change_name import rename
from manage_project.change_authors import change_author
from manage_project.change_description import change_description
from manage_project.change_version import change_version
from manage_project.change_date import update_date
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
	change_version(full_path, sys.argv[2])
elif arg1 in ["update_date"]:
	update_date(full_path)
elif arg1 in ["dependencies"]:
	if sys.argv[2].lower() in ["add"]:
		add(full_path, sys.argv[3])
	elif sys.argv[2].lower() in ["remove", "rm"]:
		remove(full_path, sys.argv[3])"""
			if lang.lower() in ["python", "python3"]:
				text4="""\
elif arg1 in ["compile"]:
	import py_compile, distutils.core
	
	n=config.directories_to_compile
	for n1 in n:
		py_files = os.listdir(full_path+os.path.sep+n1)
		for py_file in py_files:
			if py_file.endswith(".py"):
				py_compile.compile(full_path+os.path.sep+n1+os.path.sep+py_file)
		if os.path.exists(full_path+os.path.sep+n1+os.path.sep+"__pycache__"):
			distutils.dir_util.copy_tree(full_path+os.path.sep+n1+os.path.sep+"__pycache__", full_path+os.path.sep+"bin")
			distutils.dir_util.remove_tree(full_path+os.path.sep+n1+os.path.sep+"__pycache__")
		else:
			pyc_files = os.listdir(full_path+os.path.sep+n1)
			for pyc_file in pyc_files:
				if pyc_file.endswith(".pyc"):
					os.rename(full_path+os.path.sep+n1+os.path.sep+pyc_file, full_path+os.path.sep+"bin"+os.path.sep+pyc_file)"""
				manage_py.write(text3+"\n"+text4)
				manage_py.close()
				curdir=os.getcwd()
				from manage_project.pyinit import pyinit
				os.mkdir(name+os.path.sep+name)
				os.mkdir(name+os.path.sep+"bin")
				pyinit(name)
			elif lang.lower() in ["clojure"]:
				for d in [name+os.path.sep+"test", name+os.path.sep+"src", name+os.path.sep+"resources", name+os.path.sep+"src"+os.path.sep+name, name+os.path.sep+"test"+os.path.sep+name]:
					os.mkdir(d)
				doc_info=open(name+os.path.sep+"doc"+os.path.sep+"info.txt", "w+")
				doc_info.close()
				core_clj=open(name+os.path.sep+"src"+os.path.sep+name+os.path.sep+"core.clj", "w+")
				text4="""\
( ns %s.core )
""" %(name)
				core_clj.write(text4)
				core_clj.close()
				manage_py.write(text3)
				manage_py.close()
			elif lang.lower() in ["c"]:
				os.mkdir(name+os.path.sep+"bin")
				text4="""\
elif arg1 in ["compile"]:
	import subprocess
	n=config.directories_to_compile
	for n1 in n:
		for o in os.listdir(full_path+os.path.sep+n1):
			if o.lower().endswith(".c"):
				subprocess.call(config.c_compiler_command.replace("%shortname%", full_path+os.path.sep+"bin"+os.path.sep+o[0:o.rindex(".")]).replace("%fullname%", full_path+os.path.sep+n1+os.path.sep+o).split(" "))"""
				os.mkdir(name+os.path.sep+name)
				_h=open(name+os.path.sep+name+os.path.sep+name+".h", "w+")
				_h.close()
				_c=open(name+os.path.sep+name+os.path.sep+name+".c", "w+")
				wrtr(name+os.path.sep+name+os.path.sep+name+".c")
				manage_py.write(text3+"\n"+text4)
				manage_py.close()
			elif lang.lower() in ["cpp", "c++"]:
				os.mkdir(name+os.path.sep+"bin")
				text4="""\
elif arg1 in ["compile"]:
	import subprocess
	
	n=config.directories_to_compile
	
	for n1 in n:
		for o in os.listdir(full_path+os.path.sep+n1):
			if o.lower().endswith(".cpp"):
				subprocess.call(config.cpp_compiler_command.replace("%shortname%", full_path+os.path.sep+"bin"+os.path.sep+o[0:o.rindex(".")]).replace("%fullname%", full_path+os.path.sep+n1+os.path.sep+o).split(" "))"""
				manage_py.write(text3+"\n"+text4)
				manage_py.close()
				os.makedirs(name+os.path.sep+"src"+os.path.sep+name)
				_h=open(name+os.path.sep+"src"+os.path.sep+name+os.path.sep+name+".h", "w+")
				_h.close()
				_cpp=open(name+os.path.sep+"src"+os.path.sep+name+os.path.sep+name+".cpp", "w+")
				wrtr(name+os.path.sep+"src"+os.path.sep+name+os.path.sep+name+".cpp")
				_cpp.close()
			elif lang.lower() in ["lua"]:
				os.mkdir(name+os.path.sep+"bin")
				os.mkdir(name+os.path.sep+name)
				text4="""
elif arg1 in ["compile"]:
	import subprocess
	
	n=config.directories_to_compile
	
	for n1 in n:
		for i in os.listdir(full_path+os.path.sep+n1):
			if i.lower().endswith(".lua"):
				subprocess.call(config.lua_compiler_command.replace("%shortname%" full_path+os.path.sep+"bin"+os.path.sep+i[0:i.rindex(".")]+".out").replace("%fullname%", full_path+os.path.sep+n1+os.path.sep+i).split(" "))"""
				manage_py.write(text3+"\n"+text4)
				manage_py.close()
			elif lang.lower() in ["java"]:
				os.makedirs(name+os.path.sep+"src"+os.path.sep+name)
				os.mkdir(name+os.path.sep+"bin")
				wrtr(name+os.path.sep+"src"+os.path.sep+name+os.path.sep+name+".java")
			else:
				manage_py.write(text3)
				manage_py.close()
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Pro is a project manager")
	parser.add_argument("name", help="name of the project")
	parser.add_argument("language", help="programming language of the project")
	parser.add_argument("description", help="description of the project")
	parser.add_argument("authors", help="authors of the project")
	parser.add_argument("-r", "--ref", "--referenced", nargs="+", help="other directories or files to include")
	args=parser.parse_args()
	if args.name and args.language and args.authors:
		if args.description:
			d=args.description
		else:
			d=""
		if args.ref:
			r=args.ref
		else:
			r=""
		pro(args.name, args.language, d, args.authors, r)
	else:
		parser.print_help()
