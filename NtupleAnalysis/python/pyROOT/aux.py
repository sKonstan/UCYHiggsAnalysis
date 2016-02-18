#================================================================================================
# All imported modules
#================================================================================================
import os, sys
import array
import math
import copy
import inspect
import glob
import time
from optparse import OptionParser
import itertools

from itertools import tee, izip

import ROOT


#================================================================================================
# Class Definition
#================================================================================================
class AuxClass(object):
    '''
    '''
    def __init__(self, verbose=False):
        self.verbose   = verbose
        self.timerDict = {}
        return
        
    def SetAttribute(self, attr, value):
        self.Verbose()
        return setattr(self, attr, value)

    
    def GetAttribute(self, attr):
        self.Verbose()
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise Exception("Class object '%s' does not have attribute '%s'" % (self.GetSelfName(), attr))

    def Verbose(self, message=""):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.verbose:
            print "=== %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
            if message!="":
                print "\t", message
        return


    def Print(self, message=""):
        '''
        Custome made print system. Will print the message even if the verbosity boolean is set to false.
        '''
        print "=== %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        if message!="":
            print "\t", message
        return

    
    def PrintList(self, messageList=[""], printSelf=True):
        '''
        Custome made print system. Will print all messages in the messageList even if the verbosity boolean is set to false.
        '''
        for counter, message in enumerate(messageList):
            if counter == 0 and printSelf:
                self.Print(message)
            else:
                print "\t", message
        return


    def PrintWarning(self, msg, keystroke):
        '''                                                                                                                                                          
        Print a warning and make sure user sees it by requiring a keystroke
        '''
        self.Print()
        
        response = raw_input("\t" + msg + ". Press \"%s\" to quit, any other key to proceed: " % (keystroke))
        if response== "q":
            sys.exit()
        else:
            return
        return
    
        
    def PrintAttributes(self):
        '''
        Call this function to print all class attributes.
        '''
        self.Print("Attributes: %s" % (self.__dict__))
        return


    def StartTimer(self, name):
        '''
        '''
        self.Verbose()

        if isinstance(name, str):
            if name in self.timerDict:
                raise Exception("A counter with name '%s' already exists!" % (name))
            else:
                self.timerDict[name] = time.time()
        else:
            raise Exception("The parameter '%s'  is not a string, but of type '%s'" % (str(name), type(name)))
        return

    
    def PrintTimers(self):
        '''
        Print the time elapses since the creation of the plotter object.
        
        '''
        self.Verbose()

        info   = []
        align  = "{:<20} {:<20} {:<20} {:<20}"
        header = align.format("Timer Name", "Elapsed Time", "Start Time", "Finish Time")
        hLine  = "="*len(header)
        info.append(hLine)
        info.append(header)
        info.append(hLine)
        
        # For-loop: All timers and calculate start, finish and elapsed time
        for cName, cTime in self.timerDict.iteritems():
            (sTime, fTime, eTime, units) = self._CalculateTimer(cName)
            elapsed  = "%0.2f %s" % (eTime, units)
            start    = sTime
            finish   = fTime
            
            info.append( align.format(cName, elapsed, start, finish) )

        self.PrintList(info)
        return
    

    def _CalculateTimer(self, name):
        '''
        Print the time elapses since the creation of the plotter object.        
        '''
        self.Verbose()

        start   = self.timerDict[name]
        finish  = time.time()
        elapsed = finish - start
        
        sTime        = time.strftime('%H:%M:%S', time.localtime(start))
        fTime        = time.strftime('%H:%M:%S', time.localtime(finish))
        eTime, units = self._ConvertElapsedTimeT(elapsed)
        return sTime, fTime, eTime, units


    def _ConvertElapsedTimeT(self, elapsed):
        '''
        Print the time elapses since the creation of the plotter object.
        
        '''
        self.Verbose()

        if elapsed < 60:
            return elapsed, "secs"
        elif elapsed > 60 and elapsed < 3600:
            return elapsed/60.0, "mins"
        else:
            return elapsed/3600.0, "hours"
        
    
    def GetKeyFromDictValue(self, value, dictionary):
        '''
        Return the key from a dictionary given its value
        '''
        self.Verbose()
        
        myKey = None
        for key in dictionary:
            if dictionary[key] == value:
                myKey = key
            else:
                pass
        if myKey == None:
            raise Exception( "Could not find key='%s' for value='%s' in dictionary='%s'. Make sure these exist." % (myKey, value, dictionary) )
        else:
            pass
        return myKey



    def Get(self, tdir, name):
        '''
        http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=15496

        This one seems to save quite a lot of "garbage collection" time
        '''
        self.Verbose("Getting %s from %s" % (name, tdir.GetName()))

        o = tdir.Get(name)
        if o == None:
            return o
        
        ROOT.SetOwnership(o, True)
        if hasattr(o, "SetDirectory"):
            o.SetDirectory(0)
        return o


    def Divide(self, numerator, denominator):
        '''
        Safely divide two numbers without worrying about division by zero.
        '''
        self.Verbose()
        
        if (denominator <= 0):
            self.Print("WARNING! Could not proceed with the division '%s/%s'. Returning zero." % numerator, denominator)
            return 0
        else:
            return float(numerator)/float(denominator)


    def Efficiency(self, nPass, nTotal, errType = "binomial"):
        '''
        Get efficiency given the number of events passing and the total number of events.
        Return efficiency and associated error.
        '''
        self.Verbose()
        
        if nTotal == 0:
            eff = 0
            err = 0
            return eff, err
        
        eff = self.Divide(nPass, nTotal)
        if errType == "binomial":
            #errSquared = nTotal*eff*(1-eff) #eff*(1-eff)/nTotal #bug?
            #err        = math.sqrt(errSquared)
            variance = eff*(1-eff)/nTotal
            err      = math.sqrt(variance)
        else:
            raise Exception( "Only the 'binomial' error type is supported at the moment.")
        self.Verbose("eff = '%s' +/- '%s'" % (eff, err))

        return eff, err
            


    def SaveListsToFile(self, filePath, columnWidths, columnTitles, columnValues, nDecimals=3, delimiter = "~", align = " c ", bLatexTable = True):
        '''
        '''
        self.Verbose()
        
        ### Definitions
        hLine = r"\hline" + "\n"

        ### Open file in write ("w") mode
        if os.path.exists(filePath) == True:
            self.Print( ["WARNING! File '%s' already exists!" % (filePath)] )
        f = open(filePath, "w")
        
        nColumnWidths = len(columnWidths)
        nColumnTitles = len(columnTitles)
        nColumnValues = len(columnValues)
        if( (nColumnWidths != nColumnTitles) or ( nColumnWidths!= nColumnValues) or (nColumnTitles != nColumnValues) ):
            raise Exception("Number of column-widths ('%s'), column-titles ('%s') and number of column-values ('%s') differ!" % (nColumnWidths, nColumnTitles, nColumnValues) )

        nColumns = nColumnValues
        nRows    = len(columnValues[0])
            
        ### Define the template formate
        template = ""
        for i in range(0, nColumns):
            if i != nColumns-1:
                template += "{" + str(i) + ":" + str(columnWidths[i]) + "} %s " % (delimiter)
            else:
                template += "{" + str(i) + ":" + str(columnWidths[i]) + "}"
                
        ### Create the header of the file
        header = template.format(*columnTitles)

        ### Writ eteh header
        if (bLatexTable):
            f.write(r"\begin{table}" + "\n")
            f.write(r"\centering" + "\n")
            f.write(r"\begin{tabular}{%s}" % (align * nColumns) + "\n")
            f.write(hLine)
            f.write(header + r"\\" + "\n")
            f.write(hLine)
        else:
            f.write(header + "\n")
        
        ### Loop over all rows
        for r in range(0, nRows):
            row = []

            ### Loop over all columns
            for c in range(0, nColumns):
                valuesList = columnValues[c]
                rowText    = valuesList[r]
                
                ### Round floats to a max of nDecimals
                if type(rowText) == float:
                    rowText = str( round(valuesList[r], nDecimals) )
                else:
                    rowText = str( valuesList[r] )
                
                ### Append row to a list
                row.append(rowText)

            ### Create the line for this row and format it as desired
            rowLine = template.format(*row)

            self.Verbose( ["Writing line: %s " % (rowLine) ] )
            if (bLatexTable):
                f.write(rowLine + r"\\" + "\n")
            else:
                f.write(rowLine + "\n")

        ### Close file and return
        if (bLatexTable):
            f.write(hLine)
            f.write(r"\end{tabular}" + "\n")
            f.write(r"\end{table}")
        f.close()

        return



    def ReadListsFromFile(self, filePath, delimiter = "~"):
        '''
        '''
        self.Verbose()

        if os.path.exists(filePath) == False:
            raise Exception("File '%s' does not exist! Please make sure the provided path for the file is correct." % (filePath) )

        ### Declarations
        ignoreList = ["begin{table}", "centering", "begin{tabular}", "hline", "end{tabular}", "end{table}"]
        removeList = ["\\", "\n", " "]
        lineList   = []
        nColumns   = 0

        self.Print("FilePath: %s, Delimiter: %s'" % (filePath, delimiter))
        ### Loop over all lines in myFile
        with open(filePath) as f:

            ### Loop over all lines
            for line in f:

                ### Skip latex-table related stuff
                if any(ext in line for ext in ignoreList):
                    continue
                else:
                    pass

                ### Save this line to a list (after removing unwanted characters)
                for char in removeList:
                    line = line.replace(char, "")
                lineList.append(line)

                ### Determine the number of columns
                if nColumns == 0:
                    nColumns = len(line.split(delimiter))

        ### Create list of columnLists
        listOfLists = []

        ### Loop over all columns
        for c in range(0, nColumns):
            columnList  = []
            
            ### Loop over all lines (rows)
            for l in lineList:
                columns = l.split(delimiter, nColumns)
                column  = columns[c]
                columnList.append(column)

            ### Append column to listOfLists
            listOfLists.append(columnList)

        return listOfLists



    def SaveDictOfListsToFile(self, mySavePath, fileName, dictOfLists, maxDecimals = 3):
        '''
        '''
        self.Verbose()

        self.Print("FileName: %s, MaxDecimals: '%s'" % (fileName, maxDecimals))

        ### Declarations
        myFile = open( mySavePath+fileName, 'w')
        template  = ""
        iRow      = ""
        iColumn   = ""

        ### Write to file
        for iKey in dictOfLists:
            iList = dictOfLists[iKey]
            
            ### Treat differently if all elements in the list are float or strings
            myFile.write(iKey)

            if all(isinstance(item, str) for item in iList): 
                myFile.write( "".join(iList) + "\n")
            else:
                formatted = [format(iEntry, maxDecimals) for iEntry in iList]
                myFile.write(str(formatted) + "\n")
        myFile.close()
        return


    def ConvertStringToList(self, string):
        '''
        '''
        self.Verbose()
        theList = string.replace("\n", "").replace("[", "").replace("]","").replace("'","").replace(" ","").split(",")

        return theList


    def ConvertListElementsToFloat(self, myList):
        '''
        '''
        self.Verbose()
        theList = [ float(item) for item in myList ]

        return theList


    def AdjacentPairForLoop(self, iterable):
        '''
        iterate through pairs of items in python list:
        s -> (s0,s1), (s1,s2), (s2, s3), ...

        Example use:
        import aux as m_aux

        AuxObject = m_aux.AuxClass(verbose=True)
        for x1, x2 in AuxObject.AdjacentPairForLoop(xVals):
                diff = abs( x1 - x2).q
        '''
        self.Verbose()
        
        a, b = tee(iterable)
        next(b, None)
        return izip(a, b)


    def ConvertHistoToCounter(self, histo, printCounter=True):
        '''
        Transform histogram (TH1) to a list of (name, Count) pairs.
        The name is taken from the x axis label and the count is Count object with value and (statistical) uncertainty.        
        '''
        self.Verbose()

        if not isinstance(histo, ROOT.TH1):
            self.Print("The 'histo' parameter provided (%s) is not an instance of ROOT.TH1. EXIT" % (histo) )
            sys.exit()
            
        ret    = []
        nBinsX = histo.GetNbinsX()+1;
        for bin in xrange(0, nBinsX):
            name        = histo.GetXaxis().GetBinLabel(bin)
            countObject = Count(float(histo.GetBinContent(bin)), float(histo.GetBinError(bin)))
            ret.append( (name, countObject) )

        if not printCounter:
            return ret
        
        # Useful for debugging purposes
        rows   = []
        header = "{:^15} {:^50} {:^15}".format("Bin Number", "Bin Label", "Entries")
        hLine  = "="*len(header)
        title  = histo.GetTitle()        
        rows.append("")
        rows.append("{:^80}".format(title))
        rows.append(hLine)
        rows.append(header)
        rows.append(hLine)        
        for i, c in enumerate(ret): 
            row = "{:^15} {:<50} {:>15}".format(str(i), ret[i][0], str(ret[i][1].value()) )
            rows.append(row)
        rows.append(hLine)
        rows.append("")
        
        # Print the counter
        for r in rows:
            print r
        return ret


#================================================================================================
# Class Definition
#================================================================================================
class Count:
    '''
    Represents counter count value with uncertainty.
    '''
    def __init__(self, value, uncertainty=0.0, systUncertainty=0.0, verbose=False):
        '''
        Constructor
        '''
        self.verbose          = verbose
        self._value           = value
        self._uncertainty     = uncertainty
        self._systUncertainty = systUncertainty
        self.Verbose()
        return


    def Verbose(self, message=""):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if not self.verbose:
            return
        
        print "%s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        print "\t", message
        return


    def Print(self, message=""):
        '''
        Custome made print system. Will print the message even if the verbosity boolean is set to false.
        '''
        print "=== %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        print "\t", message
        return

    
    def PrintList(self, messageList=[""]):
        '''
        Custome made print system. Will print all messages in the messageList even if the verbosity boolean is set to false.
        '''        
        for counter, message in enumerate(messageList):
            if counter == 0:
                self.Print(message)
            else:
                print "\t", message
        return


    def SetVerbose(self, verbose):
        '''
        Manually enable/disable verbosity.
        '''
        self.verbose = verbose
        return

    
    def copy(self):
        self.Verbose()
        return Count(self._value, self._uncertainty, self._systUncertainty)


    def clone(self):
        self.Verbose()
        return self.copy()

    
    def value(self):
        self.Verbose()
        return self._value

    
    def uncertainty(self):
        self.Verbose()
        return self._uncertainty

    
    def uncertaintyLow(self):
        self.Verbose()
        return self.uncertainty()

    
    def uncertaintyHigh(self):
        self.Verbose()
        return self.uncertainty()

    
    def systUncertainty(self):
        self.Verbose()
        return self._systUncertainty

    
    def add(self, count):
        self.Verbose()
        
        self._value += count._value
        self._uncertainty = math.sqrt(self._uncertainty**2 + count._uncertainty**2)
        self._systUncertainty = math.sqrt(self._systUncertainty**2 + count._systUncertainty**2)
        return

    
    ## self = self - count
    def subtract(self, count):
        self.Verbose()
        
        self.add(Count(-count._value, count._uncertainty, count._systUncertainty))
        return
        

    ## self = self * count
    def multiply(self, count):
        '''
        '''
        self.Verbose()

        self._systUncertainty = math.sqrt( (count._value * self._systUncertainty)**2 +
                                       (self._value  * count._systUncertainty)**2 )
        self._uncertainty = math.sqrt( (count._value * self._uncertainty)**2 +
                                       (self._value  * count._uncertainty)**2 )
        self._value = self._value * count._value
        return

    
    ## self = self / count
    def divide(self, count):
        '''
        '''
        self.Verbose()
        
        self._systUncertainty = math.sqrt( (self._systUncertainty / count._value)**2 +
                                       (self._value*count._systUncertainty / (count._value**2) )**2 )
        self._uncertainty = math.sqrt( (self._uncertainty / count._value)**2 +
                                       (self._value*count._uncertainty / (count._value**2) )**2 )
        self._value = self._value / count._value
        return
        

#================================================================================================
# Function Definitions
#================================================================================================
def format(value, maxDecimals):
    '''
    '''
    if type(value)==float:
        return str( round( value , maxDecimals) )
    elif type(value)==int:
        return str( round( float(value) , maxDecimals) )
    else:
        raise Exception("ERROR! A float or int is required but got a '%s' instead with value '%s'" % (type(value), value))
        return str(value)

    
