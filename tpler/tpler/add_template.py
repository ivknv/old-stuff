#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

def addTemplate(filename, additional="", template_dir="", verbose=False):
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

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Add template for tpler")
	parser.add_argument("-f", "--filename", help="file name")
	parser.add_argument("-a", "--aliases", nargs="+", help="aliases")
	parser.add_argument("-T", "--template-dir", help="specific template directory", action="store_true")
	parser.add_argument("-v", "--verbose", help="verbose", action="store_true")
	args = parser.parse_args()
	if args.filename:
		if args.template_dir:
			tdir=args.template_dir
		else:
			tdir=None
		if args.verbose:
			verbose=args.verbose
		else:
			verbose=False
		if args.aliases:
			print(addTemplate(args.filename, args.aliases, template_dir=tdir, verbose=verbose))
		else:
			print(addTemplate(args.filename, template_dir=tdir, verbose=verbose))
