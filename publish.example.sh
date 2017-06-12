#!/bin/bash
#

make publish

find ./output/ -not \( -path output/en -prune \) -not \( -path output/zht -prune \) -iname '*-zht.*'| xargs /bin/rm -f
find ./output/ -not \( -path output/en -prune \) -not \( -path output/zht -prune \) -iname '*-en.*'| xargs /bin/rm -f
find ./output/en/ -iname '*-zht.*' | xargs /bin/rm -f
find ./output/en/ -iname '*-zh.*' | xargs /bin/rm -f
find ./output/zht/ -iname '*-zh.*' | xargs /bin/rm -f
find ./output/zht/ -iname '*-en.*' | xargs /bin/rm -f

a=($(diff -r ./output/ /path/to/a/output/ | grep -a '^diff -r ./output/' | grep '^diff -r ./output/' | cut -d ' ' -f 3))
b=($(diff -r ./output/ /path/to/a/output/ | grep -a '^diff -r ./output/' | grep '^diff -r ./output/' | cut -d ' ' -f 4))

if [ ${#a[@]} == ${#b[@]} ]; then
  for i in $(seq 0 $((${#a[@]} - 1)));do
    eval "cp -f ${a[$i]} ${b[$i]}"
    echo "cp -f ${a[$i]} ${b[$i]}"
  done
fi

tmpval="none"

function prepPath(){
  tmpval="none"
  local path="$1"
  if [ -e $path -a ! -d $path ]; then
    eval "path=\$(echo '$path' | sed 's/\/[^/]*$//')"
    eval "path=\$(echo '$path' | sed 's#^\./#/path/to/a/#')"
    if [ ! -e "$path" ]; then
      eval "mkdir -p '$path'"
      echo "mkdir -p '$path'"
    fi
    if [ -d "$path" ]; then
      tmpval="f"
    fi
  else
    tmpval="d"
  fi
}


a=($(diff -r ./output/ /path/to/a/output/ | grep -a '^Only in ./output' | grep '^Only in ./output' | awk -F 'Only in ./' '{printf $2"\n"}' | sed -e 's#/:\s#/#' -e 's#\([^/]\+\):\s#\1/#'))

for i in $(seq 0 $((${#a[@]} - 1)));do
  eval "prepPath '${a[$i]}'"
  eval "p0='./'${a[$i]}"
  eval "p1=\$(echo '$p0' | sed 's#^\./#/path/to/a/#')"
  if [ "$tmpval"x == "f"x ]; then
    eval "cp -f $p0 $p1"
    echo "cp -f $p0 $p1"
  elif [ "$tmpval"x == "d"x ]; then
    eval "p1=\$(echo '$p1' | sed 's/\/[^/]*$/\//')"
    eval "cp -fR $p0 $p1"
    echo "cp -fR $p0 $p1"
  fi
done

cp -f ./pelican-bootstrap3/static/css/bootstrap.min.css /path/to/a/output/theme/css/bootstrap.min.css
cp -fR ./output/images/* /path/to/a/output/images/


diff -r ./output/ /path/to/a/output/ | grep '^Only in /path/to/a/output' | sed -e 's/^Only\sin\s//' -e 's/:\s/\//' | xargs /bin/rm -rf

