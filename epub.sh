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
[ $# -lt 1 ] && version="stable" || version=$1
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

enca -L zh_CH -x UTF-8 view/$version/$HTML
cd view/$version
pandoc --verbose $HTML -o $EPUB \
	-f html+smart -t epub3+smart --toc \
	--extract-media=images/ \
	--epub-cover-image=$RSDIR/cover.jpg \
	--template=$RSDIR/book-template.epub \
	--css=stylesheets/lfs.css \
	--toc-depth=3
	
	#--epub-chapter-level=3 \

	
mv $EPUB ../../$release
	
