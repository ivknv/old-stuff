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

if __name__ == "__main__":
	main()
	#second()
