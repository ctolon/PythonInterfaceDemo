#!/usr/bin/env python3
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
if (os.path.isfile('tempCutsLibrary.h') == False):
    urlCutsLibrary = 'https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/CutsLibrary.h'

    urllib.request.urlretrieve(urlCutsLibrary,"tempCutsLibrary.h")
    
clist=[] # control list for type control
allValuesCfg = [] # counter for provided args
allCuts = [] # all analysis cuts
allPairCuts = [] # only pair cuts
nAddedAllCutsList = [] # e.g. muonQualityCuts::2
nAddedPairCutsList = [] # e.g paircutMass::3
SelsStyle1  =[ ] # track/muon cut::paircut::n
allSels = [] # track/muon cut::n
namespaceDef = ":" # Namespace reference
namespaceDef2 = "::" # Namespace reference


# Get paths in localy
#MCSignalsPath = os.path.expanduser("~/alice/O2Physics/PWGDQ/Core/MCSignalLibrary.h")
#AnalysisCutsPath = os.path.expanduser("~/alice/O2Physics/PWGDQ/Core/CutsLibrary.h")
#print(os.environ['ALIBUILD_WORK_DIR'])

# Get system variables in alienv. In alienv we don't have cuts and signal library!!! We need discuss this thing
"""
O2DPG_ROOT=os.environ.get('O2DPG_ROOT')
QUALITYCONTROL_ROOT=environ.get('QUALITYCONTROL_ROOT')
O2_ROOT=os.environ.get('O2_ROOT')
O2PHYSICS_ROOT=os.environ.get('O2PHYSICS_ROOT')
"""
            
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

# For filterPP, Filter PP Process should always true
dqSelections = ["eventSelection","barrelTrackSelection","muonSelection","barrelTrackSelectionTiny","filterPPSelectionTiny"]

PIDSelections = ["el","mu","pi","ka","pr","de","tr","he","al"]
PIDParameters = ["pid-el","pid-mu","pid-pi","pid-ka","pid-pr","pid-de","pid-tr","pid-he","pid-al"]

processDummySelections =["filter","event","barrel"]


###################
# Main Parameters #
###################
    
parser = argparse.ArgumentParser(description='Arguments to pass')
parser.add_argument('cfgFileName', metavar='text', default='config.json', help='config file name')
#parser.add_argument('-runData', help="Run over data", action="store_true")
#parser.add_argument('-runMC', help="Run over MC", action="store_true")

##################
# Interface Part #
##################

# aod
parser.add_argument('--aod', help="Add your AOD File with path", action="store", type=str)

#json output
#parser.add_argument('--outputjson', help="Your Output JSON Config Fİle", action="store", type=str)

# only select
#parser.add_argument('--onlySelect', help="An Automate parameter for keep options for only selection in process, pid and centrality table (true is highly recomended for automation)", action="store",choices=["true","false"], default="true", type=str.lower)

# Run Selection : event-selection-task ,bc-selection-task, multiplicity-table, track-extension no refactor
#parser.add_argument('--run', help="Run Selection (2 or 3)", action="store", choices=['2','3'], type=str)

# event-selection-task
parser.add_argument('--syst', help="Collision System Selection ex. pp", action="store", choices=["PbPb", "pp", "pPb", "Pbp", "XeXe"], type=str)
parser.add_argument('--muonSelection', help="0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts",choices=["0","1","2"], action="store", type=str)
parser.add_argument('--customDeltaBC', help="custom BC delta for FIT-collision matching", action="store", type=str)

#tof-pid-beta
parser.add_argument('--tof-expreso', help="Expected resolution for the computation of the expected beta", action="store", type=str)

# dummies
#parser.add_argument('--processDummy', help="Dummy function (No need If autoDummy is true)", action="store", choices=processDummySelections, nargs='*', type=str.lower) #event selection, barel track task, filter task
parser.add_argument('--autoDummy', help="Dummy automize parameter (if your selection true, it automatically activate dummy process and viceversa)", action="store", choices=["true","false"], default='true', type=str.lower) #event selection, barel track task, filter task

# DQ Task Selections
parser.add_argument('--process', help="DQ Task Selections",choices=dqSelections, action="store", type=str,  nargs='*', metavar='') # run2 

# d-q-filter-p-p-task
#parser.add_argument('--cfgPairCuts', help="Space separated list of pair cuts", action="store", choices=allPairCuts, nargs='*', type=str, metavar='') # run3
parser.add_argument('--cfgBarrelSels', help="Configure Barrel Selection <track-cut>:[<pair-cut>]:<n>,[<track-cut>:[<pair-cut>]:<n>],... | example jpsiO2MCdebugCuts2::1 ",choices=allSels, action="store", type=str, metavar='') # run2 
parser.add_argument('--cfgMuonSels', help="Configure Muon Selection <muon-cut>:[<pair-cut>]:<n> example muonQualityCuts:pairNoCut:1",choices=allSels, action="store", type=str, metavar='') # run 2

## d-q-event-selection
parser.add_argument('--cfgEventCuts', help="Space separated list of event cuts", choices=allCuts, nargs='*', action="store", type=str, metavar='')
#parser.add_argument('--processEventSelection', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

## d-q-barrel-track-selection
parser.add_argument('--cfgBarrelTrackCuts', help="Space separated list of barrel track cuts", choices=allCuts,nargs='*', action="store", type=str, metavar='')

## d-q-muons-selection
parser.add_argument('--cfgMuonsCuts', help="Space separated list of muon cuts in d-q muons selection", action="store", choices=allCuts, nargs='*', type=str, metavar='')

#all d-q tasks and selections
parser.add_argument('--cfgWithQA', help="If true, fill QA histograms", action="store", choices=['true','false'], type=str.lower)

# pid
parser.add_argument('--pid', help="Produce PID information for the particle mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)", action="store", choices=PIDSelections, nargs='*', type=str.lower)

# helper lister commands
parser.add_argument('--cutLister', help="List all of the analysis cuts from CutsLibrary.h", action="store_true")


# TODO: We don't have options for this values. Discuss with ionut
# tof-pid-full, tof-pid for run3 ???
parser.add_argument('--isProcessEvTime', help="tof-pid -> processEvTime : Process Selection options true or false (string)", action="store", choices=['true','false'], type=str.lower)

# timestamp-task
#parser.add_argument('--isRun2MC', help="Selection the Process is MC or Not", action="store", choices=['true','false'], type=str)

#parser.add_argument('--processFilterPPTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3


argcomplete.autocomplete(parser)
extrargs = parser.parse_args()

configuredCommands = vars(extrargs) # for get extrargs

###################
# HELPER MESSAGES #
###################

#TODO: Provide a Table format for print option       

if extrargs.cutLister:
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

######################
# PREFIX ADDING PART #
###################### 

# add prefix for extrargs.process for TableMaker and Filter PP
#if extrargs.process != None:
    #prefix_process = "process"
    #extrargs.process = [prefix_process + sub for sub in extrargs.process]

# add prefix for extrargs.pid for pid selection
if extrargs.pid != None:
    prefix_pid = "pid-"
    extrargs.pid = [prefix_pid + sub for sub in extrargs.pid]
    
######################################################################################

commonDeps = ["o2-analysis-timestamp", "o2-analysis-event-selection", "o2-analysis-multiplicity-table", "o2-analysis-trackselection", "o2-analysis-track-propagation", "o2-analysis-pid-tof-base", "o2-analysis-pid-tof", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]



# Make some checks on provided arguments
if len(sys.argv) < 3:
  print("ERROR: Invalid syntax! The command line should look like this:")
  print("  ./IFilterPP.py <yourConfig.json> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
config = {}
with open(sys.argv[1]) as configFile:
  config = json.load(configFile)

taskNameInConfig = "d-q-filter-p-p-task"
taskNameInCommandLine = "o2-analysis-dq-filter-pp"

if not taskNameInConfig in config:
  print("[ERROR] ",taskNameInConfig," Task to be run not found in the configuration file!")
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
                
            # DQ Selections for muons and barrel tracks
            if value =='processSelection' and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'process': #  Only Select key for analysis
                                      
                            if key == 'd-q-barrel-track-selection':                    
                                if 'barrelTrackSelection' in valueCfg:
                                    config[key][value] = 'true'
                                if 'barrelTrackSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                                      
                            if key == 'd-q-muons-selection':
                                if 'muonSelection' in valueCfg:
                                    config[key][value] = 'true'
                                if 'muonSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                                                                               
            # DQ Selections event    
            if value =='processEventSelection' and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'process': #  Only Select key for analysis
                            
                            if key == 'd-q-event-selection-task':
                                if 'eventSelection' in valueCfg:
                                    config[key][value] = 'true'
                                if 'eventSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    
            # DQ Tiny Selection for barrel track
            if value =='processSelectionTiny' and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'process': #  Only Select key for analysis
                                      
                            if key == 'd-q-barrel-track-selection':                    
                                if 'barrelTrackSelectionTiny' in valueCfg:
                                    config[key][value] = 'true'
                                if 'barrelTrackSelectionTiny' not in valueCfg:
                                    config[key][value] = 'false'
            
            # DQ Tiny Selection for filterPP
            if value =='processFilterPPTiny' and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'process': #  Only Select key for analysis
                                      
                            if key == 'd-q-filter-p-p-task':                    
                                if 'filterPPSelectionTiny' in valueCfg:
                                    config[key][value] = 'true'
                                if 'filterPPSelectionTiny' not in valueCfg:
                                    config[key][value] = 'false'
                                                                                                          
            # Filter PP Selections        
            if value == 'cfgBarrelSels' and extrargs.cfgBarrelSels:
                if type(extrargs.cfgBarrelSels) == type(clist):
                    extrargs.cfgBarrelSels = listToString(extrargs.cfgBarrelSels) 
                config[key][value] = extrargs.cfgBarrelSels
            if value == 'cfgMuonSels' and extrargs.cfgMuonSels:
                if type(extrargs.cfgMuonSels) == type(clist):
                    extrargs.cfgMuonSels = listToString(extrargs.cfgMuonSels) 
                config[key][value] = extrargs.cfgMuonSels
                
            # DQ Cuts    
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts) 
                config[key][value] = extrargs.cfgEventCuts
            if value == 'cfgBarrelTrackCuts' and extrargs.cfgBarrelTrackCuts:
                if type(extrargs.cfgBarrelTrackCuts) == type(clist):
                    extrargs.cfgBarrelTrackCuts = listToString(extrargs.cfgBarrelTrackCuts) 
                config[key][value] = extrargs.cfgBarrelTrackCuts
            if value == 'cfgMuonsCuts' and extrargs.cfgMuonsCuts:
                if type(extrargs.cfgMuonsCuts) == type(clist):
                    extrargs.cfgMuonsCuts = listToString(extrargs.cfgMuonsCuts) 
                config[key][value] = extrargs.cfgMuonsCuts
            
            # QA Options  
            if value == 'cfgWithQA' and extrargs.cfgWithQA:
                config[key][value] = extrargs.cfgWithQA  

                                    
            # Run 2/3 and MC/DATA Selections for automations
            """         
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
            """     
                  
            # PID Selections
            if  (value in PIDParameters) and extrargs.pid:
                if value in extrargs.pid:
                    value2 = "1"
                    config[key][value] = value2
                elif extrargs.onlySelect == "true":
                    value2 = "-1"
                    config[key][value] = value2
            

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
                                    
            # all d-q tasks and selections
            if value == 'cfgWithQA' and extrargs.cfgWithQA:
                config[key][value] = extrargs.cfgWithQA
                
            # processEvTime    
            if value == 'processEvTime':
                if extrargs.isProcessEvTime == "true":
                    config[key][value] = "true"
                    config[key]["processNoEvTime"] = "false"
                if extrargs.isProcessEvTime == "false":
                    config[key][value] = "false"
                    config[key]["processNoEvTime"] = "true"
                                                  
            # dummy selection
            """
            if value == 'processDummy' and extrargs.processDummy and extrargs.runData and extrargs.run == '3':
                if extrargs.processDummy == "event":
                    config['d-q-event-selection-task']['processDummy'] = "true"
                if extrargs.processDummy == "filter":
                    config['d-q-filter-p-p-task']['processDummy'] = "true"
                if extrargs.processDummy == "barrel":
                    config['d-q-barrel-track-selection-task']['processDummy'] = "true"
            """
                    
            # dummy automizer #TODO: for transaction manag. we need logger for dummy
            if value == 'processDummy' and extrargs.autoDummy:
                
                if config["d-q-barrel-track-selection"]["processSelection"] == "true":
                    config["d-q-barrel-track-selection"]["processDummy"] = "false"
                if config["d-q-barrel-track-selection"]["processSelection"] == 'false':
                    config["d-q-barrel-track-selection"]["processDummy"] = "true"
                    
                if config["d-q-muons-selection"]["processSelection"] == "true":
                    config["d-q-muons-selection"]["processDummy"] = "false"
                if config["d-q-muons-selection"]["processSelection"] == "false":
                    config["d-q-muons-selection"]["processDummy"] = "true"
                    
                if config["d-q-event-selection-task"]["processEventSelection"] == "true":
                    config["d-q-event-selection-task"]["processDummy"] = "false"
                if config["d-q-event-selection-task"]["processEventSelection"] == "false":
                    config["d-q-event-selection-task"]["processDummy"] = "true"
                    
                if config["d-q-filter-p-p-task"]["processFilterPP"] =="true":
                    config["d-q-filter-p-p-task"]["processDummy"] = "false"
                if config["d-q-filter-p-p-task"]["processFilterPP"] == "false":
                    config["d-q-filter-p-p-task"]["processDummy"] = "true"
                
# Transaction Management for Most of Parameters for debugging, monitoring and logging
"""
for key,value in configuredCommands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
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
        #if key == 'isBarrelSelectionTiny' and (extrargs.runMC or extrargs.run == '2') and extrargs.isBarrelSelectionTiny: TODO: fix logger bug
            #print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        #if key == 'processDummy' and (extrargs.runMC or extrargs.run == '2'):
            #print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
"""

  
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
updatedConfigFileName = "tempConfigFilterPP.json"
with open(updatedConfigFileName,'w') as outputFile:
  json.dump(config, outputFile ,indent=2)

# Check which dependencies need to be run
depsToRun = {}
for dep in commonDeps:
  depsToRun[dep] = 1
      
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --severity error --shm-segment-size 12000000000 -b"
for dep in depsToRun.keys():
  commandToRun += " | " + dep + " --configuration json://" + updatedConfigFileName + " -b"

print("====================================================================================================================")
print("Command to run:")
print(commandToRun)
print("====================================================================================================================")

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