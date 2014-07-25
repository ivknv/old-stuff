#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Daemonizer as d, os, time

class Daemon(object):
	def __init__(self):
		self.pidfile_path = os.path.expanduser("~/testdaemon.pid")
		self.pidfile_autoremove = True
	def onStart(self):
		for i in range(30):
			time.sleep(1)
			ii=30-i
			f1=open(os.path.expanduser("~/testdaemon"), "w")
			f1.write("Daemon is working\nThis file will be removed after %d seconds\n" %ii)
			f1.close()
		self.stop()
	def onStop(self):
		os.remove(os.path.expanduser("~/testdaemon"))

if __name__ == "__main__":
	import sys
	if len(sys.argv) == 1:
		print("%s start|stop|restart" %sys.argv[0])
	elif sys.argv[1].lower() == "start":
		d.start_daemon(Daemon)
	elif sys.argv[1].lower() == "stop":
		d.stop_daemon(Daemon)
	elif sys.argv[1].lower() == "restart":
		d.restart_daemon(Daemon)
	else:
		print("%s start|stop|restart" %sys.argv[0])
