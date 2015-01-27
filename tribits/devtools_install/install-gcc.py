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

def_gccVersion = "4.8.3"

gccDefaultCheckoutCmnd = \
  "git clone https://github.com/TriBITSPub/devtools-gcc-"+def_gccVersion+"-base" \
  + " gcc-"+def_gccVersion+"-base" 

#
# Script code
#


from InstallProgramDriver import *
from GeneralScriptSupport import *


def addRpathToLink(specFileStrIn, rpath):
  specFileStrOut = ""
  linkLastLine = False
  for line in specFileStrIn.split('\n'):
    #print "line: "+line
    if linkLastLine:
      #print "Prepending rpath!"
      newLine = """%{!rpath:-rpath """+rpath+"""} """ + line
      linkLastLine = False
    else:
      newLine = line
    #print "newLine: "+newLine
    specFileStrOut += newLine + "\n"
    if line == "*link:":
      #print "*link: found!"
      linkLastLine = True
  return specFileStrOut


def appendToRPath(rpathIn, anotherPath):
  rpathOut = rpathIn
  if rpathIn:
    rpathOut += ";:"
  rpathOut += anotherPath
  return rpathOut


class GccInstall:

  def __init__(self):
    self.dummy = None

  def getProductName(self):
    return "gcc-"+def_gccVersion

  def getScriptName(self):
    return "install-gcc.py"

  def getExtraHelpStr(self):
    return """
This script builds gcc-"""+def_gccVersion+"""" (see other versions for --gcc-version)
rom source.

NOTE: The sources for GCC may be patched so be careful to get an approved version
(which the default pulled by --checkout-cmnd).
"""

  def getBaseDirName(self):
    return "gcc-"+def_gccVersion+"-base"

  def injectExtraCmndLineOptions(self, clp):
    clp.add_option(
      "--checkout-cmnd", dest="checkoutCmnd", type="string",
      default=gccDefaultCheckoutCmnd,
      help="Command used to checkout out the sources for "+self.getProductName() \
        +"  (Default ='"+gccDefaultCheckoutCmnd+"').  WARNING: This will delete" \
        +" an existing directory if it already exists!")
    clp.add_option(
      "--extra-configure-options", dest="extraConfigureOptions", type="string", default="",
      help="Extra options to add to the 'configure' command for "+self.getProductName()+"." \
      +"  Note: This does not override the hard-coded configure options." )
    clp.add_option(
      "--embed-rpath", dest="embedRPath", action="store_true", default=False,
      help="Update the GCC specs file with the rpaths to GCC shared libraries." )
    clp.add_option(
      "--gcc-version", dest="gccVersion", type="string", default=def_gccVersion,
      help="Select GCC version: 4.8.3. Default: " + def_gccVersion )
      
  def echoExtraCmndLineOptions(self, inOptions):
    cmndLine = ""
    cmndLine += "  --checkout-cmnd='"+inOptions.checkoutCmnd+"' \\\n"
    if inOptions.extraConfigureOptions:
      cmndLine += "  --extra-configure-options='"+inOptions.extraConfigureOptions+"' \\\n"
    return cmndLine

  def selectVersion(self):
    gccVersion = self.inOptions.gccVersion 
    if gccVersion == def_gccVersion:
      None
    else:
      print "\nUnsupported GCC version. See help."
      sys.exit(1)
    #
    print "\nSelecting: \n" \
          "  gcc: " + gccVersion + "\n"
    #  
    self.gccTarball = "gcc-"+gccVersion+".tar.gz"
    self.gccSrcDir = "gcc-"+gccVersion

  def setup(self, inOptions):

    self.inOptions = inOptions
    self.selectVersion()
    self.baseDir = os.getcwd()
    self.gccBaseDir = self.baseDir+"/"+self.getBaseDirName()
    self.gccSrcBaseDir = self.gccBaseDir+"/"+self.gccSrcDir
    self.gccBuildBaseDir = self.gccBaseDir+"/gcc-build"
    self.scriptBaseDir = getScriptBaseDir()

  def doCheckout(self):
    removeDirIfExists(self.getBaseDirName(), True)
    echoRunSysCmnd(self.inOptions.checkoutCmnd)

  def doUntar(self):
   print "Nothing to untar!"

  def doConfigure(self):
    createDir(self.gccBuildBaseDir)
    echoRunSysCmnd(
      "../"+self.gccSrcDir+"/configure --enable-languages='c,c++,fortran'"+\
      " "+self.inOptions.extraConfigureOptions+\
      " --prefix="+self.inOptions.installDir,
      workingDir=self.gccBuildBaseDir)

  def doBuild(self):
    echoChDir(self.gccBuildBaseDir)
    cmnd = "make"
    if self.inOptions.parallel > 0:
      cmnd += " -j"+str(self.inOptions.parallel)
    cmnd += " "+self.inOptions.makeOptions
    echoRunSysCmnd(cmnd)

  def doInstall(self):

    print "\nInstall GCC ...\n"
    echoChDir(self.gccBuildBaseDir)
    echoRunSysCmnd("make "+self.inOptions.makeOptions+" install")

    if self.inOptions.embedRPath:
      print "\nSet up rpath for GCC versions so that you don't need to set LD_LIBRARY_PATH ...\n"
      self.updateSpecsFile()

  def getFinalInstructions(self):
    return """
In order to use """+self.getProductName()+""" prepend

   """+self.inOptions.installDir+"""/bin

to your PATH env variable.

Also, you must prepend

   """+self.inOptions.installDir+"""/lib[64]

to your LD_LIBRARY_PATH env variable.
"""

  def updateSpecsFile(self):
    gccExec = self.inOptions.installDir+"/bin/gcc"
    rpathbase = self.inOptions.installDir
    print "rpathbase = "+rpathbase
    specpath = getCmndOutput(gccExec+" --print-file libgcc.a | sed 's|/libgcc.a||'", True)
    print "specpath = "+specpath
    rpath = ""
    libPath = rpathbase+"/lib"
    if os.path.exists(libPath):
      rpath = appendToRPath(rpath, libPath)
    lib64Path = rpathbase+"/lib64"
    if os.path.exists(lib64Path):
      rpath = appendToRPath(rpath, lib64Path)
    print "rpath will be: '"+rpath+"'"
    specsfile = specpath+"/specs"
    if os.path.exists(specsfile):
      print "Backing up the existing GCC specs file '"+specsfile+"' ..."
      echoRunSysCmnd("cp "+specsfile+" "+specsfile+".backup")
    print "Writing to GCC specs file "+specsfile
    gccSpecs = getCmndOutput(gccExec+" -dumpspecs", True)
    #print "gccSpecs:\n", gccSpecs
    gccSpecsMod = addRpathToLink(gccSpecs, rpath)
    #print "gccSpecsMod:\n", gccSpecsMod
    writeStrToFile(specsfile, gccSpecsMod)


#
# Executable statements
#

gitInstaller = InstallProgramDriver(GccInstall())

gitInstaller.runDriver()
