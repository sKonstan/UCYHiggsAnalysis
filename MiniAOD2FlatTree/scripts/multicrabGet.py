#!/usr/bin/env python
'''
Usage:
multicrabcreate.py [multicrab-dir-to-be-resubmitted]

Description:
This script is used retrieve output and check status of submitted multicrab jobs.

Launching the command requires the  multicrab-dir name to be checked to be passed 
as a parameter:
[username@lxplus0036:test]$ multicrabGet.py <multicrab_dir>

Links:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
'''
                                                                                                                                                                              
#================================================================================================ 
# Import Modules
#================================================================================================ 
import os
import re
import sys
import time
import subprocess
from optparse import OptionParser

# See: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRABClientLibraryAPI#The_crabCommand_API
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import setConsoleLogLevel

# See: https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/ClientUtilities.py
from CRABClient.ClientUtilities import LOGLEVEL_MUTE
from CRABClient.UserUtilities import getConsoleLogLevel

#================================================================================================ 
# Class Definition
#================================================================================================ 
class colors:
    # http://stackoverflow.com/questions/15580303/python-output-complex-line-with-floats-colored-by-value
    colordict = {
                'RED'     :'\033[91m',
                'GREEN'   :'\033[92m',
                'BLUE'    :'\033[34m',
                'GRAY'    :'\033[90m',
                'WHITE'   :'\033[00m',
                'ORANGE'  :'\033[33m',
                'CYAN'    :'\033[36m',
                'PURPLE'  :'\033[35m',
                'LIGHTRED':'\033[91m',
                'PINK'    :'\033[95m',
                'YELLOW'  :'\033[93m',
                }
    if sys.stdout.isatty():
        RED      = colordict['RED']
        GREEN    = colordict['GREEN']
        BLUE     = colordict['BLUE']
        GRAY     = colordict['GRAY']
        WHITE    = colordict['WHITE']
        ORANGE   = colordict['ORANGE']
        CYAN     = colordict['CYAN']
        PURPLE   = colordict['PURPLE']
        LIGHTRED = colordict['LIGHTRED']
        PINK     = colordict['PINK']
        YELLOW   = colordict['YELLOW']
    else:
        RED, GREEN, BLUE, GRAY, WHITE, ORANGE, CYAN, PURPLE, LIGHTRED, PINK, YELLOW = '', '', '', '', '', '', '', '', '', '', ''


class Report:
    '''
    '''
    def __init__(self, name, allJobs, retrieved, status, dashboardURL):
        '''
        Constructor 
        '''
        self.name         = name
        self.allJobs      = str(allJobs)
        self.retrieved    = str(retrieved)
        self.dataset      = self.name.split("/")[-1]
        self.dashboardURL = dashboardURL
        self.status       = self.GetTaskStatusStyle(status)
        return

    def Print(self):
        '''
        '''
        name = os.path.basename(self.name)
        while len(name) < 30:
            name += " "
            
        print "=== multicrabGet.py:"
        msg  = '{:<20} {:<40}'.format("\t %sDataset"           % (colors.WHITE) , ": " + self.dataset)
        msg += '\n {:<20} {:<40}'.format("\t %sRetrieved Jobs" % (colors.WHITE) , ": " + self.retrieved + " / " + self.allJobs)
        msg += '\n {:<20} {:<40}'.format("\t %sStatus"         % (colors.WHITE) , ": " + self.status)
        msg += '\n {:<20} {:<40}'.format("\t %sDashboard"      % (colors.WHITE) , ": " + self.dashboardURL)
        print msg
        return
    
    def GetTaskStatusStyle(self, status):
        '''
        NEW, RESUBMIT, KILL: Temporary statuses to indicate the action ('submit', 'resubmit' or 'kill') that has to be applied to the task.
        QUEUED: An action ('submit', 'resubmit' or 'kill') affecting the task is queued in the CRAB3 system.
        SUBMITTED: The task was submitted to HTCondor as a DAG task. The DAG task is currently running.
        SUBMITFAILED: The 'submit' action has failed (CRAB3 was unable to create a DAG task).
        FAILED: The DAG task completed all nodes and at least one is a permanent failure.
        COMPLETED: All nodes have been completed
        KILLED: The user killed the task.
        KILLFAILED: The 'kill' action has failed.
        RESUBMITFAILED: The 'resubmit' action has failed.
        '''
        
        # Remove all whitespace characters (space, tab, newline, etc.)
        status = ''.join(status.split())
        if status == "NEW":
            status = "%s%s%s" % (colors.BLUE, status, colors.WHITE)
        elif status == "RESUBMIT":
            status = "%s%s%s" % (colors.BLUE, status, colors.WHITE)
        elif status == "QUEUED": 
            status = "%s%s%s" % (colors.GRAY, status, colors.WHITE)            
        elif status == "SUBMITTED":
            status = "%s%s%s" % (colors.BLUE, status, colors.WHITE)
        elif status == "SUBMITFAILED": 
            status = "%s%s%s" % (colors.RED, status, colors.WHITE)
        elif status == "FAILED": 
            status = "%s%s%s" % (colors.RED, status, colors.WHITE)
        elif status == "COMPLETED":
            status = "%s%s%s" % (colors.GREEN, status, colors.WHITE)
        elif status == "KILLED":
            status = "%s%s%s" % (colors.ORANGE, status, colors.WHITE)
        elif status == "KILLFAILED":
            status = "%s%s%s" % (colors.ORANGE, status, colors.WHITE)
        elif status == "RESUBMITFAILED": 
            status = "%s%s%s" % (colors.ORANGE, status, colors.WHITE)
        else:
            print "=== multicrabGet.py:\n\t WARNING! Unexpected task status \"%s\"" % (status)

        return status


#================================================================================================ 
# Function Definitions
#================================================================================================ 
def GetTaskStatusBool(datasetPath, verbose=False):
    '''
    Check the crab.log for the given task to determine the status.
    If the the string "Done" is found inside skip it.
    '''
    crabLog      = os.path.join(datasetPath,"crab.log")
    stringToGrep = "Done"
    cmd          = "grep '%s' %s" % (stringToGrep, crabLog)
    if os.system(cmd) == 0:
        if verbose:
            print "\t DONE! Skipping ..."
        return True 
    return False


def GetTaskDashboardURL(datasetPath, verbose=False):
    '''
    Call the "grep" command to look for the dashboard URL from the crab.log file 
    of a given dataset. It uses as input parameter the absolute path of the task dir (datasetPath)
    '''

    # Variable Declaration
    crabLog      = os.path.join(datasetPath, "crab.log")
    grepFile     = os.path.join(datasetPath, "grep.tmp")
    stringToGrep = "Dashboard monitoring URL"
    cmd          = "grep '%s' %s > %s" % (stringToGrep, crabLog, grepFile )
    dashboardURL = "UNKNOWN"

    # Execute the command
    if os.system(cmd) == 0:
        # Sanity check (file exists)
        if os.path.exists( grepFile ):
            results      = [i for i in open(grepFile, 'r').readlines()]
            dashboardURL = find_between( results[0], "URL:\t", "\n" )
            if verbose:
                print "=== multicrabGet.py:\n\t Removing temporary file \"%s\"" % (grepFile)
            os.system("rm -f %s " % (grepFile) )
        else:
            print "=== multicrabGet.py:\n\t ERROR! File \"grep.tmp\" not found! EXIT"
    else:
        dashboardURL = "UNDETERMINED"
        if verbose:
            print "=== multicrabGet.py:\n\t Could not execute command \"%s\"" % (cmd)
    return dashboardURL


def KillTask(task, verbose=False):
    ''' 
    Command to kill submitted tasks. The user must give the crab project 
    directory for the task he/she wants to kill.
    
    CRAB Commands:
    https://github.com/dmwm/CRABClient/tree/master/src/python/CRABClient/Commands
    
    crabCommand definition:
    https://github.com/dmwm/CRABClient/blob/be9eebfa41268e836fa186259ef3391f998c8fff/src/python/CRABAPI/RawCommand.py    

    kill (crabCommand) definition:
    https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/Commands/kill.py
    '''

    keystroke = raw_input("\t Press \"q\" to cancel, or any other key kill the CRAB task: ")
    if (keystroke) == "q":
        return
    else:
        print "\t crab kill %s" % (task)
        crabCommand('kill', dir = task)
        return


def GetTaskStatus(datasetPath, verbose=False):
    '''
    Call the "grep" command to look for the "Task status" from the crab.log file 
    of a given dataset. It uses as input parameter the absolute path of the task dir (datasetPath)
    '''

    # Variable Declaration
    crabLog      = os.path.join(datasetPath, "crab.log")
    grepFile     = os.path.join(datasetPath, "grep.tmp")
    stringToGrep = "Task status:"
    cmd          = "grep '%s' %s > %s" % (stringToGrep, crabLog, grepFile )
    status       = "UNKNOWN"

    # Execute the command
    if os.system(cmd) == 0:
        # Sanity check (file exists)
        if os.path.exists( grepFile ):
            results = [i for i in open(grepFile, 'r').readlines()]
            status  = find_between( results[-1], stringToGrep, "\n" )
            if verbose:
                print "=== multicrabGet.py:\n\t Removing temporary file \"%s\"" % (grepFile)
            os.system("rm -f %s " % (grepFile) )
        else:
            print "=== multicrabGet.py:\n\t ERROR! File \"grep.tmp\" not found! EXIT"
    else:
        status = "UNDETERMINED"
        if verbose:
            print "=== multicrabGet.py:\n\t Could not execute command \"%s\"" % (cmd)
    return status



def GetTaskReports(datasetPath, status, dashboardURL, verbose=False):
    '''
    '''
    # Variable Declaration
    reports = []
    
    # Get all files under <dataset_dir>/results/
    files = execute("ls %s" % os.path.join( datasetPath, "results") )

    try:
        if verbose:
            print "\t Executing \"crab status\" command"

        # Execute "crab status --dir=d"
        result = crabCommand('status', dir = datasetPath)

        # Assess JOB success/failure for task
        finished, failed, retrievedLog, retrievedOut = retrievedFiles(datasetPath, result, False)

        # Proceed according to the job status
        if retrievedLog < finished:
            print "=== multicrabGet.py:\n\t Retrieved logs (%s) < finished (%s). Executing CRAB command 'getlog'." % (retrievedLog, finished)
            touch(datasetPath)
            dummy = crabCommand('getlog', dir = datasetPath) #xenios

        if retrievedOut < finished:
            print "=== multicrabGet.py:\n\t Retrieved output (%s) < finished (%s). Executing CRAB command 'getlog'." % (retrievedOut, finished)
            dummy = crabCommand('getoutput', dir = datasetPath) #xenios
            touch(datasetPath)

        if failed > 0:
            print "=== multicrabGet.py:\n\t Found \"Failed\" jobs for task \"%s\".\n\t Executing CRAB command 'resubmit'" % ( os.path.basename(datasetPath), datasetPath )
            dummy = crabCommand('resubmit', dir = datasetPath)

        # Assess JOB success/failure for task (again)
        finished, failed, retrievedLog, retrievedOut = retrievedFiles(datasetPath, result, True)
        retrieved = min(finished, retrievedLog, retrievedOut)
        alljobs   = len(result['jobList'])
            
        # Append the report
        reports.append( Report(datasetPath, alljobs, retrieved, status, dashboardURL) )

        # Determine if task is DONE or not
        if retrieved == alljobs and retrieved > 0:
            absolutePath = os.path.join(datasetPath, "crab.log")
            os.system("sed -i -e '$a\DONE! (Written by multicrabGet.py)' %s" % absolutePath )

    # Catch exceptions (Errors detected during execution which may not be "fatal")
    except: #if 0:
        msg = sys.exc_info()[1]
        reports.append( Report(datasetPath, "?", "?", "?", dashboardURL) )
        print "\t The \"crab status\" command failed with exception \"%s\"" % ( msg )
        if verbose:
            print "\t Re-executing \"crab status\" command, this time with full verbosity"
            setConsoleLogLevel(1)
            res = crabCommand('status', dir = datasetPath)

    return reports


def find_between(myString, first, last ):
    '''
    '''
    try:
        start = myString.index( first ) + len( first )
        end   = myString.index( last, start )
        return myString[start:end]
    except ValueError:
        return ""


def find_between_r(myString, first, last ):
    '''
    '''
    try:
        start = myString.rindex( first ) + len( first )
        end   = myString.rindex( last, start )
        return myString[start:end]
    except ValueError:
        return ""


def usage():
    '''
    Informs user of how the script must be used.
    '''
    print "=== multicrabGet.py:\n\t Usage: ", os.path.basename(sys.argv[0]), " <multicrab dir>"
    sys.exit()
    

def GetMulticrabAbsolutePaths(dirs):
    '''
    '''
    datasetdirs = []
    # For-loop: All multiCRAB dirs (relative paths)
    for d in dirs:
        # Get absolute paths
        if os.path.exists(d) and os.path.isdir(d):
            datasetdirs.append( os.path.abspath(d) )

    if len(dirs) == 0:
        datasetdirs.append(os.path.abspath("."))
    return datasetdirs


def GetDatasetAbsolutePaths(datasetdirs):
    '''
    '''
    datasets = []
    # For-loop: All multiCRAB dirs (absolute paths)
    for d in datasetdirs:
        # Check that results directory exists
        if os.path.exists( os.path.join(d, "results") ):
            datasets.append(d)

        # Get the contents of this directory
        cands = execute("ls -tr %s"%d)
        # For-loop: All directory contents
        for c in cands:
            path = os.path.join(d, c)
            # Get all dataset directories 
            if os.path.exists( os.path.join(path, "results") ):
                datasets.append(path)
    return datasets


#================================================================================================
# Main Program
#================================================================================================
def main(opts, args):

    # Options
    bDebug = False

    # If you want crabCommand to be quiet:
    if not bDebug:
        setConsoleLogLevel(LOGLEVEL_MUTE)

    # Retrieve the current crabCommand console log level:
    crabConsoleLogLevel = getConsoleLogLevel()
    if bDebug:
        print "=== multicrabGet.py:\n\t The current \"crabCommand\" console log level is set to \"%s\"" % (crabConsoleLogLevel)
    
    # Ensure script is called with at least one argument (apart from script name)
    if len(sys.argv) == 1:
        scriptName = sys.argv[0] 
        usage()

    # Get the multiCRAB dir(s) name (passed as argument)
    dirs = sys.argv[1:]

    # Initialise Variables
    reports      = []
    datasetdirs  = GetMulticrabAbsolutePaths(dirs)
    datasets     = GetDatasetAbsolutePaths(datasetdirs)

    if bDebug:
        print "=== multicrabGet.py:\n\t Found \"%s\" CRAB task directories:" % ( len(datasets) )     
        for d in datasets:
            print "\t\t \"%s\"" % ( os.path.basename(d) )

    # For-loop: All dataset directories (absolute paths)
    for index, d in enumerate(datasets):
        lastTwoDirs = d.split("/")[-2]+ "/" + d.split("/")[-1]
        print "=== multicrabGet.py:\n\t %s (%s/%s)" % ( lastTwoDirs, index+1, len(datasets) )

        # Kill Mode
        if opts.kill:
            KillTask(lastTwoDirs)
        else:
            # Check if task is in "DONE" state
            if GetTaskStatusBool(d, True):
                continue

            # Get task dashboard URL
            taskDashboard = GetTaskDashboardURL(d)

            # Get task status
            taskStatus = GetTaskStatus(d) 

            # Get the reports
            reports += GetTaskReports(d, taskStatus, taskDashboard)

    # For-loop: All CRAB reports
    if bDebug:
        for r in reports:
            r.Print()
        
    return


def retrievedFiles(directory, crabResults, verbose=False):
    '''
    Determines whether the jobs Finished (Success or Failure), and whether 
    the logs and output files have been retrieved. Returns all these in form
    of lists
    '''
    # Initialise variables
    retrievedLog = 0
    retrievedOut = 0
    finished     = 0
    failed       = 0
    transferring = 0
    running      = 0
    idle         = 0
    unknown      = 0
    dataset      = directory.split("/")[-1]
    nJobs        = len(crabResults['jobList'])

    # For-loop:All CRAB results
    for index, r in enumerate(crabResults['jobList']):
        
        # The comma at the end of the print statement tells it not to go to the next line.
        if verbose:
            progress = "\r\t %s Jobs" % (index+1)
            print '{0}\r'.format(progress),
            
        # Assess the jobs status individually
        if r[0] == 'finished':
            finished += 1
            foundLog  = exists(directory, "cmsRun_%i.log.tar.gz" % r[1])
            foundOut  = exists(directory, "*_%i.root" % r[1])
            if foundLog:
                retrievedLog += 1
            if foundOut:
                retrievedOut += 1
        elif r[0] == 'failed':
            failed += 1
        elif r[0] == 'transferring':
            transferring += 1 
        elif r[0] == 'idle':
            idle += 1 
        elif r[0] == 'running':
            running+= 1 
        else:
            unknown+= 1 
        
    # Print results in a nice table
    if verbose:

        # To avoid overwriting previous print statement
        print
        
        # Summarise information
        nTotal    = str(nJobs)
        nRun      = str(running)
        nTransfer = str(transferring)
        nFinish   = str(finished)
        nUnknown  = str(unknown)
        nFail     = str(failed)
        nIdle     = str(idle)
        nLogs     = ''.join( str(retrievedLog).split() ) 
        nOut      = ''.join( str(retrievedOut).split() )

        line  = "   {:<25} {:>4} {:<1} {:<4}".format("\t %sIdle"             % (colors.GRAY  ), nIdle    , "/", nTotal )
        line += "\n {:<25} {:>4} {:<1} {:<4}".format("\t %sUnknown"          % (colors.YELLOW), nUnknown , "/", nTotal )
        line += "\n {:<25} {:>4} {:<1} {:<4}".format("\t %sFailed"           % (colors.RED   ), nFail    , "/", nTotal )
        line += "\n {:<25} {:>4} {:<1} {:<4}".format("\t %sRunning"          % (colors.GREEN ), nRun     , "/", nTotal )
        line += "\n {:<25} {:>4} {:<1} {:<4}".format("\t %sTransferring"     % (colors.ORANGE), nTransfer, "/", nTotal )
        line += "\n {:<25} {:>4} {:<1} {:<4}".format("\t %sDone"             % (colors.WHITE ), nFinish  , "/", nTotal )
        line += "\n {:<25} {:>4} {:<1} {:<4}".format("\t %sRetrieved Logs"   % (colors.PURPLE), nLogs    , "/", nTotal )
        line += "\n {:<25} {:>4} {:<1} {:<4}".format("\t %sRetrieved Outputs"% (colors.BLUE  ), nOut     , "/", nTotal )
        line += "\n {:<25} {:>4} {:<1} {:<4}".format("\t %s"                 % (colors.WHITE ), ""       , "" , ""     )
        
        #print "=== multicrabGet.py:\n\t Printing summary for task \"%s\"" % ( dataset )
        print line

    return finished, failed, retrievedLog, retrievedOut


def exists(dataset,filename):
    '''
    '''
    fname = os.path.join(dataset,"results",filename)
    fname = execute("ls %s"%fname)[0]
    return os.path.exists(fname)


def touch(path):
    '''
    The "touch" command is the easiest way to create new, empty files. 
    It is also used to change the timestamps (i.e., dates and times of the most recent access and modification)
    on existing files and directories.
    '''
    if os.path.exists(path):
        os.system("touch %s" % path)
    return


def execute(cmd):
    '''
    '''
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (s_in, s_out) = (p.stdin, p.stdout)
        
    f = s_out
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
        
    f.close()
    return ret

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
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Verbose mode")
    parser.add_option("--kill", dest="kill"   , default=False, action="store_true", help="Kill moode")
    (opts, args) = parser.parse_args()
    
    sys.exit( main(opts, args) )
