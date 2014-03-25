#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tpler.add_template import addTemplate

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Add template for tpler") # Create argument parser
	parser.add_argument("-f", "--filename", help="file name") # Add argument to parser
	parser.add_argument("-a", "--aliases", nargs="+", help="aliases") # Add argument to parser
	parser.add_argument("-T", "--template-dir", default=None, help="specific template directory", action="store_true") # Add argument to parser
	parser.add_argument("-v", "--verbose", help="verbose", action="store_true") # Add argument to parser
	args = parser.parse_args() # Parse arguments using parser options
	if args.filename:
		if args.aliases:
			print(addTemplate(args.filename, args.aliases, template_dir=args.template_dir, verbose=args.verbose)) # Add a new template
		else:
			print(addTemplate(args.filename, template_dir=args.template_dir, verbose=args.verbose)) # Add a new template
