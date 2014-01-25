#!/usr/bin/python
# -*- coding: utf-8

import sys
from PySide import QtGui

class Main(QtGui.QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		
		self.initUI()
	def initUI(self):
		self.setGeometry(300, 300, 640, 480)
		self.setWindowTitle("")
		self.show()

def main():
	app = QtGui.QApplication(sys.argv)
	M=Main()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()