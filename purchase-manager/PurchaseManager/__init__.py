#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, os

def sortByPriority(inp):
	return (inp[2], inp[1], inp[3])

class Check(object):
		def __init__(self, purchases, money):
			self.purchases = {}
			self.money = money
			for purchase in purchases:
				if not purchase[0] in self.purchases:
					self.purchases.setdefault(purchase[0], {"price": purchase[1], "amount": purchase[3], "priority": purchase[2], "totalprice": purchase[3]*purchase[1]})
			self.remains = money
			for purchase in self.purchases:
				self.remains-=self.purchases[purchase]["price"]
		def __call__(self, purchase, key=None):
			if isinstance(key, str):
				return self.purchases[purchase][key]
			else:
				purchase_={}
				for i in self.purchase[purchase]:
					purchase_.setdefault(i, self.purchase[purchase][i])
				return purchase_

def Calculate(money, csvpath="~/.items"):
	csvf=open(os.path.expanduser(csvpath), "rt")
	csvreader=csv.reader(csvf) # Parse CSV file
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
	i=0
	purchases=[]
	for item in range(len(items)):
		count=bought.count(items[item][0])
		if count > 0:
			purchases.append(items[item])
			purchases[i].append(items[item][0])
			purchases[i].append(items[item][1])
			purchases[i].append(items[item][2])
			purchases[i].append(items[item][3])
			i+=1
	return Check(purchases, money)
