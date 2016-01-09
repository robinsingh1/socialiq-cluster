#!/usr/bin/python

from ssdb import SSDB
import json
import time
import os
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import json
import subprocess
ssdb = SSDB(host=os.environ['SSDB_HOST'], port=os.environ['SSDB_PORT'])

# pop off queue
urls = ssdb.qpop("ig-queue",100)

# write to file
f = open("links.txt", "w")
f.write("\n".join(map(lambda x: str(x), urls)))
f.close()

try:
    bashCommand = "cat links.txt | parallel --gnu -j200 wget -E"
    output = subprocess.check_output(['bash','-c', bashCommand])
except Exception as e:
    print e


# parse file
onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
onlyfiles = [i for i in onlyfiles if "html" in i]

class Instagram:
    def _profile(self, body):
        bs = BeautifulSoup(body,"lxml")

        #lol = bs.find_all("script")[-4].text[21:]
        lol = bs.find_all("script")[-5].text[21:]
        lol = json.loads(lol[:-1])
        user = lol["entry_data"]["ProfilePage"][0]["user"]

        #pics = user["media"]["nodes"]
        user["_id"] = user["id"]
        del user["id"]
        user["followers"] = user["followed_by"]["count"]
        user["following"] = user["follows"]["count"]
        user["picture-count"] = user["media"]["count"]
        del user["media"]
        del user["follows"]
        del user["followed_by"]
        return user

results = []
for i in onlyfiles:
    print i
    try:
        f = open(i)
        html = f.read()
        results.append(Instagram()._profile(html))
        f.close()
    except Exception as e:
        print e

f = open("results.json", "w")
f.write(json.dumps(results))
f.close()

# upload ssdb
res = json.loads(open("results.json").read())[:]
values = dict([[i["username"],i["followers"]] for i in res])

ssdb.multi_zset("instagram-followers", **values)
ssdb.multi_zset("swarm-instagram-followers", **values)
