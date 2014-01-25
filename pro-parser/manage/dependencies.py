# -*- coding: utf-8 -*-

import os

def add(project, dependency):
	full_path=os.path.realpath(project)
	ds=full_path+"/dependencies"
	if os.path.exists(ds):
		d=open(ds, "r")
		dr=d.read()
		d.close()
		d=open(ds, "w+")
	else:
		d=open(ds, "w+")
	d.write(dr+dependency+"\n")
	d.close()
def remove(project, dependency):
	full_path=os.path.realpath(project)
	ds=full_path+"/dependencies"
	if os.path.exists(ds):
		d=open(ds, "r")
		dr=d.read()
		d.close()
		d=open(ds, "w+")
	else:
		print (ds+" does not exists.")
		exit(1)
	d.write(dr.replace(dependency+"\n", ""))
	d.close()

