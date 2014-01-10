def wrtr(filename, arg2=""):
	file_extension = filename[filename.rindex(".")::].lower()
	
	if file_extension in [".html", "htm"]:
		f1=open(filename, "w+")
		text="""\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title></title>
</head>
<body>

</body>
</html>"""
		f1.write(text)
		f1.close()
	
	elif file_extension in [".c"]:
		f1=open(filename, "w+")
		text="""\
#include <stdio.h>

int main(int argc, char *argv) {

	return 0;
}"""
		f1.write(text)
		f1.close()
	
	elif file_extension in [".cpp"]:
		f1=open(filename, "w+")
		text="""\
#include <iostream>

using namespace std;

int main(int argc, char** argv) {
	
	return 0;
}"""
		f1.write(text)
		f1.close()
	
	elif file_extension in [".php"]:
		f1=open(filename, "w+")
		text="""\
<?php 

?>"""
		f1.write(text)
		f1.close()

	elif file_extension in [".css"]:
		f1=open(filename, "w+")
		text="""\
body {

}"""
		f1.write(text)
		f1.close()
	
	elif file_extension in [".xml"]:
		f1=open(filename, "w+")
		text="""\
<?xml version="1.0" encoding="utf-8"?>"""
		if arg2.lower() in ["project", "pro"]:
			text+="""\

<project>
<name>

</name>
<version>

</version>
<language>

</language>
<description>

</description>
<authors>

</authors>
<referenced>

</referenced>
<date>
<day>

</day>
<weekday>

</weekday>
<month>

</month>
<year>

</year>
<hour>

</hour>
<minute>

</minute>
<second>

</second>
</date>
</project>"""
		f1.write(text)
		f1.close()
	
	elif file_extension in [".xsd"]:
		f1=open(filename, "w+")
		text="""\
<?xml version="1.0" encoding="utf-8"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">"""
		f1.write(text)
		f1.close()

	elif file_extension in [".xsl"]:
		f1=open(filename, "w+")
		text="""\
<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/TR/WD-xsl">
</xsl:stylesheet>"""
		f1.write(text)
		f1.close()

	elif file_extension in [".svg"]:
		f1=open(filename, "w+")
		text="""\
<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100pt" height="100pt" version="1.1">'
</svg>"""
		f1.write(text)
		f1.close()
	
	elif file_extension in [".xhtml"]:
		f1=open(filename, "w+")
		text="""\
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<meta charset="utf-8" />
<title></title>
</head>
<body>

</body>
</html>"""
		f1.write(text)
		f1.close()
	
	elif file_extension in [".py"]:
		if arg2.lower() in ["main"]:
			text="""\
#!python
# -*- coding: utf-8 -*-
def main():
	pass

if __name__ == "__main__":
	main()"""
		elif arg2.lower() in ["unittest"]:
			text="""\
#!python
# -*- coding: utf-8 -*-
import unittest

class Test(unittest.TestCase):
	def test(self):
		self.failUnless(True)"""
		else:
			text="""\
#!python
# -*- coding: utf-8 -*-"""
		f1=open(filename, "w+")
		f1.write(text)
		f1.close()
	else:
		print ("Data type isn't supported")
