#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

def addTemplate(filename, additional="", template_dir="", verbose=False): # Add a new template
	if os.path.exists(filename):
		filename=os.path.realpath(filename)
		f1=open(filename, "r")
		f1r=f1.read()
		f1.close()
		shortfname=filename[filename.rindex(os.path.sep)+1::]
		if template_dir and os.path.exists(template_dir):
			template_dir=os.path.realpath(template_dir)
		else:
			template_dir=os.path.realpath(__file__)
			template_dir=os.path.realpath(os.path.dirname(__file__))+os.path.sep+"templates"
		template_name=template_dir+os.path.sep+shortfname
		shortfname_ex=shortfname[shortfname.rindex(".")::]
		try:
			template=open(template_name, "w")
			template.write(f1r)
			template.close()
			os.chmod(template_name, 0o755)
			if isinstance(additional, str) and additional:
				if verbose:
					print("creating the symlink: {}".format(template_dir+os.path.sep+additional+shortfname_ex))
				os.symlink(template_name, template_dir+os.path.sep+additional+shortfname_ex)
			elif isinstance(additional, list) and len(additional)>0:
				for i in additional:
					if verbose:
						print("creating the symlink: {}".format(template_dir+os.path.sep+i+shortfname_ex))
					os.symlink(template_name, template_dir+os.path.sep+i+shortfname_ex)
		except IOError:
			return False
		return True
	else:
		return False
