from pssh import ParallelSSHClient
hosts = [i.ip_address for i in DOCluster().list()]
client = ParallelSSHClient(hosts, user="root")
from do_cluster import DOCluster

first = "wget https://gist.githubusercontent.com/rsimba/3081604f9271ec952de5/raw/7f05d163f671f033d3b630281240a613358d090a/crawls.py -O crawls.py"
second = "wget https://gist.githubusercontent.com/rsimba/f1424af166d9f0222427/raw/8ddcfadd0ca89660edd2f03a3a4128b7adf88988/social.py -O social.py"
third = "wget https://gist.githubusercontent.com/rsimba/e4664b0a91012cdfff91/raw/b18c9655ec38319e5161d5c978e4583fedf0c5ad/parse.py -O parse.py"
fourth = "wget https://gist.githubusercontent.com/rsimba/c24f6b7f988f95b887fb/raw/928a14684c40330ade9574603684e2820fd1dcd6/upload.py -O upload.py"
fifth = "python crawls.py"
sixth = 'cat links | head -n 1000 | parallel --gnu -j200 "wget -E {}"'
sixth = 'cat links | parallel --gnu -j200 "wget -E {}"'
seventh = "python parse.py"
eighth = "python upload.py"

#DOCluster().stop()
commands = [first, second, third, fourth, fifth]
for command in commands:
    print command
    output = client.run_command(command)
    
l = int(ssdb.hget("crawl","limit"))/2000
num = int(ssdb.hget("crawl","limit")) / l
#output = client.run_command("python crawls.py")
output = client.run_command("split -l {0} links links.".format(num))

multi_download()

commands = [seventh, eighth]
for command in commands:
    print command
    output = client.run_command(command)

""" 

Helpers 

"""

def download_status():
    output = client.run_command("ls *.html | wc -l")
    limit = int(ssdb.hget("crawl","limit"))
    vals = {}
    for k, v in output.iteritems():
        for l in v["stdout"]:
            vals[k] = int(l)
    return vals

def multi_download():
    vals = download_status()
    output = client.run_command("ls links.*")
    vals = {}
    for k, v in output.iteritems():
        for l in v["stdout"]:
            vals[k] = l

    files = vals.values()[0].split()
    sixth = 'cat {0} | parallel --gnu -j200 wget -E'
    for file in files:
        print file
        output = client.run_command(sixth.format(file))
        vals = download_status()
        time.sleep(60)
