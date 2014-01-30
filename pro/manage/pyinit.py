#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def pyinit(d):
	if not (os.path.exists(d+os.path.sep+"__init__.py") and os.path.exists(d+os.path.sep+"__init__.pyc")):
		f1=open(d+os.path.sep+"__init__.py", "w")
		f1.close()
	for i in os.listdir(d):
		if os.path.isdir(i):
			if not (os.path.exists(d+os.path.sep+"__init__.py") and os.path.exists(d+os.path.sep+"__init__.pyc")):
				f1=open(d+os.path.sep+i+os.path.sep+"__init__.py", "w")
				f1.close()
