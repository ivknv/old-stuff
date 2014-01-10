# -*- coding: utf-8 -*-
from xml.dom import minidom
import os

def change_description(project, new_description):
	project_realpath=os.path.realpath(project)
	dom=minidom.parse(project_realpath+"\\project.xml")
	current_description=dom.getElementsByTagName("description")[0]
	current_description_value=current_description.childNodes[0].nodeValue
	new_description_value=current_description.toxml().replace(current_description_value, "\n"+new_description+"\n")
	f1=open(project_realpath+"\\project.xml", "r")
	f1_content=f1.read()
	f1.close()
	f1=open(project_realpath+"\\project.xml", "w+")
	f1.write(f1_content.replace(current_description.toxml(), new_description_value))
	f1.close()
