#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml.dom import minidom
import os, xml

class ProjectError(Exception):
	pass

def isProject(path):
	if os.path.exists(path+os.path.sep+"project.xml"):
		try:
			return True if minidom.parse(path+os.path.sep+"project.xml").documentElement.tagName == "project" else False
		except xml.parsers.expat.ExpatError:
			return False
	return False

def getLang(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		dom=minidom.parse(project_xml)
		try:
			lang=dom.getElementsByTagName("language")[0]
			lang_value=lang.childNodes[0].nodeValue
			return lang_value.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getName(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		dom=minidom.parse(project_xml)
		try:
			return dom.getElementsByTagName("name")[0].childNodes[0].nodeValue.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getVersion(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		dom=minidom.parse(project_xml)
		try:
			return dom.getElementsByTagName("version")[0].childNodes[0].nodeValue.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getAuthors(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		try:
			dom=minidom.parse(project_xml)
			return dom.getElementsByTagName("authors")[0].childNodes[0].nodeValue.strip().split(",")
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getDay(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		try:
			dom=minidom.parse(project_xml)
			return dom.getElementsByTagName("day")[0].childNodes[0].nodeValue.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getMonth(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		try:
			dom=minidom.parse(project_xml)
			return dom.getElementsByTagName("month")[0].childNodes[0].nodeValue.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getYear(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		try:
			dom=minidom.parse(project_xml)
			return dom.getElementsByTagName("year")[0].childNodes[0].nodeValue.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getHour(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		try:
			dom=minidom.parse(project_xml)
			return dom.getElementsByTagName("hour")[0].childNodes[0].nodeValue.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getMinute(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		try:
			dom=minidom.parse(project_xml)
			return dom.getElementsByTagName("minute")[0].childNodes[0].nodeValue.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getSecond(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		try:
			dom=minidom.parse(project_xml)
			return dom.getElementsByTagName("second")[0].childNodes[0].nodeValue.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getWeekday(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		try:
			dom=minidom.parse(project_xml)
			return dom.getElementsByTagName("weekday")[0].childNodes[0].nodeValue.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

class getDate(object):
	def __init__(self, path, sep="."):
		self.day = getDay(path)
		self.weekday = getWeekday(path)
		self.month = getMonth(path)
		self.year = getYear(path)
		self.hour = getHour(path)
		self.minute = getMinute(path)
		self.second = getSecond(path)
		self.sep = sep
		if len(self.day) < 2:
			self.day="0"+self.day
		if len(self.month) < 2:
			self.month="0"+self.month
	def __call__(self):
		return "%s%s%s%s%s, %s, %s:%s:%s" %(self.day, self.sep, self.month, self.sep, self.year, self.weekday, self.hour, self.minute, self.second)

def getDescription(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		dom=minidom.parse(project_xml)
		try:
			return dom.getElementsByTagName("description")[0].childNodes[0].nodeValue[1:-1]
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

def getReferenced(path):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		dom=minidom.parse(project_xml)
		try:
			return dom.getElementsByTagName("referenced")[0].childNodes[0].nodeValue.strip()
		except IndexError:
			raise ProjectError("%s is corrupted" %project_xml)
	else:
		raise ProjectError("%s is not a project" %path)

class Project(object):
	def __init__(self, path):
		self.name=getName(path)
		self.language=getLang(path)
		self.description=getDescription(path)
		self.authors=getAuthors(path)
		self.version=getVersion(path)
		self.date=getDate(path)
		self.day=self.date.day
		self.weekday=self.date.weekday
		self.month=self.date.month
		self.year=self.date.year
		self.hour=self.date.hour
		self.minute=self.date.minute
		self.second=self.date.second
		self.referenced=getReferenced(path)
		self.fullpath=os.path.realpath(path)
		self.as_dict={"name": self.name, "language": self.language, "description": self.description, "authors": self.authors, "version": self.version, "date": {"day": self.day, "weekday": self.weekday, "month": self.month, "year": self.year, "hour": self.hour, "minute": self.minute, "second": self.second}, "referenced": self.referenced, "fullpath": self.fullpath}
		self.keys=[k for k in self.as_dict]
		self.n = -1
	def __call__(self, key=None, key1=None):
		if key and key1:
			return self.as_dict[key][key]
		elif key:
			return self.as_dict[key]
		else:
			return self.as_dict
	def __iter__(self):
		return self
	def __next__(self):
		if self.n < len(self.as_dict)-1:
			self.n+=1
			return self.as_dict[self.keys[self.n]]
		else:
			raise StopIteration

def listProjects(directory="."):
	curdir=os.getcwd()
	if os.path.exists(directory):
		os.chdir(directory)
		projects = [Project(d) for d in os.listdir(".") if os.path.isdir(os.path.realpath(d)) if isProject(os.path.realpath(d))]
		os.chdir(curdir)
		return projects

def listProjectsAsDict(directory="."):
	curdir=os.getcwd()
	if os.path.exists(directory):
		os.chdir(directory)
		projects = {}
		for d in os.listdir("."):
			if isProject(d):
				project=Project(d)
				projects.setdefault(project.name, project)
		os.chdir(curdir)
		return projects

def listAllProjects(directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		curdir=os.getcwd()
		os.chdir(directory)
		projects=[]
		for d in os.walk(directory):
			if isProject(d[0]):
				try:
					if func != "":
						exec(func)
					projects.append(Project(d[0]))
				except ProjectError as e:
					if func != "":
						exec(funce)
				else:
					if funcelse != "":
						exec(funcelse)
		os.chdir(curdir)
		return projects

def listAllProjectsAsDict(directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		curdir=os.getcwd()
		os.chdir(directory)
		projects={}
		for d in os.walk(directory):
			if isProject(d[0]):
				try:
					if func != "":
						exec(func)
					project=Project(d[0])
					projects.setdefault(project.name, project)
				except ProjectError as e:
					if funce != "":
						exec(funce)
				else:
					if funcelse != "":
						exec(funcelse)
		os.chdir(curdir)
		return projects

if __name__ == "__main__":
	import sys
	try:
		if sys.argv[1].lower() in ["-e"]:
			if len(sys.argv) > 3:
				prj=Project(sys.argv[2]).as_dict
				if isinstance(prj[sys.argv[3]], dict):
					for i in prj[sys.argv[3]]:
						print("%s: %s" %(i, prj[sys.argv[3]][i]))
				elif isinstance(prj[sys.argv[3]], list):
					sys.stdout.write("%s: %s" %(sys.argv[3], prj[sys.argv[3]][0]))
					if len(prj[sys.argv[3]]) > 1:
						for i in prj[sys.argv[3]][1::]:
							sys.stdout.write(", %s" %(i[1::] if i.startswith(" ") else i))
					sys.stdout.write("\n")
				else:
					print("%s: %s" %(sys.argv[3], prj[sys.argv[3]]))
		else:
			prj=Project(sys.argv[1]).as_dict
			for i in prj:
				if isinstance(prj[i], dict):
					for ii in prj[i]:
						print("%s: %s" %(ii, prj[i][ii]))
				elif isinstance(prj[i], list):
					sys.stdout.write("%s: %s" %(i, prj[i][0]))
					if len(prj[i]) > 1:
						for ii in prj[i][1::]:
							sys.stdout.write(", %s" %(ii[1::] if ii.startswith(" ") else ii))
					sys.stdout.write("\n")
				else:
					print("%s: %s" %(i, prj[i]))
	except IndexError:
		print("usage pro-parser [-e] <project> [key]")
