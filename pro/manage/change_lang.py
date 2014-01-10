# -*- coding: utf-8 -*-

from xml.dom import minidom
import os

def change_lang(project, new_lang):
	project_realpath=os.path.realpath(project)
	dom=minidom.parse(project_realpath+"\\project.xml")
	current_lang=dom.getElementsByTagName("language")[0]
	current_lang_value=current_lang.childNodes[0].nodeValue
	new_lang_value=current_lang.toxml().replace(current_lang_value, "\n"+new_lang+"\n")
	f1=open(project_realpath+"\\project.xml", "r+")
	f1_content=f1.read()
	f1.close()
	f1=open(project_realpath+"\\project.xml", "w+")
	f1.write(f1_content.replace(current_lang.toxml(), new_lang_value))
