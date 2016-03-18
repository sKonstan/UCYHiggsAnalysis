#!/usr/bin/env python
'''
Usage:
cd multicrab_CMSSWXYZ_SkimType_DayMonthYear_XhYmZs 
multicrabLumiCalc.py


Description:
This script is used to launch brilcalc -a commandline tool for calculating the 
integrated luminosity of collision data processed.
 
Links:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/TTHMultileptonsPlusHadronicTau
http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html

lumiCalc.py usage taken from:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/LumiCalc

PileUp calc according to:
https://indico.cern.ch/event/459797/contribution/3/attachments/1181542/1711291/PPD_PileUp.pdf

=======================
Important Information
=======================
Getting the task report (crab report -d <crab_task>) is relevant when running on real data, because of the files we get containing the
analyzed and the non-analyzed luminosity sections. Remember that the report includes only successfully done jobs.

For exampe, the content of our "lumiSummary.json" file is:
{"193834": [[1, 35]], "193835": [[1, 20], [22, 26]], "193836": [[1, 2]], "193999": [[1, 50]], "193998": [[66, 113], [115, 278]]}

... and the content of our "missingLumiSummary.json" file is:
{"193336": [[1, 264], [267, 492], [495, 684], [687, 729], [732, 951]], "193334": [[29, 172]]}

The "processedLumis.json" Contains the lumis that have been processed by jobs in status finished.
[See https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3Commands]

The "missingLumiSummary.json" file is just the difference between the input lumi-mask file and the lumiSummary.json file. This 
means that the "missingLumiSummary.json" file does not have to be necessarily an empty file even if all jobs have completed successfully. 
And this is simply because the input dataset and the input lumi-mask file may not span the same overall range of runs and luminosity sections. 

Links: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Running_CMSSW_analysis_with_AN1

=======================
Update, 18 Mar 2016
=======================
The command "crab report -d <crab_task> has been revisited in last CRAB version and
the file names have changed to be (hopefully) more clear.
Content is better defined as well, please see
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3Commands#crab_report

In particular I think you want to feed processedLumis.json to
the lumi-calc tool.

Links: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3Commands#crab_report
'''

#================================================================================================ 
# Import Modules
#================================================================================================ 
import os
import re
import sys
import glob
import subprocess
import json
from optparse import OptionParser

import ROOT

from UCYHiggsAnalysis.NtupleAnalysis.tools.aux import execute
import UCYHiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab


#================================================================================================ 
# Global Definitions
#================================================================================================
PileUpJSON      = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt"
dataVersion_re = re.compile("dataVersion=(?P<dataVersion>[^: ]+)")
pu_re          = re.compile("\|\s+\S+\s+\|\s+\S+\s+\|\s+.*\s+\|\s+.*\s+\|\s+\S+\s+\|\s+\S+\s+\|\s+(?P<lumi>\d+(\.\d*)?|\.\d+)\s+\|\s+(?P<pu>\d+(\.\d*)?|\.\d+)\s+\|\s+\S+\s+\|")


#================================================================================================ 
# Function Definitions
#================================================================================================
def TruncateString(myString, maxChars):
    tString = (myString[:maxChars-2] + "..") if len(myString) > maxChars else myString
    return tString


def isMCTask(taskdir):
    crabCfg = "crabConfig_"+taskdir+".py"
    if not os.path.exists(crabCfg):
        print "=== multicrabLumiCalc.py:\n\t crab.cfg at %s doesn't exist, assuming task is MC" % crabCfg
        return True

    f = open(crabCfg)
    isData = False
    for line in f:
        if "pyCfgParams" in line:
            m = dataVersion_re.search(line)
            if not m:
                print "Unable to find dataVersion, assuming task %s is MC" % taskdir
                return True
            if "data" in m.group("dataVersion"):
                isData = True
                break
    f.close()
    return not isData


def isEmpty(taskdir):
    path  = os.path.join(taskdir, "results")
    files = execute("ls %s"%path)
    return len(files)==0


def convertLumi(lumi, unit):
    '''
    Converts luminosity to pb^-1
    '''
    if unit == "ub":
        return lumi/1e6
    elif unit == "nb":
        return lumi/1e3
    elif unit == "pb":
        return lumi
    elif unit == "fb":
        return lumi*1e3
    else:
        raise Exception("Unsupported luminosity unit %s"%unit)


def main(opts, args):

    cell    = "\|\s+(?P<%s>\S+)\s+"
    lumi_re = re.compile("\|\s+(?P<recorded>\d+\.*\d*)\s+\|\s*$")
    unit_re = re.compile("totrecorded\(/(?P<unit>.*)\)")
    # lumi_re = re.compile( (cell % "deliveredls") + (cell % "delivered") + (cell % "selectedls") + (cell % "recorded")+"\|") 
    
    # Summary:  
    # +-------+------+------+------+-------------------+------------------+
    # | nfill | nrun | nls  | ncms | totdelivered(/pb) | totrecorded(/pb) |
    # +-------+------+------+------+-------------------+------------------+
    # |   1   |  1   | 1585 | 1585 |       25.515      |      25.028      |
    # +-------+------+------+------+-------------------+------------------+

    if not opts.truncate and os.path.exists(opts.output):
        f = open(opts.output, "r")
        data = json.load(f)
        f.close()
    
    files = []
    # Only if no explicit files, or some directories explicitly given
    if len(opts.files) == 0 or len(opts.dirs) > 0:
        crabdirs = multicrab.getTaskDirectories(opts)

        for d in crabdirs:
            if isMCTask(d):
                print "=== multicrabLumiCalc.py:\n\t Ignoring task directory '%s', it looks like MC" % d
                continue
            if isEmpty(d):
                print "=== multicrabLumiCalc.py:\n\t Ignoring task directory '%s', it looks empty" % d
                continue
    
            if opts.report:                
                multicrab.checkCrabInPath()
                cmd = ["crab", "report", d]
                if opts.verbose:
                    print " ".join(cmd)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = p.communicate()[0]
                ret = p.returncode
                if ret != 0:
                    print "=== multicrabLumiCalc.py:\n\t Call to 'crab report -d %s' failed with return value %d" % (d, ret)
                    print output
                    return 1
                if opts.verbose:
                    print output
                                
            lumiSummary    = os.path.join(d, "results", "lumiSummary.json")     
            processedLumis = os.path.join(d, "results", "processedLumis.json")
            
            if os.path.exists(lumiSummary):         # CRAB3 [before March 2016 update]
                files.append( (d, lumiSummary) )
            elif os.path.exists( processedLumis):   # CRAB3 [after March 2016 update]
                files.append( (d, processedLumis) )
            else:
                msg = "Neither \"%s\" nor \"%s\" exists! Have you called \"crab report\"?" % (lumiSummary, processedLumis)
                raise Exception(msg)

    files.extend([(None, f) for f in opts.files])

    print "=== multicrabLumiCalc.py:"
    data = {}    
    for task, jsonFile in files:
        lumicalc = opts.lumicalc

	# brilcalc lumi -u /pb -i JSON-file
        home = os.environ['HOME']
        path = os.path.join(home,".local/bin")
        exe  = os.path.join(path,"brilcalc")
        if not os.path.exists(exe):
            print "=== multicrabLumiCalc.py:\n\t brilcalc not found, have you installed it?\n\t See http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html"
            sys.exit()

	cmd = [exe,"lumi","--byls", "-u/pb","-i", jsonFile]
        if opts.verbose:
            print " ".join(cmd)

        p      = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        ret    = p.returncode
        if ret != 0:
            print "=== multicrabLumiCalc.py:\n\t Call to", cmd[0] , "failed with return value %d with command" % ret
            print " ".join(cmd)
            print output
            return 1
        if opts.verbose:
            print output


        lines = output.split("\n")
        lumi  = -1.0
        unit  = None
        for line in lines:
            m = unit_re.search(line)
            if m:
                unit = m.group("unit")

            m = lumi_re.search(line)
            if m:
                lumi = float(m.group("recorded")) # lumiCalc2.py returns pb^-1

        if unit == None:
            raise Exception("Didn't find unit information from lumiCalc output, command was %s" % " ".join(cmd))
        lumi = convertLumi(lumi, unit)
        data.update( doPileUp(task, jsonFile, lumi) )


    intLumi = GetIntLumi(data)
    print "{:<80} {:<12} {:<6}".format( "\t ", intLumi, "pb^-1")

    if len(data) > 0:
        f = open(opts.output, "wb")
        json.dump(data, f, sort_keys=True, indent=2)
        f.close()

    return 0


def doPileUp(task, jsonFile, lumi):
    '''
    '''
    data     = {}
    fOUT     = os.path.join(task, "results", "PileUp.root")
    pucmd    = ["pileupCalc.py","-i", jsonFile,"--inputLumiJSON",PileUpJSON,"--calcMode","true","--minBiasXsec","80000","--maxPileupBin","50","--numPileupBins","50",fOUT]
    pu       = subprocess.Popen(pucmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    puoutput = pu.communicate()[0]
    puret = pu.returncode
    if puret != 0:
        print "Call to",pucmd[0],"failed with return value %d with command" % puret
        print " ".join(pucmd)
        print puoutput
        return puret
    
    if task == None:
        print "File %s recorded luminosity %f pb^-1" % (jsonFile, lumi)
    else:
        # print "Task %s recorded luminosity %f pb^-1" % (task, lumi)
         
        print "{:<80} {:<12} {:<6}".format( "\t " + TruncateString(task, 68), lumi, "pb^-1")    
        data[task] = lumi
        
    # Save the json file after each data task in case of future errors
    if len(data) > 0:
        f = open(opts.output, "wb")
        json.dump(data, f, sort_keys=True, indent=2)
        f.close()
    return data


def GetIntLumi(data):
    intLumi = 0.0
    for key in data:
        intLumi += data[key]
    return intLumi


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)

    parser.add_option("-f", dest="files", type="string", action="append", default=[], help="JSON files to calculate the luminosity for (this or -d is required)")
    parser.add_option("--output"   , dest="output"  , default="lumi.json", type="string" , help="Output file to write the dataset integrated luminosities")
    parser.add_option("--truncate" , dest="truncate", default=False, action="store_true" , help="Truncate the output file before writing")
    parser.add_option("--noreport ", dest="report"  , default=True , action="store_false", help="Do not run 'crab -report' [you guarantee that lumiSummary.json contains all jobs]")
    parser.add_option("--verbose"  , dest="verbose" , default=False, action="store_true" , help="Print outputs of the commands which are executed")
    parser.add_option("--lumiCalc1"    , dest="lumicalc", action="store_const", const="lumiCalc1"    , help="Use lumiCalc.py instead of lumiCalc2.py")
    parser.add_option("--lumiCalc2"    , dest="lumicalc", action="store_const", const="lumiCalc2"    , help="Use lumiCalc2.py [default is to use pixelLumiCalc.py]")
    parser.add_option("--pixelLumiCalc", dest="lumicalc", action="store_const", const="pixelLumiCalc", help="Use pixelLumiCalc.py instead of lumiCalc2.py [default]")

    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)
    
    if opts.lumicalc == None:
        opts.lumicalc = "brilcalc"
    print "=== multicrabLumiCalc.py:\n\t Calculating luminosity with %s" % opts.lumicalc
    print "\t Calculating pileup with pileupCalc"

    sys.exit( main(opts, args) )
