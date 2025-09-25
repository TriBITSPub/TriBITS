#!/bin/bash -e
#
# Install CMake from binary download:
#
#   instal-cmake-binary <cmake-version> <install-prefix-base>
#
# For example, running:
#
#   instal-cmake-binary 4.0.0-rc2  ${HOME}/install
#
# will download the install binary to:
#
#  /tmp/${USER}/
#
# and then install CMake from that binary to:
#
#  ${HOME}/install/cmake-4.0.0-rc2/
#
#  

# Input args
cmake_version=$1
install_prefix_base=$2

# Names and locations
cmake_download_url=https://github.com/Kitware/CMake/releases/download
CMAKE_BINARY_TMP_DIR=/tmp/${USER}
cmake_install_script_name=cmake-${cmake_version}-Linux-x86_64.sh
cmake_install_script=${CMAKE_BINARY_TMP_DIR}/${cmake_install_script_name}
cmake_install_dir=${install_prefix_base}/cmake-${cmake_version}

if [[ ! -d ${CMAKE_BINARY_TMP_DIR} ]] ; then
  echo
  echo "Creating temp dir ${CMAKE_BINARY_TMP_DIR}"
fi
  
echo
echo "Downloading ${cmake_install_script_name} to ${cmake_install_script} ..."
time wget -O ${cmake_install_script} \
  ${cmake_download_url}/v${cmake_version}/${cmake_install_script_name}
chmod a+x ${cmake_install_script}

if [[ ! -d ${cmake_install_dir} ]] ; then
  echo
  echo "Create install dir ${cmake_install_dir}"
  mkdir ${cmake_install_dir}
fi

echo
echo "Installing binary using ${cmake_install_script} ..."
time ${cmake_install_script} --skip-license --prefix=${cmake_install_dir} \
  --exclude-subdir

echo
echo "See the binaries installed under:"
echo
echo "    ${cmake_install_dir}/"
