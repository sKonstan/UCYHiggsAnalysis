#!/usr/bin/env python

#================================================================================================
# Import modules
#================================================================================================
import os, re
import sys
import glob
import shutil
import subprocess
from optparse import OptionParser
import tarfile

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import UCYHiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab

#================================================================================================
# Global Variables
#================================================================================================
re_histos         = []
re_se             = re.compile("newPfn =\s*(?P<url>\S+)")
replace_madhatter = ("srm://madhatter.csc.fi:8443/srm/managerv2?SFN=", "root://madhatter.csc.fi:1094")


#================================================================================================
# Function Definitions
#================================================================================================
def AbortScript(keystroke, msg):
    '''
    Give user last chance to abort the script before its execution
    '''
    message = "=== multicrabMergeHistograms.py:\n\t %s\n\t Press \"%s\" to abort, any other key to proceed: " % (msg, keystroke)
    response = raw_input(message)
    if (response!= keystroke):
        return
    else:
        print "=== multicrabMergeHistograms.py:\n\t EXIT"
        sys.exit()
    return


def histoToDict(histo):
    '''
    '''
    ret = {}
    
    for bin in xrange(1, histo.GetNbinsX()+1):
        ret[histo.GetXaxis().GetBinLabel(bin)] = histo.GetBinContent(bin)    
    return ret


def GetNumOfLinesInFile(fileName):
    '''
    Self explanatory
    '''
    return sum(1 for line in fileName)    


def getHistogramFile(stdoutFile, opts, verbose=False):
    '''
    '''
    if opts.assertJobs:
        multicrab.assertJobSucceeded(stdoutFile, opts.allowJobExitCodes, verbose)
    histoFile = None

    # Sanity check
    if tarfile.is_tarfile(stdoutFile):
        if verbose:
            print "==== multicrabMergeHistograms.py:\n\t Opening tarfile %s" % (stdoutFile)
        fIN    = tarfile.open(stdoutFile)
        log_re = re.compile("cmsRun-stdout-(?P<job>\d+)\.log")
        
        # For-loop: All members  
        for member in fIN.getmembers():
            f     = fIN.extractfile(member)
            match = log_re.search(f.name)
            if match:
                if verbose:
                    progress = "\r\t Processing job %s" % (match.group("job"))
                    print '{0}\r'.format(progress),
                histoFile = "miniAOD2FlatTree_%s.root" % match.group("job")
        if verbose:
            print "==== multicrabMergeHistograms.py:\n\t Closing tarfile %s" % (stdoutFile)
        fIN.close()
    else:
        if verbose:
            print "==== multicrabMergeHistograms.py:\n\t Opening file %s" % (stdoutFile)            
        f = open(stdoutFile)
        # For-loop: All lines in file 
        for line in f:
            for r in re_histos:
                m = r.search(line)
                if m:
                    histoFile = m.group("file")
                    break
            if histoFile is not None:
                 break
        f.close()
    return histoFile


def getHistogramFileSE(stdoutFile, opts):
    '''
    '''
    if opts.assertJobs:
        multicrab.assertJobSucceeded(stdoutFile, opts.allowJobExitCodes)
    histoFile = None
    f         = open(stdoutFile)
    # For-loop: All lines in file
    for line in f:
        m = re_se.search(line)
        if m:
            histoFile = m.group("url")
            break
    f.close()

    if histoFile != None:
        if not replace_madhatter[0] in histoFile:
            raise Exception("Other output SE's than madhatter are not supported at the moment (encountered PFN %s)"%histoFile)
        histoFile = histoFile.replace(replace_madhatter[0], replace_madhatter[1])
    return histoFile


def splitFiles(files, filesPerEntry, maxSize = 2000000000):
    '''
    '''
    i = 0
    ret = []
    if filesPerEntry < 0:
        maxsize   = maxSize
        sumsize   = 0
        firstFile = 0

        # For-loop: All files
        for ifile,f in enumerate(files):
            sumsize+=os.stat(f).st_size
            if sumsize > maxsize:
                ret.append( (i, files[firstFile:ifile]) )
                i += 1
                sumsize = 0
                firstFile = ifile
            if ifile == len(files)-1:
                ret.append( (i, files[firstFile:]) )
    else:
        def beg(ind):
            return ind*filesPerEntry
        def end(ind):
            return (ind+1)*filesPerEntry
        while beg(i) < len(files):
            ret.append( (i, files[beg(i):end(i)]) )
            i += 1
    return ret


def hadd(opts, mergeName, inputFiles):
    '''
    '''
    cmd = ["hadd"]
    if opts.filesInSE:
        cmd.append("-T") # don't merge TTrees via xrootd
    cmd.append(mergeName)
    cmd.extend(inputFiles)
    if opts.verbose:
        print " ".join(cmd)
    if opts.test:
        return 0
    args = {}
    if not opts.verbose:
        args = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT}
    p = subprocess.Popen(cmd, **args)
    output = p.communicate()[0]
    ret = p.returncode
    if ret != 0:
        if not opts.verbose:
            print output
        print "Merging failed with exit code %d" % ret
        return 1
    return 0


def hplusHadd(opts, mergeName, inputFiles):
    '''
    '''
    args = {}
    if not opts.verbose:
        args = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT}

    intermediateFiles = []
    resultFiles = inputFiles[:]
    mergeRound = 0
    while len(resultFiles) > 1:
        splitted = splitFiles(resultFiles, opts.fastFilesPerMerge, opts.maxSize)
        resultFiles = []
        for index, files in splitted:
            if len(splitted) > 1 or mergeRound > 0:
                print "     merge round %d, split round %d" % (mergeRound, index)
            target = mergeName+"-m%d-s%d" % (mergeRound, index)
            if os.path.exists(target):
                shutil.move(target, target+".backup")
            cmd = ["hplusHadd.py", target]+files
            if opts.verbose:
                cmd.append("--verbose")
                print " ".join(cmd)
            if not opts.test:
                p = subprocess.Popen(cmd, **args)
                output = p.communicate()[0]
                ret = p.returncode
                if ret != 0:
                    if not opts.verbose:
                        print output
                    print "Merging failed with exit code %d" % ret
                    return 1
                if not opts.verbose and "Error in" in output:
                    print output
            resultFiles.append(target)
            intermediateFiles.append(target)
        mergeRound += 1

    if intermediateFiles[-1] != resultFiles[0]:
        raise Exception("Assertion, intermediateFiles[-1] = %s != resultFiles[0] = %s" % (intermediateFiles[-1], resultFiles[0]))
    intermediateFiles.pop()

    for tmp in intermediateFiles:
        if opts.verbose:
            print "rm %s" % tmp
        if not opts.test:
            os.remove(tmp)

    if opts.verbose:
        print "mv %s %s" % (resultFiles[0], mergeName)
    if not opts.test:
        shutil.move(resultFiles[0], mergeName)
    
    return 0


#================================================================================================
# Class Definition    
#================================================================================================
class SanityCheckException(Exception):
    '''
    Check that configInfo/configinfo control bin matches to number of
    input files, in order to monitor a mysterious bug reported by Lauri
    '''
    def __init__(self, message):
        super(SanityCheckException, self).__init__(message)


def sanityCheck(mergedFile, inputFiles):
    '''
    '''
    tfile = ROOT.TFile.Open(mergedFile)
    configinfo = tfile.Get("configInfo/configinfo")
    if configinfo:
#        info = dataset._histoToDict(configinfo)
	info = histoToDict(configinfo)
        if int(info["control"]) != len(inputFiles):
            raise SanityCheckException("configInfo/configinfo:control = %d, len(inputFiles) = %d" % (int(info["control"]), len(inputFiles)))
    return


def delete(fname,regexp):
    '''
    '''

    fIN = ROOT.TFile.Open(fname,"UPDATE")
    fIN.cd()
    keys = fIN.GetListOfKeys()
    for i in range(len(keys)):
        if keys.At(i):
            keyName = keys.At(i).GetName()
            dir = fIN.GetDirectory(keyName)
            if dir:
                fIN.cd(keyName)
                delFolder(regexp)
                fIN.cd()
    delFolder(regexp)
    fIN.Close()
    return


def pileup(fname, verbose=False):
    '''
    '''

    if not os.path.exists(fname):
        print "=== multicrabMergeHistograms.py:\n\t ERROR! Could not find file %s " % (fname)

    # Open file to update it
    fileMode = "UPDATE"
    if verbose:
        print "\t\t Opening file in %s mode" % (fileMode)
    fOUT = ROOT.TFile.Open(fname, fileMode)
    fOUT.cd()
    
    hPU = None

    dataVersion   = fOUT.Get("configInfo/dataVersion")    
    stringToMatch = "data"
    dv_re         = re.compile(stringToMatch)
    match         = dv_re.search(dataVersion.GetTitle())

    if match:
        if verbose:
            print "\t\t Dataset is of type \"%s\". Will add to it Pile-Up histogram" % (dataVersion.GetTitle())
        puFile = os.path.join(os.path.dirname(fname), "PileUp.root")
        if os.path.exists(puFile):
            if verbose:
                print "\t Opening file %s" % (puFile)
            fIN = ROOT.TFile.Open(puFile)
            hPU = fIN.Get("pileup")
        else:
            print "\t PileUp not found in" ,os.path.dirname(fname),", did you run hplusLumiCalc.py?"
    else:
        if verbose:
            print "\t\t Dataset is of type \"%s\". Skipping Pile-Up histogram" % (dataVersion.GetTitle())

    if not hPU == None:
        folder = "configInfo"
        fOUT.cd(folder)
        if verbose:
            print "\t Writing %s/%s to %s" % (folder, hPU.GetName(), puFile)            
        hPU.Write("", ROOT.TObject.kOverwrite)

    # Close file
    fOUT.Close()
    return


def delFolder(regexp):
    '''
    '''
    keys = ROOT.gDirectory.GetListOfKeys()
    del_re = re.compile(regexp)
    deleted = False
    for i in reversed(range(len(keys))):
        if keys.At(i):
            keyName = keys.At(i).GetName()
            match = del_re.search(keyName)
            if match:
                if not deleted:
                    deleted = True
                else:
                    cycle = keys.At(i).GetCycle()
                    ROOT.gDirectory.Delete(keyName+";%i"%cycle)
    return


def main(opts, args):
    '''
    '''

    # Declare Variables
    multicrabDir = os.getcwd().split("/")    
    crabdirs     = multicrab.getTaskDirectories(opts)
    exit_re      = re.compile("/results/cmsRun_(?P<exitcode>\d+)\.log\.tar\.gz")
    mergedFiles  = []

    # Print information to user
    if opts.verbose:
        print "=== multicrabMergeHistograms.py:\n\t Found %s CRAB directories:" % (len (crabdirs))
        for d in crabdirs:
            print "\t ", d

    # Append regex expressions
    global re_histos
    re_histos.append(re.compile("^output files:.*?(?P<file>%s)" % opts.input))
    re_histos.append(re.compile("^\s+file\s+=\s+(?P<file>%s)" % opts.input))

    print "=== multicrabMergeHistograms.py:"
    # For-loop: All CRAB directories
    for iDir, d in enumerate(crabdirs):

        if iDir >0:
            print
        print "\t %s (%s/%s)" % ( multicrabDir[-1] + "/" + d, iDir+1, len(crabdirs) )
        d           = d.replace("/", "")
        stdoutFiles = glob.glob(os.path.join(d, "results", "cmsRun_*.log.tar.gz"))
        files       = []
        exitCodes   = []

        #For-loop: All stdout files
        for index, f in enumerate(stdoutFiles):
            print "\r\t Processing job %s of %s%s" % (index+1, len(stdoutFiles), " "*10 ),

            try:
                if opts.filesInSE:
                    histoFile = getHistogramFileSE(f, opts)
                    if histoFile != None:
                        files.append(histoFile)
                    else:
                        print "\t Task %s, skipping job %s: input root file not found from stdout" % (d, f)
                else:
                    histoFile = getHistogramFile(f, opts, opts.verbose)
                    if histoFile != None:
                        path = os.path.join(os.path.dirname(f), histoFile)
                        if os.path.exists(path):
                            files.append(path)
                        else:
                            print "\t Task %s, skipping job %s: input root file found from stdout, but does not exist" % (d, f)
                    else:
                        print "\t Task %s, skipping job %s: input root file not found from stdout" % (d, f)
            except multicrab.ExitCodeException, e:
                print "\t Task %s, skipping job %s: %s" % (d, f, str(e) )
                exit_match = exit_re.search(f)
                if exit_match:
                    exitCodes.append( int(exit_match.group("exitcode")) )

        # Print new line (so that previous print is not deleted)
        print 

        if opts.test:
            if len(exitCodes) > 0:
                print "        jobs with problems:", sorted(exitCodes)
            continue

        if len(files) == 0:
            print "\t Task %s, skipping, no files to merge" % d
            continue

        # For loop: All files
        for f in files:
            if not os.path.isfile(f):
                raise Exception("=== multicrabMergeHistograms.py:\n\t File %s is marked as output file in the CMSSW_N.stdout, but does not exist" % f)

        # Split file to several smaller ones if its size is greater than opts.maxSize (default is 2 GB)
        filesSplit = splitFiles(files, opts.filesPerMerge, opts.maxSize)
        if len(filesSplit) == 1:
            print "\t Merging %d files" % (len(files))
        else:
            print "\t Merging %d files to %d files" % (len(files), len(filesSplit))

        # For-loop: All input files
        for index, inputFiles in filesSplit:
            tmp = d
            if len(filesSplit) > 1:
                tmp += "-%d" % index
            mergeName = os.path.join(d, "results", opts.output % tmp)
            if os.path.exists(mergeName) and not opts.test:
                if opts.verbose:
                    print "\t mv %s %s" % (mergeName, mergeName+".backup")
                shutil.move(mergeName, mergeName+".backup")

            # FIXME: add here reading of first xrootd file, finding all TTrees, and writing the TList to mergeName file
            if opts.filesInSE:
                raise Exception("--filesInSE feature is not fully implemented")

            if len(inputFiles) == 1:
                if opts.verbose:
                    print "cp %s %s" % (inputFiles[0], mergeName)
                if not opts.test:
                    shutil.copy(inputFiles[0], mergeName)
            else:
                if opts.fast:
                    ret = hplusHadd(opts, mergeName, inputFiles)
                    if ret != 0:
                        return ret
                else:
                    ret = hadd(opts, mergeName, inputFiles)
                    if ret != 0:
                        return ret
    
            if len(filesSplit) > 1:
                msg = "\r\t\t Done (%d/%d)" % (index, len(filesSplit) )
                print '{0}\r'.format(msg),
            mergedFiles.append((mergeName, inputFiles))
            try:
                sanityCheck(mergeName, inputFiles)
            except SanityCheckException, e:
                print "\t Task %s: %s; disabling input file deletion" % (d, str(e))
                opts.deleteImmediately = False
                opts.delete = False
            if opts.deleteImmediately:
                for srcFile in inputFiles:
                    if opts.verbose:
                        print "rm %s" % srcFile
                    if not opts.test:
                        os.remove(srcFile)
    
    deleteMessage = ""
    if opts.delete:
        deleteMessage = " (source files deleted)"
    if opts.deleteImmediately:
        deleteMessage = " (source files deleted immediately)"

    print "=== multicrabMergeHistograms.py:\n\t Merged histogram files:%s" % deleteMessage
    # For-loop: All merged files
    for f, sourceFiles in mergedFiles:
        print "\t\t %s (from %d files)" % (f, len(sourceFiles))
        delete(f,"Generated")
        delete(f,"Commit")
        delete(f,"dataVersion")        
        if opts.delete and not opts.deleteImmediately:
            for srcFile in sourceFiles:
                if opts.verbose:
                    print "\t rm %s" % srcFile
                if not opts.test:
                    os.remove(srcFile)
        pileup(f)
    return 0


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    #parser.add_option("-i", dest="input", type="string", default="histograms_.*?\.root",
    #                  help="Regex for input root files (note: remember to escape * and ? !) (default: 'histograms_.*?\.root')")
    parser.add_option("-i", dest="input", type="string", default="miniAOD2FlatTree_.*?\.root",
                      help="Regex for input root files (note: remember to escape * and ? !) (default: 'miniAOD2FlatTree_.*?\.root')")
    
    #parser.add_option("-o", dest="output", type="string", default="histograms-%s.root",
    #                  help="Pattern for merged output root files (use '%s' for crab directory name) (default: 'histograms-%s.root')")
    parser.add_option("-o", dest="output", type="string", default="miniAOD2FlatTree-%s.root",
                      help="Pattern for merged output root files (use '%s' for crab directory name) (default: 'histograms-%s.root')")

    parser.add_option("--test", dest="test", default=False, action="store_true",
                      help="Just test, do not do any merging or deleting (might be useful for checking what would happen). Implies --verbose.")

    parser.add_option("--delete", dest="delete", default=False, action="store_true",
                      help="Delete the source files to save disk space (default is to keep the files)")

    parser.add_option("--deleteImmediately", dest="deleteImmediately", default=False, action="store_true",
                      help="Delete the source files immediately after merging to save disk space (--delete deletes them after all crab tasks have been merged)")

    parser.add_option("--fast", dest="fast", default=False, action="store_true",
                      help="Use hplusHadd.py instead of hadd, it is faster but works only for TH1's. It also consumes (much) more memory, and is run for a couple of files at a time (see --fastFilesPerMerge).")

    parser.add_option("--fastFilesPerMerge", dest="fastFilesPerMerge", default=4, type="int",
                      help="With --fast, merge this many files at a time (default: 4)")

    parser.add_option("--filesPerMerge", dest="filesPerMerge", default=-1, type="int",
                      help="Merge at most this many files together, possibly resulting to multiple merged files. Use case: large ntuples. (default: -1 to merge all files to one)")

    parser.add_option("--filesInSE", dest="filesInSE", default=False, action="store_true",
                      help="The ROOT files to be merged are in an SE, merge the files from there. File locations are read from CMSSW_*.stdout files. NOTE: TTrees are not merged (it is assumed that due to TTrees the files are so big that they have to be stored in SE), but are replaced with TList of strings of the PFN's of the files via xrootd protocol.")

    parser.add_option("--allowJobExitCode", dest="allowJobExitCodes", default=[], action="append", type="int",
                      help="Allow merging files from this non-zero job exit code (zero exe exit code is still required). Can be given multiple times.")

    parser.add_option("--verbose", dest="verbose", default=False, action="store_true",
                      help="Verbose mode")

    parser.add_option("--assert", dest="assertJobs", default=False, action="store_true",
                      help="Before merging any files, assert that all CRAB jobs succeeded!")

    parser.add_option("--maxSize", dest="maxSize", default=2000000000, action="store_true", 
                      help="Define the maximum size of the merged ROOT file. The default value is 2000000000 (2 GB)")

    (opts, args) = parser.parse_args()

    if opts.filesPerMerge == 0:
        parser.error("--filesPerMerge must be non-zero")

    if opts.test:
        opts.verbose = True
    
    if not opts.assertJobs:
        msg = "WARNING! You have launched the script without enabling the \"--assert\" option. Are you sure you want to continue?"
        AbortScript("q", msg)

    sys.exit( main(opts, args) )
