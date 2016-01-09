import requests
#import tinycss
from bs4 import BeautifulSoup
#from splinter import Browser
import json
#import pandas as pd
#import requests
#import metadata_parser

class Vine:
    def _profile(self, body):
        #r = requests.get("https://vine.co/brittanyfurlan")
        #page = metadata_parser.MetadataParser(html=r.text)
        followers = BeautifulSoup(body, "lxml").find("li",{"class":"followers"}).text.split()[0]
        following = BeautifulSoup(body, "lxml").find("li",{"class":"following"}).text.split()[0]
        posts = BeautifulSoup(body,"lxml").find("li",{"class":"total-timeline-count"}).text.split()[0]
        name = BeautifulSoup(body,"lxml").find("h2").text
        description = BeautifulSoup(body,"lxml").find("meta",{"name":"description"})["content"]
        final = {"followers":followers,"following":following,
                 "posts":posts,"name":name,"description":description}
        return final

class Pinterest:
    def _profile(self, body):
        page = metadata_parser.MetadataParser(html=body)
        final = pd.DataFrame([page.metadata["meta"]])[["description","og:title","og:title","og:image",
                                                   "pinterestapp:followers","pinterestapp:following","pinterestapp:boards",
                                                                                          "pinterestapp:pins"]]
        #print final.to_dict("r")[0]
        _final = {}
        for i in final.to_dict("r")[0].keys():
            _final[i.split(":")[-1]] = final.to_dict("r")[0][i]
        return _final

class Twitter:
    def _profile(self, body):
        final = []
        for i in BeautifulSoup(body,"lxml").find("ul",{"class":"ProfileNav-list"}).find_all("li")[:3]:
            try:
                final.append([i.find_all("span")[0].text.lower(), i.find("a")["title"].split()[0].replace(",","")])
            except:
                """"""
        final = dict(final)
        return final

class Instagram:
    def _pictures(self, body):
        bs = BeautifulSoup(body,"lxml")
        lol = bs.find_all("script")[-5].text[21:]
        lol = json.loads(lol[:-1])
        user = lol["entry_data"]["ProfilePage"][0]["user"]
        #print user.keys()
        pics = user["media"]["nodes"]
        for pic in pics:
                del pic["dimensions"]
                #del pic["owner"]
                pic["owner"] = user["username"]
                if "comments" in pic.keys():
                        comments = pic["comments"]["count"]
                        pic["comments"] = comments
                if "likes" in pic.keys():
                        likes = pic["likes"]["count"]
                        pic["likes"] = likes
        return pics
        
    def _profile(self, body):
        #r = requests.get("https://instagram.com/justinbieber/")
        #page = metadata_parser.MetadataParser(html=r.text)
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
    
    def _profile_from_photo(self, html):
        bs = BeautifulSoup(html,"lxml")
        lol = bs.find_all("script")[-4].text[21:]
        lol = json.loads(lol[:-1])
        #user = lol["entry_data"]["ProfilePage"][0]["user"]
        user = lol["entry_data"]["PostPage"][0]["media"]["owner"]
        user["link"] = "http://instagram.com/"+user["username"]
        return html

class Youtube:
    def _profile(self, body):
        #r = requests.get("https://www.youtube.com/user/TimothyDeLaGhetto2/about")
        #page = metadata_parser.MetadataParser(html=r.text)

        bs = BeautifulSoup(body, "lxml")
        item = {}

        stats = bs.find_all("span",{"class":"about-stat"})
        subs = int(stats[0].text.split(" ")[0].replace(",",""))
        views = int(stats[1].find("b").text.replace(",",""))
        date_joined = stats[2].text.split("Joined ")[-1]
        try:
          description = bs.find("div",{"class":"about-description"}).text
        except:
          description = "desc error"

        #links = dict([[i.text.strip().replace(".","_"), i["href"]] for i in bs.find_all("div",{"class":"about-metadata"})[0].find_all("a")])
        # Only Get Youtube recomenned links for more
        other_channels = dict([[i.text.strip().replace(".","_"), i["href"]] for i in bs.find_all("ul",{"class":"branded-page-related-channels-list"})[1].find_all("a")])
        social_links = [i.find("a")["href"] for i in bs.find_all("li",{"class":"channel-links-item"})]
        channels = bs.find("div",{"class":"branded-page-v2-secondary-col"})
        _channels = []
        for i in channels.find_all("a",{"class":"spf-link"}):
            if i.text.strip() == "": continue
            _channels.append({ "name":i.text.strip(), "link": i["href"]})

        pp = bs.find("img",{"class":"channel-header-profile-image"})
        pp = pp["src"] if pp else ""

        parser = tinycss.make_parser('page3')
        stylesheet = parser.parse_stylesheet_bytes(bs.find_all("style")[1].text)
        cp = stylesheet.rules[0].declarations[0].value.as_css().split("url(")[-1].replace(")","")

        print cp
        item["subs"] = subs
        item["profile_pic"] = pp
        item["cover_pic"] = cp
        item["views"] = views
        item["handle"] = bs.find("span",{"class":"qualified-channel-title-text"}).find("a")["href"]
        item["link"] = "http://youtube.com/"+item["handle"]
        item["date_joined"] = date_joined
        item["description"] = description
        item["other_channels"] = other_channels
        item["links"] = social_links
        #item["other_channels"] = _channels
        item["followers"] = item["subs"]
        print item
        return item

    def _channel_profiles(self, html):
        bs = BeautifulSoup(html,"lxml")
        channels = []
        for li in bs.find_all("li",{"class":"channels-content-item"}):
            subs = li.find("span",{"class":"yt-subscription-button-subscriber-count-unbranded-horizontal"})["aria-label"]
            subs = int(subs.replace(",","").split()[0])
            name = li.find("h3").text.split(" - ")[0]
            link = li.find("a")["href"]
            logo = li.find("img")["src"]
            cols = ["subs","name","link","logo"]
            vals = [subs,name,link,logo]
            channels.append(dict(zip(cols, vals)))
        return channels

class Soundcloud:
    def _profile(self, html):
        bs = BeautifulSoup(html,"lxml")
        md = page = metadata_parser.MetadataParser(html=html).metadata
        song_info = json.loads(bs.find_all("script")[-1].text.split("c,o,i=")[-1].split(",u=Date")[0])
        info = dict(song_info["3476"][0].items()+ md.items())
        info["link"] = info["permalink_url"]
        return info

#r = requests.get("https://www.youtube.com/user/theTimothyDeLaGhetto/about")
#Youtube()._profile(r.text)
