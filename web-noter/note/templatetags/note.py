from django import template

register = template.Library()

@register.filter(name='br')
def replaceNewLines(value):
	return value.replaceNewLines()
