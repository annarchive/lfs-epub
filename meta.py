#!/usr/bin/env python3
#-*- coding:utf-8 -*-  

############################
# Usage:
# File Name: epub.py
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2017-10-25 17:14:18
############################

from bs4 import BeautifulSoup
import re
import sys
import os

def metadata(version):
	path = "view/" + version + "/index.html"
	html_doc=open(path)
	soup = BeautifulSoup(html_doc, "html.parser")

	titlepage = soup.find('div', { 'class': 'titlepage' })
	meta = {}
	meta['tile'] = titlepage.find('h1', class_ = 'title').find('a').string
	meta['subtitle'] = titlepage.find('h2', class_ = 'subtitle').string
	meta['rights'] = titlepage.find('p', class_ = 'copyright').find('a').string
	meta['creator'] = titlepage.find('h3', class_ = 'author').get_text()

	return meta
	
if __name__ == '__main__':
	if(len(sys.argv) < 2):
		version = "8.1-systemd"
	else:
		version = sys.argv[1];
	meta = metadata(version)
	print(meta)
	#print(get_innerlink_map(version))
