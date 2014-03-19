## Noter ##

1. [What is it?](#what-is-it)<br/>
2. [How to use](#how-to-use)<br/>
3. [Installation](#installation)<br/>

### What is it? ###
Noter - is a program that keeps all your notes in a database.<br/>

### How to use ###
```bash
noter [--init] [-a | --add -t TITLE -T TEXT] [-rm | --remove -i ID] [-e | --edit -i ID -t TITLE -T TEXT] [-l | --ls | --list] [-rs | --reverse] [-s | --slice] [-d | --db-path] [-h | --help]
```
<br/>
Option --init initializes database. Initializing database is required before doing something with notes.<br/>
Option -a adds a new note. It needs -t and -T options.<br/>
Option -t sets title.<br/>
Option -T sets text.<br/>
Option -rm removes note. It needs -i option.<br/>
Option -i set ID. You cannot change ID of note.<br/>
Option -e edits already existing note. It needs -i, -t or/and -T options.<br/>
Option -l lists all the notes.<br/>
Option -rs reverses the list of notes.<br/>
Option -s slices the list of notes.<br/>
Option -d sets path to database.<br/>
Option -h shows help message.<br/>

### Installation ###
Run setup.py:
```bash
python setup.py install
```
<br/>
Then run install.sh:
```bash
./install.sh
```
