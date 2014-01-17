#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, distutils.core
from datetime import datetime
from manage.wrtr import wrtr
import config

script_directory=os.path.realpath(__file__)
script_directory=script_directory[0:script_directory.rindex(os.path.sep)]

now = datetime.now()
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

try:
	if sys.argv[1] in [""]:
		print ("Error: empty project name.")
		exit(1)
	else:
		try:
			referenced=sys.argv[5]
		except IndexError:
			referenced=""
		os.mkdir(sys.argv[1]);
		distutils.dir_util.copy_tree(script_directory+"/manage", sys.argv[1]+"/manage")
		project_xml=open(sys.argv[1]+"/project.xml", "w+")
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
</project>""" %(sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[3], now.day, now.month, now.year, weekdays[now.isoweekday()-1], now.hour, now.minute, now.second, referenced)
		project_xml.write(text1)
		project_xml.close()
		dependencies=open(sys.argv[1]+os.path.sep+"dependencies", "w+")
		dependencies.close()
		if os.path.exists(referenced):
			distutils.dir_util.copy_tree(referenced, sys.argv[1]+"/"+referenced)
		manage_py=open(sys.argv[1]+"/manage.py", "w+")
		os.mkdir(sys.argv[1]+"/doc")
		doc_xhtml=open(sys.argv[1]+"/doc/doc.xhtml", "w+")
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
</html>""" %(sys.argv[1], sys.argv[2], sys.argv[1], sys.argv[1], sys.argv[3])
		doc_xhtml.write(text2)
		doc_xhtml.close()
		style_css=open(sys.argv[1]+"/doc/style.css", "w+")
		css_text="""\
project {
	font-family: Arial;
}
project description {
	text-align: justify;
}"""
		style_css.write(css_text)
		style_css.close()
		config_py=open(os.path.realpath(__file__)[0:os.path.realpath(__file__).rindex(os.path.sep)]+os.path.sep+"config.py", "r")
		config_text=config_py.read()
		config_py.close()
		config_py=open(sys.argv[1]+os.path.sep+"config.py", "w+")
		config_py.write(config_text)
		config_py.close()
		text3 = """\
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
		remove(full_path, sys.argv[3])"""
		if sys.argv[2].lower() in ["python", "python3"]:
			text4="""\
elif arg1 in ["compile"]:
	import py_compile, distutils.core
	directory=full_path+os.path.sep+name

	py_files = os.listdir(directory)
	for py_file in py_files:
		if py_file.endswith(".py"):
			py_compile.compile(directory+os.path.sep+py_file)
	if os.path.exists(directory+os.path.sep+"__pycache__"):
		distutils.dir_util.copy_tree(directory+os.path.sep+"__pycache__", full_path+os.path.sep+"bin")
	else:
		pyc_files = os.listdir(directory)
		for pyc_file in pyc_files:
			if pyc_file.endswith(".pyc"):
				os.rename(directory+os.path.sep+pyc_file, full_path+os.path.sep+"bin"+os.path.sep+pyc_file)"""
			manage_py.write(text3+"\n"+text4)
			manage_py.close()
			curdir=os.getcwd()
			from manage.pyinit import pyinit
			for d in [sys.argv[1]+"/bin", sys.argv[1]+"/"+sys.argv[1]]:
				os.mkdir(d)
			pyinit(sys.argv[1])
		elif sys.argv[2].lower() in ["clojure"]:
			for d in [sys.argv[1]+"/test", sys.argv[1]+"/src", sys.argv[1]+"/resources", sys.argv[1]+"/src/"+sys.argv[1], sys.argv[1]+"/test/"+sys.argv[1]]:
				os.mkdir(d)
			doc_info=open(sys.argv[1]+"/doc/info.txt", "w+")
			doc_info.close()
			core_clj=open(sys.argv[1]+"/src/"+sys.argv[1]+"/core.clj", "w+")
			text4="""\
( ns %s.core )
""" %(sys.argv[1])
			core_clj.write(text4)
			core_clj.close()
			manage_py.write(text3)
			manage_py.close()
		elif sys.argv[2].lower() in ["c"]:
			os.mkdir(sys.argv[1]+"/bin")
			text4="""\
elif arg1 in ["compile"]:
	import subprocess
	for o in os.listdir(full_path+os.path.sep+name):
		if o.lower().endswith(".c"):
			subprocess.call(config.c_compiler_command.replace("%shortname%", full_path+os.path.sep+"bin"+os.path.sep+o[0:o.rindex(".")]).replace("%fullname%", full_path+os.path.sep+name+os.path.sep+o).split(" "))"""
			os.mkdir(sys.argv[1]+os.path.sep+sys.argv[1])
			_h=open(sys.argv[1]+os.path.sep+sys.argv[1]+os.path.sep+sys.argv[1]+".h", "w+")
			_h.close()
			_c=open(sys.argv[1]+"/"+sys.argv[1]+"/"+sys.argv[1]+".c", "w+")
			wrtr(sys.argv[1]+"/"+sys.argv[1]+"/"+sys.argv[1]+".c")
			manage_py.write(text3+"\n"+text4)
			manage_py.close()
		elif sys.argv[2].lower() in ["cpp", "c++"]:
			os.mkdir(sys.argv[1]+"/bin")
			text4="""\
elif arg1 in ["compile"]:
	import subprocess
	for o in os.listdir(full_path+"/"+name):
		if o.lower().endswith(".cpp"):
			subprocess.call(config.cpp_compiler_command.replace("%shortname%", full_path+os.path.sep+"bin"+os.path.sep+o[0:o.rindex(".")]).replace("%fullname%", full_path+os.path.sep+name+os.path.sep+o).split(" "))"""
			manage_py.write(text3+"\n"+text4)
			manage_py.close()
			os.mkdir(sys.argv[1]+os.path.sep+sys.argv[1])
			_h=open(sys.argv[1]+os.path.sep+sys.argv[1]+os.path.sep+sys.argv[1]+".h", "w+")
			_h.close()
			_cpp=open(sys.argv[1]+os.path.sep+sys.argv[1]+os.path.sep+sys.argv[1]+".cpp", "w+")
			wrtr(sys.argv[1]+"/"+sys.argv[1]+"/"+sys.argv[1]+".cpp")
			_cpp.close()
		elif sys.argv[2].lower() in ["lua"]:
			os.mkdir(sys.argv[1]+os.path.sep+"bin")
			os.mkdir(sys.argv[1]+os.path.sep+sys.argv[1])
			text4="""
elif arg1 in ["compile"]:
	import subprocess
	for i in os.listdir(full_path+"/"+name):
		if i.lower().endswith(".lua"):
			subprocess.call(config.lua_compiler_command.replace("%shortname%" full_path+os.path.sep+"bin"+os.path.sep+i[0:i.rindex(".")]+".out").replace("%fullname%", full_path+os.path.sep+name+os.path.sep+i).split(" "))"""
			manage_py.write(text3+"\n"+text4)
			manage_py.close()
		else:
			manage_py.write(text3)
			manage_py.close()
except IndexError:
	usage="""\
Usage: pro [project_name] [language] [description] [authors] [referenced_projects]"""
	print (usage)
	exit(1)
