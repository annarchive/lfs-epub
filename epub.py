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

html_doc=open("index.html")
soup = BeautifulSoup(html_doc, "html.parser")

toc = soup.find('div', { 'class': 'toc' })
parts = toc.find_all('li', class_ = re.compile('part|index|preface'))

def get_part_title(part):
	try:
		title = ch.find('h3').string
	except:
		pass
	if not title:
		title = ch.find('h3').find('a').string
	return title.strip()

def get_chapters(part):
	chapters = part.find_all('li', class_ = "chapter")

def get_sects(part):
	sects = part.find_all('li', class_ = "sect1")

def get_chapter_title(part):

	title = ch.find('h4').string
	return title.strip()

for part in parts:
	part_title = get_part_title(part)
	chapter_title = get_chapter_title(part)
	print(chapter_title)
#print(chapter.prettify())
