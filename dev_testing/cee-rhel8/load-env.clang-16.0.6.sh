module purge
module load aue/cmake/3.27.7
module load aue/ninja/1.11.1
module load aue/clang/16.0.6
module load aue/openmpi/4.1.6-clang-16.0.6

export PATH=${HOME}/.local/bin:${PATH}
export TribitsExMetaProj_GIT_URL_REPO_BASE=git@github.com:tribits/
