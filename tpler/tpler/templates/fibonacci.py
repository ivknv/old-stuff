#!/usr/bin/python
# -*- coding: utf-8 -*-

def fibonacci(n):
	return fibonacci(n-2)+fibonacci(n-1) if n>2 else n