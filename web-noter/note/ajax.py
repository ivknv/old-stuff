#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse # To send data to browser

from django.shortcuts import redirect

from note.models import Note # To get notes from server's database

from django.db.models import Q # To make search results better

from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from django.db import OperationalError

from note.functions import replaceNone, checkSimilarityFromStringList

from django.template import RequestContext

import json # To send AJAX answers

def addNote(request):
	"""Add note"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		return redirect('/login?return={}'.format(request.path))
	
	if "title" in request.POST and "text" in request.POST and "tags" in request.POST and "type" in request.POST:
 # If using POST method and all the variables are on their own places
		title = request.POST["title"]
		text = request.POST["text"]
		tags = request.POST["tags"]
		type = request.POST["type"]
		
		context = {"title": title, "text": text, "tags": tags, "type": type}
		
		try: # Sometimes note cannot be added
			new_note = Note.objects.create(
				title=title,
				text=text,
				tags=tags,
				type=type,
				author=request.user
			) # Create note in a server's database
			new_note.save() # Save it
		except Exception as e: # If error occured
			context["failed"] = True # Set failed status
			print(e)
		else: # If there's no errors
			context["failed"] = False # Set not failed status
		if context["failed"]:
			return render_to_response('/add/', {
				"title": title,
				"text": text,
				"tags": tags,
				"type": type
			}, context_instance=RequestContext(request))
		return redirect("/manage/")
	
	raise HttpResponse("Wrong parameters") # Display '404 Not Found' error

def rmNote(request):
	"""Remove note"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		raise Http404 # Display '404 Not Found' error
	if request.POST and request.POST["id"]: # If using POST method and have ID
		
		context={"success": True}
		
		try: # ID of the note can be invalid
			note_id = int(request.POST["id"]) # Convert string to integer
			context["id"] = note_id
		except TypeError: # If ID is invalid
			context["success"] = False # Set status failed
		else: # If there's no errors
			try: # Note may not exist or be impossible to delete
				note = Note.objects.get(id=note_id) # Get note from server's database
				note.delete() # Delete note from server's database
			except: # If it's impossible to delete note (remember: there's nothing impossible. So 'impossible' is just a fake excuse)
				context["success"] = False
		return HttpResponse(json.dumps({"success": True}))
	raise Http404 # Display '404 Not Found' error

def update(request):
	"""Edit note"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		return redirect("/login")
	
	if request.POST and "id" in request.POST and ("title" in request.POST or "text" in request.POST or "tags" in request.POST or "type" in request.POST or "checked" in request.POST): # If using POST method and all the variables on their own places
		try: # Sometimes ID can be invalid
			note_id = int(request.POST["id"]) # Convert string to integer
		except TypeError: # If ID is still invalid
			raise Http404 # Display '404 Not Found' error
		
		try: # Sometimes note may not even exist
			note = Note.objects.get(id=note_id) # Get note by ID from server's database
		except ObjectDoesNotExist: # If note is actually doesn't exist
			raise Http404 # Display '404 Not Found' error
		if "title" in request.POST and request.POST["title"]: # If there's title
			title = request.POST["title"]
		else: # If there's note title
			title = note.title # Set it equal to title of this note or in other words - do not change it
		if "text" in request.POST and request.POST["text"]: # Same as with title but instead of title there's text
			text = request.POST["text"]
		else:
			text = note.text
		if "tags" in request.POST: # Same as with title and text
			tags = request.POST["tags"]
		else:
			tags = note.tags
		if "type" in request.POST:
			type = request.POST["type"]
		else:
			type = "Note"
		if "checked" in request.POST:
			is_checked = True if request.POST["checked"] == "true" else False
		else:
			is_checked = note.is_checked
			
		assert is_checked == False or is_checked == True, "is_checked shall be True of False but it's not: %s" %type(is_checked)
		if type == "Todo" and not is_checked:
			is_checked = not is_checked
		
		context = {
			"id": note_id, # ID of the note
			"title": title, # Title of the note
			"text": text, # Text of the note
			"type": type,
			"is_checked": is_checked
		}
		
		# Update note
		note.title = title
		note.text = text
		note.tags = tags
		note.type = type
		note.is_checked = is_checked
		
		try: # Sometimes you just cannot save your note.
			# ...But not with Noter!
			note.save() # Save the note
		except Exception as e: # If error occurred
			context["failed"] = True # Set failed status
			print(e)
		else: # If there's no errors
			context["failed"] = False # Set not failed status
		
		return HttpResponse(json.dumps(context)) # Return JSON object
		
	raise Http404 # Display '404 Not Found' error

def checkSimilarityAjax(request):
	"""Get sorted list of similiar notes.
Can be called by AJAX request"""
	
	if "id" in request.POST and "text" in request.POST and "title" in request.POST: # If using POST method and all the values on their own places
		id = request.POST["id"]
		text = request.POST["text"]
		title = request.POST["title"]
		context = {"text": text, "title": title} # This is the future JSON object
		top3 = checkSimilarityFromStringList(id, text, title)[0:3] # Top 3 similiar notes
		context["top3"] = top3
		
		return HttpResponse(json.dumps(context)) # Return JSON object
	# If using some other request method or not having values on its own place
	raise Http404 # Display '404 Not Found' error

def update_username(request):
	if not request.user.is_authenticated():
		return redirect('/login/?redirect=%2F')
	
	if "id" in request.POST and "new_username" in request.POST:
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
		
	raise Http404

def update_first_name(request):
	if not request.user.is_authenticated():
		return redirect('/login/?redirect=%2F')
	
	if "id" in request.POST and "new_first_name" in request.POST:
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
		
	raise Http404

def update_last_name(request):
	if not request.user.is_authenticated():
		return redirect('/login/?redirect=%2F')
	
	if "id" in request.POST and "new_last_name" in request.POST:
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
		
	raise Http404

def update_password(request):
	if not request.user.is_authenticated():
		return redirect('/login/?redirect=%2F')
	
	if "id" in request.POST and "new_password" in request.POST and "confirm_password" in request.POST and "current_password" in request.POST:
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
		
	raise Http404
