#!/usr/bin/env python
# -*- coding: utf-8 -*-

def checkSimilarity(s1, s2):
	is1=iter(s1)
	is2=iter(s2)
	p=0
	pc=100.0/max(len(s1), len(s2))
	for (i, ii) in zip(is1, is2):
		if i==ii:
			p+=pc
	return p

def checkSimilarityWords2(s1, s2):
	s1=s1.split(" ")
	s2=s2.split(" ")
	p=0
	pc=100.0/max(len(s1), len(s2))
	for i in s1:
		try:
			if i in s2:
				p+=pc*s2.count(i)
		except IndexError:
			pass
	return p

def checkSimilaritySort(s1, s2):
	ss1=iter(sorted(s1))
	ss2=iter(sorted(s2))
	p=0
	pc=100.0/max(len(s1), len(s2))
	for (i, ii) in zip(ss1, ss2):
		if i==ii:
			p+=pc
	return p

def checkSimilaritySortEmpty(s1, s2):
	s1=sorted(s1)
	s2=sorted(s2)
	p=0
	i=0
	pc=100.0/max(len(s1), len(s2))
	while i<max(len(s2), len(s2)):
		try:
			if s1[i]==s2[i]:
				p+=pc
		except IndexError:
			break
		i+=1

def checkSimilaritySortEmptyWords(s1, s2):
	s1=s1.split(" ")
	s2=s2.split(" ")
	s1.sort()
	s2.sort()
	p=0
	i=0
	pc=100.0/max(len(s1), len(s2))
	while i<max(len(s2), len(s2)):
		try:
			if s1[i]==s2[i]:
				p+=pc
		except IndexError:
			break
		i+=1
	
	return p

def checkSimilaritySortWords(s1, s2):
	s1=s1.split(" ")
	s2=s2.split(" ")
	s1.sort()
	s2.sort()
	p=0
	i=0
	pc=100.0/max(len(s1), len(s2))
	while i<max(len(s2), len(s2)):
		try:
			if s1[i]==s2[i]:
				p+=pc
		except IndexError:
			pass
		i+=1

def checkSimilarityWords(s1, s2):
	s1=s1.split(" ")
	s2=s2.split(" ")
	p=0
	i=0
	pc=100.0/max(len(s1), len(s2))
	while i<max(len(s2), len(s2)):
		try:
			if s1[i]==s2[i]:
				p+=pc
		except IndexError:
			pass
		i+=1
	return p

def checkSimilarityEmpty(s1, s2):
	p=0
	i=0
	pc=100.0/max(len(s1), len(s2))
	while i<max(len(s2), len(s2)):
		try:
			if s1[i]==s2[i]:
				p+=pc
		except IndexError:
			break
		i+=1
	return p

def findFirstDifference(s1, s2):
	i=0
	while i<max(len(s1), len(s2)):
		try:
			if s1[i]!=s2[i]:
				return i
		except IndexError:
			return i
		i+=1
def findAllDifferences(s1, s2):
	differences=[]
	i=0
	while i<max(len(s1), len(s2)):
		try:
			if s1[i]!=s2[i]:
				differences.append(i)
		except IndexError:
			differences.append(i)
		i+=1
	return differences

def findAllDifferencesLine(s1, s2):
	differences=[]
	i=0
	s1=s1.split("\n")
	s2=s2.split("\n")
	while i<max(len(s1), len(s2)):
		try:
			if s1[i]!=s2[i]:
				differences.append((i, s1[i], s2[i]))
		except IndexError:
			m=s1 if len(s1)>len(s2) else s2
			differences.append((i, m[i] if m == s1 else "", m[i] if m == s2 else ""))
		i+=1
	return differences

def findFirstDifferenceLine(s1, s2):
	i=0
	s1=s1.split("\n")
	s2=s2.split("\n")
	while i<max(len(s1), len(s2)):
		try:
			if s1[i]!=s2[i]:
				return [i, s1[i], s2[i]]
		except IndexError:
			m=s1 if len(s1)>len(s2) else s2
			return [i, m[i] if m == s1 else "", m[i] if m == s2 else ""]
		i+=1
	return []
