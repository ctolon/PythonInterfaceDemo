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

import json
import sys
import logging
from ast import parse
import os
import argparse
import re
import urllib.request

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

#################################
# JSON Database Read and Upload #
#################################
"""
Predefined Analysis Cuts, MCSignals and Histograms From O2-DQ Framework.
MCSignals --> https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/MCSignalLibrary.h
Analysis Cuts --> https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/CutsLibrary.h

Parameters
------------------------------------------------
analysisCutDatabaseJSON: JSON
    analysisCutDatabaseJSON is a JSON file for take the analysis cut parameters
    
analysisCutDatabase : list
    analysisCutDatabase is a List for take analysis cut parameters from JSON database

MCSignalDatabaseJSON: JSON
    MCSignalDatabaseJSON is a JSON file for take the MC signals parameters
    
MCSignalDatabase: list
    MCSignalDatabase is a List for take MC Signals from JSON database

analysisCutDatabaseJSON = json.load(open('Database/AnalysisCutDatabase.json'))
MCSignalDatabaseJSON = json.load(open('Database/MCSignalDatabase.json'))
analysisCutDatabase = []
MCSignalDatabase =[]

# control list for type control
clist=[]

# Cut Database
for key, value in analysisCutDatabaseJSON.items():
    analysisCutDatabase.append(value)

# MCSignal Database
for key, value in MCSignalDatabaseJSON.items():
    MCSignalDatabase.append(value)

"""    

"""
ListToString provides converts lists to strings.
This function is written to save as string type instead of list 
when configuring JSON values for multiple selection in CLI.

Parameters
------------------------------------------------
s: list
A simple Python List
"""
def listToString(s):
    if len(s) > 1:
        # initialize an empty string
        str1 =","
   
        # return string 
        return (str1.join(s))
    else:
        str1 = " "
        
        return (str1.join(s))

# defination for binary check #TODO Need to be integrated
"""
def binary_selector(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1') or v.upper() in (('YES', 'TRUE', 'T', 'Y', '1')):
        return "true"
        #return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0','-1') or v.upper() in ('NO', 'FALSE', 'F', 'N', '0','-1'):
        return "false"
        #return False
    else:
        raise argparse.ArgumentTypeError('Misstyped value!')
"""
    
def stringToList(string):
    li = list(string.split(" "))
    return li

# Github Links for CutsLibrary and MCSignalsLibrary from PWG-DQ --> download from github
# This condition solves performance issues
if (os.path.isfile('tempCutsLibrary.h') == False) or (os.path.isfile('tempMCSignalsLibrary.h') == False):
    urlCutsLibrary = 'https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/CutsLibrary.h'
    urlMCSignalsLibrary ='https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/MCSignalLibrary.h'

    urllib.request.urlretrieve(urlCutsLibrary,"tempCutsLibrary.h")
    urllib.request.urlretrieve(urlMCSignalsLibrary,"tempMCSignalsLibrary.h")

clist=[] # control list for type control
allValuesCfg = [] # counter for provided args
allCuts = [] # all analysis cuts
allMCSignals =[] # all MC Signals
allPairCuts = [] # only pair cuts
nAddedAllCutsList = [] # e.g. muonQualityCuts::2
nAddedPairCutsList = [] # e.g paircutMass::3
SelsStyle1  = [] # track/muon cut::paircut::n
allSels = [] # track/muon cut::n
namespaceDef = ":" # Namespace reference
namespaceDef2 = "::" # Namespace reference


# Get paths in localy
#MCSignalsPath = os.path.expanduser("~/alice/O2Physics/PWGDQ/Core/MCSignalLibrary.h")
#AnalysisCutsPath = os.path.expanduser("~/alice/O2Physics/PWGDQ/Core/CutsLibrary.h")
#print(os.environ['ALIBUILD_WORK_DIR'])

# Get system variables in alienv.#TODO:In alienv we don't have cuts and signal library!!! We need discuss this thing

O2DPG_ROOT=os.environ.get('O2DPG_ROOT')
QUALITYCONTROL_ROOT=os.environ.get('QUALITYCONTROL_ROOT')
O2_ROOT=os.environ.get('O2_ROOT')
O2PHYSICS_ROOT=os.environ.get('O2PHYSICS_ROOT')


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
                namespacedPairCuts = [x + namespaceDef for x in allPairCuts] # paircut:
            allCuts = allCuts + getAnalysisCuts # Get all Cuts from CutsLibrary.h
            nameSpacedAllCuts = [x + namespaceDef for x in allCuts] # cut:
            nameSpacedAllCutsTwoDots = [x + namespaceDef2 for x in allCuts]  # cut::

"""
with open(MCSignalsPath) as f:
    for line in f:
        stringIfSearch = [x for x in f if 'if' in x] 
        for i in stringIfSearch:
            getSignals = re.findall('"([^"]*)"', i)
            allMCSignals = allMCSignals + getSignals
            
with open(AnalysisCutsPath) as f:
    for line in f:
        stringIfSearch = [x for x in f if 'if' in x]  # get lines only includes if string
        for i in stringIfSearch:
            getAnalysisCuts = re.findall('"([^"]*)"', i)  # get in double quotes string value with regex exp.
            getPairCuts = [y for y in getAnalysisCuts         # get pair cuts
                        if 'pair' in y] 
            if getPairCuts: # if pair cut list is not empty
                allPairCuts = allPairCuts + getPairCuts # Get Only pair cuts from CutsLibrary.h
                namespacedPairCuts = [x + namespaceDef for x in allPairCuts] # paircut:
            allCuts = allCuts + getAnalysisCuts # Get all Cuts from CutsLibrary.h
            nameSpacedAllCuts = [x + namespaceDef for x in allCuts] # cut:
            nameSpacedAllCutsTwoDots = [x + namespaceDef2 for x in allCuts]  # cut::
"""

# in Filter PP Task, sels options for barrel and muon uses namespaces e.g. "<track-cut>:[<pair-cut>]:<n> and <track-cut>::<n> For Manage this issue:
for k in range (1,10):
    nAddedAllCuts = [x + str(k) for x in nameSpacedAllCutsTwoDots]
    nAddedAllCutsList = nAddedAllCutsList + nAddedAllCuts
    nAddedPairCuts = [x + str(k) for x in namespacedPairCuts]
    nAddedPairCutsList = nAddedPairCutsList + nAddedPairCuts
    
# Style 1 <track-cut>:[<pair-cut>]:<n>:
for i in nAddedPairCutsList:
    Style1 = [x + i for x in nameSpacedAllCuts]
    SelsStyle1 = SelsStyle1 + Style1
      
# Style 2 <track-cut>:<n> --> nAddedAllCutsList

# Merge All possible styles for Sels (cfgBarrelSels and cfgMuonSels) in FilterPP Task
allSels = SelsStyle1 + nAddedAllCutsList


# Debug Print Options

#print(allCuts)
#print(allPairCuts)
#print(allMCSignals)
#print(allPairCuts)
#print(namespacedPairCuts)
#print(nameSpacedAllCuts)
#print(nAddedAllCutsList)
#print(nAddedPairCutsList)
#print(SelsStyle1)
#print(nAddedAllCutsList)
#print(allSels)
    
###################################
# Interface Predefined Selections #
###################################
   

tablemakerProcessAllSelections = ["Full","FullTiny","FullWithCov","FullWithCent",
        "BarrelOnlyWithV0Bits","BarrelOnlyWithEventFilter","BarrelOnlyWithCent","BarrelOnlyWithCov","BarrelOnly",
        "MuonOnlyWithCent","MuonOnlyWithCov","MuonOnly","MuonOnlyWithFilter",
        "OnlyBCs"]

tablemakerProcessAllParameters = ["processFull","processFullTiny","processFullWithCov","processFullWithCent",
        "processBarrelOnlyWithV0Bits","processBarrelOnlyWithEventFilter","processBarrelOnlyWithCent","processBarrelOnlyWithCov","processBarrelOnly",
        "processMuonOnlyWithCent","processMuonOnlyWithCov","processMuonOnly","processMuonOnlyWithFilter",
        "processOnlyBCs"]

centralityTableSelections = ["V0M", "Run2SPDtks","Run2SPDcls","Run2CL0","Run2CL1"]
centralityTableParameters = ["estV0M", "estRun2SPDtks","estRun2SPDcls","estRun2CL0","estRun2CL1"]

V0Parameters = ["d_bz","v0cospa","dcav0dau","v0RMin","v0Rmax","dcamin","dcamax,mincrossedrows","maxchi2tpc"]

PIDSelections = ["el","mu","pi","ka","pr","de","tr","he","al"]
PIDParameters = ["pid-el","pid-mu","pid-pi","pid-ka","pid-pr","pid-de","pid-tr","pid-he","pid-al"]

processDummySelections =["filter","event","barrel"]

noDeleteNeedForCent = True
processLeftAfterCentDelete = True


###################
# Main Parameters #
###################

parser = argparse.ArgumentParser(description='Arguments to pass')
parser.add_argument('cfgFileName', metavar='text', default='config.json', help='config file name')
parser.add_argument('-runData', help="Run over data", action="store_true")
parser.add_argument('-runMC', help="Run over MC", action="store_true")
#parser.add_argument('analysisString', metavar='text', help='my analysis string', required=False) # optional interface
parser.add_argument('--add_mc_conv', help="Add the converter from mcparticle to mcparticle+001", action="store_true")
parser.add_argument('--add_fdd_conv', help="Add the fdd converter", action="store_true")
parser.add_argument('--add_track_prop', help="Add track propagation to the innermost layer (TPC or ITS)", action="store_true")

#coreArgs = ["cfgFileName","runData","runMC","add_mc_conv","add_fdd_conv","add_track_prop"]

########################
# Interface Parameters #
########################


# aod
parser.add_argument('--aod', help="Add your AOD File with path", action="store", type=str)

# json output
#parser.add_argument('--outputjson', help="Your Output JSON Config Fİle", action="store", type=str)

# only select
parser.add_argument('--onlySelect', help="An Automate parameter for keep options for only selection in process, pid and centrality table (true is highly recomended for automation)", action="store",choices=["true","false"], default="true", type=str.lower)

# table-maker cfg
parser.add_argument('--cfgEventCuts', help="Space separated list of event cuts", choices=allCuts, nargs='*', action="store", type=str, metavar='')
parser.add_argument('--cfgBarrelTrackCuts', help="Space separated list of barrel track cuts", choices=allCuts,nargs='*', action="store", type=str, metavar='')
parser.add_argument('--cfgMuonCuts', help="Space separated list of muon cuts in table-maker", action="store", choices=allCuts, nargs='*', type=str, metavar='')
parser.add_argument('--cfgBarrelLowPt', help="Low pt cut for tracks in the barrel", action="store", type=str)
parser.add_argument('--cfgMuonLowPt', help="Low pt cut for muons", action="store", type=str)
parser.add_argument('--cfgNoQA', help="If true, no QA histograms", action="store", choices=["true","false"], type=str.lower)
parser.add_argument('--cfgDetailedQA', help="If true, include more QA histograms (BeforeCuts classes and more)", action="store", choices=["true","false"], type=str.lower)
#parser.add_argument('--cfgIsRun2', help="Run selection true or false", action="store", choices=["true","false"], type=str) # no need
parser.add_argument('--cfgMinTpcSignal', help="Minimum TPC signal", action="store", type=str)
parser.add_argument('--cfgMaxTpcSignal', help="Maximum TPC signal", action="store", type=str)
parser.add_argument('--cfgMCsignals', help="Space separated list of MC signals", action="store",choices=allMCSignals, nargs='*', type=str, metavar='')

# table-maker process
parser.add_argument('--process', help="Process Selection options for TableMaker Data Processing and Skimming", action="store", choices=tablemakerProcessAllSelections, nargs='*', type=str)

# Run Selection : event-selection-task ,bc-selection-task, multiplicity-table, track-extension no refactor
parser.add_argument('--run', help="Run Selection (2 or 3)", action="store", choices=['2','3'], type=str)
#parser.add_argument('--processRun2', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) # no need
#parser.add_argument('--processRun3', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) # no need

# event-selection-task
parser.add_argument('--syst', help="Collision System Selection ex. pp", action="store", choices=["PbPb", "pp", "pPb", "Pbp", "XeXe"], type=str)
parser.add_argument('--muonSelection', help="0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts",choices=["0","1","2"], action="store", type=str)
parser.add_argument('--customDeltaBC', help="custom BC delta for FIT-collision matching", action="store", type=str)
#parser.add_argument('--isMC', help="Is it Monte Carlo options true or false", action="store", choices=["true","false"],default="false", type=str, required=True) # no need

# track-propagation
parser.add_argument('--isCovariance', help="track-propagation : If false, Process without covariance, If true Process with covariance", action="store", choices=['true','false'], type=str.lower)
#parser.add_argument('--processStandard', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str.lower)
#parser.add_argument('--processCovariance', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str.lower)

# tof-pid-full, tof-pid for run3 ???
parser.add_argument('--isProcessEvTime', help="tof-pid -> processEvTime : Process Selection options true or false (string)", action="store", choices=['true','false'], type=str.lower)
#parser.add_argument('--processEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #no need
#parser.add_argument('--processNoEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)#no need

#tof-pid-beta
parser.add_argument('--tof-expreso', help="Expected resolution for the computation of the expected beta", action="store", type=str)

#parser.add_argument('--processSelection', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #d-q barrel and d-q muon selection no need automatic with process tablemaker
#parser.add_argument('--processSelectionTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #only d-q barrel no need automatic with process tablemaker

# dummies
parser.add_argument('--processDummy', help="Dummy function (No need If autoDummy is true)", action="store", choices=processDummySelections, nargs='*', type=str.lower) #event selection, barel track task, filter task
parser.add_argument('--autoDummy', help="Dummy automize parameter (if your selection true, it automatically activate dummy process and viceversa)", action="store", choices=["true","false"], default='true', type=str.lower) #event selection, barel track task, filter task

# d-q-track barrel-task
parser.add_argument('--isBarrelSelectionTiny', help="Run barrel track selection instead of normal(process func. for barrel selection must be true)", action="store", choices=['true','false'], default='false', type=str.lower) #d-q barrel and d-q muon selection
# d-q event selection task
parser.add_argument('--cfgMuonsCuts', help="Space separated list of muon cuts in d-q muons selection", action="store", choices=allCuts, nargs='*', type=str, metavar='')

# d-q-filter-p-p-task
parser.add_argument('--cfgPairCuts', help="Space separated list of pair cuts", action="store", choices=allPairCuts, nargs='*', type=str, metavar='') # run3
parser.add_argument('--cfgBarrelSels', help="Configure Barrel Selection <track-cut>:[<pair-cut>]:<n>,[<track-cut>:[<pair-cut>]:<n>],... | example jpsiO2MCdebugCuts2::1 ",choices=allSels, action="store", type=str, metavar='') # run2 
parser.add_argument('--cfgMuonSels', help="Configure Muon Selection <muon-cut>:[<pair-cut>]:<n> example muonQualityCuts:pairNoCut:1",choices=allSels, action="store", type=str, metavar='') # run 2
parser.add_argument('--isFilterPPTiny', help="Run filter tiny task instead of normal (processFilterPP must be true) ", action="store", choices=['true','false'], type=str.lower)
#parser.add_argument('--processFilterPP', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3 no need
#parser.add_argument('--processFilterPPTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3 no need

# centrality-table
parser.add_argument('--est', help="Produces centrality percentiles parameters", action="store", choices=centralityTableSelections,nargs="*", type=str)

# timestamp-task
#parser.add_argument('--isRun2MC', help="Selection the Process is MC or Not", action="store", choices=['true','false'], type=str)

# track-selection
#parser.add_argument('--isRun3', help="Add track propagation to the innermost layer (TPC or ITS)", action="store", choices=['true','false'], type=str)

#all d-q tasks and selections
parser.add_argument('--cfgWithQA', help="If true, fill QA histograms", action="store", choices=['true','false'], type=str.lower)

# v0-selector
parser.add_argument('--d_bz', help="bz field", action="store", type=str)
parser.add_argument('--v0cospa', help="v0cospa", action="store", type=str)
parser.add_argument('--dcav0dau', help="DCA V0 Daughters", action="store", type=str)
parser.add_argument('--v0Rmin', help="v0Rmin", action="store", type=str)
parser.add_argument('--v0Rmax', help="v0Rmax", action="store", type=str)
parser.add_argument('--dcamin', help="dcamin", action="store", type=str)
parser.add_argument('--dcamax', help="dcamax", action="store", type=str)
parser.add_argument('--mincrossedrows', help="Min crossed rows", action="store", type=str)
parser.add_argument('--maxchi2tpc', help="max chi2/NclsTPC", action="store", type=str)

# pid
parser.add_argument('--pid', help="Produce PID information for the particle mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)", action="store", choices=PIDSelections, nargs='*', type=str.lower)

# helper lister commands
parser.add_argument('--cutLister', help="List all of the analysis cuts from CutsLibrary.h", action="store_true")
parser.add_argument('--MCSignalsLister', help="List all of the MCSignals from MCSignalLibrary.h", action="store_true")

argcomplete.autocomplete(parser)
extrargs = parser.parse_args()

configuredCommands = vars(extrargs) # for get extrargs

#####################################################
# Selection Parameters for run number and data type #
#####################################################

# Selection Options for Run<Data|MC> Run<2|3> #TODO  Integrate them over extrags checks
"""
run2Selected = False
run3Selected = False
MCSelected = False
dataSelected = False

run2MCSelected = False
run2DataSelected = False
run3MCSelected = False
run3DataSelected = False

if extrargs.run == '2':
    run2Selected = True
if extrargs.run == 3:
    run3Selected = True
if extrargs.runMC:
    MCSelected = True
if extrargs.runData:
    dataSelected = True

if extrargs.run == '2' and extrargs.runMC:
    run2MCSelected = True
if extrargs.run == '2' and extrargs.runData:
    run2DataSelected = True
if extrargs.run == '3' and extrargs.runMC:
    run3MCSelected = True
if extrargs.run == '3' and extrargs.runData:
    run3DataSelected = True
    
"""

###################
# HELPER MESSAGES #
###################

#TODO: Provide a Table format for print option       
if extrargs.cutLister and extrargs.MCSignalsLister:
    counter = 0
    print("====================")
    print("Analysis Cut Options :")
    print("====================")
    for i in allCuts:   
        print(i,end="\t")
        counter += 1
        if counter == 5:
            print("\n")
            counter = 0
        
    print("\n====================\nMC Signals :")
    print("====================")
    counter = 0
    for i in allMCSignals:
        print(i,end="\t")
        counter += 1
        if counter == 5:
            print("\n")
            counter = 0
    print("\n")
    sys.exit()
if extrargs.cutLister:
    """
    print("  {: >20} {: >20} {: >20}".format(*allCuts))
    #for row in allCuts:
    #for i in range(len(allCuts)):
        #print(" {: >20} {: >20} {: >20}".format(*allCuts[i]))
        #print(type(format(*row)))
    """
    counter = 0
    print("Analysis Cut Options :")
    print("====================")
    for i in allCuts:   
        print(i,end="\t")
        counter += 1
        if counter == 5:
            print("\n")
            counter = 0
    print("\n")
    sys.exit()
    
if extrargs.MCSignalsLister:
    counter = 0
    print("MC Signals :")
    print("====================")
    for i in allMCSignals:   
        print(i,end="\t")
        counter += 1
        if counter == 5:
            print("\n")
            counter = 0
    print("\n")
    sys.exit()

######################
# PREFIX ADDING PART #
###################### 

# add prefix for extrargs.process for TableMaker and Filter PP
if extrargs.process != None:
    prefix_process = "process"
    extrargs.process = [prefix_process + sub for sub in extrargs.process]

# add prefix for extrargs.pid for pid selection
if extrargs.pid != None:
    prefix_pid = "pid-"
    extrargs.pid = [prefix_pid + sub for sub in extrargs.pid]
    
# add prefix for extrargs.est for centrality table
if extrargs.est != None:
    prefix_est = "est"
    extrargs.est = [prefix_est + sub for sub in extrargs.est]
    
######################################################################################

commonDeps = ["o2-analysis-timestamp", "o2-analysis-event-selection", "o2-analysis-multiplicity-table"]
barrelDeps = ["o2-analysis-trackselection", "o2-analysis-trackextension","o2-analysis-pid-tof-base", "o2-analysis-pid-tof", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]
specificDeps = {
  "processFull" : [],
  "processFullTiny" : [],
  "processFullWithCov" : [],
  "processFullWithCent" : ["o2-analysis-centrality-table"],
  "processBarrelOnly" : [],
  "processBarrelOnlyWithCov" : [],
  "processBarrelOnlyWithV0Bits" : ["o2-analysis-dq-v0-selector", "o2-analysis-weak-decay-indices"],
  "processBarrelOnlyWithEventFilter" : ["o2-analysis-dq-filter-pp"],
  "processBarrelOnlyWithCent" : ["o2-analysis-centrality-table"],
  "processMuonOnly" : [],
  "processMuonOnlyWithCov" : [],
  "processMuonOnlyWithCent" : ["o2-analysis-centrality-table"],
  "processMuonOnlyWithFilter" : ["o2-analysis-dq-filter-pp"]
  #"processFullWithCentWithV0Bits" : ["o2-analysis-centrality-table","o2-analysis-dq-v0-selector", "o2-analysis-weak-decay-indices"],
  #"processFullWithEventFilterWithV0Bits" : ["o2-analysis-dq-filter-pp","o2-analysis-dq-v0-selector", "o2-analysis-weak-decay-indices"],
} 

# Definition of all the tables we may write
tables = {
  "ReducedEvents" : {"table": "AOD/REDUCEDEVENT/0", "treename": "ReducedEvents"},
  "ReducedEventsExtended" : {"table": "AOD/REEXTENDED/0", "treename": "ReducedEventsExtended"},
  "ReducedEventsVtxCov" : {"table": "AOD/REVTXCOV/0", "treename": "ReducedEventsVtxCov"},
  "ReducedMCEventLabels" : {"table": "AOD/REMCCOLLBL/0", "treename": "ReducedMCEventLabels"},
  "ReducedMCEvents" : {"table": "AOD/REMC/0", "treename": "ReducedMCEvents"},
  "ReducedTracks" : {"table": "AOD/REDUCEDTRACK/0", "treename": "ReducedTracks"},
  "ReducedTracksBarrel" : {"table": "AOD/RTBARREL/0", "treename": "ReducedTracksBarrel"},
  "ReducedTracksBarrelCov" : {"table": "AOD/RTBARRELCOV/0", "treename": "ReducedTracksBarrelCov"},
  "ReducedTracksBarrelPID" : {"table": "AOD/RTBARRELPID/0", "treename": "ReducedTracksBarrelPID"},
  "ReducedTracksBarrelLabels" : {"table": "AOD/RTBARRELLABELS/0", "treename": "ReducedTracksBarrelLabels"},
  "ReducedMCTracks" : {"table": "AOD/RTMC/0", "treename": "ReducedMCTracks"},
  "ReducedMuons" : {"table": "AOD/RTMUON/0", "treename": "ReducedMuons"},
  "ReducedMuonsExtra" : {"table": "AOD/RTMUONEXTRA/0", "treename": "ReducedMuonsExtra"},
  "ReducedMuonsCov" : {"table": "AOD/RTMUONCOV/0", "treename": "ReducedMuonsCov"},
  "ReducedMuonsLabels" : {"table": "AOD/RTMUONSLABELS/0", "treename": "ReducedMuonsLabels"}
}
# Tables to be written, per process function
commonTables = ["ReducedEvents", "ReducedEventsExtended", "ReducedEventsVtxCov"]
barrelCommonTables = ["ReducedTracks","ReducedTracksBarrel","ReducedTracksBarrelPID"]
muonCommonTables = ["ReducedMuons", "ReducedMuonsExtra"]
specificTables = {
  "processFull" : [],
  "processFullTiny" : [],
  "processFullWithCov" : ["ReducedTracksBarrelCov", "ReducedMuonsCov"],
  "processFullWithCent" : [],
  "processBarrelOnly" : [],
  "processBarrelOnlyWithCov" : ["ReducedTracksBarrelCov"],
  "processBarrelOnlyWithV0Bits" : [],
  "processBarrelOnlyWithEventFilter" : [],
  "processBarrelOnlyWithCent" : [],
  "processMuonOnly" : [],
  "processMuonOnlyWithCov" : ["ReducedMuonsCov"],
  "processMuonOnlyWithCent" : [],
  "processMuonOnlyWithFilter" : []
}

# Make some checks on provided arguments
if len(sys.argv) < 3:
  print("ERROR: Invalid syntax! The command line should look like this:")
  print("  ./IRunTableMaker.py <yourConfig.json> <runData|runMC> --run <2|3> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
config = {}
#cfgFileName = 'configTableMakerDataRun3.json'
with open(extrargs.cfgFileName) as configFile:
  config = json.load(configFile)

# Check whether we run over data or MC
if not (extrargs.runMC or extrargs.runData):
  print("ERROR: You have to specify either runMC or runData !")
  sys.exit()
  
# Check whether we run over run 2 or run 3
if not (extrargs.run == '3' or extrargs.run == '2'):
  print("ERROR: You have to specify either --run 3 or --run 2 !")
  sys.exit()

runOverMC = False
if (extrargs.runMC):
  runOverMC = True

print("runOverMC ",runOverMC)

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
            pass
    except:
        print("[ERROR] JSON config does not include table-maker-m-c, It's for Data. Misconfiguration JSON File!!!")
        sys.exit()
if extrargs.runData:
    try:
        if config["table-maker"]:
            pass
    except:
        print("[ERROR] JSON config does not include table-maker, It's for MC. Misconfiguration JSON File!!!")
        sys.exit()
        
# Check alienv
if O2PHYSICS_ROOT == None:
   print("[ERROR] You must load O2Physics with alienv")
   sys.exit()
 
           
#############################
# Start Interface Processes #
#############################

# For adding a process function from TableMaker and all process should be added only once so set type used
tableMakerProcessSearch= set ()

for key, value in config.items():
    if type(value) == type(config):
        for value, value2 in value.items():
                       
            # aod
            if value =='aod-file' and extrargs.aod:
                config[key][value] = extrargs.aod
                
            # Process Table Maker
            if (value in tablemakerProcessAllParameters) and extrargs.process:
                if value in extrargs.process:
                    value2 = "true"
                    config[key][value] = value2
                    
                    # For find all process parameters for TableMaker/TableMakerMC in Orginal JSON
                    for s in config[key].keys():
                        if s in tablemakerProcessAllParameters:
                            tableMakerProcessSearch.add(s)
                            
                    # check extraargs is contain Full Barrel Muon or Bcs
                    fullSearch = [s for s in extrargs.process if "Full" in s]
                    barrelSearch = [s for s in extrargs.process if "Barrel" in s]
                    muonSearch = [s for s in extrargs.process if "Muon" in s]
                    bcsSearch = [s for s in extrargs.process if "BCs" in s]
                    
                    #check extrargs is contain Filter for automatize Filter PP task
                    filterSearch = [s for s in extrargs.process if "Filter" in s]   
                                                         
                    # Automatization for Activate or Disable d-q barrel, muon and event tasks regarding to process func. in tablemaker
                    if len(fullSearch) > 0 and extrargs.runData and extrargs.run == '3':
                        config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                        
                        if extrargs.isBarrelSelectionTiny == "false":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
                        if extrargs.isBarrelSelectionTiny == "true":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny

                        config["d-q-muons-selection"]["processSelection"] = "true"
                        config["d-q-event-selection-task"]["processEventSelection"] = "true"
                                   
                    if len(barrelSearch) > 0 and extrargs.runData and extrargs.run == '3':
                        if extrargs.isBarrelSelectionTiny == "false":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
                        if extrargs.isBarrelSelectionTiny == "true":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
   
                    if len(barrelSearch) == 0 and len(fullSearch) == 0 and extrargs.runData and extrargs.run == '3':
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = "false"
                                         
                    if len(muonSearch) > 0 and extrargs.runData and extrargs.run == '3':
                            config["d-q-muons-selection"]["processSelection"] = "true"
                    if len(muonSearch) == 0 and len(fullSearch) == 0 and extrargs.runData and extrargs.run == '3':
                            config["d-q-muons-selection"]["processSelection"] = "false"
                            
                    if len(bcsSearch) > 0 and extrargs.runData and extrargs.run == '3':
                            config["d-q-event-selection-task"]["processEventSelection"] = "true"
                    if len(bcsSearch) == 0 and len(fullSearch) == 0 and extrargs.runData and extrargs.run =='3':
                            config["d-q-event-selection-task"]["processEventSelection"] = "false"
                            
                    # Automatization for Activate or Disable d-q filter pp run3
                    if len(filterSearch) > 0 and extrargs.runData and extrargs.run == '3':
                        config["d-q-filter-p-p-task"]["processFilterPP"] ="true"
                        config["d-q-filter-p-p-task"]["processFilterPPTiny"] ="false"
                        if extrargs.isFilterPPTiny == 'true':
                            config["d-q-filter-p-p-task"]["processFilterPP"] = "false"
                            config["d-q-filter-p-p-task"]["processFilterPPTiny"] = "true"
                                 
                    if len(filterSearch) == 0 and extrargs.runData and extrargs.run == '3':
                            config["d-q-filter-p-p-task"]["processFilterPP"] = "false"
                            config["d-q-filter-p-p-task"]["processFilterPPTiny"] = "false"
                                                                        
                elif extrargs.onlySelect == "true":
                    value2 = "false"
                    config[key][value] = value2
                                 
            # Filter PP Selections        
            if value =='cfgPairCuts' and extrargs.cfgPairCuts:
                if type(extrargs.cfgPairCuts) == type(clist):
                    extrargs.cfgPairCuts = listToString(extrargs.cfgPairCuts) 
                config[key][value] = extrargs.cfgPairCuts
            if value == 'cfgBarrelSels' and extrargs.cfgBarrelSels:
                if type(extrargs.cfgBarrelSels) == type(clist):
                    extrargs.cfgBarrelSels = listToString(extrargs.cfgBarrelSels) 
                config[key][value] = extrargs.cfgBarrelSels
            if value == 'cfgMuonSels' and extrargs.cfgMuonSels:
                if type(extrargs.cfgMuonSels) == type(clist):
                    extrargs.cfgMuonSels = listToString(extrargs.cfgMuonSels) 
                config[key][value] = extrargs.cfgMuonSels
                                    
            # Run 2/3 and MC/DATA Selections for automations            
            if extrargs.run == "2":
                if value == 'isRun3':
                    config[key][value] = "false"
                if value == 'processRun3':
                    config[key][value] = "false"
                if value == 'processRun2':
                    config[key][value] = "true"
            if extrargs.run == "3":
                if value == 'isRun3':
                    config[key][value] = "true"
                if value == 'processRun3':
                    config[key][value] = "true"
                if value == 'processRun2':
                    config[key][value] = "false"
            
            if extrargs.run == '2' and extrargs.runMC:
                if value == 'isRun2MC':
                    config[key][value] = "true"
            if extrargs.run != '2' and extrargs.runData:
                if value == 'isRun2MC':
                    config[key][value] = "false"
                                            
            if value == "isMC" and extrargs.runMC:
                    config[key][value] = "true"
            if value == "isMC" and extrargs.runData:
                    config[key][value] = "false"                        
                       
            # PID Selections
            if  (value in PIDParameters) and extrargs.pid:
                if value in extrargs.pid:
                    value2 = "1"
                    config[key][value] = value2
                elif extrargs.onlySelect == "true":
                    value2 = "-1"
                    config[key][value] = value2
                    
            # v0-selector
            if value =='d_bz' and extrargs.d_bz:
                config[key][value] = extrargs.d_bz
            if value == 'v0cospa' and extrargs.v0cospa:
                config[key][value] = extrargs.v0cospa
            if value == 'dcav0dau' and extrargs.dcav0dau:
                config[key][value] = extrargs.dcav0dau
            if value =='v0Rmin' and extrargs.v0Rmin:
                config[key][value] = extrargs.v0Rmin
            if value == 'v0Rmax' and extrargs.v0Rmax:
                config[key][value] = extrargs.v0Rmax
            if value == 'dcamin' and extrargs.dcamin:
                config[key][value] = extrargs.dcamin
            if value == 'dcamax' and extrargs.dcamax:
                config[key][value] = extrargs.dcamax
            if value =='mincrossedrows' and extrargs.mincrossedrows:
                config[key][value] = extrargs.mincrossedrows
            if value == 'maxchi2tpc' and extrargs.maxchi2tpc:
                config[key][value] = extrargs.maxchi2tpc
                
            # centrality table
            if (value in centralityTableParameters) and extrargs.est:
                if value in extrargs.est:
                    value2 = "1"
                    config[key][value] = value2
                elif extrargs.onlySelect == "true":
                    value2 = "-1"
                    config[key][value] = value2
                    
            # cfg in TableMaker
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts)
                config[key][value] = extrargs.cfgEventCuts
            if value == 'cfgBarrelTrackCuts' and extrargs.cfgBarrelTrackCuts:
                if type(extrargs.cfgBarrelTrackCuts) == type(clist):
                    extrargs.cfgBarrelTrackCuts = listToString(extrargs.cfgBarrelTrackCuts)
                config[key][value] = extrargs.cfgBarrelTrackCuts
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                if type(extrargs.cfgMuonCuts) == type(clist):
                    extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts)                
                config[key][value] = extrargs.cfgMuonCuts
            if value == 'cfgBarrelLowPt' and extrargs.cfgBarrelLowPt:
                config[key][value] = extrargs.cfgBarrelLowPt
            if value == 'cfgMuonLowPt' and extrargs.cfgMuonLowPt:
                config[key][value] = extrargs.cfgMuonLowPt
            if value =='cfgNoQA' and extrargs.cfgNoQA:
                config[key][value] = extrargs.cfgNoQA
            if value == 'cfgDetailedQA' and extrargs.cfgDetailedQA:
                config[key][value] = extrargs.cfgDetailedQA
            if value == 'cfgIsRun2' and extrargs.run == "2":
                config[key][value] = "true"
            if value =='cfgMinTpcSignal' and extrargs.cfgMinTpcSignal:
                config[key][value] = extrargs.cfgMinTpcSignal
            if value == 'cfgMaxTpcSignal' and extrargs.cfgMaxTpcSignal:
                config[key][value] = extrargs.cfgMaxTpcSignal
            if value == 'cfgMCsignals' and extrargs.cfgMCsignals:
                if type(extrargs.cfgMCsignals) == type(clist):
                    extrargs.cfgMCsignals = listToString(extrargs.cfgMCsignals)                     
                config[key][value] = extrargs.cfgMCsignals
                
            #d-q muons selection cut
            if value =='cfgMuonsCuts' and extrargs.cfgMuonsCuts:
                if type(extrargs.cfgMuonsCuts) == type(clist):
                    extrargs.cfgMuonsCuts = listToString(extrargs.cfgMuonsCuts)                
                config[key][value] = extrargs.cfgMuonsCuts

            # event-selection
            if value == 'syst' and extrargs.syst:
                config[key][value] = extrargs.syst
            if value =='muonSelection' and extrargs.muonSelection:
                config[key][value] = extrargs.muonSelection
            if value == 'customDeltaBC' and extrargs.customDeltaBC:
                config[key][value] = extrargs.customDeltaBC
                
            # tof-pid-beta
            if value == 'tof-expreso' and extrargs.tof_expreso:
                config[key][value] = extrargs.tof_expreso
                
            # tof-pid-full, tof-pid for data run 3                
            if value == 'processEvTime' and extrargs.runData and extrargs.run == '3': 
                if extrargs.isProcessEvTime == "true":
                    config[key][value] = "true"
                    config[key]["processNoEvTime"] = "false"
                if extrargs.isProcessEvTime == "false":
                    config[key][value] = "false"
                    config[key]["processNoEvTime"] = "true"
                    
            # all d-q tasks and selections
            if value == 'cfgWithQA' and extrargs.cfgWithQA:
                config[key][value] = extrargs.cfgWithQA
                                  
            # track-propagation
            if extrargs.isCovariance:
                if (value =='processStandard' or value == 'processCovariance') and extrargs.isCovariance == 'false' :
                    config[key]["processStandard"] = "true"
                    config[key]["processCovariance"] = "false"
                if (value =='processStandard' or value == 'processCovariance') and extrargs.isCovariance == 'true' :
                    config[key]["processStandard"] = "false"
                    config[key]["processCovariance"] = "true"
                
            # dummy selection
            if value == 'processDummy' and extrargs.processDummy and extrargs.runData and extrargs.run == '3':
                if extrargs.processDummy == "event":
                    config['d-q-event-selection-task']['processDummy'] = "true"
                if extrargs.processDummy == "filter":
                    config['d-q-filter-p-p-task']['processDummy'] = "true"
                if extrargs.processDummy == "barrel":
                    config['d-q-barrel-track-selection-task']['processDummy'] = "true"
                    
            # dummy automizer #TODO: for transaction manag. we need logger for dummy
            if value == 'processDummy' and extrargs.autoDummy and extrargs.runData and extrargs.run == '3':
                
                if config["d-q-barrel-track-selection-task"]["processSelection"] == "true" or config["d-q-barrel-track-selection-task"]["processSelectionTiny"] == "true":
                    config["d-q-barrel-track-selection-task"]["processDummy"] = "false"
                if config["d-q-barrel-track-selection-task"]["processSelection"] == 'false' and config["d-q-barrel-track-selection-task"]["processSelectionTiny"]  == "false":
                    config["d-q-barrel-track-selection-task"]["processDummy"] = "true"
                    
                if config["d-q-muons-selection"]["processSelection"] == "true":
                    config["d-q-muons-selection"]["processDummy"] = "false"
                if config["d-q-muons-selection"]["processSelection"] == "false":
                    config["d-q-muons-selection"]["processDummy"] = "true"
                    
                if config["d-q-event-selection-task"]["processEventSelection"] == "true":
                    config["d-q-event-selection-task"]["processDummy"] = "false"
                if config["d-q-event-selection-task"]["processEventSelection"] == "false":
                    config["d-q-event-selection-task"]["processDummy"] = "true"
                    
                if config["d-q-filter-p-p-task"]["processFilterPP"] =="true" or config["d-q-filter-p-p-task"]["processFilterPPTiny"] == "true":
                    config["d-q-filter-p-p-task"]["processDummy"] = "false"
                if config["d-q-filter-p-p-task"]["processFilterPP"] == "false" and config["d-q-filter-p-p-task"]["processFilterPPTiny"] == "false" :
                    config["d-q-filter-p-p-task"]["processDummy"] = "true"


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
                    print("[WARNING]", j ,"is Not valid Configurable Option for TableMaker regarding to Orginal JSON Config File!!! It will fix by CLI")
                if extrargs.runMC:
                    print("[WARNING]", j ,"is Not valid Configurable Option for TableMakerMC regarding to Orginal JSON Config File!!! It will fix by CLI")
            if j in tableMakerProcessSearch:
                validProcessListAfterDataMCFilter.append(j)
    print("[INFO] Valid processes are after MC/Data Filter: ",validProcessListAfterDataMCFilter)
except:
    print("[WARNING] No process function provided in args, CLI Will not Check process validation for tableMaker/tableMakerMC process")

            
                
# Transaction Management for Most of Parameters for debugging, monitoring and logging
for key,value in configuredCommands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
        if key in V0Parameters and extrargs.runMC:
            print("[WARNING]","--"+key+" Not Valid Parameter. V0 Selector parameters only valid for Data, not MC. It will fixed by CLI")
        if key == 'cfgWithQA' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run 3, not MC and Run 2. It will fixed by CLI")
        if key == 'est' and extrargs.runMC:
            print("[WARNING]","--"+key+" Not Valid Parameter. Centrality Table parameters only valid for Data, not MC. It will fixed by CLI")
        if key =='isFilterPPTiny' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. Filter PP Tiny parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'cfgMuonSels' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'cfgBarrelSels' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'cfgPairCuts' and (extrargs.runMC or extrargs.run == '3'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run2, not MC and Run3. It will fixed by CLI")
        #if key == 'isBarrelSelectionTiny' and (extrargs.runMC or extrargs.run == '2') and extrargs.isBarrelSelectionTiny: TODO: fix logger bug
            #print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'processDummy' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'cfgMCsignals' and extrargs.runData:
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for MC, not Data. It will fixed by CLI")
        if key == 'isProcessEvTime' and (extrargs.run == '2' or extrargs.runMC):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
                                         
# Centrality table delete for pp processes
if extrargs.syst == 'pp' or  config["event-selection-task"]["syst"] == "pp":
    # delete centrality-table configurations for data. If it's MC don't delete from JSON
    # Firstly try for Data then if not data it gives warning message for MC
    noDeleteNeedForCent = False
    try:
            print("[INFO] JSON file does not include configs for centrality-table task, It's for DATA. Centrality will removed because you select pp collision system.")
        #del(config["centrality-table"])
    except:
        if extrargs.runMC:
            print("[INFO] JSON file does not include configs for centrality-table task, It's for MC. Centrality will removed because you select pp collision system.")
    # check for is TableMaker includes task related to Centrality?
    try:
        processCentralityMatch = [s for s in extrargs.process if "Cent" in s]
        if len(processCentralityMatch) > 0:
            print("[WARNING] Collision System pp can't be include related task about Centrality. They Will be removed in automation. Check your JSON configuration file for Tablemaker process function!!!")
            for paramValueTableMaker in processCentralityMatch:
                # Centrality process should be false
                if extrargs.runMC:
                    try:       
                        config["table-maker-m-c"][paramValueTableMaker] = 'false'
                    except:
                        print("[ERROR] JSON config does not include table-maker-m-c, It's for Data. Misconfiguration JSON File!!!")
                        sys.exit()
                if extrargs.runData:
                    try:       
                        config["table-maker"][paramValueTableMaker] = 'false'
                    except:
                        print("[ERROR] JSON config does not include table-maker, It's for MC. Misconfiguration JSON File!!!")
                        sys.exit()
    except:
        print("[WARNING] No process function provided so no need delete related to centrality-table dependency")
         
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

# Logger Message
if noDeleteNeedForCent == False: 
    print("[INFO]","After deleting the process functions related to the centrality table (for collision system pp), the remaining processes: ",leftProcessAfterDeleteCent)
 
if processLeftAfterCentDelete == False and noDeleteNeedForCent == False:
    print("[ERROR] After deleting the process functions related to the centrality table, there are no functions left to process, misconfigure for process!!!")    
    sys.exit()       
  
# AOD File checker 
if extrargs.aod != None:
    if os.path.isfile(extrargs.aod) == False:
        print("[ERROR]",extrargs.aod,"File not found in path!!!")
        sys.exit()
elif os.path.isfile((config["internal-dpl-aod-reader"]["aod-file"])) == False:
        print("[ERROR]",config["internal-dpl-aod-reader"]["aod-file"],"File not found in path!!!")
        sys.exit()



###########################
# End Interface Processes #
###########################



# Write the updated configuration file into a temporary file
updatedConfigFileName = "tempConfigTableMaker.json"
# TODO Fix and implemente it
"""
Transaction Management for Json File Name

if(extrargs.outputjson == None):       
    config_output_json = open(updatedConfigFileName,'w')
    config_output_json.write(json.dumps(config, indent= 2))
    print("[WARNING] Forget to Give output JSON name. Output JSON will created as tempConfig.json")
elif(extrargs.outputjson[-5:] == ".json"):
    updatedConfigFileName = extrargs.outputjson
    config_output_json = open(updatedConfigFileName,'w')
    config_output_json.write(json.dumps(config, indent= 2))
elif(extrargs.outputjson[-5:] != ".json"):
    if '.' in extrargs.outputjson:
        print("[ERROR] Wrong formatted input for JSON output!!! Script will Stopped.")
        sys.exit()
    temp = extrargs.outputjson
    temp = temp+'.json'
    updatedConfigFileName = temp
    config_output_json = open(updatedConfigFileName,'w')
    config_output_json.write(json.dumps(config, indent= 2))
else:
    print("Logical json input error. Report it!!!")
"""
    
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
    print("processFunc ========")
    print(processFunc)
    if "processFull" in processFunc or "processBarrel" in processFunc:
      print("common barrel tables==========")      
      for table in barrelCommonTables:
        print(table)      
        tablesToProduce[table] = 1
      if runOverMC == True:
        tablesToProduce["ReducedTracksBarrelLabels"] = 1
    if "processFull" in processFunc or "processMuon" in processFunc:
      print("common muon tables==========")      
      for table in muonCommonTables:
        print(table)
        tablesToProduce[table] = 1
      if runOverMC == True:
        tablesToProduce["ReducedMuonsLabels"] = 1  
    if runOverMC == True:
      tablesToProduce["ReducedMCTracks"] = 1
    print("specific tables==========")      
    for table in specificTables[processFunc]:
      print(table)      
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
iTable = 0
for table in tablesToProduce.keys():
  writerConfig["OutputDirector"]["OutputDescriptors"].insert(iTable, tables[table])
  iTable += 1
  
writerConfigFileName = "aodWriterTempConfig.json"
with open(writerConfigFileName,'w') as writerConfigFile:
  json.dump(writerConfig, writerConfigFile, indent=2)  
  
print(writerConfig)
#sys.exit()
      
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --severity error --shm-segment-size 12000000000 --aod-writer-json " + writerConfigFileName + " -b"
for dep in depsToRun.keys():
  commandToRun += " | " + dep + " --configuration json://" + updatedConfigFileName + " -b"

if extrargs.add_mc_conv:
    commandToRun += " | o2-analysis-mc-converter --configuration json://" + updatedConfigFileName + " -b"

if extrargs.add_fdd_conv:
    commandToRun += " | o2-analysis-fdd-converter --configuration json://" + updatedConfigFileName + " -b"

if extrargs.add_track_prop:
    commandToRun += " | o2-analysis-track-propagation --configuration json://" + updatedConfigFileName + " -b"

print("====================================================================================================================")
print("Command to run:")
print(commandToRun)
print("====================================================================================================================")
print("Tables to produce:")
print(tablesToProduce.keys())
print("====================================================================================================================")
#sys.exit()

# Listing Added Commands
print("Args provided configurations List")
print("====================================================================================================================")
forgetParams = []
for key,value in configuredCommands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
        print("--"+key,":", value)
        if (type(value) == type("string") or type(value) == type(clist)) and len(value) == 0:
            forgetParams.append(key)
print("[WARNING] Your forget assign a value to for this parameters: ", forgetParams)

os.system(commandToRun)
