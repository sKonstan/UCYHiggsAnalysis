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

from CRABAPI.RawCommand import crabCommand


#================================================================================================ 
# Function Definitions
#================================================================================================ 
def usage():
    '''
    Informs user of how the script must be used.
    '''
    print "=== multicrabGet.py:\n\t Usage: ", os.path.basename(sys.argv[0]), " <multicrab dir>"
    sys.exit()


def main():
    '''
    '''
    # Ensure script is called with at least one argument (apart from script name)
    if len(sys.argv) == 1:
        scriptName = sys.argv[0] 
        usage()

    # Get the multiCRAB dir(s) name (passed as argument)
    dirs = sys.argv[1:]

    datasetdirs = []
    # For-loop: All multiCRAB dirs (relative paths)
    for d in dirs:
        # Get absolute paths
        if os.path.exists(d) and os.path.isdir(d):
            datasetdirs.append( os.path.abspath(d) )
    if len(dirs) == 0:
        datasetdirs.append(os.path.abspath("."))

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

    class Report:
        '''
        '''
        def __init__(self, name, all, retrieved):
            '''
            Constructor 
            '''
            self.name      = name
            self.all       = str(all)
            self.retrieved = str(retrieved)
            self.dataset   = self.name.split("/")[-1]
            self.progress  = "UNKNOWN"
            
            nPending = all-retrieved
            if all == 0:
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
            
            print "===multicrabGet.py:"
            msg  = '{:<20} {:<40}'.format("\t Dataset"          , ": " + self.dataset)
            msg += '\n {:<20} {:<40}'.format("\t Retrieved Jobs", ": " + self.retrieved)
            msg += '\n {:<20} {:<40}'.format("\t All Jobs"      , ": " + self.all)
            msg += '\n {:<20} {:<40}'.format("\t Progress"      , ": " + self.progress)
            print msg
            return

    reports = []

    print "=== multicrabGet.py:\n\t Found \"%s\" CRAB task directories:" % ( len(datasets) ) 
    for d in datasets:
        print "\t \"%s\"" % ( os.path.basename(d) )

    # xenios
    #del datasets[0]
    #del datasets[0]

    # For-loop: All dataset directories (absolute paths)
    for d in datasets:
        # print "=== multicrabGet.py:\n\t Checking crab.log to determine status for task \"%s\"" % ( os.path.basename(d) )

        # If Done in the crab.log, skip.
        if os.system("grep Done %s" % os.path.join(d,"crab.log")) == 0:
            print "\t DONE! Skipping ..."
            continue

        # Get all files under <dataset_dir>/results/
        files = execute("ls %s" % os.path.join( d, "results") )

        try:
            print "=== multicrabGet.py:\n\t Executing \"crab status\" for task \"%s\"" % ( os.path.basename(d) )
            res = crabCommand('status', dir = d)

            # Assess JOB success/failure for task
            finished, failed, retrievedLog, retrievedOut = retrievedFiles(d, res)

            # Proceed according to the job status
            if retrievedLog < finished:
                touch(d)
                dummy=crabCommand('getlog', dir = d)

            if retrievedOut < finished:
                dummy=crabCommand('getoutput', dir = d)
                touch(d)

            if failed > 0:
                dummy=crabCommand('resubmit', dir = d)

            # Assess JOB success/failure for task
            finished, failed, retrievedLog, retrievedOut = retrievedFiles(d, res, False)
            retrieved = min(finished, retrievedLog, retrievedOut)
            alljobs   = len(res['jobList'])

            reports.append( Report(d, alljobs, retrieved) )

            # Determine if task is DONE or not
            if retrieved == alljobs and retrieved > 0:
                absolutePath = os.path.join(d,"crab.log")
                os.system("sed -i -e '$a\DONE! (Written by multicrabGet.py)' %s" % absolutePath )
                # relativePath = os.path.join(d.split("/")[-2] + "/" + d.split("/")[-1] + "/" + "crab.log")
                # print "=== multicrabGet.py:\n\t Task \"%s\" is DONE!" % ( os.path.basename(d) )

        except:
            reports.append( Report(d, "?", "?") )
            print "=== multicrabGet.py:\n\t The \"crab status\" command failed for task \"%s\"!\n\t Skipping ..."   % ( os.path.basename(d) )

    # For-loop: All CRAB reports (for given dataset)
    for r in reports:
        r.Print()


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
    dataset      = directory.split("/")[-1]
    nJobs        = len(crabResults['jobList'])

    if verbose:
        print "=== multicrabGet.py:"

    # For-loop:All CRAB results
    for iJob, r in enumerate(crabResults['jobList']):

        # The comma at the end of the print statement tells it not to go to the next line.
        if verbose:
            progress = "\r\t Assessing job %s of %s for task \"%s\"" % (iJob, nJobs-1, dataset)
            print '{0}\r'.format(progress),

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
    print
        
    # Print results in a nice table
    if verbose:
        summary = []
        summary.append("\t " + str(finished))
        summary.append("\t " + str(failed))
        summary.append("\t " + str(retrievedLog))
        summary.append("\t " + str(retrievedOut))
        
        line  = '{:<20} {:<1} {:<5} {:>5}'.format("\t Finished"            , ":", summary[0], " / " + str(nJobs) )
        line += "\n {:<20} {:<1} {:<5} {:>5}".format("\t Failed"           , ":", summary[1], " / " + str(nJobs) )
        line += "\n {:<20} {:<1} {:<5} {:>5}".format("\t Retrieved Logs"   , ":", summary[2], " / " + str(nJobs) )
        line += "\n {:<20} {:<1} {:<5} {:>5}".format("\t Retrieved Outputs", ":", summary[3], " / " + str(nJobs) )
        print "=== multicrabGet.py:\n\t Printing summary for task \"%s\"" % ( dataset )
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
    '''
    if os.path.exists(path):
        os.system("touch %s"%path)

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
