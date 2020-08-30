#!/bin/bash
#

t=$(find /usr -path '*/docutils/parsers/rst/__init__.py' -exec grep 'tools\.ietf\.org' '{}' \; | wc -l)

if [ "$t"x != 2x ]; then
  echo "The default rfc url is not under tools.ietf.org, abort!";
  exit 1;
fi

vernum=$(awk -F '.' '{printf $4+1}' ./moegoTheme/version)
verdate=$(date '+%Y.%m.%d')
echo -n ${verdate}.${vernum} > ./moegoTheme/version
sed -i.bak -e "s/THEMEVERSION\s=\s'[\.0-9]*'/THEMEVERSION = '${verdate}.${vernum}'/" ./pelicanconf-t.py
sed -i.bak -e "s/THEMEVERSION\s=\s'[\.0-9]*'/THEMEVERSION = '${verdate}.${vernum}'/" ./pelicanconf.py

make publish

cp -f ./sw-precache-config.js ./output/
cp -f ./service-worker.tmpl ./output/
cp -f ./keybase.txt ./output/
cp -f ./content/static/count.js ./output
cp -f ./content/static/robots.txt ./output

pushd ./output/
rm -f theme/css/*.scss
~/node_modules/.bin/sw-precache --config sw-precache-config.js
popd


cp -R output/* ~/Nextcloud/moego/output/
