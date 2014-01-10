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
Example of using manage.py:
$ python manage.py compile
# it will compile your source code
# in your main project directory. In
# our case the main directory is Test/Test.
# manage.py can compile only Python, C, C++
# and Lua source code
You can use manage.py to change project's information:
$ python manage.py change_authors "authors"
# this will change authors of the project
$ python manage.py change_description "some description"
# this will chnage description of the project
$ python manage.py change_name "Tst"
# this will change name of your project
# also this will change it's directory on Tst
$ python manage.py change_lang
# this will change language of your project
$ python manage.py update_date
# this will set creation date of your project to current
$ python manage.py change_version 1.1
# this will change current version of your project
