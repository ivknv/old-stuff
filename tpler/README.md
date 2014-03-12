<h1 id="tpler"><a style="text-decoration: none; color: black;" href="#tpler">tpler</a></h1>
<h3 id="contents"><a href="#contents">Contents</a></h3>
<p>
1. <a href="#description">Description</a><br/>
2. <a href="#how-to-use">How to use</a><br/>
3. <a href="#adding-custom-templates">Adding custom templates</a><br/>
4. <a href="#add_templatepy-and-rm_templatepy-examples">add_template.py and rm_template.py examples</a><br/>
5. <a href="#installing-as-a-command-line-script">Installation</a>
</p>
<h3 id="description"><a style="text-decoration: none; color: black;" href="#description">Description</a></h3>
<p>
tpler is a <b>t</b>em<b>pl</b>at<b>er</b>. It allows you to <b style="text-decoration: underline;">stop</b> always <b style="text-decoration: underline;">writting the same code</b>.<br/>
tpler will automatically recognize file type and write apropriate code (you can manually set file type with -f option. See tpler -h ).
</p>
<h3 id="how-to-use"><a style="text-decoration: none; color: black;" href="#how-to-use">How to use</a></h3>
Create a generic HTML file:<br/>
```bash
tpler -i html_file.html
```

It will write following text to 'html_file.html':
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title></title>
</head>
<body>
</body>
</html>
```
<br/>
Tpler can create even more useful templates:<br/>
```bash
tpler -i html_file_with_jquery.html -t jquery
```
Now 'html_file_with_jquery.html' look like this:<br/>
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title></title>
<script type="text/javascript" src="http://code.jquery.com/jquery-latest.min.js">
</script>
</head>
<body>
</body>
<html>
```
<br/>
Or you can include AngularJS:<br/><br/>
```bash
tpler -i html_angular.html -t angular
```
Or jQueryUI<br/><br/>
You can use tpler with other source code files:<br/>
```bash
tpler -i main.py -t main
tpler -i file.cpp
tpler -i xmlfile.xml
tpler -i xhtml_file.xhtml
tpler -i factorial.clj -t factorial
tpler -i ncurses_program.c -t ncurses
tpler -i java_program.java
```
<br/>
All supported file types and templates:
<ul>
<li>.c</li>
	<ul>
	<li>default</li>
	<li>ncurses</li>
	<li>gtk</li>
	<li>fibonacci</li>
	<li>factorial</li>
	<li>empty (only main function)</li></ul>
<li>.cpp</li>
	<ul>
	<li>default</li>
	<li>empty (only main function)</li>
	<li>qapplication</li>
	</ul>
<li>.html or .htm</li>
	<ul>
	<li>default</li>
	<li>jquery</li>
	<li>jqueryui</li>
	<li>angular</li>
	<li>base (django template) </li>
	</ul>
<li>.py</li>
	<ul>
	<li>default</li>
	<li>main</li>
	<li>pyside</li>
	<li>pyqt</li>
	<li>gtk</li>
	<li>setuptools_setup</li>
	<li>distutils_setup</li>
	<li>fibonacci</li>
	<li>curses</li>
	<li>factorial</li>
	</ul>
<li>.js</li>
        <ul><li>jquery</li></ul>
<li>.xhtml</li>
	<ul><li>default</li></ul>
<li>.xml</li>
	<ul>
	<li>default</li>
	<li>project</li>
	<li>strings</li>
	<li>android-linear-layout</li>
	<li>androidmanifest</li>
	</ul>
<li>.xsd</li>
	<ul><li>default</li></ul>
<li>.xsl</li>
	<ul><li>default</li></ul>
<li>.svg</li>
	<ul><li>default</li></ul>
<li>.php</li>
	<ul><li>default</li></ul>
<li>.css</li>
	<ul><li>button</li></ul>
<li>.java</li>
	<ul>
	<li>default</li>
	<li>android-activity</li>
	</ul>
<li>.wsgi</li>
	<ul><li>django</li></ul>
<li>.clj</li>
	<ul><li>factorial</li>
	<li>fibonacci</li></ul>
</ul>
And also every file type supports <i>random template selection</i>. Just type "random", "rand" or "rnd" as a second argument:<br/><br/>
```bash
tpler -i code.py -t random
```
<br/><br/>
You can list all available templates with <code>tpler -l</code>.<br/><br/>
</p>
<h3 id="adding-custom-templates"><a style="text-decoration: none; color: black;" href="#adding-custom-templates">Adding custom templates</a></h3>
<p>
If you want to add some new template you can use <b>add_template.py</b> script.
To delete templates use <b>rm_template.py</b>.<br/>
add_template.py usage:<br/><br/>
<pre>
<code>python add_template.py [-h] [-v] [-f filename] [-a alias]</code></pre>
<br/><br/>
rm_template.py usage:<br/>
<pre>
<code>python rm_template.py [-h] template_name [-a] [-v]</code></pre>
</p>
<h3 id="add_templatepy-and-rm_templatepy-examples"><a style="text-decoration: none; color: black;" href="#add_templatepy-and-rm_templatepy-examples">add_template.py and rm_template.py examples</a></h3>
<p>
Let's say we want to add a new template called <i>setup.py</i>.<br/>
Our <i>setup.py</i> will contain this code:<br/><br/>
<pre><code>from distutils.core import setup

setup(name="",
description="",
version="1.0",
author="",
author_email="",
packages=[])
</code></pre>
Also, we want to make an alias to setup.py.
And if want to use tpler like this:<br/><br/>
<code>
tpler -i mysetup.py -t stp
</code>
<br/>
or<br/>
<code>
tpler -i mysetup.py -t dsetup
</code><br/>
we need to run the following command:<br/>
<code>add_template.py -f setup.py -a stp dsetup</code>
<br/>
<b>Note:</b> if you have problems with adding/removing templates, make sure you're running script as root.<br/><br/>
Now we can use this template:<br/><br/>
<code>tpler -i mysetup.py -t stp</code>
<br/>or<br/>
<code>tpler -i mysetup.py -t setup</code>
<br/><br/>
or<br/><br/>
<code>tpler -i mysetup.py -t dsetup</code><br/>
If you want to remove some of aliases, you can run<br/>
<code>rm_template.py stp.py dsetup.py</code>
<br/><br/>
Every alias is just a symlink to original template, so if you remove original template (in this case setup.py), all aliases will disapear.</br><br/>
<code>rm_template setup.py</code><br/>
This command will completely remove setup.py and all it's aliases (stp.py, dsetup.py).<br/>
If you want to completely remove template and all it's aliases but don't know which template is real, you can use rm_template with option -a:<br/>
<code>rm_template.py dsetup.py -a</code><br/>
This will remove setup.py, dsetup.py and stp.py.<br/><br/>
add_template.py and rm_template.py can be found in <b>tpler</b> directory.
<br/><br/>
</p>
<h3 id="installation"><a style="text-decoration: none; color: black;" href="#installing-as-a-command-line-script">Installing as a command line script</a></h3>
<p>
To install this script, you need to run <i>setup.py</i> and then <i>install.sh</i>:<br/><br/>
<pre><code>python setup.py install
./install.sh
</code></pre>
<br/><br/>
</p>
