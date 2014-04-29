#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys # To check Python version

from note.models import Note # To get notes from server's database

from django.core.exceptions import ObjectDoesNotExist

import Diff # To find similiar notes

if sys.version_info.major < 3: # If version of Python is lower than 3
	range=xrange # Use xrange instead of range

def similarityPercentage(title1, title2, text1, text2):
	"""Get similarity percentage of two notes"""
	
	return (Diff.checkSimilarityWords2(text1, text2)+Diff.checkSimilarityWords2(title1, title2))/2

def checkSimilarity(note, notes=Note.objects.all()):
	"""Get sorted list of similiar notes"""
	
	sorted_list = [] # This is the future sorted list
	
	for n in notes: # Iterate over notes
		if n.id == note.id: # If first note is equal to second note
			continue # Start next iteration
		
		sorted_list.append([
			similarityPercentage(title1=note.title,
			title2=n.title,
			text1=note.text,
			text2=n.text),
			(note, n)
		])
	
	sorted_list.sort() # Sort list of notes
	sorted_list.reverse() # Reverse the list of notes
	return sorted_list

def checkSimilarityFromString(text, title, notes=Note.objects.all()):
	"""Get sorted list of similiar notes from string"""
	
	sorted_list = [] # This is the future sorted list
	
	for note in notes: # Iterate over notes
		sp = similarityPercentage(title1=title,
			title2=note.title,
			text1=text,
			text2=note.text)
		if sp > 15:
			sorted_list.append([
				sp,
				("<Note: {title}>".format(title=title), note)
			])
	
	sorted_list.sort() # Sort list of notes
	sorted_list.reverse() # Reverse the list of notes
	
	return sorted_list

def checkSimilarityFromStringList(id, text, title, notes=Note.objects.all()):
	"""Get sorted list of similiar notes from string.
Using lists instead of Note objects"""
	
	id = int(id)
	sorted_list = [] # This is the future sorted list
	
	for note in notes: # Iterate over notes
		if id == note.id:
			continue
		sp = similarityPercentage(title1=title,
			title2=note.title,
			text1=text,
			text2=note.text)
		if sp > 15:
			sorted_list.append([
				sp,
				("<Note: {title}>".format(title=title), [note.title, note.text, transformTagsSingle(replaceNone(note.tags))])
			])
	
	sorted_list.sort() # Sort list of notes
	sorted_list.reverse() # Reverse the list of notes
	
	return sorted_list

def page_range(pn, num_pages, max_next=3):
	"""Generate (x)range from pages"""
	
	return range(pn-max_next if num_pages > max_next and pn > max_next else 1, pn+max_next if num_pages > pn+max_next else pn+num_pages-pn+1 or num_pages)

def replaceNewLinesString(s):
	"""Replace all the newlines (\n) by <br/> in a string"""
	
	return s.replace("\n", "<br/>").replace(" ", "&nbsp;")

def replaceNewLines(obj):
	"""Replace all the newlines (\n) in notes by <br/> HTML tags"""
	
	for i in range(len(obj.object_list)):
		obj.object_list[i].text = replaceNewLinesString(obj.object_list[i].text)
	return obj

def replaceNewLinesSearch(obj):
	"""Replace all the newlines (\n) in notes by <br/> HTML tags.
Works only with lists ([7.2, <Note>])."""
	
	for i in range(len(obj.object_list)):
		obj.object_list[i][1].text = replaceNewLinesString(obj.object_list[i][1].text)
	return obj

def replaceNewLinesSingleObject(obj):
	"""Replace all the newlines (\n) in note by <br/> HTML tags"""
	
	obj.text = replaceNewLinesString(obj.text)
	return obj

def transformTags(notes):
	"""Transforms a string with commas into a list of tags"""
	
	for i in range(len(notes)): # Iterate over a list with index
		if notes[i][1][1].tags and not isinstance(notes[i][1][1].tags, list): # If tags aren't empty
			notes[i][1][1].tags = notes[i][1][1].tags.split(",") # Split it into the list
			for ii in range(len(notes[i][1][1].tags)):
				if notes[i][1][1].tags[ii][0] == " ":
					notes[i][1][1].tags[ii] = notes[i][1][1].tags[ii][1:]
	return notes # return the result

def transformTagsSingle(tags):
	"""Transforms a string with commas into a list of tags"""
	
	if tags and not isinstance(tags, list):
		tags = tags.split(",")
		for i in range(len(tags)):
			if tags[i][0] == " ":
				tags[i] = tags[i][1:]
	return tags # return the result

def replaceNone(tags):
	"""If tags column was added by ALTER TABLE command
tags can be empty (None object).
This function replaces tags with None value by empty string"""
	
	if tags == None: # If tags is a None object
		tags = "" # Set it equal to empty string
	
	return tags # Return result

def PlaceByRelevance(note, q, splitted=False, lower=False):
	"""Place notes by relevance"""
	if not lower:
		q = q.lower()
	if not splitted:
		q = q.split()
	count = 0
	tagcount = 0
	note = replaceNewLinesSingleObject(note)
	title = note.title.lower()
	text = note.text.lower()
	tags = note.tags.lower()
	q_in = 0
	for i in q:
		q_in += 1
		count -= note.title.count(i)
		count -= note.text.count(i)
		tagcount -= note.tags.count(i)
		if q_in > 1:
			count *= q_in**2
	tagcount *= 2
	return [
		count-tagcount,
		note
	]

#def PlaceByRelevanceList(note, q, splitted=False, lower=False):
#	"""Place notes by relevance"""
#	if not lower:
#		q = q.lower()
#	if not splitted:
#		q = q.split()
#	count = 0
#	tagcount = 0
#	note = replaceNewLinesSingleObject(note)
#	title = note.title.lower()
#	text = note.text.lower()
#	tags = note.tags.lower()
#	for i in q:
#		count -= title.count(i)*1.5
#		count -= text.count(i)
#		tagcount -= tags.count(i)
#	tagcount *= 2
#	return [
#		count-tagcount,
#		(note.id, note.title, note.text, note.tags, formatDate(note))
#	]

#def PlaceByRelevanceList(note, q):
#	"""Place notes by relevance"""
#	
#	return [
#		-note.title.lower().count(q)-note.text.lower().count(q)-(note.tags.lower().count(q)*1.5),
#		(note.id, note.title, note.text, note.tags, formatDateSearch(note.date))
#	]

# Date must look good
# So there must be a days of the week, not numbers
#weekdays = [
#	"Sunday",
#	"Monday",
#	"Tuesday",
#	"Wednesday",
#	"Thursday",
#	"Friday",
#	"Saturday"
#]
# And definetly there must be names of the months
#months = [
#	"January",
#	"February",
#	"March",
#	"April",
#	"May",
#	"June",
#	"Jule",
#	"August",
#	"Semptember",
#	"October",
#	"November",
#	"December"
#]

#def formatDate(note):
#	"""Make date look cool"""
#	
#	return weekdays[note.date.weekday()-1]+", "+note.date.strftime("%d ")+months[note.date.month-1]+note.date.strftime(" %Y %H:%M") # Date of the note
#
#def formatDateSearch(note):
#	"""Make date look cool"""
#	
#	return weekdays[note.date().weekday()-1]+", "+note.date().strftime("%d ")+months[note.date().month-1]+note.date().strftime(" %Y %H:%M") # Date of the note
