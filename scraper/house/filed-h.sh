#!/bin/bash

curl -s 'http://www.legis.state.tx.us/Reports/Report.aspx?LegSess=85R&ID=housefiled' > raw-house.txt

python ../filed.py raw-house.txt house-bills.txt

python ../update.py house-bills.txt house-current.txt
