#!/usr/bin/python3
# -*- coding: utf-8 -*-
def dinge(prices):
    t=0.0
    for price in prices:
      t=t+1/price
    return len(prices)/t

def dingliang(prices):
    t=0.0
    for price in prices:
      t=t+price
    return t/len(prices)


fo = open("000002.csv")
lista=[]
for line in fo.readlines():
 list=line.strip().split(',')
 lista.append("'%s',%s,%s,%s,%s," % (list[0],list[4],list[1],list[3],list[2]))
lista.reverse()
dates='['
prices=[]
c=[]
for l in lista:
  list=l.split(',')
  dates=dates+list[0]+','
  prices.append(float(list[1]))
  c.append(dinge(prices)/dingliang(prices))
print(dates+']')
print(c)
fo.close()
