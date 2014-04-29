#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse # To send data to browser

from note.models import Note # To get notes from server's database

from django.db.models import Q # To make search results better

from django.core.exceptions import ObjectDoesNotExist

from django.db import OperationalError

from note.functions import replaceNone, checkSimilarityFromStringList

import json # To send AJAX answers

def addNote(request):
	"""Add note"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		raise Http404 # Display '404 Not Found' error
	
	if "title" in request.POST and "text" in request.POST and "tags" in request.POST and "todo" in request.POST:
 # If using POST method and all the variables on their own places
		title = request.POST["title"]
		text = request.POST["text"]
		tags = request.POST["tags"]
		is_todo = True if request.POST["todo"] == "true" else False
		
		context = {"title": title, "text": text, "tags": tags, "is_todo": is_todo}
		
		try: # Sometimes note cannot be added
			new_note = Note.objects.create(
				title=title,
				text=text,
				tags=tags,
				id=note_id,
				is_todo=is_todo) # Create note in a server's database
			new_note.save() # Save it
		except: # If error occured
			context["failed"] = True # Set failed status
		else: # If there's no errors
			context["failed"] = False # Set not failed status
		return HttpResponse(json.dumps(context)) # Return JSON object
	
	raise Http404 # Display '404 Not Found' error

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
	
	print("Called update")
	if not request.user.is_authenticated(): # If user is not logged in
		raise Http404 # Display '404 Not Found' error
	
	if request.POST and "id" in request.POST and ("title" in request.POST or "text" in request.POST or "tags" in request.POST or "todo" in request.POST or "checked" in request.POST): # If using POST method and all the variables on their own places
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
		if "todo" in request.POST:
			is_todo = True if request.POST["todo"] == "true" else False
			print(is_todo)
		else:
			is_todo = note.is_todo
		if "checked" in request.POST:
			is_checked = True if request.POST["checked"] == "true" else False
			print(is_checked)
		else:
			is_checked = note.is_checked
			
		assert is_todo == False or is_todo == True, "is_todo shall be True of False but it's not: %s" %type(is_todo)
		assert is_checked == False or is_checked == True, "is_checked shall be True of False but it's not: %s" %type(is_checked)
		if not is_todo and is_checked:
			is_checked = not is_checked
		
		context = {
			"id": note_id, # ID of the note
			"title": title, # Title of the note
			"text": text, # Text of the note
			"is_todo": is_todo,
			"is_checked": is_checked
		}
		
		# Update note
		note.title = title
		note.text = text
		note.tags = tags
		note.is_todo = is_todo
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

#def getNoteAjax(request):
#	"""Get note object"""
#	
#	if request.POST and "id" in request.POST and request.POST["id"]: # If ID is on its own place
#		context = {"failed": False} # Not failed by default
#		try: # Note may not exist
#			note = Note.objects.get(id=request.POST["id"]) # Get note from server's database
#		except ObjectDoesNotExist: # If note doesn't exist
#			raise Http404 # Display '404 Not Found' error
		# If note does exist
#		
		# Pack the future JSON object
#		context["id"] = note.id # ID of the note
#		context["title"] = note.title # Title of the note
#		
		# Date must look good
#		context["date"] = formatDate(note) # Format date
#		context["text"] = replaceNewLinesString(note.text) # Replace newlines by <br/> in text of the note
#		try: # Sometimes note can be latest
#			context["next"] = note.get_next_by_date().id # Get id of the next note
#		except ObjectDoesNotExist: # If note doesn't exist
			# Damn, I'm tired of all this comments!
#			context["next"] = note.id
#		
#		try: # Sometimes note can be first
			# - Can I have a break?
			# - ugh... Fine!
			# - Thanks! I'll be back in 15 minutes.
			# - What a lazy bastard.
			# - I'm still here!
			# - Forget what I said! Now go have your damn break!
			# 15 minutes later...
			# - Comment code? Again?
			# - Yep!
#			context["previous"] = note.get_previous_by_date().id # Get previous note
#		except ObjectDoesNotExist: # Sometimes note can be first as I said
#			context["previous"] = note.id
#		
#		return HttpResponse(json.dumps(context)) # Return JSON object
#	else: # If not using POST method or having problems with variables
#		raise Http404 # ugh... Display '404 Not GOD DAMN FOUND' ERROR! I'm tired of all this!

def checkSimilarityAjax(request):
	"""Get sorted list of similiar notes.
Can be called by AJAX request"""
	
	if "id" in request.POST and request.POST and "text" in request.POST and "title" in request.POST: # If using POST method and all the values on their own places
		id = request.POST["id"]
		text = request.POST["text"]
		title = request.POST["title"]
		context = {"text": text, "title": title} # This is the future JSON object
		top3 = checkSimilarityFromStringList(id, text, title)[0:3] # Top 3 similiar notes
		context["top3"] = top3
		
		return HttpResponse(json.dumps(context)) # Return JSON object
	# If using some other request method or not having values on its own place
	raise Http404 # Display '404 Not Found' error

#def searchAjax(request, q):
#	"""Search for notes (AJAX)"""
#	
#	context = {"errors": [], "q": q}
#	
	# Define error messages
#	too_long_error = "Search query can contain no more than 150 symbols"
#	empty_error = "Search query cannot be empty"
#	
#	if q:
#		q = q.lower()
#		context["q"] = q
#		qs = q.split()
#		context["qs"] = qs
#		
#		if len(q) > 150: # If search query is too long
#			context["errors"].append(too_long_error) # Append error
#		
#		if "p" in request.GET: # If page number is set
#			try: # Page number can be invalid
#				pn = int(request.GET["p"]) # Try to convert string to integer
#			except TypeError: # If page number is invalid
#				pn = 1 # Go to first page
#		else: # If page number is not set
#			pn = 1 # Go to first page
#	else: # If search query is empty
#		context["errors"].append(empty_error) # Append error
#	
#	if not context["errors"]: # If there's no errors
#		found = []
#		for i in qs:
#			found_ = Note.objects.filter( # Filter notes
#				Q(title__icontains=i) |
#				Q(text__icontains=i) |
#				Q(tags__icontains=i)
#			)
#			for note in found_:
#				if not note in found:
#					found.append(note)
#		sorted_found = [] # Will contain sorted results later
#		
#		for note in found: # Iterate over found notes
#			note.tags = replaceNone(note.tags) # Replace None in tags by empty string
#			sorted_found.append(PlaceByRelevanceList(note, qs, splitted=True, lower=True)) # Place by relevance
#			
#		sorted_found.sort()	# Sort notes
#		
#		context["found"] = sorted_found
#		
#	return HttpResponse(json.dumps(context))
