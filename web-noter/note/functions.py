#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov

Functions that used by views.py, ajax.py and api.py
"""

import sys # To check Python version

import re

from note.models import Note # To get notes from server's database

if sys.version_info.major < 3: # If version of Python is lower than 3
	range = xrange # Use xrange instead of range

def leave_unique(list_):
	for elem in list_:
		while list_.count(elem) > 1:
			list_.remove(elem)
	
	return list_

def get_pairs(string):
	pairs = []
	
	for i in range(len(string)-1):
		pairs.append(string[i:i+2])
	
	return pairs

def remove_tags_from_string(string):
	"""Remove all HTML tags from string"""
	
	return re.sub("<.*?>", "", string)

def check_similarity_from_strings(string1, string2):
	"""
	Check similarity of 2 strings.
	Returns number from 0 to 1.
	1 means that strings are identical.
	0 means that strings have nothing in common.
	
	@param string1: First string
	@param string2: Second string
	@type string1: str
	@type string2: str
	@rtype: float
	
	>>> check_similarity_from_strings("test number 1", "test number 1")
	1.0
	
	>>> check_similarity_from_strings("test number 1", "test number 2")
	0.9166666666666666
	
	>>> check_similarity_from_strings("test food", "tasty food")
	0.5882352941176471
	
	"""
	
	char = r"[\.,_\+\\/\|`~<>\?!@#\$%\^&\*\(\)\[\]\{\};:'\"=\r\t]"
	
	string1 = remove_tags_from_string(string1)
	string2 = remove_tags_from_string(string2)
	
	string1 = re.sub(char, "", string1.lower())
	string2 = re.sub(char, "", string2.lower())
	
	string1 = string1.replace("\n", " ")
	string2 = string2.replace("\n", " ")
	
	pairs1 = get_pairs(string1)
	pairs2 = get_pairs(string2)
	
	len_all_pairs = len(pairs1) + len(pairs2)
	
	shrd = leave_unique([pair for pair in pairs1 if pair in pairs2])
	
	if len_all_pairs == 0:
		return 0
	
	return 2.0 * len(shrd) / len_all_pairs
	
def similarity_score(title1, title2, text1, text2):
	"""Get similarity percentage of two notes"""
	
	return (
		check_similarity_from_strings(
			title1,
			title2),
		check_similarity_from_strings(
				text1,
				text2)
		)

def check_similarity(note, notes=Note.objects.all()):
	"""Get sorted list of similiar notes"""
	
	sorted_list = [] # This is the future sorted list
	
	for note2 in notes: # Iterate over notes
		if note2.id == note.id: # If first note is equal to second note
			continue # Start next iteration
		
		similarity = similarity_score(
			title1=note.title,
			title2=note2.title,
			text1=note.text,
			text2=note2.text
		)
		
		if sum(similarity) > 0:
			sorted_list.append([
				similarity[1]*100,
				similarity[0]*100,
				(note, note2)
			])
	
	sorted_list.sort(key=lambda x: (x[0]+x[1])/2.0) # Sort list of notes
	sorted_list.reverse() # Reverse the list of notes
	return sorted_list

def check_similarity_from_string(text, title, notes=Note.objects.all()):
	"""Get sorted list of similiar notes from string"""
	
	sorted_list = [] # This is the future sorted list
	
	for note in notes: # Iterate over notes
		similarity = similarity_score(
			title1=title,
			title2=note.title,
			text1=text,
			text2=note.text
		)
		if sum(similarity) > 0:
			sorted_list.append([
				similarity[1]*100,
				similarity[0]*100,
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
		similarity = similarity_score(title1=title,
			title2=note.title,
			text1=text,
			text2=note.text)
		if sum(similarity) > 0:
			sorted_list.append([
				similarity[1]*100,
				similarity[0]*100,
				("<Note: {}>".format(title),
					[
						note.title,
						note.text,
						transform_tags_single(
							note.tags
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
	
	text = ""
	text_splitted = string.split("\n")
	length = len(text_splitted)
	i = 0
	
	for line in text_splitted:
		i += 1
		line = line.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
		text += line
		
		if i < length: # Check if it's last line:
			if not re.search("<.*?>$", line):
				text += "<br/>"
			text += "\n"
		
	return text

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
		if obj.object_list[i][2][1].type != "s":
			obj.object_list[i][2][1].text = replace_newlines_string(
				obj.object_list[i][2][1].text
			)
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

def transform_tags_sim(notes):
	"""Transforms a string with commas into a list of tags"""
	
	for i in range(len(notes)): # Iterate over a list with index
		if notes[i][2][1].tags \
		and not isinstance(notes[i][2][1].tags, list):
			notes[i][2][1].tags = notes[i][2][1].tags.split(",")
			for j in range(len(notes[i][2][1].tags)):
				if notes[i][2][1].tags[j][0] == " ":
					notes[i][2][1].tags[j] = notes[i][2][1].tags[j][1:]
	return notes

def transform_tags_single(tags):
	"""Transforms a string with commas into a list of tags"""
	
	if tags and not isinstance(tags, list):
		tags = tags.split(",")
		for i in range(len(tags)):
			if tags[i][0] == " ":
				tags[i] = tags[i][1:]
	return tags # return the result

def place_by_relevance(note, query, splitted=False, lower=False):
	"""Place notes by relevance"""
	if not lower:
		query = query.lower()
	if not splitted:
		query = query.split()
	rating = 0
	title = note.title.lower()
	text = note.no_html().lower()
	tags = note.tags.lower()
	q_in = 0
	for i in query:
		rating_prev = rating
		rating -= title.count(i)
		rating -= text.count(i)
		rating -= tags.count(i)
		if rating < rating_prev:
			q_in += 1
		if q_in > 1:
			rating *= q_in
	return [
		rating,
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
