#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tpler.rm_template import rmTemplate, rmTemplateAll

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Remove tpler template(s)") # Create argument parser
	parser.add_argument("filename", nargs="+", help="template name") # Add argument to parser
	parser.add_argument("-a", "--all", help="rm template and all it's symlinks", action="store_true") # Add argument to parser
	parser.add_argument("-T", "--template-dir", default="", help="specific template directory", action="store_true") # Add argument to parser
	parser.add_argument("-v", "--verbose", help="verbose", action="store_true") # Add argument to parser
	args=parser.parse_args() # Parse arguments using parser options
	if args.filename:
		if args.all:
			rmTemplateAll(args.filename, template_dir=args.template_dir, verbose=args.verbose) # Remove a template and all its symlinks
		else:
			rmTemplate(args.filename, template_dir=args.template_dir, verbose=args.verbose) # Remove a template
