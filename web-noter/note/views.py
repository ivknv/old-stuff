from django.shortcuts import render_to_response # To render templates

from django.http import Http404, HttpResponse # To send data to browser

from note.models import Note # To get notes from server's database

from django.core.paginator import Paginator, EmptyPage # To split content into pages

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q # To make search results better

from django.template import RequestContext

import json # To send AJAX answers

from note.functions import *

from note.ajax import *

def home(request, pn=1):
	"""Home page"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		raise Http404 # Display '404 Not Found' error
	
	try:
		pn = int(pn)
	except ValueError:
		pn = 1

	notes = Note.objects.all() # Get all the notes
	
	p = Paginator(notes, 10) # Split into pages
	
	if pn > p.num_pages: # if current page number is too big show 404 error
		raise Http404
	
	current_page = replaceNewLines(p.page(pn)) # Replace all the newlines by <br/> HTML tags
	prange = page_range(pn, p.num_pages) # Generate page range
	context = {
		"notes": current_page, # Content of current page
		"current_page_number": pn, # Current page number
		"num_pages": p.num_pages, # Number of pages
		"page_range": prange # Pages that will be displayed
	}
	return render_to_response("home.html", context) # Render page

def getNote(request, id):
	"""Get Note by id.
It's a page"""
	
	if not request.user.is_authenticated(): # If user isn't logged in
		raise Http404 # Display '404 Not Found' error
	
	try: # Sometimes there's no such note
		note = Note.objects.get(id=id) # Get note by ID
		note = replaceNewLinesSingleObject(note) # Replace newlines by <br/>
	except ObjectDoesNotExist: # I've already said that sometimes note may not exist
		raise Http404 # Display '404 Not Found' error
	
	try: # Sometimes note can be latest
		next_note = note.get_next_by_date() # Get next note
	except ObjectDoesNotExist: # If there's no next note
		next_note = None # Next note will be None
	
	try: # Sometimes note can be first
		previous_note = note.get_previous_by_date() # Get previous note
	except ObjectDoesNotExist: # If there's no previous note
		previous_note = None # Previous note will be None
	
	context = {
		"note": note, # Note object
		"next": next_note, # Next note object
		"previous": previous_note # Previous note object
	}
	return render_to_response("note.html", context) # Render page

def addNote_page(request):
	"""Add note page"""

	if not request.user.is_authenticated(): # If user is not logged in
		raise Http404 # Display '404 Not Found' error
	
	return render_to_response("add_note.html", {}) # Render page

def manageNotes(request, pn=1):
	"""Manage notes"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		raise Http404 # Display '404 Not Found' error
	
	try:
		pn = int(pn)
	except ValueError: # If page number is not set
		pn = 1 # Go to the first page
	
	notes = Note.objects.all() # Get all the notes
	p = Paginator(notes, 10) # Split notes into pages
	
	try: # Page number can be too big
		current_page = replaceNewLines(p.page(pn)) # Set current page content & Replace all the newlines by <br/>
	except EmptyPage: # If page number is too big
		raise Http404 # Display '404 Not Found' error
	
	prange = page_range(pn, p.num_pages) # Generate page range
	
	context = {
		"notes": current_page, # Current page content
		"current_page_number": pn, # Current page number
		"num_pages": p.num_pages, # Number of pages
		"page_range": prange # Page range
	}
	
	return render_to_response("manage.html", context) # Render page

def edit(request, id):
	"""Edit note. It's a page"""
	
	if not request.user.is_authenticated(): # If user isn't logged in
		raise Http404 # Display '404 Not Found' Error
	
	try: # Sometimes we confuse the digit with a string
		note_id = int(id) # Convert string into integer
		try: # Sometimes we request something that doesn't exist
			note = Note.objects.get(id=note_id) # Get a note from server's database
		except ObjectDoesNotExist: # If somebody mistaken with existence of the note
			raise Http404 # Well, in this case the only thing server has to say is '404 Not Found'
		note.tags = replaceNone(note.tags) # Replace tags with None value with empty string
	except TypeError: # If somebody confused the digit with the string (Sometimes it happens)
		raise Http404 # I will raise the great '404 Not Found' error!
	
	note.text = note.text.replace("\\n", "\n")
	similiar = checkSimilarity(note)[0:3] # Top 3 similiar notes
	similiar = transformTags(similiar) # Split tags separated with commas into a list
	context = {
		"note": note, # Note object
		"similiar": similiar # Top 3 similiar notes
	}
	
	return render_to_response("edit.html", context) # Render page

def search(request, q, pn=1):
	"""Search for notes (AJAX)"""
	
	context = {"errors": [], "q": q}
	
	# Define error messages
	too_long_error = "Search query can contain no more than 150 symbols"
	empty_error = "Search query cannot be empty"
	
	if q:
		q = q.lower()
		qs = q.split()
		context["qs"] = qs
		
		if len(q) > 150: # If search query is too long
			context["errors"].append(too_long_error) # Append error
		
		try: # Page number can be invalid
			pn = int(pn) # Try to convert string to integer
		except TypeError: # If page number is invalid
			pn = 1 # Go to first page
		
	else: # If search query is empty
		context["errors"].append(empty_error) # Append error
	
	if not context["errors"]: # If there's no errors
		found = []
		for i in qs:
			found_ = Note.objects.filter( # Filter notes
				Q(title__icontains=i) |
				Q(text__icontains=i) |
				Q(tags__icontains=i)
			)
			for note in found_:
				if not note in found:
					found.append(note)
		sorted_found = [] # Will contain sorted results later
		
		for note in found: # Iterate over found notes
			note.tags = replaceNone(note.tags) # Replace None in tags by empty string
			sorted_found.append(PlaceByRelevance(note, qs, splitted=True, lower=True)) # Place by relevance
			
		sorted_found.sort()	# Sort notes
		
		try: # Page number can be too big
			p = Paginator(sorted_found, 10) # Split content into pages
			found = replaceNewLinesSearch(p.page(pn)) # Replace newlines (\n, \\n) by <br/>
		except EmptyPage: # If page number is too big
			raise Http404 # Display '404 Not found' error
		
		prange = page_range(pn, p.num_pages) # Generate page range
		
		# Pack context
		context["found"] = found # Set list with found notes
		context["num_pages"] = p.num_pages # Set number of pages
		context["current_page_number"] = pn # Set current page number
		context["page_range"] = prange # Set page range
		
		return render_to_response("search.html", context)

def filter(request, tags="", pn=1):
	context = {}
	context["tags"] = tags
	if tags:
		context["tags"] = tags+"/"
	tags = replaceNone(transformTagsSingle(tags))
	
	notes = Note.objects.all()
	filtered = []
	
	for note in notes:
		ntags = replaceNone(transformTagsSingle(note.tags))
		if tags:
			for tag in tags:
				if tag in ntags:
					have_tag = True
				else:
					have_tag = False
					break
			if have_tag:
				filtered.append(note)
		else:
			filtered.append(note)
	
	try:
		pn = int(pn)
	except ValueError:
		pn=1
	
	p = Paginator(filtered, 10)
	filtered_page = replaceNewLines(p.page(pn))
	prange = page_range(pn, p.num_pages)

	context["filtered"] = filtered_page
	context["current_page_number"] = pn
	context["num_pages"] = p.num_pages
	context["page_range"] = prange
	context["urlprefix"] = ""

	return render_to_response("filter.html", context)

def filterDone(request, tags="", pn=1):
	context = {}
	context["tags"] = tags
	if tags:
		context["tags"] = tags+"/"
	tags = replaceNone(transformTagsSingle(tags))
	
	notes = Note.objects.filter(is_todo=True, is_checked=True)
	filtered = []
	
	for note in notes:
		ntags = replaceNone(transformTagsSingle(note.tags))
		if tags:
			for tag in tags:
				if tag in ntags:
					have_tag = True
				else:
					have_tag = False
					break
			if have_tag:
				filtered.append(note)
		else:
			filtered.append(note)
	
	try:
		pn = int(pn)
	except ValueError:
		pn=1
	
	p = Paginator(filtered, 10)
	filtered_page = replaceNewLines(p.page(pn))
	prange = page_range(pn, p.num_pages)

	context["filtered"] = filtered_page
	context["current_page_number"] = pn
	context["num_pages"] = p.num_pages
	context["page_range"] = prange
	context["done_or_undone"] = " checked"
	context["urlprefix"] = "done"

	return render_to_response("filter.html", context)

def filterUndone(request, tags="", pn=1):
	context = {}
	context["tags"] = tags
	if tags:
		context["tags"] = tags+"/"
	tags = replaceNone(transformTagsSingle(tags))
	
	notes = Note.objects.filter(is_todo=True, is_checked=False)
	filtered = []
	
	for note in notes:
		ntags = replaceNone(transformTagsSingle(note.tags))
		if tags:
			for tag in tags:
				if tag in ntags:
					have_tag = True
				else:
					have_tag = False
					break
			if have_tag:
				filtered.append(note)
		else:
			filtered.append(note)
	
	try:
		pn = int(pn)
	except ValueError:
		pn=1
	
	p = Paginator(filtered, 10)
	filtered_page = replaceNewLines(p.page(pn))
	prange = page_range(pn, p.num_pages)

	context["filtered"] = filtered_page
	context["current_page_number"] = pn
	context["num_pages"] = p.num_pages
	context["page_range"] = prange
	context["done_or_undone"] = " unchecked"
	context["urlprefix"] = "undone"

	return render_to_response("filter.html", context)


def contact(request):
	
	if "text" in request.POST and "subject" in request.POST:
		return HttpResponse("Thanks. <a href='/contact/'>Back</a>")
	
	return render_to_response("contact.html", RequestContext(request, {}))

def about(request):
	return render_to_response("about.html", {})
