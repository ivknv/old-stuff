#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, os, time
from datetime import datetime

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def fix(db=os.path.expanduser("~/notes.db")):
	today = weekdays[datetime.now().weekday()]
	print("Yet another {weekday}.".format(weekday=today))
	if today == "Monday":
		print("Damn, I hate mondays!")
	elif today in ["Saturday", "Sunday"]:
		print("Why do I even work on weekends?")
	else:
		print("Well at least today is not monday.")
	con = sqlite3.connect(db) # Connect SQLite database
	try:
		cur = con.cursor() # Get cursor
		cur.execute("PRAGMA table_info('notes');") # Execute SQLite command
		required_columns = [("id", "INTEGER PRIMARY KEY AUTOINCREMENT"), ("title", "VARCHAR(100)"), ("text", "TEXT"), ("tags", "VARCHAR"), ("date", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"), ("todo", "VARCHAR DEFAULT \"0, 0\"")]
		result = [res[1] for res in cur.fetchall()] # Get result of executing SQLite command
		for column in required_columns:
			if not column[0] in result:
				print("{column} is missing. Nothing special.".format(column=column[0]))
				print("Adding {column}.".format(column=column[0]))
				sql="ALTER TABLE notes ADD COLUMN {missing_column} {type};".format(missing_column=column[0], type=column[1])
				print("Here's the SQL command")
				print(sql)
				cur.execute(sql) # Execute SQLite command
				con.commit()
				print("I've added new column. Now I will test it.")
				try:
					cur.execute("SELECT tags FROM notes;") # Execute SQLite command
				except sqlite3.OperationalError as e:
					print("Whoops! I've got an error from SQLite:")
					print(e)
				else:
					print("Yet another success. Test has been passed.")
			else:
				print("{column} is on it's own place".format(column=column[0]))
		print("I'm done!")
	finally:
		print("Finally closing the database")
		con.close()
		print("Everything seems to be fine.")
		print("Hmm... Not sure...")
		print("Well, at least I closed the database.")

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Add missing columns in a database so Noter will work fine.") # Create argument parser
	parser.add_argument("db", nargs="+", default=os.path.expanduser("~/notes.db"), help="Path to database. Defaults to ~/notes.db") # Add argument to parser
	args = parser.parse_args() # Parse arguments
	for arg in args.db:
		fix(arg)
