#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, os

def sortByPriority(inp):
	return (inp[2], inp[1], inp[3])

def Calculate(money, currency="", csvpath="~/.finances"):
	csvf=open(os.path.expanduser(csvpath), "rt")
	csvreader=csv.reader(csvf)
	csvarr=[]
	i=0
	for row in csvreader:
		csvarr.append([row[0]])
		csvarr[i].append(float(row[1]))
		csvarr[i].append(float(row[2]))
		csvarr[i].append(float(row[3]))
		i+=1
	csvf.close()
	items=sorted(csvarr, key=sortByPriority)
	items.reverse()
	money_2=money
	bought=[]
	i=0
	amount=0
	while money_2 >= items[-1][1]:
		if money_2 < items[i][1] or amount >= items[i][3]:
			i+=1
			if i >= len(items):
				break
			amount=0
		if money_2 >= items[i][1]:
			if amount < items[i][3]:
				money_2-=items[i][1]
				bought.append(items[i][0])
				amount+=1
	class Check(object):
		def __init__(self, groceries, money, currency=""):
			self.groceries = {}
			self.currency = currency
			self.money = money
			for grocerie in groceries:
				if not grocerie[0] in self.groceries:
					self.groceries.setdefault(grocerie[0], {"price": grocerie[1], "amount": grocerie[3], "priority": grocerie[2], "totalprice": grocerie[3]*grocerie[1]})
			self.remains = money
			for grocerie in self.groceries:
				self.remains-=self.groceries[grocerie]["price"]
		def __call__(self, grocerie, key=None):
			if isinstance(key, str):
				return self.groceries[grocerie][key]
			else:
				grocerie_={}
				for i in self.groceries[grocerie]:
					grocerie_.setdefault(i, self.groceries[grocerie][i])
				return grocerie_
#	print("You can buy:")
	i=0
	groceries=[]
	for item in range(len(items)):
		count=bought.count(items[item][0])
		if count > 0:
			groceries.append(items[item])
			groceries[i].append(items[item][0])
			groceries[i].append(items[item][1])
			groceries[i].append(items[item][2])
			groceries[i].append(items[item][3])
			i+=1
			#print("%d %s(s) for %f %s(s): %f %s(s)" %(count, items[item][0], items[item][1], currency, items[item][1]*count, currency))
	#print("And now we have %f %s" %(money_2, currency+"(s)"))
	return Check(groceries, money, currency)

if __name__ == "__main__":
	import sys
	if len(sys.argv) == 2:
		check=Calculate(float(sys.argv[1]))
	elif len(sys.argv) == 3:
		check=Calculate(float(sys.argv[1]), sys.argv[2])
	elif len(sys.argv) > 3:
		check=Calculate(float(sys.argv[1]), sys.argv[2], sys.argv[3])
	else:
		print("usage: financer <money_amount> <currency> <csvfilepath>")
		exit(1)
	print("You can buy:")
	for grocerie in check.groceries:
		print("%d \033[1m%s\033[0m(s) for %f %s: total sum is %f %s" %(check.groceries[grocerie]["amount"], grocerie, check.groceries[grocerie]["price"], check.currency, check.groceries[grocerie]["price"]*check.groceries[grocerie]["amount"], check.currency))
print("Remaining money: %f %s" %(check.remains, check.currency))
print("You spent %f %s" %(float(sys.argv[1])-check.remains, check.currency))
