#!/usr/bin/env python

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
# Version info that will change with new versions
#

mpichVersion = "3.1.3"

mpichSrcDir = "mpich-"+mpichVersion
mpichTarball = mpichSrcDir+".tar.gz"
mpichDefaultCheckoutCmnd = \
  "git clone https://github.com/TriBITSPub/devtools-mpich-"+mpichVersion+"-base" \
  + " mpich-"+mpichVersion+"-base" 

#
# Script code
#


from InstallProgramDriver import *
from GeneralScriptSupport import *


class MpichInstall:

  def __init__(self):
    self.dummy = None

  def getProductName(self):
    return "mpich-"+mpichVersion

  def getBaseDirName(self):
    return "mpich-"+mpichVersion+"-base"

  def getScriptName(self):
    return "install-mpich.py"

  def getExtraHelpStr(self):
    return """
This script builds MPICH """+self.getProductName()+""" from source compiled
with the configured C/C++ compilers in your path or set by the env vars CC and
CXX.

NOTE: The assumed directory structure of the download source provided by the
command --checkout-cmnd=<checkout-cmnd> is:

   mpich-<version>-base/
     mpich-<version>/

ToDo: Allow user to select different mpich versions.
"""

  def injectExtraCmndLineOptions(self, clp):
    clp.add_option(
      "--checkout-cmnd", dest="checkoutCmnd", type="string",
      default=mpichDefaultCheckoutCmnd,
      help="Command used to check out MPICH and dependent source." \
        +"  (Default ='"+mpichDefaultCheckoutCmnd+"')  WARNING: This will delete" \
        +" an existing directory if it already exists!")
    clp.add_option(
      "--extra-configure-options", dest="extraConfigureOptions", type="string", \
      default="", \
      help="Extra options to add to the 'configure' command for "+self.getProductName()+"." \
        +"  Note: This does not override the hard-coded configure options." )

  def echoExtraCmndLineOptions(self, inOptions):
    cmndLine = ""
    cmndLine += "  --checkout-cmnd='"+inOptions.checkoutCmnd+"' \\\n"
    cmndLine += "  --extra-configure-options='"+inOptions.extraConfigureOptions+"' \\\n"
    return cmndLine
    
  def setup(self, inOptions):
    self.inOptions = inOptions
    self.baseDir = os.getcwd()
    self.mpichBaseDir = self.baseDir+"/"+self.getBaseDirName()
    self.mpichSrcBaseDir = self.mpichBaseDir+"/"+mpichSrcDir
    self.mpichBuildBaseDir = self.mpichBaseDir+"/mpich-build"
    self.scriptBaseDir = getScriptBaseDir()

  def getParallelOpt(self, optName):
    if self.inOptions.parallel > 0:
      return " "+optName+str(self.inOptions.parallel)
    return " "

  def doCheckout(self):
    removeDirIfExists(self.getBaseDirName(), True)
    echoRunSysCmnd(self.inOptions.checkoutCmnd)

  def doUntar(self):
    echoChDir(self.mpichBaseDir)
    echoRunSysCmnd("tar -xzf "+mpichTarball)
    # NOTE: I found that you have to untar the tarball and can't store the
    # open source.  Otherwise the timestaps are messed up and it 'make' tries
    # to recreate some generated files.

  def doConfigure(self):
    createDir(self.mpichBuildBaseDir, True, True)
    echoRunSysCmnd(
      "../"+mpichSrcDir+"/configure " \
      +" "+self.inOptions.extraConfigureOptions \
      +" --prefix="+self.inOptions.installDir)

  def doBuild(self):
    echoChDir(self.mpichBuildBaseDir)
    echoRunSysCmnd("make "+self.getParallelOpt("-j")+self.inOptions.makeOptions)

  def doInstall(self):
    echoChDir(self.mpichBuildBaseDir)
    echoRunSysCmnd("make "+self.inOptions.makeOptions+" install")

  def getFinalInstructions(self):
    return """
In order to use """+self.getProductName()+""" prepend

   """+self.inOptions.installDir+"""/bin

to your PATH env variable.

Also, you must prepend

   """+self.inOptions.installDir+"""/lib[64]

to your LD_LIBRARY_PATH env variable.
"""


#
# Executable statements
#

mpichInstaller = InstallProgramDriver(MpichInstall())
mpichInstaller.runDriver()
