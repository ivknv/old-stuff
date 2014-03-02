#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def rmTemplateAll(tfnames, template_dir="", verbose=False):
	if template_dir and os.path.exists(template_dir):
		template_dir=os.path.realpath(template_dir)
	else:
		template_dir=os.path.realpath(os.path.dirname(__file__))+os.path.sep+"templates"
	for tfname in tfnames:
		if os.path.exists(template_dir+os.path.sep+tfname):
			for i in os.listdir(template_dir):
				if os.path.islink(template_dir+os.path.sep+i):
					if verbose:
						print("%s is a symlink: deleting it" %i)
					if os.readlink(template_dir+os.path.sep+i) == template_dir+os.path.sep+tfname:
						linkpath=os.readlink(template_dir+os.path.sep+i)
						os.unlink(template_dir+os.path.sep+i)
						if os.path.exists(linkpath):
							if verbose:
								print("Deleting %s" %linkpath)
							os.remove(linkpath)
				elif os.path.isfile(template_dir+os.path.sep+i) and i==tfname:
						if verbose:
							print("%s is a file: deleting it" %i)
						os.remove(template_dir+os.path.sep+i)

def rmTemplate(tfnames, template_dir="", verbose=False):
	if template_dir and os.path.exists(template_dir):
		template_dir=os.path.realpath(template_dir)
	else:
		template_dir=os.path.realpath(os.path.dirname(__file__))+os.path.sep+"templates"
	for tfname in tfnames:
		if os.path.exists(template_dir+os.path.sep+tfname):
			for i in os.listdir(template_dir+os.path.sep):
				if os.path.islink(template_dir+os.path.sep+i):
					if os.readlink(template_dir+os.path.sep+i) == template_dir+os.path.sep+tfname:
						if verbose:
							print("%s is a symlink: unlinking it" %i)
						os.unlink(template_dir+os.path.sep+i)
			if os.path.isfile(template_dir+os.path.sep+tfname):
				if verbose:
					print("%s is a file: deleting it" %tfname)
				os.remove(template_dir+os.path.sep+tfname)
			elif os.path.islink(template_dir+os.path.sep+tfname):
				if verbose:
					print("%s is a link: unlinking it" %tfname)
				os.unlink(template_dir+os.path.sep+tfname)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Remove tpler template(s)")
	parser.add_argument("filename", nargs="+", help="template name")
	parser.add_argument("-a", "--all", help="rm template and all it's symlinks", action="store_true")
	parser.add_argument("-T", "--template-dir", help="specific template directory", action="store_true")
	parser.add_argument("-v", "--verbose", help="verbose", action="store_true")
	args=parser.parse_args()
	if args.filename:
		if args.verbose:
			verbose=args.verbose
		else:
			verbose=False
		if args.template_dir:
			tdir=args.template_dir
		else:
			tdir=""
		if args.all:
			rmTemplateAll(args.filename, template_dir=tdir, verbose=verbose)
		else:
			rmTemplate(args.filename, template_dir=tdir, verbose=verbose)
