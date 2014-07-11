from django.contrib import admin

from note.models import Note

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "type", "date")

admin.site.register(Note, NoteAdmin)
