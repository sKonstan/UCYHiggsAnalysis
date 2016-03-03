'''
As the name indicates this modules is the main file loaded in all analysis 
scripts for histogram creation.

It contains basic and auxiliary  methods and classes for creating analyzers, adding datasets
and customising the workflow.

Example (import):
from UCYHiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
'''

#================================================================================================
# Imports
#================================================================================================
import os
import time
import copy
import json

import ROOT

import datasets as datasets
import UCYHiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import UCYHiggsAnalysis.NtupleAnalysis.tools.aux as aux
import UCYHiggsAnalysis.NtupleAnalysis.tools.git as git


#================================================================================================
# ROOT Configurations
#================================================================================================
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

#================================================================================================
# Class Definition
#================================================================================================
class PSet:
    def __init__(self, **kwargs):
        self.__dict__["_data"] = copy.deepcopy(kwargs)
        return
    
    def clone(self, **kwargs):
        pset = PSet(**self._data)
        for key, value in kwargs.iteritems():
            setattr(pset, key, value)
        return pset

    def __getattr__(self, name):
        return self._data[name]

    def __hasattr__(self, name):
        return name in self._data.keys()

    def __setattr__(self, name, value):
        self.__dict__["_data"][name] = value
        return

    def _asDict(self):
        data = {}
        for key, value in self._data.iteritems():
            if isinstance(value, PSet):
                # Support for json dump of PSet
                data[key] = value._asDict()
            elif isinstance(value, list):
                # Support for json dump of list of PSets
                myList = []
                for item in value:
                    if isinstance(item, PSet):
                        myList.append(item._asDict())
                    else:
                        myList.append(item)
                data[key] = myList
            else:
                data[key] = value
        return data

    def __str__(self):
        return self.serialize_()

    def __repr__(self):
        return self.serialize_()

    def serialize_(self):
        return json.dumps(self._asDict(), sort_keys=True, indent=2)


def File(fileName):
    fullpath = os.path.join(aux.higgsAnalysisPath(), fileName)
    if not os.path.exists(fullpath):
        raise Exception("=== main.py:\n\t The file '%s' does not exist" % self._fullpath)
    return fullpath

#================================================================================================
# Class Definition
#================================================================================================
class Analyzer:
    def __init__(self, className, **kwargs):
        self.__dict__["_className"] = className
        silentStatus = True

        if "silent" in kwargs:
            silentStatus = kwargs["silent"]
            del kwargs["silent"]

        if "config" in kwargs:
            if isinstance(kwargs["config"], PSet):
                self.__dict__["_pset"] = kwargs["config"]
            else:
                raise Exception("=== main.py:\n\t The keyword config should be used only for providing the parameters as a PSet!")
        else:
            self.__dict__["_pset"] = PSet(**kwargs)

        if not silentStatus:
            print "=== main.py:\n\t Configuration parameters:"
            print self.__dict__["_pset"]

    def __getattr__(self, name):
        return getattr(self._pset, name)

    def __hasattr__(self, name):
        return hasattr(self._pset, name)

    def __setattr__(self, name, value):
        setattr(self.__dict__["_pset"], name, value)

    def exists(self, name):
        return name in self._pset._asDict()

    def className_(self):
        return self.__dict__["_className"]

    def config_(self):
        return self.__dict__["_pset"].serialize_()

#================================================================================================
# Class Definition
#================================================================================================
class AnalyzerWithIncludeExclude:

    def __init__(self, analyzer, **kwargs):
        self._analyzer = analyzer
        if len(kwargs) > 0 and (len(kwargs) != 1 or not ("includeOnlyTasks" in kwargs or "excludeTasks" in kwargs)):
            raise Exception("AnalyzerWithIncludeExclude expects exactly 1 keyword argument, which is 'includeOnlyTasks' or 'excludeTasks'")
        self._includeExclude = {}
        self._includeExclude.update(kwargs)

    def getAnalyzer(self):
        return self._analyzer

    def runForDataset_(self, datasetName):
        if len(self._includeExclude) == 0:
            return True
        tasks = aux.includeExcludeTasks([datasetName], **(self._includeExclude))
        return len(tasks) == 1


#================================================================================================
# Class Definition
#================================================================================================
class DataVersion:

    def __init__(self, dataVersion):
        self._version = dataVersion
        self._isData  = "data" in self._version
        self._isMC    = "mc" in self._version

    def __str__(self):
        return self._version

    def isData(self):
        return self._isData

    def isMC(self):
        return self._isMC

    def is53X(self):
        return "53X" in self._version

    def is74X(self):
        return "74X" in self._version

    def isS10(self):
        return self._isMC() and "S10" in self._version


#================================================================================================
# Class Definition
#================================================================================================
class Dataset:
    def __init__(self, name, files, dataVersion, lumiFile, pileup, nAllEvents):
        self._name        = name
        self._files       = files
        self._dataVersion = DataVersion(dataVersion)
        self._lumiFile    = lumiFile
        self._pileup      = pileup
        self._nAllEvents  = nAllEvents

    def getName(self):
        return self._name

    def getFileNames(self):
        return self._files

    def getDataVersion(self):
        return self._dataVersion

    def getLumiFile(self):
        return self._lumiFile

    def getPileUp(self):
        return self._pileup
      
    def getNAllEvents(self):
        return self._nAllEvents


#================================================================================================
# Class Definition
#================================================================================================
class Process:

    def __init__(self, outputPrefix="analysis", outputPostfix="", maxEvents=-1, verbose=False):
        ROOT.gSystem.Load("libHPlusAnalysis.so") #attikis xenios
        self._outputPrefix    = outputPrefix
        self._outputPostfix   = outputPostfix
        self._datasets        = []
        self._analyzers       = {}
        self._datasetStats    = {}
        self._maxEvents       = maxEvents
        self._options         = PSet()
        self._verbose         = verbose
        self._realTimeTotal   = 0
        self._cpuTimeTotal    = 0
        self._readMbytesTotal = 0
        self._callsTotal      = 0

        return

    def addDataset(self, name, files=None, dataVersion=None, lumiFile=None):
        '''
        Adds dataset and stores its attributes (name, files, dataVersion,
        and associated luminosity file). All dataset properties are also
        determined (PileUp, nEvts).
        '''

        # Get the files
        if files is None:
            files = datasets.getFiles(name)

        # Get precursor for dataset
        precursor = dataset.DatasetPrecursor(name, files)

        # Get the dataset version
        if dataVersion is None:
            dataVersion = precursor.getDataVersion()

        # Get dataset properties
        pileUp     = precursor.getPileUp()
        nAllEvents = precursor.getNAllEvents()
        precursor.close()

        # Append the dataset
        self._datasets.append( Dataset(name, files, dataVersion, lumiFile, pileUp, nAllEvents) )
        return

    def addDatasets(self, names):
        '''
        No explicit files possible here
        '''       
        for name in names:
            if self._verbose:
                print "=== main.py:\n\t Adding dataset '%s'" % (name)
            self.addDataset(name)
        return

    def addDatasetsFromMulticrab(self, directory, *args, **kwargs):
        '''
        '''
        dataset._optionDefaults["input"] = "miniAOD2FlatTree*.root"
        dsetMgrCreator = dataset.readFromMulticrabCfg(directory=directory, *args, **kwargs)
        datasets = dsetMgrCreator.getDatasetPrecursors()
        dsetMgrCreator.close()

        # For-loop: All datasets
        for dset in datasets:
            name        = dset.getName()
            fileNames   = dset.getFileNames()
            dataVer     = dset.getDataVersion()
            lumi        = dsetMgrCreator.getLumiFile()

            if self._verbose:
                print "=== main.py:\n\t Adding dataset to self with following properties:"
                attr = '{:<15} {:<40}\n {:<15} {:<40}\n {:<15} {:<40}\n {:<15} {:<40}'.format("\t dataset", ": " + name, "\t files", ": " + ",".join(fileNames), "\t data-version", ": "+dataVer, "\t lumi-file", ": " + lumi)
                print attr
            self.addDataset(name, fileNames, dataVersion=dataVer, lumiFile=lumi)
        return

    # kwargs for 'includeOnlyTasks' or 'excludeTasks' to set the datasets over which this analyzer is processed, default is all datasets
    def addAnalyzer(self, name, analyzer, **kwargs):
        if self.hasAnalyzer(name):
            raise Exception("Analyzer '%s' already exists" % name)

        if self._verbose:
            print "=== main.py:\n\t Added Analyzer with name '%s'" % (name)
        self._analyzers[name] = AnalyzerWithIncludeExclude(analyzer, **kwargs)
        return

    # FIXME: not sure if these two actually make sense
    def getAnalyzer(self, name):
        if not self.hasAnalyzer(name):
            raise Exception("Analyzer '%s' does not exist" % name)
        return self._analyzers[name].getAnalyzer()

    def removeAnalyzer(self, name):
        if not self.hasAnalyzer(name):
            raise Exception("Analyzer '%s' does not exist" % name)
        del self._analyzers[name]

    def hasAnalyzer(self, name):
        return name in self._analyzers

    def addOptions(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self._options, key, value)

    def run(self, proof=False, proofWorkers=None):
        '''
        '''
        outputDir = self._outputPrefix + "_" + time.strftime("%d%b%Y_%Hh%Mm%Ss") #time.strftime("%y%m%d_%H%M%S")
        if self._outputPostfix != "":
            outputDir += "_"+self._outputPostfix

        # Create output directory
        if self._verbose:
            print "=== main.py:\n\t Creating directory '%s'" % (outputDir) 

        os.mkdir(outputDir)
        multicrabCfg = os.path.join(outputDir, "multicrab.cfg")
        f = open(multicrabCfg, "w")

        # For-loop: All datasets
        for dset in self._datasets:
            f.write("[%s]\n\n" % dset.getName())
        f.close()

        # Copy/merge lumi files
        lumifiles = set([d.getLumiFile() for d in self._datasets])
        lumidata = {}
        for fname in lumifiles:
            if not os.path.exists(fname):
                continue
            f = open(fname)
            data = json.load(f)
            f.close()
            for k in data.keys():
                if k in lumidata:
                    raise Exception("Luminosity JSON file %s has a dataset for which the luminosity has already been loaded; please check the luminosity JSON files\n%s" % (fname, k, "\n".join(lumifiles)))
            lumidata.update(data)
        if len(lumidata) > 0:
            f = open(os.path.join(outputDir, "lumi.json"), "w")
            json.dump(lumidata, f, sort_keys=True, indent=2)
            f.close()

            # Add run range in a json file, if runMin and runMax in pset
            rrdata = {}
            for aname, analyzerIE in self._analyzers.iteritems():
                ana = analyzerIE.getAnalyzer()
                if hasattr(ana, "__call__"):
                    for dset in self._datasets:
                        if dset.getDataVersion().isData():
                            ana = ana(dset.getDataVersion())
                            if ana.__getattr__("runMax") > 0:
                                rrdata[aname] = "%s-%s"%(ana.__getattr__("runMin"),ana.__getattr__("runMax"))
                                break
            if len(rrdata) > 0:
                f = open(os.path.join(outputDir, "runrange.json"), "w")
                json.dump(rrdata, f, sort_keys=True, indent=2)
                f.close()

        # Setup proof if asked
        _proof = None
        if proof:
            opt = ""
            if proofWorkers is not None:
                opt = "workers=%d"%proofWorkers
            _proof = ROOT.TProof.Open(opt)
            _proof.Exec("gSystem->Load('libHPlusAnalysis.so');")
        
        # Sum data PU distributions
        hPUs = {}

        # For-loop: All analyzers
        for aname, analyzerIE in self._analyzers.iteritems():
            hPU = None
            # For-loop: All datasets
            for dset in self._datasets:
                if dset.getDataVersion().isData() and analyzerIE.runForDataset_(dset.getName()):
                    if hPU is None:
                        hPU = dset.getPileUp()
                    else:
                        hPU.Add(dset.getPileUp())
            if hPU != None:
                hPU.SetName("PileUpData")
                hPUs[aname] = hPU
            #else:
            #    raise Exception("Cannot determine PU spectrum for data!")
 
        # Process over datasets
        ndset = 0
        # For-loop: All datsets
        for dset in self._datasets:
            ndset               += 1
            inputList            = ROOT.TList()
            nanalyzers           = 0
            anames               = []
            usePUweights         = False
            useTopPtCorrection   = False
            nAllEventsPUWeighted = 0.0
            
            # For-loop: All analyzers
            for aname, analyzerIE in self._analyzers.iteritems():
                if analyzerIE.runForDataset_(dset.getName()):
                    nanalyzers += 1
                    analyzer = analyzerIE.getAnalyzer()
                    if hasattr(analyzer, "__call__"):
                        analyzer = analyzer(dset.getDataVersion())
                        if analyzer is None:
                            raise Exception("=== main.py:\n\t Analyzer '%s' was specified as a function, but returned None" % aname)
                        if not isinstance(analyzer, Analyzer):
                            raise Exception("=== main.py:\n\t Analyzer '%s' was specified as a function, but returned object of '%s' instead of Analyzer" % (aname, analyzer.__class__.__name__))
                    inputList.Add(ROOT.TNamed("analyzer_"+aname, analyzer.className_()+":"+analyzer.config_()))

                    # ttbar status for top pt corrections
                    ttbarStatus = "0"
                    useTopPtCorrection = analyzer.exists("useTopPtWeights") and analyzer.__getattr__("useTopPtWeights")
                    # useTopPtCorrection = useTopPtCorrection and dset.getName().startswith("TTJets")
                    useTopPtCorrection = useTopPtCorrection and dset.getName().lower().startswith("tt")
                    if useTopPtCorrection:
                        ttbarStatus = "1"
                    inputList.Add(ROOT.TNamed("isttbar", ttbarStatus))

                    # Pileup reweighting
                    if dset.getDataVersion().isMC():

                        if aname in hPUs.keys():
                            if self._verbose:
                                for k in range(hPUs[aname].GetNbinsX()):
                                    print "=== main.py:\n\t DEBUG(PUreweighting): dataPU:%d:%f"%(k+1, hPUs[aname].GetBinContent(k+1))
                            inputList.Add(hPUs[aname])
                        else:
                            n = 50
                            hFlat = ROOT.TH1F("dummyPU" + aname,"dummyPU" + aname, n, 0, n)
                            hFlat.SetName("PileUpData")
                            for k in range(n):
                                hFlat.Fill(k+1, 1.0/n)
                            inputList.Add(hFlat)
                            hPUs[aname] = hFlat
                            print "=== main.py:\n\t WARNING! Using a flat PU spectrum for data (which is missing). The MC PU spectrum is unchanged."

                        if dset.getPileUp() == None:
                            raise Exception("=== main.py:\n\t Error: PU spectrum is missing from dataset! Please switch to using newest multicrab!")
                        hPUMC = dset.getPileUp().Clone()

                        if aname not in hPUs.keys():
                            print "===main.py:\n\t The key '%s' does not exist in dictionary variable 'hPUs'. Continue" % (aname)
                            continue

                        if hPUMC.GetNbinsX() != hPUs[aname].GetNbinsX():
                            raise Exception("=== main.py:\n\t Pileup histogram dimension mismatch! data nPU has %d bins and MC nPU has %d bins"%(hPUs[aname].GetNbinsX(), hPUMC.GetNbinsX()))
                        hPUMC.SetName("PileUpMC")
                        if self._verbose:
                            for k in range(hPUMC.GetNbinsX()):
                                print "=== main.py:\n\t Debug(PUreweighting): MCPU:%d:%f"%(k+1, hPUMC.GetBinContent(k+1))
                        inputList.Add(hPUMC)
                        if analyzer.exists("usePileupWeights"):
                            usePUweights = analyzer.__getattr__("usePileupWeights")
                            if hPUs[aname].Integral() > 0.0:
                                factor = hPUMC.Integral() / hPUs[aname].Integral()
                                for k in range(0, hPUMC.GetNbinsX()+2):
                                    if hPUMC.GetBinContent(k) > 0.0:
                                        w = hPUs[aname].GetBinContent(k) / hPUMC.GetBinContent(k) * factor
                                        nAllEventsPUWeighted += w * hPUMC.GetBinContent(k)
                    anames.append(aname)
            if nanalyzers == 0:
                print "=== main.py:\n\t Skipping %s, no analyzers" % dset.getName()
                continue

            print "=== main.py:\n\t Processing dataset (%d/%d): " % (ndset, len(self._datasets))
            info  = '{:<20} {:<40}'.format("\t Dataset", ": " + dset.getName())
            info += '\n{:<20} {:<40}'.format("\t Is Data", ": " + str(dset.getDataVersion().isData()) )

            if dset.getDataVersion().isData():
                lumivalue = "--- not available in lumi.json (or lumi.json not available) ---"
                if dset.getName() in lumidata.keys():
                    lumivalue = lumidata[dset.getName()]
                info  += '\n{:<20} {:<40}'.format("\t Luminosity", ": " + str(lumivalue) + " [pb-1]")
            else:
                info += '\n{:<20} {:<40}'.format("\t Luminosity", ": -")

            # PileUp Weights
            info  += '\n{:<20} {:<40}'.format("\t Pile-Up Weights", ": " + str(usePUweights))

            # Top pT Corrections
            info  += '\n{:<20} {:<40}'.format("\t Top-pT Weights", ": " + str(useTopPtCorrection))

            # Print combined information
            print info
            
            resDir      = os.path.join(outputDir, dset.getName(), "res")
            resFileName = os.path.join(resDir, "histograms-%s.root" % dset.getName())
            os.makedirs(resDir)
            tchain = ROOT.TChain("Events")

            if self._verbose:
                print "=== main.py:"
            # For-loop: All dataset files
            for f in dset.getFileNames():
                if self._verbose:
                    print "\t Adding file '%s' to TChain" % (f)
                tchain.Add(f)
            tchain.SetCacheLearnEntries(100);

            tselector = ROOT.SelectorImpl()

            # FIXME: TChain.GetEntries() is needed only to give a time estimate for the analysis. 
            # If this turns out to be slow, we could store the number of events along the file names    
            # inputList.Add(ROOT.SelectorImplParams(tchain.GetEntries(), dset.getDataVersion().isMC(), self._options.serialize_(), True))
            inputList.Add(ROOT.TNamed("entries", str(tchain.GetEntries())))
            if dset.getDataVersion().isMC():
                inputList.Add(ROOT.TNamed("isMC", "1"))
            else:
                inputList.Add(ROOT.TNamed("isMC", "0"))
            inputList.Add(ROOT.TNamed("options", self._options.serialize_()))
            inputList.Add(ROOT.TNamed("printStatus", "1"))

            if _proof is not None:
                tchain.SetProof(True)
                inputList.Add(ROOT.TNamed("PROOF_OUTPUTFILE_LOCATION", resFileName))
            else:
                inputList.Add(ROOT.TNamed("OUTPUTFILE_LOCATION", resFileName))

            if self._verbose:
                print "=== main.py:"
            for counter, i in enumerate(inputList):
                if self._verbose:
                    print "\t inputList[%s] = %s" % (counter, i.GetName())
            tselector.SetInputList(inputList)

            readBytesStart = ROOT.TFile.GetFileBytesRead()
            readCallsStart = ROOT.TFile.GetFileReadCalls()
            timeStart = time.time()
            clockStart = time.clock()

            if self._maxEvents > 0:
                tchain.SetCacheEntryRange(0, self._maxEvents)
                tchain.Process(tselector, "", self._maxEvents)
            else:                
                tchain.Process(tselector)

            timeStop      = time.time()
            clockStop     = time.clock()
            readCallsStop = ROOT.TFile.GetFileReadCalls()
            readBytesStop = ROOT.TFile.GetFileBytesRead()

            # Obtain Nall events for top pt corrections
            NAllEventsTopPt = 0
            if useTopPtCorrection:
                for inname in dset.getFileNames():
                    fIN = ROOT.TFile.Open(inname)
                    h = fIN.Get("configInfo/topPtWeightAllEvents")
                    if h != None:
                        binNumber = 2 # nominal
                        if hasattr(analyzer, "topPtSystematicVariation"):
                            variation = getattr(analyzer, "topPtSystematicVariation")
                            if variation == "minus":
                                binNumber = 0
                            # FIXME: The bin is to be added to the ttrees
                            #elif variation == "plus":
                                #binNumber = 3
                                #if not h.GetXaxis().GetBinLabel().endsWith("Plus"):
                                    #raise Exception("This should not happen")
                        if binNumber > 0:
                            NAllEventsTopPt += h.GetBinContent(binNumber)
                    else:
                        print "=== main.py:\n\tWARNING! Could not obtain N(AllEvents) for top pt reweighting"
                    fIN.Close()

            # Write configInfo
            fIN = ROOT.TFile.Open(dset.getFileNames()[0])
            cinfo = fIN.Get("configInfo/configinfo")
            tf = ROOT.TFile.Open(resFileName, "UPDATE")
            configInfo = tf.Get("configInfo")
            if configInfo == None:
                configInfo = tf.mkdir("configInfo")
            configInfo.cd()
            dv = ROOT.TNamed("dataVersion", str(dset.getDataVersion()))
            dv.Write()
            cv = ROOT.TNamed("codeVersionAnalysis", git.getCommitId())
            cv.Write()
            if not cinfo == None:
                # Add more information to configInfo
                n = cinfo.GetNbinsX()
                cinfo.SetBins(n+3, 0, n+3)
                cinfo.GetXaxis().SetBinLabel(n+1, "isData")
                cinfo.GetXaxis().SetBinLabel(n+2, "isPileupReweighted")
                cinfo.GetXaxis().SetBinLabel(n+3, "isTopPtReweighted")

                # Add "isData" column
                if not dset.getDataVersion().isMC():
                    cinfo.SetBinContent(n+1, cinfo.GetBinContent(1))

                # Add "isPileupReweighted" column
                if usePUweights:
                    cinfo.SetBinContent(n+2, nAllEventsPUWeighted / nanalyzers)

                # Add "isTopPtReweighted" column
                if useTopPtCorrection:
                    cinfo.SetBinContent(n+3, NAllEventsTopPt / nanalyzers)
                # Write
                cinfo.Write()
                fIN.Close()

            # Sum skim counters counters (from ttree)
            hSkimCounterSum = None
            fINs = None
            for inname in dset.getFileNames():
                fIN = ROOT.TFile.Open(inname)
                hSkimCounters = fIN.Get("configInfo/SkimCounter")
                if hSkimCounterSum == None:
                    hSkimCounterSum = hSkimCounters.Clone()
                else:
                    hSkimCounterSum.Add(hSkimCounters)
                if fINs == None:
                    fINs = []
                fINs.append(fIN)
            if hSkimCounterSum != None:
                # Find out directories in the output file
                dirlist = []
                for key in tf.GetListOfKeys():
                    matchStatus = False
                    for name in anames:
                        if key.GetTitle().startswith(name):
                            dirlist.append(key.GetTitle())
                # Add skim counters to the counter histograms
                for d in dirlist:
                    hCounter = tf.Get("%s/counters/counter"%d).Clone()
                    hCounterWeighted = tf.Get("%s/counters/weighted/counter"%d).Clone()
                    # Resize axis
                    nCounters = hCounter.GetNbinsX()
                    nSkimCounters = hSkimCounterSum.GetNbinsX()
                    hCounter.SetBins(nCounters+nSkimCounters, 0., nCounters+nSkimCounters)
                    hCounterWeighted.SetBins(nCounters+nSkimCounters, 0., nCounters+nSkimCounters)
                    # Move bin data to right
                    for i in range(0, nCounters):
                        j = nCounters-i
                        hCounter.SetBinContent(j+nSkimCounters, hCounter.GetBinContent(j))
                        hCounter.SetBinError(j+nSkimCounters, hCounter.GetBinError(j))
                        hCounter.GetXaxis().SetBinLabel(j+nSkimCounters, hCounter.GetXaxis().GetBinLabel(j))
                        hCounterWeighted.SetBinContent(j+nSkimCounters, hCounterWeighted.GetBinContent(j))
                        hCounterWeighted.SetBinError(j+nSkimCounters, hCounterWeighted.GetBinError(j))
                        hCounterWeighted.GetXaxis().SetBinLabel(j+nSkimCounters, hCounterWeighted.GetXaxis().GetBinLabel(j))
                    # Add skim counters
                    for i in range(1, nSkimCounters+1):
                        hCounter.SetBinContent(i, hSkimCounterSum.GetBinContent(i))
                        hCounter.SetBinError(i, hSkimCounterSum.GetBinError(i))
                        hCounter.GetXaxis().SetBinLabel(i, "ttree: %s"%hSkimCounterSum.GetXaxis().GetBinLabel(i))
                        hCounterWeighted.SetBinContent(i, hSkimCounterSum.GetBinContent(i))
                        hCounterWeighted.SetBinError(i, hSkimCounterSum.GetBinError(i))
                        hCounterWeighted.GetXaxis().SetBinLabel(i, "ttree: %s"%hSkimCounterSum.GetXaxis().GetBinLabel(i))
                    hCounter.Sumw2(False)
                    hCounter.Sumw2()
                    hCounterWeighted.Sumw2(False)
                    hCounterWeighted.Sumw2()
                    tf.cd("%s/counters"%d)
                    hCounter.Write("counter", ROOT.TObject.kOverwrite)
                    tf.cd("%s/counters/weighted"%d)
                    hCounterWeighted.Write("counter", ROOT.TObject.kOverwrite)
            if fINs != None:
                for f in fINs:
                  f.Close()
            tf.Close()

            calls = 0
            if _proof is not None:
                tchain.SetProof(False)
                queryResult = _proof.GetQueryResult()
                cpuTime     = queryResult.GetUsedCPU()
                readMbytes  = queryResult.GetBytes()/1024/1024
            else:
                cpuTime    = clockStop-clockStart
                readMbytes = float(readBytesStop-readBytesStart)/1024/1024
                calls      = int(readCallsStop-readCallsStart)
            
            self.CalculateStatistics(dset.getName(), timeStart, timeStop, cpuTime, readMbytes, calls)
        
        self.PrintStatisticsTotal()
        if self._verbose:
            print "=== main.py:\n\t Results are in '%s'" % (outputDir)
        return outputDir


    def CalculateStatistics(self, dataset, timeStart, timeStop, cpuTime, readMbytes, calls, bPrintStats=False, bPrintTotalStats=False):
        '''
        Prints a table summarising the CPU usage and time elapsed since job started.
        '''
        realTime = timeStop-timeStart

        # Create statistics list
        stats = []
        stats.append("%s"      % (dataset)   )
        stats.append("%.2f"    % (realTime)   )
        stats.append("%.2f"    % (cpuTime)    )
        stats.append("%.1f"    % (cpuTime/realTime*100) )
        stats.append("%.2f"    % (readMbytes) )
        stats.append("%s"      % (calls)      )
        stats.append("%.2f"    % (readMbytes/realTime)  )

        # Save the stats
        self._datasetStats[dataset] = stats

        heading = "{:<40} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("\t Dataset", "Real Time [s]", "CPU Time [s]", "CPU Time [%]", "Read [MB]", "File Reads [Calls]", "Read Speed [MB/s]")
        values  = "{:<40} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("\t " + stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6])
        hLine   = len(values)*"="

        if bPrintStats:
            print "=== main.py:"
            print "\t", hLine
            print heading
            print "\t", hLine
            print values
            
        # Calculations (Total)
        self._realTimeTotal   += realTime
        self._cpuTimeTotal    += cpuTime
        self._readMbytesTotal += readMbytes
        self._callsTotal      += calls

        if len(self._datasets) > 1 and bPrintTotalStats==True:
            self.PrintStatisticsTotal(bPrintTableLayout=False)
        return


    def PrintStatisticsTotal(self, bPrintTableLayout=True):
        '''
        Prints a table summarising the CPU usage and time elapsed for all jobs (datasets).
        '''
        # Create total statistics list
        stats = []
        stats.append("TOTAL") 
        stats.append("%.2f"    % (self._realTimeTotal)   )
        stats.append("%.2f"    % (self._cpuTimeTotal)    )
        stats.append("%.1f"    % (self._cpuTimeTotal/self._realTimeTotal*100) )
        stats.append("%.2f"    % (self._readMbytesTotal) )
        stats.append("%s"      % (self._callsTotal)      )
        stats.append("%.2f"    % (self._readMbytesTotal/self._realTimeTotal)  )

        heading = "{:<40} {:>20} {:>20} {:>20} {:>20} {:>20} {:>20}".format("\t Dataset", "Real Time [s]", "CPU Time [s]", "CPU Time [%]", "Read [MB]", "File Reads [Calls]", "Read Speed [MB/s]")
        values  = "{:<40} {:>20} {:>20} {:>20} {:>20} {:>20} {:>20}".format("\t " + stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6])
        hLine   = len(values)*"="

        print "=== main.py:"
        if bPrintTableLayout:
            print "\t", hLine
        print heading
        if bPrintTableLayout:
            print "\t", hLine
        for key, value in self._datasetStats.iteritems():
            dStats = value
            dVals  = "{:<40} {:>20} {:>20} {:>20} {:>20} {:>20} {:>20}".format("\t " + dStats[0], dStats[1], dStats[2], dStats[3], dStats[4], dStats[5], dStats[6])
            print dVals
        print values
        return


if __name__ == "__main__":
    import unittest

    class TestPSet(unittest.TestCase):
        def testConstruct(self):
            d = {"foo": 1, "bar": 4}
            a = PSet(**d)
            self.assertEqual(a.foo, 1)
            self.assertEqual(a.bar, 4)
            d["foo"] = 5
            self.assertEqual(a.foo, 1)

        def testClone(self):
            a = PSet(foo=1, bar=4)
            b = a.clone()
            self.assertEqual(b.foo, a.foo)
            self.assertEqual(b.bar, a.bar)
            a.foo = 5
            self.assertEqual(a.foo, 5)
            self.assertEqual(b.foo, 1)

            c = a.clone(foo=10, xyzzy=42)
            self.assertEqual(a.foo, 5)
            self.assertEqual(c.foo, 10)
            self.assertEqual(c.xyzzy, 42)

        def testRecursive(self):
            a = PSet(foo=1, bar=PSet(a=4, b="foo"))
            self.assertEqual(a.foo, 1)
            self.assertEqual(a.bar.a, 4)
            self.assertEqual(a.bar.b, "foo")

        def testSet(self):
            a = PSet()
            a.foo = 1
            a.bar = "foo"

            setattr(a, "xyzzy", 42)

            self.assertEqual(a.foo, 1)
            self.assertEqual(a.bar, "foo")
            self.assertEqual(a.xyzzy, 42)

        def testSerialize(self):
            a = PSet(foo=1, bar=PSet(a=0.5, b="foo"))
            a.xyzzy = 42
            setattr(a, "fred", 56)
            self.assertEqual(a.serialize_(), """{
  "bar": {
    "a": 0.5, 
    "b": "foo"
  }, 
  "foo": 1, 
  "fred": 56, 
  "xyzzy": 42
}""")
        def testSerializeListOfPSet(self):
            a = PSet(foo=1, bar=[PSet(a=0.5),PSet(a=0.7)])
            self.assertEqual(a.serialize_(), """{
  "bar": [
    {
      "a": 0.5
    }, 
    {
      "a": 0.7
    }
  ], 
  "foo": 1
}""")

    class TestFile(unittest.TestCase):
        def testConstruct(self):
            f = File("NtupleAnalysis/python/main.py")
            self.assertEqual(f, os.path.join(aux.higgsAnalysisPath(), "NtupleAnalysis/python/main.py"))
            self.assertRaises(Exception, File, "NtupleFoo")

        def testSerialize(self):
            a = PSet(foo=File("NtupleAnalysis/python/main.py"))
            self.assertEqual(a.serialize_(), """{
  "foo": "%s/NtupleAnalysis/python/main.py"
}""" % aux.higgsAnalysisPath())


    class TestAnalyzer(unittest.TestCase):
        def testConstruct(self):
            a = Analyzer("Foo", foo=1, bar="plop", xyzzy = PSet(fred=42))
            self.assertEqual(a.className_(), "Foo")
            self.assertEqual(a.foo, 1)
            self.assertEqual(a.bar, "plop")
            self.assertEqual(a.xyzzy.fred, 42)
            self.assertEqual(a.config_(), """{
  "bar": "plop", 
  "foo": 1, 
  "xyzzy": {
    "fred": 42
  }
}""")

        def testModify(self):
            a = Analyzer("Foo", foo=1)
            self.assertEqual(a.foo, 1)

            a.bar = "plop"
            a.foo = 2
            setattr(a, "xyzzy", PSet(a=10))
            self.assertEqual(a.foo, 2)
            self.assertEqual(a.bar, "plop")
            self.assertEqual(a.xyzzy.a, 10)
            self.assertEqual(a.config_(), """{
  "bar": "plop", 
  "foo": 2, 
  "xyzzy": {
    "a": 10
  }
}""")

            a.xyzzy.a = 20
            self.assertEqual(a.xyzzy.a, 20)

            setattr(a, "xyzzy", 50.0)
            self.assertEqual(a.xyzzy, 50.0)

    class TestAnalyzerWithIncludeExclude(unittest.TestCase):
        def testIncludeExclude(self):
            a = AnalyzerWithIncludeExclude(None, includeOnlyTasks="Foo")
            self.assertEqual(a.runForDataset_("Foo"), True)
            self.assertEqual(a.runForDataset_("Bar"), False)
            self.assertEqual(a.runForDataset_("Foobar"), True)

            a = AnalyzerWithIncludeExclude(None, excludeTasks="Foo")
            self.assertEqual(a.runForDataset_("Foo"), False)
            self.assertEqual(a.runForDataset_("Bar"), True)
            self.assertEqual(a.runForDataset_("Foobar"), False)

    class TestProcess(unittest.TestCase):

        def testAnalyzer(self):
            p = Process()
            p.addAnalyzer("Test1", Analyzer("FooClass", foo=1))
            p.addAnalyzer("Test2", Analyzer("FooClass", foo=2))

            self.assertEqual(len(p._analyzers), 2)
            self.assertTrue(p.hasAnalyzer("Test1"))
            self.assertTrue(p.hasAnalyzer("Test2"))
            self.assertFalse(p.hasAnalyzer("Test3"))

            self.assertEqual(p.getAnalyzer("Test1").foo, 1)
            self.assertEqual(p.getAnalyzer("Test2").foo, 2)

            p.removeAnalyzer("Test2")
            self.assertEqual(len(p._analyzers), 1)
            self.assertTrue(p.hasAnalyzer("Test1"))
            self.assertFalse(p.hasAnalyzer("Test2"))

        def testOptions(self):
            p = Process()
            p.addOptions(Foo = "bar", Bar = PSet(x=1, y=2.0))

            self.assertEqual(p._options.Foo, "bar")
            self.assertEqual(p._options.Bar.x, 1)
            self.assertEqual(p._options.Bar.y, 2)

            p.addOptions(Foo = "xyzzy", Plop = PSet(x=1, b=3))

            self.assertEqual(p._options.Foo, "xyzzy")
            self.assertEqual(p._options.Plop.x, 1)
            self.assertEqual(p._options.Plop.b, 3)

        def testSelectorImpl(self):
            t = ROOT.SelectorImpl()

            # dummy test
            self.assertEqual(isinstance(t, ROOT.TSelector), True)

    unittest.main()
