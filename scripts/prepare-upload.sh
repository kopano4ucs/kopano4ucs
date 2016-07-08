#!/bin/bash
## Script makes use of the open build service cli client and a private buildnode. Therefore it only works from the Kopano offices.

## TODO: copy stuff from the core download into subdir for webapp app

osc_get () {
	arch="x86_64"
	distro="Univention_4.0"
	project="$1"
	package="$2"
	out="$3"
	mkdir -p  $out
	echo "$package - $out"
	osc getbinaries $project $package $distro $arch -d $out
}

outdir="$HOME/ownCloud-Kopano/kopano4ucs"

# kopano4ucs
osc_get kopano4ucs kopano4ucs $outdir/kopano4ucs
osc_get kopano4ucs meetings4ucs $outdir/webmeetings
osc_get kopano4ucs mod_proxy_wstunnel $outdir/webmeetings

# core
osc_get core:pre-final kopano $outdir/core

# webapp
osc_get webapp:final kopano-webapp $outdir/webapp

# webmeetings
osc_get webmeetings:final kopano-webmeetings $outdir/webmeetings
osc_get webmeetings:final kopano-webapp-plugin-meetings $outdir/webmeetings

# z-push
osc_get z-push:pre-final z-push $outdir/z-push

# remove source and other files
find $outdir -type f ! -name "*.deb" -delete
