#!/bin/bash
#

t=$(find /usr -path '*/docutils/parsers/rst/__init__.py' -exec grep 'tools\.ietf\.org' '{}' \; | wc -l)

if [ "$t"x != 2x ]; then
  echo "The default rfc url is not under tools.ietf.org, abort!";
  exit 1;
fi

make publish

cp -f ./sw-precache-config.js ./output/
cp -f ./service-worker.tmpl ./output/
cp -f ./keybase.txt ./output/
cp -f ./content/static/count.js ./output

pushd ./output/
rm -f theme/css/*.map theme/css/*.scss
~/node_modules/.bin/sw-precache --config sw-precache-config.js

popd
