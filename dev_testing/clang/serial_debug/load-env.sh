# Simple build and test with no coverage or anything
# Make sure that the clang env is loaded if not already
if [[ -e /home/runner/.bashrc ]] ; then
  source /home/runner/.bashrc
fi
export OMPI_CC=$(which clang)
export OMPI_CXX=$(which clang++)
#export OMPI_FC=$(which gfortran)
