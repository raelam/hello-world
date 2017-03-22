#!/usr/bin/python
import subprocess                 # For issuing commands to the OS.
import os
import locale
import sys                        # For determining the Python version.
import re
import time
import numpy as np

def get_nfiled(fname):
	filer=open(fname,'r')
	i = 0
	for atom in filer:
		if re.search('Number of Bills: (\d+\d+)', atom):
			head=re.search('Number of Bills: (\d+\d+)', atom)
			i = locale.atoi(head.group(1))
	return i

def get_nB(fname):
	filer=open(fname,'r')
	SYS1=[]
	SYS2=[]
	SYS3=[]
	for atom in filer:
		if re.search('^(\d+) \t(\w\w\w?).+(http.+)',atom):
			head=re.search('^(\d+) \t(\w\w\w?).+(http.+)',atom)
			SYS1.append(head.group(1))
			SYS2.append(head.group(2))
			SYS3.append(head.group(3))
	return SYS1,SYS2,SYS3

def get_auth(fname):
	filer=open(fname,'r')
	SYS=[]
	SYS.append('none')
	for atom in filer:
		if re.search('Author:.+>(.+)</',atom):
			head=re.search('Author:.+>(.+)</',atom)
			SYS[0]= head.group(1).replace(',', '').replace(' |', ',')
	return SYS

def get_caption(fname):
	filer=open(fname,'r')
	SYS=[]
	SYS.append('no caption')
	for atom in filer:
		if re.search('Caption Text:.+>(.+)</td>',atom):
			head=re.search('Caption Text:.+>(.+)</td>',atom)
			SYS[0]=head.group(1).replace(',','')
	return SYS

def get_action(fname):
	filer=open(fname,'r')
	SYS=[]
	MSYS=[]
	KSYS=[]
	for atom in filer:
		if re.search('Last Action:.+<i>(\d+\D\d+\D201\d)\s(\w)\s(.+)</i>',atom):
			head=re.search('Last Action:.+<i>(\d+\D\d+\D201\d)\s(\w)\s(.+)</i>',atom)
			SYS.append(head.group(1))
			MSYS.append(head.group(2).replace('H','House').replace('S','Senate'))
			KSYS.append(head.group(3).replace(',', ''))
	return SYS, MSYS, KSYS

def get_subjects(fname):
	filer=open(fname,'r')
	SYS=[]
	SYS.append('none')
	for atom in filer:
		if re.search('Subjects:.+cellSubjects">(.+)<br/>',atom):
			head=re.search('Subjects:.+cellSubjects">(.+)<br/>',atom)
			SYS[0]=head.group(1).replace(',','').replace('<br/>',',')
	return SYS

def get_Housecomm(fname):
	filer=open(fname,'r')
	SYS=[]
	SYS.append('unassigned')
	for atom in filer:
		if re.search('House Committee:.+>(.+)</a>',atom):
			head=re.search('House Committee:.+>(.+)</a>',atom)
			SYS[0]=head.group(1).replace(',','')
	return SYS

def get_Senatecomm(fname):
	filer=open(fname,'r')
	SYS=[]
	SYS.append('unassigned')
	for atom in filer:
		if re.search('Senate Committee:.+>(.+)</a>',atom):
			head=re.search('Senate Committee:.+>(.+)</a>',atom)
			SYS[0]=head.group(1).replace(',','')
	return SYS

def get_companions(fname):
	filer=open(fname,'r')
	SYS=[]
	SYS.append('none')
	i=0
	for atom in filer:
		if re.search('<a href="History.aspx.LegSess.+>(.+)</a>',atom):
			SYS.append('filler')
			head=re.search('<a href="History.aspx.LegSess.+>(.+)</a>',atom)
			SYS[i]=head.group(1)
			i = i + 1
	return SYS

name1 = sys.argv[1]
length = get_nfiled(name1)
nB, nType, nURL = get_nB(name1)
nCap=[]
nAuth=[]
nDate=[]
nC=[]
nDesc = []
nSub = []

out1 = sys.argv[2]
fout = open(out1,'w')
i = 0
for num in range(0,length):
	curlCom = "curl -s -retry 2 '%s' > dummy1.txt" % (nURL[num])
	subprocess.call(curlCom, shell=True)
	nCap.append(get_caption('dummy1.txt')[0])
	nAuth.append(get_auth('dummy1.txt')[0])
	nDate, nC, nDesc = get_action('dummy1.txt')
	nSCom = get_Senatecomm('dummy1.txt')
	nHCom = get_Housecomm('dummy1.txt')
	nSub = get_subjects('dummy1.txt')
	URL2 = "http://www.legis.state.tx.us/BillLookup/Companions.aspx?LegSess=85R&Bill="+nType[num]+nB[num]
	curlCom = "curl -s -retry 2 '%s' > dummy2.txt" % (URL2)
	subprocess.call(curlCom, shell=True)
	nComp = get_companions('dummy2.txt')
	print >> fout, nType[num],int(nB[num]),'\t',nType[num],'\t',nAuth[num],'\t',nCap[num],'\t',nSub,'\t',nDate[0],'\t',nDesc[0],'\t',nC[0],'\t',nSCom[0],'\t',nHCom[0],'\t',nURL[num],'\t',nComp
	i = i + 1
	if i == 225:
		time.sleep(20)
		i = 0

