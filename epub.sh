#!/bin/bash

############################
# Usage:
# File Name: epub.sh
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2017-10-26 14:04:10
############################
release="release"
[ ! -d $release ] && mkdir $release
[ $# -lt 1 ] && version="8.1-systemd" || version=$1

HTML="lfs-$version.html"
EPUB="lfs-$version.epub"

./epub.py $version >view/$version/$HTML
cd view/$version
pandoc -t epub3 --toc --smart \
	$HTML -o $EPUB \
	--extract-media=images/ \
	--epub-stylesheet=stylesheets/lfs.css \
	--toc-depth=3
	
	#--epub-chapter-level=3 \

	
mv $EPUB ../../$release
	
