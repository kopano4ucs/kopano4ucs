#!/bin/bash
## Script makes use of the open build service cli client and a private buildnode. Therefore it only works from the Kopano offices.

tempdir=$(mktemp -d)

mkdir -p $tempdir/{kopano4ucs,core,webapp,webmeetings,z-push}

# kopano4ucs
osc getbinaries kopano4ucs kopano4ucs Univention_4.0 x86_64 -d $tempdir/kopano4ucs

# core
osc getbinaries core:pre-final kopano Univention_4.0 x86_64 -d $tempdir/core

# webapp
osc getbinaries webapp:final kopano-webapp Univention_4.0 x86_64 -d $tempdir/webapp

# webmeetings
osc getbinaries webmeetings:final kopano-webmeetings Univention_4.0 x86_64 -d $tempdir/webmeetings
osc getbinaries webmeetings:final kopano-webapp-plugin-meetings Univention_4.0 x86_64 -d $tempdir/webmeetings

# z-push
osc getbinaries z-push:pre-final z-push Univention_4.0 x86_64 -d $tempdir/z-push

# remove source and other files
find $tempdir -type f ! -name "*.deb" -delete

tar czvf univention-kopano-release.tar.gz $tempdir

rm -r $tempdir
