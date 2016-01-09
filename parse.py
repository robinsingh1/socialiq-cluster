# for all the html files
# parse html to json
# from json file update ssdb
from os import listdir
from os.path import isfile, join
from ssdb import SSDB
import json
ssdb = SSDB(host='104.131.54.255', port=8888)
from social import *
import arrow

onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
#print onlyfiles
onlyfiles = [i for i in onlyfiles if "html" in i]

print len(onlyfiles)
results = []
pictures = []
# thousand files at a time append to results.json + pictures.json
for i in range(len(onlyfiles)/2000):
        for count, f in enumerate(onlyfiles[i*2000:(i+1)*2000]):
                print f, i, count
                try:
                        f = open(f)
                        html = f.read()
                        results.append(Instagram()._profile(html))
                        pictures.append(Instagram()._pictures(html))
                        f.close()
                except Exception as e:
                        print e
        
        f = open("results-{0}.json".format(i), "w")
        f.write(json.dumps(results))
        f.close()
        
        f = open("pictures-{0}.json".format(i), "w")
        f.write(json.dumps(pictures))
        f.close()
        results, pictures = [], []