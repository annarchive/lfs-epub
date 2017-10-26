#!/bin/bash

############################
# Usage:
# File Name: epub.sh
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2017-10-26 14:04:10
############################

pandoc --toc --smart  --epub-stylesheet=view/8.1-systemd/stylesheets/lfs.css --extract-media=view/8.1-systemd/images/ --number-sections --epub-chapter-level=2 view/8.1-systemd/lfs.html -o lfs.epub
