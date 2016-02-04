'''
'''
#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import os
import copy
import glob
import ConfigParser

import ROOT

import UCYHiggsAnalysis.NtupleAnalysis.tools.OrderedDict as OrderedDict
import UCYHiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import UCYHiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.aux as m_aux

#================================================================================================ 
# Global Definitions
#================================================================================================
# Default command line options
_optionDefaults = {
    "input": "histograms-*.root",
    }


#================================================================================================ 
# Class Definition
#================================================================================================ 
class Multicrab(object): 
    '''
    '''
    def __init__(self, verbose=False):
        self.bVerbose = verbose
        return


    def Verbose(self, messageList=None):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.bVerbose == True:
            print "*** %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
            if messageList==None:
                return
            else:
                for message in messageList:
                    print "\t", message
        return


    def Print(self, messageList=[""]):
        '''
        Custome made print system. Will print all messages in the messageList
        even if the verbosity boolean is set to false.
        '''
        print "*** %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        for message in messageList:
            print "\t", message
        return



    def GetResultsDirPath(self, pathToProbe):
        '''
        '''
        self.Verbose()
        
        resDirs = ["res", "results"]
        path    = None

        # For-loop: All possible dir names
        for r in resDirs:
            resDir = os.path.join(pathToProbe, r )
            if os.path.exists( resDir ):
                path = resDir
                break
            
        if path == None:
            self.Print(["ERROR! Could not find a %s directory under %s%s/" % (" or ".join("\"" + r + "\"" for r in resDirs), multicrabDir, item)])
            exit(-1)
        else:
            self.Print(["Found the results dir under %s " % path])
            return path


    def GetRootFile(self, path, fName, mode="r"):
        '''
        '''
        self.Verbose()

        rootFile = None
        # Determined if item is a ROOT file        
        if fName.startswith("histograms-") and fName.endswith(".root"):
            rootFile = fName
        else:
            return rootFile

        # Open the ROOT file (read mode)
        filePath = os.path.join(path, rootFile)
        rootFile = ROOT.TFile.Open( filePath, mode)
        self.Print(["Read ROOT file %s" % filePath])
        return rootFile


    def GetModulesList(self, rootFile, prefix):
        '''
        '''
        self.Verbose()

        # Print list of keys of ROOT File
        if self.bVerbose:
            rootFile.GetListOfKeys().Print()
        
        myList = []
        # For-loop: All Keys in ROOT file
        for key in rootFile.GetListOfKeys():
            cName   = key.GetClassName()
            objName = key.ReadObj().GetName()
            if not cName == "TDirectoryFile":
                continue
            if not objName.startswith(prefix):
                continue
            myList.append(objName)

        # Close ROOT file
        rootFile.Close()
        return myList
                

    def FindModuleNames(self, multicrabDir, prefix):
        '''
        '''
        self.Verbose()
        self.Print(["{:<15} {:<20}".format("Directory", ": " + multicrabDir), "{:<15} {:<20}".format("Prefix", ": "+ prefix)])

        # Get all items under multicrabDir (files & dirs)
        items = os.listdir(multicrabDir)
        self.Verbose([items])

        # For-loop: Items under multicrabDir
        for i in items:
            
            tmpDir = os.path.join(multicrabDir, i)

            # Skip items which are not of type "directory"
            if not os.path.isdir( tmpDir ):
                continue 

            # Get the results path
            path = self.GetResultsDirPath( tmpDir )
                
            # Get all items under path (files & dir)
            newItems = os.listdir(path)
            self.Verbose([newItems])

            # For-loop: Items under multicrabDir/res (or multicrabDir/results)
            for j in newItems:

                # Find the ROOT file(s)
                f = self.GetRootFile(path, j)
                if f == None:
                    continue
                
                # Print list of keys of ROOT File
                if self.bVerbose:
                    f.GetListOfKeys().Print()
                
                # Get Module Names
                return self.GetModulesList(f, prefix)

        # If nothing found return empty list
        return []


    def GetDatasetsFromMulticrabDirs(self, multiDirs, **kwargs):
        '''
        Construct DatasetManager from a list of MultiCRAB directory names.
        
        \param multiDirs   List of strings or pairs of strings of the MultiCRAB
        directories (relative to the working directory). If the item of the list
        is pair of strings, the first element is the directory, and the second 
        element is the postfix for the dataset names from that directory.
        
        \param kwargs      Keyword arguments (forwarded to GetDatasetsFromMulticrabCfg())
        
        \return DatasetManager object
        '''
        self.Verbose()

        if "cfgfile" in kwargs:
            raise Exception("'cfgfile' keyword argument not allowed")
        if "namePostfix" in kwargs:
            raise Exception("'namePostfix' keyword argument not allowed")
        
        datasets = dataset.DatasetManager()
        
        # For-loop: All multiCRAB directories
        for d in multiDirs:
            self.Print(["Accessing dataset ", d])
            if isinstance(d, str):
                dset = self.GetDatasetsFromMulticrabCfg(directory=d, **kwargs)
            else:
                dset = self.GetDatasetsFromMulticrabCfg(directory=d[0], namePostfix=d[1], **kwargs)
                
            datasets.extend(dset)
        return datasets


    def GetDatasetsFromMulticrabCfg(self, **kwargs):
        '''
        Construct DatasetManager from a multicrab.cfg
        
        \param kwargs   Keyword arguments (see below)
        
        All keyword arguments are forwarded to ReadFromMulticrabCfg()
        
        All keyword arguments <b>except</b> the ones below are forwarded to
        DatasetManagerCreator.createDatasetManager()
        
        \li \a directory
        \li \a cfgfile
        \li \a excludeTasks
        \li \a includeOnlyTasks
        \li \a namePostfix
        
        \return DatasetManager object
        
        \see dataset.ReadFromMulticrabCfg()
        '''
        self.Verbose()

        _args = copy.copy(kwargs)

        # For-loop: All argument names in list
        for argName in ["directory", "cfgfile", "excludeTasks", "includeOnlyTasks", "namePostfix"]:
            try:
                del _args[argName]
            except KeyError:
                pass

        managerCreator = self.ReadFromMulticrabCfg(**kwargs)
        return managerCreator.createDatasetManager(**_args)


    def GetDatasetManagersFromMuldicrabDirs(self, multicrabDir, analysisNames):
        '''
        '''
        self.Verbose()

        # For-loop: All analysis names
        for aName in analysisNames:
            datasets = self.GetDatasetsFromMulticrabDirs([multicrabDir], analysisName=aName)
        return datasets


    def ReadFromMulticrabCfg(self, **kwargs):
        '''
        Construct DatasetManagerConstructor from a multicrab.cfg
        
        \param kwargs   Keyword arguments (see below)
        
        <b>Keyword arguments</b>
        \li \a opts              Optional OptionParser object. Should have options added with addOptions() and multicrab.addOptions()
        \li \a directory         Directory where to look for \a cfgfile
        \li \a cfgfile           Path to the multicrab.cfg file (for default, see GetTaskDirectories())
        \li \a excludeTasks      String, or list of strings, to specify regexps
        
        If a dataset name matches to any of the regexps, Dataset object is not constructed for that. 
        Conflicts with \a includeOnlyTasks 
        
        \li \a includeOnlyTasks  String, or list of strings, to specify regexps. Only datasets whose name matches to any of the regexps are kept. 
        Conflicts with \a excludeTasks
        
        \li Rest are forwarded to readFromCrabDirs()
        
        \return DatasetManagerCreator object 
        The section names in multicrab.cfg are taken as the dataset names in the DatasetManager object.
        '''
        self.Verbose()
        
        taskDirs = []
        dirname = ""
        opts    = kwargs.get("opts", None)
    
        if "directory" in kwargs or "cfgfile" in kwargs:
            _args = {}
            if "directory" in kwargs:
                dirname = kwargs["directory"]
                _args["directory"] = dirname
            if "cfgfile" in kwargs:
                _args["filename"] = kwargs["cfgfile"]
                dirname = os.path.dirname(os.path.join(dirname, kwargs["cfgfile"]))
            taskDirs = self.GetTaskDirectories(opts, **_args)
        else:
            taskDirs = self.GetTaskDirectories(opts)

        aux      = m_aux.AuxClass(self.bVerbose)
        taskDirs = aux.IncludeExcludeTasks(taskDirs, **kwargs)
        taskDirs.sort()        
        managerCreator = self.ReadFromCrabDirs(taskDirs, baseDirectory=dirname, **kwargs)        
        return managerCreator


    def ReadFromCrabDirs(self, taskdirs, emptyDatasetsAsNone=False, **kwargs):
        '''
        Construct DatasetManagerCreator from a list of CRAB task directory names
        
        \param taskdirs     List of strings for the CRAB task directories (relative to the working directory)
        
        \param emptyDatasetsAsNone  If true, in case of no datasets return None instead of raising an Exception (default False)
        
        \param kwargs       Keyword arguments (see below)
        
        <b>Keyword arguments</b>, all are also forwarded to ReadFromRootFiles()
        
        \li \a opts         Optional OptionParser object. Should have options added with addOptions()
        
        \li \a namePostfix  Postfix for the dataset names (default: '')OB
        
        \return DatasetManagerCreator object
        
        The basename of the task directories are taken as the dataset names in the DatasetManagerCreator object 
        (e.g. for directory '../Foo', 'Foo' will be the dataset name)
        '''
        self.Verbose()
        
        inputFile = None
        if "opts" in kwargs:
            opts = kwargs["opts"]
            inputFile = opts.input
        else:
            inputFile = _optionDefaults["input"]
        
        postfix = kwargs.get("namePostfix", "")
        dlist   = []
        noFiles = False

        # For-loop: All task directories
        for d in taskdirs:                    
            resdir = os.path.join(d, "res")
            name   = os.path.basename(d)

            if os.path.exists(resdir): # CRAB2
                files = glob.glob(os.path.join(resdir, inputFile))
            else: # CRAB3
                files = glob.glob(os.path.join(d, "results", inputFile))
                name = name.replace("crab_", "")

            self.Verbose(["files = %s " % (files), "name = %s "  %(name)])
            if len(files) == 0:
                print >> sys.stderr, "=== multicrab.py:\n\t Ignoring dataset %s: no files matched to '%s' in task directory %s" % (d, inputFile, os.path.join(d, "res"))
                noFiles = True
                continue

            dlist.append( (name+postfix, files) )

        if noFiles:
            print >> sys.stderr, ""
            print >> sys.stderr, "=== multicrab.py:\n\t There were datasets without files. Have you merged the files with hplusMergeHistograms.py?"
            print >> sys.stderr, ""
            if len(dlist) == 0:
                raise Exception("multicrab.py:\n\t No datasets. Have you merged the files with hplusMergeHistograms.py?")

        if len(dlist) == 0:
            if emptyDatasetsAsNone:
                return None
            raise Exception("multicrab.py:\n\t No datasets from CRAB task directories %s" % ", ".join(taskdirs))

        return self.ReadFromRootFiles(dlist, **kwargs)
            

    def ReadFromRootFiles(self, rootFileList, **kwargs):
        '''
        Construct DatasetManagerCreator from a list of CRAB task directory names
        
        \param rootFileList  List of (\a name, \a filenames) pairs (\a name should be string, \a filenames can 
        be string or list of strings). \a name is taken as the dataset name, and \a filenames as the path(s) to 
        the ROOT file(s). Forwarded to DatasetManagerCreator.__init__()
                                                                       
        \param kwargs        Keyword arguments (see below), all forwarded to DatasetManagerCreator.__init__()
        
        <b>Keyword arguments</b>
        \li \a opts          Optional OptionParser object. Should have options added with addOptions().
        
        \return DatasetManagerCreator object
        
        If \a opts exists, and the \a opts.listAnalyses is set to True, list all available analyses
        (with DatasetManagerCreator.printAnalyses()), and exit.
        '''
        self.Verbose()

        creator = dataset.DatasetManagerCreator(rootFileList, **kwargs)
        if "opts" in kwargs and kwargs["opts"].listAnalyses:
            creator.printAnalyses()
            sys.exit(0)
        return creator


    def GetTaskDirectories(self, opts, filename="multicrab.cfg", directory=""):
        '''
        '''
        self.Verbose()

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
                taskNames = self.GetTaskDirectories_CRAB2(fname)
                dirname   = os.path.dirname(fname)
                taskNames = [os.path.join(dirname, task) for task in taskNames]
            else:
                taskNames = self.GetTaskDirectories_CRAB3(directory)
 
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
            self.Verbose(["taskNames = ", taskNames])
            return taskNames


    def GetTaskDirectories_CRAB3(self, directory):
        '''
        '''
        self.Verbose()

        dirs = glob.glob(os.path.join(directory, "*"))
        dirs = filter(lambda d: os.path.isdir(d), dirs)
        return dirs


    def GetTaskDirectories_CRAB2(self, filename):
        '''
        '''
        self.Verbose()
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
