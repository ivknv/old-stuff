#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple module for writting daemons.

Includes class for creating simple daemons.
"""

import os, time, signal, sys

class DaemonError(Exception):
	pass

class Daemon(object):
	"""Daemon class"""
	
	def __init__(self, pidfile_path, pidfile_autoremove=True):
		if not os.path.exists(os.path.dirname(pidfile_path)):
			raise DaemonError(
				"Unable to create PID file: directory doesn't exist")
		
		if pidfile_autoremove is not True and pidfile_autoremove is not False:
			pidfile_autoremove = True
		
		self.pidfile_path = pidfile_path
		
		self.pidfile_autoremove = pidfile_autoremove
	
	def onStart(self):
		pass
	
	def onStop(self):
		pass
	
	def onRestart(self):
		pass
	
	def start(self):
		"""Start daemon"""
		
		pid = os.fork()
		
		try:
			f = open(self.pidfile_path, "w")
		except IOError:
			raise DaemonError("Unable to create/open PID file")
		
		f.write(str(os.getpid()))
		f.close()
		
		if pid != 0:
			sys.exit(0)
		
		self.onStart()
		
		if self.pidfile_autoremove:
			os.remove(self.pidfile_path)

	def stop(self):
		"""Stop daemon"""
		
		try:
			f = open(self.pidfile_path)
		except IOError:
			raise DaemonError("Daemon is not running or PID file doesn't exist")
		
		pid = f.read()
		f.close()
		
		if self.pidfile_autoremove:
			os.remove(self.pidfile_path)
		
		self.onStop()
		
		try:
			os.kill(int(pid), signal.SIGTERM)
		except OSError:
			raise DaemonError("Daemon is not running")
	
	def restart(self):
		"""Restart daemon"""
		
		self.stop()
		
		self.onRestart()
		
		self.start()
