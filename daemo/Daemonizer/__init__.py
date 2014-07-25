#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple module for writting daemons.

Includes functions for starting, stopping and restarting daemons.
"""

import os, time, signal, sys

def start_daemon(obj):
	"""Start daemon"""
	
	pid = os.fork()
	obj = obj()
	f = open(obj.pidfile_path, "w")
	f.write(str(os.getpid()))
	f.close()
	
	if pid != 0:
		sys.exit(0)
	
	if hasattr(obj, "onStart"):
		obj.onStart()
	
	if obj.pidfile_autoremove:
		os.remove(obj.pidfile_path)

def stop_daemon(obj):
	"""Stop daemon"""
	
	obj = obj()
	f = open(obj.pidfile_path)
	pid = f.read()
	f.close()
	os.remove(obj.pidfile_path)
	
	if hasattr(obj, "onStop"):
		obj.onStop()
	
	os.kill(int(pid), signal.SIGTERM)

def restart_daemon(obj):
	"""Restart daemon"""
	
	stop_daemon(obj)
	
	if hasattr(obj, "onRestart"):
		obj.onRestart()
	
	start_daemon(obj)
