#!/usr/bin/env python
# -*- coding: utf-8 -*-

# all the comments except this are autogenerated with CodeCommenter
# see https://github.com/SPython/code-commenter

import os
from Noter import init, get, add_note, rm_note, read, edit_note, search, ID, TITLE, TEXT, TAGS, DATE

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Allows to keep notes") # Create argument parser
	parser.add_argument("-a", "--add", action="store_true", help="Add note") # Add argument to parser
	parser.add_argument("-t", "--title", default=None, help="Title of the note") # Add argument to parser
	parser.add_argument("-T", "--text", default=None, help="Text of the note") # Add argument to parser
	parser.add_argument("-tg", "--tags", default="", help="Tags") # Add argument to parser
	parser.add_argument("-g", "--get", action="store_true", help="Get note") # Add argument to parser
	parser.add_argument("-i", "--id", default=None, type=int, help="ID of the note") # Add argument to parser
	parser.add_argument("-l", "--ls", "--list", action="store_true", help="List all notes") # Add argument to parser
	parser.add_argument("-rm", "--rm", "--remove", action="store_true", help="Remove note") # Add argument to parser
	parser.add_argument("-d", "--db-path", default=os.path.expanduser("~/notes.db"), help="Path to the database") # Add argument to parser
	parser.add_argument("-rs", "--reverse", action="store_true", help="Reverse sort") # Add argument to parser
	parser.add_argument("--init", action="store_true", help="Initialize database") # Add argument to parser
	parser.add_argument("-s", "--slice", default="0:", help="Slice note list") # Add argument to parser
	parser.add_argument("-e", "--edit", action="store_true", help="Edit note") # Add argument to parser
	parser.add_argument("--search", default=None, action="store", help="Search for note") # Add argument to parser
	args = parser.parse_args() # Parse arguments
	
	if args.init:
		init(db=args.db_path) # Initialize database for keeping notes
	
	if args.add:
		if args.title and args.text:
			add_note(title=args.title, text=args.text, tags=args.tags, db=args.db_path) # Add a new note
	elif args.get and args.id:
		note=get(id=args.id, db=args.db_path) # Get note by id
		print("{id}. {title}\n  {text}\n    {date}".format(id=note[ID], title=note[TITLE], text=note[TEXT].replace("\n", "\n ").replace("\\t", "\t").replace("\\n", "\n "), date=note[DATE]))
	elif args.ls:
		from pydoc import pager
		notes=""
		read_=read(db=args.db_path, slice_string=args.slice)
		if not args.reverse:
			read_.reverse()
		for note in read_:
			notes+="{id}. {title}\n  {text}\n    {date}\n\n".format(id=note[ID], title=note[TITLE], text=note[TEXT], date=note[DATE])
			notes.replace("\n", "\n ").replace("\\t", "\t").replace("\\n", "\n ")
		pager(notes)
	elif args.rm:
		rm_note(id=args.id, title=args.title, db=args.db_path) # Remove note
	elif args.edit and args.id:
		result=edit_note(id=args.id, title=args.title, text=args.text, tags=args.tags, db=args.db_path) # Edit note
		if result:
			print("Successfully edited note")
		else:
			print("Failed to edit note")
	elif args.search:
		from pydoc import pager
		found=search(q=args.search)
		text=""
		for note in found:
			text+="{id}. {title}\n {text}\n    {date}\n\n".format(id=note[ID], title=note[TITLE], text=note[TEXT].replace("\n", "\n ").replace("\\t", "\t").replace("\\n", "\n "), date=note[DATE])
		pager(text)
