## Description ##
Pro - is a script that allows
you to create projects.<br>
Requires Python. 

## How to use ##

You can use pro as a command line script or a Python module.<br/>
As a Python module:
```
from pro import pro
pro(project-name, language, description, authors, other_project_to_include)
```
As a command line script:
```
pro project-name language "description" "authors" [-r directories-to-include]
```

project.xml - XML file that
contains information about project.<br>
manage.py - a Python script that
allows you to easily edit
project.xml.<br>
config.py - a configuration file. Contains compilation commands.

## How to use manage.py ##
```
python manage.py [options]
```
<br>
Change author: python manage.py change_authors [authors]<br>
Change name of the project: python manage.py rename [new-name]<br>
Change version: python manage.py change_version [version]<br>
Change programming language: python manage.py change_lang [language]<br>
Change description: python manage.py change_description [new-description]<br>
Update date of creation: python manage.py update_date<br>
Compile source code: python manage.py compile<br>
__Note__: At the moment manage.py can compile only Python, C, C++, Lua and Java source code. Soon there will be more supported languages.<br>
Add dependency: python manage.py dependencies add [library-or-framework]<br>
Remove dependency: python manage.py dependencies rm [library-or-framework]<br>
# Project structure #
Python project: <br>
```
project-name/
	bin/
		... -  compiled source code
	doc/
		doc.xhtml  -  documentation
		style.css  - stylesheet for documentation
	project-name/ - main project directory
		...  -  source code files
	config.py - this file contains compiler configuration
	dependencies - this file contains required libraries and frameworks
	manage.py  -  manage.py script
	project.xml  -  information about project
```

C++ project: <br>
```
project-name/
	bin/
		... - compiled source code
	doc/
		doc.xhtml - documentation
		style.css - stylesheet for documentation
	src/ - source code directory
		project-name/ - main project directory
			... - source code files
	config.py - this file contains compiler configuration
	dependencies - this file contains required libraries and frameworks
	manage.py  -  manage.py script
	project.xml  -  information about project
```

## Examples ##

Create a Python project named 'Test' with description: 'A simple project' and author: 'Somebody'<br>
```
from pro import pro
pro("Test", "Python", "A simple project", "Somebody")
```
Create a C++ project named 'Test' with description: 'A simple project' and author: 'Somebody'<br>
```
from pro import pro
pro("Test", "C++", "A simple project", "Somebody")
```

## How to install ##

### As a Python module ###
```
python setup.py install
```

### As a command line script ###
```
./install.sh [script-name] [installation-path]
```
By default it will install script as /usr/local/bin/pro
