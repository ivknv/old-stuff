#!/usr/bin/env python
# -*- coding: utf-8 -*-

# all the comments except this are autogenerated

from CodeCommenter import *

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Automatic code commenting") # Create argument parser
	parser.add_argument("file", help="File name") # Add argument to parser
	parser.add_argument("-p", "--path", help="Path to the patterns file") # Add argument to parser
	parser.add_argument("-w", "--write", action="store_true", help="Write to the file") # Add argument to parser
	parser.add_argument("-rm", "--remove-comments", action="store_true", help="Remove all the comments written before") # Add argument to parser
	parser.add_argument("-cs", "--comment-start", help="Comment start") # Add argument to parser
	parser.add_argument("-ce", "--comment-end", help="Comment end") # Add argument to parser
	parser.add_argument("-f", "--filetype", help="Manually set filetype") # Add argument to parser
	parser.add_argument("-sp", "--start-pos", type=int, default=0, help="Set starting line") # Add argument to parser
	parser.add_argument("-ep", "--end-pos", type=int, default=None, help="Set ending line") # Add argument to parser
	args=parser.parse_args() # Parse arguments using parser options
	if args.file:
		if args.filetype:
			filetype=args.filetype
		else:
			filetype=args.file[args.file.rindex(".")+1:].lower()
		f1=open(args.file)
		code=f1.read()
		f1.close()
		if args.remove_comments:
			comments=re.findall(args.comment_start+".*"+args.comment_end, code)
			for i in comments:
				code=code.replace(i, "")
		if args.path:
			modified=comment(code, args.path, filetype, startpos=args.start_pos, endpos=args.end_pos)
		else:
			modified=comment(code, "patterns.xml", filetype, startpos=args.start_pos, endpos=args.end_pos)
		if args.write:
			f1=open(args.file, "w")
			f1.write(modified)
			f1.close()
		else:
			print(modified)
