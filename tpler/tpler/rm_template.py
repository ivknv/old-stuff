#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def main(tfname):
	template_dir=os.path.realpath(__file__)
	template_dir=template_dir[0:template_dir.rindex(os.path.sep)]+os.path.sep+"templates"
	if os.path.exists(template_dir+os.path.sep+tfname):
		for i in os.listdir(template_dir):
			if os.path.islink(template_dir+os.path.sep+i):
				print("%s is a symlink: deleting it" %i)
				if os.readlink(template_dir+os.path.sep+i) == template_dir+os.path.sep+tfname:
					linkpath=os.readlink(template_dir+os.path.sep+i)
					os.remove(template_dir+os.path.sep+i)
					if os.path.exists(linkpath):
						print("Deleting %s" %linkpath)
						os.remove(linkpath)
			elif os.path.isfile(template_dir+os.path.sep+i) and template_dir+os.path.sep+i==tfname:
					if os.path.exists(template_dir+os.path.sep+i):
						print("%s is a file: deleting it" %i)
						os.remove(template_dir+os.path.sep+i)
				

if __name__ == "__main__":
	main("config.py")
