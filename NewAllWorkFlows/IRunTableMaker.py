#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
#############################################################################
##  © Copyright CERN 2018. All rights not expressly granted are reserved.  ##
##                   Author: ionut.cristian.arsene@cern.ch                 ##
##               Interface:  cevat.batuhan.tolon@cern.ch                   ## 
## This program is free software: you can redistribute it and/or modify it ##
##  under the terms of the GNU General Public License as published by the  ##
## Free Software Foundation, either version 3 of the License, or (at your  ##
## option) any later version. This program is distributed in the hope that ##
##  it will be useful, but WITHOUT ANY WARRANTY; without even the implied  ##
##     warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    ##
##           See the GNU General Public License for more details.          ##
##    You should have received a copy of the GNU General Public License    ##
##   along with this program. if not, see <https://www.gnu.org/licenses/>. ##
#############################################################################

# Orginal Task For tableMaker.cxx: https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/TableProducer/tableMaker.cxx
# Orginal Task For tableMakerMC.cxx: https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/TableProducer/tableMakerMC.cxx

import json
import sys
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from logging import handlers
from ast import parse
import os
import argparse
import re
import urllib.request
from urllib.request import Request, urlopen
import ssl

"""
argcomplete - Bash tab completion for argparse
Documentation https://kislyuk.github.io/argcomplete/
Instalation Steps
pip install argcomplete
sudo activate-global-python-argcomplete
Only Works On Local not in O2
Activate libraries in below and activate #argcomplete.autocomplete(parser) line
"""
import argcomplete  
from argcomplete.completers import ChoicesCompleter 

def listToString(s):
    """
    ListToString provides converts lists to strings with commas.
    This function is written to save as string type instead of list


    Args:
        s (list): Input as List

    Returns:
        string: Comma seperated string
    """
    if len(s) > 1:
        # initialize an empty string
        str1 = ","

        # return string
        return str1.join(s)
    else:
        str1 = " "

        return str1.join(s)


def stringToList(string):
    """
    stringToList provides converts strings to list with commas.
    This function is written to save as list type instead of string

    Args:
        string (string): Input as String

    Returns:
        list: Comma separated list
    """
    li = list(string.split(","))
    return li


class NoAction(argparse.Action):
    """
    NoAction class adds dummy positional arguments to an argument,
    so sub helper messages can be created

    Args:
        argparse (Class): Input as args
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("default", argparse.SUPPRESS)
        kwargs.setdefault("nargs", 0)
        super(NoAction, self).__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        pass


class ChoicesAction(argparse._StoreAction):
    """
    ChoicesAction class is used to add extra choices
    to a parseargs choices list

    Args:
        argparse (Class): Input as args
    """

    def add_choice(self, choice, help=""):
        if self.choices is None:
            self.choices = []
        self.choices.append(choice)
        self.container.add_argument(choice, help=help, action="none")


class ChoicesCompleterList(object):
    """
    For the ChoicesCompleterList package argcomplete,
    the TAB key is the class written for autocomplete and validation when an argument can take multiple values.
    By default, the argcomplete package has the ChoicesCompleter Class,
    which can only validate arguments that take an one value and allows autocomplete with the TAB key.

    Args:
        object (list): parserargs choices object as a list
    """

    def __init__(self, choices):
        self.choices = list(choices)

    def __call__(self, **kwargs):
        return self.choices

        
###################################
# Interface Predefined Selections #
###################################
   
tablemakerProcessAllSelections = {
    "Full": "Build full DQ skimmed data model, w/o centrality",
    "FullTiny": "Build full DQ skimmed data model tiny",
    "FullWithCov": "Build full DQ skimmed data model, w/ track and fwdtrack covariance tables",
    "FullWithCent": "Build full DQ skimmed data model, w/ centrality",
    "BarrelOnly": "Build barrel-only DQ skimmed data model, w/o centrality",
    "BarrelOnlyWithCov": "Build barrel-only DQ skimmed data model, w/ track cov matrix",
    "BarrelOnlyWithV0Bits": "Build full DQ skimmed data model, w/o centrality, w/ V0Bits",
    "BarrelOnlyWithEventFilter": "Build full DQ skimmed data model, w/o centrality, w/ event filter",
    "BarrelOnlyWithQvector": "Build full DQ skimmed data model, w/ centrality, w/ q vector",
    "BarrelOnlyWithCent": "Build barrel-only DQ skimmed data model, w/ centrality",
    "MuonOnly": "Build muon-only DQ skimmed data model",
    "MuonOnlyWithCov": "Build muon-only DQ skimmed data model, w/ muon cov matrix",
    "MuonOnlyWithCent": "Build muon-only DQ skimmed data model, w/ centrality",
    "MuonOnlyWithFilter": "Build muon-only DQ skimmed data model, w/ event filter",
    "MuonOnlyWithQvector": "Build muon-only DQ skimmed data model, w/ q vector",
    "OnlyBCs": "Analyze the BCs to store sampled lumi"
}
tablemakerProcessAllSelectionsList = []
for k, v in tablemakerProcessAllSelections.items():
    tablemakerProcessAllSelectionsList.append(k)

tablemakerProcessAllParameters = [
    "processFull",
    "processFullTiny",
    "processFullWithCov",
    "processFullWithCent",
    "processBarrelOnlyWithV0Bits",
    "processBarrelOnlyWithEventFilter",
    "processBarrelOnlyWithQvector",
    "processBarrelOnlyWithCent",
    "processBarrelOnlyWithCov",
    "processBarrelOnly",
    "processMuonOnlyWithCent",
    "processMuonOnlyWithCov",
    "processMuonOnly",
    "processMuonOnlyWithFilter",
    "processMuonOnlyWithQvector",
    "processOnlyBCs"
]

centralityTableSelections = {
    "Run2V0M": "Produces centrality percentiles using V0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "Run2SPDtks": "Produces Run2 centrality percentiles using SPD tracklets multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "Run2SPDcls": "Produces Run2 centrality percentiles using SPD clusters multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "Run2CL0": "Produces Run2 centrality percentiles using CL0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "Run2CL1": "Produces Run2 centrality percentiles using CL1 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "FV0A": "Produces centrality percentiles using FV0A multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "FT0M": "Produces centrality percentiles using FT0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "FDDM": "Produces centrality percentiles using FDD multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "NTPV": "Produces centrality percentiles using number of tracks contributing to the PV. -1: auto, 0: don't, 1: yes. Default: auto (-1)"
}
centralityTableSelectionsList = []
for k, v in centralityTableSelections.items():
    centralityTableSelectionsList.append(k)

centralityTableParameters = [
    "estRun2V0M",
    "estRun2SPDtks",
    "estRun2SPDcls",
    "estRun2CL0",
    "estRun2CL1",
    "estFV0A",
    "estFT0M",
    "estFDDM",
    "estNTPV"
]
# TODO: Add genname parameter

v0SelectorParameters = [
    "d_bz",
    "v0cospa",
    "dcav0dau",
    "v0RMin",
    "v0Rmax",
    "dcamin",
    "dcamax,mincrossedrows",
    "maxchi2tpc"
]

ft0Selections = ["FT0", "NoFT0", "OnlyFT0", "Run2"]

ft0Parameters = ["processFT0", "processNoFT0", "processOnlyFT0", "processRun2"]

pidSelections = {
    "el": "Produce PID information for the Electron mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "mu": "Produce PID information for the Muon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "pi": "Produce PID information for the Pion mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "ka": "Produce PID information for the Kaon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "pr": "Produce PID information for the Proton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "de": "Produce PID information for the Deuterons mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "tr": "Produce PID information for the Triton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "he": "Produce PID information for the Helium3 mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "al": "Produce PID information for the Alpha mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)"
}
pidSelectionsList = []
for k, v in pidSelections.items():
    pidSelectionsList.append(k)

pidParameters = [
    "pid-el",
    "pid-mu",
    "pid-pi",
    "pid-ka",
    "pid-pr",
    "pid-de",
    "pid-tr",
    "pid-he",
    "pid-al"
]

collisionSystemSelections = ["PbPb", "pp", "pPb", "Pbp", "XeXe"]

booleanSelections = ["true", "false"]

debugLevelSelections = {
    "NOTSET": "Set Debug Level to NOTSET",
    "DEBUG": "Set Debug Level to DEBUG",
    "INFO": "Set Debug Level to INFO",
    "WARNING": "Set Debug Level to WARNING",
    "ERROR": "Set Debug Level to ERROR",
    "CRITICAL": "Set Debug Level to CRITICAL"
}
debugLevelSelectionsList = []
for k, v in debugLevelSelections.items():
    debugLevelSelectionsList.append(k)

eventMuonSelections = ["0", "1", "2"]

noDeleteNeedForCent = True
processLeftAfterCentDelete = True

isValidProcessFunc = True

threeSelectedList = []

clist = []  # control list for type control
allValuesCfg = []  # counter for provided args
allCuts = []  # all analysis cuts
allMCSignals = []  # all MC Signals
allPairCuts = []  # only pair cuts
nAddedAllCutsList = []  # e.g. muonQualityCuts:2
nAddedPairCutsList = []  # e.g paircutMass:3
selsWithOneColon = []  # track/muon cut:paircut:n
allSels = []  # track/muon cut::n
oneColon = ":"  # Namespace reference
doubleColon = "::"  # Namespace reference

# List for Transcation management for FilterPP
muonCutList = []  # List --> transcation management for filterPP
barrelTrackCutList = []  # List --> transcation management for filterPP
barrelSelsList = []
muonSelsList = []
barrelSelsListAfterSplit = []
muonSelsListAfterSplit = []

O2DPG_ROOT = os.environ.get("O2DPG_ROOT")
QUALITYCONTROL_ROOT = os.environ.get("QUALITYCONTROL_ROOT")
O2_ROOT = os.environ.get("O2_ROOT")
O2PHYSICS_ROOT = os.environ.get("O2PHYSICS_ROOT")

# Predefined values for DQ Logger messages
DQ_BARREL_SELECTED = False
DQ_BARRELTINY_SELECTED = False
DQ_MUON_SELECTED = False
DQ_EVENT_SELECTED = False
DQ_FULL_SELECTED = False
DQ_FILTERPP_SELECTED = False
DQ_FILTERPPTINY_SELECTED = False
DQ_QVECTOR_SELECTED = False


################################
# Download DQ Libs From Github #
################################

# It works on for only master branch

# header for github download
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}

urlCutsLibrary = 'https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/CutsLibrary.h'
urlMCSignalsLibrary ='https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/MCSignalLibrary.h'
urlEventMixing ='https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/MixingLibrary.h'

 
# Github Links for CutsLibrary and MCSignalsLibrary from PWG-DQ --> download from github
# This condition solves performance issues    
if (os.path.isfile('tempCutsLibrary.h') == False) or (os.path.isfile('tempMCSignalsLibrary.h') == False) or (os.path.isfile('tempMixingLibrary.h')) == False:
    print("[INFO] Some Libs are Missing. They will download.")
    
    # Dummy SSL Adder
    context = ssl._create_unverified_context()  # prevent ssl problems
    request = urllib.request.urlopen(urlCutsLibrary, context=context)
    
    # HTTP Request
    requestCutsLibrary = Request(urlCutsLibrary, headers=headers)
    requestMCSignalsLibrary = Request(urlMCSignalsLibrary, headers=headers)
    requestEventMixing  = Request(urlEventMixing , headers=headers)
    
    # Get Files With Http Requests
    htmlCutsLibrary = urlopen(requestCutsLibrary, context=context).read()
    htmlMCSignalsLibrary = urlopen(requestMCSignalsLibrary, context=context).read()
    htmlEventMixing = urlopen(requestEventMixing, context=context).read()
     
    # Save Disk to temp DQ libs  
    with open('tempCutsLibrary.h', 'wb') as f:
         f.write(htmlCutsLibrary)
    with open('tempMCSignalsLibrary.h', 'wb') as f:
         f.write(htmlMCSignalsLibrary)
    with open('tempMixingLibrary.h', 'wb') as f:
        f.write(htmlEventMixing)

# Read Cuts, Signals, Mixing vars from downloaded files
with open('tempMCSignalsLibrary.h') as f:
    for line in f:
        stringIfSearch = [x for x in f if 'if' in x] 
        for i in stringIfSearch:
            getSignals = re.findall('"([^"]*)"', i)
            allMCSignals = allMCSignals + getSignals
            
with open('tempCutsLibrary.h') as f:
    for line in f:
        stringIfSearch = [x for x in f if 'if' in x]  # get lines only includes if string
        for i in stringIfSearch:
            getAnalysisCuts = re.findall('"([^"]*)"', i)  # get in double quotes string value with regex exp.
            getPairCuts = [y for y in getAnalysisCuts         # get pair cuts
                        if 'pair' in y] 
            if getPairCuts: # if pair cut list is not empty
                allPairCuts = allPairCuts + getPairCuts # Get Only pair cuts from CutsLibrary.h
                namespacedPairCuts = [x + oneColon for x in allPairCuts] # paircut:
            allCuts = allCuts + getAnalysisCuts # Get all Cuts from CutsLibrary.h
            nameSpacedAllCuts = [x + oneColon for x in allCuts] # cut:
            nameSpacedAllCutsTwoDots = [x + doubleColon for x in allCuts]  # cut::

 
# in Filter PP Task, sels options for barrel and muon uses namespaces e.g. "<track-cut>:[<pair-cut>]:<n> and <track-cut>::<n> For Manage this issue:
for k in range (1,10):
    nAddedAllCuts = [x + str(k) for x in nameSpacedAllCutsTwoDots]
    nAddedAllCutsList = nAddedAllCutsList + nAddedAllCuts
    nAddedPairCuts = [x + str(k) for x in namespacedPairCuts]
    nAddedPairCutsList = nAddedPairCutsList + nAddedPairCuts
    
# Style 1 <track-cut>:[<pair-cut>]:<n>:
for i in nAddedPairCutsList:
    Style1 = [x + i for x in nameSpacedAllCuts]
    selsWithOneColon = selsWithOneColon + Style1
      
# Style 2 <track-cut>:<n> --> nAddedAllCutsList

# Merge All possible styles for Sels (cfgBarrelSels and cfgMuonSels) in FilterPP Task
allSels = selsWithOneColon + nAddedAllCutsList

    
###################
# Main Parameters #
###################

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='Arguments to pass')
parser.register('action', 'none', NoAction)
parser.register('action', 'store_choice', ChoicesAction)
groupCoreSelections = parser.add_argument_group(title='Core configurations that must be configured')
groupCoreSelections.add_argument('cfgFileName', metavar='Config.json', default='config.json', help='config JSON file name')
groupCoreSelections.add_argument('-runData', help="Run over data", action="store_true")
groupCoreSelections.add_argument('-runMC', help="Run over MC", action="store_true")
parser.add_argument('--run', help="Run Number Selection (2 or 3)", action="store", type=str, choices=("2","3")).completer = ChoicesCompleter(["2","3"])
#parser.add_argument('analysisString', metavar='text', help='my analysis string', required=False) # optional interface
groupTaskAdders = parser.add_argument_group(title='Additional Task Adding Options')
groupTaskAdders.add_argument('--add_mc_conv', help="Add the converter from mcparticle to mcparticle+001 (Adds your workflow o2-analysis-mc-converter task)", action="store_true")
groupTaskAdders.add_argument('--add_fdd_conv', help="Add the fdd converter (Adds your workflow o2-analysis-fdd-converter task)", action="store_true")
groupTaskAdders.add_argument('--add_track_prop', help="Add track propagation to the innermost layer (TPC or ITS) (Adds your workflow o2-analysis-track-propagation task)", action="store_true")

########################
# Interface Parameters #
########################

# aod
groupDPLReader = parser.add_argument_group(title='Data processor options: internal-dpl-aod-reader')
groupDPLReader.add_argument('--aod', help="Add your AOD File with path", action="store", type=str)
groupDPLReader.add_argument('--aod-memory-rate-limit', help="Rate limit AOD processing based on memory", action="store", type=str)

# automation params
groupAutomations = parser.add_argument_group(title='Automation Parameters')
groupAutomations.add_argument('--onlySelect', help="If false JSON Overrider Interface If true JSON Additional Interface", action="store", default="true", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
groupAutomations.add_argument('--autoDummy', help="Dummy automize parameter (don't configure it, true is highly recomended for automation)", action="store", default='true', type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# table-maker
groupTableMakerConfigs = parser.add_argument_group(title='Data processor options: table-maker/table-maker-m-c')
groupTableMakerConfigs.add_argument('--cfgEventCuts', help="Space separated list of event cuts", nargs='*', action="store", type=str, metavar='CFGEVENTCUTS', choices=allCuts).completer = ChoicesCompleterList(allCuts)
groupTableMakerConfigs.add_argument('--cfgBarrelTrackCuts', help=" Space separated list of barrel track cuts", nargs='*', action="store", type=str, metavar='CFGBARRELTRACKCUTS', choices=allCuts).completer = ChoicesCompleterList(allCuts)
groupTableMakerConfigs.add_argument('--cfgMuonCuts', help="Space separated list of muon cuts in table-maker", action="store", nargs='*', type=str, metavar='CFGMUONCUTS', choices=allCuts).completer = ChoicesCompleterList(allCuts)
groupTableMakerConfigs.add_argument('--cfgBarrelLowPt', help="Low pt cut for tracks in the barrel", action="store", type=str)
groupTableMakerConfigs.add_argument('--cfgMuonLowPt', help="Low pt cut for muons", action="store", type=str)
groupTableMakerConfigs.add_argument('--cfgNoQA', help="If true, no QA histograms", action="store", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
groupTableMakerConfigs.add_argument('--cfgDetailedQA', help="If true, include more QA histograms (BeforeCuts classes and more)", action="store", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
#groupTableMakerConfigs.add_argument('--cfgIsRun2', help="Run selection true or false", action="store", choices=["true","false"], type=str) # no need
groupTableMakerConfigs.add_argument('--cfgMinTpcSignal', help="Minimum TPC signal", action="store", type=str)
groupTableMakerConfigs.add_argument('--cfgMaxTpcSignal', help="Maximum TPC signal", action="store", type=str)
groupTableMakerConfigs.add_argument('--cfgMCsignals', help="Space separated list of MC signals", action="store", nargs='*', type=str, metavar='CFGMCSIGNALS', choices=allMCSignals).completer = ChoicesCompleterList(allMCSignals)

# table-maker process
groupProcessTableMaker = parser.add_argument_group(title='Data processor options: table-maker/table-maker-m-c')
groupProcessTableMaker.add_argument('--process',help="Process Selection options for tableMaker/tableMakerMC Data Processing and Skimming", action="store", type=str, nargs='*', metavar='PROCESS', choices=tablemakerProcessAllSelectionsList).completer = ChoicesCompleterList(tablemakerProcessAllSelectionsList)
for key,value in tablemakerProcessAllSelections.items():
    groupProcessTableMaker.add_argument(key, help=value, action='none')

# event-selection-task
groupEventSelection = parser.add_argument_group(title='Data processor options: event-selection-task')
groupEventSelection.add_argument('--syst', help="Collision System Selection ex. pp", action="store", type=str, choices=(collisionSystemSelections)).completer = ChoicesCompleter(collisionSystemSelections)
groupEventSelection.add_argument('--muonSelection', help="0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts", action="store", type=str, choices=(eventMuonSelections)).completer = ChoicesCompleter(eventMuonSelections)
groupEventSelection.add_argument('--customDeltaBC', help="custom BC delta for FIT-collision matching", action="store", type=str)

# multiplicity-table
groupMultiplicityTable = parser.add_argument_group(title='Data processor options: multiplicity-table')
groupMultiplicityTable.add_argument('--isVertexZeq', help="if true: do vertex Z eq mult table", action="store", type=str.lower, choices=(booleanSelections)).completer = ChoicesCompleter(booleanSelections)

# tof-pid, tof-pid-full
groupTofPid = parser.add_argument_group(title='Data processor options: tof-pid, tof-pid-full')
groupTofPid.add_argument('--isWSlice', help="Process with track slices", action="store",type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
groupTofPid.add_argument('--enableTimeDependentResponse', help="Flag to use the collision timestamp to fetch the PID Response", action="store",type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# track-propagation
groupTrackPropagation = parser.add_argument_group(title='Data processor options: track-propagation')
groupTrackPropagation.add_argument('--isCovariance', help="track-propagation : If false, Process without covariance, If true Process with covariance", action="store",type=str.lower, choices=(booleanSelections)).completer = ChoicesCompleter(booleanSelections)

# tof-pid-beta
groupTofPidBeta = parser.add_argument_group(title='Data processor options: tof-pid-beta')
groupTofPidBeta.add_argument('--tof-expreso', help="Expected resolution for the computation of the expected beta", action="store", type=str)

# tof-event-time
groupTofEventTime = parser.add_argument_group(title='Data processor options: tof-event-time')
groupTofEventTime.add_argument('--FT0', help="FT0: Process with FT0, NoFT0: Process without FT0, OnlyFT0: Process only with FT0, Run2: Process with Run2 data", action="store", type=str, choices=ft0Selections).completer = ChoicesCompleter(ft0Selections)

# d-q-track barrel-task
groupDQTrackBarrelTask = parser.add_argument_group(title='Data processor options: d-q-track barrel-task')
groupDQTrackBarrelTask.add_argument('--isBarrelSelectionTiny', help="Run barrel track selection instead of normal(process func. for barrel selection must be true)", action="store", default='false', type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# d-q muons-selection
groupDQMuonsSelection = parser.add_argument_group(title='Data processor options: d-q muons-selection')
groupDQMuonsSelection.add_argument('--cfgMuonsCuts', help="Space separated list of ADDITIONAL muon track cuts", action="store", nargs='*', type=str, metavar='CFGMUONSCUT', choices=allCuts).completer = ChoicesCompleterList(allCuts)

# d-q-filter-p-p-task
groupDQFilterPP = parser.add_argument_group(title='Data processor options: d-q-filter-p-p-task')
groupDQFilterPP.add_argument('--cfgBarrelSels', help="Configure Barrel Selection <track-cut>:[<pair-cut>]:<n>,[<track-cut>:[<pair-cut>]:<n>],... | example jpsiO2MCdebugCuts2::1 ", action="store", type=str,nargs="*", metavar='CFGBARRELSELS', choices=allSels).completer = ChoicesCompleterList(allSels)
groupDQFilterPP.add_argument('--cfgMuonSels', help="Configure Muon Selection <muon-cut>:[<pair-cut>]:<n> example muonQualityCuts:pairNoCut:1", action="store", type=str,nargs="*", metavar='CFGMUONSELS', choices=allSels).completer = ChoicesCompleterList(allSels)
groupDQFilterPP.add_argument('--isFilterPPTiny', help="Run filter tiny task instead of normal (processFilterPP must be true) ", action="store", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

groupAnalysisQvector = parser.add_argument_group(title='Data processor options: analysis-qvector')
#groupAnalysisQvector.add_argument('--cfgTrackCuts', help="Space separated list of barrel track cuts", choices=allCuts,nargs='*', action="store", type=str, metavar='CFGTRACKCUTS').completer = ChoicesCompleterList(allCuts)
#groupAnalysisQvector.add_argument('--cfgMuonCuts', help="Space separated list of muon cuts", action="store", choices=allCuts, nargs='*', type=str, metavar='CFGMUONCUTS').completer = ChoicesCompleterList(allCuts)
#groupAnalysisQvector.add_argument('--cfgEventCuts', help="Space separated list of event cuts", choices=allCuts, nargs='*', action="store", type=str, metavar='CFGEVENTCUT').completer = ChoicesCompleterList(allCuts)
#groupAnalysisQvector.add_argument('--cfgWithQA', help="If true, fill QA histograms", action="store", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
groupAnalysisQvector.add_argument('--cfgCutPtMin', help="Minimal pT for tracks", action="store", type=str, metavar='CFGCUTPTMIN')
groupAnalysisQvector.add_argument('--cfgCutPtMax', help="Maximal pT for tracks", action="store", type=str, metavar='CFGCUTPTMAX')
groupAnalysisQvector.add_argument('--cfgCutEta', help="Eta range for tracks", action="store", type=str, metavar='CFGCUTETA')
groupAnalysisQvector.add_argument('--cfgEtaLimit', help="Eta gap separation, only if using subEvents", action="store", type=str, metavar='CFGETALIMIT')
groupAnalysisQvector.add_argument('--cfgNPow', help="Power of weights for Q vector", action="store", type=str, metavar='CFGNPOW')

groupAnalysisQvector.add_argument('--cfgEfficiency', help="CCDB path to efficiency object", action="store", type=str)
groupAnalysisQvector.add_argument('--cfgAcceptance', help="CCDB path to acceptance object", action="store", type=str)

# centrality-table
groupCentralityTable = parser.add_argument_group(title='Data processor options: centrality-table')
groupCentralityTable.add_argument('--est', help="Produces centrality percentiles parameters", action="store", nargs="*", type=str, metavar='EST', choices=centralityTableSelectionsList).completer = ChoicesCompleterList(centralityTableSelectionsList)

for key,value in centralityTableSelections.items():
    groupCentralityTable.add_argument(key, help=value, action='none')

#all d-q tasks and selections
groupQASelections = parser.add_argument_group(title='Data processor options: d-q-barrel-track-selection-task, d-q-muons-selection, d-q-event-selection-task, d-q-filter-p-p-task, analysis-qvector')
groupQASelections.add_argument('--cfgWithQA', help="If true, fill QA histograms", action="store", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# v0-selector
groupV0Selector = parser.add_argument_group(title='Data processor options: v0-selector')
groupV0Selector.add_argument('--d_bz', help="bz field", action="store", type=str)
groupV0Selector.add_argument('--v0cospa', help="v0cospa", action="store", type=str)
groupV0Selector.add_argument('--dcav0dau', help="DCA V0 Daughters", action="store", type=str)
groupV0Selector.add_argument('--v0Rmin', help="v0Rmin", action="store", type=str)
groupV0Selector.add_argument('--v0Rmax', help="v0Rmax", action="store", type=str)
groupV0Selector.add_argument('--dcamin', help="dcamin", action="store", type=str)
groupV0Selector.add_argument('--dcamax', help="dcamax", action="store", type=str)
groupV0Selector.add_argument('--mincrossedrows', help="Min crossed rows", action="store", type=str)
groupV0Selector.add_argument('--maxchi2tpc', help="max chi2/NclsTPC", action="store", type=str)

# pid
groupPID = parser.add_argument_group(title='Data processor options: tof-pid, tpc-pid-full, tof-pid-full')
groupPID.add_argument('--pid', help="Produce PID information for the <particle> mass hypothesis", action="store", nargs='*', type=str.lower, metavar='PID', choices=pidSelectionsList).completer = ChoicesCompleterList(pidSelectionsList)

for key,value in pidSelections.items():
    groupPID.add_argument(key, help=value, action = 'none')

# helper lister commands
groupAdditionalHelperCommands = parser.add_argument_group(title='Additional Helper Command Options')
groupAdditionalHelperCommands.add_argument('--cutLister', help="List all of the analysis cuts from CutsLibrary.h", action="store_true")
groupAdditionalHelperCommands.add_argument('--MCSignalsLister', help="List all of the MCSignals from MCSignalLibrary.h", action="store_true")

# debug options
groupAdditionalHelperCommands.add_argument('--debug', help="execute with debug options", action="store", type=str.upper, default="INFO", choices=debugLevelSelectionsList).completer = ChoicesCompleterList(debugLevelSelectionsList)
groupAdditionalHelperCommands.add_argument('--logFile', help="Enable logger for both file and CLI", action="store_true")
groupDebug= parser.add_argument_group(title='Choice List for debug Parameters')

for key,value in debugLevelSelections.items():
    groupDebug.add_argument(key, help=value, action='none')

argcomplete.autocomplete(parser, always_complete_options=False)
extrargs = parser.parse_args()

configuredCommands = vars(extrargs) # for get extrargs

# Transcation management for forgettining assign a value to parameters
forgetParams = []
for key,value in configuredCommands.items():
    if(value != None):
        if (type(value) == type("string") or type(value) == type(clist)) and len(value) == 0:
            forgetParams.append(key)
if len(forgetParams) > 0: 
    print("[ERROR] Your forget assign a value to for this parameters: ", forgetParams)
    sys.exit()
    
# Debug Settings
if extrargs.debug and extrargs.logFile == False:
    DEBUG_SELECTION = extrargs.debug
    numeric_level = getattr(logging, DEBUG_SELECTION.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % DEBUG_SELECTION)
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=DEBUG_SELECTION)
    
if extrargs.logFile and extrargs.debug:
    log = logging.getLogger('')
    level = logging.getLevelName(extrargs.debug)
    log.setLevel(level)
    format = logging.Formatter("%(asctime)s - [%(levelname)s] %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(format)
    log.addHandler(ch)
    
    loggerFile = "tableMaker.log"
    if os.path.isfile(loggerFile) == True:
        os.remove(loggerFile)
    
    fh = handlers.RotatingFileHandler(loggerFile, maxBytes=(1048576*5), backupCount=7, mode='w')
    fh.setFormatter(format)
    log.addHandler(fh)


###################
# HELPER MESSAGES #
###################
   
if extrargs.cutLister and extrargs.MCSignalsLister:
    counter = 0
    print("Analysis Cut Options :")
    print("====================")
    temp = ''  
    for i in allCuts:
        if len(temp) == 0:
            temp = temp + i
        else:
            temp = temp + "," + i
        counter = counter + 1
        if counter == 3:
            temp = stringToList(temp)
            threeSelectedList.append(temp)
            temp = ''
            counter = 0
    for list_ in threeSelectedList:
        print('{:<40s} {:<40s} {:<40s}'.format(*list_)) 
        
    counter = 0
    print("MC Signals :")
    print("====================")
    temp = ''
    threeSelectedList.clear()  
    for i in allMCSignals:
        if len(temp) == 0:
            temp = temp + i
        else:
            temp = temp + "," + i
        counter = counter + 1
        if counter == 3:
            temp = stringToList(temp)
            threeSelectedList.append(temp)
            temp = ''
            counter = 0
    for list_ in threeSelectedList:
        print('{:<40s} {:<40s} {:<40s}'.format(*list_))  
    sys.exit()
    
if extrargs.cutLister:
    counter = 0
    print("Analysis Cut Options :")
    print("====================")
    temp = ''  
    for i in allCuts:
        if len(temp) == 0:
            temp = temp + i
        else:
            temp = temp + "," + i
        counter = counter + 1
        if counter == 3:
            temp = stringToList(temp)
            threeSelectedList.append(temp)
            temp = ''
            counter = 0
    for list_ in threeSelectedList:
        print('{:<40s} {:<40s} {:<40s}'.format(*list_))      
    sys.exit()
    
if extrargs.MCSignalsLister:
    counter = 0
    print("MC Signals :")
    print("====================")
    temp = ''  
    for i in allMCSignals:
        if len(temp) == 0:
            temp = temp + i
        else:
            temp = temp + "," + i
        counter = counter + 1
        if counter == 3:
            temp = stringToList(temp)
            threeSelectedList.append(temp)
            temp = ''
            counter = 0
    for list_ in threeSelectedList:
        print('{:<40s} {:<40s} {:<40s}'.format(*list_))     
    sys.exit()

######################
# PREFIX ADDING PART #
###################### 

# add prefix for extrargs.process for table-maker/table-maker-m-c and d-q-filter-p-p
if extrargs.process != None:
    prefix_process = "process"
    extrargs.process = [prefix_process + sub for sub in extrargs.process]

# add prefix for extrargs.pid for pid selection
if extrargs.pid != None:
    prefix_pid = "pid-"
    extrargs.pid = [prefix_pid + sub for sub in extrargs.pid]
    
# add prefix for extrargs.est for centrality-table
if extrargs.est != None:
    prefix_est = "est"
    extrargs.est = [prefix_est + sub for sub in extrargs.est]

# add prefix for extrargs.FT0 for tof-event-time
if extrargs.FT0 != None:
    prefix_process = "process"
    extrargs.FT0 = prefix_process + extrargs.FT0
    
######################################################################################

commonDeps = [
    "o2-analysis-timestamp",
    "o2-analysis-event-selection",
    "o2-analysis-multiplicity-table"
]
barrelDeps = [
    "o2-analysis-trackselection",
    "o2-analysis-trackextension",
    "o2-analysis-pid-tof-base",
    "o2-analysis-pid-tof",
    "o2-analysis-pid-tof-full",
    "o2-analysis-pid-tof-beta",
    "o2-analysis-pid-tpc-full"
]
specificDeps = {
  "processFull": [],
  "processFullTiny": [],
  "processFullWithCov": [],
  "processFullWithCent": ["o2-analysis-centrality-table"],
  "processBarrelOnly": [],
  "processBarrelOnlyWithCov": [],
  "processBarrelOnlyWithV0Bits": ["o2-analysis-dq-v0-selector", "o2-analysis-weak-decay-indices"],
  "processBarrelOnlyWithEventFilter": ["o2-analysis-dq-filter-pp"],
  "processBarrelOnlyWithQvector": ["o2-analysis-centrality-table", "o2-analysis-dq-flow"],
  "processBarrelOnlyWithCent": ["o2-analysis-centrality-table"],
  "processMuonOnly": [],
  "processMuonOnlyWithCov": [],
  "processMuonOnlyWithCent": ["o2-analysis-centrality-table"],
  "processMuonOnlyWithQvector": ["o2-analysis-centrality-table", "o2-analysis-dq-flow"],
  "processMuonOnlyWithFilter": ["o2-analysis-dq-filter-pp"]
  #"processFullWithCentWithV0Bits": ["o2-analysis-centrality-table","o2-analysis-dq-v0-selector", "o2-analysis-weak-decay-indices"],
  #"processFullWithEventFilterWithV0Bits": ["o2-analysis-dq-filter-pp","o2-analysis-dq-v0-selector", "o2-analysis-weak-decay-indices"],
} 

# Definition of all the tables we may write
tables = {
  "ReducedEvents": {"table": "AOD/REDUCEDEVENT/0", "treename": "ReducedEvents"},
  "ReducedEventsExtended": {"table": "AOD/REEXTENDED/0", "treename": "ReducedEventsExtended"},
  "ReducedEventsVtxCov": {"table": "AOD/REVTXCOV/0", "treename": "ReducedEventsVtxCov"},
  "ReducedEventsQvector": {"table": "AOD/REQVECTOR/0", "treename": "ReducedEventsQvector"},
  "ReducedMCEventLabels": {"table": "AOD/REMCCOLLBL/0", "treename": "ReducedMCEventLabels"},
  "ReducedMCEvents": {"table": "AOD/REMC/0", "treename": "ReducedMCEvents"},
  "ReducedTracks": {"table": "AOD/REDUCEDTRACK/0", "treename": "ReducedTracks"},
  "ReducedTracksBarrel": {"table": "AOD/RTBARREL/0", "treename": "ReducedTracksBarrel"},
  "ReducedTracksBarrelCov": {"table": "AOD/RTBARRELCOV/0", "treename": "ReducedTracksBarrelCov"},
  "ReducedTracksBarrelPID": {"table": "AOD/RTBARRELPID/0", "treename": "ReducedTracksBarrelPID"},
  "ReducedTracksBarrelLabels": {"table": "AOD/RTBARRELLABELS/0", "treename": "ReducedTracksBarrelLabels"},
  "ReducedMCTracks": {"table": "AOD/RTMC/0", "treename": "ReducedMCTracks"},
  "ReducedMuons": {"table": "AOD/RTMUON/0", "treename": "ReducedMuons"},
  "ReducedMuonsExtra" : {"table": "AOD/RTMUONEXTRA/0", "treename": "ReducedMuonsExtra"},
  "ReducedMuonsCov": {"table": "AOD/RTMUONCOV/0", "treename": "ReducedMuonsCov"},
  "ReducedMuonsLabels": {"table": "AOD/RTMUONSLABELS/0", "treename": "ReducedMuonsLabels"}
}
# Tables to be written, per process function
commonTables = ["ReducedEvents", "ReducedEventsExtended", "ReducedEventsVtxCov"]
barrelCommonTables = ["ReducedTracks","ReducedTracksBarrel","ReducedTracksBarrelPID"]
muonCommonTables = ["ReducedMuons", "ReducedMuonsExtra"]
specificTables = {
  "processFull": [],
  "processFullTiny": [],
  "processFullWithCov": ["ReducedTracksBarrelCov", "ReducedMuonsCov"],
  "processFullWithCent": [],
  "processBarrelOnly": [],
  "processBarrelOnlyWithCov": ["ReducedTracksBarrelCov"],
  "processBarrelOnlyWithV0Bits": [],
  "processBarrelOnlyWithQvector": ["ReducedEventsQvector"],
  "processBarrelOnlyWithEventFilter": [],
  "processBarrelOnlyWithCent": [],
  "processMuonOnly": [],
  "processMuonOnlyWithCov": ["ReducedMuonsCov"],
  "processMuonOnlyWithCent": [],
  "processMuonOnlyWithQvector": ["ReducedEventsQvector"],
  "processMuonOnlyWithFilter": []
}

# Make some checks on provided arguments
if len(sys.argv) < 3:
  logging.error("Invalid syntax! The command line should look like this:")
  logging.info("  ./IRunTableMaker.py <yourConfig.json> <-runData|-runMC> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
cfgControl = sys.argv[1] == extrargs.cfgFileName 
config = {}
try:
    if cfgControl:
        with open(extrargs.cfgFileName) as configFile:           
            config = json.load(configFile)
    else:
        logging.error("Invalid syntax! After the script you must define your json configuration file!!! The command line should look like this:")
        logging.info("  ./IRunTableMaker.py <yourConfig.json> <-runData|-runMC> --param value ...")
        sys.exit()
        
except FileNotFoundError:
    isConfigJson = sys.argv[1].endswith('.json')
    if isConfigJson == False:
            logging.error("Invalid syntax! After the script you must define your json configuration file!!! The command line should look like this:")
            logging.info("  ./IRunTableMaker.py <yourConfig.json> <-runData|-runMC> --param value ...")
            sys.exit()
    logging.error("Your JSON Config File found in path!!!")
    sys.exit()

# Check whether we run over data or MC
if not (extrargs.runMC or extrargs.runData):
    logging.error("You have to specify either runMC or runData !")
    logging.info("Example For MC : python3 IRunTableMaker.py <yourConfig.json> -runMC --run <2|3> --param value ...")
    logging.info("Example For MC : python3 IRunTableMaker.py <yourConfig.json> -runData --run <2|3> --param value ...")
    sys.exit()
    
# Transcation management for Data and MC
if extrargs.runMC and extrargs.runData:
    logging.error("runData and runMC cannot be configured at the same time ! Choose one")
    logging.info("Example For MC : python3 IRunTableMaker.py <yourConfig.json> -runMC --run <2|3> --param value ...")
    logging.info("Example For MC : python3 IRunTableMaker.py <yourConfig.json> -runData --run <2|3> --param value ...")
    sys.exit()
    
runOverMC = False
if (extrargs.runMC):
    runOverMC = True

logging.info("runOverMC : %s ",runOverMC)

# Optional Interface
"""
if extrargs.analysisString != "":
  args = [line.split(':') for line in extrargs.analysisString.split(',') if line]
  for arg in args:
    config[arg[0]][arg[1]] = arg[2]
"""

taskNameInConfig = "table-maker"
taskNameInCommandLine = "o2-analysis-dq-table-maker"
if runOverMC == True:
  taskNameInConfig = "table-maker-m-c"
  taskNameInCommandLine = "o2-analysis-dq-table-maker-mc"
  
# Check table-maker and tablemaker-m-c dependencies
if extrargs.runMC:
    try:
        if config["table-maker-m-c"]:
            logging.info("tablemaker-m-c is in your JSON Config File")
    except:
        logging.error("JSON config does not include table-maker-m-c, It's for Data. Misconfiguration JSON File!!!")
        sys.exit()
if extrargs.runData:
    try:
        if config["table-maker"]:
            logging.info("tablemaker is in your JSON Config File")
    except:
        logging.error("JSON config does not include table-maker, It's for MC. Misconfiguration JSON File!!!")
        sys.exit()
        
# Check alienv
if O2PHYSICS_ROOT == None:
   logging.error("You must load O2Physics with alienv")
   sys.exit()

#############################
# Start Interface Processes #
#############################

logging.info("Only Select Configured as %s", extrargs.onlySelect)
if extrargs.onlySelect == "true":
    logging.info("INTERFACE MODE : JSON Overrider")
if extrargs.onlySelect == "false":
    logging.info("INTERFACE MODE : JSON Additional")

# For adding a process function from TableMaker and all process should be added only once so set type used
tableMakerProcessSearch= set ()

for key, value in config.items():
    if type(value) == type(config):
        for value, value2 in value.items():
                       
            # aod
            if value =='aod-file' and extrargs.aod:
                config[key][value] = extrargs.aod
                logging.debug(" - [%s] %s : %s",key,value,extrargs.aod)
                
            # table-maker/table-maker-m-c process selections
            if (value in tablemakerProcessAllParameters) and extrargs.process:
                if value in extrargs.process:
                    value2 = "true"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)
                                           
                    # For find all process parameters for TableMaker/TableMakerMC in Orginal JSON
                    for s in config[key].keys():
                        if s in tablemakerProcessAllParameters:
                            tableMakerProcessSearch.add(s)
                    # check extraargs is contain Full Barrel Muon or Bcs
                    fullSearch = [s for s in extrargs.process if "Full" in s]
                    barrelSearch = [s for s in extrargs.process if "Barrel" in s]
                    muonSearch = [s for s in extrargs.process if "Muon" in s]
                    bcsSearch = [s for s in extrargs.process if "BCs" in s]
                    
                    # check extrargs is contain Cent for transcation management Centrality Filter
                    centSearch = [s for s in extrargs.process if "Cent" in s]
                    
                    # check extrargs is contain Filter for automatize Filter PP task
                    filterSearch = [s for s in extrargs.process if "Filter" in s]   
                    
                    # check extrargs is contain Qvector for automatize dqFlow task
                    qvectorSearch = [s for s in extrargs.process if "Qvector" in s] 
                                                         
                    # Automatization for Activate or Disable d-q barrel, muon and event tasks regarding to process func. in tablemaker
                    if len(fullSearch) > 0 and extrargs.runData:
                        config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                        DQ_FULL_SELECTED = True
                        #logging.debug(" - [d-q-barrel-track-selection-task] processSelection : true")
                        
                        if extrargs.isBarrelSelectionTiny == "false":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
                            #logging.debug(" - [d-q-barrel-track-selection-task] processSelection : true")
                            #logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : false")
                        if extrargs.isBarrelSelectionTiny == "true":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
                            DQ_BARRELTINY_SELECTED = True
                            #logging.debug(" - [d-q-barrel-track-selection-task] processSelection : false")
                            #logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : true")

                        config["d-q-muons-selection"]["processSelection"] = "true"
                        DQ_MUON_SELECTED  = True
                        #logging.debug(" - [d-q-muons-selection] processSelection : true")

                        config["d-q-event-selection-task"]["processEventSelection"] = "true"
                        DQ_EVENT_SELECTED = True
                        #logging.debug(" - [d-q-event-selection-task] processEventSelection : true")
                                   
                    if len(barrelSearch) > 0 and extrargs.runData:
                        if extrargs.isBarrelSelectionTiny == "false":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
                            DQ_BARREL_SELECTED = True
                            DQ_BARRELTINY_SELECTED = False
                            #logging.debug(" - [d-q-barrel-track-selection-task] processSelection : true")
                            #logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : false")
                        if extrargs.isBarrelSelectionTiny == "true":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
                            DQ_BARREL_SELECTED = False
                            DQ_BARRELTINY_SELECTED = True
                            #logging.debug(" - [d-q-barrel-track-selection-task] processSelection : false")
                            #logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : true")
   
                    if len(barrelSearch) == 0 and len(fullSearch) == 0 and extrargs.runData:
                        config["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                        config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = "false"
                        #logging.debug(" - [d-q-barrel-track-selection-task] processSelection : false")
                        #logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : false")
                                         
                    if len(muonSearch) > 0 and extrargs.runData:
                        config["d-q-muons-selection"]["processSelection"] = "true"
                        #logging.debug(" - [d-q-muons-selection] processSelection : true")
                        DQ_MUON_SELECTED  = True
                    if len(muonSearch) == 0 and len(fullSearch) == 0 and extrargs.runData:
                        config["d-q-muons-selection"]["processSelection"] = "false"
                        #logging.debug(" - [d-q-muons-selection] processSelection : false")
                            
                    if len(bcsSearch) > 0 and extrargs.runData:
                        config["d-q-event-selection-task"]["processEventSelection"] = "true"
                        DQ_EVENT_SELECTED = True
                        #logging.debug(" - [d-q-event-selection-task] processEventSelection : true")
                    if len(bcsSearch) == 0 and len(fullSearch) == 0 and extrargs.runData:
                        config["d-q-event-selection-task"]["processEventSelection"] = "false"
                        #logging.debug(" - [d-q-event-selection-task] processEventSelection : false")
                           
                    # Automatization for Activate or Disable d-q filter-p-p
                    if len(filterSearch) > 0 and extrargs.runData:
                        config["d-q-filter-p-p-task"]["processFilterPP"] ="true"
                        config["d-q-filter-p-p-task"]["processFilterPPTiny"] ="false"
                        DQ_FILTERPP_SELECTED = True
                        DQ_FILTERPPTINY_SELECTED = False                     
                        #logging.debug(" - [d-q-filter-p-p-task-task] processFilterPP : true")
                        #logging.debug(" - [d-q-filter-p-p-task-task] processFilterPPTiny : false")
                        if extrargs.isFilterPPTiny == 'true':
                            config["d-q-filter-p-p-task"]["processFilterPP"] = "false"
                            config["d-q-filter-p-p-task"]["processFilterPPTiny"] = "true"
                            DQ_FILTERPP_SELECTED = False
                            DQ_FILTERPPTINY_SELECTED = True  
                            #logging.debug(" - [d-q-filter-p-p-task-task] processFilterPP : false")
                            #logging.debug(" - [d-q-filter-p-p-task-task] processFilterPPTiny : true")
                                 
                    if len(filterSearch) == 0 and extrargs.runData:
                        config["d-q-filter-p-p-task"]["processFilterPP"] = "false"
                        config["d-q-filter-p-p-task"]["processFilterPPTiny"] = "false"
                        DQ_FILTERPP_SELECTED = False
                        DQ_FILTERPPTINY_SELECTED = False 
                        #logging.debug(" - [d-q-filter-p-p-task-task] processFilterPP : false")
                        #logging.debug(" - [d-q-filter-p-p-task-task] processFilterPPTiny : true")
                        
                    # Automatization for Activate or Disable analysis-qvector
                    if len(qvectorSearch) > 0 and extrargs.runData:
                        config["analysis-qvector"]["processQvector"] ="true"
                        DQ_QVECTOR_SELECTED = True

                    if len(qvectorSearch) == 0 and extrargs.runData:
                        config["analysis-qvector"]["processQvector"] ="false"
                        DQ_QVECTOR_SELECTED = False
                                                                        
                elif extrargs.onlySelect == "true":
                    value2 = "false"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)
                                                     
            # filterPP Selections        
            if value == 'cfgBarrelSels' and extrargs.cfgBarrelSels:
                if type(extrargs.cfgBarrelSels) == type(clist):
                    extrargs.cfgBarrelSels = listToString(extrargs.cfgBarrelSels) 
                config[key][value] = extrargs.cfgBarrelSels
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgBarrelSels)
            if value == 'cfgMuonSels' and extrargs.cfgMuonSels:
                if type(extrargs.cfgMuonSels) == type(clist):
                    extrargs.cfgMuonSels = listToString(extrargs.cfgMuonSels) 
                config[key][value] = extrargs.cfgMuonSels
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonSels)
                                    
            # Run 2/3 and MC/DATA Selections for automations            
            if extrargs.run == "2":
                if value == 'isRun3':
                    config[key][value] = "false"
                    logging.debug(" - [%s] %s : false",key,value)
                if value == 'processRun3':
                    config[key][value] = "false"
                    logging.debug(" - [%s] %s : false",key,value)
                if value == 'processRun2':
                    config[key][value] = "true"
                    logging.debug(" - [%s] %s : true",key,value)
                    
            if extrargs.run == "3":
                if value == 'isRun3':
                    config[key][value] = "true"
                    logging.debug(" - [%s] %s : true",key,value)
                if value == 'processRun3':
                    config[key][value] = "true"
                    logging.debug(" - [%s] %s : true",key,value)
                if value == 'processRun2':
                    config[key][value] = "false"
                    logging.debug(" - [%s] %s : false",key,value)
            
            if extrargs.run == '2' and extrargs.runMC:
                if value == 'isRun2MC':
                    config[key][value] = "true"
                    logging.debug(" - [%s] %s : true",key,value)
            if extrargs.run != '2' and extrargs.runData:
                if value == 'isRun2MC':
                    config[key][value] = "false"
                    logging.debug(" - [%s] %s : false",key,value)
                                            
            if value == "isMC" and extrargs.runMC:
                    config[key][value] = "true"
                    logging.debug(" - [%s] %s : true",key,value)        
            if value == "isMC" and extrargs.runData:
                    config[key][value] = "false"
                    logging.debug(" - [%s] %s : false",key,value)                          
                       
            # PID Selections
            if  (value in pidParameters) and extrargs.pid:
                if value in extrargs.pid:
                    value2 = "1"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)  
                elif extrargs.onlySelect == "true":
                    value2 = "-1"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)
                    
            # analysis-qvector selections    
            if value =='cfgCutPtMin' and extrargs.cfgCutPtMin:
                config[key][value] = extrargs.cfgCutPtMin
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgCutPtMin)
            if value =='cfgCutPtMax' and extrargs.cfgCutPtMax:
                config[key][value] = extrargs.cfgCutPtMax
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgCutPtMax)
            if value =='cfgCutEta' and extrargs.cfgCutEta:
                config[key][value] = extrargs.cfgCutEta
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgCutEta)
            if value =='cfgEtaLimit' and extrargs.cfgEtaLimit:
                config[key][value] = extrargs.cfgEtaLimit
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgEtaLimit)
            if value =='cfgNPow' and extrargs.cfgNPow:
                config[key][value] = extrargs.cfgNPow
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgNPow)
            if value =='cfgEfficiency' and extrargs.cfgEfficiency:
                config[key][value] = extrargs.cfgEfficiency
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgEfficiency)
            if value =='cfgAcceptance' and extrargs.cfgAcceptance:
                config[key][value] = extrargs.cfgAcceptance
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgAcceptance)  
                    
            # v0-selector
            if value =='d_bz' and extrargs.d_bz:
                config[key][value] = extrargs.d_bz
                logging.debug(" - [%s] %s : %s",key,value,extrargs.d_bz)  
            if value == 'v0cospa' and extrargs.v0cospa:
                config[key][value] = extrargs.v0cospa
                logging.debug(" - [%s] %s : %s",key,value,extrargs.v0cospa)  
            if value == 'dcav0dau' and extrargs.dcav0dau:
                config[key][value] = extrargs.dcav0dau
                logging.debug(" - [%s] %s : %s",key,value,extrargs.dcav0dau)                  
            if value =='v0Rmin' and extrargs.v0Rmin:
                config[key][value] = extrargs.v0Rmin
                logging.debug(" - [%s] %s : %s",key,value,extrargs.v0Rmin)                  
            if value == 'v0Rmax' and extrargs.v0Rmax:
                config[key][value] = extrargs.v0Rmax
                logging.debug(" - [%s] %s : %s",key,value,extrargs.v0Rmax)                  
            if value == 'dcamin' and extrargs.dcamin:
                config[key][value] = extrargs.dcamin
                logging.debug(" - [%s] %s : %s",key,value,extrargs.dcamin)                  
            if value == 'dcamax' and extrargs.dcamax:
                config[key][value] = extrargs.dcamax
                logging.debug(" - [%s] %s : %s",key,value,extrargs.dcamax)                  
            if value =='mincrossedrows' and extrargs.mincrossedrows:
                config[key][value] = extrargs.mincrossedrows
                logging.debug(" - [%s] %s : %s",key,value,extrargs.mincrossedrows)                  
            if value == 'maxchi2tpc' and extrargs.maxchi2tpc:
                config[key][value] = extrargs.maxchi2tpc
                logging.debug(" - [%s] %s : %s",key,value,extrargs.maxchi2tpc)                  
                
            # centrality-table
            if (value in centralityTableParameters) and extrargs.est:
                if value in extrargs.est:
                    value2 = "1"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)   
                elif extrargs.onlySelect == "true":
                    value2 = "-1"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)  
                    
            # table-maker/table-maker-m-c cfg selections
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts)
                if extrargs.onlySelect == 'false':
                    actualConfig = config[key][value]
                    extrargs.cfgEventCuts = actualConfig + ',' + extrargs.cfgEventCuts 
                config[key][value] = extrargs.cfgEventCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgEventCuts)  
            if (value == 'cfgBarrelTrackCuts' or value == 'cfgTrackCuts') and extrargs.cfgBarrelTrackCuts:
                if type(extrargs.cfgBarrelTrackCuts) == type(clist):
                    extrargs.cfgBarrelTrackCuts = listToString(extrargs.cfgBarrelTrackCuts)
                if extrargs.onlySelect == 'false':
                    actualConfig = config[key][value]
                    extrargs.cfgBarrelTrackCuts = actualConfig + ',' + extrargs.cfgBarrelTrackCuts 
                config[key][value] = extrargs.cfgBarrelTrackCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgBarrelTrackCuts)  
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                if type(extrargs.cfgMuonCuts) == type(clist):
                    extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts)  
                if extrargs.onlySelect == 'false':
                    actualConfig = config[key][value]
                    extrargs.cfgMuonCuts = actualConfig + ',' + extrargs.cfgMuonCuts               
                config[key][value] = extrargs.cfgMuonCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonCuts)  
            if value == 'cfgBarrelLowPt' and extrargs.cfgBarrelLowPt:
                config[key][value] = extrargs.cfgBarrelLowPt
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgBarrelLowPt)  
            if value == 'cfgMuonLowPt' and extrargs.cfgMuonLowPt:
                config[key][value] = extrargs.cfgMuonLowPt
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonLowPt)  
            if value =='cfgNoQA' and extrargs.cfgNoQA:
                config[key][value] = extrargs.cfgNoQA
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgNoQA)  
            if value == 'cfgDetailedQA' and extrargs.cfgDetailedQA:
                config[key][value] = extrargs.cfgDetailedQA
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgDetailedQA)  
            if value == 'cfgIsRun2' and extrargs.run == "2":
                config[key][value] = "true"
                logging.debug(" - %s %s : true",key,value)  
            if value =='cfgMinTpcSignal' and extrargs.cfgMinTpcSignal:
                config[key][value] = extrargs.cfgMinTpcSignal
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMinTpcSignal)  
            if value == 'cfgMaxTpcSignal' and extrargs.cfgMaxTpcSignal:
                config[key][value] = extrargs.cfgMaxTpcSignal
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMaxTpcSignal)  
            if value == 'cfgMCsignals' and extrargs.cfgMCsignals:
                if type(extrargs.cfgMCsignals) == type(clist):
                    extrargs.cfgMCsignals = listToString(extrargs.cfgMCsignals)
                if extrargs.onlySelect == 'false':
                    actualConfig = config[key][value]
                    extrargs.cfgMCsignals = actualConfig + ',' + extrargs.cfgMCsignals                     
                config[key][value] = extrargs.cfgMCsignals
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMCsignals)  
                
            #d-q-muons-selection
            if value =='cfgMuonsCuts' and extrargs.cfgMuonsCuts:
                if type(extrargs.cfgMuonsCuts) == type(clist):
                    extrargs.cfgMuonsCuts = listToString(extrargs.cfgMuonsCuts)
                if extrargs.onlySelect == 'false':
                    actualConfig = config[key][value]
                    extrargs.cfgMuonsCuts = actualConfig + ',' + extrargs.cfgMuonsCuts                  
                config[key][value] = extrargs.cfgMuonsCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonsCuts) 

            # event-selection-task
            if value == 'syst' and extrargs.syst:
                config[key][value] = extrargs.syst
                logging.debug(" - [%s] %s : %s",key,value,extrargs.syst)  
            if value =='muonSelection' and extrargs.muonSelection:
                config[key][value] = extrargs.muonSelection
                logging.debug(" - [%s] %s : %s",key,value,extrargs.muonSelection)  
            if value == 'customDeltaBC' and extrargs.customDeltaBC:
                config[key][value] = extrargs.customDeltaBC
                logging.debug(" - [%s] %s : %s",key,value,extrargs.customDeltaBC)  
             
            # multiplicity-table
            if value == "doVertexZeq" and extrargs.isVertexZeq:
                if extrargs.isVertexZeq == "true":
                    config[key][value] = "1"
                    config[key]["doDummyZeq"] = "0"
                    logging.debug(" - %s %s : 1",key,value)
                    logging.debug(" - [%s] doDummyZeq : 0",key)  
                if extrargs.isVertexZeq == "false":
                    config[key][value] = "0"
                    config[key]["doDummyZeq"] = "1"
                    logging.debug(" - %s %s : 0",key,value) 
                    logging.debug(" - [%s] doDummyZeq : 1",key)
                    
            # tof-pid, tof-pid-full
            if value == "processWSlice" and extrargs.isWSlice:
                if extrargs.isWSlice == "true":
                    config[key][value] = "true"
                    config[key]["processWoSlice"] = "false"
                    logging.debug(" - %s %s : true",key,value)
                    logging.debug(" - [%s] processWoSlice : false",key)  
                if extrargs.isWSlice == "false":
                    config[key][value] = "false"
                    config[key]["processWoSlice"] = "true"
                    logging.debug(" - %s %s : false",key,value) 
                    logging.debug(" - [%s] processWoSlice : true",key)
                    
            if value == "enableTimeDependentResponse" and extrargs.enableTimeDependentResponse:
                    config[key][value] = extrargs.enableTimeDependentResponse
                    logging.debug(" - [%s] %s : %s",key,value,extrargs.enableTimeDependentResponse)
                     
            # tof-pid-beta
            if value == 'tof-expreso' and extrargs.tof_expreso:
                config[key][value] = extrargs.tof_expreso
                logging.debug(" - [%s] %s : %s",key,value,extrargs.tof_expreso)
                
            # tof-event-time
            if  (value in ft0Parameters) and extrargs.FT0 and key == 'tof-event-time':
                if value  == extrargs.FT0:
                    value2 = "true"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)  
                elif value != extrargs.FT0:
                    value2 = "false"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)  
                                             
            # all d-q tasks and selections
            if (value == 'cfgWithQA' or value == 'cfgQA') and extrargs.cfgWithQA:
                config[key][value] = extrargs.cfgWithQA
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgWithQA)  
                                  
            # track-propagation
            if extrargs.isCovariance:
                if (value =='processStandard' or value == 'processCovariance') and extrargs.isCovariance == 'false' :
                    config[key]["processStandard"] = "true"
                    config[key]["processCovariance"] = "false"
                    logging.debug(" - [%s] processStandart : true",key)
                    logging.debug(" - [%s] processCovariance : false",key) 
                if (value =='processStandard' or value == 'processCovariance') and extrargs.isCovariance == 'true' :
                    config[key]["processStandard"] = "false"
                    config[key]["processCovariance"] = "true"
                    logging.debug(" - [%s] processStandart : false",key)
                    logging.debug(" - [%s] processCovariance : true",key) 
                                    
            # dummy automizer
            if value == 'processDummy' and extrargs.autoDummy and extrargs.runData:
                
                if config["d-q-barrel-track-selection-task"]["processSelection"] == "true" or config["d-q-barrel-track-selection-task"]["processSelectionTiny"] == "true":
                    config["d-q-barrel-track-selection-task"]["processDummy"] = "false"
                    #logging.debug("d-q-barrel-track-selection-task:processDummy:false") 
                if config["d-q-barrel-track-selection-task"]["processSelection"] == 'false' and config["d-q-barrel-track-selection-task"]["processSelectionTiny"]  == "false":
                    config["d-q-barrel-track-selection-task"]["processDummy"] = "true"
                    #logging.debug("d-q-barrel-track-selection-task:processDummy:true") 
                    
                if config["d-q-muons-selection"]["processSelection"] == "true":
                    config["d-q-muons-selection"]["processDummy"] = "false"
                    #logging.debug("d-q-muons-selection:processDummy:false") 
                if config["d-q-muons-selection"]["processSelection"] == "false":
                    config["d-q-muons-selection"]["processDummy"] = "true"
                    #logging.debug("d-q-muons-selection:processDummy:true") 
                    
                if config["d-q-event-selection-task"]["processEventSelection"] == "true":
                    config["d-q-event-selection-task"]["processDummy"] = "false"
                    #logging.debug("d-q-event-selection-task:processDummy:false") 
                if config["d-q-event-selection-task"]["processEventSelection"] == "false":
                    config["d-q-event-selection-task"]["processDummy"] = "true"
                    #logging.debug("d-q-event-selection-task:processDummy:true") 
                    
                if config["d-q-filter-p-p-task"]["processFilterPP"] =="true" or config["d-q-filter-p-p-task"]["processFilterPPTiny"] == "true":
                    config["d-q-filter-p-p-task"]["processDummy"] = "false"
                    #logging.debug("d-q-filter-p-p-task:processDummy:false")
                if config["d-q-filter-p-p-task"]["processFilterPP"] == "false" and config["d-q-filter-p-p-task"]["processFilterPPTiny"] == "false" :
                    config["d-q-filter-p-p-task"]["processDummy"] = "true"
                    #logging.debug("d-q-filter-p-p-task:processDummy:true")
                    
                if config["analysis-qvector"]["processQvector"] == "true":
                    config["analysis-qvector"]["processDummy"] = "false" 
                if config["analysis-qvector"]["processQvector"] == "false":
                    config["analysis-qvector"]["processDummy"] = "true"             
                    
# LOGGER MESSAGES FOR DQ SELECTIONS

if extrargs.runData:

    if DQ_FULL_SELECTED == True:
        logging.debug(" - [d-q-event-selection-task] processEventSelection : true")
        
        if DQ_BARREL_SELECTED == True:
            logging.debug(" - [d-q-barrel-track-selection-task] processSelection : true")
            logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : false")
        if DQ_BARRELTINY_SELECTED == True:
            logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : true")
            logging.debug(" - [d-q-barrel-track-selection-task] processSelection : false")
            
        logging.debug(" - [d-q-muons-selection] processSelection : true")

    if DQ_EVENT_SELECTED == True and DQ_FULL_SELECTED == False:
        logging.debug(" - [d-q-event-selection-task] processEventSelection : true") 
    if DQ_EVENT_SELECTED == False and DQ_FULL_SELECTED == False:
        logging.debug(" - [d-q-event-selection-task] processEventSelection : false")                        
    if DQ_BARREL_SELECTED == True and DQ_FULL_SELECTED == False:           
        logging.debug(" - [d-q-barrel-track-selection-task] processSelection : true")
    if DQ_BARREL_SELECTED == False and DQ_FULL_SELECTED == False:           
        logging.debug(" - [d-q-barrel-track-selection-task] processSelection : false")                 
    if DQ_BARRELTINY_SELECTED == True and DQ_FULL_SELECTED == False:
        logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : true")
    if DQ_BARRELTINY_SELECTED == False and DQ_FULL_SELECTED == False:
        logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : false")                    
    if DQ_MUON_SELECTED  == True and DQ_FULL_SELECTED == False:
        logging.debug(" - [d-q-muons-selection] processSelection : true")
    if DQ_MUON_SELECTED  == False and DQ_FULL_SELECTED == False:
        logging.debug(" - [d-q-muons-selection] processSelection : false")         
    if DQ_FILTERPP_SELECTED == True:
        logging.debug(" - [d-q-filter-p-p-task-task] processFilterPP : true")
    if DQ_FILTERPP_SELECTED == False:
        logging.debug(" - [d-q-filter-p-p-task-task] processFilterPP : false")                  
    if DQ_FILTERPPTINY_SELECTED == True:
        logging.debug(" - [d-q-filter-p-p-task-task] processFilterPPTiny : true")
    if DQ_FILTERPPTINY_SELECTED == False:
        logging.debug(" - [d-q-filter-p-p-task-task] processFilterPPTiny : false")
    if DQ_QVECTOR_SELECTED == True:
        logging.debug(" - [analysis-qvector] processQvector : true") 
    if DQ_QVECTOR_SELECTED == False:
        logging.debug(" - [analysis-qvector] processQvector : false") 


# Transaction Management for process function in TableMaker/TableMakerMC Task

# set to List convert for tableMakerProcessSearch
tableMakerProcessSearch = list(tableMakerProcessSearch)
tempListProcess = []
validProcessListAfterDataMCFilter = []
try:
    for i in configuredCommands["process"]:
        tempListProcess.append(i)

    if extrargs.process:
        for j in tempListProcess:
            if j not in tableMakerProcessSearch:
                if extrargs.runData:
                    logging.warning("%s is Not valid Configurable Option for TableMaker regarding to Orginal JSON Config File!!! It will fix by CLI",j)
                    isValidProcessFunc  = False
                if extrargs.runMC:
                    logging.warning("%s is Not valid Configurable Option for TableMakerMC regarding to Orginal JSON Config File!!! It will fix by CLI",j)
                    isValidProcessFunc  = False
            if j in tableMakerProcessSearch:
                validProcessListAfterDataMCFilter.append(j)
    
    if isValidProcessFunc == False:
        logging.info("Valid processes are after MC/Data Filter: %s",validProcessListAfterDataMCFilter)

except:
    logging.warning("No process function provided in args, CLI Will not Check process validation for tableMaker/tableMakerMC process")
             
# Transaction Management for Most of Parameters for debugging, monitoring and logging
for key,value in configuredCommands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
        if key in v0SelectorParameters and extrargs.runMC:
            logging.warning("--%s Not Valid Parameter. V0 Selector parameters only valid for Data, not MC. It will fixed by CLI", key)
        if key == 'cfgWithQA' and extrargs.runMC:
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data, not MC. It will fixed by CLI", key)
        if key == 'est' and extrargs.runMC:
            logging.warning("--%s Not Valid Parameter. Centrality Table parameters only valid for Data, not MC. It will fixed by CLI", key)
        if key =='isFilterPPTiny' and extrargs.runMC:
            logging.warning("--%s Not Valid Parameter. Filter PP Tiny parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)
        if key == 'cfgMuonSels' and extrargs.runMC:
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data, not MC. It will fixed by CLI", key)
        if key == 'cfgBarrelSels' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data, not MC. It will fixed by CLI", key)
        if key == 'cfgMCsignals' and extrargs.runData:
            logging.warning("--%s Not Valid Parameter. This parameter only valid for MC, not Data. It will fixed by CLI", key)
                                         
# Centrality table delete for pp processes
if extrargs.process and len(centSearch) != 0 and (extrargs.syst == 'pp' or (extrargs.syst == None and config["event-selection-task"]["syst"] == "pp")):
    # delete centrality-table configurations for data. If it's MC don't delete from JSON
    # Firstly try for Data then if not data it gives warning message for MC
    noDeleteNeedForCent = False
    try:
        logging.warning("JSON file does not include configs for centrality-table task, It's for DATA. Centrality will removed because you select pp collision system.")
        #del(config["centrality-table"])
    except:
        if extrargs.runMC:
            logging.warning("JSON file does not include configs for centrality-table task, It's for MC. Centrality will removed because you select pp collision system.")
    # check for is TableMaker includes task related to Centrality?
    try:
        processCentralityMatch = [s for s in extrargs.process if "Cent" in s]
        if len(processCentralityMatch) > 0:
            logging.warning("Collision System pp can't be include related task about Centrality. They Will be removed in automation. Check your JSON configuration file for Tablemaker process function!!!")
            for paramValueTableMaker in processCentralityMatch:
                # Centrality process should be false
                if extrargs.runMC:
                    try:       
                        config["table-maker-m-c"][paramValueTableMaker] = 'false'
                    except:
                        logging.error("JSON config does not include table-maker-m-c, It's for Data. Misconfiguration JSON File!!!")
                        sys.exit()
                if extrargs.runData:
                    try:       
                        config["table-maker"][paramValueTableMaker] = 'false'
                    except:
                        logging.error("JSON config does not include table-maker, It's for MC. Misconfiguration JSON File!!!")
                        sys.exit()
    except:
        logging.warning("No process function provided so no need delete related to centrality-table dependency")
         
    # After deleting centrality we need to check if we have process function
    processLeftAfterCentDelete = True
    leftProcessAfterDeleteCent =[] 
    if extrargs.runData:
        for deletedParamTableMaker in config["table-maker"]:
            if "process" not in deletedParamTableMaker: 
                continue
            elif config["table-maker"].get(deletedParamTableMaker) == 'true':
                processLeftAfterCentDelete = True
                leftProcessAfterDeleteCent.append(deletedParamTableMaker)

    if extrargs.runMC:
        for deletedParamTableMaker in config["table-maker-m-c"]:
            if "process" not in deletedParamTableMaker: 
                continue
            elif config["table-maker-m-c"].get(deletedParamTableMaker) == 'true':
                processLeftAfterCentDelete = True
                leftProcessAfterDeleteCent.append(deletedParamTableMaker)

# logging Message for Centrality
if noDeleteNeedForCent == False: 
    logging.info("After deleting the process functions related to the centrality table (for collision system pp), the remaining processes: %s",leftProcessAfterDeleteCent)
 
if processLeftAfterCentDelete == False and noDeleteNeedForCent == False:
    logging.error("After deleting the process functions related to the centrality table, there are no functions left to process, misconfigure for process!!!")    
    sys.exit()    
    
  
# ================================================================    
# Transcation Management for barrelsels and muonsels in filterPP 
# ================================================================

for key,value in configuredCommands.items():
    if(value != None):
        #if type(value) == type(clist):
            #listToString(value)
        if key == 'cfgMuonsCuts':
            muonCutList.append(value)
        if key == 'cfgBarrelTrackCuts':
            barrelTrackCutList.append(value)
        if key == 'cfgBarrelSels':
            barrelSelsList.append(value)
        if key == 'cfgMuonSels':
            muonSelsList.append(value)

##############################
# For MuonSels From FilterPP #
##############################
if extrargs.cfgMuonSels:
    
    # transcation management
    if extrargs.cfgMuonsCuts == None:
        logging.error("For configure to cfgMuonSels (For DQ Filter PP Task), you must also configure cfgMuonsCuts!!!")
        sys.exit()
        
    # Convert List Muon Cuts                     
    for muonCut in muonCutList:
        muonCut = stringToList(muonCut)

    # seperate string values to list with comma
    for muonSels in muonSelsList:
        muonSels = muonSels.split(",")    

    # remove string values after :
    for i in muonSels:
        i = i[ 0 : i.index(":")]
        muonSelsListAfterSplit.append(i)

    # Remove duplicated values with set convertion
    muonSelsListAfterSplit = set(muonSelsListAfterSplit)
    muonSelsListAfterSplit = list(muonSelsListAfterSplit)

    for i in muonSelsListAfterSplit:
        if i in muonCut:
            continue
        else:
            print("====================================================================================================================")
            logging.error("--cfgMuonSels <value>: %s not in --cfgMuonsCuts %s ",i, muonCut)
            logging.info("For fixing this issue, you should have the same number of cuts (and in the same order) provided to the cfgMuonsCuts from dq-selection as those provided to the cfgMuonSels in the DQFilterPPTask.") 
            print("For example, if cfgMuonCuts is muonLowPt,muonHighPt, then the cfgMuonSels has to be something like: muonLowPt::1,muonHighPt::1,muonLowPt:pairNoCut:1")  
            sys.exit()
                            
    for i in muonCut:    
        if i in muonSelsListAfterSplit:
            continue
        else:
            print("====================================================================================================================")
            logging.error("--cfgMuonsCut <value>: %s not in --cfgMuonSels %s ",i,muonSelsListAfterSplit)
            logging.info("[INFO] For fixing this issue, you should have the same number of cuts (and in the same order) provided to the cfgMuonsCuts from dq-selection as those provided to the cfgMuonSels in the DQFilterPPTask.") 
            print("For example, if cfgMuonCuts is muonLowPt,muonHighPt, then the cfgMuonSels has to be something like: muonLowPt::1,muonHighPt::1,muonLowPt:pairNoCut:1")  
            sys.exit()
            
################################
# For BarrelSels from FilterPP # 
################################
if extrargs.cfgBarrelSels:
    
    # transcation management
    if extrargs.cfgBarrelTrackCuts == None:
        logging.error("For configure to cfgBarrelSels (For DQ Filter PP Task), you must also configure cfgBarrelTrackCuts!!!")
        sys.exit()
         
    # Convert List Barrel Track Cuts                     
    for barrelTrackCut in barrelTrackCutList:
        barrelTrackCut = stringToList(barrelTrackCut)

    # seperate string values to list with comma
    for barrelSels in barrelSelsList:
        barrelSels = barrelSels.split(",")   

    # remove string values after :
    for i in barrelSels:
        i = i[ 0 : i.index(":")]
        barrelSelsListAfterSplit.append(i)

    # Remove duplicated values with set convertion
    barrelSelsListAfterSplit = set(barrelSelsListAfterSplit)
    barrelSelsListAfterSplit = list(barrelSelsListAfterSplit)

    for i in barrelSelsListAfterSplit:
        if i in barrelTrackCut:
            continue
        else:
            print("====================================================================================================================")
            logging.error("--cfgBarrelTrackCuts <value>: %s not in --cfgBarrelSels %s",i,barrelTrackCut)
            logging.info("For fixing this issue, you should have the same number of cuts (and in the same order) provided to the cfgBarrelTrackCuts from dq-selection as those provided to the cfgBarrelSels in the DQFilterPPTask.")  
            print("For example, if cfgBarrelTrackCuts is jpsiO2MCdebugCuts,jpsiO2MCdebugCuts2, then the cfgBarrelSels has to be something like: jpsiO2MCdebugCuts::1,jpsiO2MCdebugCuts2::1,jpsiO2MCdebugCuts:pairNoCut:1") 
            sys.exit()
                            
    for i in barrelTrackCut:    
        if i in barrelSelsListAfterSplit:
            continue
        else:
            print("====================================================================================================================")
            logging.error("--cfgBarrelTrackCuts <value>: %s not in --cfgBarrelSels %s",i,barrelSelsListAfterSplit)
            logging.info("For fixing this issue, you should have the same number of cuts (and in the same order) provided to the cfgBarrelTrackCuts from dq-selection as those provided to the cfgBarrelSels in the DQFilterPPTask.") 
            print("For example, if cfgBarrelTrackCuts is jpsiO2MCdebugCuts,jpsiO2MCdebugCuts2, then the cfgBarrelSels has to be something like: jpsiO2MCdebugCuts::1,jpsiO2MCdebugCuts2::1,jpsiO2MCdebugCuts:pairNoCut:1")      
            sys.exit()
            
# AOD File Checker 
if extrargs.aod != None:
    myAod =  extrargs.aod
    textAodList = myAod.startswith("@")
    aodRootFile = myAod.endswith(".root")
    textControl = myAod.endswith("txt") or myAod.endswith("text") 
    if textAodList == True and textControl == True:
        myAod = myAod.replace("@","")
        logging.info("You provided AO2D list as text file : %s",myAod)
        if os.path.isfile(myAod) == False:
            logging.error("%s File not found in path!!!", myAod)
            sys.exit()
        else:
            logging.info("%s has valid File Format and Path, File Found", myAod)
         
    elif aodRootFile == True:
        logging.info("You provided single AO2D as root file  : %s",myAod)
        if os.path.isfile(myAod) == False:
            logging.error("%s File not found in path!!!", myAod)
            sys.exit()
        else:
            logging.info("%s has valid File Format and Path, File Found", myAod)                
    else:
        logging.error("%s Wrong formatted File, check your file!!!", myAod)
        sys.exit()     
        
#####################
# Deps Transcations #
#####################

# In extended tracks, o2-analysis-trackextension is not a valid dep for run 3
# More Information : https://aliceo2group.github.io/analysis-framework/docs/helperTasks/trackselection.html?highlight=some%20of%20the%20track%20parameters
"""
Some of the track parameters used in the track selection require additional calculation effort and are then stored in a table called TracksExtended 
which is produced by either the o2-analysis-trackextension task (Run 2) or o2-analysis-track-propagation (Run 3). 
The quantities contained in this table can also be directly used in the analysis.
"""
if config["bc-selection-task"]["processRun3"] == "true":
    barrelDeps.remove("o2-analysis-trackextension")
    logging.info("o2-analysis-trackextension is not valid dep for run 3, It will deleted from your workflow.")

                 
###########################
# End Interface Processes #
###########################

# Write the updated configuration file into a temporary file
updatedConfigFileName = "tempConfigTableMaker.json"
    
with open(updatedConfigFileName,'w') as outputFile:
  json.dump(config, outputFile ,indent=2)

# Check which dependencies need to be run  
depsToRun = {}
for dep in commonDeps:
  depsToRun[dep] = 1

for processFunc in specificDeps.keys():
  if not processFunc in config[taskNameInConfig].keys():
    continue        
  if config[taskNameInConfig][processFunc] == "true":      
    if "processFull" in processFunc or "processBarrel" in processFunc:
      for dep in barrelDeps:
        depsToRun[dep] = 1
    for dep in specificDeps[processFunc]:
      depsToRun[dep] = 1

# Check which tables are required in the output
tablesToProduce = {}
for table in commonTables:
  tablesToProduce[table] = 1

if runOverMC == True:
  tablesToProduce["ReducedMCEvents"] = 1
  tablesToProduce["ReducedMCEventLabels"] = 1
  
for processFunc in specificDeps.keys():
  if not processFunc in config[taskNameInConfig].keys():
    continue          
  if config[taskNameInConfig][processFunc] == "true":
    logging.info("processFunc ========")
    logging.info("%s", processFunc)
    if "processFull" in processFunc or "processBarrel" in processFunc:
      logging.info("common barrel tables==========")      
      for table in barrelCommonTables:
        logging.info("%s", table)      
        tablesToProduce[table] = 1
      if runOverMC == True:
        tablesToProduce["ReducedTracksBarrelLabels"] = 1
    if "processFull" in processFunc or "processMuon" in processFunc:
      logging.info("common muon tables==========")      
      for table in muonCommonTables:
        logging.info("%s", table)
        tablesToProduce[table] = 1
      if runOverMC == True:
        tablesToProduce["ReducedMuonsLabels"] = 1  
    if runOverMC == True:
      tablesToProduce["ReducedMCTracks"] = 1
    logging.info("specific tables==========")      
    for table in specificTables[processFunc]:
      logging.info("%s", table)      
      tablesToProduce[table] = 1

# Generate the aod-writer output descriptor json file
writerConfig = {}
writerConfig["OutputDirector"] = {
  "debugmode": True,
  "resfile": "reducedAod",
  "resfilemode": "RECREATE",
  "ntfmerge": 1,
  "OutputDescriptors": []
}

# Generate the aod-reader output descriptor json file
readerConfig = {}
readerConfig["InputDirector"] = {
    "debugmode": True,
    "InputDescriptors": []
}

iTable = 0
for table in tablesToProduce.keys():
  writerConfig["OutputDirector"]["OutputDescriptors"].insert(iTable, tables[table])
  readerConfig["InputDirector"]["InputDescriptors"].insert(iTable, tables[table])
  iTable += 1
  
writerConfigFileName = "aodWriterTempConfig.json"
with open(writerConfigFileName,'w') as writerConfigFile:
  json.dump(writerConfig, writerConfigFile, indent=2)
  
  
readerConfigFileName = "aodReaderTempConfig.json"
with open(readerConfigFileName,'w') as readerConfigFile:
  json.dump(readerConfig, readerConfigFile, indent=2)
  
logging.info("aodWriterTempConfig==========")  
print(writerConfig)
#sys.exit()
logging.info("aodReaderTempConfig==========")  
print(readerConfig)
      
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --severity error --shm-segment-size 12000000000 --aod-writer-json " + writerConfigFileName + " -b"
if extrargs.aod_memory_rate_limit:
    commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --severity error --shm-segment-size 12000000000 --aod-memory-rate-limit " + extrargs.aod_memory_rate_limit + " --aod-writer-json " + writerConfigFileName + " -b"
    
for dep in depsToRun.keys():
  commandToRun += " | " + dep + " --configuration json://" + updatedConfigFileName + " -b"
  logging.debug("%s added your workflow",dep)

if extrargs.add_mc_conv:
    logging.debug("o2-analysis-mc-converter added your workflow")
    commandToRun += " | o2-analysis-mc-converter --configuration json://" + updatedConfigFileName + " -b"

if extrargs.add_fdd_conv:
    commandToRun += " | o2-analysis-fdd-converter --configuration json://" + updatedConfigFileName + " -b"
    logging.debug("o2-analysis-fdd-converter added your workflow")

if extrargs.add_track_prop:
    commandToRun += " | o2-analysis-track-propagation --configuration json://" + updatedConfigFileName + " -b"
    logging.debug("o2-analysis-track-propagation added your workflow")

print("====================================================================================================================")
logging.info("Command to run:")
logging.info(commandToRun)
print("====================================================================================================================")
logging.info("Tables to produce:")
logging.info(tablesToProduce.keys())
print("====================================================================================================================")
#sys.exit()

# Listing Added Commands
logging.info("Args provided configurations List")
print("====================================================================================================================")
for key,value in configuredCommands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
        logging.info("--%s : %s ",key,value)

os.system(commandToRun)