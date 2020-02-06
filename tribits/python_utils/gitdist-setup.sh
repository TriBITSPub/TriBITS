# Assert this script is sourced, not run!
called=$_
if [ "$called" == "$0" ] ; then
  echo "This script '$0' is being called.  Instead, it must be sourced!"
  exit 1
fi

# Get the base dir for the sourced script
SCRIPT_DIR=`echo $BASH_SOURCE | sed "s/\(.*\)\/.*\.sh/\1/g"`
#echo "SCRIPT_DIR = '$SCRIPT_DIR'"

existing_gitdist=`which gitdist 2> /dev/null`
if [[ "${existing_gitdist}" == "" ]] ; then
  echo "Setting alias gitdist=${SCRIPT_DIR}/gitdist"
  alias gitdist=${SCRIPT_DIR}/gitdist
fi

function gitdist_repo_versions {
  gitdist "$@" --dist-no-color log -1 --pretty=format:"%h [%ad] <%ae>%n%s" | grep -v "^$"
}
export -f gitdist_repo_versions

function gitdist_show_full_repo_state {
  echo
  echo "Repo versions:"
  echo
  gitdist_repo_versions "$@"
  echo
  echo "Repo branch status:"
  echo
  gitdist-status "$@" | grep -v "^$" | grep -v "(tip: to see a legend"
  echo
  echo "Repo remotes:"
  echo
  gitdist --dist-no-color "$@" remote -v | grep "\(Git Repo\|push\)"
}
export -f gitdist_show_full_repo_state

# Source this with bash to load useful env for using gitdist
alias gitdist-status="gitdist dist-repo-status"
alias gitdist-mod="gitdist --dist-mod-only"
alias gitdist-mod-status="gitdist --dist-mod-only dist-repo-status"
alias gitdist-repo-versions=gitdist_repo_versions
alias gitdist-show-full-repo-state=gitdist_show_full_repo_state

# Setup for completions for git command and gitdist options commands
complete -o default -o nospace -F _git \
   -W "dist-repo-status --dist-help --dist-use-git --dist-repos --dist-not-repos --dist-version-file --dist-version-file2 --dist-no-color --dist-debug --dist-no-opt --dist-mod-only --dist-legend" \
   gitdist gitdist-mod
complete -o default -o nospace \
   -W "--dist-use-git --dist-repos --dist-not-repos --dist-mod-only" \
   gitdist_repo_versions gitdist-repo-versions
complete -o default -o nospace \
   -W "--dist-use-git --dist-repos --dist-not-repos --dist-mod-only" \
   gitdist_show_full_repo_state gitdist-show-full-repo-state
complete -o default -o nospace \
   -W "--dist-repos --dist-not-repos --dist-mod-only" \
   gitdist-status
