'''
Cross sections from:
 [1] PREP
 [2] https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingSummer2011
 [3] from https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
 [4] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
 [5] https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopMC2011
 [6] https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopSigma
 [7] https://twiki.cern.ch/twiki/bin/view/CMS/UCYHiggsToTauTauWorkingHCP2012#53X_MC_Samples
 [8] https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopSigma8TeV (other useful page https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopMC2012)
 [9] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
[10] http://arxiv.org/abs/1303.6254
[11] https://twiki.cern.ch/twiki/bin/viewauth/CMS/UCYHiggsToTauTauWorkingSummer2013
[12] https://twiki.cern.ch/twiki/bin/view/CMS/TmdRecipes
[13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
[14] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV / GenXSecAnalyzer
[15] McM
[16] https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#TT_X
[17] https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt8TeV
[18] https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV
[19] https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR
[20] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopHiggsGeneration13TeV
[21] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
[22] https://twiki.cern.ch/twiki/pub/CMS/SingleTopHiggsGeneration13TeV/tHQ_cross_sections.txt
[23] https://indico.cern.ch/event/476022/session/11/contribution/25/attachments/1217408/1778610/SashaLHCHXSWGreport.pdf


Usage Example:
from UCYHiggsAnalysis.NtupleAnalysis.pyROOT.crossSection import xSections
print xSections.crossSection("QCD_Pt_30to50", "8")
'''

#================================================================================================
# Imports
#================================================================================================
import sys


#================================================================================================
# Class Definition
#================================================================================================
class CrossSection:
    '''
    Cross section of a single process (physical dataset)
    '''
    def __init__(self, name, energyDictionary, verbose=False):
        '''
        The parameter "name" is the Name of the physics process. The parameter "energyDictionary" is 
        a  Dictionary of energy -> cross section (energy as string in TeV, cross section as float in pb)
        '''
        self.verbose    = verbose
        self.name       = name
        self.energyDict = {}
        for key, value in energyDictionary.iteritems():
            setattr(self, key, value)
        return


    def Verbose(self, messageList=None):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.verbose:
            print "=== %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
            if messageList==None:
                return
            else:
                for message in messageList:
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


    def Get(self, energy):
        '''
        Get the cross section for the given energy (in TeV)
        '''
        try:
            return getattr(self, energy)
        except AttributeError:
            msg = "No cross section set for process %s for energy %s. EXIT" % (self.name, energy)
            self.Print(msg)
            sys.exit()
        
        return


#================================================================================================
# Class Definition
#================================================================================================
class CrossSectionList:
    '''
    ## List of CrossSection objects
    '''
    def __init__(self, *args):
        self.crossSections = args[:]
        return

    
    def crossSection(self, name, energy):
        for obj in self.crossSections:
            if name == obj.name:
                return obj.Get(energy)
        return None


#================================================================================================    
xSections = CrossSectionList(
    CrossSection("QCD_Pt_30to50", {
        "7": 5.312e+07,   #  [2]
        "8": 6.6285328e7, #  [1]
        "13": 161500000., # [12]
    }),
    CrossSection("QCD_Pt_50to80", {
        "7": 6.359e+06,  #  [2]
        "8": 8148778.0,  #  [1]
        "13": 22110000., # [12]
    }),
    CrossSection("QCD_Pt_80to120", {
        "7": 7.843e+05,  #  [2]
        "8": 1033680.0,  #  [1]
        "13": 3000114.3, # [12]
    }),
    CrossSection("QCD_Pt_120to170", {
        "7": 1.151e+05, #  [2]
        "8": 156293.3,  #  [1]
        "13": 493200.,  # [12] # McM: 471100
    }),
    CrossSection("QCD_Pt_170to300", {
        "7": 2.426e+04, #  [2]
        "8": 34138.15,  #  [1]
        "13": 120300.,  # [12]
    }),
    CrossSection("QCD_Pt_300to470", {
        "7": 1.168e+03, #  [2]
        "8": 1759.549,  #  [1]
        "13": 7475.,    # [12]
    }),
    CrossSection("QCD_Pt_470to600", {
        "13": 587.1, # [12]
    }),
    CrossSection("QCD_Pt_600to800", {
        "13": 167., # [12]
    }),
    CrossSection("QCD_Pt_800to1000", {
        "13": 28.25, # [12]
    }),
    CrossSection("QCD_Pt_1000to1400", {
        "13": 8.195, # [12]
    }),
    CrossSection("QCD_Pt_1400to1800", {
        "13": 0.7346, # [12] # McM: 0.84265
    }),
    CrossSection("QCD_Pt_1800to2400", {
        "13": 0.1091, # [12] # McM: 0.114943
    }),
    CrossSection("QCD_Pt_2400to3200", {
        "13": 0.00682981, # [15]
    }),
    CrossSection("QCD_Pt_3200toInf", {
        "13": 0.000165445 , # [15]
    }),
    CrossSection("QCD_Pt20_MuEnriched", {
        "7": 296600000.*0.0002855, # [2]
        "8": 3.64e8*3.7e-4, # [1]
    }),
    CrossSection("QCD_Pt_50to80_MuEnrichedPt5", {
        "13": 4.487e+05, # 4.487e+05 +- 1.977e+02 pb [14]
    }),
    CrossSection("QCD_Pt_80to120_MuEnrichedPt5", {
        "13": 1.052e+05, # 1.052e+05 +- 5.262e+01 [14]
    }),
    CrossSection("QCD_Pt_120to170_MuEnrichedPt5", {
        "13": 2.549e+04, # 2.549e+04 +- 1.244e+01 [14]
    }),
    CrossSection("QCD_Pt_170to300_MuEnrichedPt5", {
        "13": 8.644e+03, # 8.644e+03 +- 4.226e+00 [14]
    }),
    CrossSection("QCD_Pt_300to470_MuEnrichedPt5", {
        "13": 7.967e+02, # 7.967e+02 +- 3.845e-0 [14]
    }),
    CrossSection("WW", {
        "7": 43.0,   #  [3]
        "8": 54.838, #  [9] Took value for CTEQ PDF since CTEQ6L1 was used in pythia simulation)
        "13": 118.7, # [13] NNLO QCD
    }),
    CrossSection("WWTo2L2Nu", {
        "13": 12.178, # [16] NNLO
    }),
    CrossSection("WWDPS", {
        "13": 1.64, # [16] LO
    }),
    CrossSection("WZ", {
        "7": 18.2,         #  [3]
        "8": 33.21,        #  [9], took value for CTEQ PDF since CTEQ6L1 was used in pythia simulation
        "13": 29.8 + 18.6, # [13] W+ Z/a* + W- Z/a*, MCFM 6.6 m(l+l-) > 40 GeV (I cant say about ref [13], but at ref [16] its given sig = 47.13 at NLO)
    }),
    CrossSection("WZTo3LNu", {
        "13": 4.42965, # [16]
    }),
    CrossSection("ZZ", {   #:Ather:/ZZ
        "7": 5.9,    #  [3]
        "8": 17.654, #  [9] Took value for CTEQ PDF since CTEQ6L1 was used in pythia simulation, this is slightly questionmark, since the computed value is for m(ll) > 12
        "13": 15.4,  # [13] This was already included but I cannot find this value at ref [13] as mentioned, at ref [16] sig = 16.523 at NLO
    }),
    CrossSection("ZZTo4L", {
        "13": 1.256, # [16]
    }),
    CrossSection("WZZ", {
        "13": 0.05565, # [16] NLO
    }),
    CrossSection("WZZ", {
        "13": 0.1651, # [16] NLO
    }),
    CrossSection("WZZ", {
        "13": 0.01398, # [16]
    }),
    CrossSection("TTJets_FullLept", {
        "8": 245.8* 26.1975/249.50, # [10], BR from [11]
    }),
    CrossSection("TTJets_SemiLept", {
        "8": 245.8* 109.281/249.50, # [10], BR from [11]
    }),
    CrossSection("TTJets_Hadronic", {
        "8": 245.8* 114.0215/249.50, # [10], BR from [11]
    }),
    CrossSection("TTJets", {
        "7": 172.0,   # [10]
        "8": 245.8,   # [10]
        "13": 831.76, # [13] top mass 172.5, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
    }),
    CrossSection("TTJets_HT600to800", {
        "13": 0.0, 
    }),
    CrossSection("TTJets_HT800to1200", {
        "13": 0.0, 
    }),
    CrossSection("TTJets_HT1200to2500", {
        "13": 0.0, 
    }),
    CrossSection("TTJets_HT2500toInf", {
        "13": 0.0, 
    }),
    CrossSection("TTWJetsToLNu", {
        #"7": 0.1473, #  [4] NLO (this is for inclusive not LNu, for LNu = sig*(1-BR(W->qq)): 0.0477)
        #"8": 0.232,  #  [9] NLO (this is for inclusive not LNu, for LNu = sig*(1-BR(W->qq)): 0.07516)
        "13": 0.2043, # [16] NLO
    }),
    CrossSection("TTZToLLNuNu", {
        #"7": 0.1369,  #  [4] NLO (this is for inclusive not LNu, for LNu = sig*(1-BR(Z->qq)): 0.041193)
        #"8": 0.2057,  #  [9] NLO (this is for inclusive not LNu, for LNu = sig*(1-BR(Z->qq)): 0.061895)
        "13": 0.2529,  # [16]
    }),
    CrossSection("TTGJets", {
            "13": 3.697,  # [16] NLO
    }),
    CrossSection("WJetsToLNu", {
        "7": 31314,       #  [4] NNLO (this was included but commented out)
        "8": 12234.4*3,   #  [9] NNLO (this was included but commented out)
        "13": 20508.9*3,  # [13] 20508.9*3, McM for the MLM dataset: 5.069e4
    }),
    CrossSection("WJetsToLNu_HT_100To200", {
        "13": 1.293e+03*1.2138, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("WJetsToLNu_HT_200To400", {
        "13": 3.86e+02*1.2138, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("WJetsToLNu_HT_400To600", {
        "13": 47.9*1.2138, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("WJetsToLNu_HT_600ToInf", {
        "13": 0.0, # Forcing to zero to avoid overlap
    }),
    CrossSection("WJetsToLNu_HT_600To800", {
        "13": 12.8*1.2138, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("WJetsToLNu_HT_800To1200", {
        "13": 5.26*1.2138, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("WJetsToLNu_HT_1200To2500", {
        "13": 1.33*1.2138, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("WJetsToLNu_HT_2500ToInf", {
        "13": 3.089e-02*1.2138, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("PREP_WJets", { # PREP (LO) cross sections, for W+NJets weighting
        "7": 27770.0,
        "8": 30400.0,
    }),
    CrossSection("PREP_W1Jets", {
        "7": 4480.0,
        "8": 5400.0,
    }),
    CrossSection("PREP_W2Jets", {
        "7": 1435.0,
        "8": 1750.0,
    }),
    CrossSection("PREP_W3Jets", {
        "7": 304.2,
        "8": 519.0,
    }),
    CrossSection("PREP_W4Jets", {
        "7": 172.6,
        "8": 214.0,
    }),
    CrossSection("DYJetsToLL_M_50", {
        "7": 3048.0,     #  [4], NNLO
        "8": 3531.9,     #  [9], NNLO
        "13": 2008.4*3.0 # [14]
    }),
    CrossSection("DYJetsToLL_M_50_TauHLT", {
        "7": 3048.0,     #  [4], NNLO
        "8": 3531.9,     #  [9], NNLO
        "13": 2008.4*3.0 # [14]
    }),
    CrossSection("DYJetsToLL_M_10to50", {
        "7": 9611.0,      #  [1]
        "8": 11050.0,     #  [1]
        "13" :3205.6*3.0, # [14] (value at [16] = 18610)
    }),
    CrossSection("DYJetsToLL_M_50_HT_100to200", {
        "13": 139.4*1.231, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("DYJetsToLL_M_50_HT_200to400", {
        "13": 42.75*1.231, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("DYJetsToLL_M_50_HT_400to600", {
        "13": 5.497*1.231, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("DYJetsToLL_M_50_HT_600toInf", {
        "13": 2.21*1.231, # McM times NNLO/LO ratio of inclusive sample
    }),
    CrossSection("DYJetsToLL_M_100to200", {
        "13": 0.0, # FIXME
    }),
    CrossSection("DYJetsToLL_M_200to400", {
        "13": 0.0, # FIXME
    }),
    CrossSection("DYJetsToLL_M_400to500", {
        "13": 0.0, # FIXME
    }),
    CrossSection("DYJetsToLL_M_500to700", {
        "13": 0.0, # FIXME
    }),
    CrossSection("DYJetsToLL_M_700to800", {
        "13": 0.0, # FIXME
    }),
    CrossSection("DYJetsToLL_M_800to1000", {
        "13": 0.0, # FIXME
    }),
    CrossSection("DYJetsToLL_M_1000to1500", {
        "13": 0.0, # FIXME
    }),
    CrossSection("DYJetsToLL_M_1500to2000", {
        "13": 0.0, # FIXME
    }),
    CrossSection("DYJetsToLL_M_2000to3000", {
        "13": 0.0, # FIXME
    }),
    CrossSection("DYToTauTau_M_20_", {
        "7": 4998,    # [4], NNLO
        "8": 5745.25, # [9], NNLO
    }),
    CrossSection("DYToTauTau_M_100to200", {
        "7": 0,          #  [?]
        "8": 34.92,      #  [1]
	"13": 2.307e+02, # [14]
    }),
    CrossSection("DYToTauTau_M_200to400", {
        "7": 0,          #  [?]
        "8": 1.181,      #  [1]
        "13": 7.839e+00, # [14]
    }),
    CrossSection("DYToTauTau_M_400to500", {
        "13": 3.957e-01, # [14]
    }),
    CrossSection("DYToTauTau_M_500to700", {
        "13": 2.352e-01, # [14]
    }),
    CrossSection("DYToTauTau_M_700to800", {
        "13": 3.957e-02, # [14]
    }),
    CrossSection("DYToTauTau_M_400to800", {
        "7": 0,       # [?]
        "8": 0.08699, # [1]
    }),
    CrossSection("DYToTauTau_M_800", {
        "7": 0,        # [?]
        "8": 0.004527, # [1]
    }),
    CrossSection("GluGluHToTauTau_M125", {
        "13": 1, # dummy value, not really needed as this sample is not merged with anything else
    }),
    CrossSection("GluGluHToTauTau_M125_TauHLT", {
        "13": 1, # dummy value, not really needed as this sample is not merged with anything else
    }),
    CrossSection("T_t-channel", {
        "7": 41.92, # [5,6]
        "8": 56.4, # [8]
    }),
    CrossSection("Tbar_t-channel", {
        "7": 22.65, # [5,6]
        "8": 30.7,  #   [8]
    }),
    CrossSection("T_tW-channel", {
        "7": 7.87, # [5,6]
        "8": 11.1, #   [8]
    }),
    CrossSection("Tbar_tW-channel", {
        "7": 7.87, # [5,6]
        "8": 11.1, #   [8]
    }),
    CrossSection("T_s-channel", {
        "7": 3.19, # [5,6]
        "8": 3.79, #   [8]
    }),
    CrossSection("Tbar_s-channel", {
        "7": 1.44, # [5,6]
        "8": 1.76, #   [8]
    }),
    CrossSection("ST_tW_antitop_5f_inclusiveDecays", {
        "7": 7.87,   #  [21]
        "8": 11.19,  #  [21]
        "13": 35.85, #  [21] (at [16] sigma is 35.6)
    }),
    CrossSection("ST_tW_top_5f_inclusiveDecays", {
            "7": 7.87,   #  [21]
            "8": 11.19,  #  [21]
            "13": 35.85, #  [21] (at [16] sigma is 35.6)
            }),
    CrossSection("ST_t_channel_antitop_4f_leptonDecays", {
            "7": 22.02,  # [13, 21]
            "8": 29.74,  # [13, 21]
            "13": 80.95, # [13, 21] (at [16] sigma is 26.38 Huge Difference)
            }),
    CrossSection("ST_t_channel_4f_leptonDecays", {
            "13": 70.69, # [16]
            }),
    CrossSection("ST_t_channel_top_4f_leptonDecays", {
            "7": 41.80,   # [13, 21]
            "8": 54.87,   # [13, 21]
            "13": 136.02, # [13, 21]
            }),
    CrossSection("ST_s_channel_4f_leptonDecays", {
            "13": 10.32, # [13, 21] (at [16] sigma is 3.36)
            }),
    CrossSection("TZQToLL", {
            "13": 0.0758, # [16] NLO
            }),
    CrossSection("THQHIncl", {
            "13": 0.07096, # [20, 22]
            }),
    CrossSection("THWHIncl", {
            "13": 0.01561, # [20, 22]
            }),
    CrossSection("ttHJetToNonbb_M120", {
        "13": 0.20197, #[17][18][19] 
        # From [23]: XS_120(13TeV) = XS_125(13TeV)*XS_120(8TeV)/XS_125(8TeV) => XS_120(13TeV) = 0.5737, and XS_nonbb = XS*(1-BR(Hbb)) => XS_nonbb = 0.20197
    }),
    CrossSection("ttHJetToNonbb_M125", {
            "13": 0.2151, # [16]
            }),
    CrossSection("ttHJetToNonbb_M130", {
        "13": 0.22909, #[17][18][19]
        # From [23]: XS_120(13TeV) = XS_125(13TeV)*XS_120(8TeV)/XS_125(8TeV) => XS_120(13TeV) = 0.4518, and XS_nonbb = XS*(1-BR(Hbb)) => XS_nonbb = 0.22909
    }),
)
