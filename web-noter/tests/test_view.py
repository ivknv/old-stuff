#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase, Client
from note.models import Note
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import json

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

class View(TestCase):
	"""Simple view test"""
	
	def setUp(self):
		self.client = Client()
		guest = User.objects.create(username="guest")
		guest.set_password("guest")
		guest.save()
		
		self.test_note = Note.objects.create(
			title="test",
			text="Test note",
			tags="test",
			author=guest)
	
	def test_if_authentication_works(self):
		response = self.client.get("/", follow=True)
		
		self.assertEqual(len(response.redirect_chain), 2)
		
		self.assertEqual(
			response.redirect_chain[1][0],
			"http://testserver/login/?return=%2F")
		
		self.assertTrue(response.status_code in [200, 304])
		
		response = self.client.post(
			"/login/",
			{
				"user": "guest",
				"password": "guest"
			},
			follow=True)
		
		self.assertEqual(len(response.redirect_chain), 0)
		
		self.assertTrue(response.status_code in [200, 304])
	
	def getNotesTest(self):
		response = self.client.post(reverse("API:getNotes"),
			{
				"username": "guest",
				"password": "guest"
			})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, list))
	
	def getNoteTest(self):
		response = self.client.post(reverse("API:getNote"),
			{
				"username": "guest",
				"password": "guest",
				"id": self.test_note.id
			})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, list))
		
		self.assertEqual(len(data), 1)
		
		self.assertTrue("pk" in data[0])
		
		self.assertTrue("fields" in data[0])
		
	def addNoteTest(self):
		response = self.client.post(reverse("API:addNote"),
			{
				"username": "guest",
				"password": "guest",
				"title": "Test",
				"text": "Test note",
				"tags": "test, note",
				"type": "n"
			})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)		
		
		self.assertTrue(isinstance(data, dict))
		
		self.assertTrue("id" in data)
		
		self.assertTrue(isinstance(data["id"], int))
		
		self.test_note1 = Note.objects.get(id=data["id"])
		
		self.assertTrue("success" in data)
		
		self.assertTrue(data["success"])
	
	def rmNoteTest(self):
		response = self.client.post(reverse("API:rmNote"),
			{
				"username": "guest",
				"password": "guest",
				"id": self.test_note.id
			})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		
		self.assertTrue("id" in data)
		
		self.assertTrue(isinstance(data["id"], int))
		
		self.assertTrue("success" in data)
		
		self.assertTrue(data["success"])
	
	def addNotesTest(self):
		response = self.client.post(reverse("API:addNotes"),
			{
				"username": "guest",
				"password": "guest",
				"list": json.dumps([{"title": "Test note #1",
				"text": "Nothing special, just a test.",
				"tags": "test, nothing special",
				"type": "n"},
				{"title": "Test note #2",
				"text": "Nothing special, just a test.",
				"tags": "test, nothing special",
				"type": "n"}])})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		
		self.assertTrue("saved" in data)
		
		self.assertTrue(isinstance(data["saved"], list))
		
		self.saved = data["saved"]
		
		self.assertTrue("success" in data)
		
		self.assertTrue(data["success"])
	
	def rmNotesTest(self):
		response = self.client.post(reverse("API:rmNotes"),
			{
				"username": "guest",
				"password": "guest",
				"list": "%i, %i" %(self.saved[0], self.saved[1])})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		
		self.assertTrue(
			str(self.saved[0]) in data and str(self.saved[1]) in data)
		
		self.assertTrue(
			data[str(self.saved[0])] and data[str(self.saved[1])])

	def editNoteTest(self):
		response = self.client.post(reverse("API:editNote"),
			{
				"username": "guest",
				"password": "guest",
				"id": self.test_note1.id,
				"title": "Edited note"})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		
		self.assertTrue("title" in data)
		self.assertTrue("text" in data)
		self.assertTrue("tags" in data)
		self.assertTrue("type" in data)
		self.assertTrue("id" in data)
		
		self.assertNotEqual(self.test_note1.title, data["title"])
	
	def getUserInfoTest(self):
		response = self.client.post(reverse("API:getUserInfo"),
			{
				"username": "guest",
				"password": "guest"})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		
		self.assertTrue("username" in data)
		self.assertTrue("first_name" in data)
		self.assertTrue("last_name" in data)
		self.assertTrue("email" in data)
		self.assertTrue("id" in data)
		
		self.assertTrue(isinstance(data["username"], unicode_))
		self.assertTrue(isinstance(data["first_name"], unicode_))
		self.assertTrue(isinstance(data["last_name"], unicode_))
		self.assertTrue(isinstance(data["email"], unicode_))
		self.assertTrue(isinstance(data["id"], int))
	
	def updateUsernameTest(self):
		response = self.client.post(reverse("API:updateUsername"),
			{
				"username": "guest",
				"password": "guest",
				"new_username": "guest123"})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		
		self.assertTrue("old_username" in data)
		self.assertTrue("new_username" in data)
		
		self.assertTrue(isinstance(data["old_username"], unicode_))
		self.assertTrue(isinstance(data["new_username"], unicode_))
		self.assertNotEqual(data["old_username"], data["new_username"])

	def updateFirstNameTest(self):
		response = self.client.post(reverse("API:updateFirstName"),
			{
				"username": "guest123",
				"password": "guest",
				"new_first_name": "someone"})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		
		self.assertTrue("old_first_name" in data)
		self.assertTrue("new_first_name" in data)
		
		self.assertTrue(isinstance(data["old_first_name"], unicode_))
		self.assertTrue(isinstance(data["new_first_name"], unicode_))
		self.assertNotEqual(data["old_first_name"], data["new_first_name"])
	
	def updateLastNameTest(self):
		response = self.client.post(reverse("API:updateLastName"),
			{
				"username": "guest123",
				"password": "guest",
				"new_last_name": "someone"})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		
		self.assertTrue("old_last_name" in data)
		self.assertTrue("new_last_name" in data)
		
		self.assertTrue(isinstance(data["old_last_name"], unicode_))
		self.assertTrue(isinstance(data["new_last_name"], unicode_))
		self.assertNotEqual(data["old_last_name"], data["new_last_name"])
	
	def updateEmailTest(self):
		response = self.client.post(reverse("API:updateEmail"),
			{
				"username": "guest123",
				"password": "guest",
				"new_email": "someone@gmail.com"})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		
		self.assertTrue("old_email" in data)
		self.assertTrue("new_email" in data)
		
		self.assertTrue(isinstance(data["old_email"], unicode_))
		self.assertTrue(isinstance(data["new_email"], unicode_))
		self.assertNotEqual(data["old_email"], data["new_email"])
	
	def updatePasswordTest(self):
		response = self.client.post(reverse("API:updatePassword"),
			{
				"username": "guest123",
				"password": "guest",
				"new_password": "guest123",
				"confirm_password": "guest123"})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		self.assertTrue("success" in data)
		self.assertTrue(data["success"])
	
	def deleteAccountTest(self):
		response = self.client.post(reverse("API:deleteAccount"),
			{
				"username": "guest123",
				"password": "guest123"})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		self.assertTrue("success" in data)
		self.assertTrue(data["success"])
	
	def registerTest(self):
		response = self.client.post(reverse("API:register"),
			{
				"username": "guest123",
				"first_name": "guest",
				"last_name": "guest",
				"email": "guest@gmail.com",
				"password": "guest123",
				"confirm_password": "guest123"})
		
		self.assertTrue(response.status_code in [200, 304])
		
		data = json.loads(response.content)
		
		self.assertTrue(isinstance(data, dict))
		self.assertTrue("success" in data)
		self.assertTrue(data["success"])
	
	def test_if_API_works(self):
		self.getNotesTest()
		self.getNoteTest()
		self.addNoteTest()
		self.rmNoteTest()
		self.addNotesTest()
		self.rmNotesTest()
		self.editNoteTest()
		self.getUserInfoTest()
		self.updateUsernameTest()
		self.updateFirstNameTest()
		self.updateLastNameTest()
		self.updateEmailTest()
		self.updatePasswordTest()
		self.deleteAccountTest()
		self.registerTest()
