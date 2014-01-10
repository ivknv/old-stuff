Pro is a simple script that allows
 you to creates simple projects.

Example:
$ pro Test Python "Just a test" Ivan test01
Test/
	bin/
		init.py
	doc/
		doc.xhtml
		style.css
	manage/
		__init__.py
		change_author.py
		change_date.py
		change_description.py
		change_lang.py
		change_name.py
		change_version.py
		pycompileall.py
		pyinit.py
		wrtr.py
	Test/
		init.py
	__init__.py
	test01/
		...
	manage.py
	project.xml

project.xml - a XML file that
contains information about project.
manage.py - a Python script that
allows you to easily edit
project.xml.
