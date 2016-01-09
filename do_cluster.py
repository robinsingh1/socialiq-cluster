import digitalocean
from shortid import ShortId

sid = ShortId().generate()

class DOCluster:
    def start(self, num=1):
        droplets = []
        name = ShortId().generate().replace("_","")
        print name
        for i in range(num):
            droplet = digitalocean.Droplet(token="0bf26a0e6e20f740f55bd809b3058c076d41e2d50632c6ebc51817f174e22d85",
                                           name='cluster-machine-{0}-{1}'.format(i, name),
                                           region='nyc3', # New York 2
                                           # snapshot
                                           ssh_keys=["ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDM/T9hA07F7Dzy8xSuM1K+0z/uOtUUDz6Hv/yi5IiGaoFyr0JoKJPV8aK0pDA6UgLg4e8mYucawk6lUs6jQ4IGeCu829a27Erlwyq1J50k5SX0Qu9qIKWOnwORIFEqsvlQA9KAet/W18cN2m2X8aVlhGo8M23SDzUIhD2kdN4bEP0i5cMerLMtKB0K2GWjw5kDwjm4qud04YAsLrwV7gcZug0pi/mzQJ+XGAM4LS3vU1rNFtHX6cPVAU9S2QeV3hN9IIiSE883fiS8f1Iw1sAvnQe8A6VJYl1z6CJpHQaabloJ6ULdtvfAqGPYYSKyLZdDhHFP+yLsLQKgpkr353jz robin.singh.1991@gmail.com"],
                                           #image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
                                           image='15200406',
                                           size_slug='512mb',  # 512MB
                                           backups=False)
            droplet.create()
            droplets.append(droplet)
        return droplets
    
    def stop(self):
        """ """
        manager = digitalocean.Manager(token="0bf26a0e6e20f740f55bd809b3058c076d41e2d50632c6ebc51817f174e22d85")
        my_droplets = manager.get_all_droplets()
        for droplet in my_droplets:
            if "cluster-machine" in droplet.name:
                print droplet.destroy()
        
    def list(self):
        manager = digitalocean.Manager(token="0bf26a0e6e20f740f55bd809b3058c076d41e2d50632c6ebc51817f174e22d85")
        my_droplets = manager.get_all_droplets()
        
        return [i for i in my_droplets if "cluster-machine-" in i.name]
    
    def status(self):
        manager = digitalocean.Manager(token="0bf26a0e6e20f740f55bd809b3058c076d41e2d50632c6ebc51817f174e22d85")
        my_droplets = manager.get_all_droplets()
        
        cluster = [i.load() for i in my_droplets if "cluster-machine-" in i.name]
        print cluster
        return dict([[i.ip_address, i.status] for i in cluster])
    
    def create_crawl(self):
        ids = [i.ip_address for i in DOCluster().list()]
        limit = ssdb.zsize("instagram-users")/len(ids)
        offset = ""
        vals = dict(zip(ids, [i*limit for i in range(len(ids))]))
        for k in vals.keys():
            if vals[k] == 0:
                vals[k] = 1
        vals["limit"] = limit
        ssdb.multi_hset("crawl", **vals)
        print vals
        # ssdb.hget("crawl","limit")
