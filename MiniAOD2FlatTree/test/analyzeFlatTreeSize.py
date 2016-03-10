#!/usr/bin/env python
# http://wlav.web.cern.ch/wlav/pyroot/
###############################################################
### All imported modules
###############################################################
import ROOT
import os
import sys
import numpy
import math

###############################################################
### Options here
###############################################################
#filePath    = "/afs/cern.ch/work/a/attikis/multicrab/multicrab_CMSSW752_Default_06Mar2016_20h39m12s/"
#datasets    = ["MuonEG_Run2015D_05Oct2015_v2_246908_260426_25ns_Silver"]
filePath    = "/afs/cern.ch/user/a/attikis/scratch0/CMSSW_7_5_2/src/UCYHiggsAnalysis/MiniAOD2FlatTree/test/"
datasets    = ["test2"]
outFileName = "treeInfo.log"
treeName    = "Events"

def GetObjectByName(fileIn, objectName):
    '''
    '''

    # For-loop: Over all keys in file
    for key in fileIn.GetListOfKeys():    

        # Skip if object name is wrong
        keyName = key.GetName()
        if (keyName!= treeName):
            continue
        else:
            o = fileIn.Get(keyName)
            return o
    raise Exception("Could not find object with name '%s' in input ROOT file with name '%s'." % ( objectName, fileIn.GetName() ) )


def OpenTFile(filePath, dataset, fileName, mode):
    '''
    '''
    fullPath = filePath + dataset + "/results/" + fileName
    return ROOT.TFile.Open(fullPath, mode, fileName, 1, 0)
            

def CreateFile(filePath, fileName, fileMode, titleLines, ):
    '''
    '''
    if (filePath.endswith("/") == False):
        filePath = filePath + "/"

    # Create the file
    f = open(filePath + fileName , fileMode)

    # Write the title lines (if any)
    for l in titleLines:
        f.write(l)

    return f

###############################################################
if __name__ == "__main__":

    # For-loop: All datasets
    for dataset in datasets:
        inFileName  = "miniAOD2FlatTree-%s.root" % (dataset)

        # Open ROOT file
        print "=== analyzeFlatTreeSize.py:\n\t Opening ROOT file \"%s\"" % (filePath + inFileName)
        fileIn = OpenTFile(filePath, dataset, inFileName, "READ")

        # Get the TTree    
        treeIn = GetObjectByName(fileIn, treeName) #treeIn = fileIn.Get(treeName)
    
        # For-loop: All TBranches in the TTree
        treeBranches   = treeIn.GetListOfBranches()
        bName_to_bSize = {}
        bNames         = []
        bSizes         = []
        totalSize_MB   = 0
        basketSize_MB  = 0;
        nEntries       = treeIn.GetEntries()

        # For-loop: All TTree branches
        for b in treeBranches:
            totalSize_MB  += b.GetTotalSize() * 1e-06
            basketSize_MB += b.GetBasketSize() * 1e-06

        # For-loop: All TTree branches
        for b in treeBranches:

            # Get the values
            bName   = b.GetName()
            bSize   = b.GetTotalSize()
            
            # Savee the names/size
            bNames.append(bName)
            bSizes.append((bSize * 1e-06)/(totalSize_MB)*100)
            bName_to_bSize[bName] = (bSize * 1e-06)/(totalSize_MB)*100

        # Sort the two lists according to the bSizes list (descding order)
        from operator import itemgetter
        bSizes, bNames = [list(x) for x in zip(*sorted(zip(bSizes, bNames), key=itemgetter(0), reverse=True))]

        # Create a txt file
        title     = []
        hLine     = '='*90
        txtAlign  = '\n{:<65}  {:>10}  {:>5}'
        titleLine = txtAlign.format("TBranch", "Size", "Units")
        title.append(" "*30 + dataset)
        title.append("\n" + hLine)
        title.append(titleLine)
        title.append("\n" + hLine)
        fileOut = CreateFile(os.getcwd(), "treeSize.txt", "a", title)

        # For-loop: All dictionary keys/values
        for bName, bSize in zip(bNames, bSizes):
            bSize = bName_to_bSize[bName]
        
            # Convert to kilo-bytes before saving and Keep only two decimals
            bSize   = '%0.3f' % (bSize)
            newLine = txtAlign.format(bName, bSize, "%")

            # Write line to file
            fileOut.write(newLine)

        # Write final lines
        lastLine_1a = txtAlign.format("Total Size"         , '%0.2f' % (totalSize_MB) , "MB")
        lastLine_1b = txtAlign.format("Basket Size "       , '%0.2f' % (basketSize_MB), "MB")
        lastLine_2a = txtAlign.format("Total Size  / Event", '%0.2f' % ((totalSize_MB/nEntries)*1e+03), "kB")
        lastLine_2b = txtAlign.format("Basket Size / Event", '%0.2f' % ((basketSize_MB/nEntries)*1e+03), "kB")
        # 
        fileOut.write(lastLine_1a)
        fileOut.write(lastLine_1b)
        fileOut.write(lastLine_2a)
        fileOut.write(lastLine_2b)
        fileOut.write("\n" + hLine + "\n")
        fileOut.write("\n")
        
    # Close file
    fileOut.close()

