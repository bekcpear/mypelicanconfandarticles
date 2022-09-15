#!/usr/bin/env bash
#

verfile=${1}
jsfile=${2}

echo "hash version ..."
md5sum=$(md5sum ${verfile} | cut -d' ' -f1)
echo "sed -Ei 's@/version@/version?s=${md5sum}@' '${jsfile}' ..."
eval "sed -Ei 's@/version@/version?s=${md5sum}@' '${jsfile}'"
