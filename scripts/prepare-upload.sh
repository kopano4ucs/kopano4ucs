#!/bin/bash
## Script makes use of the open build service cli client and a private buildnode. Therefore it only works from the Kopano offices.
set -e

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

if [ ! -d "$outdir" ]; then
	git clone https://fbartels@stash.z-hub.io/scm/k4u/app-metadata.git $outdir
fi

# kopano4ucs
osc_get kopano4ucs kopano4ucs $outdir/kopano4ucs

# core
osc_get core:pre-final kopano $outdir/kopano-core/packages

# copying over kopano4ucs dependencies
mkdir -p $outdir/kopano-webapp/packages
deps="kopano4ucs-lib kopano4ucs-multiserver kopano4ucs-schema kopano4ucs-udm kopano4ucs"
for pkg in $deps; do
  cp $outdir/kopano4ucs/"$pkg"*.deb $outdir/kopano-webapp/packages/
done

# webapp
osc_get webapp:final kopano-webapp $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-delayeddelivery $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-desktopnotifications $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-filepreviewer $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-spell $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-spell-de-at $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-spell-de-ch $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-spell-de-de $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-spell-en-gb $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-spell-en-us $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-spell-es-es $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-spell-fr-fr $outdir/kopano-webapp/packages
osc_get webapp:final kopano-webapp-plugin-spell-nl-nl $outdir/kopano-webapp/packages

osc_get files:final kopano-webapp-plugin-files $outdir/kopano-webapp/packages
osc_get files:final kopano-webapp-plugin-filesbackend-owncloud $outdir/kopano-webapp/packages
osc_get files:final kopano-webapp-plugin-filesbackend-smb $outdir/kopano-webapp/packages

osc_get mdm:final kopano-webapp-plugin-mdm $outdir/kopano-webapp/packages

osc_get smime:final kopano-webapp-plugin-smime $outdir/kopano-webapp/packages

# copying over dependencies from kopano core
deps="libgsoap-kopano-2-8 libkcutil0 libkcmapi0 libmapi1 libkcfreebusy0 libkcsoapclient0 libkcssl0 libkcsync0 kopano-lang kopano-client kopano-contacts libkcicalmapi0 libvmime-kopano0 libkcinetmapi0 php5-mapi"
echo "webapp dependencies - $outdir/kopano-webapp/packages"
for pkg in $deps; do
	find $outdir/kopano-core/packages -name "$pkg"*.deb -exec cp {} $outdir/kopano-webapp/packages \;
done

# copying over kopano4ucs dependencies
deps="kopano4ucs-lib kopano4ucs-webapp"
for pkg in $deps; do
  cp $outdir/kopano4ucs/"$pkg"*.deb $outdir/kopano-webapp/packages/
done

# webmeetings
osc_get kopano4ucs meetings4ucs $outdir/kopano-webmeetings/packages
osc_get kopano4ucs mod_proxy_wstunnel $outdir/kopano-webmeetings/packages
osc_get webmeetings:final kopano-webmeetings $outdir/kopano-webmeetings/packages
osc_get webmeetings:final kopano-webapp-plugin-meetings $outdir/kopano-webmeetings/packages

# z-push
osc_get z-push:pre-final z-push $outdir/z-push-kopano/packages

# remove source and other files
cd $outdir
outdirs="$outdir/kopano-core/packages $outdir/kopano-webapp/packages $outdir/meetings4ucs/packages $outdir/z-push-kopano/packages"
for finaldir in $(find . -mindepth 1 -maxdepth 1 -type d); do
	[[ $finaldir = ./kopano4ucs ]] && continue
	[[ $finaldir = ./.git ]] && continue
	if [ ! -e $(basename $finaldir).tar.gz ]; then
		#find $finaldir/packages -type f ! -name "*.deb" -delete
		tar --exclude='*.gz' --exclude='*.dsc' --exclude='*.changes' --exclude='_buildenv' --exclude='_statistics' \
		-czvf $(basename $finaldir).tar.gz $finaldir
	fi
done

