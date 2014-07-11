from django.db import models

from django.conf import settings

import sys, re

def replace_newlines_string(string):
	"""Replace all the newlines (\n) by <br/> in a string"""
	
	text = ""
	text_splitted = string.split("\n")
	length = len(text_splitted)
	i = 0
	
	for line in text_splitted:
		i += 1
		line = line.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
		text += line
		
		if i < length: # Check if it's last line:
			if not re.search("<.*?>$", line):
				text += "<br/>"
			text += "\n"
		
	return text

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
			return replace_newlines_string(self.text)
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
		r1 = re.compile("<[ \t]*script[ \t]*.*?>.*<[ \t]*/[ \t]*script[ \t]*>", re.I)
		r2 = re.compile("<[ \t]*script[ \t]*.*?>.*", re.I)
		self.text = re.sub(r1, "", self.text)
		self.text = re.sub(r2, "", self.text)
		super(Note, self).save(*args, **kwargs)
