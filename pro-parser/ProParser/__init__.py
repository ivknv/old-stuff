#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml.dom import minidom
from math import ceil
import datetime
import os, xml, sys, sqlite3

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

def getLang(path, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT language FROM project;")
				lang = cur.fetchall()
				con.close()
				return lang[0][0]
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			dom=minidom.parse(project_info)
			try:
				lang=dom.getElementsByTagName("language")[0]
				lang_value=lang.childNodes[0].nodeValue
				return lang_value.strip()
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getName(path, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT name FROM project;")
				name = cur.fetchall()
				con.close()
				return name[0][0]
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			dom=minidom.parse(project_info)
			try:
				return dom.getElementsByTagName("name")[0].childNodes[0].nodeValue.strip()
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getVersion(path, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT version FROM project;")
				version = cur.fetchall()
				con.close()
				return version[0][0]
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			dom=minidom.parse(project_info)
			try:
				return dom.getElementsByTagName("version")[0].childNodes[0].nodeValue.strip()
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getAuthors(path, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT authors FROM project;")
				authors = cur.fetchall()[0][0]
				if "," in authors:
					authors=authors.split(",")
				else:
					authors=[authors]
				con.close()
				return authors
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			try:
				dom=minidom.parse(project_info)
				return dom.getElementsByTagName("authors")[0].childNodes[0].nodeValue.strip().split(",")
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getDay(path, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT day FROM project;")
				day = cur.fetchall()
				con.close()
				return str(day[0][0])
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			try:
				dom=minidom.parse(project_info)
				return dom.getElementsByTagName("day")[0].childNodes[0].nodeValue.strip()
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getMonth(path, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT month FROM project;")
				month = cur.fetchall()
				con.close()
				return str(month[0][0])
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			try:
				dom=minidom.parse(project_info)
				return dom.getElementsByTagName("month")[0].childNodes[0].nodeValue.strip()
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getYear(path, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT year FROM project;")
				year = cur.fetchall()
				con.close()
				return str(year[0][0])
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			try:
				dom=minidom.parse(project_info)
				return dom.getElementsByTagName("year")[0].childNodes[0].nodeValue.strip()
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getHour(path, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT hour FROM project;")
				hour = cur.fetchall()
				con.close()
				return str(hour[0][0])
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			try:
				dom=minidom.parse(project_info)
				return dom.getElementsByTagName("hour")[0].childNodes[0].nodeValue.strip()
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getTag(path, tag, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT %s FROM project;" %tag)
				tagres = cur.fetchall()
				con.close()
				return str(tagres[0][0])
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			try:
				dom=minidom.parse(project_info)
				return dom.getElementsByTagName(tag)[0].childNodes[0].nodeValue[1:-1]
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getMinute(path, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT minute FROM project;")
				minute = cur.fetchall()
				con.close()
				return str(minute[0][0])
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			try:
				dom=minidom.parse(project_info)
				return dom.getElementsByTagName("minute")[0].childNodes[0].nodeValue.strip()
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getSecond(path, db=False):
	if isProject(path):
		if db:
			project_info=path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT second FROM project;")
				second = cur.fetchall()
				con.close()
				return str(second[0][0])
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			try:
				dom=minidom.parse(project_info)
				return dom.getElementsByTagName("second")[0].childNodes[0].nodeValue.strip()
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getWeekday(path, db=False):
	if isProject(path):
		if db:
			project_info = path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT * FROM project;")
				weekday = cur.fetchall()
				con.close()
				return weekday[0][0]
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			try:
				dom=minidom.parse(project_info)
				return dom.getElementsByTagName("weekday")[0].childNodes[0].nodeValue.strip()
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

class getDate(object):
	def __init__(self, path, sep=".", db=False):
		self.day = getDay(path, db=db)
		self.weekday = getWeekday(path, db=db)
		self.month = getMonth(path, db=db)
		self.year = getYear(path, db=db)
		self.hour = getHour(path, db=db)
		self.minute = getMinute(path, db=db)
		self.second = getSecond(path, db=db)
		self.sep = sep
		if len(self.day) < 2:
			self.day="0"+self.day
		if len(self.month) < 2:
			self.month="0"+self.month
		if len(self.hour) < 2:
			self.hour="0"+self.hour
		if len(self.minute) < 2:
			self.minute="0"+self.minute
		if len(self.second) < 2:
			self.second="0"+self.second
	def __call__(self):
		return "%s%s%s%s%s, %s, %s:%s:%s" %(self.day, self.sep, self.month, self.sep, self.year, self.weekday, self.hour, self.minute, self.second)

def getDescription(path, db=False):
	if isProject(path):
		if db:
			project_info=path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				cur.execute("SELECT description FROM project;")			
				description=cur.fetchall()
				con.close()
				return description[0][0]
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			dom=minidom.parse(project_info)
			try:
				return dom.getElementsByTagName("description")[0].childNodes[0].nodeValue[1:-1]
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getReferenced(path, db=False):
	if isProject(path):
		if db:
			project_info=path+os.path.sep+"project.db"
			con = sqlite3.connect(project_info)
			cur = con.cursor()
			try:
				con.execute("SELECT referenced FROM project;")
				ref=cur.fetchall()
				if ref:
					con.close()
					if "," in ref[0][0]:
						ref=ref[0][0].split(",")
					else:
						ref=[ref[0][0]]
				return ref
			except sqlite3.OperationalError as e:
				print(e)
		else:
			project_info=path+os.path.sep+"project.xml"
			dom=minidom.parse(project_info)
			try:
				return dom.getElementsByTagName("referenced")[0].childNodes[0].nodeValue.split("\n")
			except IndexError:
				raise ProjectError("%s is corrupted" %project_info)
	else:
		raise ProjectError("%s is not a project" %path)

def getHalfOfTheDay(path, db=False):
		date=getDate(path, db=db)
		m=int(date.minute)/60
		h=int(date.hour)
		s=int(date.second)/6000
		return ceil((h+m+s)/12)

def getWeekNumber(path, db=False):
	date=getDate(path, db=db)
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
	def __init__(self, path, db=False):
		self.name=getName(path)
		self.language=getLang(path)
		try:
			self.description=getDescription(path, db=db)
		except ProjectError:
			self.description=None
		try:
			self.authors=getAuthors(path, db=db)
		except ProjectError:
			self.authors=None
		try:
			self.version=getVersion(path, db=db)
		except ProjectError:
			self.version=None
		try:
			self.date=getDate(path, db=db)
			self.day=self.date.day
			self.weekday=self.date.weekday
			self.month=self.date.month
			self.year=self.date.year
			self.hour=self.date.hour
			self.minute=self.date.minute
			self.second=self.date.second
			self.referenced=getReferenced(path, db=db)
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

def convertProjectToSql(path):
	project = Project(path)
	a = project.authors
	authors=a[0]
	if len(authors) > 1:
		for i in a[1:]:
			authors+=", {}".format(i)
	r = project.referenced
	if r:
		ref=r[0]
		if len(r) > 1:
			for i in r[1:]:
				ref+=", {}".format(i)
	else:
		ref=""
	con = sqlite3.connect(path+os.path.sep+"project.db")
	cur = con.cursor()
	sqls = "CREATE TABLE project(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(120), version VARCHAR(50), authors VARCHAR(300), description TEXT, day INTEGER, month INTEGER, year INTEGER, hour INTEGER, minute INTEGER, second INTEGER, weekday VARCHAR(30), referenced TEXT);"
	sqls1="INSERT INTO project(name, version, authors, description, day, month, year, hour, minute, second, weekday, referenced) VALUES(\"{}\", \"{}\", \"{}\", \"{}\", {}, {}, {}, {}, {}, {}, \"{}\", \"{}\");".format(project.name, project.version, authors, project.description, project.day, project.month, project.year, project.hour, project.minute, project.second, project.weekday, ref)
	try:
		cur.execute(sqls)
		cur.execute(sqls1)
		con.commit()
		con.close()
	except sqlite3.OperationalError as e:
		print(e)

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

def getPercentageByTag(tag, directory=".", func="", funce="", funcelse=""):
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

def getPercentage(directory=".", func="", funce="", funcelse=""):
	projects={}
	for d in os.walk(directory):
		if isProject(d[0]):
			try:
				exec(func)
				project=Project(d[0])
				if project.name:
					projects[project.name] = project
				else:
					continue
			except ProjectError as e:
				exec(funce)
			else:
				exec(funcelse)
	languages={}
	authors={}
	weekdays={}
	days={}
	months={}
	years={}
	referenced={}
	versions={}
	
	for i in projects:
		project=projects[i]
		if project.language:
			pl=project.language.lower().capitalize()
			if not pl in languages:
				languages[pl]=1
			else:
				languages[pl]+=1
		if project.authors:
			for a in project.authors:
				if not a in authors:
					authors[a]=1
				else:
					authors[a]+=1
		if project.weekday:
			w=project.weekday.lower().capitalize()
			if not w in weekdays:
				weekdays[w]=1
			else:
				weekdays[w]+=1
		if project.day:
			if not project.day in days:
				days[project.day]=1
			else:
				days[project.day]+=1
		if project.month:
			if not project.month in months:
				months[project.month]=1
			else:
				months[project.month]+=1
		if project.year:
			if not project.year in years:
				years[project.year]=1
			else:
				years[project.year]+=1
		if project.referenced:
			if not project.referenced in referenced:
				referenced[project.referenced]=1
			else:
				referenced[project.referenced]+=1
		if project.version:
			if not project.version in versions:
				versions[project.version]=1
			else:
				versions[project.version]+=1
	data={"languages": languages, "versions": versions, "referenced": referenced, "days": days, "weekdays": weekdays, "authors": authors, "months": months, "years": years}
	ds={}
	for i in data:
		ds[i]={}
		for j in data[i]:
			ds[i][j] = 100.0/sum([data[i][ii] for ii in data[i]])*data[i][j]
	return ds


if __name__ == "__main__":
	import argparse
	from sys import stdout
	parser = argparse.ArgumentParser(description="The parser for projects, created with pro.")
	parser.add_argument("path", help="path to the project")
	parser.add_argument("-e", "--exact", nargs="+", help="keys to print")
	args = parser.parse_args()
	if args.path:
		try:
			project=Project(args.path)
		except ProjectError:
			print("Doesn't look like '{}' is a project, created with pro".format(path))
		
		if args.exact:
			if len(args.exact) == 1:
				try:
					if isinstance(project.as_dict[args.exact[0]], dict):
						for i in project.as_dict[args.exact[0]]:
							print("\033[1m{}\033[0m: {}".format(i.capitalize(), project.as_dict[args.exact[0]][i]))
					elif isinstance(project.as_dict[args.exact[0]], list):
						for i in project.as_dict[args.exact[0]]:
							print("\033[1m{}\033[0m: {}".format(args.exact[0].capitalize(), i))
					else:
						print("\033[1m{}\033[0m: {}".format(args.exact[0].lower().capitalize(), project.as_dict[args.exact[0]]))
				except KeyError:
					print("'{}' project doesn't have such key".format(project.name))
			else:
				for key in args.exact:
					key=key.lower()
					if key in project.as_dict:
						if isinstance(project.as_dict[key], dict):
							for k in project.as_dict[key]:
								print("\033[1m{}\033[0m: {}".format(k.capitalize(), project.as_dict[key][k]))
						elif isinstance(project.as_dict[key], list):
							stdout.write("\033[1m{}\033[0m: {}".format(key.capitalize(), project.as_dict[key][0]))
							if len(project.as_dict[key]) > 1:
								for i in project.as_dict[key][1:]:
									stdout.write(", {}".format(i))
							stdout.write("\n")
							stdout.flush()
							print("\033[1m{}\033[0m: {}".format(key.capitalize(), project.as_dict[key]))
						else:
							print("\033[1m{}\033[0m: {}".format(key.capitalize(), project.as_dict[key]))
		else:
			for i in project.as_dict:
				if isinstance(project.as_dict[i], dict):
					for ii in project.as_dict[i]:
						print("\033[1m{}\033[0m: {}".format(ii.capitalize(), project.as_dict[i][ii]))
				elif isinstance(project.as_dict[i], list):
					stdout.write("\033[1m{}\033[0m: ".format(i.capitalize()))
					stdout.write(project.as_dict[i][0])
					if len(project.as_dict[i]) > 1:
						for ii in project.as_dict[i][1::]:
							stdout.write(", {}".format(ii))
					stdout.write("\n")
					stdout.flush()
				else:
					print("\033[1m{}\033[0m: {}".format(i.capitalize(), project.as_dict[i]))	
