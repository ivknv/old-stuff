from django.db import models
from django.contrib import admin
import sys

class Note(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100)
	text = models.TextField()
	tags = models.TextField()
	is_todo = models.BooleanField(default=False)
	is_checked = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ["-date"]
	if sys.version_info.major > 2:
		def __str__(self):
			return self.title
	else:
		def __unicode__(self):
			return self.title

class NoteAdmin(admin.ModelAdmin):
	list_display = ("title", "date")

admin.site.register(Note, NoteAdmin)
