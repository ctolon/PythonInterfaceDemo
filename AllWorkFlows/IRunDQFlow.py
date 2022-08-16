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
from urllib.request import Request, urlopen

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

# Get system variables in alienv. In alienv we don't have cuts and signal library!!! We need discuss this thing
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
    
    # HTTP Request
    requestCutsLibrary = Request(urlCutsLibrary, headers=headers)
    requestMCSignalsLibrary = Request(urlMCSignalsLibrary, headers=headers)
    requestEventMixing  = Request(urlEventMixing , headers=headers)
    
    # Get Files With Http Requests
    htmlCutsLibrary = urlopen(requestCutsLibrary).read()
    htmlMCSignalsLibrary = urlopen(requestMCSignalsLibrary).read()
    htmlEventMixing = urlopen(requestEventMixing ).read()
     
    # Save Disk to temp DQ libs  
    with open('tempCutsLibrary.h', 'wb') as f:
         f.write(htmlCutsLibrary)
    with open('tempMCSignalsLibrary.h', 'wb') as f:
         f.write(htmlMCSignalsLibrary)
    with open('tempMixingLibrary.h', 'wb') as f:
        f.write(htmlEventMixing)

# Read Cuts, Signals, Mixing vars from downloaded files    
with open('tempCutsLibrary.h') as f:
    for line in f:
        stringIfSearch = [x for x in f if 'if' in x] 
        for i in stringIfSearch:
            getAnalysisCuts = re.findall('"([^"]*)"', i)
            allCuts = allCuts + getAnalysisCuts

 
#print(allCuts)
#print(allMixing)  


###################################
# Interface Predefined Selections #
###################################

# For filterPP, Filter PP Process should always true
#dqSelections = ["eventSelection","barrelTrackSelection","muonSelection","barrelTrackSelectionTiny","filterPPSelectionTiny"]

PIDSelections = ["el","mu","pi","ka","pr","de","tr","he","al"]
PIDParameters = ["pid-el","pid-mu","pid-pi","pid-ka","pid-pr","pid-de","pid-tr","pid-he","pid-al"]

#processDummySelections =["filter","event","barrel"]


###################
# Main Parameters #
###################
    
parser = argparse.ArgumentParser(description='Arguments to pass')
parser.add_argument('cfgFileName', metavar='text', default='config.json', help='config file name')
#parser.add_argument('-runData', help="Run over data", action="store_true")
#parser.add_argument('-runMC', help="Run over MC", action="store_true")
parser.add_argument('--add_mc_conv', help="Add the converter from mcparticle to mcparticle+001", action="store_true")
parser.add_argument('--add_fdd_conv', help="Add the fdd converter", action="store_true")
parser.add_argument('--add_track_prop', help="Add track propagation to the innermost layer (TPC or ITS)", action="store_true")

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

# DQ Flow Task Selections
#parser.add_argument('--process', help="DQ Task Selections",choices=dqSelections, action="store", type=str,  nargs='*', metavar='') # run2 
parser.add_argument('--cfgTrackCuts', help="Space separated list of barrel track cuts", choices=allCuts,nargs='*', action="store", type=str, metavar='')
parser.add_argument('--cfgMuonCuts', help="Space separated list of muon cuts in d-q muons selection", action="store", choices=allCuts, nargs='*', type=str, metavar='')
parser.add_argument('--cfgEventCuts', help="Space separated list of event cuts", choices=allCuts, nargs='*', action="store", type=str, metavar='')
parser.add_argument('--cfgWithQA', help="If true, fill QA histograms", action="store", choices=['true','false'], type=str.lower)
parser.add_argument('--cfgCutPtMin', help="Minimal pT for tracks", action="store", type=str, metavar='')
parser.add_argument('--cfgCutPtMax', help="Maximal pT for tracks", action="store", type=str, metavar='')
parser.add_argument('--cfgCutEta', help="Eta range for tracks", action="store", type=str, metavar='')
parser.add_argument('--cfgEtaLimit', help="Eta gap separation, only if using subEvents", action="store", type=str, metavar='')
parser.add_argument('--cfgNPow', help="Power of weights for Q vector", action="store", type=str, metavar='')

parser.add_argument('--cfgEfficiency', help="CCDB path to efficiency object", action="store", type=str)
parser.add_argument('--cfgAcceptance', help="CCDB path to acceptance object", action="store", type=str)
#parser.add_argument('--ccdb-url', help="url of the ccdb repository", action="store", type=str, metavar='')
#parser.add_argument('--ccdbPath', help="base path to the ccdb object", action="store", type=str, metavar='')

# pid
parser.add_argument('--pid', help="Produce PID information for the particle mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)", action="store", choices=PIDSelections, nargs='*', type=str.lower)

# helper lister commands
parser.add_argument('--cutLister', help="List all of the analysis cuts from CutsLibrary.h", action="store_true")

# tof-pid-full, tof-pid for run3 ???
#parser.add_argument('--isProcessEvTime', help="tof-pid -> processEvTime : Process Selection options true or false (string)", action="store", choices=['true','false'], type=str.lower)

# timestamp-task
#parser.add_argument('--isRun2MC', help="Selection the Process is MC or Not", action="store", choices=['true','false'], type=str)

#parser.add_argument('--processFilterPPTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3


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

commonDeps = ["o2-analysis-timestamp", "o2-analysis-event-selection", "o2-analysis-multiplicity-table","o2-analysis-centrality-table", "o2-analysis-trackselection", "o2-analysis-trackextension", "o2-analysis-pid-tof-base", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]
#o2-analysis-timestamp - b| o2-analysis-event-selection -b | o2-analysis-multiplicity-table -b | o2-analysis-centrality-table -b | o2-analysis-trackselection -b | o2-analysis-trackextension -b | o2-analysis-pid-tpc-full -b | o2-analysis-pid-tof-full -b | o2-analysis-pid-tof-base -b | o2-analysis-pid-tof-beta -b
#| o2-analysis-dq-flow -b
#| o2-analysis-fdd-converter -b



# Make some checks on provided arguments
if len(sys.argv) < 2:
  print("ERROR: Invalid syntax! The command line should look like this:")
  print("  ./IRunDQFlow.py <yourConfig.json> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
config = {}
with open(sys.argv[1]) as configFile:
  config = json.load(configFile)

taskNameInConfig = "analysis-qvector"
taskNameInCommandLine = "o2-analysis-dq-flow"

if not taskNameInConfig in config:
  print("[ERROR] ",taskNameInConfig," Task to be run not found in the configuration file!")
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

                                                                                                          
            # DQ Flow Selections        
            if value == 'cfgTrackCuts' and extrargs.cfgTrackCuts:
                if type(extrargs.cfgTrackCuts) == type(clist):
                    extrargs.cfgTrackCuts = listToString(extrargs.cfgTrackCuts) 
                config[key][value] = extrargs.cfgTrackCuts
            if value == 'cfgMuonCuts' and extrargs.cfgMuonCuts:
                if type(extrargs.cfgMuonCuts) == type(clist):
                    extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts) 
                config[key][value] = extrargs.cfgMuonCuts
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts) 
                config[key][value] = extrargs.cfgEventCuts
            if value == 'cfgWithQA' and extrargs.cfgWithQA:
                config[key][value] = extrargs.cfgWithQA  
            if value =='cfgCutPtMin' and extrargs.cfgCutPtMin:
                config[key][value] = extrargs.cfgCutPtMin
            if value =='cfgCutPtMax' and extrargs.cfgCutPtMax:
                config[key][value] = extrargs.cfgCutPtMax
            if value =='cfgCutEta' and extrargs.cfgCutEta:
                config[key][value] = extrargs.cfgCutEta
            if value =='cfgEtaLimit' and extrargs.cfgEtaLimit:
                config[key][value] = extrargs.cfgEtaLimit
            if value =='cfgNPow' and extrargs.cfgNPow:
                config[key][value] = extrargs.cfgNPow
            if value =='cfgEtaLimit' and extrargs.cfgEtaLimit:
                config[key][value] = extrargs.cfgEtaLimit
            if value =='cfgNPow' and extrargs.cfgNPow:
                config[key][value] = extrargs.cfgNPow
            if value =='cfgEfficiency' and extrargs.cfgEfficiency:
                config[key][value] = extrargs.cfgEfficiency
            if value =='cfgAcceptance' and extrargs.cfgAcceptance:
                config[key][value] = extrargs.cfgAcceptance
                                                      
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
                                                    
            # processEvTime 
            """  
            if value == 'processEvTime':
                if extrargs.isProcessEvTime == "true":
                    config[key][value] = "true"
                    config[key]["processNoEvTime"] = "false"
                if extrargs.isProcessEvTime == "false":
                    config[key][value] = "false"
                    config[key]["processNoEvTime"] = "true"
            """
                                                  
            # dummy selection
            """
            if value == 'processDummy' and extrargs.processDummy and extrargs.runData and extrargs.run == '3':
                if extrargs.processDummy == "event":
                    config['d-q-event-selection-task']['processDummy'] = "true"
            """
                    
            # dummy automizer #TODO: for transaction manag. we need logger for dummy
            """
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
            """
                
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
updatedConfigFileName = "tempConfigDQFlow.json"
with open(updatedConfigFileName,'w') as outputFile:
  json.dump(config, outputFile ,indent=2)

# Check which dependencies need to be run
depsToRun = {}
for dep in commonDeps:
  depsToRun[dep] = 1
      
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --severity error --shm-segment-size 12000000000 -b"
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

# Listing Added Commands
print("Args provided configurations List")
print("====================================================================================================================")
for key,value in configuredCommands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
        print("--"+key,":", value)

os.system(commandToRun)