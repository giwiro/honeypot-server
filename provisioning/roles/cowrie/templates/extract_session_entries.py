#!/usr/bin/python

activate_this = "{{ cowrie_venv }}/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

from geoip import geolite2
import MySQLdb
import subprocess
import time
import csv
import os

now = time.strftime("%Y%m%d-%H%M")

out_directory = "{{ cowrie_dataset_location }}/session-entries-" + now
out_file = out_directory + "/main.csv"

conn = MySQLdb.connect(host="localhost",
        user="{{ cowrie_mysql_user }}",
        passwd="{{ cowrie_mysql_password }}",
        db="{{ cowrie_mysql_name }}")

cursor = conn.cursor()
query = "SELECT sessions.id, sessions.starttime, sessions.endtime, sessions.ip, ttylog.ttylog FROM sessions LEFT JOIN ttylog on sessions.id = ttylog.session;"

print query

cursor.execute(query)
rows = cursor.fetchall()

os.makedirs(out_directory)

with open(out_file, "w") as out:
    fields = ("id", "starttime", "endtime", "ip", "country")
    writer = csv.writer(out, delimiter=",", doublequote=False,
            quoting=csv.QUOTE_ALL, quotechar="\"", escapechar="\\")
    writer.writerow(fields)
    for r in rows:
        idee = r[0]
        ip = r[3]
        country = ""
        if ip is not None:
            match = geolite2.lookup(ip)
            if match is not None:
                country = match.country
        if r[4] is not None:
            if not os.path.exists(out_directory + "/" + idee):
                os.makedirs(out_directory + "/" + idee)
            tty_location = "{{ cowrie_location }}/" + r[4]
            out_asciinema = out_directory + "/" + idee + "/tty.json"
            command = "{{ cowrie_location }}/bin/asciinema" + " -o " + out_asciinema + " " + tty_location
            # print command
            try:
                # subprocess.call(command)
                os.system(command)
            except Exception as e:
                print "error", e
        data = (idee, r[1], r[2], ip, country)
        writer.writerow(data)
    
cursor.close()
conn.close()
