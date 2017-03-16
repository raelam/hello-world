#!/bin/bash

curl -s 'http://www.legis.state.tx.us/Reports/Report.aspx?LegSess=85R&ID=senatefiled' > raw-senate.txt

python ../filed.py raw-senate.txt senate-bills.txt

python ../update.py senate-bills.txt senate-current.txt
