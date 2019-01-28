#!/usr/bin/env python3
# Created by: Tommy Asmund Gunnar Kristiansen
# takes the path of a youtube playlist and creates
# a file compatible for use with mpv as a playlist object



import requests
import re
import sys, subprocess, os



def help():
	print("Make sure the url you try\nmatches this reged\n\nyoutube.com\/playlist\?list=PL(.{32})")
	return






def html_decode(s): #stackoverflow, cuz why make a wheel
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

class video: #container for the video setup
	default = "ytdl://youtube.com"
	url = ""
	title = ""
	episode = ""
	duration = ""	
	def __init__(self, url, title, episode, duration):
		self.url = self.default + url
		self.title = title
		self.episode = episode
		self.duration = duration


def validate_input(data):
	#pattern = r"youtube.com\/playlist\?list=PL(.{32})"
	pattern = r".+?youtube.com\/playlist\?list=PL(.{32})"
	test = re.findall(pattern, data)
	if len(test) == 1:
		url = data
	else:
		print("it did not match, try again")
		help()
		sys.exit(2)
	return url


def get_data(url):


#The actual work begins here, read the url and then process it.
#	r = requests.get('https://www.youtube.com/playlist?list=PLxIQ9fpV90xMG4FheSs0FGsORme8IayF0')
	
	#r = requests.get(url)
	#workaround
	#f = open("test.txt", "w")
	#f.write(r.text)
	#f.close()
	cmd = "curl "+ url + " > tmp.src"
	print(cmd)
	returned_val = os.system(cmd)
	#print(returned_val)
	tmp  = open("tmp.src")
	r = tmp.read()

	
# Extract the url for the video, and the name of the episode
	eprgx = r"(\/watch\?v=.{11}).+?\n\s+(.+(Ep \d+)(.+\n))" #youtube url
	#eprgx = r".+?\n\s+(.+(Ep \d+)(.+\n))"
	#eprgx = r"(\/watch\?v=.{11}).+?\n\s+(.+)"
	#eprgx = r"(\/watch\?v=.{11})"
	tsrgx = r"timestamp.+\">(.+)<\/s"
	shrgx = r"descr.+ent=\"(.+\.)\""
	desc = re.search(shrgx, r)
	#time = re.findall(tsrgx, r)
	pat = re.findall(eprgx, r)
	vids = list()

	write_showdata(desc)
#	if len(pat) != len(time):
#		print("sumtingwong")
	for vid in pat:
		#v = video(vid[0], html_decode(vid[1]), html_decode(vid[2]), time[pat.index(vid)])
		v = video(vid[0], html_decode(vid[1]), html_decode(vid[2]), "1")
		vids.append(v)
	return vids

def write_showdata(desc):
	
	if (desc==None):

		return
	else:
		with open("show.txt","w") as s:
			s.write(html_decode(desc.group(1)))
			s.close()

		return	


def store_data(vids):
	print(vids)
	with open("playlist.m3u", "w") as f:
		f.write("#EXTM3U")
		for vid in vids:
			f.write("#EXTINFO:"+ vid.duration+", "  +vid.episode+ " " +vid.title+ "\n" +  vid.url +"\n\n" )

	f.close()

	print("All done, enjoy your show")
	return

# first argument is always the path, then the first argument and then the second.
if (len(sys.argv)>0):
	if (sys.argv[1] == "-h"):
		help()
	elif(sys.argv[1]== "-p"):
		store_data(get_data(validate_input(sys.argv[2])))
