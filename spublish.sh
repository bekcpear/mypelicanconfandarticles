#!/bin/bash
#

t=$(find /usr -path '*/docutils/parsers/rst/__init__.py' -exec grep 'tools\.ietf\.org' '{}' \; 2>/dev/null | wc -l)

if [ $t -lt 2 ]; then
  echo "The default rfc url is not under tools.ietf.org, abort!";
  exit 1;
fi

vernum=$(awk -F '.' '{printf $4+1}' ./version)
verdate=$(date '+%Y.%m.%d')
echo -n ${verdate}.${vernum} > ./version
sed -i.bak -e "s/MIGVERSION\s=\s'[\.0-9]*'/MIGVERSION = '${verdate}.${vernum}'/" ./pelicanconf-t.py
sed -i.bak -e "s/MIGVERSION\s=\s'[\.0-9]*'/MIGVERSION = '${verdate}.${vernum}'/" ./pelicanconf.py

make publish

rsync -rlcv ./sw-precache-config.js ./output/
rsync -rlcv ./service-worker-min.tmpl ./output/
rsync -rlcv ./keybase.txt ./output/
rsync -rlcv ./content/static/count.js ./output/
rsync -rlcv ./content/static/robots.txt ./output/
rsync -rlcv ./content/static/BingSiteAuth.xml ./output/
rsync -rlcv ./version ./output/version.txt

# some fixes
rsync -rlcv ./content/fixes/set_proxy_for_gentoo_portage.html ./output/


pushd ./output/
rm -f theme/css/*.scss
../node_modules/.bin/sw-precache --config sw-precache-config.js
popd

rsync --delete -rlcv output/ ~/Nextcloud/bitbili/output/
