#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov

Functions that used views.py, ajax.py and api.py
"""

import sys # To check Python version

import re

from note.models import Note # To get notes from server's database

if sys.version_info.major < 3: # If version of Python is lower than 3
	range = xrange # Use xrange instead of range

def check_similarity_from_strings(string1, string2):
	"""
	Split and check similarity of 2 strings.
	
	@param string1: First string
	@param string2: Second string
	@type string1: str
	@type string2: str
	@rtype: float
	
	>>> check_similarity_from_strings("test number 1", "test number 1")
	100.0
	
	>>> check_similarity_from_strings("test number 1", "test number 2")
	66.66666666666667
	
	"""
	string1 = string1.split(" ")
	string2 = string2.split(" ")
	percents = 0
	percents_per_word = 100.0/max(len(string1), len(string2))
	for i in string1:
		try:
			if i in string2:
				percents += percents_per_word * string2.count(i)
		except IndexError:
			pass
	return percents


def similarity_percentage(title1, title2, text1, text2):
	"""Get similarity percentage of two notes"""
	
	return (
		check_similarity_from_strings(
			text1,
			text2
		)
			+
			check_similarity_from_strings(
				title1,
				title2)
		)/2

def check_similarity(note, notes=Note.objects.all()):
	"""Get sorted list of similiar notes"""
	
	sorted_list = [] # This is the future sorted list
	
	for note2 in notes: # Iterate over notes
		if note2.id == note.id: # If first note is equal to second note
			continue # Start next iteration
		
		percent = similarity_percentage(
			title1=note.title,
			title2=note2.title,
			text1=note.text,
			text2=note2.text
		)
		
		if percent > 0:
			sorted_list.append([
				percent,
				(note, note2)
			])
	
	sorted_list.sort() # Sort list of notes
	sorted_list.reverse() # Reverse the list of notes
	return sorted_list

def check_similarity_from_string(text, title, notes=Note.objects.all()):
	"""Get sorted list of similiar notes from string"""
	
	sorted_list = [] # This is the future sorted list
	
	for note in notes: # Iterate over notes
		similarity_percent = similarity_percentage(
			title1=title,
			title2=note.title,
			text1=text,
			text2=note.text
		)
		if similarity_percent > 15:
			sorted_list.append([
				similarity_percent,
				("<Note: {title}>".format(title=title), note)
			])
	
	sorted_list.sort() # Sort list of notes
	sorted_list.reverse() # Reverse the list of notes
	
	return sorted_list

def check_similarity_from_string_list(note_id, text, title, notes=Note.objects.all()):
	"""Get sorted list of similiar notes from string.
Using lists instead of Note objects"""
	
	note_id = int(note_id)
	sorted_list = [] # This is the future sorted list
	
	for note in notes: # Iterate over notes
		if note_id == note.id:
			continue
		similarity_percent = similarity_percentage(title1=title,
			title2=note.title,
			text1=text,
			text2=note.text)
		if similarity_percent > 15:
			sorted_list.append([
				similarity_percent,
				("<Note: {}>".format(title),
					[
						note.title,
						note.text,
						transform_tags_single(
							replace_none(note.tags)
						)
					])
			])
	
	sorted_list.sort() # Sort list of notes
	sorted_list.reverse() # Reverse the list of notes
	
	return sorted_list

def page_range(page_number, num_pages, max_next=3):
	"""Generate (x)range from pages"""
	
	return range(
		page_number-max_next if num_pages > max_next \
		and page_number > max_next else 1,
		page_number+max_next if num_pages > page_number+max_next \
		else page_number+num_pages-page_number+1 or num_pages
	)

def replace_newlines_string(string):
	"""Replace all the newlines (\n) by <br/> in a string"""
	
	string = string.replace("\n\r", "<br/>").replace("\n", "<br/>")
	string = string.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
	return string

def replace_newlines(obj):
	"""Replace all the newlines (\n) in notes by <br/> HTML tags"""
	
	for i in range(len(obj.object_list)):
		if obj.object_list[i].type != "s":
			obj.object_list[i].text = replace_newlines_string(
				obj.object_list[i].text
			)
	return obj

def replace_newlines_search(obj):
	"""Replace all the newlines (\n) in notes by <br/> HTML tags.
Works only with lists ([7.2, <Note>])."""
	
	for i in range(len(obj.object_list)):
		if obj.object_list[i][1].type != "s":
			obj.object_list[i][1].text = replace_newlines_string(
				obj.object_list[i][1].text
			)
	return obj

def replace_newlines_sim(obj):
	"""Replace all the newlines (\n) in notes by <br/> HTML tags.
Works only with lists ([7.2, <Note>])."""
	
	for i in range(len(obj.object_list)):
		if obj.object_list[i][1][1].type != "s":
			obj.object_list[i][1][1].text = replace_newlines_string(
				obj.object_list[i][1][1].text
			)
	return obj

def replace_newlines_single_object(obj):
	"""Replace all the newlines (\n) in note by <br/> HTML tags"""
	if obj.type != "s":
		obj.text = replace_newlines_string(obj.text)
	return obj

def transform_tags(notes):
	"""Transforms a string with commas into a list of tags"""
	
	for i in range(len(notes)): # Iterate over a list with index
		if notes[i][1][1].tags \
		and not isinstance(notes[i][1][1].tags, list):
			notes[i][1][1].tags = notes[i][1][1].tags.split(",")
			for j in range(len(notes[i][1][1].tags)):
				if notes[i][1][1].tags[j][0] == " ":
					notes[i][1][1].tags[j] = notes[i][1][1].tags[j][1:]
	return notes

def transform_tags_single(tags):
	"""Transforms a string with commas into a list of tags"""
	
	if tags and not isinstance(tags, list):
		tags = tags.split(",")
		for i in range(len(tags)):
			if tags[i][0] == " ":
				tags[i] = tags[i][1:]
	return tags # return the result

def replace_none(tags):
	"""If tags column was added by ALTER TABLE command
tags can be empty (None object).
This function replaces tags with None value by empty string"""
	
	if tags == None: # If tags is a None object
		tags = "" # Set it equal to empty string
	
	return tags # Return result

def place_by_relevance(note, query, splitted=False, lower=False):
	"""Place notes by relevance"""
	if not lower:
		query = query.lower()
	if not splitted:
		query = query.split()
	count = 0
	note = replace_newlines_single_object(note)
	title = note.title.lower()
	text = note.text.lower()
	tags = note.tags.lower()
	q_in = 0
	for i in query:
		count_prev = count
		count -= title.count(i)
		count -= text.count(i)
		count -= tags.count(i)
		if count < count_prev:
			q_in += 1 
		if q_in > 1:
			count *= q_in
	return [
		count,
		note
	]

def htmlbody(string, title):
	"""Returns HTML skeleton"""
	
	return """\
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, user-scalable=no" />
		<title>{}</title>
	</head>
	<body>
		{}
	</body>
</html>
""".format(title, string)

def remove_tags(obj):
	"""Remove all the HTML tags from text"""
	
	obj.text = re.sub("<.*?>", "", obj.text)
	
	return obj

def remove_tags_in_all_notes(notes=Note.objects.all()):
	"""Remove all the HTML tags from text in all the notes"""
	
	for note in notes:
		if note.type != 's':
			note = remove_tags(note)
	
	return notes
