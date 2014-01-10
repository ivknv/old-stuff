#!python
# -*- coding: utf-8 -*-
import os

def pyinit(d):
	if not (os.path.exists(d+"/__init__.py") and os.path.exists(d+"/__init__.pyc")):
		f1=open(d+"/__init__.py", "w")
		f1.close()
	for i in os.listdir(d):
		if os.path.isdir(i):
			if not (os.path.exists(d+"/__init__.py") and os.path.exists(d+"/__init__.pyc")):
				f1=open(d+"/"+i+"/__init__.py", "w")
				f1.close()
