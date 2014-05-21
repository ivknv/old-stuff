from django.contrib.auth import authenticate

from django.core import serializers

from django.http import HttpResponse, Http404

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User

import re, json

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
def API_getUserInfo(request):
	try:
		user = API_authenticate(request)
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	
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
	try:
		user = API_authenticate(request)
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	
	notes = Note.objects.filter(author=user)
	
	notes_json = serializers.serialize("json", notes)
	
	return HttpResponse(notes_json)

@csrf_exempt
def API_getNote(request):
	try:
		user = API_authenticate(request)
	except AssertionError as e:
		return JsonResponse("false", message='"'+e.message+'"')
	
	assert "id" in request.POST, "ID is missing"
	id_ = id_of_note(request)
	
	try:
		note = Note.objects.get(id=id_)
	except ObjectDoesNotExist:
		return JsonResponse("false", message='"Note with ID==%s doesn\'t exist"')
	
	note_json = serializers.serialize("json", [note])
	
	return HttpResponse(note_json)

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
		assert "title" in n, "Title is missing"
		assert "text" in n, "Text is missing"
		assert "tags" in n, "Tags are missing"
		assert "type" in n, "Type is missing"
		
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
		
		j = "[%s" %added[0]
		for i in added[1:]:
			j += ", %s" %i
		j += "]"
	
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
