#!/usr/bin/env python

from tpler import *
	
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
