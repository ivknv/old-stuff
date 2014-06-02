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
		if self.type != "s":
			return re.sub("<.*?>", "", self.text)
		else:
			return self.text
	
	def getTags(self):
		tags = self.tags.split(",")
		for i in range(len(tags)):
			if tags[i].startswith(" "):
				tags[i] = tags[i][1:]
		return tags
	
	def replaceNewLines(self):
		if self.type != "s":
			return self.text.replace("\n\r", "<br/>").replace("\n", "<br/>").replace("\t", "&nbsp;&nbsp;&nbps;&nbsp;")
		else:
			return self.text
	
	class Meta:
		ordering = ["-date"]
	if sys.version_info.major > 2:
		def __str__(self):
			return self.title
	else:
		def __unicode__(self):
			return self.title
	
	def save(self, *args, **kwargs):
		self.text = re.sub("<[ \t]*script[ \t]*.*?[ \t]*>.*<[ \t]*/[ \t]*script[ \t]*>", "", self.text)
		self.text = re.sub("<[ \t]*script[ \t]*.*?[ \t]*>.*", "", self.text)
		super(Note, self).save(*args, **kwargs)

class NoteAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "type", "date")

admin.site.register(Note, NoteAdmin)
