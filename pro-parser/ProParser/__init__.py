#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml.dom import minidom
from math import ceil
import datetime
import os, xml

weekdays=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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

def getHalfOfTheDay(path):
		date=getDate(path)
		m=int(date.minute)/60
		h=int(date.hour)
		s=int(date.second)/6000
		return ceil((h+m+s)/12)

def getWeekNumber(path):
	date=getDate(path)
	d=int(date.day)
	m=int(date.month)
	y=int(date.year)
	return datetime.date(y, m, d).isocalendar()[1]

def findProjectByName(name, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		name=name.lower()
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				if name in getName(d[0]).lower():
					return Project(d[0])
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)

def findProjectByDescription(description, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		description=description.lower()
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				if description in getDescription(d[0]).lower():
					return Project(d[0])
			except ProjectErrpr as e:
				exec(funce)
			else:
				exec(funcelse)

def findProjectsByName(name, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		name=name.lower()
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				if name in getName(d[0]).lower():
					projects.append(Project(d[0]))
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByNameAsDict(name, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		name=name.lower()
		projects={}
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				gn=getName(d[0])
				if name in gn.lower():
					projects[gn]=Project(d[0])
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByDescription(description, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		description=description.lower()
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				if description in getDescription().lower():
					projects.append(Project(d[0]))
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByDescriptionAsDict(description, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		description=description.lower()
		projects={}
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				if description in getDescription(d[0]).lower():
					gn=getName(d[0])
					if gn:
						projects[gn]=Project(d[0])
					else:
						continue
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByLanguage(lang, directory=".", func="", funce="", funcelse="", strict=False):
	if os.path.exists(directory):
		lang=lang.lower()
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				if not strict:
					if lang in getLang(d[0]).lower():
						projects.append(Project(d[0]))
				else:
					if lang == getLang(d[0]).lower():
						projects.append(Project(d[0]))
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByLanguageAsDict(lang, directory=".", func="", funce="", funcelse="", strict=False):
	if os.path.exists(directory):
		lang=lang.lower()
		projects={}
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				if not strict:
					if lang in getLang(d[0]).lower():
						gn=getName(d[0])
						if gn:
							projects[gn]=Project(d[0])
						else:
							continue
				else:
					if lang == getLang(d[0]).lower():
						gn=getName(d[0])
						if gn:
							projects[gn]=Project(d[0])
						else:
							continue
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByAuthor(author, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		author=author.lower()
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				if author in [a.lower() for a in getAuthors(d[0])]:
					projects.append(Project(d[0]))
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByAuthorAsDict(author, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		author=author.lower()
		projects={}
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				if author in [a.lower() for a in getAuthors(d[0])]:
					gn=getName(d[0])
					if gn:
						projects[gn]=Project(d[0])
					else:
						continue
			
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByAuthors(authors, directory=".", func="", funce="", funcelse="", strict=False):
	if os.path.exists(directory):
		authors=[a.lower() for a in authors]
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				a1=[a.lower() for a in getAuthors(d[0])]
				if not strict:
					for author in authors:
						if author in a1:
							project=Project(d[0])
							if project not in projects:
								projects.append(project)
				else:
					for author in authors:
						if author not in a1:
							break
						project=Project(d[0])
						if project not in projects:
							projects.append(project)

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByAuthorsAsDict(authors, directory=".", func="", funce="", funcelse="", strict=False):
	if os.path.exists(directory):
		authors=[a.lower() for a in authors]
		projects={}
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				a1=[a.lower() for a in getAuthors(d[0])]
				if not strict:
					for author in authors:
						if author in a1:
							gn=getName(d[0])
							if gn and gn not in projects:
								projects[gn]=Project(d[0])
				else:
					for author in authors:
						if author not in a1:
							break
						gn=getName(d[0])
						if gn and gn not in projects:
							projects[gn]=Project(d[0])

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByReferenced(referenced, directory=".", func="", funce="", funcelse="", strict=False):
	if os.path.exists(directory):
		referenced=referenced.lower()
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				r=getReferenced(d[0]).lower()
				if not strict:
					if referenced in r:
						projects.append(Project(d[0]))
				else:
					if referenced == r:
						projects.append(Project(d[0]))

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByReferencedAsDict(referenced, directory=".", func="", funce="", funcelse="", strict=False):
	if os.path.exists(directory):
		referenced=referenced.lower()
		projects={}
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				r=getReferenced(d[0]).lower()
				if not strict:
					if referenced in r:
						gn=getName(d[0])
						if gn:
							projects[gn]=Project(d[0])
						else:
							continue
				else:
					if referenced == r:
						gn=getName(d[0])
						if gn:
							projects[gn]=Project(d[0])
						else:
							continue

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByVersion(version, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		version=version.lower()
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				v=getVersion(d[0]).lower()
				if not strict:
					if version in v:
						projects.append(Project(d[0]))
				else:
					if version == v:
						projects.append(Project(d[0]))

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByVersionAsDict(version, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		version=version.lower()
		projects={}
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				v=getVersion(d[0]).lower()
				if not strict:
					if version in v:
						gn=getName(d[0])
						if gn:
							projects[gn]=Project(d[0])
						else:
							continue
				else:
					if version == v:
						gn=getName(d[0])
						if gn:
							projects[gn]=Project(d[0])
						else:
							continue

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByYearAsDict(year, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		projects={}
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				y=getYear(d[0]).lower()
				if year == y:
					gn=getName(d[0])
					if gn:
						projects[gn]=Project(d[0])
					else:
						continue

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByYear(year, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				y=getYear(d[0]).lower()
				if year == y:
						projects.append(Project(d[0]))
				else:
					continue

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByMonth(month, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		if len(month) == 1:
			month="0"+month
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				m=getMonth(d[0]).lower()
				if month == m:
						projects.append(Project(d[0]))
				else:
					continue

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByMonthAsDict(month, directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		if len(month) == 1:
			month="0"+month
		projects={}
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				m=getMonth(d[0]).lower()
				if month == m:
					gn=getName(d[0])
					if gn:
						projects[gn]=Project(d[0])
				else:
					continue

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByWeek(week=datetime.date(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day).isocalendar()[1], directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		if isinstance(week, str):
			week=int(week)
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				w=getWeekNumber(d[0])
				if week == w:
						projects.append(Project(d[0]))
				else:
					continue

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByWeekAsDict(week=datetime.date(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day).isocalendar()[1], directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		if isinstance(week, str):
			week=int(week)
		projects={}
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				w=getWeekNumber(d[0])
				if week == w:
					gn=getName(d[0])
					if gn:
						projects[gn]=Project(d[0])
				else:
					continue

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByDate(year="", month="", day="", weekday="", directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		year=str(year)
		month=str(month)
		if len(month) == 1:
			month="0"+month
		day=str(day)
		if len(day) == 1:
			day="0"+day
		projects=[]
		for d in os.walk(directory):
			if not isProject(d[0]):
				continue
			try:
				exec(func)
				if year:
					y=getYear(d[0])
				if month:
					m=getMonth(d[0])
				if day:
					d1=getDay(d[0])
				if weekday:
					w=getWeekday(d[0])
				
				if year and not month and not day and not weekday:
					if y == year:
						projects.append(Project(d[0]))
				elif year and month and not day and not weekday:
					if y == year and m == month:
						projects.append(Project(d[0]))
				elif year and month and day and not weekday:
					if y == year and m == month and d1 == day:
						projects.append(Project(d[0]))
				elif not year and month and not day and not weekday:
					if m == month:
						projects.append(Projects(d[0]))
				elif not year and month and day and not weekday:
					if m == month and d1 == day:
						projects.append(Project(d[0]))
				elif not year and not month and day and not weekday:
					if d1 == day:
						projects.append(Project(d[0]))
				elif year and month and not day and weekday:
					if y == year and month == m and w == weekday:
						projects.append(Project(d[0]))
				elif year and month and day and weekday:
					if y == year and m == month and d1 == day and w == weekday:
						projects.append(Project(d[0]))
				elif not year and month and not day and weekday:
					if m == month and w == weekday:
						projects.append(Project(d[0]))
				elif not year and month and day and weekday:
					if m == month and d1 == day and w == weekday:
						projects.append(Project(d[0]))
				elif year and not month and not day and weekday:
					if y == year and w == weekday:
						projects.append(Project(d[0]))
				elif year and not month and day and weekday:
					if y == year and d1 == day and w == weekday:
						projects.append(Project(d[0]))
				elif not year and not month and not day and weekday:
					if w == weekday:
						projects.append(Project(d[0]))

			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
		return projects

def findProjectsByDateAsDict(year="", month="", day="", weekday="", directory=".", func="", funce="", funcelse=""):
	if os.path.exists(directory):
		year=str(year)
		month=str(month)
		if len(month) == 1:
			month="0"+month
		day=str(day)
		if len(day) == 1:
			day="0"+day
		projects={}
		for d in os.walk(directory):
			if isProject(d[0]):
				try:
					exec(func)
					if year:
						y=getYear(d[0])
					if month:
						m=getMonth(d[0])
					if day:
						d1=getDay(d[0])
					if weekday:
						w=getWeekday(d[0])
					
					if year and not month and not day and not weekday:
						if y == year:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
					elif year and month and not day and not weekday:
						if y == year and m == month:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
					elif year and month and day and not weekday:
						if y == year and m == month and d1 == day:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
					elif not year and month and not day and not weekday:
						if m == month:
							gn=getName(d[0])
							if gn:
								projects[gn]=Projects(d[0])
							else:
								continue
					elif not year and month and day and not weekday:
						if m == month and d1 == day:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
					elif not year and not month and day and not weekday:
						if d1 == day:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
					elif year and month and not day and weekday:
						if y == year and month == m and w == weekday:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
					elif year and month and day and weekday:
						if y == year and m == month and d1 == day and w == weekday:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
					elif not year and month and not day and weekday:
						if m == month and w == weekday:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
					elif not year and month and day and weekday:
						if m == month and d1 == day and w == weekday:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
					elif year and not month and not day and weekday:
						if y == year and w == weekday:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
					elif year and not month and day and weekday:
						if y == year and d1 == day and w == weekday:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
					elif not year and not month and not day and weekday:
						if w == weekday:
							gn=getName(d[0])
							if gn:
								projects[gn]=Project(d[0])
							else:
								continue
			
				except ProjectError as e:
					exec(funce)
				else:
					exec(funcelse)
		return projects

class Project(object):
	def __init__(self, path):
		self.name=getName(path)
		self.language=getLang(path)
		try:
			self.description=getDescription(path)
		except ProjectError:
			self.description=None
		try:
			self.authors=getAuthors(path)
		except ProjectError:
			self.authors=None
		try:
			self.version=getVersion(path)
		except ProjectError:
			self.version=None
		try:
			self.date=getDate(path)
			self.day=self.date.day
			self.weekday=self.date.weekday
			self.month=self.date.month
			self.year=self.date.year
			self.hour=self.date.hour
			self.minute=self.date.minute
			self.second=self.date.second
			self.referenced=getReferenced(path)
		except ProjectError:
			self.date=None
			self.day=None
			self.weekday=None
			self.month=None
			self.year=None
			self.hour=None
			self.minute=None
			self.second=None
			self.referenced=None
		self.fullpath=os.path.realpath(path)
		self.as_dict={"name": self.name, "language": self.language, "description": self.description, "authors": self.authors, "version": self.version, "date": {"day": self.day, "weekday": self.weekday, "month": self.month, "year": self.year, "hour": self.hour, "minute": self.minute, "second": self.second}, "referenced": self.referenced, "fullpath": self.fullpath}
		self.keys=["name", "version", "language", "description", "authors", "date", "referenced"]
		k1=[kk for kk in self.as_dict]
		k2=[kk for kk in self.as_dict["date"]]
		for i in range(len(self.as_dict)):
			if not self.as_dict[k1[i]]:
				if i in self.keys:
					self.keys.remove(k1[i])
				self.as_dict.pop(k1[i])
			elif self.as_dict[k1[i]] and isinstance(self.as_dict[k1[i]], dict):
				for ii in range(len(self.as_dict[k1[i]])):
					if not self.as_dict[k1[i]][k2[ii]]:
						self.as_dict[k1[i]].pop(k2[ii])
					if not self.as_dict[k1[i]]:
						self.as_dict.pop(k1[i])
		
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
