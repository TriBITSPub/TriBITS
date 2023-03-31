#!/bin/sh
#
# Run from the base TriBITS git repo clone to install local git hooks
#
#   $ cd TriBITS/
#   $ ./commont_tools/git/client-side/copy_hooks_scripts.sh
#

if [[ ! -d .git ]] ; then
  echo "Error, must be a base git repo with subdir .git/!"
  exit 1
fi

_SCRIPT_DIR=`echo $0 | sed "s/\(.*\)\/copy_hooks_scripts.sh/\1/g"`

function copy_hook_script {
  orig_file="$_SCRIPT_DIR/$1"
  dest_file=".git/hooks/$1"
  
  if diff ${orig_file} ${dest_file} &> /dev/null ; then
    :
  else
    echo "Copy local git hook script: $1"
    cp "${orig_file}" "${dest_file}"
  fi
}

#echo "_SCRIPT_DIR = '$_SCRIPT_DIR'"

copy_hook_script commit-msg

