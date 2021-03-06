#!/usr/bin/env python

from tpler import __path__ as tpler_path, writeTemplate, getTemplateWithFT
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="A simple templater.") # Create argument parser
	parser.add_argument("-l", "--ls", "--list", help="List all available templates", action="store_true") # Add argument to parser
	parser.add_argument("-i", "--input-file", help="File name", nargs="+", action="store") # Add argument to parser
	parser.add_argument("-t", "--template", help="Specific template", action="store", default="") # Add argument to parser
	parser.add_argument("-f", "--filetype", help="Use a specific filetype", action="store") # Add argument to parser
	parser.add_argument("-T", "--template-dir", help="Specific template directory", action="store") # Add argument to parser
	args=parser.parse_args() # Parse arguments using parser options
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
				if infile.endswith("/") or infile.endswith("\\"):
					infile=infile[0:-1]
				f1=open(infile, "w")
				if "." in args.infile:
					rpl=args.infile[0:args.infile.index(".")]
				else:
					rpl=args.infile
				if "/" in rpl:
					rpl=rpl[rpl.rindex("/")+1:]
				if "\\" in rpl:
					rpl=rpl[rpl.rindex("\\")+1:]
				txt=getTemplateWithFT(args.filetype, tmpl, template_dir=tmpldir).replace("%name%", rpl) # Get template by specific filetype and second argument (template name)
				f1.write(txt)
				f1.close()
		else:
			if args.input_file:
				writeTemplate(args.input_file, tmpl, template_dir=tmpldir) # Get some of the templates and write its content to the file
			else:
				writeTemplate(args.input_file, tmpl, template_dir=tmpldir) # Get some of the templates and write its content to the file
	else:
		from pydoc import pager
		if tmpldir:
			files=os.listdir(tmpldir)
		else:
			files=os.listdir(tpler_path[0]+os.path.sep+"templates")
		extensions={ex[ex.rindex("."):].lower() for ex in files}
		txt=""
		for ex in extensions:
			txt+="{}:\n".format(ex)
			for f1 in files:
				if f1.endswith(ex):
					txt+="  {}\n".format(f1[0:f1.rindex(".")])
		pager(txt)
