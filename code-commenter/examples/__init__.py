#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.dom.minidom as minidom, re

# all the comments except this are autogenerated

class ParseError(Exception):
	pass

def parsePatterns(path): # Get patterns from path
	dom=minidom.parse(path) # Parse XML document
	comments=dom.getElementsByTagName("comment") # Get list of tags with name "comment"
	patterns={}
	for comment in comments:
		patterns_=comment.getElementsByTagName("pattern") # Get list of tags with name "pattern"
		for pattern in patterns_:
			try:
				text=comment.getElementsByTagName("text")[0].firstChild.nodeValue # Get list of tags with name "text"
			except IndexError:
				raise ParseError("comment text is empty")
			try:
				position=comment.getElementsByTagName("position")[0].firstChild.nodeValue.strip().lower() # Get list of tags with name "position"
			except IndexError:
				position="top"
			commentStart=comment.getAttribute("commentStart") # Get "commentStart" attribute from tag
			commentEnd=comment.getAttribute("commentEnd") # Get "commentEnd" attribute from tag
			filetype=comment.getAttribute("filetype").lower() # Get "filetype" attribute from tag
			variables=comment.getElementsByTagName("variable") # Get list of tags with name "variable"
			vs={}
			for v in variables:
				index=v.getAttribute("index") # Get "index" attribute from tag
				vs[v.getAttributeNode("name").nodeValue]={"value": v.firstChild.nodeValue, "type": v.getAttribute("type"), "index": int(index) if index else 0 } # Get "index" attribute from tag
			patterns[pattern.firstChild.nodeValue]={"text": text, "position": position, "variables": vs, "filetype": filetype, "commentStart": commentStart, "commentEnd": commentEnd}
	return patterns

def comment(code, path, filetype, startpos=0, endpos=None):
	if type(startpos)!=int:
		startpos=int(startpos)
	if not endpos:
		codelines=code.split("\n")[startpos:]
	else:
		if type(endpos)!=int:
			endpos=int(endpos)
		codelines=code.split("\n")[startpos:endpos]
	patterns=parsePatterns(path) # Get patterns from path
	i=0
	for line in codelines:
		for pattern in patterns:
			if patterns[pattern]["filetype"]==filetype.lower():
				if re.findall(pattern, line):
					vs={}
					if patterns[pattern]["variables"]:
						for v in patterns[pattern]["variables"]:
							
							if patterns[pattern]["variables"][v]["type"]=="regex":
								res=re.findall(patterns[pattern]["variables"][v]["value"], line)
								if res:
									vs[v]=res[patterns[pattern]["variables"][v]["index"]]
								else: vs[v]=""
							else:
								vs[v]=patterns[pattern]["variables"][v]["value"]
					if not re.search(patterns[pattern]["commentStart"], line):
						if patterns[pattern]["position"]=="top":
							codelines[i]="%s\n%s" %(patterns[pattern]["commentStart"].replace("\\", "")+patterns[pattern]["text"]+patterns[pattern]["commentEnd"].replace("\\", ""), line)
						elif patterns[pattern]["position"]=="bottom":
							codelines[i]="%s\n%s" %(line, patterns[pattern]["commentStart"]+patterns[pattern]["text"]+patterns[pattern]["commetnEnd"])
						elif patterns[pattern]["position"]=="right":
							codelines[i]="%s %s" %(line, patterns[pattern]["commentStart"].replace("\\", "")+patterns[pattern]["text"]+patterns[pattern]["commentEnd"].replace("\\", ""))
						elif patterns[pattern]["position"]=="left":
							codelines[i]="%s %s" %(patterns[pattern]["text"], line)
						else:
							codelines[i]="%s\n%s" %(patterns[pattern]["text"], line)
						for v in vs:
							codelines[i]=codelines[i].replace("%%%s%%" %v, vs[v])
		i+=1
	codestr=""
	for i in codelines:
		codestr+=i+"\n"
	return codestr[0:-1]