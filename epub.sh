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
cwd=`cd $(dirname $0);pwd`
RSDIR="$cwd/resources"

HTML="lfs-$version.html"
EPUB="lfs-$version.epub"
META="META-$version.html"

echo "<head>" > view/$version/$HTML
./make_meta.py $version >> view/$version/$HTML
echo "</head><body>" >> view/$version/$HTML
./make_html.py $version >> view/$version/$HTML
echo "</body>" >> view/$version/$HTML

cd view/$version
pandoc --verbose $HTML -o $EPUB \
	-t epub3 --toc --smart \
	--extract-media=images/ \
	--epub-cover-image=$RSDIR/cover.jpg \
	--template=$RSDIR/book-template.epub \
	--epub-stylesheet=stylesheets/lfs.css \
	--toc-depth=3
	
	#--epub-chapter-level=3 \

	
mv $EPUB ../../$release
	
