#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re


# Define regexes for matches

commandCallRegex = \
  re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*[\s]*\(', re.DOTALL)
macroDefRegex = \
  re.compile(r'[mM][aA][cC][rR][oO][\s]*\([\s]*[a-zA-Z_][a-zA-Z0-9_]*', re.DOTALL)
functionDefRegex = \
  re.compile(r'[fF][uU][nN][cC][tT][iI][oO][nN][\s]*\([\s]*[a-zA-Z_][a-zA-Z0-9_]*',
    re.DOTALL)
andLogicalRegex = re.compile(r'AND[\s]*\(', re.DOTALL)
orLogicalRegex = re.compile(r'OR[\s]*\(', re.DOTALL)
notLogicalRegex = re.compile(r'NOT[\s]*\(', re.DOTALL)


# Lower case CMake command calls and macro and function names.
#
def makeCmndsLowerCaseInCMakeStr(cmakeCodeStrIn):
  cmakeCodeStrOut = cmakeCodeStrIn
  cmakeCodeStrOut = makeRegexMatchesLowerCaseInCMakeStr(cmakeCodeStrOut,
    commandCallRegex)
  cmakeCodeStrOut = makeRegexMatchesLowerCaseInCMakeStr(cmakeCodeStrOut,
    macroDefRegex)
  cmakeCodeStrOut = makeRegexMatchesLowerCaseInCMakeStr(cmakeCodeStrOut,
    functionDefRegex)
  return cmakeCodeStrOut


# Make regex pattern matches lower cases.
#
def makeRegexMatchesLowerCaseInCMakeStr(cmakeCodeStrIn, regex):
  cmakeCodeStrOut = ""
  cmakeCodeStrInLen = len(cmakeCodeStrIn)
  cmakeCodeStrStartSearchIdx = 0
  while cmakeCodeStrStartSearchIdx < cmakeCodeStrInLen:
    m = regex.search(cmakeCodeStrIn[cmakeCodeStrStartSearchIdx:])
    if m:
      # Get the substr for the match
      cmakeCodeStrMatchStartIdx = cmakeCodeStrStartSearchIdx + m.start() 
      cmakeCodeStrMatchEndIdx = cmakeCodeStrStartSearchIdx + m.end() 
      commandCallMatchStr = \
        cmakeCodeStrIn[cmakeCodeStrMatchStartIdx:cmakeCodeStrMatchEndIdx]
      assert m.group() == commandCallMatchStr
      # Lower case the matching command call and update the output string
      # since last match
      cmakeCodeStrOut += \
        cmakeCodeStrIn[cmakeCodeStrStartSearchIdx:cmakeCodeStrMatchStartIdx]
      cmakeCodeStrOut += conditionalLowerCaseCMakeGroup(commandCallMatchStr)
      # Update indexes for next search
      cmakeCodeStrStartSearchIdx += m.end()
    else:
      # No more matches so copy the rest of the string
      cmakeCodeStrOut += \
        cmakeCodeStrIn[cmakeCodeStrStartSearchIdx:]
      break

  return cmakeCodeStrOut


def conditionalLowerCaseCMakeGroup(cmakeMatchGroup):
  if andLogicalRegex.match(cmakeMatchGroup) \
    or orLogicalRegex.match(cmakeMatchGroup) \
    or notLogicalRegex.match(cmakeMatchGroup) \
    :
    return cmakeMatchGroup
  return cmakeMatchGroup.lower()


#
# Helper functions for main()
#


usageHelp = r"""

Convert the cmake command calls to lower case and macro and function names
in defintions to lower case in a given file.
"""


def getCmndLineOptions():
  from argparse import ArgumentParser, RawDescriptionHelpFormatter
  clp = ArgumentParser(description=usageHelp,
    formatter_class=RawDescriptionHelpFormatter)
  clp.add_argument("file",
    help="The file to lower-case the CMake commands within." )
  options = clp.parse_args(sys.argv[1:])
  return options


def validateCmndLineOptions(inOptions):
  if not os.path.exists(inOptions.file):
    print("Error, the file '"+inOptions.file+"' does not exist!")
    sys.exit(1)


def lowerCaseCMakeCodeInFile(inOptions):
  with open(inOptions.file, 'r') as fileHandle:
    cmakeStrOrig = fileHandle.read()
  cmakeStrLowerCased = makeCmndsLowerCaseInCMakeStr(cmakeStrOrig)
  with open(inOptions.file, 'w') as fileHandle:
    fileHandle.write(cmakeStrLowerCased)

#
# main()
#


if __name__ == '__main__':
  inOptions = getCmndLineOptions()
  validateCmndLineOptions(inOptions)
  lowerCaseCMakeCodeInFile(inOptions)
