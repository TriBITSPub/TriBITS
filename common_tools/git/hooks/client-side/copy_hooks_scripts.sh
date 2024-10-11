#!/bin/sh
#
# Run from a base git repo clone to install local git hooks
#
# For example:
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
  hook_file_name=$1
  orig_file="$_SCRIPT_DIR/${hook_file_name}"
  dest_file=".git/hooks/${hook_file_name}"
  
  if diff ${orig_file} ${dest_file} &> /dev/null ; then
    echo "NOTE: Local git hook script is same as installed: ${hook_file_name}"
  else
    echo "Copy local git hook script: ${hook_file_name}"
    cp "${orig_file}" "${dest_file}"
  fi
}

#echo "_SCRIPT_DIR = '$_SCRIPT_DIR'"

copy_hook_script commit-msg

