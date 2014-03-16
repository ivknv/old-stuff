## CodeCommenter ##
1. [What is it?] (#what-is-it)<br/>
2. [How to use] (#how-to-use)<br/>
3. [Installation] (#installation)<br/>

### What is it? ###
CodeCommenter is a tool for automatic code commenting.<br/>
It uses XML to keep patterns, texts, variables and other settings.

### How to use ###
```bash
ccommenter file [-p PATH] [-f] [-h] [-rm] [-cs] [-ce]
```
<br/>
Option -p sets path to file with patterns.<br/>
Option -f sets file type.<br/>
Option -rm removes all the comments, it needs also -cs and -ce options.<br/>
Option -cs sets beginning of a comment. __Warning__: it's a regular expression.<br/>
Option -ce sets ending of a comment. __Warning__: it's a regular expression too.<br/>
Option -h shows help message.<br/><br/>

Before using ccommenter you have to set up XML file that will contain patterns.<br/>
You can see example in examples directory.<br/>
&lt;comment filetype="extension" commentStart="" commentEnd=""&gt; - main comment tag. filetype attribute sets extension. Comment will be used only if file extension==filetype. commentStart - with what begins comment, commentEnd - comment end. You can leave commentEnd empty.<br/>
   &lt;pattern&gt; - pattern. Uses regular expression.<br/>
   &lt;text&gt; - comment text.<br/>
   &lt;variable name="name" type="type" index="0"&gt; - declare a variable. It can be used by appending and prepending %. Example: test comment number %number%. Type can be regex or overything else.
   &lt;position&gt; - sets position of a comment. Default position is top. Available positions are: top, right, bottom, left.<br/>

### Installation ###
First you have to run setup.py
```bash
python setup.py install
```
And then install.sh
```bash
./install.sh
```
