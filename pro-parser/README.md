pro-parser
==========

A parser of projects created with pro.<br>
__ProParser is importable__.<br>
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
version: 1.1
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
1. As a command line script<br/>
2. As a Python module
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
First, run setup.py to install proParser.<br/>
Now, let's parse some project:
```
from ProParser import Project
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
print(myproject.date()) # Because myproject.date is an object
print(myproject.hour)
print(myproject.second)
print(myproject.description)
info=myproject.as_dict # Dictionary of project information.
print(info["date"]["hour"]) # Because info["date"] is dictionary
print(info["date"]["minute"])
print(info["name"])
print(info["description"])
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
