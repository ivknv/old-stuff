from django.db import models

from django.contrib import admin

from django.conf import settings

import sys, re

class Note(models.Model):
	title = models.CharField(max_length=100)
	text = models.TextField()
	tags = models.TextField()
	type = models.CharField(max_length=50, choices=(
		("n", "Note"),
		("s", "Snippet"),
		("t", "Todo"),
		("w", "Warning")
	), default="n")
	is_checked = models.BooleanField(default=False)
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	date = models.DateTimeField(auto_now_add=True)
	
	def no_html(self):
		return re.sub("<.*?>", "", self.text)
	
	class Meta:
		ordering = ["-date"]
	if sys.version_info.major > 2:
		def __str__(self):
			return self.title
	else:
		def __unicode__(self):
			return self.title

class NoteAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "type", "date")

admin.site.register(Note, NoteAdmin)
