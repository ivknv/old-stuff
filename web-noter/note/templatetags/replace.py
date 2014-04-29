#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter(name="replace")
def replace(value, arg):
	args=arg.split(".;.")
	return value.replace(args[0], args[1])
