'''
\package multicrab
Python interface for multicrab, also the default SE black list

The functionality is divided to
\li creating (multi)crab tasks (also multicrabDataset package)
\li querying the status of crab jobs (via hplusMultiCrabStatus.py)
'''

#================================================================================================
# Import modules
#================================================================================================
import os, re
import sys
import subprocess, errno
import time
import math
import glob
import shutil
import select
import ConfigParser
import OrderedDict

import tarfile

#================================================================================================
# Function Definitions
#================================================================================================
def getTaskDirectories(opts, filename="multicrab.cfg", directory=""):
    '''
    '''
    if hasattr(opts, "dirs") and len(opts.dirs) > 0:
        ret = []
        for d in opts.dirs:
            if d[-1] == "/":
                ret.append(d[0:-1])
            else:
                ret.append(d)
        return ret
    else:
        fname = os.path.join(directory, filename)
        if os.path.exists(fname):
            taskNames = _getTaskDirectories_crab2(fname)
            dirname = os.path.dirname(fname)
            taskNames = [os.path.join(dirname, task) for task in taskNames]
        else:
            taskNames = _getTaskDirectories_crab3(directory)

        def filt(dir):
            '''
            '''
            if opts.filter in dir:
                return True
            return False
        if opts != None:
            if opts.filter != "":
                taskNames = filter(filt, taskNames)
            if len(opts.skip) > 0:
                for skip in opts.skip:
                    taskNames = filter(lambda n: skip not in n, taskNames)

        return taskNames


def _getTaskDirectories_crab2(filename):
    '''
    '''
    if not os.path.exists(filename):
        raise Exception("Multicrab configuration file '%s' does not exist" % filename)

    mc_ignore = ["MULTICRAB", "COMMON"]
    mc_parser = ConfigParser.ConfigParser(dict_type=OrderedDict.OrderedDict)
    mc_parser.read(filename)

    sections = mc_parser.sections()

    for i in mc_ignore:
        try:
            sections.remove(i)
        except ValueError:
            pass
    return sections


def _getTaskDirectories_crab3(directory):
    '''
    '''
    dirs = glob.glob(os.path.join(directory, "*")) #fixme
    dirs = filter(lambda d: os.path.isdir(d), dirs)
    return dirs


def addOptions(parser):
    '''
    Add common MultiCRAB options to OptionParser object.

    \param parser  optparse.OptionParser object
    '''
    parser.add_option("--dir", "-d", dest="dirs", type="string", action="append", default=[],
                      help="CRAB task directory to have the files to merge (default: read multicrab.cfg and use the sections in it)")
    parser.add_option("--filter", dest="filter", type="string", default="",
                      help="When reading CRAB tasks from multicrab.cfg, take only tasks whose names contain this string")
    parser.add_option("--skip", dest="skip", type="string", action="append", default=[],
                      help="When reading CRAB tasks from multicrab.cfg, skip tasks containing this string (can be given multiple times)")
    return


def checkCrabInPath():
    '''
    Raise OSError if 'crab' command is not found in $PATH.
    '''
    try:
        retcode = subprocess.call(["crab"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError, e:
        if e.errno == errno.ENOENT:
            raise Exception("crab executable not found in $PATH. Is the crab environment loaded?")
        else:
            raise e
    return


def crabCfgTemplate(scheduler="arc", return_data=None, copy_data=None, crabLines=[], cmsswLines=[], userLines=[], gridLines=[]):
    '''
    '''
    if return_data is None and copy_data is None:
        raise Exception("You must give either return_data or copy_data, you gave neither")
    if return_data is not None and copy_data is not None:
        raise Exception("You must give either return_data or copy_data, you gave both")
    if copy_data is not None:
        return_data = not copy_data
    if return_data:
        r = 1
        c = 0
    else:
        r = 0
        c = 1

    lines = [
        "[CRAB]",
        "jobtype = cmssw",
        "scheduler = %s" % scheduler,
        ]
    lines.extend(crabLines)
    if len(cmsswLines) > 0:
        lines.extend(["",
                      "[CMSSW]",
                      "use_dbs3 = 1"
                      ])
        lines.extend(cmsswLines)
    lines.extend([
        "",
        "[USER]",
        "return_data = %d" % r,
        "copy_data = %d" % c,
        ])
    lines.extend(userLines)
    lines.extend([
        "",
        "[GRID]",
        "virtual_organization = cms"
        ])
    lines.extend(gridLines)
    return "\n".join(lines)


def writeGitVersion(dirname):
    '''
    Write git version information to a directory

    \param dirname  Path to multicrab directory
    '''
    version = git.getCommitId()
    if version != None:
        f = open(os.path.join(dirname, "codeVersion.txt"), "w")
        f.write(version+"\n")
        f.close()
        f = open(os.path.join(dirname, "codeStatus.txt"), "w")
        f.write(git.getStatus()+"\n")
        f.close()
        f = open(os.path.join(dirname, "codeDiff.txt"), "w")
        f.write(git.getDiff()+"\n")
        f.close()
    return


#================================================================================================
# Class Definition
#================================================================================================
class ExitCodeException(Exception):
    '''
    Exception for non-succesful crab job exit codes
    '''
    def __init__(self, message):
        self.message = message
        return
    def __str__(self):
        return self.message


def assertJobSucceeded(stdoutFile, allowJobExitCodes=[], verbose=False):
    '''
    Given crab job stdout file (tar file), ensure that the job succeeded

    \param stdoutFile   Path to crab job stdout file
    \param allowJobExitCodes  Consider jobs with these non-zero exit codes to be succeeded
    If any of the checks fail, raises multicrab.ExitCodeException

    for documentation on "tarfile" see https://pymotw.com/2/tarfile/
    '''

    # Create a string representing a pattern to look for
    re_exe = re.compile("process\s+id\s+is\s+\d+\s+status\s+is\s+(?P<code>\d+)")
    re_job = re.compile("JobExitCode=(?P<code>\d+)")

    # Initialise Variables
    exeExitCode = None
    jobExitCode = None

    # Sanity check
    if tarfile.is_tarfile(stdoutFile):

        if verbose:
            print "\t Opening tarfile %s" % (stdoutFile)
        fIN    = tarfile.open(stdoutFile, "r")
        log_re = re.compile("cmsRun-stdout-(?P<job>\d+)\.log")
        
        # For-loop: All meta-data [via getmembers()]
        for member in fIN.getmembers():
            
            # Extract tarfile and look for matching string
            if verbose:
                print "\t\t Extracting member with name %s" % (member.name)

            # Access the data from archive member 
            f       = fIN.extractfile(member)
            match   = log_re.search(f.name)

            # For-loop: All lines in file
            if match:
                for iLine, line in enumerate(f):

                    # Get execution exit code
                    m = re_exe.search(line)
                    if m:
                        exeExitCode = int( m.group("code") )
                        continue                    

                    # Get job exit code
                    m = re_job.search(line)
                    if m:
                        jobExitCode = int(m.group("code"))
                        continue
        # Close the tarfile
        if verbose:
            print "\t Closing tarfile %s" % (stdoutFile)
        fIN.close()

    jobExitCode = exeExitCode
    if exeExitCode == None:
        raise ExitCodeException("No exeExitCode")
    if jobExitCode == None:
        raise ExitCodeException("No jobExitCode")
    if exeExitCode != 0:
        raise ExitCodeException("Executable exit code is %d" % exeExitCode)
    if jobExitCode != 0 and not jobExitCode in allowJobExitCodes:
        raise ExitCodeException("Job exit code is %d" % jobExitCode)

    # if verbose:
    if 0:
        print "=== multicrab.py\n\t File %s has exit code %s" % (stdoutFile, jobExitCode)
    return


def prettyJobnums(jobnums):
    '''
    Compact job number list
    
    \param jobnums  List of job numbers (as integers)
    
    \return String of compacted job number list
    '''
    ret = []

    stack = []
    for i in range(0, len(jobnums)):
        if len(stack) == 0:
            stack.append(jobnums[i])
        elif len(stack) == 1:
            if stack[-1] != jobnums[i]-1:
                num = stack.pop()
                ret.append(str(num))
            stack.append(jobnums[i])
        else:
            if stack[-1] == jobnums[i]-1:
                stack.pop()
            else:
                end = stack.pop()
                begin = stack.pop()
                if begin == end-1:
                    ret.append("%d,%d" % (begin, end))
                else:
                    ret.append("%d-%d" % (begin, end))
            stack.append(jobnums[i])
    if len(stack) == 1:
        ret.append(str(stack.pop()))
    elif len(stack) == 2:
        end = stack.pop()
        begin = stack.pop()
        if begin == end-1:
            ret.append("%d,%d" % (begin, end))
        else:
            ret.append("%d-%d" % (begin, end))
    elif len(stack) != 0:
        raise Exception("Internal error: stack size is %d, content is %s" % (len(stack), str(stack)), "pretty_jobnums")

    return ",".join(ret)


def prettyToJobList(prettyString):
    '''
    Transform pretty job number string to list of job numbers

    \param prettyString   String for pretty job number list (of the form '1,2,3-6,9')
    
    \return List of ints for job numbers
    '''
    commaSeparated = prettyString.split(",")
    ret = []
    for item in commaSeparated:
        if "-" in item:
            if item.count("-") != 1:
                raise Exception("=== multicrab.py:\n\t Item '%s' has more than 1 occurrances of '-', in string '%s'" % (item, prettyString))
            (first, last) = item.split("-")
            ret.extend(range(int(first), int(last)+1))
        else:
            ret.append(int(item))
    return ret


def crabStatusOutput(task, printCrab):
    '''
    Get output of 'crab -status' of one CRAB task

    \param task      CRAB task directory name
    \param printCrab Print CRAB output

    \return Output (stdout+stderr) as a string
    '''
    if False: # debugging
        out = open("crabOutput-%s.txt" % time.strftime("%y%m%d_%H%M%S"), "w")
    else:
        out = None

    command = ["crab", "-status", "-c", task]
    p       = subprocess.Popen(command, stdout=subprocess.PIPE)
    output  = ""

    # The process may finish between p.poll() and p.stdout.readline()
    # http://stackoverflow.com/questions/10756383/timeout-on-subprocess-readline-in-python
    # Try first just using select for polling if p.stdout has anything
    # If that doesn't work out, add the timeout (currently in comments)
    poll_obj = select.poll()
    poll_obj.register(p.stdout, select.POLLIN)

    while True:
        exit_result = p.poll()
        while True:
            poll_result = poll_obj.poll(0) # poll timeout is 0 ms
            if poll_result:
                line = p.stdout.readline()
                if line:
                    if printCrab:
                        print line.strip("\n")
                    if out is not None:
                        out.write(line)
                    output += line
                else:
                    break
            else: # if nothing to read, continue to check if the process has finished
                break
        if exit_result is None:
            time.sleep(1)
        else:
            break

    if out is not None:
        out.close()

    if p.returncode != 0:
        if printCrab:
            raise Exception("Command '%s' failed with exit code %d" % (" ".join(command), p.returncode))
        else:
            raise Exception("Command '%s' failed with exit code %d, output:\n%s" % (" ".join(command), p.returncode, output))
    return -output


#================================================================================================
# Class Definition
#================================================================================================
class CrabOutputException(Exception):
    '''
    Exception for something being wrong in the crab output
    '''
    def __init__(self, message):
        Exception.__init__(self, message)
        return

def crabOutputToJobs(task, output):
    '''
    Transform 'crab -status' output to list of multicrab.CrabJob objects

    \param task    CRAB task directory
    \param output  Output from 'crab -status', e.g. from multicrab.crabStatusOutput()

    \return List of multicrab.CrabJob objects
    '''
    status_re = re.compile("(?P<id>\d+)\s+(?P<end>\S)\s+(?P<status>\S+)(\s+\(.*?\))?\s+(?P<action>\S+)\s+(?P<execode>\S+)?\s+(?P<jobcode>\S+)?\s+(?P<host>\S+)?")
    total_re  = re.compile("crab:\s+(?P<njobs>\d+)\s+Total\s+Jobs")
    jobs      = {}
    njobs     = 0
    total     = None
    for line in output.split("\n"):
        m = status_re.search(line)
        if m:
            job = CrabJob(task, m)
            aux.addToDictList(jobs, job.status, job)
            njobs += 1
            continue
        m = total_re.search(line)
        if m:
            total = int(m.group("njobs"))

    if total is None:
        raise CrabOutputException("Did not find total number of jobs from the crab output")
    if total != njobs:
        raise CrabOutputException("Crab says total number of jobs is %d, but only %d was found from the input" % (total, njobs))
    return jobs


def _intIfNotNone(n):
    '''
    Convert argument to int if it is not None
    '''
    if n == None:
        return n
    return int(n)

def crabStatusToJobs(task, printCrab):
    '''
    Run 'crab -status' and create multicrab.CrabJob objects
    
    \param task  CRAB task directory
    \param printCrab Print CRAB output

    \return List of multicrab.CrabJob objects
    '''
    # For some reason in lxplus sometimes the crab output is
    # garbled. In case of value errors try 4 times.
    maxTrials = 4
    for i in xrange(0, maxTrials):
        try:
            output = crabStatusOutput(task, printCrab)
            return crabOutputToJobs(task, output)
        except ValueError, e:
            if i == maxTrials-1:
                raise e
            print >>sys.stderr, "%s: Got garbled output from 'crab -status' (parse error), trying again" % task
        except CrabOutputException, e:
            if i == maxTrials-1:
                raise e
            print >>sys.stderr, "%s: Got garbled output from 'crab -status' (mismatch in number of jobs), trying again" % task

    raise Exception("Assetion, this line should never be reached")


#================================================================================================
# Class Definition
#================================================================================================
class CrabJob:
    '''
    Class for containing the information of finished CRAB job
    '''
    def __init__(self, task, match):
        '''
        Constructor
        
        \param task   CRAB task directory
        \param match  Regex match object from multicrab.crabOutputToJobs() function
        '''
        self.task = task
        self.id = int(match.group("id"))
        self.end = match.group("end")
        self.status = match.group("status")
        self.origStatus = self.status[:]
        self.action = match.group("action")

        if self.status == "Cancelled":
            self.exeExitCode = None
            self.jobExitCode = None
        else:
            self.exeExitCode = _intIfNotNone(match.group("execode"))
            self.jobExitCode = _intIfNotNone(match.group("jobcode"))
        self.host = match.group("host")

        if self.jobExitCode != None and self.jobExitCode != 0:
            self.status += " (%d)" % self.jobExitCode
        elif self.exeExitCode != None and self.exeExitCode != 0:
            self.status += " (exe %d)" % self.exeExitCode
        return

    def stdoutFile(self):
        '''
        Get path to the job stdout file
        '''
        return os.path.join(self.task, "res", "CMSSW_%d.stdout"%self.id)


    def failed(self, status):
        '''
        Check if job has failed
        
        \param status  "all", "aborted", or "done". 
        
        \return True, if job has failed, False, if job has succeedded
        
        Job can fail either before it has started to run (by grid,
        "aborted"), or after it has started to run (site/software
        problem, "done". With \a status parameter, one can control if
        one want's to check the status of aborted jobs only, done jobs
        only, or both. Use case is the resubmission of aborted-only,
        done-only, or all failed jobs.        
        '''
        if (status == "all" or status == "aborted") and self.origStatus == "Aborted":
            return True
        if status == "done" and self.origStatus == "Done":
            return True
        if self.origStatus != "Retrieved":
            return False
        if self.exeExitCode == 0 and self.jobExitCode == 0:
            return False

        if status == "all":
            return True
        if status == "aborted":
            return False
        if self.jobExitCode in status:
            return True
        return False


#================================================================================================
# Class Definition
#================================================================================================
class Multicrab:
    '''
    Abstraction of the entire multicrab configuration for the configuration generation (intended for users)
    '''
    # "Enumeration" for task splitting mode for tasks with >= 500 jobs
    NONE   = 1
    SPLIT  = 2
    SERVER = 3

    def __init__(self, crabConfig=None, pyConfig=None, lumiMaskDir="", crabConfigTemplate=None, ignoreMissingDatasets=False):
        '''
        ## Constructor.
        
        \param crabConfig   String for crab configuration file
        \param pyConfig     If set, override the python CMSSW configuration file of crabConfig

        \param lumiMaskDir  The directory for lumi mask (aka JSON) files, can be absolute or relative path

        \param crabConfigTemplate  String containing the crab.cfg. Either this ir crabConfig must be given

        \param ignoreMissingDatasets  If true, missing datasets in a workflow are ignored in _createDatasets()

        Parses the crabConfig file for CMSSW.pset and CMSSW.lumi_mask.
        Ensures that the CMSSW configuration file exists.
        '''
        if crabConfig is None and crabConfigTemplate is None:
            raise Exception("You must specify either crabConfig or crabConfigTemplate, you gave neither")
        if crabConfig is not None and crabConfigTemplate is not None:
            raise Exception("You must specify either crabConfig or crabConfigTemplate, you gave both")

        self.generatedFiles        = []
        self.filesToCopy           = []
        self.commonLines           = []
        self.lumiMaskDir           = lumiMaskDir
        self.datasetNames          = []
        self.datasets              = None
        self.ignoreMissingDatasets = ignoreMissingDatasets

        # Read crab.cfg for lumi_mask and optionally pset
        if crabConfig is not None:
            if not os.path.exists(crabConfig):
                raise Exception("CRAB configuration file '%s' doesn't exist!" % crabConfig)

            self.crabConfig = os.path.basename(crabConfig)
            self.filesToCopy.append(crabConfig)            

            crab_parser = ConfigParser.ConfigParser()
            crab_parser.read(crabConfig)

            optlist = ["lumi_mask"]
            if pyConfig is None:
                optlist.append("pset")
            for opt in optlist:
                try:
                    self.filesToCopy.append(crab_parser.get("CMSSW", opt))
                except ConfigParser.NoOptionError:
                    pass
                except ConfigParser.NoSectionError:
                    pass
        else:
            self.crabConfig = "crab.cfg"
            self.generatedFiles.append( ("crab.cfg", crabConfigTemplate) )
    
        # If pyConfig is given, use it
        if pyConfig != None:
            if not os.path.exists(pyConfig):
                raise Exception("Python configuration file '%s' doesn't exist!" % pyConfig)

            self.filesToCopy.append(pyConfig)
            self.commonLines.append("CMSSW.pset = "+os.path.basename(pyConfig))
        return


    def extendDatasets(self, workflow, datasetNames):
        '''
        Extend the list of datasets for which the multicrab configuration is generated.
    
        \param workflow      String for workflow

        \param datasetNames  List of strings of the dataset names.
        '''
        if self.datasets != None:
            raise Exception("Unable to add more datasets, the dataset objects are already created")

        self.datasetNames.extend([(name, workflow) for name in datasetNames])
        return


    def _createDatasets(self):
        '''
        Create the MulticrabDataset objects.
        
        This method was intended to be called internally.
        '''

        if len(self.datasetNames) == 0:
            raise Exception("Call addDatasets() first!")

        self.datasets   = []
        self.datasetMap = {}

        for dname, workflow in self.datasetNames:
            try:
                dset = MulticrabDataset(dname, workflow, self.lumiMaskDir)
                self.datasets.append(dset)
                self.datasetMap[dname] = dset
            except Exception, e:
                if not self.ignoreMissingDatasets:
                    raise
                print "Warning: dataset %s ignored for workflow %s, reason: %s" % (dname, workflow, str(e))
        return

    def getDataset(self, name):
        '''
        Get MulticrabDataset object for name.
        '''
        if self.datasets == None:
            self._createDatasets()
        return self.datasetMap[name]


    def getNumberOfDatasets(self):
        '''
        '''
        if self.datasets == None:
            self._createDatasets()
        return len(self.datasets)

    def forEachDataset(self, function):
        '''
        Apply a function for each MulticrabDataset.
    
        \param function    Function
     
        The function should take the MulticrabDataset object as an
        argument. The return value of the function is not used.
     
        Example:
        \code
        obj.forEachDataset(lambda d: d.setNumberOfJobs(6))
        \endcode
        '''
        if self.datasets == None:
            self._createDatasets()

        for d in self.datasets:
            function(d)
        return


    def modifyNumberOfJobsAll(self, func):
        '''
        Modify the number of jobs of all dataset with a function.
    
        \param func    Function
    
        The function gets the original number of jobs as an argument,
        and the function should return a number for the new number of
        jobs.
        
        Example:
        \code
        obj.modifyNumberOfJobsAll(lambda n: 2*n)
        \endcode
        '''
        if self.datasets == None:
            self._createDatasets()

        for d in self.datasets:
            if "number_of_jobs" in d.data:
                d.modifyNumberOfJobs(func)
        return


    def modifyLumisPerJobAll(self, func):
        '''
        Modify the lumis per job s of all dataset with a function.
    
        The function gets the original lumis per job as an argument,
        and the function should return a number for the new number of
        lumis per job.
        
        Example:
        \code
        obj.modifyLumisPerJobAll(lambda n: 2*n)
        \endcode
        '''
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            if "lumis_per_job" in d.data:
                d.modifyLumisPerJob(func)
        return


    def appendArgAll(self, arg):
        '''
        Append an argument to the pycfg_params list for all datasets.
        '''
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.appendArg(arg)
        return


    def appendLineAll(self, line):
        '''
        Append a line to multicrab.cfg configuration for all datasets.
        
        \param line   Line to add
         
        Line can be any string multicrab eats, e.g.
        \li USER.publish_dataset = foo
        CMSSW.output_file = foo.root
        '''
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.appendLine(line)
        return


    def extendBlackWhiteListAll(self, blackWhiteList, sites):
        '''
        Extend the CE/SE black/white list with a list of sites for all datasets.
        
        \param blackWhiteList    String specifying which list is modified  ('ce_black_list', 'ce_white_list', 'se_black_list', 'se_white_list')

        \param sites             List of sites to extend the given black/white list
        '''
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.extendBlackWhiteList(blackWhiteList, sites)
        return


    def addCommonLine(self, line):
        '''
        Append a line to multicrab.cfg configuration to the [COMMON] section.
        
        Line can be any string multicrab eats, e.g.
        \li USER.publish_dataset = foo
        \li CMSSW.output_file = foo.root
        '''
        self.commonLines.append(line)
        return

        
    def _getConfig(self, datasetNames):
        '''
        Generate the multicrab configration as a string.
        
        \param datasetNames  List of dataset names for which to write the configuration
    
        This method was intended to be called internally.
        '''
        if self.datasets == None:
            self._createDatasets()

        ret = "[MULTICRAB]\n"
        ret += "cfg = %s\n" % self.crabConfig

        ret += "\n[COMMON]\n"
        for line in self.commonLines:
            ret += line + "\n"

        for name in datasetNames:
            ret += "\n" + self.getDataset(name)._getConfig()
        return ret


    def _writeGeneratedFiles(self, directory):
        '''
        Write generated files to a directory.
        
        \param directory   Directory where to write the generated files
        
        This method was intended to be called internally.
        '''
        for fname, content in self.generatedFiles:
            f = open(os.path.join(directory, fname), "wb")
            f.write(content)
            f.close()
        return


    def _writeConfig(self, filename, datasetNames):
        '''
        Write the multicrab configuration to a given file name.
        
        \param filename      Write the configuration to this file

        \param datasetNames  List of dataset names for which to write the configuration
        
        This method was intended to be called internally.
        '''
        f = open(filename, "wb")
        f.write(self._getConfig(datasetNames))
        f.close()

        directory = os.path.dirname(filename)
        self._writeGeneratedFiles(directory)

        for name in datasetNames:
            self.getDataset(name)._writeGeneratedFiles(directory)

        print "Wrote multicrab configuration to %s" % filename
        return


    def createTasks(self, configOnly=False, codeRepo='git', over500JobsMode=NONE, **kwargs):
        '''
        Create the multicrab task.
        
        \param configOnly   If true, generate the configuration only (default: False).

        \param kwargs       Keyword arguments (forwarded to multicrab.createTaskDir, see also below)
        
        <b>Keyword arguments</b>
        \li\a prefix       Prefix of the multicrab task directory (default: 'multicrab')
        
        Creates a new directory for the CRAB tasks, generates the
        multicrab.cfg in there, copies and generates the necessary
        files to the directory and optionally run 'multicrab -create'
        in the directory.
        '''
        if self.datasets == None:
            self._createDatasets()

        # If mode is NONE, create tasks for all datasets
        if over500JobsMode == Multicrab.NONE:
            return self._createTasks(configOnly, codeRepo, **kwargs)

        datasetsOver500Jobs  = OrderedDict.OrderedDict()
        datasetsUnder500Jobs = OrderedDict.OrderedDict()
        def checkAnyOver500Jobs(dataset):
            njobs = dataset.getNumberOfJobs()
            if njobs > 500:
                datasetsOver500Jobs[dataset.getName()] = njobs
            else:
                datasetsUnder500Jobs[dataset.getName()] = njobs
        self.forEachDataset(checkAnyOver500Jobs)

        # If all tasks have < 500 jobs, create all tasks
        if len(datasetsOver500Jobs) == 0:
            return self._createTasks(configOnly, codeRepo, **kwargs)

        # If mode is SERVER, set server=1 for tasks with >= 500 jobs
        if over500JobsMode == Multicrab.SERVER:
            for dname in datasetsOver500Jobs.iterkeys():
                self.getDataset(dname).useServer(True)
            return self._createTasks(configOnly, codeRepo, **kwargs)

        # If mode is SPLIT, first create < 500 job tasks in one
        # multicrab directory, then for each tasks with >= 500 jobs
        # create one multicrab directory per 500 jobs
        if over500JobsMode == Multicrab.SPLIT:
            ret = self._createTasks(configOnly, codeRepo, datasetNames=datasetsUnder500Jobs.keys(), **kwargs)

            args = {}
            args.update(kwargs)
            prefix = kwargs.get("prefix", "multicrab")
            
            for datasetName, njobs in datasetsOver500Jobs.iteritems():
                dname = datasetName.split("_")[0]
                nMulticrabTasks = int(math.ceil(njobs/500.0))
                for i in xrange(nMulticrabTasks):
                    firstJob = i*500+1
                    lastJob = (i+1)*500
                    args["prefix"] = "%s_%s_%d-%d" % (prefix, dname, firstJob, lastJob)
                    ret.extend(self._createTasks(configOnly, codeRepo, datasetNames=[datasetName], **args))

            return ret
        raise Exception("Incorrect value for over500JobsMode: %d" % over500JobsMode)
                                                    

    def _createTasks(self, configOnly=False, codeRepo='git', datasetNames=None, **kwargs):
        '''
        Create the multicrab task.
        
        \param configOnly   If true, generate the configuration only (default: False).
        \param codeRepo     If something else than 'git', don't produce codeVersion/Status/Diff files
        \param datasetNames If not None, should be list of dataset names for which to create tasks
        \param kwargs       Keyword arguments (forwarded to multicrab.createTaskDir, see also below)
        
        <b>Keyword arguments</b>
        \li\a prefix       Prefix of the multicrab task directory (default: 'multicrab')
        
        Creates a new directory for the CRAB tasks, generates the multicrab.cfg in there, copies and generates the necessary
        files to the directory and optionally run 'multicrab -create' in the directory.
        '''
        if not configOnly:
            checkCrabInPath()
        dirname = createTaskDir(**kwargs)

        if datasetNames != None:
            dsetNames = datasetNames[:]
        else:
            dsetNames = [d.getName() for d in self.datasets]

        self._writeConfig(os.path.join(dirname, "multicrab.cfg"), dsetNames)

        # Create code versions
	if codeRepo == 'git':
            writeGitVersion(dirname)

        files = self.filesToCopy[:]
        for name in dsetNames:
            files.extend(self.getDataset(name)._getCopyFiles())
        
        # Unique list of files
        keys = {}
        for f in files:
            keys[f] = 1
        files = keys.keys()
        for f in files:
            shutil.copy(f, dirname)
        print "Copied %s to %s" % (", ".join(files), dirname)
    
        if not configOnly:
            print "Creating multicrab task"
            print 
            print "############################################################"
            print

            prevdir = os.getcwd()
            os.chdir(dirname)
            subprocess.call(["multicrab", "-create"])
            print
            print "############################################################"
            print
            print "Created multicrab task to subdirectory "+dirname
            print

            os.chdir(prevdir)

        return [(dirname, dsetNames)]
