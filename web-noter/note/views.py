"""
@author: Ivan Konovalov

Views for Noter, Django site
"""

from django.shortcuts import render_to_response, redirect

from django.http import Http404, HttpResponse

from note.models import Note

from django.core.paginator import Paginator, EmptyPage

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from django.template import RequestContext

from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.views import password_reset, password_reset_confirm

from django.contrib.auth.models import User

from django.core.mail import send_mail

from note.functions import check_similarity, transform_tags

from note.functions import replace_none, htmlbody, place_by_relevance

from note.functions import replace_newlines, page_range

from note.functions import replace_newlines_single_object

from note.functions import replace_newlines_search, transform_tags_single

from note.functions import replace_newlines_sim, remove_tags_in_all_notes

def home(request, page_number=1):
	"""Home page"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		return redirect('/login?return={}'.format(request.path))
	
	try:
		page_number = int(page_number)
	except ValueError:
		page_number = 1

	notes = Note.objects.filter(author=request.user.id) # Get all the notes
	
	paginator = Paginator(notes, 10) # Split into pages
	
	if page_number > paginator.num_pages:
		raise Http404
	
	current_page = replace_newlines(paginator.page(page_number))
	prange = page_range( # Generate page range
		page_number,
		paginator.num_pages
	)
	context = {
		"notes": current_page, # Content of current page
		"current_page_number": page_number, # Current page number
		"num_pages": paginator.num_pages, # Number of pages
		"page_range": prange # Pages that will be displayed
	}
	return render_to_response("home.html", context) # Render page

def get_note(request, note_id):
	"""Get Note by id.
It's a page"""
	
	if not request.user.is_authenticated(): # If user isn't logged in
		return redirect('/login?return={}'.format(request.path))
	
	try: # Sometimes there's no such note
		note = Note.objects.get(author=request.user.id, id=note_id)
		note = replace_newlines_single_object(note) # Replace newlines by <br/>
	except ObjectDoesNotExist: # Sometimes note may not exist
		raise Http404 # Display '404 Not Found' error
	
	try: # Sometimes note can be latest
		next_note = note.get_next_by_date( # Get next note
			author=request.user.id
		)
	except ObjectDoesNotExist: # If there's no next note
		next_note = None # Next note will be None
	
	try: # Sometimes note can be first
		previous_note = note.get_previous_by_date( # Get previous note
			author=request.user.id
		)
	except ObjectDoesNotExist: # If there's no previous note
		previous_note = None # Previous note will be None
	
	context = {
		"note": note, # Note object
		"next": next_note, # Next note object
		"previous": previous_note # Previous note object
	}
	return render_to_response("note.html", context) # Render page

def add_note_page(request):
	"""Add note page"""

	if not request.user.is_authenticated(): # If user is not logged in
		return redirect('/login?return={}'.format(request.path))
	
	return render_to_response(
		"add_note.html",
		{},
		context_instance=RequestContext(request)
	)

def manage_notes(request, page_number=1):
	"""Manage notes"""
	
	if not request.user.is_authenticated(): # If user is not logged in
		return redirect('/login?return={}'.format(request.path))
	
	try:
		page_number = int(page_number)
	except ValueError: # If page number is not set
		page_number = 1 # Go to the first page
	
	notes = Note.objects.filter(author=request.user.id) # Get all the notes
	paginator = Paginator(notes, 10) # Split notes into pages
	
	try: # Page number can be too big
		current_page = replace_newlines(paginator.page(page_number))
	except EmptyPage: # If page number is too big
		raise Http404 # Display '404 Not Found' error
	
	prange = page_range( # Generate page range
		page_number,
		paginator.num_pages)
	
	context = {
		"notes": current_page, # Current page content
		"current_page_number": page_number, # Current page number
		"num_pages": paginator.num_pages, # Number of pages
		"page_range": prange # Page range
	}
	
	return render_to_response("manage.html", context) # Render page

def edit(request, note_id):
	"""Edit note. It's a page"""
	
	if not request.user.is_authenticated(): # If user isn't logged in
		return redirect('/login?return={}'.format(request.path))
	
	try: # Sometimes we confuse the digit with a string
		note_id = int(note_id) # Convert string into integer
		try: # Sometimes we request something that doesn't exist
			note = Note.objects.get( # Get note from database
				author=request.user,
				id=note_id
			)
		except ObjectDoesNotExist: # If note doesn't exist
			raise Http404
		note.tags = replace_none(note.tags)
	except TypeError: # If somebody confused the digit with the string
		raise Http404 # I will raise the great '404 Not Found' error!
	
	similiar = check_similarity(note)[0:3] # Top 3 similiar notes
	similiar = transform_tags(similiar) # Split tags into a list
	
	context = {
		"note": note, # Note object
		"similiar": similiar, # Top 3 similiar notes
	}
	
	return render_to_response("edit.html", context) # Render page

def search(request, query, page_number=1):
	"""Search for notes"""
	
	if not request.user.is_authenticated():
		return redirect('/login?return={}'.format(request.path))
	
	context = {"errors": [], "q": query}
	
	# Define error messages
	too_long_error = "Search query can contain no more than 150 symbols"
	empty_error = "Search query cannot be empty"
	
	if query:
		query = query.lower()
		query_splitted = query.split()
		context["qs"] = query_splitted
		
		if len(query) > 150: # If search query is too long
			context["errors"].append(too_long_error) # Append error
		
		try: # Page number can be invalid
			page_number = int(page_number) # Convert string to integer
		except TypeError: # If page number is invalid
			page_number = 1 # Go to first page
		
	else: # If search query is empty
		context["errors"].append(empty_error) # Append error
	
	if not context["errors"]: # If there's no errors
		found = []
		for i in query_splitted:
			found_ = remove_tags_in_all_notes(
				Note.objects.filter(
					Q(author=request.user.id) &
					(Q(title__icontains=i) |
					Q(text__icontains=i) |
					Q(tags__icontains=i))
				)
			)
			for note in found_:
				if not note in found:
					found.append(Note.objects.get(id=note.id))
		sorted_found = [] # Will contain sorted results later
		
		for note in found: # Iterate over found notes
			note.tags = replace_none(note.tags)
			sorted_found.append( # Place by relevance
				place_by_relevance(
					note,
					query_splitted,
					splitted=True,
					lower=True
				)
			)
			
		sorted_found.sort()	# Sort notes
		
		try: # Page number can be too big
			paginator = Paginator(sorted_found, 10) # Split content into pages
			found = replace_newlines_search( # Replace newlines (\n) by <br/>
				paginator.page(page_number)
			)
		except EmptyPage: # If page number is too big
			raise Http404 # Display '404 Not found' error
		
		prange = page_range( # Generate page range
			page_number,
			paginator.num_pages
		)
		
		# Pack context
		context["found"] = found # Set list with found notes
		context["num_pages"] = paginator.num_pages # Set number of pages
		context["current_page_number"] = page_number # Set current page number
		context["page_range"] = prange # Set page range
		
		return render_to_response("search.html", context)

def filter_all_notes(request, tags="", page_number=1):
	"""Filter all the notes"""
	
	if not request.user.is_authenticated():
		return redirect('/login?return={}'.format(request.path))

	context = {}
	context["tags"] = tags
	if tags:
		context["tags"] = tags+"/"
	tags = replace_none(transform_tags_single(tags))
	
	notes = Note.objects.filter(author=request.user.id)
	filtered = []
	
	for note in notes:
		ntags = replace_none(transform_tags_single(note.tags))
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
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	paginator = Paginator(filtered, 10)
	filtered_page = replace_newlines(paginator.page(page_number))
	prange = page_range(page_number, paginator.num_pages)

	context["filtered"] = filtered_page
	context["current_page_number"] = page_number
	context["num_pages"] = paginator.num_pages
	context["page_range"] = prange
	context["urlprefix"] = ""

	return render_to_response("filter.html", context)

def filter_done(request, tags="", page_number=1):
	"""Filter checked todo notes"""

	if not request.user.is_authenticated():
		return redirect('/login?return={}'.format(request.path))

	context = {}
	context["tags"] = tags
	if tags:
		context["tags"] = tags+"/"
	tags = replace_none(transform_tags_single(tags))
	
	notes = Note.objects.filter(
		author=request.user.id,
		type="t",
		is_checked=True
	)
	filtered = []
	
	for note in notes:
		ntags = replace_none(transform_tags_single(note.tags))
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
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	paginator = Paginator(filtered, 10)
	filtered_page = replace_newlines(paginator.page(page_number))
	prange = page_range(page_number, paginator.num_pages)

	context["filtered"] = filtered_page
	context["current_page_number"] = page_number
	context["num_pages"] = paginator.num_pages
	context["page_range"] = prange
	context["urlprefix"] = "done"

	return render_to_response("filter.html", context)

def filter_undone(request, tags="", page_number=1):
	"""Filter unchecked todo notes"""

	if not request.user.is_authenticated():
		return redirect('/login?return={}'.format(request.path))

	context = {}
	context["tags"] = tags
	if tags:
		context["tags"] = tags+"/"
	tags = replace_none(transform_tags_single(tags))
	
	notes = Note.objects.filter(
		author=request.user.id,
		type="t",
		is_checked=False
	)
	filtered = []
	
	for note in notes:
		ntags = replace_none(transform_tags_single(note.tags))
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
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	paginator = Paginator(filtered, 10)
	filtered_page = replace_newlines(paginator.page(page_number))
	prange = page_range(page_number, paginator.num_pages)

	context["filtered"] = filtered_page
	context["current_page_number"] = page_number
	context["num_pages"] = paginator.num_pages
	context["page_range"] = prange
	context["urlprefix"] = "undone"

	return render_to_response("filter.html", context)

def filter_snippets(request, tags="", page_number=1):
	"""Filter snippets"""

	if not request.user.is_authenticated():
		return redirect('/login?return={}'.format(request.path))

	context = {}
	context["tags"] = tags
	if tags:
		context["tags"] = tags+"/"
	tags = replace_none(transform_tags_single(tags))
	
	notes = Note.objects.filter(author=request.user.id, type="s")
	filtered = []
	
	for note in notes:
		ntags = replace_none(transform_tags_single(note.tags))
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
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	paginator = Paginator(filtered, 10)
	filtered_page = replace_newlines(paginator.page(page_number))
	prange = page_range(page_number, paginator.num_pages)

	context["filtered"] = filtered_page
	context["current_page_number"] = page_number
	context["num_pages"] = paginator.num_pages
	context["page_range"] = prange
	context["urlprefix"] = "snippets"

	return render_to_response("filter.html", context)

def filter_warnings(request, tags="", page_number=1):
	"""Filter warnings"""

	if not request.user.is_authenticated():
		return redirect('/login?return={}'.format(request.path))

	context = {}
	context["tags"] = tags
	if tags:
		context["tags"] = tags+"/"
	tags = replace_none(transform_tags_single(tags))
	
	notes = Note.objects.filter(author=request.user.id, type="w")
	filtered = []
	
	for note in notes:
		ntags = replace_none(transform_tags_single(note.tags))
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
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	paginator = Paginator(filtered, 10)
	filtered_page = replace_newlines(paginator.page(page_number))
	prange = page_range(page_number, paginator.num_pages)

	context["filtered"] = filtered_page
	context["current_page_number"] = page_number
	context["num_pages"] = paginator.num_pages
	context["page_range"] = prange
	context["urlprefix"] = "warnings"

	return render_to_response("filter.html", context)

def filter_notes(request, tags="", page_number=1):
	"""Filter notes"""

	if not request.user.is_authenticated():
		return redirect('/login?return={}'.format(request.path))

	context = {}
	context["tags"] = tags
	if tags:
		context["tags"] = tags+"/"
	tags = replace_none(transform_tags_single(tags))
	
	notes = Note.objects.filter(author=request.user.id, type="n")
	filtered = []
	
	for note in notes:
		ntags = replace_none(transform_tags_single(note.tags))
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
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	paginator = Paginator(filtered, 10)
	filtered_page = replace_newlines(paginator.page(page_number))
	prange = page_range(page_number, paginator.num_pages)

	context["filtered"] = filtered_page
	context["current_page_number"] = page_number
	context["num_pages"] = paginator.num_pages
	context["page_range"] = prange
	context["urlprefix"] = "notes"

	return render_to_response("filter.html", context)


def login_view(request):
	"""Log in view"""
	
	if 'email' in request.POST and 'password' in request.POST:
		email = request.POST['email']
		password = request.POST['password']
		incorrect_username_or_password = "Incorrect username or password"
		too_long_username = "Too long username"
		empty_password = "Password cannot be empty"
		empty_username = "Username cannot be empty"
		errors = []
		if len(email) > 150:
			errors.append(too_long_username)
		
		elif not email:
			errors.append(empty_username)
		
		if not password:
			errors.append(empty_password)
		
		try:
			username = User.objects.get(
				Q(email=email) |
				Q(username=email)
			).username
		except ObjectDoesNotExist:
			errors.append(incorrect_username_or_password)
		
		if errors:
			return render_to_response(
				"login.html",
				{"errors": errors},
				context_instance=RequestContext(request)
			)
		
		user = authenticate(username=username, password=password)
		if user is None:
			errors.append(incorrect_username_or_password)
			return render_to_response(
				"login.html",
				{"errors": errors},
				context_instance=RequestContext(request)
			)
		
		if "return" in request.POST:
			return_page = request.POST["return"]
		else:
			return_page = "/"
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(return_page)
			else:
				return redirect("/login/?return=%s" %return_page)
		else:
			return redirect("/login/?return=%s" %return_page)
	if request.user.is_authenticated():
		return redirect("/")
	return render_to_response(
		"login.html",
		RequestContext(request, {}),
		context_instance=RequestContext(request)
	)

def logout_view(request):
	"""Log out view"""
	
	if request.user.is_authenticated():
		logout(request)
	return redirect("/")

def register(request):
	"""Registration page"""
	
	if request.user.is_authenticated():
		return redirect("/")
	
	assert 'username' in request.POST, "Username is missing"
	assert 'password' in request.POST, "Password is missing"
	assert 'confirm_password' in request.POST, "Password not confirmed"
	assert 'first_name' in request.POST, "First name is missing"
	assert 'last_name' in request.POST, "Last name is missing"
	assert 'email' in request.POST, "Email is missing"
	username = request.POST["username"]
	password = request.POST["password"]
	confirm_password = request.POST["confirm_password"]
	first_name = request.POST["first_name"]
	last_name = request.POST["last_name"]
	email = request.POST["email"]
	invalid_email = "Invalid email"
	too_long_email = "Too long email"
	too_long_username = "Too long username"
	too_long_firstname = "Too long first name"
	too_long_lastname = "Too long last name"
	passwords_are_different = "You entered 2 different passwords"
	first_name_is_empty = "First name cannot be empty"
	last_name_is_empty = "Last name cannot be empty"
	username_is_empty = "Username cannot be empty"
	password_is_empty = "Password cannot be empty"
	email_is_empty = "Email cannot be empty"
	errors = []
	
	if "@" not in email:
		errors.append(invalid_email)
	
	if len(email) > 150:
		errors.append(too_long_email)
	elif not email:
		errors.append(email_is_empty)
	
	if len(first_name) > 150:
		errors.append(too_long_firstname)
	elif not first_name:
		errors.append(first_name_is_empty)
	
	if len(last_name) > 150:
		errors.append(too_long_lastname)
	elif not last_name:
		errors.append(last_name_is_empty)
	
	if len(username) > 150:
		errors.append(too_long_username)
	elif not username:
		errors.append(username_is_empty)
	
	if not password:
		errors.append(password_is_empty)
	elif password != confirm_password:
		errors.append(passwords_are_different)
	
	if errors:
		return render_to_response("register.html", {
			"errors": errors,
			"first_name": first_name,
			"last_name": last_name,
			"email": email,
			"username": username
		})
		
	if "return" in request.POST:
		return_page = request.POST["return"]
	else:
		return_page = "/"
	try:
		User.objects.get(username=username, email=email)
	except ObjectDoesNotExist:
		user = User.objects.create(
			username=username,
			first_name=first_name,
			last_name=last_name,
			email=email
		)
		user.set_password(password)
		user.save()
		
		return redirect(return_page)
	else:
		return redirect("/")
	return render_to_response(
		"register.html",
		RequestContext(request, {}),
		context_instance=RequestContext(request)
	   )

def contact(request):
	"""Contact form"""

	if not request.user.is_authenticated():
		return redirect('/login?return={}'.format(request.path))
	
	if "text" in request.POST and "subject" in request.POST:
		send_mail(
			request.POST['subject'],
			"{text}\n	{user_email}".format(
				text=request.POST['text'],
				user_email=request.user.email
			),
			request.user.email,
			[su.email for su in User.objects.filter(is_superuser=True)],
			fail_silently=False
			)
		return HttpResponse(
			htmlbody("""\
Thanks for feedback. <a href='/contact/'>Back</a>""",
            "Thanks for feedback!"
            )
		)
	
	return render_to_response("contact.html", RequestContext(request))

def profile(request):
	"""Profile page"""
	
	if not request.user.is_authenticated():
		return redirect('/login?return={}'.format(request.path))
	
	user = request.user
	username = user.username
	first_name = user.first_name
	last_name = user.last_name
	
	context = {
		"user": user,
		"username": username,
		"first_name": first_name,
		"last_name": last_name,
		"id": user.id
	}
	
	return render_to_response(
		'profile.html',
		context,
		context_instance=RequestContext(request, context))

def delete_account(request):
	"""Delete user account"""
	
	if not request.user.is_authenticated():
		raise Http404
	
	if "confirm" in request.POST:
		confirm = request.POST["confirm"]
		user = request.user
		
		user_notes = Note.objects.filter(author=user)
		user_notes.delete()
		
		if user.check_password(confirm):
			user.delete()
		else:
			return redirect(request.path)
		return redirect("/")
	
	return render_to_response(
		"delete_account.html",
		context_instance=RequestContext(request)
	)

def reset_password_confirm(request, uidb64=None, token=None):
	"""Password reset confirmation"""
	return password_reset_confirm(
		request, template_name='registration/password_reset_confirm.html',
		uidb64=uidb64, token=token, post_reset_redirect='/reset/complete'
	)

def reset_password(request):
	"""Reset password"""
	
	return password_reset(
		request,
		template_name='registration/password_reset_form.html',
		subject_template_name='registration/password_reset_subject.txt',
		post_reset_redirect="/reset/sent"
	)

def find_similiar_notes(request, note_id, page_number=1):
	"""Find notes, similiar to some note
	
	@param note_id: ID of the note
	"""
	
	if not request.user.is_authenticated():
		return redirect('/login?return=%s' %request.path)
	
	try:
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	try:
		note = Note.objects.get(id=note_id)
	except ObjectDoesNotExist:
		raise Http404
	
	notes = Note.objects.filter(author=request.user.id)
	
	sorted_notes = check_similarity(note, notes)
	paginator = Paginator(sorted_notes, 10)
	try:
		current_page = replace_newlines_sim(paginator.page(page_number))
	except EmptyPage:
		raise Http404
	
	print(current_page.object_list)
	
	prange = page_range(page_number, paginator.num_pages)
	
	context = {
		"note_": note,
		"notes": current_page,
		"current_page_number": page_number,
		"page_range": prange,
		"current_url": "/similiar/%s/" %note_id
	}
	
	return render_to_response(
		"similiar.html",
		context,
		context_instance=RequestContext(request)
	)
