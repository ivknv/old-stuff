#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.dom.minidom as minidom, re

class ParseError(Exception):
	pass

def parsePatterns(path):
	dom=minidom.parse(path)
	comments=dom.getElementsByTagName("comment")
	patterns={}
	for comment in comments:
		patterns_=comment.getElementsByTagName("pattern")
		for pattern in patterns_:
			try:
				text=comment.getElementsByTagName("text")[0].firstChild.nodeValue
			except IndexError:
				raise ParseError("There's a problem with comment text")
			try:
				position=comment.getElementsByTagName("position")[0].firstChild.nodeValue.strip().lower()
			except IndexError:
				position="top"
			commentStart=comment.getAttribute("commentStart")
			commentEnd=comment.getAttribute("commentEnd")
			filetype=comment.getAttribute("filetype")
			variables=comment.getElementsByTagName("variable")
			vs={}
			for v in variables:
				index=v.getAttribute("index")
				vs[v.getAttributeNode("name").nodeValue]={"value": v.firstChild.nodeValue, "type": v.getAttribute("type"), "index": int(index) if index else 0 }
			patterns[pattern.firstChild.nodeValue]={"text": text, "position": position, "variables": vs, "filetype": filetype, "commentStart": commentStart, "commentEnd": commentEnd}
	return patterns

def comment(code, path, filetype):
	codelines=code.split("\n")
	patterns=parsePatterns(path)
	i=0
	for line in codelines:
		for pattern in patterns:
			if patterns[pattern]["filetype"]==filetype:
				if re.findall(pattern, line):
					if patterns[pattern]["variables"]:
						vs={}
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
	return codestr

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Automatic code commenting")
	parser.add_argument("file", help="File name")
	parser.add_argument("-p", "--path", help="Path to the patterns file")
	parser.add_argument("-w", "--write", action="store_true", help="Write to the file")
	parser.add_argument("-i", "--ignore-comments", action="store_true", help="Ignore comments")
	parser.add_argument("-cs", "--comment-start", help="Comment start")
	parser.add_argument("-ce", "--comment-end", help="Comment end")
	args=parser.parse_args()
	if args.file:
		f1=open(args.file)
		code=f1.read()
		f1.close()
		if args.ignore_comments:
			comments=re.findall(args.comment_start+".*"+args.comment_end, code)
			for i in comments:
				code=code.replace(i, "")
		if args.path:
			modified=comment(code, args.path, args.file[args.file.rindex(".")+1:].lower())
		else:
			modified=comment(code, "patterns.xml", args.file[args.file.rindex(".")+1:].lower())
		if args.write:
			f1=open(args.file, "w")
			f1.write(modified)
			f1.close()
		else:
			print(modified)
