#!/usr/bin/env python
import os
import re
import sys
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

re_vector = re.compile("vector<(?P<type>.*)>")

def writeFiles(header, source, headerName, sourceName):
    '''
    '''
    basedir = os.path.join(os.environ["HIGGSANALYSIS_BASE"], "NtupleAnalysis", "src", "DataFormat")
    hfile = os.path.join(basedir, "interface", headerName)
    ccfile = os.path.join(basedir, "src", sourceName)
    f = open(hfile, "w")
    f.write(header)
    f.close()
    f = open(ccfile, "w")
    f.write(source)
    f.close()

    print "\n=== hplusGenerateDataFormats.py:"
    print "\t Generated " + hfile
    print "\t Generated " + ccfile
    return


def getAdditionalFourVectorBranches(types, prefix):
    '''
    '''
    result = []
    for t in types.keys():
        if t.startswith("%s_eta"%prefix):
            suffix = t.replace("%s_eta"%prefix,"")
            if len(suffix) > 0 and "%s_pt%s"%(prefix,suffix) in types.keys() and "%s_phi%s"%(prefix,suffix) in types.keys() and "%s_e%s"%(prefix,suffix) in types.keys():
                if not (suffix.endswith("up") or suffix.endswith("Up") or suffix.endswith("down") or suffix.endswith("Down")):
                    # Ignore syst. variations
                    if suffix.startswith("_") and len(suffix) > 1:
                        suffix = suffix[1:]
                    result.append(suffix)
    return result


def GenerateParticle(types, particle, discriminatorCaptions):
    '''
    '''
    discriminatorList = {}
    # For-loop: All discriminator captions
    for k in discriminatorCaptions.keys():
        discriminatorList[k] = []
        
    particleBranches = [particle + "s_" + x for x in ["pt", "eta", "phi", "e", "pdgId"]] # these are handled by Particle class
    branchNames      = filter(lambda n: n[0:len(particle)+2] == particle + "s_", types.keys())
    branchNames.sort(key=lambda n: types[n]+n)
    print "\n=== hplusGenerateDataFormats.py: Branch names for '%s' are:\n\t %s" % (particle, "\n\t ".join(branchNames))

    # Obtain four-vector branches and remove them from the branch list
    additionalFourVectorBranches = getAdditionalFourVectorBranches(types, particle + "s")    
    additionalFourVectorBranches.sort()
    
    print "=== hplusGenerateDataFormats.py: Additional 4-vector Branches for '%s' are:\n\t %s" % (particle, "\n\t ".join(additionalFourVectorBranches))
    for item in additionalFourVectorBranches:
        i = 0
        while i < len(branchNames):
            b = branchNames[i]
            # Remove also syst. uncertainties (since they are handled separately)
            if b.endswith(item) or b.endswith("up") or b.endswith("Up") or b.endswith("down") or b.endswith("Down"):
                del branchNames[i]
            else:
                i += 1


    particleFloatType = None
    branchObjects     = []
    branchAccessors   = []
    branchBooks       = []
    # For-loop: All branch names
    for i, branch in enumerate(branchNames):
        name    = branch[len(particle)+2:]
        capname = name[0].upper()+name[1:]
        vectype = types[branch]
        if "vector<vector" in vectype:
            vectype = vectype.replace("vector<vector", "vector<std::vector")
            # print vectype
        
        m = re_vector.search(vectype)
        if not m:
            raise Exception("Could not interpret type %s as vector" % vectype)
        realtype = m.group("type")

        # Print a table to see what's going on
        PrintTable(i, "{:<55} {:<55} {:<30} {:>30}", ["Name", "CapName", "VecType", "RealType"], [name, capname, vectype, realtype], True)

        # For "pt", "eta", "phi", "e", "pdgId"
        if branch in particleBranches:
            if particleFloatType == None:
                particleFloatType = realtype
            elif particleFloatType != realtype:
                if realtype in ["float", "double"]:
                    raise Exception("Mismatch in 4-vector branch types: all of them must be of the same type, and now {branch} has {type} while others have {otype}".format(branch=branch, type=realtype, otype=particleFloatType))
        else: # Not "pt", "eta", "phi", "e", "pdgId"
            # Collect branches
            branchObjects.append("  const Branch<std::{vectype}> *f{vecname};".format(vectype=vectype, vecname=capname))
            branchAccessors.append("  {type} {name}() const {{ return this->fCollection->f{capname}->value()[this->index()]; }}".format(type=realtype, name=name, capname=capname))
            branchBooks.append("  mgr.book(prefix()+\"_{name}\", &f{capname});".format(name=name, capname=capname))

            # Collect discriminators
            for k in discriminatorCaptions.keys():
                if branch.startswith(particle) and k in branch:
                    veto = False
                    for kk in discriminatorCaptions.keys():
                        if name in discriminatorList[kk]:
                            veto = True
                    if not veto:
                        discriminatorList[k].append(name)
    if particleFloatType is None:
        if len(branchObjects):
            raise Exception("Unable to infer the floating point type for {particle}".format(particle=particle))
        else:
            particleFloatType = "double" # default value

    # Getter for discriminator method names
    discriminatorCaptionGetters = ""
    for k in discriminatorCaptions.keys():
        #print k, discriminatorList[k]
        discriminatorCaptionGetters += "  std::vector<std::string> get%sDiscriminatorNames() const {\n"%discriminatorCaptions[k]
        discriminatorCaptionGetters += "    static std::vector<std::string> n = { std::string(\"%s\")};\n"%("\"), std::string(\"".join(map(str, discriminatorList[k])))
        discriminatorCaptionGetters += "    return n;\n"
        discriminatorCaptionGetters += "  }\n"
    # Getter for discriminator method values
    discriminatorMethodGetters = ""
    for k in discriminatorCaptions.keys():
        discriminatorMethodGetters += "  std::vector<std::function<bool()>> get%sDiscriminatorValues() const {\n"%discriminatorCaptions[k]
        discriminatorMethodGetters += "    static std::vector<std::function<bool()>> values = {\n"
        for i in range(len(discriminatorList[k])):
            if i < len(discriminatorList[k])-1:
                discriminatorMethodGetters += "      [&](){ return this->%s(); },\n"%discriminatorList[k][i]
            else:
                discriminatorMethodGetters += "      [&](){ return this->%s(); }\n"%discriminatorList[k][i]
        discriminatorMethodGetters += "    };\n"
        discriminatorMethodGetters += "    return values;\n"
        discriminatorMethodGetters += "  }\n"

    includes = "#include \"DataFormat/interface/Particle.h\"\n"
    if len(discriminatorCaptions.keys()):
        includes += "#include <string>\n"
        includes += "#include <vector>\n"
        includes += "#include <functional>\n"

    prefix = particle
    if particle != "HLTTau":
        prefix += "s"

    # Additional four-vectors for collection
    preInit = ": ParticleCollection(prefix)"
    for item in additionalFourVectorBranches:
        preInit += ",\n    f%s(prefix)"%item
    initList = []
    for item in additionalFourVectorBranches:
        initList.append('    f%s.setEnergySystematicsVariation("_%s");'%(item, item))
    inits = ""
    inits += "\n".join(map(str,initList))
    fvectorgetters = ""
    
    for item in additionalFourVectorBranches:
        fvectorgetters += "  const ParticleCollection<double>* get%sCollection() const { return &f%s; }\n"%(item, item)
    if len(additionalFourVectorBranches) > 0:
        fvectorgetters += "protected:\n"
    for item in additionalFourVectorBranches:
        fvectorgetters += "  ParticleCollection<double> f%s;\n"%item
    # additional four-vectors for particle
    preInitParticle = "  : Particle<Coll>(coll, index)"
    for item in additionalFourVectorBranches:
        preInitParticle += ",\n    f%s(coll->get%sCollection(), index)"%(item, item)
    fvectorgettersParticle = ""
    for item in additionalFourVectorBranches:
        fvectorgettersParticle += "  const Particle<ParticleCollection<double>>* %s() const { return &f%s; }\n"%(item,item)
    fvectorItemsParticle = ""
    for item in additionalFourVectorBranches:
        fvectorItemsParticle += "  Particle<ParticleCollection<double>> f%s;\n"%item
    # additional four-vectors for source
    fvectorBranches = ""
    for item in additionalFourVectorBranches:
        fvectorBranches += "  f%s.setupBranches(mgr);\n"%item
    
    header = """// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_{type}_h
#define DataFormat_{type}_h

{includes}
class {type}Collection: public ParticleCollection<{particleFloatType}> {{
public:
  explicit {type}Collection(const std::string& prefix="{prefix}")
  {preinit}
  {{
{inits}
  }}
  ~{type}Collection() {{}}

  void setupBranches(BranchManager& mgr);

{discrCaptionGetters}
{fvectorgetters}
protected:
{branchObjects}
}};


template <typename Coll>
class {type}: public Particle<Coll> {{
public:
  {type}() {{}}
  {type}(const Coll* coll, size_t index)
{preInitParticle}
  {{}}
  ~{type}() {{}}

{discrMethodGetters}
{fvectorgettersParticle}
{branchAccessors}

protected:
{fvectorItemsParticle}
}};

#endif
""".format(type=particle+"Generated", 
           includes=includes,
           prefix=prefix,
           preinit=preInit,
           inits=inits,
           fvectorgetters=fvectorgetters,
           preInitParticle=preInitParticle,
           fvectorgettersParticle=fvectorgettersParticle,
           fvectorItemsParticle=fvectorItemsParticle,
           particle=particle,
           particleFloatType=particleFloatType,
           branchObjects="\n".join(branchObjects),
           discrCaptionGetters=discriminatorCaptionGetters,
           discrMethodGetters=discriminatorMethodGetters,
           branchAccessors="\n".join(branchAccessors))

    source = """
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/{type}.h"

#include "Framework/interface/BranchManager.h"

void {type}Collection::setupBranches(BranchManager& mgr) {{
  ParticleCollection::setupBranches(mgr);
{fvectorBranches}
{branchBooks}
}}
""".format(type=particle+"Generated", fvectorBranches=fvectorBranches, branchBooks="\n".join(branchBooks))
    writeFiles(header, source, particle+"Generated.h", particle+"Generated.cc")
    return


def GenerateGenParticles(types, particle):
    '''
    Auto-generates the contents of the genparticle collection (note: only collection, no single genparticles provided)
    '''

    # Generate branch names 
    branchNames = filter(lambda n: n[0:len(particle)+2] == particle + "s_", types.keys() )
    branchNames.sort(key=lambda n: types[n]+n)
    print "\n=== hplusGenerateDataFormats.py: Branch names for '%s' are:\n\t %s" % (particle, "\n\t ".join(branchNames))

    # Obtain four-vector branches and remove them from the branch list
    additionalFourVectorBranches = getAdditionalFourVectorBranches(types, particle+"s")
    additionalFourVectorBranches.sort()

    print "=== hplusGenerateDataFormats.py: Additional 4-vector Branches for '%s' are:\n\t %s" % (particle, "\n\t ".join(additionalFourVectorBranches))
    for item in additionalFourVectorBranches:
        i = 0
        while i < len(branchNames):
            b = branchNames[i]
            # Remove also syst. uncertainties since they are handled separately
            if b.endswith(item) or b.endswith("up") or b.endswith("Up") or b.endswith("down") or b.endswith("Down"):
                del branchNames[i]
            else:
                i += 1

    # Determine float type
    floattype = None
    if len(additionalFourVectorBranches) > 0:
        for t in types.keys():
            if "%ss_pt_%s"%(particle, additionalFourVectorBranches[0]) == t:
                m = re_vector.search(types[t])
                if not m:
                    raise Exception("Error (%s): Additional four vector type is not a vector!"%particle)
                floattype = m.group("type")
        if floattype == None:
            raise Exception("Error: this should not happen")

    branchObjects = []
    branchBooks   = []
    branchGetters = []
    for i, branch in enumerate(branchNames):
        name     = branch[len(particle)+2:]
        capname  = name[0].upper()+name[1:]
        datatype = types[branch]

        m        = re_vector.search(datatype)
        realtype = types[branch]
        if not m:
            datatype = types[branch]
        else:
            datatype = "std::%s"%datatype
            realtype = m.group("type")
        
        # Print a table to see what's going on
        PrintTable(i, "{:<20} {:<20} {:<40} {:>20}", ["Name", "CapName", "DataType", "RealType"], [name, capname, datatype, realtype], True)

        # Collect branches
        branchObjects.append("  const Branch<{datatype}> *f{vecname};".format(datatype=datatype, vecname=capname))
        branchBooks.append("  mgr.book(\"{type}s_{name}\", &f{capname});".format(type=particle, name=name, capname=capname))
        branchGetters.append("  const {datatype} get{capname}() const {{ return f{capname}->value(); }}".format(datatype=datatype, capname=capname))
        
    includes = "#include \"DataFormat/interface/Particle.h\"\n"
    includes += "#include <vector>\n"

    prefix = particle
    if particle != "HLTTau":
        prefix += "s"

    # Additional four-vectors for collection
    preInit = ""
    for item in additionalFourVectorBranches:
        if len(preInit) > 0:
            preInit += ",\n    "
        else:
            preInit += ": "
        preInit += "f%s(prefix)"%item
    initList = []
    for item in additionalFourVectorBranches:
        initList.append('    f%s.setEnergySystematicsVariation("_%s");'%(item, item))
    inits = ""
    inits += "\n".join(map(str,initList))
    fvectorgetters = ""
    fvectorgettersimpl = ""

    for item in additionalFourVectorBranches:
        print "item = ", item
        fvectorgetters += "  const std::vector<Particle<ParticleCollection<float_type>>> get%sCollection() const;\n"%item
        fvectorgettersimpl += "const std::vector<Particle<ParticleCollection<%s>>> %sGeneratedCollection::get%sCollection() const {\n"%(floattype, particle[0].upper()+particle[1:],item)
        fvectorgettersimpl += "  std::vector<Particle<ParticleCollection<float_type>>> v;\n"
        fvectorgettersimpl += "  for (size_t i = 0; i < f%s.size(); ++i)\n"%item
        fvectorgettersimpl += "    v.push_back(Particle<ParticleCollection<float_type>>(&f%s, i));\n"%item
        fvectorgettersimpl += "  return v;\n"
        fvectorgettersimpl += "}\n"
    if len(additionalFourVectorBranches) > 0:
        fvectorgetters += "protected:\n"
    for item in additionalFourVectorBranches:
        fvectorgetters += "  ParticleCollection<float_type> f%s;\n"%item
    # additional four-vectors for source
    fvectorBranches = ""
    for item in additionalFourVectorBranches:
        fvectorBranches += "  f%s.setupBranches(mgr);\n"%item
    
    header = """// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_{type}_h
#define DataFormat_{type}_h

{includes}
class {type}Collection {{
public:
  using float_type = {floattype};
  explicit {type}Collection(const std::string& prefix="{prefix}")
  {preinit}
  {{
{inits}
  }}
  ~{type}Collection() {{}}

  void setupBranches(BranchManager& mgr);

{fvectorgetters}

public:
{branchgetters}

protected:
{branchObjects}
}};

#endif
""".format(type=particle[0].upper()+particle[1:]+"Generated", 
           includes=includes,
           floattype=floattype,
           prefix=prefix,
           preinit=preInit,
           inits=inits,
           fvectorgetters=fvectorgetters,
           branchgetters="\n".join(branchGetters),
           particle=particle,
           branchObjects="\n".join(branchObjects))

    source = """
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/{type}.h"

#include "Framework/interface/BranchManager.h"

void {type}Collection::setupBranches(BranchManager& mgr) {{
{fvectorBranches}
{branchBooks}
}}

{fvectorgettersimpl}
""".format(type=particle[0].upper()+particle[1:]+"Generated",
           fvectorBranches=fvectorBranches,
           branchBooks="\n".join(branchBooks),
           fvectorgettersimpl=fvectorgettersimpl)
    name = particle[0].upper()+particle[1:]
    writeFiles(header, source, name+"Generated.h", name+"Generated.cc")
    return


def GenerateDiscriminator(types, name, discriminatorPrefix):
    '''
    Method for creating a class for a simple discriminator
    '''
    # Obtain list of discriminators
    branchNames = filter(lambda n: n[0:len(discriminatorPrefix)+1] == discriminatorPrefix+"_", types.keys())
    branchNames.sort(key=lambda n: types[n]+n)
    print "\n=== hplusGenerateDataFormats.py: Branch names for '%s' are:\n\t %s" % (name, "\n\t ".join(branchNames))

    # Create list of discriminator names
    discriminatorNameList  = []
    discrMethodGettersList = []
    branchAccessors = ""
    branchObjects   = ""
    branchBookings  = ""

    # For-loop: All branch names    
    for n in branchNames:
        shortName = n.replace(discriminatorPrefix+"_", "")
        shortNameOriginal = shortName
        shortName = shortName[0].upper()+shortName[1:]
        # Create list of discriminator names
        discriminatorNameList.append('std::string("%s")'%shortNameOriginal)
        # Create list of branch accessors
        branchAccessors += "  bool pass%s() const { return f%s->value(); }\n"%(shortName, shortName)
        # Create list of branch objects
        branchObjects += "  const Branch<bool> *f%s;\n"%shortName
        # Getter for discriminators methods
        discrMethodGettersList.append("      [&](){ return this->pass%s(); }"%shortName)
        # Branch bookings
        branchBookings += '  mgr.book("%s", &f%s);\n'%(n, shortName)
    # Generate header file
    includes = ""
    includes += "#include <string>\n"
    includes += "#include <vector>\n"
    includes += "#include <functional>\n"
    includes += '#include "Framework/interface/BranchManager.h"\n'

    header = """// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_{type}_h
#define DataFormat_{type}_h

{includes}
class {type} {{
public:
  explicit {type}() {{}}
  ~{type}() {{}}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getDiscriminatorNames() const {{
    static std::vector<std::string> n = {{ {discrNames} }};
    return n;
  }}

  std::vector<std::function<bool()>> getDiscriminatorValues() const {{
    static std::vector<std::function<bool()>> values = {{
{discrMethodGetters}
    }};
    return values;
  }}

{branchAccessors}
protected:
{branchObjects}
}};

#endif
""".format(type=name+"Generated", 
           includes=includes,
           discrNames=", ".join(map(str,discriminatorNameList)),
           discrMethodGetters=",\n".join(map(str,discrMethodGettersList)),
           branchAccessors=branchAccessors,
           branchObjects=branchObjects)
    # Generate source file
    source = """
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/{type}.h"

void {type}::setupBranches(BranchManager& mgr) {{
{branchBooks}
}}
""".format(type=name+"Generated", branchBooks=branchBookings)
    # Write files
    writeFiles(header, source, name+"Generated.h", name+"Generated.cc")
    return


def PrintTable(counter, textAlign, colNamesList, colValuesList, bPrint=False):
    '''
    '''
    if not bPrint:
        return

    rows  = []
    title = textAlign.format(*colNamesList)
    hLine = "="*len(title)
    vals  = textAlign.format(*colValuesList)

    if (counter < 1):
        rows.append(hLine)
        rows.append(title)
        rows.append(hLine)
    rows.append(vals)

    for r in rows:
        print r
    return


def main(opts, args):
    '''
    '''
    if not "HIGGSANALYSIS_BASE" in os.environ:
        print "=== hplusGenerateDataFormats.py:\n\t Environment variable $HIGGSANALYSIS_BASE not set, please source setup.sh"
        return 1

    # Open the input flat-tree ROOT file
    f = ROOT.TFile.Open(opts.file)

    # Geth the Tree
    tree  = f.Get(opts.tree)
    types = {}

    # For-loop: All Branches
    for branch in tree.GetListOfBranches():

        # Get objects (vector<int>, vector<float>, etc..)
        t = branch.GetClassName() 

        # Get basic types (bool, int, float,  etc..)
        if t == "":
            t = branch.GetListOfLeaves()[0].GetTypeName() 

        # Create dictionary: key= BranchName, value = variable type
        types[branch.GetName()] = t

    # Close ROOT file
    f.Close()

    print "=== hplusGenerateDataFormats.py:\n\t Found '%s' Branches in TTree with name '%s', inside ROOT file '%s'" % (len(types), opts.tree, opts.file)
    
    # The provided dictionaries are for grouping discriminators
    #GenerateParticle(types, "Electron", {"ID": "ID"}) # checked (includes trigger match)
    #GenerateParticle(types, "Muon", {"ID": "ID"})     # checked (includes trigger match)
    #GenerateParticle(types, "Tau", {"Isolation": "Isolation", "againstElectron": "AgainstElectron", "againstMuon": "AgainstMuon"}) #checked
    #GenerateParticle(types, "PFCHSJet", {"BJetTags": "BJetTags", "PUID": "PUID", "ID" : "JetID"}) # checked
    #GenerateParticle(types, "PuppiJet", {"BJetTags": "BJetTags", "PUID": "PUID", "ID" : "JetID"}) # checked
    #GenerateParticle(types, "GenJet", {})      # checked
    #GenerateParticle(types, "PFcandidate", {}) # checked
    #GenerateParticle(types, "HLTEle", {}) # HLTEle, HLTMu, HLTTau only contain  generic momentum and pdgId information, no generation needed
    #GenerateParticle(types, "HLTMu" , {}) # Since no future changes are foreseen it can be run once and then removed from from the autogeneration
    #GenerateParticle(types, "HLTTau", {}) 
    # GenerateGenParticles(types , "GenParticle")            # checked. N.B: At the momment ome things had to be added by hand.
    GenerateParticle(types , "GenParticle", {})            # checked. N.B: At the momment ome things had to be added by hand.
    #GenerateDiscriminator(types, "METFilter", "METFilter") # checked

    return 0


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] root_file")

    parser.add_option("-f", "--file", dest="file", help="Generate data format from this flat-tree ROOT file (default: None)")
    parser.add_option("-t", "--tree", dest="tree", default="Events", help="Generate data format from this tree (default: 'Events')")
    (opts, args) = parser.parse_args()

    if opts.file == None:
        parser.error("\n\t You should give a flat-tree ROOT file as argument with the -f options")

    sys.exit(main(opts, args))
