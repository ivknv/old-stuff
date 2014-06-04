"""
@author: Ivan Konovalov

Noter API functions
"""

from django.contrib.auth import authenticate

from django.core import serializers

from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User

from note.models import Note

from django.core.exceptions import ObjectDoesNotExist

from django.db import OperationalError, IntegrityError

import re, json

def to_json(success="true", **kwargs):
	"""Returns JSON string
	
	@param success: True or False
	
	@rtype: str
	"""
	
	response = '{"success": %s' %success
	for arg in kwargs:
		response += ', "{arg}": {value}'.format(arg=arg, value=kwargs[arg])
	response += "}"
	
	return response

def JsonResponse(success="true", **kwargs):
	"""Returns HttpResponse with json string as a parameter"""
	
	return HttpResponse(to_json(success, **kwargs))

def API_authenticate(request):
	"""Check username/email and password"""
	
	assert "username" in request.POST or "email" in request.POST, \
	"Authentication Failed: username or/and email are missing"
	assert "password" in request.POST, \
	"Authentication failed: paassword is missing"
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
	assert user is not None, \
	"Authentication failed: incorrect username/email or password"
	return user

@csrf_exempt
def API_getUserInfo(request):
	"""Get user info"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	return JsonResponse(
		"true",
		username='"'+user.username+'"',
		first_name='"'+user.first_name+'"',
		last_name='"'+user.last_name+'"',
		email='"'+user.email+'"',
		id=user.id
	)



@csrf_exempt
def API_getNotes(request):
	"""Get all the notes"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	notes = Note.objects.filter(author=user)
	
	notes_json = serializers.serialize("json", notes)
	
	return HttpResponse(notes_json)

@csrf_exempt
def API_getNote(request):
	"""Get note"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	assert "id" in request.POST, "ID is missing"
	id_ = id_of_note(request)
	
	try:
		note = Note.objects.get(id=id_)
	except ObjectDoesNotExist:
		return JsonResponse("false", message='"Note with ID==%s doesn\'t exist"')
	
	note_json = serializers.serialize("json", [note])
	
	return HttpResponse(note_json)

def id_of_note(request):
	"""Get note ID from request"""
	
	return request.POST["id"]

def type_of_note(request):
	"""Get note type from request"""
	
	return request.POST["type"]

def title_of_note(request):
	"""Get note title from request"""
	
	return request.POST["title"]

def text_of_note(request):
	"""Get note text from request"""
	
	return request.POST["text"]

def tags_of_note(request):
	"""Get note tags from request"""
	
	return request.POST["tags"]

def registration_data(request):
	"""Validate registration data and pack it into dictionary"""
	
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
	
	email_validator = re.compile(r"[a-zA-Z\.]+@[a-zA-Z\.]+")
	
	assert len(first_name) < 150, "First name cannot be longer than 150 symbols"
	assert first_name, "First name cannot be empty"
	assert len(last_name) < 150, "Last name cannot be longer than 150 symbols"
	assert last_name, "Last name cannot be empty"
	assert len(username) < 150, "Username cannot be longer than 150 symbols"
	assert username, "Username cannot be empty"
	assert re.match(email_validator, email) is not None, "Invalid email"
	assert password, "Password cannot be empty"
	assert confirm_password == password or confirm_password, \
	"Password isn't confirmed"
	
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
	"""Add single note"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	try:
		assert "type" in request.POST, "Type is missing"
		assert request.POST["type"] in ["n", "t", "s", "w"], \
		"Type should be n(ote), t(odo), s(nippet) or w(arning)"
		assert "text" in request.POST, "Text is missing"
		assert "title" in request.POST, "Title is missing"
		assert "tags" in request.POST, "Tags are missing"
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	type_ = type_of_note(request)
	title = title_of_note(request)
	text = text_of_note(request)
	tags = tags_of_note(request)
	
	new_note = Note.objects.create(
		title=title,
		text=text,
		tags=tags,
		type=type_,
		author=user
	)
	try:
		new_note.save()
	except OperationalError as error:
		return JsonResponse(
			"false",
			message='"Failed to save note: %s"' %error.message
		)
	
	return JsonResponse("true", id=new_note.id)

@csrf_exempt
def API_addNotes(request):
	"""Add multiple notes"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	try:
		assert "list" in request.POST, "List of notes is missing"
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	json_list = json.loads(request.POST["list"])
	added = []
	
	for note in json_list:
		assert "title" in note, "Title is missing"
		assert "text" in note, "Text is missing"
		assert "tags" in note, "Tags are missing"
		assert "type" in note, "Type is missing"
		
		title = note["title"]
		text = note["text"]
		tags = note["tags"]
		type_ = note["type"]
		new_note = Note.objects.create(
			title=title,
			text=text,
			tags=tags,
			type=type_,
			author=user
		)
		
		try:
			new_note.save()
			added.append(new_note.id)
		except OperationalError as error:
			return JsonResponse("false", message='"Failed to add note: %s"' %new_note.id)
		
		j = "[%s" %added[0]
		for i in added[1:]:
			j += ", %s" %i
		j += "]"
	
	return JsonResponse("true", saved=j)

@csrf_exempt
def API_rmNote(request):
	"""Delete single note"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	try:
		assert "id" in request.POST, "ID is missing"
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	id_ = id_of_note(request)
	try:
		note = Note.objects.get(id=id_, author=user)
		note.delete()
	except ObjectDoesNotExist:
		return JsonResponse("false", message='"Object does not exist"', id=id_)
	
	return JsonResponse("true", id=id_)

@csrf_exempt
def API_rmNotes(request):
	"""Delete multiple notes"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	try:
		assert "list" in request.POST, "List of IDs is missing"
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	list_ = request.POST["list"].split(", ")
	deleted = {}
	
	for note_id in list_:
		try:
			note = Note.objects.get(id=note_id, author=user)
			note.delete()
			deleted[int(note_id)] = True
		except ObjectDoesNotExist:
			deleted[int(note_id)] = False
	
	deleted_json = json.dumps(deleted)
	
	return HttpResponse(deleted_json)

@csrf_exempt
def API_register(request):
	"""Register"""
	
	try:
		data = registration_data(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
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
	"""Delete user's account"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user_id = user.id
	
	user_notes = Note.objects.filter(author=user)
	
	user_notes.delete()
	user.delete()
	
	return JsonResponse("true", id=user_id)

@csrf_exempt
def API_update_username(request):
	"""Update username"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user_id = user.id
	old_username = user.username
	
	try:
		assert "new_username" in request.POST, "New username is missing"
		new_username = request.POST["new_username"]
		assert new_username, "New username cannot be empty"
		assert len(new_username) < 150, "New username is too long"
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user.username = new_username
	try:
		user.save()
	except IntegrityError:
		return JsonResponse("false",
			message='"User with this username already exists"')
	
	return JsonResponse("true",
		id=user_id,
		old_username='"'+old_username+'"',
		new_username='"'+new_username+'"'
	)

@csrf_exempt
def API_update_first_name(request):
	"""Update first name"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user_id = user.id
	old_first_name = user.first_name
	
	try:
		assert "new_first_name" in request.POST, "New first name is missing"
		new_first_name = request.POST["new_first_name"]
		assert new_first_name, "New first name cannot be empty"
		assert len(new_first_name) < 150, "New first name is too long"
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user.first_name = new_first_name
	try:
		user.save()
	except OperationalError as error:
		print(error.message)
		return JsonResponse("false",
			message='"Failed to save"')
	
	return JsonResponse("true",
		id=user_id,
		old_first_name='"'+old_first_name+'"',
		new_first_name='"'+new_first_name+'"'
	)

@csrf_exempt
def API_update_last_name(request):
	"""Update last name"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user_id = user.id
	old_last_name = user.last_name
	
	try:
		assert "new_last_name" in request.POST, "New last name is missing"
		new_last_name = request.POST["new_last_name"]
		assert new_last_name, "New last name cannot be empty"
		assert len(new_last_name) < 150, "New last name is too long"
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user.last_name = new_last_name
	try:
		user.save()
	except OperationalError as error:
		print(error.message)
		return JsonResponse("false",
			message='"Failed to save"')
	
	return JsonResponse("true",
		id=user_id,
		old_last_name='"'+old_last_name+'"',
		new_last_name='"'+new_last_name+'"'
	)

@csrf_exempt
def API_update_email(request):
	"""Update email"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user_id = user.id
	old_email = user.email
	
	try:
		assert "new_email" in request.POST, "New email is missing"
		new_email = request.POST["new_email"]
		assert new_email, "New email cannot be empty"
		assert len(new_email) < 150, "New email is too long"
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user.email = new_email
	try:
		user.save()
	except OperationalError as error:
		print(error.message)
		return JsonResponse("false",
			message='"Failed to save"')
	
	return JsonResponse("true",
		id=user_id,
		old_email='"'+old_email+'"',
		new_email='"'+new_email+'"'
	)

@csrf_exempt
def API_update_password(request):
	"""Update password"""
	
	try:
		user = API_authenticate(request)
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user_id = user.id
	
	try:
		assert "new_password" in request.POST, "New password is missing"
		new_password = request.POST["new_password"]
		assert new_password, "New password cannot be empty"
		assert len(new_password) < 150, "New password is too long"
		assert "confirm_password" in request.POST, "Password isn't confirmed"
		confirm_password = request.POST["confirm_password"]
		assert new_password == confirm_password, "You entered two different passwords"
	except AssertionError as error:
		return JsonResponse("false", message='"'+error.message+'"')
	
	user.set_password(new_password)
	try:
		user.save()
	except OperationalError as error:
		print(error.message)
		return JsonResponse("false",
			message='"Failed to save"')
	
	return JsonResponse("true",
		id=user_id
	)
