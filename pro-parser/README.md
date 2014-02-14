pro-parser
==========

A parser of projects created with pro.<br>
See also [pro](https://github.com/SPython/pro)
## How to use ##
```
pro-parser [path-to-project]
```
or
```
pro-parser -e [path-to-project] [key]
```

option -e is used to print information only for following key.<br>
Output might look like this:
```
name: ProParser
language: Python
version: 1.2
authors: Ivan Konovalov
hour: 21
month: 1
second: 38
weekday: Saturday
year: 2014
day: 18
minute: 14
description: This script allows to get information about project (if it was created with pro).
```

## Examples ##
There are two ways to use pro-parser:<br/>
1. [As a command line script](#command-line-script)<br/>
2. [As a Python module](#python-module)
### Command line script ###
First you need to create a project using [pro](https://github.com/SPython/pro).
Let's create a project called _myproject_, its language will be _C++_, description will be empty and author will be _Somebody_:
```
pro myproject C++ "" Somebody
```
Now we can get information about 'myproject' using proParser:
```
pro-parser myproject
```
### Python module ###
First, run setup.py to install ProParser.<br/>
Now, let's parse some project:
```
from ProParser import *
myproject=Project("myproject")
```
To see what you can do with 'Project' object use dir:
```
dir(myproject)
```
We can print its name, authors, version, date, description and more:
```
print(myproject.name)
print(myproject.authors)
print(myproject.date()) # Because myproject.date is a class
print(myproject.hour)
print(myproject.second)
print(myproject.description)
info=myproject.as_dict # Dictionary of project information.
print(info["date"]["hour"]) # Because info["date"] is dictionary
print(info["date"]["minute"])
print(info["name"])
print(info["description"])
# without Project class
print(getName("myproject"))
print(getLang("myproject"))
print(getDate("myproject")) # getDate is a class
print(getDate("myproject").hour)
print(getDate("myproject").day)
print(getAuthors("myproject"))
print(getDescription("myproject"))
# and of course you can check if it's a project
if isProject("myproject"):
	print("myproject is a project")
else:
	print("myproject is not a project")
```

With ProParser you can do even more. For example, you can find projects in some directory:
```
projects=ProParser.listProjects(".") # it will return a list of projects in current directory
for project in projects:
	print(project.name)

projects_dict=ProParser.listProjectsAsDict(".") # it will return a dictionary of projects in current directory
print(projects_dict["projectName"]["authors"])

all_projects=ProParser.listAllProjects("/home/ivan") # list all the projects recuresively
for project in all_projects:
	print(project.name)
all_projects_dict=ProParser.listAllProjectsAsDict("/home/ivan") # almost like listAllProjects, but returns dictionary
print(all_projects_dict["projectName"]["language"])
```



## Installation ##
### As a Python module ###
```
python setup.py install
```
### As a command line script  ###
```
./install.sh [script-name] [installation-dir]
```
By default it will install script as /usr/local/bin/pro-parser
