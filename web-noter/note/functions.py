#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys # To check Python version

from note.models import Note # To get notes from server's database

from django.core.exceptions import ObjectDoesNotExist

import Diff # To find similiar notes

from django.contrib.auth import authenticate

from django.core import serializers

from django.http import HttpResponse, Http404

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User

import re, json

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
	
	return s.replace("\n\r", "<br/>").replace("\n", "<br/>").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

def replaceNewLines(obj):
	"""Replace all the newlines (\n) in notes by <br/> HTML tags"""
	
	for i in range(len(obj.object_list)):
		if obj.object_list[i].type != "s":
			obj.object_list[i].text = replaceNewLinesString(obj.object_list[i].text)
	return obj

def replaceNewLinesSearch(obj):
	"""Replace all the newlines (\n) in notes by <br/> HTML tags.
Works only with lists ([7.2, <Note>])."""
	
	for i in range(len(obj.object_list)):
		if obj.object_list[i][1].type != "s":
			obj.object_list[i][1].text = replaceNewLinesString(obj.object_list[i][1].text)
	return obj

def replaceNewLinesSingleObject(obj):
	"""Replace all the newlines (\n) in note by <br/> HTML tags"""
	if obj.type != "s":
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
	note = replaceNewLinesSingleObject(note)
	title = note.title.lower()
	text = note.text.lower()
	tags = note.tags.lower()
	q_in = 0
	for i in q:
		count_prev = count
		count -= note.title.count(i)
		count -= note.text.count(i)
		count -= note.tags.count(i)
		if count < count_prev:
			q_in += 1 
		if q_in > 1:
			count *= q_in
	return [
		count,
		note
	]

def to_json(success="true", **kwargs):
	response = '{"success": %s' %success
	for arg in kwargs:
		response += ', "{arg}": {value}'.format(arg=arg, value=kwargs[arg])
	response += "}"
	
	return response

def JsonResponse(success="true", **kwargs):
	return HttpResponse(to_json(success, **kwargs))

def API_authenticate(request):
	assert "username" in request.POST or "email" in request.POST, "Authentication Failed: username or/and email are missing"
	assert "password" in request.POST, "Authentication failed: paassword is missing"
	if "username" in request.POST:
		username = request.POST["username"]
	else:
		username = None
		if "email" in request.POST:
			email = request.POST["email"]
		else:
			email = None
	
	password = request.POST["password"]
	
	user = authenticate(username=username, password=password)
	assert user is not None, "Authentication failed: wrong username/email or password"
	return user

@csrf_exempt
def API_getNotes(request):
	try:
		user = API_authenticate(request)
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	
	notes = Note.objects.filter(author=user)
	
	notes_json = serializers.serialize("json", notes)
	
	return HttpResponse(notes_json)

def id_of_note(request):
	return request.POST["id"]

def type_of_note(request):
	return request.POST["type"]

def title_of_note(request):
	return request.POST["title"]

def text_of_note(request):
	return request.POST["text"]

def tags_of_note(request):
	return request.POST["tags"]

def registration_data(request):
	assert "username" in request.POST, "Username is missing"
	assert "first_name" in request.POST, "First name is missing"
	assert "last_name" in request.POST, "Last name is missing"
	assert "email" in request.POST, "Email address is missing"
	assert "password" in request.POST, "Password is missing"
	assert "confirm_password" in request.POST, "Password isn't confirmed"
	
	username = request.POST["username"]
	first_name = request.POST["first_name"]
	last_name = request.POST["last_name"]
	email = request.POST["email"]
	password = request.POST["password"]
	confirm_password = request.POST["confirm_password"]
	
	email_validator = re.compile("[a-zA-Z\.]+@[a-zA-Z\.]+")
	
	assert len(first_name) < 150, "First name cannot be longer than 150 symbols"
	assert first_name, "First name cannot be empty"
	assert len(last_name) < 150, "Last name cannot be longer than 150 symbols"
	assert last_name, "Last name cannot be empty"
	assert len(username) < 150, "Username cannot be longer than 150 symbols"
	assert username, "Username cannot be empty"
	assert re.match(email_validator, email) is not None, "Invalid email"
	assert password, "Password cannot be empty"
	assert confirm_password == password or confrim_password, "Password isn't confirmed"
	
	dictionary = {
		"username": username,
		"first_name": first_name,
		"last_name": last_name,
		"email": email,
		"password": password,
		"confirm_password": confirm_password
	}
	
	return dictionary

@csrf_exempt
def API_addNote(request):
	try:
		user = API_authenticate(request)
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	try:
		assert "type" in request.POST, "Type is missing"
		assert request.POST["type"] in ["n", "t", "s", "w"], "Type should be n(ote), t(odo), s(nippet) or w(arning)"
		assert "text" in request.POST, "Text is missing"
		assert "title" in request.POST, "Title is missing"
		assert "tags" in request.POST, "Tags are missing"
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	type_ = type_of_note(request)
	title = title_of_note(request)
	text = text_of_note(request)
	tags = tags_of_note(request)
	
	new_note = Note.objects.create(title=title, text=text, tags=tags, type=type_, author=user)
	try:
		new_note.save()
	except Exception as e:
		return JsonResponse("false", message='"Failed to save note: %s"' %e)
	
	return JsonResponse("true", id=new_note.id)

@csrf_exempt
def API_addNotes(request):
	try:
		user = API_authenticate(request)
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	try:
		assert "list" in request.POST, "List of notes is missing"
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	json_list = json.loads(request.POST["list"])
	added = []
	
	for n in json_list:
		title = n["title"]
		text = n["text"]
		tags = n["tags"]
		type_ = n["type"]
		new_note = Note.objects.create(title=title, text=text, tags=tags, type=type_, author=user)
		try:
			new_note.save()
			added.append(new_note.id)
		except Exception as e:
			return JsonResponse("false", message='"Failed to add note: %s"' %new_note.id)
		
		j = "{%s" %added[0]
		for i in added[1:]:
			j += ", %s" %i
		j += "}"
	
	return JsonResponse("true", saved=j)


@csrf_exempt
def API_rmNote(request):
	try:
		user = API_authenticate(request)
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	
	try:
		assert "id" in request.POST, "ID is missing"
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	id_ = id_of_note(request)
	try:
		note = Note.objects.get(id=id_, author=user)
		note.delete()
	except ObjectDoesNotExist:
		return JsonResponse("false", message='"Object does not exist"', id=id_)
	
	return JsonResponse("true", id=id_)

@csrf_exempt
def API_rmNotes(request):
	try:
		user = API_authenticate(request)
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	
	try:
		assert "list" in request.POST, "List of IDs is missing"
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	list_ = request.POST["list"].split(", ")
	deleted = {}
	
	for j in list_:
		try:
			note = Note.objects.get(id=j, author=user)
			note.delete()
			deleted[int(j)] = True
		except ObjectDoesNotExist:
			deleted[int(j)] = False
	
	deleted_json = json.dumps(deleted)
	
	return HttpResponse(deleted_json)

@csrf_exempt
def API_register(request):
	try:
		data = registration_data(request)
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	
	username = data['username']
	first_name = data['first_name']
	last_name = data['last_name']
	email = data['email']
	password = data['password']
	
	new_user = User.objects.create(
		username=username,
		first_name=first_name,
		last_name=last_name,
		email=email
	)
	
	new_user.set_password(password)
	new_user.save()
	
	return JsonResponse(
		"true",
		userid=new_user.id,
		username='"'+username+'"',
		first_name='"'+first_name+'"',
		last_name='"'+last_name+'"',
		email='"'+email+'"'
	)

@csrf_exempt
def API_deleteAccount(request):
	try:
		user = API_authenticate(request)
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	
	user_id = user.id
	
	user_notes = Note.objects.filter(author=user)
	
	user_notes.delete()
	user.delete()
	
	return JsonResponse("true", id=user_id)
