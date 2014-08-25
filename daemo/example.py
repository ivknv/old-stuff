#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example daemon created by using Daemo.

It writes message with countdown to ~/testdaemon.
After 30 seconds it shuts down and removes ~/testdaemon.

To start daemon run
  $ python example.py start

To stop daemon:
  $ python example.py stop

And to restart daemon run
  $ python example.py restart
"""

import os, time

from Daemo import Daemon, DaemonError

class TestDaemon(Daemon):
	"""Example daemon created with Daemo"""
	
	def __init__(self):
		"""Daemon initialization function"""
		
		# Path to PID file
		pidfile_path = os.path.expanduser("~/testdaemon.pid")
		
		# Call Daemon initialization function
		super(TestDaemon, self).__init__(pidfile_path)
	
	def onStart(self):
		"""This function is being called when daemon starts"""
		
		if __name__ == "__main__":
			print("Go check %s" %os.path.expanduser("~/testdaemon"))
		
		for i in range(30):
			time.sleep(1)
			j = 30-i
			f = open(os.path.expanduser("~/testdaemon"), "w")
			f.write("""Daemon is working
This file will be removed after %d seconds\n""" %j)
			f.close()
	
	def onStop(self):
		"""This function is being called when daemon stops"""
		
		os.remove(os.path.expanduser("~/testdaemon"))
	
	def onRestart(self):
		"""This function is being called when daemon restarts."""
		
		pass

if __name__ == "__main__":
	import sys
	
	daemon = TestDaemon() # Initialize daemon
	
	try:
		if len(sys.argv) == 1:
			print("%s start|stop|restart" %sys.argv[0]) # Show usage
		else:
			command = sys.argv[1].lower()
			
			if command == "start":
				daemon.start() # Start daemon
			elif command == "stop":
				daemon.stop() # Stop daemon
			elif command == "restart":
				daemon.restart() # Restart daemon
			else:
				print("%s start|stop|restart" %sys.argv[0]) # Show usage
	except DaemonError as error:
		print(error)
		sys.exit(1)
