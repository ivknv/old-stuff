#!/usr/bin/python
# -*- coding: utf-8 -*-

def factorial(n):
	return n*factorial(n-1) if n>2 else n