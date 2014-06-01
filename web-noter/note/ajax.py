#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov

This module contains methods that called from JavaScript via AJAX requests
"""

from django.http import Http404, HttpResponse # To send data to browser

from django.shortcuts import redirect, render_to_response

from note.models import Note # To get notes from server's database

from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from django.db import OperationalError

from note.functions import check_similarity_from_string_list

from django.template import RequestContext

import json # To send AJAX answers

def add_note(request):
	"""Add note"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		return redirect('/login?return={}'.format(request.path))
	
	try:
		assert "title" in request.POST, "Title is missing"
		assert "text" in request.POST, "Text is missing"
		assert "tags" in request.POST, "Tags are missing"
		assert "type" in request.POST, "Type is missing"
	except AssertionError:
		raise HttpResponse("Wrong parameters")	

	title = request.POST["title"]
	text = request.POST["text"]
	tags = request.POST["tags"]
	type_ = request.POST["type"]
	
	context = {
		"title": title,
		"text": text,
		"tags": tags,
		"type": type_
	}
	
	try:
		new_note = Note.objects.create(
			title=title,
			text=text,
			tags=tags,
			type=type_,
			author=request.user
		)
		new_note.save()
	except OperationalError as error:
		context["failed"] = True
		print(error)
	else: # If there's no errors
		context["failed"] = False # Set not failed status
	
	if context["failed"]:
		return render_to_response('/add/', {
			"title": title,
			"text": text,
			"tags": tags,
			"type": type_
		}, context_instance=RequestContext(request))
	
	return redirect("/manage/")

def remove_note(request):
	"""Remove note"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		raise Http404 # Display '404 Not Found' error
	
	if "id" in request.POST and request.POST["id"]:
		
		context = {"success": True}
		
		try: # ID of the note can be invalid
			note_id = int(request.POST["id"]) # Convert string to integer
			context["id"] = note_id
		except TypeError: # If ID is invalid
			context["success"] = False # Set status failed
		else: # If there's no errors
			try: # Note may not exist or be impossible to delete
				note = Note.objects.get(id=note_id)
				note.delete()
			except OperationalError as error:
				context["success"] = False
				print(error)
			
		return HttpResponse(json.dumps({"success": True}))
	raise Http404 # Display '404 Not Found' error

def update(request):
	"""Edit note"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		return redirect("/login")
	
	try:
		assert "id" in request.POST, "ID is missing"
		assert "title" in request.POST or "text" in request.POST \
		or "tags" in request.POST or "type" in request.POST \
		or "checked" in request.POST, "Nothing to edit"
	except AssertionError:
		raise Http404
	
	try: # Sometimes ID can be invalid
		note_id = int(request.POST["id"]) # Convert string to integer
	except TypeError: # If ID is still invalid
		raise Http404 # Display '404 Not Found' error
	
	try: # Sometimes note may not even exist
		note = Note.objects.get(id=note_id)
	except ObjectDoesNotExist:
		raise Http404 # Display '404 Not Found' error
	if "title" in request.POST and request.POST["title"]:
		title = request.POST["title"]
	else:
		title = note.title
	if "text" in request.POST and request.POST["text"]:
		text = request.POST["text"]
	else:
		text = note.text
	if "tags" in request.POST:
		tags = request.POST["tags"]
	else:
		tags = note.tags
	if "type" in request.POST:
		type_ = request.POST["type"]
	else:
		type_ = "n"
	if "checked" in request.POST:
		is_checked = True if request.POST["checked"] == "true" else False
	else:
		is_checked = note.is_checked
	
	try:
		assert is_checked == False or is_checked == True, \
		"is_checked shall be True of False but it's not: %s" %type(is_checked)
	except AssertionError:
		is_checked = False
	
	if type_ != "t" and not is_checked:
		is_checked = not is_checked
		
	context = {
		"id": note_id, # ID of the note
		"title": title, # Title of the note
		"text": text, # Text of the note
		"type": type_,
		"is_checked": is_checked
	}
	
	# Update note
	note.title = title
	note.text = text
	note.tags = tags
	note.type = type_
	note.is_checked = is_checked
	
	try:
		note.save()
	except OperationalError as error:
		context["failed"] = True
		print(error)
	else:
		context["failed"] = False
		return HttpResponse(json.dumps(context)) # Return JSON object
		
	raise Http404 # Display '404 Not Found' error

def check_similarity_ajax(request):
	"""Get sorted list of similiar notes.
Can be called by AJAX request"""
	
	try:
		assert "id" in request.POST, "ID is missing"
		assert "text" in request.POST, "Text is missing"
		assert "title" in request.POST, "Title is missing"
	except AssertionError:
		raise Http404
	
	id_ = request.POST["id"]
	text = request.POST["text"]
	title = request.POST["title"]
	context = { # This is the future JSON object
		"text": text,
		"title": title
	}
	top3 = check_similarity_from_string_list( # top 3 similiar notes
		id_,
		text,
		title
	)[0:3]
	
	context["top3"] = top3
	
	return HttpResponse(json.dumps(context))

def update_username(request):
	"""Update username"""
	
	if not request.user.is_authenticated():
		return redirect('/login/?redirect=%2F')
	
	try:
		assert "id" in request.POST, "ID is missing"
		assert "new_username" in request.POST, "New username is missing"
	except AssertionError:
		raise Http404
	
	userid = request.POST["id"]
	try:
		user = User.objects.get(id=userid)
	except ObjectDoesNotExist:
		success = False
	else:
		new_username = request.POST["new_username"]
		if new_username:
			user.username = new_username
			user.save()
			success = True
		else:
			success = False
	
	context = {
		"success": success,
		"result": "Current username: %s" %user.username,
		"eid":  "#current_username"
	}
	
	return HttpResponse(json.dumps(context))

def update_first_name(request):
	"""Update user's first name"""
	
	if not request.user.is_authenticated():
		return redirect('/login/?redirect=%2F')
	
	try:
		assert "id" in request.POST, "ID is missing"
		assert "new_first_name" in request.POST, "New first name is missing"
	except AssertionError:
		raise Http404
	
	userid = request.POST["id"]
	try:
		user = User.objects.get(id=userid)
	except ObjectDoesNotExist:
		success = False
	else:
		new_first_name = request.POST["new_first_name"]
		if new_first_name:
			user.first_name = new_first_name
			user.save()
			success = True
		else:
			success = False
	
	context = {
		"success": success,
		"result": "Current first name: %s" % user.first_name,
		"eid": "#current_first_name"
	}
	
	return HttpResponse(json.dumps(context))

def update_last_name(request):
	"""Update user's last name"""
	
	if not request.user.is_authenticated():
		return redirect('/login/?redirect=%2F')
	
	try:
		assert "id" in request.POST, "ID is missing"
		assert "new_last_name" in request.POST, "New last name is missing"
	except AssertionError:
		raise Http404
	
	userid = request.POST["id"]
	try:
		user = User.objects.get(id=userid)
	except ObjectDoesNotExist:
		success = False
	else:
		new_last_name = request.POST["new_last_name"]
		if new_last_name:
			user.last_name = new_last_name
			user.save()
			success = True
		else:
			success = False
	
	context = {
		"success": success,
		"result": "Current last name: %s" %user.last_name,
		"eid": "#current_last_name"
	}
	
	return HttpResponse(json.dumps(context))

def update_password(request):
	"""Update user's password"""
	
	if not request.user.is_authenticated():
		return redirect('/login/?redirect=%2F')
	
	try:
		assert "id" in request.POST, "ID is missing"
		assert "new_password" in request.POST, "New password is missing"
		assert "confirm_password" in request.POST, "New password isn't confirmed"
		assert "current_password" in request.POST, "Current password is missing"
	except AssertionError:
		raise Http404
	
	userid = request.POST["id"]
	try:
		user = User.objects.get(id=userid)
	except ObjectDoesNotExist:
		success = False
	else:
		new_password = request.POST["new_password"]
		confirm_password = request.POST["confirm_password"]
		current_password = request.POST["current_password"]
		password_is_correct = user.check_password(current_password)
		
		if password_is_correct and new_password and confirm_password == new_password:
			user.set_password(new_password)
			user.save()
			success = True
		else:
			success = False
	
	context = {
		"success": success,
		"result": "",
		"eid": ""
	}
	
	return HttpResponse(json.dumps(context))
