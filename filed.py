#!/usr/bin/python
import subprocess                 # For issuing commands to the OS.
import os
import locale
import sys                        # For determining the Python version.
import re
import numpy as np

def get_nfiled(fname):
	filer=open(fname,'r')
	i = 0
	for atom in filer:
		if re.search('Number of Bills: (\d+\,\d+)', atom):
			head=re.search('Number of Bills: (\d+\,\d+)', atom)
			i = locale.atoi(head.group(1).replace(',', ''))
	return i

def get_nB(fname,bills):
	filer=open(fname,'r')
	SYS=np.zeros(bills)
	MSYS=[]
	i = 0
	for atom in filer:
		if re.search('"_blank">(\w+) (\d+)\s+',atom):
			head=re.search('"_blank">(\w+) (\d+)\s+',atom)
			MSYS.append(head.group(1))
			SYS[i]=locale.atoi(head.group(2))
			i = i + 1
	return MSYS, SYS

def get_auth(fname,bills):
	filer=open(fname,'r')
	SYS=[]
	i = 0
	for atom in filer:
		if re.search('Author',atom):
			i = 1
		if re.search('"77%">(\D+)</td',atom) and i==1:
			head=re.search('"77%">(\D+)</td',atom)
			SYS.append(head.group(1).replace(',', '').replace(' |', ','))
			i = 0
	return SYS

def get_caption(fname,bills):
	filer=open(fname,'r')
	SYS=[]
	i = 0
	for atom in filer:
		if re.search('Caption',atom):
			i = 1
		if re.search('"top">(.+)<br><br>',atom) and i==1:
			head=re.search('"top">(.+)<br><br>',atom)
			SYS.append(head.group(1))
			i = 0
	return SYS

def get_action(fname,bills):
	filer=open(fname,'r')
	SYS=[]
	MSYS=[]
	KSYS=[]
	i = 0
	for atom in filer:
		if re.search('Last Action',atom):
			i = 1
		if re.search('"77%">(\d+\D\d+\D201\d)\s(\w)\s(.+)</td>',atom) and i==1:
			head=re.search('"77%">(\d+\D\d+\D201\d)\s(\w)\s(.+)</td>',atom)
			SYS.append(head.group(1))
			MSYS.append(head.group(2))
			KSYS.append(head.group(3))
			i = 0
	return SYS, MSYS, KSYS

def get_URL(fname,bills):
	filer=open(fname,'r')
	SYS=[]
	for atom in filer:
		if re.search('href="(.*)" target',atom):
			head=re.search('href="(.*)" target',atom)
			SYS.append(head.group(1).replace('amp;',''))
	return SYS

name1 = sys.argv[1]
length = get_nfiled(name1)
nType, nB = get_nB(name1, length)
nAuth = get_auth(name1,length)
nCap = get_caption(name1,length)
nDate, nC, nDesc = get_action(name1,length)
nURL = get_URL(name1,length)

out1 = sys.argv[2]
fout = open(out1,'w')
print >> fout, 'Number of Bills:',length
for i in range(0,length):
	print >> fout, int(nB[i]),'\t', nType[i],'\t', nAuth[i],'\t', nCap[i],'\t', nDate[i],'\t', nC[i],'\t', nDesc[i],'\t', nURL[i]
	
