import sys, os, py_compile

try:
	directory=sys.argv[1]
except IndexError:
	directory="."

py_files = os.listdir(directory)
for py_file in py_files:
	if py_file.endswith(".py"):
		py_compile.compile(py_file)