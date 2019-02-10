# Youtube-to-m3u
A python script that takes a youtube URL and turns it into a m3u file for use with a video player via the youtube-dl subsystem, in players like mpv.

mpv does support this by default, this script was written as a way to learn python3.


use:
 yt-m3u.py -f html_source_code_from_the_playlist_page.
 
 
 yt-m3u.py -p some_youtube.com_playlist_url
 
 Tool outputs a file with the title of the playlist from the page, in the m3u fileformat.
