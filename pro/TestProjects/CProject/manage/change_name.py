# -*- coding: cp1251 -*-
from xml.dom import minidom
import os

def rename(project, new_name):
	project_realpath=os.path.realpath(project)
	dom=minidom.parse(project_realpath+"\\project.xml")
	current_name=dom.getElementsByTagName("name")[0]
	current_name_value=current_name.childNodes[0].nodeValue
	new_name_value=current_name.toxml().replace(current_name_value, "\n"+new_name+"\n")
	f1=open(project_realpath+"\\project.xml", "r")
	f1_content=f1.read()
	f1.close()
	f1=open(project_realpath+"\\project.xml", "w+")
	f1.write(f1_content.replace(current_name.toxml(), new_name_value))
	f1.close()