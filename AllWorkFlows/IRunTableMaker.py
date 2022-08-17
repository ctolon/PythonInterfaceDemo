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
    li = list(string.split(","))
    return li

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

# List for Transcation management for FilterPP
muonCutList = [] # List --> transcation management for filterPP
barrelTrackCutList = [] # List --> transcation management for filterPP
barrelSelsList = []
muonSelsList = []
barrelSelsListAfterSplit = []
muonSelsListAfterSplit = []

# Get system variables in alienv.#TODO:In alienv we don't have cuts and signal library!!! We need discuss this thing
O2DPG_ROOT=os.environ.get('O2DPG_ROOT')
QUALITYCONTROL_ROOT=os.environ.get('QUALITYCONTROL_ROOT')
O2_ROOT=os.environ.get('O2_ROOT')
O2PHYSICS_ROOT=os.environ.get('O2PHYSICS_ROOT')

################################
# Download DQ Libs From Github #
################################

# It works on for only master branch

# header for github download
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

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
                namespacedPairCuts = [x + namespaceDef for x in allPairCuts] # paircut:
            allCuts = allCuts + getAnalysisCuts # Get all Cuts from CutsLibrary.h
            nameSpacedAllCuts = [x + namespaceDef for x in allCuts] # cut:
            nameSpacedAllCutsTwoDots = [x + namespaceDef2 for x in allCuts]  # cut::

 
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
parser.add_argument('--logFile', help="Enable logger for both file and CLI", action="store_true")

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
parser.add_argument('--cfgBarrelSels', help="Configure Barrel Selection <track-cut>:[<pair-cut>]:<n>,[<track-cut>:[<pair-cut>]:<n>],... | example jpsiO2MCdebugCuts2::1 ",choices=allSels, action="store", type=str,nargs="*", metavar='') # run2 
parser.add_argument('--cfgMuonSels', help="Configure Muon Selection <muon-cut>:[<pair-cut>]:<n> example muonQualityCuts:pairNoCut:1",choices=allSels, action="store", type=str,nargs="*", metavar='') # run 2
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

# debug options
parser.add_argument('--debug', help="execute with debug options", action="store", choices=["NOTSET","DEBUG","INFO","WARNING","ERROR","CRITICAL"], type=str.upper, default="INFO")

argcomplete.autocomplete(parser)
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
  logging.error("Invalid syntax! The command line should look like this:")
  logging.info("  ./IRunTableMaker.py <yourConfig.json> <runData|runMC> --run <2|3> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
config = {}
#cfgFileName = 'configTableMakerDataRun3.json'
with open(extrargs.cfgFileName) as configFile:
  config = json.load(configFile)

# Check whether we run over data or MC
if not (extrargs.runMC or extrargs.runData):
  logging.error("You have to specify either runMC or runData !")
  sys.exit()
  
# Check whether we run over run 2 or run 3
if not (extrargs.run == '3' or extrargs.run == '2'):
  logging.error("You have to specify either --run 3 or --run 2 !")
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

# For adding a process function from TableMaker and all process should be added only once so set type used
tableMakerProcessSearch= set ()

for key, value in config.items():
    if type(value) == type(config):
        for value, value2 in value.items():
                       
            # aod
            if value =='aod-file' and extrargs.aod:
                config[key][value] = extrargs.aod
                logging.debug(" - [%s] %s : %s",key,value,extrargs.aod)
                
            # Process Table Maker
            if (value in tablemakerProcessAllParameters) and extrargs.process:
                if value in extrargs.process:
                    value2 = "true"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)
                #if value not in extrargs.process:
                    #logging.debug(" - [%s] %s : %s",key,value,value2)
                    
                    
                    # For find all process parameters for TableMaker/TableMakerMC in Orginal JSON
                    for s in config[key].keys():
                        if s in tablemakerProcessAllParameters:
                            tableMakerProcessSearch.add(s)
                    # check extraargs is contain Full Barrel Muon or Bcs
                    fullSearch = [s for s in extrargs.process if "Full" in s]
                    barrelSearch = [s for s in extrargs.process if "Barrel" in s]
                    muonSearch = [s for s in extrargs.process if "Muon" in s]
                    bcsSearch = [s for s in extrargs.process if "BCs" in s]
                    
                    #check extrargs is contain Cent for transcation management Centrality Filter
                    centSearch = [s for s in extrargs.process if "Cent" in s]
                    logging.info("cent search : %s",centSearch)   
                    
                    #check extrargs is contain Filter for automatize Filter PP task
                    filterSearch = [s for s in extrargs.process if "Filter" in s]   
                                                         
                    # Automatization for Activate or Disable d-q barrel, muon and event tasks regarding to process func. in tablemaker
                    if len(fullSearch) > 0 and extrargs.runData and extrargs.run == '3':
                        config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                        logging.debug(" - [d-q-barrel-track-selection-task] processSelection : true")
                        
                        if extrargs.isBarrelSelectionTiny == "false":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
                            logging.debug(" - [d-q-barrel-track-selection-task] processSelection : true")
                            logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : false")
                        if extrargs.isBarrelSelectionTiny == "true":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
                            logging.debug(" - [d-q-barrel-track-selection-task] processSelection : false")
                            logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : true")

                        config["d-q-muons-selection"]["processSelection"] = "true"
                        logging.debug(" - [d-q-muons-selection] processSelection : true")
                        config["d-q-event-selection-task"]["processEventSelection"] = "true"
                        logging.debug(" - [d-q-event-selection-task] processEventSelection : true")

                                   
                    if len(barrelSearch) > 0 and extrargs.runData and extrargs.run == '3':
                        if extrargs.isBarrelSelectionTiny == "false":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
                            logging.debug(" - [d-q-barrel-track-selection-task] processSelection : true")
                            logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : false")
                        if extrargs.isBarrelSelectionTiny == "true":
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                            config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = extrargs.isBarrelSelectionTiny
                            logging.debug(" - [d-q-barrel-track-selection-task] processSelection : false")
                            logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : true")
   
                    if len(barrelSearch) == 0 and len(fullSearch) == 0 and extrargs.runData and extrargs.run == '3':
                        config["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                        config["d-q-barrel-track-selection-task"]["processSelectionTiny"] = "false"
                        logging.debug(" - [d-q-barrel-track-selection-task] processSelection : false")
                        logging.debug(" - [d-q-barrel-track-selection-task] processSelectionTiny : false")
                                         
                    if len(muonSearch) > 0 and extrargs.runData and extrargs.run == '3':
                        config["d-q-muons-selection"]["processSelection"] = "true"
                        logging.debug(" - [d-q-muons-selection] processSelection : true")
                    if len(muonSearch) == 0 and len(fullSearch) == 0 and extrargs.runData and extrargs.run == '3':
                        config["d-q-muons-selection"]["processSelection"] = "false"
                        logging.debug(" - [d-q-muons-selection] processSelection : false")
                            
                    if len(bcsSearch) > 0 and extrargs.runData and extrargs.run == '3':
                        config["d-q-event-selection-task"]["processEventSelection"] = "true"
                        logging.debug(" - [d-q-event-selection-task] processEventSelection : true")
                    if len(bcsSearch) == 0 and len(fullSearch) == 0 and extrargs.runData and extrargs.run =='3':
                        config["d-q-event-selection-task"]["processEventSelection"] = "false"
                        logging.debug(" - [d-q-event-selection-task] processEventSelection : false")
                            
                    # Automatization for Activate or Disable d-q filter pp run3
                    if len(filterSearch) > 0 and extrargs.runData and extrargs.run == '3':
                        config["d-q-filter-p-p-task"]["processFilterPP"] ="true"
                        config["d-q-filter-p-p-task"]["processFilterPPTiny"] ="false"
                        logging.debug(" - [d-q-filter-p-p-task-task] processFilterPP : true")
                        logging.debug(" - [d-q-filter-p-p-task-task] processFilterPPTiny : false")
                        if extrargs.isFilterPPTiny == 'true':
                            config["d-q-filter-p-p-task"]["processFilterPP"] = "false"
                            config["d-q-filter-p-p-task"]["processFilterPPTiny"] = "true"
                            logging.debug(" - [d-q-filter-p-p-task-task] processFilterPP : false")
                            logging.debug(" - [d-q-filter-p-p-task-task] processFilterPPTiny : true")
                                 
                    if len(filterSearch) == 0 and extrargs.runData and extrargs.run == '3':
                        config["d-q-filter-p-p-task"]["processFilterPP"] = "false"
                        config["d-q-filter-p-p-task"]["processFilterPPTiny"] = "false"
                        logging.debug(" - [d-q-filter-p-p-task-task] processFilterPP : false")
                        logging.debug(" - [d-q-filter-p-p-task-task] processFilterPPTiny : true")
                                                                        
                elif extrargs.onlySelect == "true":
                    value2 = "false"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)
                    
                                 
            # Filter PP Selections        
            if value =='cfgPairCuts' and extrargs.cfgPairCuts:
                if type(extrargs.cfgPairCuts) == type(clist):
                    extrargs.cfgPairCuts = listToString(extrargs.cfgPairCuts) 
                config[key][value] = extrargs.cfgPairCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgPairCuts)
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
                    logging.debug(" - [%s] %s : true",key,value)                          
                       
            # PID Selections
            if  (value in PIDParameters) and extrargs.pid:
                if value in extrargs.pid:
                    value2 = "1"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)  
                elif extrargs.onlySelect == "true":
                    value2 = "-1"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)  
                    
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
                
            # centrality table
            if (value in centralityTableParameters) and extrargs.est:
                if value in extrargs.est:
                    value2 = "1"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)   
                elif extrargs.onlySelect == "true":
                    value2 = "-1"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)  
                    
            # cfg in TableMaker
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts)
                config[key][value] = extrargs.cfgEventCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgEventCuts)  
            if value == 'cfgBarrelTrackCuts' and extrargs.cfgBarrelTrackCuts:
                if type(extrargs.cfgBarrelTrackCuts) == type(clist):
                    extrargs.cfgBarrelTrackCuts = listToString(extrargs.cfgBarrelTrackCuts)
                config[key][value] = extrargs.cfgBarrelTrackCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgBarrelTrackCuts)  
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                if type(extrargs.cfgMuonCuts) == type(clist):
                    extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts)                
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
                config[key][value] = extrargs.cfgMCsignals
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMCsignals)  
                
            #d-q muons selection cut
            if value =='cfgMuonsCuts' and extrargs.cfgMuonsCuts:
                if type(extrargs.cfgMuonsCuts) == type(clist):
                    extrargs.cfgMuonsCuts = listToString(extrargs.cfgMuonsCuts)                
                config[key][value] = extrargs.cfgMuonsCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonsCuts) 

            # event-selection
            if value == 'syst' and extrargs.syst:
                config[key][value] = extrargs.syst
                logging.debug(" - [%s] %s : %s",key,value,extrargs.syst)  
            if value =='muonSelection' and extrargs.muonSelection:
                config[key][value] = extrargs.muonSelection
                logging.debug(" - [%s] %s : %s",key,value,extrargs.muonSelection)  
            if value == 'customDeltaBC' and extrargs.customDeltaBC:
                config[key][value] = extrargs.customDeltaBC
                logging.debug(" - [%s] %s : %s",key,value,extrargs.customDeltaBC)  
                
            # tof-pid-beta
            if value == 'tof-expreso' and extrargs.tof_expreso:
                config[key][value] = extrargs.tof_expreso
                logging.debug(" - [%s] %s : %s",key,value,extrargs.tof_expreso)  
                
            # tof-pid-full, tof-pid for data run 3                
            if value == 'processEvTime' and extrargs.runData and extrargs.run == '3': 
                if extrargs.isProcessEvTime == "true":
                    config[key][value] = "true"
                    config[key]["processNoEvTime"] = "false"
                    logging.debug(" - %s %s : true",key,value)
                    logging.debug(" - [%s] processNoEvTime : false",key)  
                if extrargs.isProcessEvTime == "false":
                    config[key][value] = "false"
                    config[key]["processNoEvTime"] = "true"
                    logging.debug(" - %s %s : false",key,value) 
                    logging.debug(" - [%s] processNoEvTime : true",key)  
                    
                    
            # all d-q tasks and selections
            if value == 'cfgWithQA' and extrargs.cfgWithQA:
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
                
            # dummy selection
            if value == 'processDummy' and extrargs.processDummy and extrargs.runData and extrargs.run == '3':
                if extrargs.processDummy == "event":
                    config['d-q-event-selection-task']['processDummy'] = "true"
                if extrargs.processDummy == "filter":
                    config['d-q-filter-p-p-task']['processDummy'] = "true"
                if extrargs.processDummy == "barrel":
                    config['d-q-barrel-track-selection-task']['processDummy'] = "true"
                    
            # dummy automizer
            if value == 'processDummy' and extrargs.autoDummy and extrargs.runData and extrargs.run == '3':
                
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
                if extrargs.runMC:
                    logging.warning("%s is Not valid Configurable Option for TableMakerMC regarding to Orginal JSON Config File!!! It will fix by CLI",j)
            if j in tableMakerProcessSearch:
                validProcessListAfterDataMCFilter.append(j)
    logging.info("Valid processes are after MC/Data Filter: %s",validProcessListAfterDataMCFilter)
except:
    logging.warning("No process function provided in args, CLI Will not Check process validation for tableMaker/tableMakerMC process")

            
                
# Transaction Management for Most of Parameters for debugging, monitoring and logging
for key,value in configuredCommands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
        if key in V0Parameters and extrargs.runMC:
            logging.warning("--%s Not Valid Parameter. V0 Selector parameters only valid for Data, not MC. It will fixed by CLI", key)
        if key == 'cfgWithQA' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run 3, not MC and Run 2. It will fixed by CLI", key)
        if key == 'est' and extrargs.runMC:
            logging.warning("--%s Not Valid Parameter. Centrality Table parameters only valid for Data, not MC. It will fixed by CLI", key)
        if key =='isFilterPPTiny' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. Filter PP Tiny parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)
        if key == 'cfgMuonSels' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)
        if key == 'cfgBarrelSels' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)
        if key == 'cfgPairCuts' and (extrargs.runMC or extrargs.run == '3'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run2, not MC and Run3. It will fixed by CLI", key)
        #if key == 'isBarrelSelectionTiny' and (extrargs.runMC or extrargs.run == '2') and extrargs.isBarrelSelectionTiny: TODO: fix logging bug
            #print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'processDummy' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)
        if key == 'cfgMCsignals' and extrargs.runData:
            logging.warning("--%s Not Valid Parameter. This parameter only valid for MC, not Data. It will fixed by CLI", key)
        if key == 'isProcessEvTime' and (extrargs.run == '2' or extrargs.runMC):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)
                                         
# Centrality table delete for pp processes
if len(centSearch) != 0 and (extrargs.syst == 'pp' or (extrargs.syst == None and config["event-selection-task"]["syst"] == "pp")):
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
    #print("after split: ", muonSels)

    # remove string values after :
    for i in muonSels:
        i = i[ 0 : i.index(":")]
        muonSelsListAfterSplit.append(i)
    #print("after split muonSels: ", muonSelsListAfterSplit)

    # Remove duplicated values with set convertion
    muonSelsListAfterSplit = set(muonSelsListAfterSplit)
    muonSelsListAfterSplit = list(muonSelsListAfterSplit)
    #print("after remove duplicated values from muonSels: ", muonSelsListAfterSplit)

    for i in muonSelsListAfterSplit:
        if i in muonCut:
            #print("selection: ", i,"in", muonCut)
            #count = count +1
            continue
        else:
            print("====================================================================================================================")
            logging.error("--cfgMuonSels <value>: %s not in --cfgMuonsCuts %s ",i, muonCut)
            logging.info("For fixing this issue, you should have the same number of cuts (and in the same order) provided to the cfgMuonsCuts from dq-selection as those provided to the cfgMuonSels in the DQFilterPPTask.") 
            print("For example, if cfgMuonCuts is muonLowPt,muonHighPt, then the cfgMuonSels has to be something like: muonLowPt::1,muonHighPt::1,muonLowPt:pairNoCut:1")  
            sys.exit()
                            
    for i in muonCut:    
        if i in muonSelsListAfterSplit:
            #print("muon cut: ",i," in", muonSelsListAfterSplit)
            #count2 = count2 +1
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
    #print("after split: ", barrelSels)

    # remove string values after :

    for i in barrelSels:
        i = i[ 0 : i.index(":")]
        barrelSelsListAfterSplit.append(i)
    #print("after split barrelSels: ", barrelSelsListAfterSplit)

    # Remove duplicated values with set convertion
    barrelSelsListAfterSplit = set(barrelSelsListAfterSplit)
    barrelSelsListAfterSplit = list(barrelSelsListAfterSplit)
    #print("after remove duplicated values from barrelSels: ", barrelSelsListAfterSplit)

    for i in barrelSelsListAfterSplit:
        if i in barrelTrackCut:
            #print("selection: ", i,"in", barrelTrackCut)
            #count = count +1
            continue
        else:
            print("====================================================================================================================")
            logging.error("--cfgBarrelTrackCuts <value>: %s not in --cfgBarrelSels %s",i,barrelTrackCut)
            logging.info("For fixing this issue, you should have the same number of cuts (and in the same order) provided to the cfgBarrelTrackCuts from dq-selection as those provided to the cfgBarrelSels in the DQFilterPPTask.")  
            print("For example, if cfgBarrelTrackCuts is jpsiO2MCdebugCuts,jpsiO2MCdebugCuts2, then the cfgBarrelSels has to be something like: jpsiO2MCdebugCuts::1,jpsiO2MCdebugCuts2::1,jpsiO2MCdebugCuts:pairNoCut:1") 
            sys.exit()
                            
    for i in barrelTrackCut:    
        if i in barrelSelsListAfterSplit:
            #print("barrel track cut: ",i," in", barrelSelsListAfterSplit)
            #count2 = count2 +1
            continue
        else:
            print("====================================================================================================================")
            logging.error("--cfgBarrelTrackCuts <value>: %s not in --cfgBarrelSels %s",i,barrelSelsListAfterSplit)
            logging.info("For fixing this issue, you should have the same number of cuts (and in the same order) provided to the cfgBarrelTrackCuts from dq-selection as those provided to the cfgBarrelSels in the DQFilterPPTask.") 
            print("For example, if cfgBarrelTrackCuts is jpsiO2MCdebugCuts,jpsiO2MCdebugCuts2, then the cfgBarrelSels has to be something like: jpsiO2MCdebugCuts::1,jpsiO2MCdebugCuts2::1,jpsiO2MCdebugCuts:pairNoCut:1")      
            sys.exit()

 
# AOD File checker 
if extrargs.aod != None:
    if os.path.isfile(extrargs.aod) == False:
        logging.error("%s File not found in path!!!",extrargs.aod)
        sys.exit()
elif os.path.isfile((config["internal-dpl-aod-reader"]["aod-file"])) == False:
        print("[ERROR]",config["internal-dpl-aod-reader"]["aod-file"],"File not found in path!!!")
        sys.exit()



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
iTable = 0
for table in tablesToProduce.keys():
  writerConfig["OutputDirector"]["OutputDescriptors"].insert(iTable, tables[table])
  iTable += 1
  
writerConfigFileName = "aodWriterTempConfig.json"
with open(writerConfigFileName,'w') as writerConfigFile:
  json.dump(writerConfig, writerConfigFile, indent=2)  

logging.info("aodWriterTempConfig==========")  
print(writerConfig)
#sys.exit()
      
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --severity error --shm-segment-size 12000000000 --aod-writer-json " + writerConfigFileName + " -b"
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
