#!/usr/bin/python

activate_this = "{{ cowrie_venv }}/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

import MySQLdb
import time
import csv

now = time.strftime("%Y%m%d-%H%M")

out_file = "{{ cowrie_dataset_location }}/aut--entries-" + now + ".csv"

conn = MySQLdb.connect(host="localhost",
        user="{{ cowrie_mysql_user }}",
        passwd="{{ cowrie_mysql_password }}",
        db="{{ cowrie_mysql_name }}")

cursor = conn.cursor()
query = "SELECT DISTINCT auth.username, auth.password FROM auth;"

print query

cursor.execute(query)
rows = cursor.fetchall()

with open(out_file, "w") as out:
    fields = ("username", "password")
    writer = csv.writer(out, delimiter=",", doublequote=False,
            quoting=csv.QUOTE_ALL, quotechar="\"", escapechar="\\")
    writer.writerow(fields)
    for r in rows:
        writer.writerow(r)
    
cursor.close()
conn.close()
