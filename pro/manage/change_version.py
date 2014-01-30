# -*- coding: utf-8 -*-
from xml.dom import minidom
import os

def change_version(project, new_version):
	project_realpath=os.path.realpath(project)
	dom=minidom.parse(project_realpath+os.path.sep+"project.xml")
	current_version=dom.getElementsByTagName("version")[0]
	current_version_value=current_version.childNodes[0].nodeValue
	new_version_value=current_version.toxml().replace(current_version_value, "\n"+new_version+"\n")
	f1=open(project_realpath+os.path.sep+"project.xml", "r")
	f1_content=f1.read()
	f1.close()
	f1=open(project_realpath+os.path.sep+"project.xml", "w+")
	f1.write(f1_content.replace(current_version.toxml(), new_version_value))
	f1.close()
