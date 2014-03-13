#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, random

def writeTemplate(filenames, arg2="", template_dir=None):
	for filename in filenames:
		if filename.endswith("/") or filename.endswith("\\"):
			filename=filename[0:-1]
		ex=filename[filename.rindex(".")::].lower()
		if ex == ".htm":
			ex=".html"
		arg2=arg2.lower()
		if not isinstance(template_dir, str) or not template_dir:
			template_dir=os.path.realpath(__file__)
			template_dir=template_dir[0:template_dir.rindex(os.path.sep)]+os.path.sep+"templates"
		elif os.path.exists(template_dir):
			template_dir=os.path.realpath(template_dir)
		templates=os.listdir(template_dir)
		extensions=[extension[extension.rindex(".")::] for extension in templates]
		if not ex in extensions:
			print("File type is not supported")
			return False
		if isinstance(arg2, str) and arg2 != "":
			if arg2 in ["random", "rand", "rnd"]:
				tname=template_dir+os.path.sep+random.choice([arg2file for arg2file in templates if arg2file.endswith(ex)])
			else:
				tname=template_dir+os.path.sep+arg2+ex	
			try:
				template=open(tname)
			except IOError:
				print("No such template")
				return False
		else:
			template=open(template_dir+os.path.sep+"default"+ex)
		if "." in filename:
			rpl=filename[0:filename.index(".")]
		else:
			rpl=filename
		if "/" in rpl:
			rpl=rpl[rpl.rindex("/")+1:]
		if "\\" in rpl:
			rpl=rpl[rpl.rindex("\\")+1:]
		templateread=template.read().replace("%name%", rpl)
		template.close()
		f1=open(filename, "w")
		f1.write(templateread)
		f1.close()
	return True

def getTemplateWithFT(ft, arg2="", template_dir=None):
	ft=ft.lower()
	if template_dir and os.path.exists(template_dir):
		template_dir=os.path.realpath(template_dir)
	else:
		template_dir=os.path.realpath(os.path.dirname(__file__)+os.path.sep+"templates")
	extensions={ex[ex.rindex("."):].lower() for ex in os.listdir(template_dir)}
	if ft[0] != ".":
		ft="."+ft
	if ft in extensions:
		if arg2:
			tfiles={f1 for f1 in os.listdir(template_dir) if f1.endswith(ft)}
			if arg2 in ["random", "rand", "rnd"]:
				tname=r'%s' %template_dir+os.path.sep+random.choice(tfiles)
			else:
				tname=r'%s' %template_dir+os.path.sep+arg2+ft
		else:
			tname=r'%s' %template_dir+os.path.sep+"default"+ft
		template=open(tname)
		template_read=template.read()
		template.close()
		return template_read
