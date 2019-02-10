#!/usr/bin/env python3
# Created by: Tommy Asmund Gunnar Kristiansen


from bs4 import BeautifulSoup
import requests
import sys,os,re


class video: 
	default = "ytdl://youtube.com"
	def __init__(self, url, title, episode, duration):
		self.url = self.default + url
		self.title = title
		self.episode = episode
		self.duration = duration[2:-2]


def help():
	print("Make sure the url you try\nmatches this regex\n\nyoutube.com\/playlist\?list=PL(.{32})")
	return

def html_decode(s):
	html_codes=(
		("'",'&#39;'),
		('"','&quot;'),
		('>','&gt;'),
		('<','&lt;'),
		('&','&amp;')
		)
	for code in html_codes:
		s = s.replace(code[1], code[0])
	return s


def Load_url(url):
	urlpat = r".+?youtube.com\/playlist\?list=PL(.{32})"
	if (re.findall(urlpat, url)):
		req  = requests.get(url)
		return req.text
	else:
		print("Not valid url")
		help()
		sys.exit(2)
		return


def Traverse(page):
	if (page):
		soup = BeautifulSoup(page, "html5lib")
		title = soup.find("title").text
		raw_ep_url = []
		raw_titles = []
		raw_desc = []
		raw_dur = []
		for tag in soup.find_all("a", class_="yt-uix-sessionlink"):
#/watch?v=ciZNuy3-jlM
			tmp = tag.get("href")[:20]
			m = re.search( r"(.+watch.+)",tmp)
			if (m):
				if (m[0] in raw_ep_url):
					continue
				else: 
					raw_ep_url.append(m[0])
			
		for tg in soup.find_all("a",{"class":"yt-uix-tile-link"}):
			tmp = tg.text
			if(tmp):
				if (tmp in raw_titles):
					continue
				else:
					tmp = tmp.strip()
					raw_titles.append(tmp)

		for tag in soup.find_all("tr", class_="pl-video yt-uix-tile"):
			raw_desc.append(tag["data-title"])

		for tag in soup.find_all("div", class_="timestamp"):
			tmp = tag.contents[0].contents
			if (tmp in raw_dur):
				continue
			else:
				raw_dur.append(str(tmp))
		show = []
		for index in range(len(raw_titles)):
			v = video(raw_ep_url[index],raw_titles[index],raw_desc[index],raw_dur[index])
			show.append(v)
	return show, title

def CreatePlaylist(show, title):
	title = title.strip()
	with open(title[:-10]+'.m3u',"w") as f:
		f.write("#EXTM3U")
		for vid in show:
			f.write("#EXTINFO:"+ str(vid.duration)+", "   +vid.title+ "\n" +  vid.url +"\n\n" )
		f.close()
		print("All done, enjoy your show")
	return

def Fromfile(path):
	with open(path) as f:
		CreatePlaylist(*Traverse(f.read()))
	return


# get the args and handle them if any.
if (len(sys.argv)>0):
	if (sys.argv[1] == "-h"):
		help()
	elif(sys.argv[1] == "-f"):
		#do the thing
		Fromfile(sys.argv[2])
	elif(sys.argv[1] == "-p"):
		CreatePlaylist(*Traverse(Load_url(sys.argv[2])))
	else:
		print("Supported args are -h for help or -p for playlist")
		help()
