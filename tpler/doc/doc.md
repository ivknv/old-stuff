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
tpler will automatically recognize file type and write apropriate code.
</p>
<h3 id="how-to-use"><a style="text-decoration: none; color: black;" href="#how-to-use">How to use</a></h3>
Create a generic HTML file:<br/>
```tpler html_file.html```

It will write following text to 'html_file.html':
```
<!DOCTYPE html>
<html>
head>
<meta charset="utf-8">
<title></title>
</head>
<body>
</body>
</html>
```
<br/>
Tpler can create even more useful templates:<br/>
```
tpler html_file_with_jquery.html jquery
```
Now 'html_file_with_jquery.html' look like this:<br/>
```
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
```tpler html_angular.html angular```
Or jQueryUI<br/><br/>
You use tpler with other source code files:<br/>
```
tpler main.py main
tpler file.cpp
tpler xmlfile.xml
tpler xhtml_file.xhtml
tpler factorial.clj factorial
tpler ncurses_program.c ncurses
tpler java_program.java
```
You can do similiar things with other source code files.<br/>
<ul>
Supported are
<li>.c</li>
	<ul>
	<li>ncurses</li>
	<li>fibonacci</li>
	<li>factorial</li>
	<li>empty (only main function)</li></ul>
<li>.cpp</li>
	<ul><li>empty (only main function)</li></ul>
<li>.html or .htm with options</li>
	<ul><li>jquery</li>
	<li>jqueryui</li>
	<li>angular</li>
	<li>base (django template) </li>
	</ul>
<li>.py</li>
	<ul><li>main</li>
	<li>pyside</li>
	<li>fibonacci</li>
	<li>curses</li>
	<li>factorial</li>
	</ul>
<li>.xhtml</li>
<li>.xml</li>
	<ul><li>project</li></ul>
<li>.xsd</li>
<li>.xsl</li>
<li>.svg</li>
<li>.php</li>
<li>.css</li>
	<ul><li>button</li></ul>
<li>.java</li>
</ul>
And also every data type supports <i>random type selection</i>. Just type "random", "rand" or "rnd" as a second argument:<br/><br/>
```tpler code.py random```
</p>
<h3 id="adding-custom-templates"><a style="text-decoration: none; color: black;" href="#adding-custom-templates">Adding custom templates</a></h3>
<p>
If you want to add some new template you can use <b>add_template.py</b> script.
To delete templates use <b>rm_template.py</b>.<br/>
add_template.py usage:<br/><br/>
<code>python add_template.py <filename></code>
<br/><br/>
With add_template.py you can also make an alias to your template:<br/><br/>
<code>python add_template.py <filename> <alias1> <alias2> <alias3> <aliasn></code>
<br/><br/>
rm_template.py usage:<br/><br/>
<code>python rm_template.py <template_name></code>
</p>
<h3 id="add_template-and-rm_template-examples"><a style="text-decoration: none; color: black;" href="#add_template-and-rm_template-examples">add_template.py and rm_template.py examples</a></h3>
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
Also, we want to make an alias to config.py.
And if want to use tpler like this:<br/><br/>
<code>
python tpler.py mysetup.py stp
</code>
<br/><br/>
then we need to add template and make an alias:<br/><br/>
<code>
python add_template.py setup.py stp
</code>
<br/><br/>
<b>Note:</b> if you have problems with adding/removing templates, make sure you're running script as root.<br/><br/>
Now we can use this template:<br/><br/>
<code>tpler mysetup.py stp</code>
<br/><br/>or<br/><br/>
<code>tpler mysetup.py setup</code>
<br/><br/>
If we want to remove this template and all its aliases we just need to run<br/><br/>
<code>python rm_template.py setup.py</code>
<br/><br/>
add_template.py and rm_template.py can be found in <b>tpler</b> directory.
<br/><br/>
</p>
<h3 id="installation"><a style="text-decoration: none; color: black;" href="#installation">Installing as a command line script</a></h3>
<p>
To install this script, all you need is to run <i>install.sh</i>:<br/><br/>
<code>./install.sh</code>
<br/><br/>
</p>
