#!/bin/bash
#

set -e

t=$(find /usr -path '*/docutils/parsers/rst/__init__.py' -exec grep 'tools\.ietf\.org' '{}' \; 2>/dev/null | wc -l)

if [ $t -lt 2 ]; then
  echo "The default rfc url is not under tools.ietf.org, abort!";
  exit 1;
fi

vernum=$(awk -F '.' '{printf $4+1}' ./content/rootpath/version)
verdate=$(date '+%Y.%m.%d')
echo -n ${verdate}.${vernum} > ./content/rootpath/version
#sed -i.bak -E "s/SITE_VERSION(\s*)=(\s*['\"])[\.0-9]*(')/SITE_VERSION\1=\2${verdate}.${vernum}\3/" ./pelicanconf_test.py
#sed -i.bak -E "s/SITE_VERSION(\s*)=(\s*['\"])[\.0-9]*(')/SITE_VERSION\1=\2${verdate}.${vernum}\3/" ./pelicanconf.py

make publish

# some fixes
cp ./content/fixes/set_proxy_for_gentoo_portage.html ./output/

rsync --delete -rlcv output/ ~/syncthingData/bitbili/output
