# Script for setting up standalone environment, without CMSSW
# release area, for accessing the python libraries and scripts.
#
# Usage:
# cd CMSSW_X_Y_Z/src/UCYHiggsAnalysis/
# source setup.csh

if ( $?HIGGSANALYSIS_BASE ) then
    echo "=== setup.csh:\n\t Standalone environment already loaded (HIGGSANALYSIS_BASE)"
    exit
endif

set LOCATION=""
if ( $?CMSSW_BASE ) then
    set LOCATION="CMSSW"
endif

# Detect and store host name (LOCATION)
if ( $LOCATION == "" ) then
    if (`hostname` =~ "lxplus"* ) then
        set LOCATION="lxplus"
    else if (`hostname` =~ "jade"* ) then
	set LOCATION="jade"
    endif
endif

setenv HIGGSANALYSIS_BASE $PWD

if ( $LOCATION == "lxplus" ) then
    echo "=== setup.csh:\n\t Sourcing lxplus environments for gcc 4.8 and ROOT 6.02"
    source /afs/cern.ch/sw/lcg/contrib/gcc/4.8/x86_64-slc6-gcc48-opt/setup.csh
    setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/6.04.00/x86_64-slc6-gcc48-opt/root
    setenv LD_LIBRARY_PATH "${ROOTSYS}/lib:${LD_LIBRARY_PATH}"
    setenv PATH "${ROOTSYS}/bin:${PATH}"

    if ($?PYTHONPATH) then
        setenv PYTHONPATH "$ROOTSYS/lib:$PYTHONPATH"
    else
        setenv PYTHONPATH "$ROOTSYS/lib"
    endif 
#    pushd $ROOTSYS >/dev/null 
#    source bin/thisroot.csh
#    popd >/dev/null
endif

set LD_LIBRARY_PATH_APPEND=""
set LD_LIBRARY_PATH_APPEND="$HIGGSANALYSIS_BASE/NtupleAnalysis/lib:${LD_LIBRARY_PATH_APPEND}"
if ( ! $?LD_LIBRARY_PATH ) then
    setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH_APPEND}"
else
    setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH_APPEND}:${LD_LIBRARY_PATH}"
endif

if ( $LOCATION == "CMSSW" ) then
    if ( ! $?CMSSW_BASE || ! -e $CMSSW_BASE/python/UCYHiggsAnalysis/NtupleAnalysis ) then
	echo "=== setup.csh:"
	set SOURCEFILE=$HIGGSANALYSIS_BASE/NtupleAnalysis/python
	set LINKFILE=$CMSSW_BASE/python/UCYHiggsAnalysis/NtupleAnalysis
	
	echo "\t Linking $SOURCEFILE to $LINKFILE"
        ln -s  $SOURCEFILE $LINKFILE
    endif
else
    if ( ! -e .python/UCYHiggsAnalysis ) then
	echo "=== setup.csh:"
	set DIRNAME=.python/UCYHiggsAnalysis

	echo "\t Making directory $DIRNAME"
        mkdir -p $DIRNAME

	echo "\t Creating $DIRNAME/__init__.py"
        touch $DIRNAME/__init__.py
    endif

    #foreach DIR ( NtupleAnalysis HeavyChHiggsToTauNu ) #attikis
    foreach DIR ( NtupleAnalysis )
        if ( ! -e .python/UCYHiggsAnalysis/$DIR ) then
	    echo "=== setup.csh:"
	    set SOURCEFILE=$HIGGSANALYSIS_BASE/$DIR/python
	    set LINKFILE=.python/UCYHiggsAnalysis/`basename ${DIR}`

	    echo "\t Linking $SOURCEFILE to $LINKFILE"
            ln -s  $SOURCEFILE $LINKFILE

	    echo "\t Creating $LINKFILE/__init__.py"
            touch $LINKFILE/__init__.py
	    
            foreach d ( .python/UCYHiggsAnalysis/$DIR/* )
                if ( -d $d ) then
		    echo "\t Creating $d/__init__.py"
                    touch $d/__init__.py
                endif
            end
        endif
    end

    foreach DIR ( `ls NtupleAnalysis/src` )	
        if ( ! -e .python/UCYHiggsAnalysis/$DIR && -e $HIGGSANALYSIS_BASE/NtupleAnalysis/src/$DIR/python ) then
	    echo "=== setup.csh:"
	    set SOURCEFILE=$HIGGSANALYSIS_BASE/NtupleAnalysis/src/$DIR/python
	    set LINKFILE=.python/UCYHiggsAnalysis/`basename ${DIR}`

	    echo "\t Linking $SOURCEFILE to $LINKFILE"
            ln -s  $SOURCEFILE $LINKFILE

	    echo "\t Creating $LINKFILE/__init__.py"
            touch $LINKFILE/__init__.py

            foreach d ( .python/UCYHiggsAnalysis/$DIR/* )
                if ( -d $d ) then
		    echo "\t Creating $d/__init__.py"
                    touch $d/__init__.py
                endif
            end
        endif
    end

    if ( -z PYTHONPATH ) then
        setenv PYTHONPATH "${PWD}/.python"
    else
        setenv PYTHONPATH "${PWD}/.python:${PYTHONPATH}"
    endif

endif

#setenv PATH "${HIGGSANALYSIS_BASE}/HeavyChHiggsToTauNu/scripts:${HIGGSANALYSIS_BASE}/NtupleAnalysis/scripts:${PATH}" #attikis
echo "=== setup.csh:\n\t Setting PATH variable to ${HIGGSANALYSIS_BASE}/NtupleAnalysis/scripts:${PATH}"
setenv PATH "${HIGGSANALYSIS_BASE}/NtupleAnalysis/scripts:${PATH}"

# Install externals if necessary
echo "=== setup.csh:\n\t sh +x installexternals.sh"
sh +x installexternals.sh
