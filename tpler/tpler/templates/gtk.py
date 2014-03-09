#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, sys

class Main(gtk.Window):
	def __init__(self):
		super(Main, self).__init__()
		
		self.initUI()
	
	def initUI(self):
		self.set_title("")
		self.set_size_request(640, 480)
		self.set_position(gtk.WIN_POS_CENTER)
		self.connect("destroy", gtk.main_quit)
		self.show()

if __name__ == "__main__":
	Main()
	gtk.main()
