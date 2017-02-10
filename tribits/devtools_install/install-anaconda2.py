#!/usr/bin/env python
import os, sys, urllib2

# @HEADER
# ************************************************************************
#
#            TriBITS: Tribal Build, Integrate, and Test System
#                    Copyright 2013 Sandia Corporation
#
# Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
# the U.S. Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the Corporation nor the names of the
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SANDIA CORPORATION "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SANDIA CORPORATION OR THE
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ************************************************************************
# @HEADER


#
# Defaults
#

CONDA_BASE_NAME = 'anaconda2'
CONDA_DEFAULT_VERSION = '4.3.0'
CONDA_SUPPORTED_VERSIONS = [ '4.2.0', '4.3.0' ]
CONDA_INSTALLER_VERSIONS = { '4.2.0': '4.2.0', '4.3.0' : '4.3.0' }


#
# Script code
#


from InstallProgramDriver import *
from GeneralScriptSupport import *


class Anaconda2Install:

  def __init__( self ):
    pass

  #
  # Called before even knowing the product version
  #

  def getScriptName( self ):
    return "install-anaconda2.py"

  def getProductBaseName( self ):
    return CONDA_BASE_NAME

  def getProductDefaultVersion( self ):
    return CONDA_DEFAULT_VERSION

  def getProductSupportedVersions(self):
    return CONDA_SUPPORTED_VERSIONS

  #
  # Called after knowing the product version but before parsing the
  # command-line.
  #

  def getProductName(self, version):
    return CONDA_BASE_NAME + "-" + version

  def getBaseDirName(self, version):
    return CONDA_BASE_NAME + "-" + version + "-base"

  def getExtraHelpStr(self, version):
    return """
This script installs """ + self.getProductName(version) + """.
"""


  def injectExtraCmndLineOptions(self, clp, version):
    setStdDownloadCmndOption(self, clp, version)


  def echoExtraCmndLineOptions(self, inOptions):
    cmndLine = ""
    cmndLine += "  --download-cmnd='" + inOptions.downloadCmnd + "' \\\n"
    return cmndLine


  #
  # Called after parsing the command-line
  #
    
  def setup( self, in_options ):
    print >> sys.stderr, '[setup] in_options=', str( in_options )
    self.inOptions = in_options
    self.baseDir = os.getcwd()
    self.condaBaseDir = \
        self.baseDir + '/' + self.getBaseDirName( self.inOptions.version )
    full_version = CONDA_INSTALLER_VERSIONS[ self.inOptions.version ]

    self.condaInstallScript = 'Anaconda2-' + full_version + '-Linux-x86_64.sh'
    print >> sys.stderr, \
        '[setup]%s  baseDir=%s%s  condaBaseDir=%s%s  condaInstallScript=%s' % \
	( os.linesep, self.baseDir, os.linesep, self.condaBaseDir,
	  os.linesep, self.condaInstallScript )
    #self.anacondaTarball = 'cmake-' + cmakeVersionFull + '.tar.gz'
    #self.cmakeSrcDir = "cmake-"+cmakeVersionFull
    #self.cmakeBuildBaseDir = self.cmakeBaseDir+"/cmake-build"
    self.scriptBaseDir = getScriptBaseDir()


  #
  # Called after setup()
  #

  def doDownload( self ):
    removeDirIfExists( self.condaBaseDir, True )
    os.makedirs( self.condaBaseDir )

    download_url = self.inOptions.anaconda2UrlBase
    if not download_url.endswith( '/' ):
      download_url += '/'
    download_url += self.condaInstallScript

    url_fp = file_fp = None
    try:
      file_fp = file( os.path.join( targetToolSrcDir, fname ), 'wb' )
      url_fp = urllib2.urlopen( download_url )
      file_fp.write( url_fp.read() )
    finally:
      if file_fp: file_fp.close()
      if url_fp: url_fp.close()
  #end doDownload


  def doUntar( self ):
    pass


  def doConfigure( self ):
    pass


  def doBuild( self ):
    pass


  def doInstall( self ):
    print >> sys.stderr, '[doInstall] baseDir=', self.baseDir
    #echoChDir( self.baseDir )
    echoChDir( self.condaBaseDir )
    command = \
	'bash ' + \
	os.path.join( '.', self.condaInstallScript ) + \
	' -b -p ' + \
	self.inOptions.installDir
    print >> sys.stderr, '[doInstall] command="%s"' % command
    echoRunSysCmnd( command )


  def getFinalInstructions(self):
    return """
To use the installed version of anaconda2-""" + self.inOptions.version + """ add the path:

  """ + self.inOptions.installDir + """/bin

to your path and that should be it!
"""


#
# Executable statements
#

#anacondaInstaller = InstallProgramDriver( Anaconda2Install() )
#anacondaInstaller.runDriver()
InstallProgramDriver( Anaconda2Install() ).runDriver()
