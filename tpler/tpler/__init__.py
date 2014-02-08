#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, random

def writeTemplate(filename, arg2=""):
	ex=filename[filename.rindex(".")::].lower()
	if ex == ".htm":
		ex=".html"
	arg2=arg2.lower()
	template_dir=os.path.realpath(__file__)
	template_dir=template_dir[0:template_dir.rindex(os.path.sep)]+os.path.sep+"templates"
	templates=os.listdir(template_dir)
	extensions=[extension[extension.rindex(".")::] for extension in templates]
	if not ex in extensions:
		print("Data type is not supported")
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
	templateread=template.read()
	template.close()
	f1=open(filename, "w")
	f1.write(templateread)
	f1.close()
	return True
if __name__ == "__main__":
	import sys
	if len(sys.argv) == 2:
		writeTemplate(sys.argv[1])
	elif len(sys.argv) == 3:
		writeTemplate(sys.argv[1], sys.argv[2])
	elif len(sys.argv) > 3:
		writeTemplate(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print("usage: tpler [filname] [type]")
