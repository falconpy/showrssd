#!/usr/bin/python

import feedparser
import urllib
import sys, os.path, datetime
from settings import Settings

def download_file(filename, fileURL):
	urllib.urlretrieve(fileURL, filename)

def disk_space(path):
	ds = os.statvfs(path)
	free = ds.f_bavail * ds.f_frsize
	free_MB = free / 1048576.0
	free_GB = free_MB / 1024
	return free_GB

path = os.path.dirname(os.path.abspath(__file__))

info_time = str(datetime.datetime.now())
info_torrent = ''
dir_down = Settings.dir_download
SRurl = Settings.showrssURL
log = Settings.log_enabled
email = Settings.email_enabled

rss = feedparser.parse(SRurl)
n_entries=len(rss['entries'])
all_downloaded = True

for i in range(0,n_entries):
	torrentname = rss['entries'][i]['title']
	if (os.path.isfile(dir_down + '/' + torrentname + '.torrent') or os.path.isfile(dir_down + '/' + torrentname + '.torrent.added')) == False:
		torrentlink = rss['entries'][i]['link']
		#info = info + ',link ' + torrentlink
		download_file(dir_down + '/'+ torrentname  + '.torrent', torrentlink)
		info_torrent = info_torrent + '\n[' + str(i + 1) + '] ' + torrentname 
		all_downloaded = False


if all_downloaded == True:
	info = info_time + ' All downloaded'
else:
	info = info_time + ' New torrents!!!' + info_torrent
	info_email = info_torrent + '\n\nDisc Space: %.2f' % disk_space(dir_down) + 'GB'

if (disk_space(dir_down) <= Settings.space_alert):
	print 'Low Disc Space!: %.2f' % disk_space(dir_down) + 'GB'
	info_email = info_email + '\nLow Disc Space!!!!' 
	
print info

if email == True and all_downloaded == False:
	import gmail
	email_user = Settings.email_user
	email_pwd = Settings.email_pwd
	email_dst = Settings.email_dst
	for send_to in email_dst:
		print send_to	
		gmail.send_mail(email_user, email_pwd, send_to, 'Rpi: new shows!!!', info_email)
	
if log == True:
	log_file = path + '/showrssd.log'
	mylog = open(log_file, 'a')
	mylog.write(info + '\n')
	mylog.close


