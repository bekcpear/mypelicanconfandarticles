#!/bin/bash
#

t=$(find /usr -path '*/docutils/parsers/rst/__init__.py' -exec grep 'tools\.ietf\.org' '{}' \; 2>/dev/null | wc -l)

if [ "$t"x != 2x ]; then
  echo "The default rfc url is not under tools.ietf.org, abort!";
  exit 1;
fi

vernum=$(awk -F '.' '{printf $4+1}' ./version)
verdate=$(date '+%Y.%m.%d')
echo -n ${verdate}.${vernum} > ./version
sed -i.bak -e "s/MIGVERSION\s=\s'[\.0-9]*'/MIGVERSION = '${verdate}.${vernum}'/" ./pelicanconf-t.py
sed -i.bak -e "s/MIGVERSION\s=\s'[\.0-9]*'/MIGVERSION = '${verdate}.${vernum}'/" ./pelicanconf.py

make publish

rsync -acv ./sw-precache-config.js ./output/
rsync -acv ./service-worker-min.tmpl ./output/
rsync -acv ./keybase.txt ./output/
rsync -acv ./content/static/count.js ./output/
rsync -acv ./content/static/robots.txt ./output/
rsync -acv ./version ./output/version.txt

pushd ./output/
rm -f theme/css/*.scss
../node_modules/.bin/sw-precache --config sw-precache-config.js
popd

rsync --delete -acv output/ ~/Nextcloud/bitbili/output/
