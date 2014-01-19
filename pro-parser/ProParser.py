from xml.dom import minidom
import os

def isProject(path):
	if os.path.exists(path+os.path.sep+"project.xml"):
		return True if minidom.parse(path+os.path.sep+"project.xml").getElementsByTagName("project") else False
	return False

def parseProject(path):
	if isProject(path):
		project_xml=minidom.parse(path+os.path.sep+"project.xml")
		project=project_xml.getElementsByTagName("project")[0]
		name=project.getElementsByTagName("name")[0].childNodes[0].nodeValue
		language=project.getElementsByTagName("language")[0].childNodes[0].nodeValue
		description=project.getElementsByTagName("description")[0].childNodes[0].nodeValue
		authors=project.getElementsByTagName("authors")[0].childNodes[0].nodeValue
		version=project.getElementsByTagName("version")[0].childNodes[0].nodeValue
		date=project.getElementsByTagName("date")[0]
		day=date.getElementsByTagName("day")[0].childNodes[0].nodeValue
		weekday=date.getElementsByTagName("weekday")[0].childNodes[0].nodeValue
		month=date.getElementsByTagName("month")[0].childNodes[0].nodeValue
		year=date.getElementsByTagName("year")[0].childNodes[0].nodeValue
		hour=date.getElementsByTagName("hour")[0].childNodes[0].nodeValue
		minute=date.getElementsByTagName("minute")[0].childNodes[0].nodeValue
		second=date.getElementsByTagName("second")[0].childNodes[0].nodeValue
		return {"name": name.strip(), "language": language.strip(), "description": description[1:-1], "authors": authors.strip(), "version": version.strip(), "date": {"day": day.strip(), "weekday": weekday.strip(), "month": month.strip(), "year": year.strip(), "hour": hour.strip(), "minute": minute.strip(), "second": second.strip()}}
if __name__ == "__main__":
	import sys
	if sys.argv[1].lower() in ["-e"]:
		if len(sys.argv) > 3:
			prj=parseProject(sys.argv[2])
			if isinstance(prj[sys.argv[3]], dict):
				for i in prj[sys.argv[3]]:
					print("%s: %s" %(i, prj[sys.argv[3]][i]))
			else:
				print("%s: %s" %(sys.argv[3], prj[sys.argv[3]]))
	else:
		prj=parseProject(sys.argv[1])
		for i in prj:
			if isinstance(prj[i], dict):
				for ii in prj[i]:
					print("%s: %s" %(ii, prj[i][ii]))
			else:
				print("%s: %s" %(i, prj[i]))