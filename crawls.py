# Get URLS from SSDB and turn into a text file called links
import subprocess
import os

from ssdb import SSDB
ssdb = SSDB(host='104.131.54.255', port=8888)

# get hostid
hostid = subprocess.check_output(['curl','http://ipinfo.io/ip']).strip()

limit = ssdb.hget("crawl","limit")
offset = ssdb.hget("crawl", hostid)

users = ssdb.zrange("instagram-users", int(offset), int(limit))
arr = users
 
f = open("links", "w")
f.write("\n".join(map(lambda x: str(x), arr)))
f.close()