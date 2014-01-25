#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def writeTemplate(filename, arg2="", arg3="1.2.8"):
	ex=filename[filename.rindex(".")::].lower()
	arg2=arg2.lower()
	template_dir=os.path.realpath(__file__)
	template_dir=template_dir[0:template_dir.rindex(os.path.sep)]+os.path.sep+"templates"
	if ex in [".py"]:
		f1=open(filename, "w+")
		if arg2 in ["main"]:
			t=template_dir+os.path.sep+"python_main.py"
		elif arg2 in ["pyside"]:
			t=template_dir+os.path.sep+"python_pyside.py"
		elif arg2 in ["factorial", "fac"]:
			t=template_dir+os.path.sep+"factorial.py"
		elif arg2 in ["fibonacci", "fib"]:
			t=template_dir+os.path.sep+"fibonacci.py"
		elif arg2 in ["random", "rand"]:
			import random
			t=template_dir+os.path.sep+random.choice(["python_pyside.py", "python_main.py", "python.py", "factorial.py", "fibonacci.py"])
		else:
			t=template_dir+os.path.sep+"python.py"
		t=open(t, "r")
		tr=t.read()
		t.close()
		f1.write(tr)
		f1.close()
	elif ex in [".html", ".htm"]:
		f1=open(filename, "w+")
		if arg2 in ["jquery"]:
			t=template_dir+os.path.sep+"html_jquery.html"
		elif arg2 in ["jqueryui"]:
			t=template_dir+os.path.sep+"html_jqueryui.html"
		elif arg2 in ["angular", "angularjs", "angular.js"]:
			t=template_dir+os.path.sep+"html_angular.html"
		elif arg2 in ['base', 'dajngo_base', 'django base', 'django-base']:
			t=template_dir+os.path.sep+"base.html"
		elif arg2 in ["random", "rand"]:
			import random
			t=template_dir+os.path.sep+random.choice(["html.html", "html_jquery.html", "html_jqueryui.html", "html_angular.html", "base.html"])
		else:
			t=template_dir+os.path.sep+"html.html"
		t=open(t, "r")
		tr=t.read().replace("%version%", arg3)
		t.close()
		f1.write(tr)
		f1.close()
	elif ex in [".c"]:
		f1=open(filename, "w+")
		if arg2 in ["empty"]:
			t=template_dir+os.path.sep+"c_empty.c"
		elif arg2 in ["ncurses"]:
			t=template_dir+os.path.sep+"c_ncurses.c"
		elif arg2 in ["factorial", "fac"]:
			t=template_dir+os.path.sep+"factorial.c"
		elif arg2 in ["fibonacci", "fib"]:
			t=template_dir+os.path.sep+"fibonacci.c"
		else:
			t=template_dir+os.path.sep+"c.c"
		t=open(t, "r")
		tr=t.read()
		t.close()
		f1.write(tr)
		f1.close()
	elif ex in [".cpp"]:
		f1=open(filename, "w+")
		if arg2 in ["factorial", "fac"]:
			t=template_dir+os.path.sep+"factorial.c"
		elif arg2 in ["fibonacci", "fib"]:
			t=template_dir+os.path.sep+"fibonacci.c"
		else:
			t=template_dir+os.path.sep+"cpp.cpp"
		t=open(t, "r")
		tr=t.read()
		t.close()
		f1.write(tr)
		f1.close()
	elif ex in [".xml"]:
		f1=open(filename, "w+")
		if arg2 in ["project", "pro"]:
			t=template_dir+os.path.sep+"xml.xml"
		else:
			t=template_dir+os.path.sep+"xml.xml"
		t=open(t, "r")
		tr=t.read()
		t.close()
		f1.write(tr)
		f1.close()
	elif ex in [".css"]:
		if arg2 in ["button"]:
			f1=open(filename, "w+")
			t=template_dir+os.path.sep+"css_button.css"
			t=open(t, "r")
			tr=t.read()
			t.close()
			f1.write(tr)
			f1.close()
	elif ex in [".java"]:
		f1=open(filename, "w+")
		t=template_dir+os.path.sep+"java.java"
		t=open(t, "r")
		tr=t.read().replace("%name%", filename[0:filename.index(".")])
		t.close()
		f1.write(tr)
		f1.close()
	elif ex in [".xsl"]:
		f1=open(filename, "w+")
		t=template_dir+os.path.sep+"xsl.xsl"
		t=open(t, "r")
		tr=t.read()
		t.close()
		f1.write(tr)
		f1.close()
	elif ex in [".xsd"]:
		f1=open(filename, "w+")
		t=template_dir+os.path.sep+"xsd.xsd"
		t=open(t, "r")
		tr=t.read()
		t.close()
		f1.write(tr)
		f1.close()
	elif ex in [".svg"]:
		f1=open(filename, "w+")
		t=template_dir+os.path.sep+"svg.svg"
		t=open(t, "r")
		tr=t.read()
		t.close()
		f1.write(tr)
		f1.close()
	elif ex in [".php"]:
		f1=open(filename, "w+")
		t=template_dir+os.path.sep+"php.php"
		t=open(t, "r")
		tr=t.read()
		t.close()
		f1.write(tr)
		t.close()
	elif ex in [".xhtml"]:
		f1=open(filename, "w+")
		t=template_dir+os.path.sep+"xhtml.xhtml"
		t=open(t, "r")
		tr=t.read()
		t.close()
		f1.write(tr)
		f1.close()
if __name__ == "__main__":
	import sys
	if len(sys.argv)==2:
		writeTemplate(sys.argv[1])
	elif len(sys.argv)==3:
		writeTemplate(sys.argv[1], sys.argv[2])
	elif len(sys.argv)>3:
		writeTemplate(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print("Usage: tpler [filename] [type] [type2]\ntype2 can be used only with html and with type==angularjs")
