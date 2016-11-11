#!/usr/bin/python
# Version 0.5
# add magnet and torrent links throught command torrent client (tested with transmission)
import feedparser
import urllib
import os.path, datetime
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

rss = feedparser.parse(Settings.showrssURL)
n_entries=len(rss['entries'])
all_downloaded = True

for i in range(0,n_entries):
	torrentname = rss['entries'][i]['title']
	if (os.path.isfile(dir_down + '/' + torrentname + '.torrent') or os.path.isfile(dir_down + '/' + torrentname + '.torrent.added') or os.path.isfile(dir_down + '/' + torrentname + '.magnet.added')) == False:
			link = rss['entries'][i]['link']
			os.system(Settings.torrent_client_cmd + link)
			if link[0:6]=='magnet':      
				magnet_file=open(dir_down + '/'+ torrentname  + '.magnet.added','a')
				magnet_file.write(link)
				magnet_file.close()             
			else:
				download_file(dir_down + '/'+ torrentname  + '.torrent', link)
			info_torrent = info_torrent + '\n[' + str(i + 1) + '] ' + torrentname 
			all_downloaded = False


if all_downloaded == True:
	info = info_time + ' Todo descargado'
else:
	info = info_time + ' Nuevos torrents!!!' + info_torrent
	info_email = info_torrent + '\n\nEspacio en Disco: %.2f' % disk_space(dir_down) + 'GB'

if (disk_space(dir_down) <= Settings.space_alert):
	print 'Hay poco espacio en disco!: %.2f' % disk_space(dir_down) + 'GB'
	info_email = info_email + '\nHay poco espacio disponible!!!' 
	
print info

if Settings.email_enabled == True and all_downloaded == False:
	import gmail
	email_user = Settings.email_user
	email_pwd = Settings.email_pwd
	email_dst = Settings.email_dst
	for send_to in email_dst:
		gmail.send_mail(email_user, email_pwd, send_to, 'Rpi: nuevos episodios!!!', info_email)
	
if Settings.log_enabled == True:
	log_file = path + '/showrssd.log'
	mylog = open(log_file, 'a')
	mylog.write(info + '\n')
	mylog.close

