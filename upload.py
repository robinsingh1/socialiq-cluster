import arrow
from ssdb import SSDB
import json
ssdb = SSDB(host='104.131.54.255', port=8888)

onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
onlyfiles = [i for i in onlyfiles if "results-" in i]

for file_name in onlyfiles:
        timestamp = arrow.utcnow().timestamp
        res = json.loads(open("results.json").read())[:]
        values = dict([[i["username"],i["followers"]] for i in res])
        #print values[values.keys()[0]], values.keys()[0]
        ssdb.multi_zset("instagram-followers", **values)
        ssdb.multi_zset("test-instagram-followers", **values)
        
        values = dict([[i["username"], timestamp] for i in res])
        ssdb.multi_zset("ig-last-crawled", **values)
        ssdb.multi_zset("ig-last-updated", **values)
        
        values = dict([[i[_id], i["username"]] for i in res])
        ssdb.multi_hset("ig-username-id", **values)

        for c, user in enumerate(json.loads(open("results.json").read())[:]):
                print c
                un = user["username"]
                cols = ["profile_pic_url","full_name","followers","following","username"]
                vals = [user[c] for c in cols]
                info = dict(zip(cols, vals))
        
                #Information
                ssdb.set("ig-{0}-user-bio".format(un), user["biography"])
                ssdb.set("ig-{0}-user-info".format(un), info)
        
                # TODO multizset
                ssdb.zset("ig-{0}-followers".format(un), timestamp, user["followers"])
                ssdb.zset("ig-{0}-following".format(un), timestamp, user["following"])
                ssdb.zset("ig-{0}-picture-count".format(un), timestamp, user["picture-count"])
                
onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
onlyfiles = [i for i in onlyfiles if "pictures-" in i]
for file_name in onlyfiles:
        timestamp = arrow.utcnow().timestamp
        res = json.loads(open(file_name).read())[:]

        values = dict([[i["code"], 0 for i in res])
        ssdb.multi_zset("instagram-pictures", **values)

        for i in res:
                pic_id = i["code"]
                ssdb.set("ig-{0}-pic-caption".format(pic_id), i["caption"])
                ssdb.set("ig-{0}-pic-info".format(pic_id), json.dumps(i))
                del i["caption"]

                ssdb.multi_zset("ig-{0}-pictures".format(i["owner"]), i["date"], i["code"])
                ssdb.multi_zset("ig-{0}-likes".format(pic_id), timestamp, i["likes"])
                ssdb.multi_zset("ig-{0}-comments".format(pic_id), timestamp, i["comments"])