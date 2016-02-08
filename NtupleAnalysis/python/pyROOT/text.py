#================================================================================================
# All imported modules
#================================================================================================
import os, sys
import array
import math
import copy
import inspect
import glob
from optparse import OptionParser

import ROOT


#================================================================================================
# Define class here
#================================================================================================
class TextClass(object):
    def __init__(self, xPos=0.0, yPos=0.0, text="", size=None, bold=False, align="left", color=ROOT.kBlack, verbose = False):
        self.verbose = verbose
        self.xPos    = xPos
        self.yPos    = yPos
        self.text    = text
        self.tlatex  = ROOT.TLatex()
        self.tlatex.SetNDC()
        if not bold:
            self.tlatex.SetTextFont(self.tlatex.GetTextFont()-20) # bold -> normal
        if size != None:
            self.tlatex.SetTextSize(size)
        if align.lower() == "left":
            self.tlatex.SetTextAlign(11)
        elif align.lower() == "center":
            self.tlatex.SetTextAlign(21)
        elif align.lower() == "right":
            self.tlatex.SetTextAlign(31)
        else:
            raise Exception("Error: Invalid option '%s' for text alignment! Options are: 'left', 'center', 'right'." % align)
        self.tlatex.SetTextColor(color)
        self._SetDefaults("lumi"       , xPos=0.64, yPos=0.955, text = "")
        self._SetDefaults("energy"     , xPos=0.80, yPos=0.955, text = "")
        self._SetDefaults("preliminary", xPos=0.18, yPos=0.955, text = "#font[62]{CMS} #font[52]{Preliminary}")
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
        print "*** %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
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


    def _SetDefaults(self, name, **kwargs):
        self.Verbose()

        # Set all arguments and their values
        for argument, value in kwargs.iteritems():
            setattr(self, name + "_" + argument, value)
        return


    def _GetValues(self, name):
        self.Verbose()

        xPos = getattr(self, name + "_xPos" )
        yPos = getattr(self, name + "_yPos" )
        text = getattr(self, name + "_text" )
        return (xPos, yPos, text)


    def Draw(self, options=None):
        self.Verbose()

        self.tlatex.DrawLatex(self.xPos, self.yPos, str(self.text) )
        return


    def AddEnergyText(self, energy=""):
        self.Verbose()

        (_x, _y, _text) = self._GetValues("energy")
        self.AddText(_x, _y, "(" + energy + " TeV)" )
        return
    

    def AddLumiText(self, lumi):
        self.Verbose()

        (_x, _y, _text) = self._GetValues("lumi")
        self.AddText(_x, _y, lumi)
        return


    def AddPreliminary(self, text=""):
        self.Verbose()

        (_x, _y, _text) = self._GetValues("preliminary")
        self.AddText(_x, _y, _text)
        return
    

    def AddText(self,xPos, yPos, text, *args, **kwargs):
        self.Verbose()

        t = TextClass(xPos, yPos, text, *args, **kwargs)
        t.Draw()
        return
