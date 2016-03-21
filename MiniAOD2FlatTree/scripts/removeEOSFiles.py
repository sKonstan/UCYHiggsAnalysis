#!/usr/bin/env python
'''
Usage:
./removeEOSFiles.py --quota --promptUser --verbose 

Description:
This script is used to delete files and directories from EOS, most likely created
through a multi-CRAB job.

Links:
https://cern.service-now.com/service-portal/article.do?n=KB0001998
https://twiki.cern.ch/twiki/bin/view/EOS/UserHowTo
'''


#================================================================================================
# Import Modules
#================================================================================================
import os
import sys
import subprocess

from optparse import OptionParser

#================================================================================================
# Function Definitions
#================================================================================================
def Verbose(msg, printHeader=False):
    if not opts.verbose:
        return

    if printHeader:
        print "=== removeEOSFiles.py:"
    print "\t", msg
    return


def GetEosQuota(opts):

    csh_cmd = "eos quota | grep ^user -A1 -B2"
    Verbose(csh_cmd, True)

    p = subprocess.Popen(['/bin/csh', '-c', csh_cmd], stdout=subprocess.PIPE)

    # Use Popen with the communicate() method when you need pipes
    cmd_out, cmd_err = p.communicate()
    return cmd_out, cmd_err


def GetEosContentsList(path, opts):

    # Construct & Execute command
    cmd     = "eos ls"
    csh_cmd = cmd + " " + path
    Verbose(csh_cmd, True)

    # Execute shell command
    p = subprocess.Popen(['/bin/csh', '-c', csh_cmd], stdout=subprocess.PIPE)

    # Use Popen with the communicate() method when you need pipes
    cmd_out, cmd_err = p.communicate()

    # Convert string result to a list (of strings)
    fileList = cmd_out.split("\n")
    fileList.remove('')

    Verbose("Found %s files/dirs under %s:\n\t%s" % (len(fileList), path+"/","\n\t".join(fileList)), True)
    return fileList


def UserConfirm(fileOrDir):
    '''
    Prompts user for keystroke. Returns True if keystroke is "y", False otherwise
    '''
    keystroke = raw_input("\tDelete \"%s\" ? " % (fileOrDir) )
    if (keystroke) == "y":
        return True
    elif (keystroke) == "n":
        return False
    else:
        UserConfirm(fileOrDir)
    return


#================================================================================================
# Main Program
#================================================================================================
def main(opts, args):
    
    pathPrefix = "/store/user/"
    userName   = os.getenv("USER")
    eosPath    = os.path.join(pathPrefix, userName)
    fileList   = GetEosContentsList(eosPath, opts)

    if len(fileList) < 1:
        print "\tNothing to delete!"
        quota_out, quota_err = GetEosQuota(opts)
        print "\n", quota_out
        return     

    for l in fileList:
        # Construct command
        cmd     = "eos rm -r"
        path    = os.path.join(eosPath,l)
        csh_cmd = cmd + " " + path
        Verbose(csh_cmd, True)

        # Execute command
        if opts.promptUser:
            if UserConfirm(path):
                p = subprocess.Popen(['/bin/csh', '-c', csh_cmd], stdout=subprocess.PIPE)
            else:
                pass
        else:
            p = subprocess.Popen(['/bin/csh', '-c', csh_cmd], stdout=subprocess.PIPE)

    # Get EOS quota & print it
    quota_out, quota_err = GetEosQuota(opts)
    print 
    print quota_out

    return


if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html
                                                   
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-v", "--verbose"   , dest="verbose"   , default=False, action="store_true", help="Verbose mode")
    parser.add_option("-p", "--promptUser", dest="promptUser", default=False, action="store_true", help="Prompt user to delete specific file/dir or not")
    (opts, args) = parser.parse_args()
    
    sys.exit( main(opts, args) )
