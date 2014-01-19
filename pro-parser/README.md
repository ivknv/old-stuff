pro-parser
==========

A parser for projects created by pro.<br>
__ProParser is importable__.<br>
See also [pro](https://github.com/SPython/pro)
## How to use ##
```
proParser [path-to-project]
```
or
```
proParser -e [path-to-project] [key]
```
__If you use Linux (If you do, then you go the right way)__:<br>
if you want to use ProParser the same way as in example above, rename ProParser.py to ProParser (or anything else). But if you want to use it as a Python module, then make an alias.<br>

option -e is used to print information only for following key.<br>
Output might look like this:
```
name: ProParser
language: Python
version: 1.0
authors: Ivan
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
First you need to create project using [pro](https://github.com/SPython/pro).
Let's create a project called _myproject_, it's language will be _C++_, description will be empty and author will be _Somebody_:
```
pro myproject C++ "" Somebody
```
Now we can get information about 'myproject' using proParser:
```
proParser myproject
```
