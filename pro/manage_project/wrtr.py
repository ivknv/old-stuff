import sys, os

def wrtr(filename, arg2="", arg3="1.2.8"):
	file_extension = filename[filename.rindex(".")::].lower()
	
	if file_extension in [".html", "htm"]:
		f1=open(filename, "w+")
		if arg2.lower() in ["jquery"]:
			text="""\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title></title>
<script type="text/javascript" src="http://code.jquery.com/jquery-latest.min.js"></script>
</head>
<body>

</body>
</html>"""
		elif arg2.lower() in ["jqueryui", "jquery-ui", "jquery_ui", "jquery ui"]:
			text="""\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title></title>
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>
</head>
<body>

</body>
</html>"""

		elif arg2.lower() in ["angular", "angularjs", "angular.js",
						"angular js"]:
				text="""\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title></title>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/angularjs/%s/angular.min.js"></script>
</head>
<body>

</body>
</html>""" %(arg3)

		else:
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

int main(int argc, char **argv) {

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
#!/usr/bin/python
# -*- coding: utf-8 -*-
def main():
	pass

if __name__ == "__main__":
	main()"""
		elif arg2.lower() in ["unittest"]:
			text="""\
#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

class Test(unittest.TestCase):
	def test(self):
		self.failUnless(True)"""
		elif arg2.lower() in ["pyside"]:
			text="""\
#!/usr/bin/python
# -*- coding: utf-8

import sys
from PySide import QtGui

class Main(QtGui.QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		
		self.initUI()
	def initUI(self):
		self.setGeometry(300, 300, 640, 480)
		self.setWindowTitle("")
		self.show()

def main():
	app = QtGui.QApplication(sys.argv)
	M=Main()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()"""
		else:
			text="""\
#!/usr/bin/python
# -*- coding: utf-8 -*-"""
		f1=open(filename, "w+")
		f1.write(text)
		f1.close()
	elif file_extension in [".java"]:
		text="""\
public class %name% {
	public static void main(String args[]) {
		
	}
}""".replace("%name%", filename[filename.rindex(os.path.sep)+1:filename.index(".")])
		f1=open(filename, "w")
		f1.write(text)
		f1.close()
	else:
		print ("Data type isn't supported")
