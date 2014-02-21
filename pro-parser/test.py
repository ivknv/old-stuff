#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ProParser

def sortByPercent(inp):
	return inp[0]

def main():
	#print(ProParser.listProjects(".."))
	#print(ProParser.listProjectsAsDict(".."))
	total_projects=ProParser.listAllProjectsAsDict("/home/ivan/Dropbox/Python", funce="print(e)", funcelse="print(d[0])")
	print("There are %d projects created with pro" %len(total_projects))
	languages={}
	for project in total_projects:
		if total_projects[project].language not in languages:
			languages.setdefault(total_projects[project].language, 0)
		else:
			languages[total_projects[project].language]+=1
	if "" in languages:
		languages.pop("")
	m=[]
	for lang in languages:
		print("There are %d projects with programming language %s" %(languages[lang], lang))
		m.append([languages[lang]/float(len(total_projects))*100, lang])
		print("It's %f%% of all others" %(languages[lang]/float(len(total_projects))*100))
	m.sort(key=sortByPercent)
	m.reverse()
	print(m)
	input_=input(">>> ")
	for i in total_projects[input_]:
		print(i)

def second():
	prj=ProParser.Project(".")
	for i in prj:
		print(i)
def third():
	i=ProParser.getPercentageByYear("2014", "../../../Dropbox", func="print(\"projects: %d\" %(projects_with_year));print(\"Year: %s\" %getYear(d[0]))")

	print(i)

def fourth():
	print(ProParser.getPercentageLang("../../../Dropbox", func="print(d[0])", funce="print(e)"))

if __name__ == "__main__":
	#main()
	#second()
	#third()
	fourth()
