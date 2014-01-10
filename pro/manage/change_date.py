# -*- coding: utf-8 -*-
from xml.dom import minidom
import os
from datetime import datetime

def update_date(project):
	weekdays=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	now=datetime.now()
	project_realpath=os.path.realpath(project)
	dom=minidom.parse(project_realpath+"\\project.xml")
	current_day=dom.getElementsByTagName("day")[0]
	current_day_value=current_day.childNodes[0].nodeValue
	new_day_value=current_day.toxml().replace(current_day_value, "\n"+str(now.day)+"\n")
	current_month=dom.getElementsByTagName("month")[0]
	current_month_value=current_month.childNodes[0].nodeValue
	new_month_value=current_month.toxml().replace(current_month_value, "\n"+str(now.month)+"\n")
	current_year=dom.getElementsByTagName("year")[0]
	current_year_value=current_year.childNodes[0].nodeValue
	new_year_value=current_year.toxml().replace(current_year_value, "\n"+str(now.year)+"\n")
	current_weekday=dom.getElementsByTagName("weekday")[0]
	current_weekday_value=current_weekday.childNodes[0].nodeValue
	new_weekday_value=current_weekday.toxml().replace(current_weekday_value, "\n"+weekdays[now.isoweekday()-1]+"\n")
	current_hour=dom.getElementsByTagName("hour")[0]
	current_hour_value=current_hour.childNodes[0].nodeValue
	new_hour_value=current_hour.toxml().replace(current_hour_value, "\n"+str(now.hour)+"\n")
	current_minute=dom.getElementsByTagName("minute")[0]
	current_minute_value=current_minute.childNodes[0].nodeValue
	new_minute_value=current_minute.toxml().replace(current_minute_value, "\n"+str(now.minute)+"\n")
	current_second=dom.getElementsByTagName("second")[0]
	current_second_value=current_second.childNodes[0].nodeValue
	new_second_value=current_second.toxml().replace(current_second_value, "\n"+str(now.second)+"\n")
	f1=open(project_realpath+"\\project.xml", "r")
	f1_content=f1.read()
	f1.close()
	f1=open(project_realpath+"\\project.xml", "w+")
	f1.write(f1_content.replace(current_day.toxml(), new_day_value).replace(current_month.toxml(), new_month_value).replace(current_year.toxml(), new_year_value).replace(current_weekday.toxml(), new_weekday_value).replace(current_hour.toxml(), new_hour_value).replace(current_minute.toxml(), new_minute_value).replace(current_second.toxml(), new_second_value))
	f1.close()
