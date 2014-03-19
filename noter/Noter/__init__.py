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
