#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def addTemplate(filename, additional=""):
	if os.path.exists(filename):
		filename=os.path.realpath(filename)
		f1=open(filename, "r")
		f1r=f1.read()
		f1.close()
		shortfname=filename[filename.rindex(os.path.sep)+1::]
		template_dir=os.path.realpath(__file__)
		template_dir=template_dir[0:template_dir.rindex(os.path.sep)]+os.path.sep+"templates"
		template_name=template_dir+os.path.sep+shortfname
		shortfname_ex=shortfname[shortfname.rindex(".")::]
		try:
			template=open(template_name, "w")
			template.write(f1r)
			template.close()
			if isinstance(additional, str) and additional != "":
				os.symlink(template_name, template_dir+os.path.sep+additional+shortfname_ex)
				os.chmod(template_name, 0o755)
			elif isinstance(additional, list) and len(additional)>0:
				for i in additional:
					os.symlink(template_name, template_dir+os.path.sep+i+shortfname_ex)
				os.chmod(template_name, 0o755)
		except IOError:
			return False
		return True
	else:
		return False

if __name__ == "__main__":
	import sys
	if len(sys.argv) == 2:
		status=addTemplate(sys.argv[1])
		if status:
			print("Success")
		else:
			print("Fail")
	elif len(sys.argv) > 2:
		status=addTemplate(sys.argv[1], sys.argv[2::])
		if status:
			print("Success")
		else:
			print("Fail")
	else:
		print("usage: add-template [filename] [additional-filenames]")
