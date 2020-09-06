#!/bin/bash

############################
# Usage:
# File Name: download.sh
# Author: annhe  
# Mail: i@annhe.net
# Created Time: 2017-10-25 18:41:07
############################

rm -fr www.linuxfromscratch.org
lfsdir="view"
[ ! -d $lfsdir ] && mkdir $lfsdir
[ $# -lt 1 ] && version="stable" || version=$1
wget -r -p -np -k "http://www.linuxfromscratch.org/lfs/view/$version/"
mv www.linuxfromscratch.org/lfs/view/* $lfsdir
rm -fr www.linuxfromscratch.org
