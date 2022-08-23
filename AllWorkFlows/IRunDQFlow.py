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
ListToString provides converts lists to strings with commas.
This function is written to save as string type instead of list 

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
"""
stringToList provides converts strings to list with commas.
This function is written to save as list type instead of string 

Parameters
------------------------------------------------
s: list
A simple Python String
"""    
def stringToList(string):
    li = list(string.split(","))
    return li

class NoAction(argparse.Action):
    def __init__(self, **kwargs):
        kwargs.setdefault('default', argparse.SUPPRESS)
        kwargs.setdefault('nargs', 0)
        super(NoAction, self).__init__(**kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        pass

class ChoicesAction(argparse._StoreAction):
    def add_choice(self, choice, help=''):
        if self.choices is None:
            self.choices = []
        self.choices.append(choice)
        self.container.add_argument(choice, help=help, action='none')
        
class ChoicesCompleterList(object):
    def __init__(self, choices):
        self.choices = list(choices)        
    def __call__(self, **kwargs):
        return self.choices
        
###################################
# Interface Predefined Selections #
###################################

centralityTableSelections = {
    "V0M" : "Produces centrality percentiles using V0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "Run2SPDtks" :"Produces Run2 centrality percentiles using SPD tracklets multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "Run2SPDcls" :"Produces Run2 centrality percentiles using SPD clusters multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "Run2CL0" :"Produces Run2 centrality percentiles using CL0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)",
    "Run2CL1" : "Produces Run2 centrality percentiles using CL1 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)"
}

centralityTableSelectionsList = []
for k,v in centralityTableSelections.items():
    centralityTableSelectionsList.append(k)
    
centralityTableParameters = ["estV0M", "estRun2SPDtks","estRun2SPDcls","estRun2CL0","estRun2CL1"]
PIDSelections = {
    "el" : "Produce PID information for the Electron mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "mu" : "Produce PID information for the Muon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)" ,
    "pi" : "Produce PID information for the Pion mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "ka" : "Produce PID information for the Kaon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "pr" : "Produce PID information for the Proton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)", 
    "de" : "Produce PID information for the Deuterons mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "tr" : "Produce PID information for the Triton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "he" : "Produce PID information for the Helium3 mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
    "al" : "Produce PID information for the Alpha mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)"
}
PIDSelectionsList = []
for k,v in PIDSelections.items():
    PIDSelectionsList.append(k)
    
PIDParameters = ["pid-el","pid-mu","pid-pi","pid-ka","pid-pr","pid-de","pid-tr","pid-he","pid-al"]

collisionSystemSelections = ["PbPb", "pp", "pPb", "Pbp", "XeXe"]

booleanSelections = ["true","false"]

debugLevelSelections = {
    "NOTSET" : "Set Debug Level to NOTSET",
    "DEBUG" : "Set Debug Level to DEBUG",
    "INFO" : "Set Debug Level to INFO",
    "WARNING" : "Set Debug Level to WARNING",
    "ERROR" : "Set Debug Level to ERROR", 
    "CRITICAL" : "Set Debug Level to CRITICAL"
}
debugLevelSelectionsList = []
for k,v in debugLevelSelections.items():
    debugLevelSelectionsList.append(k)

eventMuonSelections = ["0","1","2"]
    
clist=[] # control list for type control
allValuesCfg = [] # counter for provided args
allCuts = [] # all analysis cuts

# Get system variables in alienv. In alienv we don't have cuts and signal library!!! We need discuss this thing
O2DPG_ROOT=os.environ.get('O2DPG_ROOT')
QUALITYCONTROL_ROOT=os.environ.get('QUALITYCONTROL_ROOT')
O2_ROOT=os.environ.get('O2_ROOT')
O2PHYSICS_ROOT=os.environ.get('O2PHYSICS_ROOT')

threeSelectedList = []

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
with open('tempCutsLibrary.h') as f:
    for line in f:
        stringIfSearch = [x for x in f if 'if' in x] 
        for i in stringIfSearch:
            getAnalysisCuts = re.findall('"([^"]*)"', i)
            allCuts = allCuts + getAnalysisCuts

 
#print(allCuts)
#print(allMixing)  


###################
# Main Parameters #
###################
    
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='Arguments to pass')
groupCoreSelections = parser.add_argument_group(title='Core configurations that must be configured')
groupCoreSelections.add_argument('cfgFileName', metavar='Config.json', default='config.json', help='config JSON file name')
parser.register('action', 'none', NoAction)
parser.register('action', 'store_choice', ChoicesAction)
groupTaskAdders = parser.add_argument_group(title='Additional Task Adding Options')
groupTaskAdders .add_argument('--add_mc_conv', help="Add the converter from mcparticle to mcparticle+001 (Adds your workflow o2-analysis-mc-converter task)", action="store_true")
groupTaskAdders .add_argument('--add_fdd_conv', help="Add the fdd converter (Adds your workflow o2-analysis-fdd-converter task)", action="store_true")
groupTaskAdders .add_argument('--add_track_prop', help="Add track propagation to the innermost layer (TPC or ITS) (Adds your workflow o2-analysis-track-propagation task)", action="store_true")

##################
# Interface Part #
##################

# aod
groupDPLReader = parser.add_argument_group(title='Data processor options: internal-dpl-aod-reader')
groupDPLReader .add_argument('--aod', help="Add your AOD File with path", action="store", type=str)

groupAutomations = parser.add_argument_group(title='Automation Parameters')
groupAutomations.add_argument('--autoDummy', help="Dummy automize parameter (don't configure it, true is highly recomended for automation)", action="store", default='true', type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# event-selection-task
groupEventSelection = parser.add_argument_group(title='Data processor options: event-selection-task')
groupEventSelection.add_argument('--syst', help="Collision System Selection ex. pp", action="store", type=str, choices=collisionSystemSelections).completer = ChoicesCompleter(collisionSystemSelections)
groupEventSelection.add_argument('--muonSelection', help="0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts", action="store", type=str, choices=eventMuonSelections).completer = ChoicesCompleter(eventMuonSelections)
groupEventSelection.add_argument('--customDeltaBC', help="custom BC delta for FIT-collision matching", action="store", type=str)

#tof-pid-beta
groupTofPidBeta = parser.add_argument_group(title='Data processor options: tof-pid-beta')
groupTofPidBeta.add_argument('--tof-expreso', help="Expected resolution for the computation of the expected beta", action="store", type=str)

# DQ Flow Task Selections
GroupAnalysisQvector = parser.add_argument_group(title='Data processor options: analysis-qvector')
GroupAnalysisQvector.add_argument('--cfgTrackCuts', help="Space separated list of barrel track cuts", choices=allCuts,nargs='*', action="store", type=str, metavar='CFGTRACKCUTS').completer = ChoicesCompleterList(allCuts)
GroupAnalysisQvector.add_argument('--cfgMuonCuts', help="Space separated list of muon cuts in d-q muons selection", action="store", choices=allCuts, nargs='*', type=str, metavar='CFGMUONCUTS').completer = ChoicesCompleterList(allCuts)
GroupAnalysisQvector.add_argument('--cfgEventCuts', help="Space separated list of event cuts", choices=allCuts, nargs='*', action="store", type=str, metavar='CFGEVENTCUT').completer = ChoicesCompleterList(allCuts)
GroupAnalysisQvector.add_argument('--cfgWithQA', help="If true, fill QA histograms", action="store", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
GroupAnalysisQvector.add_argument('--cfgCutPtMin', help="Minimal pT for tracks", action="store", type=str, metavar='CFGCUTPTMIN')
GroupAnalysisQvector.add_argument('--cfgCutPtMax', help="Maximal pT for tracks", action="store", type=str, metavar='CFGCUTPTMAX')
GroupAnalysisQvector.add_argument('--cfgCutEta', help="Eta range for tracks", action="store", type=str, metavar='CFGCUTETA')
GroupAnalysisQvector.add_argument('--cfgEtaLimit', help="Eta gap separation, only if using subEvents", action="store", type=str, metavar='CFGETALIMIT')
GroupAnalysisQvector.add_argument('--cfgNPow', help="Power of weights for Q vector", action="store", type=str, metavar='CFGNPOW')

GroupAnalysisQvector.add_argument('--cfgEfficiency', help="CCDB path to efficiency object", action="store", type=str)
GroupAnalysisQvector.add_argument('--cfgAcceptance', help="CCDB path to acceptance object", action="store", type=str)
GroupAnalysisQvector.add_argument('--ccdb-url', help="url of the ccdb repository", action="store", type=str, metavar='')
GroupAnalysisQvector.add_argument('--ccdbPath', help="base path to the ccdb object", action="store", type=str, metavar='')

# centrality-table
groupCentralityTable = parser.add_argument_group(title='Data processor options: centrality-table')
groupCentralityTable.add_argument('--est', help="Produces centrality percentiles parameters", action="store", nargs="*", type=str, metavar='EST', choices=centralityTableSelectionsList).completer = ChoicesCompleterList(centralityTableSelectionsList)
groupEst = parser.add_argument_group(title='Choice List centrality-table Parameters (when a value added to parameter, value is converted from -1 to 1)')

for key,value in centralityTableSelections.items():
    groupEst.add_argument(key, help=value, action='none')

# pid
groupPID = parser.add_argument_group(title='Data processor options: tof-pid, tpc-pid, tpc-pid-full')
groupPID.add_argument('--pid', help="Produce PID information for the <particle> mass hypothesis", action="store", nargs='*', type=str.lower, metavar='PID', choices=PIDSelectionsList).completer = ChoicesCompleterList(PIDSelectionsList)

for key,value in PIDSelections.items():
    groupPID.add_argument(key, help=value, action = 'none')

# helper lister commands
groupAdditionalHelperCommands = parser.add_argument_group(title='Additional Helper Command Options')
groupAdditionalHelperCommands.add_argument('--cutLister', help="List all of the analysis cuts from CutsLibrary.h", action="store_true")

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
    logging.error("Your forget assign a value to for this parameters: ", forgetParams)
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
    
    loggerFile = "DQFlow.log"
    if os.path.isfile(loggerFile) == True:
        os.remove(loggerFile)
    
    fh = handlers.RotatingFileHandler(loggerFile, maxBytes=(1048576*5), backupCount=7, mode='w')
    fh.setFormatter(format)
    log.addHandler(fh)

###################
# HELPER MESSAGES #
###################
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

######################
# PREFIX ADDING PART #
###################### 

# add prefix for extrargs.pid for pid selection
if extrargs.pid != None:
    prefix_pid = "pid-"
    extrargs.pid = [prefix_pid + sub for sub in extrargs.pid]
    
# add prefix for extrargs.est for centrality table
if extrargs.est != None:
    prefix_est = "est"
    extrargs.est = [prefix_est + sub for sub in extrargs.est]
    
######################################################################################

commonDeps = ["o2-analysis-timestamp", "o2-analysis-event-selection", "o2-analysis-multiplicity-table","o2-analysis-centrality-table", "o2-analysis-trackselection", "o2-analysis-trackextension", "o2-analysis-pid-tof-base", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]
#o2-analysis-timestamp - b| o2-analysis-event-selection -b | o2-analysis-multiplicity-table -b | o2-analysis-centrality-table -b | o2-analysis-trackselection -b | o2-analysis-trackextension -b | o2-analysis-pid-tpc-full -b | o2-analysis-pid-tof-full -b | o2-analysis-pid-tof-base -b | o2-analysis-pid-tof-beta -b
#| o2-analysis-dq-flow -b
#| o2-analysis-fdd-converter -b

# Make some checks on provided arguments
if len(sys.argv) < 2:
  logging.error("Invalid syntax! The command line should look like this:")
  logging.info("  ./IRunDQFlow.py <yourConfig.json> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
config = {}
with open(sys.argv[1]) as configFile:
  config = json.load(configFile)

taskNameInConfig = "analysis-qvector"
taskNameInCommandLine = "o2-analysis-dq-flow"

if not taskNameInConfig in config:
  logging.error("%s Task to be run not found in the configuration file!", taskNameInConfig)
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
                                                                                                     
            # analysis-qvector selections      
            if value == 'cfgTrackCuts' and extrargs.cfgTrackCuts:
                if type(extrargs.cfgTrackCuts) == type(clist):
                    extrargs.cfgTrackCuts = listToString(extrargs.cfgTrackCuts) 
                config[key][value] = extrargs.cfgTrackCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgTrackCuts)
            if value == 'cfgMuonCuts' and extrargs.cfgMuonCuts:
                if type(extrargs.cfgMuonCuts) == type(clist):
                    extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts) 
                config[key][value] = extrargs.cfgMuonCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonCuts)
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts) 
                config[key][value] = extrargs.cfgEventCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgEventCuts)
            if value == 'cfgWithQA' and extrargs.cfgWithQA:
                config[key][value] = extrargs.cfgWithQA  
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgWithQA)
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
  
# AOD File checker from only interface TODO: We need also checker from JSON 
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

        
        
#elif os.path.isfile((config["internal-dpl-aod-reader"]["aod-file"])) == False:
        #print("[ERROR]",config["internal-dpl-aod-reader"]["aod-file"],"File not found in path!!!")
        #sys.exit()

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

# Listing Added Commands
logging.info("Args provided configurations List")
print("====================================================================================================================")
for key,value in configuredCommands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
        logging.info("--%s : %s ",key,value)

os.system(commandToRun)