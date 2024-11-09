#!/usr/bin/env python3

import sqlite3
import json
#Vulnerability - SQL Injection 
from urllib.parse import unquote

FILENAME = 'rtbb.sqlite3'
SQL_ELECTIONS = "SELECT * FROM Election"
SQL_OFFICES = "SELECT * FROM Office"
SQL_ZIPS = "SELECT * FROM AllowedZip WHERE office="
SQL_CANDIDATES = "SELECT * FROM Candidate WHERE office="

#Vulnerability - SQL Injection 
conn = sqlite3.connect(FILENAME)
c = conn.cursor()
# Original
# c = sqlite3.connect(FILENAME)

elections = {}
dates = {}

for row in c.execute(SQL_ELECTIONS):
    date = "{}-{:02d}-{:02d}".format(row[3] + 1900, row[2], row[1])
    dates[row[0]] = date
    status = 'closed'
    if row[4] == 1:
        status = 'open'
    elif row[4] == 2:
        status = 'published'
    elections[date] = {
        "offices": [],
        "status": status
    }

# NEW START --------------------------------
for row in c.execute(SQL_OFFICES):
    if row[2] not in dates:
        continue 

    # Vulnerability - Format String Vul
    office_name = unquote(row[1]) if row[1] else row[1]

    elections[dates[row[2]]]['offices'].append(
        {
            "name": office_name, # Use decoded office name
            "id": row[0],
            "zips": [],
            "candidates": []
        }
    )
    for subrow in c.execute(SQL_ZIPS + str(row[0])):
        elections[dates[row[2]]]['offices'][-1]['zips'].append(subrow[0])
    for subrow in c.execute(SQL_CANDIDATES + "'" + str(row[1])+ "'"): # SQL Injection - row[1], getting second value from Office table
        elections[dates[row[2]]]['offices'][-1]['candidates'].append({
            "name": subrow[1],
            "id": subrow[0],
            "votes": subrow[2]
        })
# NEW END --------------------------------


# ORIGINAL START --------------------------------
# for row in c.execute(SQL_OFFICES):
    # if row[2] not in dates:
    #     continue 

    # elections[dates[row[2]]]['offices'].append(
    #     {
    #         "name": row[1],
    #         "id": row[0],
    #         "zips": [],
    #         "candidates": []
    #     }
    # )
    # for subrow in c.execute(SQL_ZIPS + str(row[0])):
    #     elections[dates[row[2]]]['offices'][-1]['zips'].append(subrow[0])
    # for subrow in c.execute(SQL_CANDIDATES + str(row[0])):
    #     elections[dates[row[2]]]['offices'][-1]['candidates'].append({
    #         "name": subrow[1],
    #         "id": subrow[0],
    #         "votes": subrow[2]
    #     })
# ORIGINAL END --------------------------------
print(json.dumps(elections), end="") # dumps convert python data to json strings
c.close()
