#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, random

def writeTemplate(filenames, arg2="", template_dir=None):
	for filename in filenames:
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
		templateread=template.read()
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

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="A simple templater.")
	parser.add_argument("-l", "--ls", "--list", help="List all available templates", action="store_true")
	parser.add_argument("-i", "--input-file", help="File name", nargs="+", action="store")
	parser.add_argument("-t", "--template", help="Specific template", action="store", default="")
	parser.add_argument("-f", "--filetype", help="Use a specific filetype", action="store")
	parser.add_argument("-T", "--template-dir", help="Specific template directory", action="store")
	args=parser.parse_args()
	if args.template_dir:
		tmpldir=args.template_dir
	else:
		tmpldir=None
	if not args.ls:
		if args.template:
			tmpl=args.template
		else:
			tmpl=""
		if args.filetype:
			for infile in args.input_file:
				f1=open(infile, "w")
				txt=getTemplateWithFT(args.filetype, tmpl, template_dir=tmpldir)
				f1.write(txt)
				f1.close()
		else:
			if args.input_file:
				writeTemplate(args.input_file, tmpl, template_dir=tmpldir)
			else:
				writeTemplate(args.input_file, tmpl, template_dir=tmpldir)
	else:
		from pydoc import pager
		if tmpldir:
			files=os.listdir(tmpldir)
		else:
			files=os.listdir(os.path.dirname(__file__)+os.path.sep+"templates")
		extensions={ex[ex.rindex("."):].lower() for ex in files}
		txt=""
		for ex in extensions:
			txt+="{}:\n".format(ex)
			for f1 in files:
				if f1.endswith(ex):
					txt+="  {}\n".format(f1[0:f1.rindex(".")])
		pager(txt)
