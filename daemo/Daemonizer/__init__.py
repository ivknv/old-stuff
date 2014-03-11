#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, signal, sys

def start_daemon(c):
	pid=os.fork()
	c=c()
	f1=open(c.pidfile_path, "w")
	f1.write(str(os.getpid()))
	f1.close()
	if pid!=0:
		time.sleep(10)
		sys.exit(0)
	c.start()
	if c.pidfile_autoremove:
		os.remove(c.pidfile_path)

def stop_daemon(c):
	c=c()
	f1=open(c.pidfile_path)
	pid=f1.read()
	f1.close()
	os.remove(c.pidfile_path)
	c.stop()
	os.kill(int(pid), signal.SIGTERM)

def restart_daemon(c):
	stop_daemon(c)
	start_daemon(c)
