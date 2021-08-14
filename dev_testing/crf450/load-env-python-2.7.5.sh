# Env for testing TriBITS on crf450 using Python 2.7.5 (the default on RHEL-7)

module purge

export PATH=${PATH_ORIG}

# From ~/load_dev_env.sh

source ~/load_vera_dev_env.gcc-4.8.3.crf450.sh
module load sems-env
module load sems-git/2.10.1
module load sems-cmake/3.17.1
module load sems-ninja_fortran/1.10.0

# Extra stuff for TriBITS

#export PATH=/home/vera_env/common_tools/cmake-3.17.0/bin:${PATH}
export PATH=/home/vera_env/common_tools/ccache-3.7.9/bin:${PATH}

# Make default install permissions 700 so that we can test that TriBITS will
# use recursive chmod to open up permissions.
umask g-rwx,o-rwx

export TribitsExMetaProj_GIT_URL_REPO_BASE=git@github.com:tribits/
