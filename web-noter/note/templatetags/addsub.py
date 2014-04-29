#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter(name="sub")
def sub(value, arg):
	return eval(str(value))-eval(arg)

@register.filter(name="addd")
def addd(value, arg):
	return eval(str(value))+eval(arg)
