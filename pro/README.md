#Description
Pro is a simple script that allows
you to create simple projects.<br>
Requires Python. 

#How to use
$ pro [project-name] [language] [description] [authors] [other-project-to-include]

project.xml - XML file that
contains information about project.<br>
manage.py - a Python script that
allows you to easily edit
project.xml.

#How to use manage.py
python manage.py [options]
<br>
Change author: python manage.py change_authors [authors]<br>
Change name of the project: python manage.py change_name [new-name]<br>
__Note__: It will also rename directory of your project<br>
Change version: python manage.py change_version [version]<br>
Change programming language: python manage.py change_lang [language]<br>
Change description: python manage.py change_description [new-description]<br>
Update date of creation: python manage.py update_date<br>
Compile source code: python manage.py compile<br>
__Note__: At the moment manage.py can compile only Python, C, C++ and Lua source code. Soon there will be more supported languages.<br>
#Structure of the project
Simple Python project: <br>
project-name/<br>
&nbsp;&nbsp;&nbsp;&nbsp;bin/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;... -  compiled source code<br>
&nbsp;&nbsp;&nbsp;&nbsp;doc/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;doc.xhtml  -  documentation<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;style.css  - stylesheet for documentation<br>
&nbsp;&nbsp;&nbsp;&nbsp;manage/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...  -  modules for manage.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;project_name/  -  main directory<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...  -  source code<br>
&nbsp;&nbsp;&nbsp;&nbsp;manage.py  -  manage.py script<br>
&nbsp;&nbsp;&nbsp;&nbsp;project.xml  -  information about project<br>

#Examples

Create a Python project named Test with description: "A simple project" and author: Somebody<br>
$ pro Test Python "A simple project" Somebody

#How to install

Just directory with script to your PATH
