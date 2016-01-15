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

# See: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRABClientLibraryAPI#The_crabCommand_API
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import setConsoleLogLevel

# See: https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/ClientUtilities.py
from CRABClient.ClientUtilities import LOGLEVEL_MUTE
from CRABClient.UserUtilities import getConsoleLogLevel

#================================================================================================ 
# Class Definition
#================================================================================================ 
class Report:
    '''
    '''
    def __init__(self, name, allJobs, retrieved, dashboardURL):
        '''
        Constructor 
        '''
        self.name         = name
        self.allJobs      = str(allJobs)
        self.retrieved    = str(retrieved)
        self.dataset      = self.name.split("/")[-1]
        self.progress     = "UNKNOWN"
        self.dashboardURL = dashboardURL
        nPending          = -1

        if type(allJobs)!=str and type(retrieved)!=str:
            nPending = allJobs-retrieved

        if allJobs == 0:
            self.progress  = "NOT SUBMITTED"
        elif nPending == 0:
            self.progress = "DONE"
        else:
            self.progress = "PENDING"
        return


    def Print(self):
        '''
        '''
        name = os.path.basename(self.name)
        while len(name) < 30:
            name += " "
            
        print "=== multicrabGet.py:"
        msg  = '{:<20} {:<40}'.format("\t Dataset"          , ": " + self.dataset)
        msg += '\n {:<20} {:<40}'.format("\t Retrieved Jobs", ": " + self.retrieved + " / " + self.allJobs)
        msg += '\n {:<20} {:<40}'.format("\t Dashboard"     , ": " + self.dashboardURL)
        msg += '\n {:<20} {:<40}'.format("\t Progress"      , ": " + self.progress)
        print msg
        return


#================================================================================================ 
# Function Definitions
#================================================================================================ 
def GetTaskStatus(datasetPath, verbose=False):
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
        print "=== multicrabGet.py:\n\t Could not execute command \"%s\"" % (cmd)
    return dashboardURL


def GetTaskReports(datasetPath, dashboardURL, verbose=False):
    '''
    '''
    # Variable Declaration
    reports = []
    
    # Get all files under <dataset_dir>/results/
    files = execute("ls %s" % os.path.join( datasetPath, "results") )

    try:
        if verbose:
            print "=== multicrabGet.py:\n\t Executing \"crab status\" for task \"%s\"" % ( os.path.basename(datasetPath) )

        # Execute "crab status --dir=d"
        result = crabCommand('status', dir = datasetPath)

        # Assess JOB success/failure for task
        finished, failed, retrievedLog, retrievedOut = retrievedFiles(datasetPath, result)

        # Proceed according to the job status
        if retrievedLog < finished:
            touch(datasetPath)
            dummy = crabCommand('getlog', dir = datasetPath)

        if retrievedOut < finished:
            dummy = crabCommand('getoutput', dir = datasetPath)
            touch(datasetPath)

        if failed > 0:
            print "=== multicrabGet.py:\n\t Executing \"crab status\" for task \"%s\"" % ( os.path.basename(datasetPath) )
            dummy = crabCommand('resubmit', dir = datasetPath)

        # Assess JOB success/failure for task (again)
        finished, failed, retrievedLog, retrievedOut = retrievedFiles(datasetPath, result, False)
        retrieved = min(finished, retrievedLog, retrievedOut)
        alljobs   = len(res['jobList'])
            
        # Append the report
        reports.append( Report(datasetPath, alljobs, retrieved, dashboardURL) )

        # Determine if task is DONE or not
        if retrieved == alljobs and retrieved > 0:
            absolutePath = os.path.join(datasetPath, "crab.log")
            os.system("sed -i -e '$a\DONE! (Written by multicrabGet.py)' %s" % absolutePath )

    # Catch exceptions (Errors detected during execution which may not be "fatal")
    except:
        exceptionType = sys.exc_info()[1]
        reports.append( Report(datasetPath, "?", "?", dashboardURL) )
        print "=== multicrabGet.py:\n\t The \"crab status\" failed for task \"%s\" with exception \"%s\". \n\t Skipping ..." % ( os.path.basename(datasetPath), exceptionType )
        if verbose:
            print "=== multicrabGet.py:\n\t Re-executing \"crab status\" command for taask with full verbosity" % ( os.path.basename(datasetPath) )
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


def main():
    '''
    Do all steps here
    '''

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
    datasetdirs  = GetMulticrabAbsolutePaths(dirs)
    datasets     = GetDatasetAbsolutePaths(datasetdirs)
    reports      = []
    dashboardURL = "UNKNOWN"

    print "=== multicrabGet.py:\n\t Found \"%s\" CRAB task directories:" % ( len(datasets) )     
    for d in datasets:
        print "\t\t \"%s\"" % ( os.path.basename(d) )

    # For-loop: All dataset directories (absolute paths)
    for index, d in enumerate(datasets):
        print "=== multicrabGet.py:\n\t \"%s\" (%s/%s)" % ( os.path.basename(d), index+1, len(datasets) )

        # Check if task is in "DONE" state
        if GetTaskStatus(d, True):            
            continue

        # Get task dashboard URL
        dashboard = GetTaskDashboardURL(d)
        
        # Get the reports
        reports = GetTaskReports(d, dashboardURL)
    
    # For-loop: All CRAB reports (for given dataset)
    for r in reports:
        r.Print()

    sys.exit()
    return


def retrievedFiles(directory, crabResults, verbose=True):
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
    idle         = 0
    dataset      = directory.split("/")[-1]
    nJobs        = len(crabResults['jobList'])

    if verbose:
        print "=== multicrabGet.py:"

    # For-loop:All CRAB results
    for iJob, r in enumerate(crabResults['jobList']):
        
        # The comma at the end of the print statement tells it not to go to the next line.
        if verbose:
            #progress = "\r\t \"%s\" Proceesed JOBS: %s / %s)" % (dataset, iJob, nJobs-1)
            progress = "\r\t Assessing jobs for task \"%s\" (%s / %s)" % (dataset, iJob, nJobs-1)
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
        if r[0] == 'failed':
            failed += 1
        if r[0] == 'transferring':
            transferring += 1 
        if r[0] == 'idle':
            idle += 1 
            
    if verbose:
        print "\n"
        
    # Print results in a nice table
    if verbose:
        summary = []
        summary.append("\t " + str(finished))
        summary.append("\t " + str(failed))
        summary.append("\t " + str(transferring))
        summary.append("\t " + str(idle))
        summary.append("\t " + str(retrievedLog))
        summary.append("\t " + str(retrievedOut))
        
        line  = '{:<20} {:<1} {:<5} {:>5}'.format("\t Finished"            , ":", summary[0], " / " + str(nJobs) )
        line += "\n {:<20} {:<1} {:<5} {:>5}".format("\t Failed"           , ":", summary[1], " / " + str(nJobs) )
        line += "\n {:<20} {:<1} {:<5} {:>5}".format("\t Transferring"     , ":", summary[2], " / " + str(nJobs) )
        line += "\n {:<20} {:<1} {:<5} {:>5}".format("\t Idle        "     , ":", summary[3], " / " + str(nJobs) )
        line += "\n {:<20} {:<1} {:<5} {:>5}".format("\t Retrieved Logs"   , ":", summary[4], " / " + str(nJobs) )
        line += "\n {:<20} {:<1} {:<5} {:>5}".format("\t Retrieved Outputs", ":", summary[5], " / " + str(nJobs) )

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
    main()
