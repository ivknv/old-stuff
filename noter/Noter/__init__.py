#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, os

def init(db=os.path.expanduser("~/notes.db")):
	con = sqlite3.connect(db)
	cur = con.cursor()
	cur.execute("CREATE TABLE notes(id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(100), text TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
	con.commit()
	con.close()

def add_note(title, text, todo=0, db=os.path.expanduser("~/notes.db")):
	con = sqlite3.connect(db)
	cur = con.cursor()
	cur.execute("INSERT INTO notes(title, text) VALUES(\"{}\", \"{}\");".format(title, text))
	con.commit()
	con.close()

def rm_note(id=None, title=None,db=os.path.expanduser("~/notes.db")):
	if id or title:
		con = sqlite3.connect(db)
		cur = con.cursor()
	else:
		return None
	if id and not title:
		cur.execute("DELETE FROM notes WHERE id={};".format(id))
	elif title and not id:
		cur.execute("DELETE FROM notes WHERE title=\"{}\";".format(title))
	elif id and title:
		cur.execute("DELETE FROM notes WHERE id={} AND title=\"{}\"".format(id, title))
	con.commit()
	con.close()

def read(db=os.path.expanduser("~/notes.db"), slice_string="0:"):
	slice_string=[int(s) for s in slice_string.split(":") if s]
	con = sqlite3.connect(db)
	cur = con.cursor()
	cur.execute("SELECT * FROM notes;")
	if len(slice_string) == 2:
		notes = cur.fetchall()[slice_string[0]:slice_string[1]]
	else:
		notes = cur.fetchall()[slice_string[0]:]
	con.close()
	return notes

def get(id, db=os.path.expanduser("~/notes.db")):
	if id:
		con = sqlite3.connect(db)
		cur = con.cursor()
		cur.execute("SELECT * FROM notes WHERE id={};".format(id))
		found=cur.fetchall()
		con.close()
		return found

def edit_note(id, title=None, text=None, db=os.path.expanduser("~/notes.db")):
	if id and (title or text):
		con = sqlite3.connect(db)
		cur = con.cursor()
		if not title and text:
			cur.execute("UPDATE notes SET text=\"{}\" WHERE id={};".format(text, id))
		elif title and not text:
			cur.execute("UPDATE notes SET title=\"{}\" WHERE id={};".format(title, id))
		elif title and text:
			cur.execute("UPDATE notes SET title=\"{}\", text=\"{}\" WHERE id={};".format(title, text, id))
		con.commit()
		con.close()
		return True
	return False

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Allows to keep notes")
	parser.add_argument("-a", "--add", action="store_true", help="Add note")
	parser.add_argument("-t", "--title", help="Note title")
	parser.add_argument("-T", "--text", help="Note text")
	parser.add_argument("-g", "--get", action="store_true", help="Get note")
	parser.add_argument("-i", "--id", help="Note id")
	parser.add_argument("-l", "--ls", "--list", action="store_true", help="List all notes")
	parser.add_argument("-rm", "--rm", "--remove", action="store_true", help="Remove note")
	parser.add_argument("-d", "--db-path", default=os.path.expanduser("~/notes.db"), help="Path to the database")
	parser.add_argument("-rs", "--reverse", action="store_true", help="Reverse sort")
	parser.add_argument("--init", action="store_true", help="Initialize database")
	parser.add_argument("-s", "--slice", help="Slice the note list")
	parser.add_argument("-e", "--edit", action="store_true", help="Edit note")
	args = parser.parse_args()
	
	if args.init:
		init(db=args.db_path)
	
	if args.add:
		if args.title and args.text:
			add_note(title=args.title, text=args.text, db=args.db_path)
	elif args.get and args.id:
		note=get(id=args.id, db=args.db_path)
		print("{}. {}\n  {}\n    {}".format(note[0], note[1], note[2], note[3]))
	elif args.ls:
		from pydoc import pager
		notes=""
		if args.slice:
			slice_=args.slice
		else:
			slice_="0:"
		read_=read(db=args.db_path, slice_string=slice_)
		if args.reverse:
			read_.reverse()
		for note in read_:
			notes+="{}. {}\n  {}\n    {}\n\n".format(note[0], note[1], note[2], note[3])
		pager(notes.replace("\\n", "  \n").replace("\\t", "\t"))
	elif args.rm:
		if args.title:
			t=args.title
		else:
			t=None
		if args.id:
			i=args.id
		else:
			i=None
		rm_note(id=i, title=t, db=args.db_path)
	elif args.edit and args.id:
		if args.title:
			title=args.title
		else:
			title=None
		if args.text:
			text=args.text
		else:
			text=None
		result=edit_note(id=args.id, title=title, text=text, db=args.db_path)
		if result:
			print("Successfully edited note")
		else:
			print("Failed to edit note")
