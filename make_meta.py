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
from time import strftime

def metadata(version):
	path = "view/" + version + "/index.html"
	html_doc=open(path,"rb")
	soup = BeautifulSoup(html_doc, "html.parser")

	titlepage = soup.find('div', { 'class': 'titlepage' })
	meta = {}
	meta['title'] = titlepage.find('h1', class_ = 'title').get_text().strip()
	meta['subtitle'] = titlepage.find('h2', class_ = 'subtitle').string.strip()
	meta['rights'] = titlepage.find('p', class_ = 'copyright').decode_contents(formatter="html")
	meta['rights'] = meta['rights'].replace('</a>','')
	meta['rights'] = meta['rights'].strip()
	meta['rights'] = re.sub('<a.*?>', '', meta['rights'])
	meta['author'] = "Author: " + titlepage.find('h3', class_ = 'author').get_text().strip()
	meta['publisher'] = "Publisher: https://github.com/annProg/lfs-epub"
	meta['date'] = "Compile Date: " + strftime("%m/%d/%Y %H:%M")
	for k,v in meta.items():
		meta[k] = re.sub('\n\s*', ' ', meta[k])
		
	return meta
	
def metaxml(meta):
	xml = []
	for k,v in meta.items():
		xml.append('<dc:' + k + '>' + v + '</dc:' + k + '>')
	return xml

def metacmd(meta):
	cmd = []
	for k,v in meta.items():
		cmd.append('-V --' + k + '=' + v.replace(' ', '-'))
	return cmd
def metayaml(meta):
	yaml = []
	for k,v in meta.items():
		yaml.append(k + ':' + ' ' + v)
	return '---\n' + "\n".join(yaml) + '\n---'

def metahtml(meta):
	html = []
	for k,v in meta.items():
		html.append('<meta name="' + k + '" content="' + v + '">')
	return "\n".join(html)
	
if __name__ == '__main__':
	if(len(sys.argv) < 2):
		version = "8.1-systemd"
	else:
		version = sys.argv[1];
	meta = metadata(version)
	html = metahtml(meta)
	print(html)