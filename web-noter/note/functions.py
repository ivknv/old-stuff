#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov

Functions that used by views.py, ajax.py and api.py
"""

import re

from note.models import Note # To get notes from database

default_excluded_words = ["a", "an", "the", "is", "am", "are",
	"for", "that", "of", "to", "so", "in", "on"]

def get_pairs(words):
	pairs = []
	for word in words:
		if len(word) == 1:
			pairs.append(word)
		else:
			pairs += [word[i:i+2] for i in range(len(word))]
	return pairs

def remove_tags_from_string(string):
	"""Remove all HTML tags from string"""
	
	return re.sub("<.*?>", "", string)

def prepare_string(s):
	"""Remove non-letters, HTML tags,
	   some common words and split string into words"""
	
	s = s.strip().lower()
	r1 = re.compile(r"(?P<g1>\w+)n['\u2019]t", re.UNICODE)
	r2 = re.compile(r"(?P<g1>\w+)['\u2019]s", re.UNICODE)
	r3 = re.compile(r"(?P<g1>\w+)['\u2019]m", re.UNICODE)
	r4 = re.compile(r"(?P<g1>\w+)['\u2019]re", re.UNICODE)
	r5 = re.compile(r"(?P<g1>\w+)['\u2019]ve", re.UNICODE)
	r6 = re.compile(r"(?P<g1>\w+)['\u2019]d", re.UNICODE)
	r7 = re.compile(r"(?P<g1>\w+)['\u2019]ll", re.UNICODE)
	r8 = re.compile(r"gonna", re.UNICODE)
	
	s = remove_tags_from_string(s)
	s = r1.sub(r"\g<g1> not", s)
	s = r2.sub(r"\g<g1>", s)
	s = r3.sub(r"\g<g1> am", s)
	s = r4.sub(r"\g<g1> are", s)
	s = r5.sub(r"\g<g1> have", s)
	s = r6.sub(r"\g<g1> would", s)
	s = r7.sub(r"\g<g1> will", s)
	s = r8.sub(r"going to", s)
	words = re.split(r"\W", s)
	for word in default_excluded_words:
		while words.count(word) > 0:
			words.remove(word)
	
	return [word for word in words if len(word)]

def get_shrd(pairs1, pairs2):
	"""Get list of common pairs"""
	
	shrd = []
	for pair in pairs1:
		if pair in pairs2:
			if shrd.count(pair) < min(pairs1.count(pair), pairs2.count(pair)):
				shrd.append(pair)
	
	return shrd

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
	"""
	
	words1 = prepare_string(string1)
	words2 = prepare_string(string2)
	
	pairs1 = get_pairs(words1)
	pairs2 = get_pairs(words2)
	
	len_all_pairs = len(pairs1) + len(pairs2)
	
	shrd = get_shrd(pairs1, pairs2)
	
	if len_all_pairs == 0:
		return 0.0
	
	return 2.0 * len(shrd) / len_all_pairs
	
def similarity_score(title1, title2, text1, text2):
	"""Get similarity percentage of two notes"""
	
	return (check_similarity_from_strings(title1, title2),
			check_similarity_from_strings(text1, text2))

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
			text2=note2.text)
		
		if sum(similarity) > 0:
			sorted_list.append([
				similarity[1]*100,
				similarity[0]*100,
				(note, note2)])
	
	sorted_list.sort(key=lambda x: (x[0]+x[1])/2.0) # Sort list of notes
	sorted_list.reverse() # Reverse the list of notes
	return sorted_list

def check_similarity_list(note, notes=Note.objects.all()):
	"""Get sorted list of similiar notes"""
	
	sorted_list = [] # This is the future sorted list
	
	for note2 in notes: # Iterate over notes
		if note2.id == note.id: # If first note is equal to second note
			continue # Start next iteration
		
		similarity = similarity_score(
			title1=note.title,
			title2=note2.title,
			text1=note.text,
			text2=note2.text)
		
		if sum(similarity) > 0:
			sorted_list.append([
				similarity[1]*100,
				similarity[0]*100,
				({
					"id": note.id,
					"title": note.title,
					"text": note.text,
					"tags": transform_tags_single(note.tags)},
				{
					"id": note2.id,
					"title": note2.title,
					"text": note2.text,
					"tags": transform_tags_single(note2.tags)})])
	
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
			text2=note.text)
		
		if sum(similarity) > 0:
			sorted_list.append([
				similarity[1]*100,
				similarity[0]*100,
				("<Note: {title}>".format(title=title), note)])
	
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
					[note.title,
					note.text,
					transform_tags_single(note.tags)])])
	
	# Sort list of notes
	sorted_list.sort(key=lambda x: (x[0]+x[1])/2.0, reverse=True)
	
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
			if tags[i].startswith(" "):
				if len(tags[i]) > 1:
					tags[i] = tags[i][1:]
	return tags

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
