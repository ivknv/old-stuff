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

def getTag(path, tag):
	if isProject(path):
		project_xml=path+os.path.sep+"project.xml"
		try:
			dom=minidom.parse(project_xml)
			return dom.getElementsByTagName(tag)[0].childNodes[0].nodeValue[1:-1]
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
		self.keys=["name", "version", "language", "description", "authors", "date", "referenced"]
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
		if self.n < len(self.keys)-1:
			self.n+=1
			return self.as_dict[self.keys[self.n]]
		else:
			raise StopIteration

def listProjects(directory="."):
	if os.path.exists(directory):
		projects = [Project(directory+os.path.sep+d) for d in os.listdir(directory) if os.path.isdir(os.path.realpath(directory+os.path.sep+d)) if isProject(os.path.realpath(directory+os.path.sep+d))]
		return projects

def listProjectsAsDict(directory="."):
	if os.path.exists(directory):
		projects = {}
		for d in os.listdir(directory):
			if isProject(directory+os.path.sep+d):
				project=Project(directory+os.path.sep+d)
				projects.setdefault(project.name, project)
		return projects

def listAllProjects(directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
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
		return projects

def listAllProjectsAsDict(directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
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
		return projects

def getPercentageOfProjects(directory=".", func="", funce="", funcelse=""):
	projects=0
	dirs=0
	for d in os.walk(directory):
		if os.path.isdir(d[0]):
			dirs+=1
		if isProject(d[0]):
			try:
				exec(func)
				project=Project(d[0])
			except ProjectError as e:
				exec(funce)
			else:
				projects+=1
				exec(funcelse)
	
	return 100.0/dirs*projects

def getPercentageByLanguage(lang, directory=".", func="", funce="", funcelse=""):
	projects=0
	projects_with_lang=0
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				if getLang(d[0]).lower() == lang.lower():
					projects_with_lang+=1
				projects+=1
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	return 100.0/projects*projects_with_lang

def getPercentageByMonth(month, directory=".", func="", funce="", funcelse=""):
	if len(month) == 1:
		month="0"+month
	projects=0
	projects_with_month=0
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				if month == getMonth(d[0]):
					projects_with_month+=1
				projects+=1
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	return 100.0/projects*projects_with_month

def getPercentageByYear(year, directory=".", func="", funce="", funcelse=""):
	projects=0
	projects_with_year=0
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				if year == getYear(d[0]):
					projects_with_year+=1
				projects+=1
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	return 100.0/projects*projects_with_year

def getPercentageByDay(day, directory=".", func="", funce="", funcelse=""):
	if len(day) == 1:
		day="0"+day
	projects=0
	projects_with_day=0
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				if day == getDay(d[0]):
					projects_with_day+=1
				projects+=1
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	return 100.0/projects*projects_with_day

def getPercentageByWeekday(weekday, directory=".", func="", funce="", funcelse=""):
	weekdays=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	if isinstance(weekday, int):
		weekday=weekdays[weekday-1]
	elif isinstance(weekday, str):
		if weekday.isdigit():
			weekday=weekdays[int(weekday)-1]
	projects=0
	projects_with_weekday=0
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				if weekday == getWeekday(d[0]):
					projects_with_weekday+=1
				projects+=1
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	return 100.0/projects*projects_with_weekday

def getPercentageByHour(hour, directory=".", func="", funce="", funcelse=""):
	projects=0
	projects_with_hour=0
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				if hour == getHour(d[0]):
					projects_with_hour+=1
				projects+=1
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	return 100.0/projects*projects_with_hour

def getPercentageByDescription(description, directory=".", func="", funce="", funcelse=""):
	projects=0
	projects_with_description=0
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				if description.lower() in getDescription(d[0]).lower():
					projects_with_description+=1
				projects+=1
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	return 100.0/projects*projects_with_description

def getPercentageByAuthor(author, directory=".", func="", funce="", funcelse=""):
	projects=0
	projects_with_author=0
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				if author.lower() in [a.lower() for a in getAuthors(d[0])]:
					projects_with_author+=1
				projects+=1
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	return 100.0/projects*projects_with_author

def getPercentageByReferenced(referenced, directory=".", func="", funce="", funcelse=""):
	projects=0
	projects_with_referenced=0
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				if referenced.lower() == getReferenced(d[0]):
					projects_with_referenced+=1
				projects+=1
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	return 100.0/projects*projects_with_referenced

def getPercentage(tag, directory=".", func="", funce="", funcelse=""):
	projects={}
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				gn=getName(d[0])
				tvalue=getTag(d[0], tag)
				if gn and tvalue:
					projects[gn] = tvalue
				else:
					continue
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	data={}
	for j in projects:
		if not projects[j] in data:
			data[projects[j]]=1
		else:
			data[projects[j]]+=1	
	ds={}
	for j in data:
		ds[j] = 100.0/len(projects)*data[j]
	return ds

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
