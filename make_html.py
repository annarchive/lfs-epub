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

def _init(version):
	path = "view/" + version + "/index.html"
	html_doc=open(path, "rb")
	soup = BeautifulSoup(html_doc, "html.parser")

	toc = soup.find('div', { 'class': 'toc' })
	parts = toc.find_all('li', class_ = re.compile('part|index|preface'))
	return soup,parts

def get_part_title(part):
	title = ""
	try:
		title = part.find('h3').string
	except:
		title = part.find('h4').string
	if not title:
		title = part.find('h3').find('a').string
	return title.strip()

def get_innerlink_map(version):
	inner_link_map_long = {}
	inner_link_map_short = {}
	rootdir = 'view/' + version
	listdir = os.walk(rootdir)
	title_class = re.compile('sect1|part|chapter|title|appendindex|preface')
	for root,dirs,files in listdir:
		long_root = root.replace(rootdir, '..')
		short_root = root.replace(rootdir + '/', '').replace(rootdir, '')
		for name in files:
			if name.endswith(".html"):
				k = os.path.join(root,name)
				kl = os.path.join(long_root, name)
				ks = os.path.join(short_root, name)
				try:
					sp = BeautifulSoup(open(k, "rb"), 'html.parser')
					sect_title_id = sp.find('h1', class_ = title_class).find('a')['id']
					sect_title_id = '#' + sect_title_id
					inner_link_map_long[kl] = sect_title_id
					inner_link_map_short[ks] = sect_title_id
				except:
					pass

	return inner_link_map_long, inner_link_map_short

def copyrightPage(version):
	sp = BeautifulSoup(open('view/' + version + '/legalnotice.html', "rb"), 'html.parser')
	html = sp.find('div', class_ = 'legalnotice').decode_contents(formatter="html")
	html = "<h1>Legal Notice</h1>" + html
	return html
	
def genHtml(version):
	path = 'view/' + version + '/'
	soup,parts = _init(version)
	book = soup.find("div", class_ = "book")
	
	html = ""
	inner_link_map_long, inner_link_map_short = get_innerlink_map(version)
	for part in parts:
		part_title = get_part_title(part)
		html += '<h1>' + part_title + '</h1>'
		
		chapters = part.find_all('li', class_ = "chapter")
		if not chapters:
			chapters = part.find_all('li', class_ = "sect1")
		if not chapters:
			chapters = []
			chapters.append(part)

		for chapter in chapters:
			try:
				chapter_title = chapter.find('h4').string.strip()
			except:
				chapter_title = ""
			if chapter_title:
				html += '<h2>' + chapter_title + '</h2>'
			
			sects = chapter.find_all('a')
			for sect in sects:
				link = sect['href']
				fullpath = path + link
				sp = BeautifulSoup(open(fullpath, "rb"), "html.parser")
				content = sp.find('div', class_ = re.compile('sect1|appendix|index|wrap')).decode_contents(formatter="html")
				#sect_title = replace("h1", "h3")
				html += content.replace('h1', 'h3')
	#new_tag = soup.new_tag('div')
	#lfs_replace_str = "LFS_CONTENT_REPLACE_FROM_LFS_EPUB"
	#new_tag.string = lfs_replace_str
	#soup.find('div', class_ = "toc").append(new_tag)
	#ret = soup.decode_contents(formatter="html").replace(lfs_replace_str, html)
	ret = html.replace('../images/', 'images/')
	for k,v in inner_link_map_long.items():
		ret = ret.replace(k, v)
	for k,v in inner_link_map_short.items():
		ret = ret.replace(k, v)
	
	ret = re.sub('href="#(.*?)#(.*?)"', 'href="#\\2"', ret)
	return ret

if __name__ == '__main__':
	if(len(sys.argv) < 2):
		version = "8.1-systemd"
	else:
		version = sys.argv[1];
	legalnotice = copyrightPage(version)
	html = genHtml(version)
	print(legalnotice + html)
	#print(get_innerlink_map(version))
