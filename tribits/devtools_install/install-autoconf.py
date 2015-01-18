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

autoconfVersion = "2.69"
autoconfVersionFull = "2.69"

autoconfTarball = "autoconf-"+autoconfVersionFull+".tar.gz"
autoconfSrcDir = "autoconf-"+autoconfVersionFull
autoconfDefaultCheckoutCmnd = \
  "git clone https://github.com/TriBITSPub/devtools-autoconf-"+autoconfVersion+"-base" \
  + " autoconf-"+autoconfVersion+"-base" 

#
# Script code
#


from InstallProgramDriver import *
from GeneralScriptSupport import *


class AutoconfInstall:

  def __init__(self):
    self.dummy = None

  def getProductName(self):
    return "autoconf-"+autoconfVersion

  def getBaseDirName(self):
    return "autoconf-"+autoconfVersion+"-base"

  def getScriptName(self):
    return "install-autoconf.py"

  def getExtraHelpStr(self):
    return """
The assumed directory structure of the download source provided by the
command --checkout-cmnd=<checkout-cmnd> is:

   autoconf-<version>-base/
     autoconf-<version>.tar.gz

ToDo: Allow user to select different autoconf versions.
"""

  def injectExtraCmndLineOptions(self, clp):
    clp.add_option(
      "--checkout-cmnd", dest="checkoutCmnd", type="string",
      default=autoconfDefaultCheckoutCmnd,
      help="Command used to check out Autoconf and dependent source." \
        +"  (Default ='"+autoconfDefaultCheckoutCmnd+"')  WARNING: This will delete" \
        +" an existing directory if it already exists!")
    clp.add_option(
      "--extra-configure-options", dest="extraConfigureOptions", type="string", \
      default="", \
      help="Extra options to add to the 'configure' command for "+self.getProductName()+"." \
        +"  Note: This does not override the hard-coded configure options." )

  def echoExtraCmndLineOptions(self, inOptions):
    cmndLine = ""
    cmndLine += "  --checkout-cmnd='"+inOptions.checkoutCmnd+"' \\\n"
    return cmndLine
    
  def setup(self, inOptions):
    self.inOptions = inOptions
    self.baseDir = os.getcwd()
    self.autoconfBaseDir = self.baseDir+"/"+self.getBaseDirName()
    self.autoconfSrcBaseDir = self.autoconfBaseDir+"/"+autoconfSrcDir
    self.autoconfBuildBaseDir = self.autoconfBaseDir+"/autoconf-build"
    self.scriptBaseDir = getScriptBaseDir()

  def getParallelOpt(self, optName):
    if self.inOptions.parallel > 0:
      return " "+optName+str(self.inOptions.parallel)
    return " "

  def doCheckout(self):
    removeDirIfExists(self.getBaseDirName(), True)
    echoRunSysCmnd(self.inOptions.checkoutCmnd)

  def doUntar(self):
    echoChDir(self.autoconfBaseDir)
    echoRunSysCmnd("tar -xzf "+autoconfTarball)

  def doConfigure(self):
    createDir(self.autoconfBuildBaseDir, True, True)
    echoRunSysCmnd(
      "../"+autoconfSrcDir+"/configure "+\
      " "+self.inOptions.extraConfigureOptions+\
      " --prefix="+self.inOptions.installDir)

  def doBuild(self):
    echoChDir(self.autoconfBuildBaseDir)
    echoRunSysCmnd("make "+self.getParallelOpt("-j")+self.inOptions.makeOptions)

  def doInstall(self):
    echoChDir(self.autoconfBuildBaseDir)
    echoRunSysCmnd("make "+self.inOptions.makeOptions+" install")

  def getFinalInstructions(self):
    return """
To use the installed version of autoconf-"""+autoconfVersion+""" add the path:

  """+self.inOptions.installDir+"""/bin

to your path and that should be it!
"""


#
# Executable statements
#

autoconfInstaller = InstallProgramDriver(AutoconfInstall())
autoconfInstaller.runDriver()
