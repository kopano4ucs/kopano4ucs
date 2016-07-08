#!/bin/bash
## Script makes use of the open build service cli client and a private buildnode. Therefore it only works from the Kopano offices.

## TODO: copy stuff from the core download into subdir for webapp app

osc_get () {
	arch="x86_64"
	distro="Univention_4.0"
	project="$1"
	package="$2"
	out="$3"

	echo "$package - $out"
	mkdir -p  $out
	osc getbinaries $project $package $distro $arch -d $out
}

outdir="$HOME/ownCloud-Kopano/kopano4ucs"

# kopano4ucs
osc_get kopano4ucs kopano4ucs $outdir/kopano4ucs

# core
osc_get core:pre-final kopano $outdir/core

# webapp
osc_get webapp:final kopano-webapp $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-delayeddelivery $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-desktopnotifications $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-filepreviewer $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-spell $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-spell-de-at $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-spell-de-ch $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-spell-de-de $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-spell-en-gb $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-spell-en-us $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-spell-es-es $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-spell-fr-fr $outdir/webapp
osc_get webapp:final kopano-webapp-plugin-spell-nl-nl $outdir/webapp

osc_get files:final kopano-webapp-plugin-files $outdir/webapp
osc_get files:final kopano-webapp-plugin-filesbackend-owncloud $outdir/webapp
osc_get files:final kopano-webapp-plugin-filesbackend-smb $outdir/webapp

osc_get mdm:final kopano-webapp-plugin-mdm $outdir/webapp

deps="php5-mapi"
echo "webapp dependencies - $outdir/webapp-dependencies"
mkdir -p $outdir/webapp-dependencies
for pkg in $deps; do
	find $outdir/core -name "$pkg"*.deb -exec cp {} $outdir/webapp-dependencies \;
done

# webmeetings
osc_get kopano4ucs meetings4ucs $outdir/webmeetings
osc_get kopano4ucs mod_proxy_wstunnel $outdir/webmeetings
osc_get webmeetings:final kopano-webmeetings $outdir/webmeetings
osc_get webmeetings:final kopano-webapp-plugin-meetings $outdir/webmeetings

# z-push
osc_get z-push:pre-final z-push $outdir/z-push

# remove source and other files
#find $outdir -type f ! -name "*.deb" -delete
