# -*- coding: cp1251 -*-
from xml.dom import minidom
import os

def change_author(project, new_author):
	project_realpath=os.path.realpath(project)
	dom=minidom.parse(project_realpath+"\\project.xml")
	current_author=dom.getElementsByTagName("authors")[0]
	current_author_value=current_author.childNodes[0].nodeValue
	new_author_value=current_author.toxml().replace(current_author_value, "\n"+new_author+"\n")
	f1=open(project_realpath+"\\project.xml", "r")
	f1_content=f1.read()
	f1.close()
	f1=open(project_realpath+"\\project.xml", "w+")
	f1.write(f1_content.replace(current_author.toxml(), new_author_value))
	f1.close()
