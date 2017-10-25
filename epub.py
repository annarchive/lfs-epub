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

def _init(version):
	path = "view/" + version + "/index.html"
	html_doc=open(path)
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

def genHtml(version):
	path = 'view/' + version + '/'
	soup,parts = _init(version)
	book = soup.find("div", class_ = "book")
	
	html = ""
	inner_link_map = {}
	for part in parts:
		part_title = get_part_title(part)
		html += '<div class="part"><div class="part-title"><h1>' + part_title + '</h1></div>'
		
		chapters = part.find_all('li', class_ = "chapter")
		for chapter in chapters:
			chapter_title = chapter.find('h4').string.strip()
			if chapter_title:
				html += '<div class="chapter-title"><h2>' + chapter_title + '</h2></div>'
			
			sects = chapter.find_all('a')
			for sect in sects:
				link = sect['href']
				fullpath = path + link
				sp = BeautifulSoup(open(fullpath), "html.parser")
				content = sp.find('div', class_ = re.compile('sect1|appendix|index|wrap')).decode_contents(formatter="html")
				sect_title_id = sp.find('h1', class_ = 'sect1').find('a')['id']
				inner_link_map['../' + link] = "#" + sect_title_id
				#sect_title = replace("h1", "h3")
				html += content.replace('h1', 'h3')
		html += '</div>'
	new_tag = soup.new_tag('div')
	lfs_replace_str = "LFS_CONTENT_REPLACE_FROM_LFS_EPUB"
	new_tag.string = lfs_replace_str
	soup.find('div', class_ = "toc").append(new_tag)
	ret = soup.decode_contents(formatter="html").replace(lfs_replace_str, html)
	ret = ret.replace('../images/', 'images/')
	for k,v in inner_link_map.items():
		ret = ret.replace(k, v)
	return inner_link_map, ret

if __name__ == '__main__':
	if(len(sys.argv) < 2):
		version = "8.1-systemd"
	else:
		version = sys.argv[1];
	inner_link_map, html = genHtml(version)
	print(html)
