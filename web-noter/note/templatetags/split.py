from django import template

register = template.Library()

@register.filter(name='splitags')
def split_tags(value):
	tags = value.tags.split(",")
	for i in range(len(tags)):
		tag = tags[i]
		if tag.startswith(" "):
			tag = tag[1:]
		tags[i] = tag
	
	return tags
