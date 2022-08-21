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
import logging
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
    
clist=[] # control list for type control
allValuesCfg = [] # counter for provided args
allCuts = [] # all analysis cuts
allPairCuts = [] # only pair cuts
nAddedAllCutsList = [] # e.g. muonQualityCuts::2
nAddedPairCutsList = [] # e.g paircutMass::3
SelsStyle1 = [] # track/muon cut::paircut::n
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

# For filterPP, Filter PP Process should always true. So you don't need configure it
dqSelections =  {"eventSelection" : "Run DQ event selection",
                 "barrelTrackSelection" : "Run DQ barrel track selection" ,
                 "muonSelection" : "Run DQ muon selection",
                 "barrelTrackSelectionTiny" : "Run DQ barrel track selection tiny",
                 "filterPPSelectionTiny" : "Run filter task tiny"
                 }

PIDSelections = {"el" : "Produce PID information for the Electron mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
                 "mu" : "Produce PID information for the Muon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)" ,
                 "pi" : "Produce PID information for the Pion mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
                 "ka" : "Produce PID information for the Kaon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
                 "pr" : "Produce PID information for the Proton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)", 
                 "de" : "Produce PID information for the Deuterons mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
                 "tr" : "Produce PID information for the Triton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
                 "he" : "Produce PID information for the Helium3 mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)",
                 "al" : "Produce PID information for the Alpha mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)"
                 }
PIDParameters = ["pid-el","pid-mu","pid-pi","pid-ka","pid-pr","pid-de","pid-tr","pid-he","pid-al"]

processDummySelections =["filter","event","barrel"]


###################
# Main Parameters #
###################
    
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='Arguments to pass')
parser.add_argument('cfgFileName', metavar='text', default='config.json', help='config file name')
parser.register('action', 'none', NoAction)
parser.register('action', 'store_choice', ChoicesAction)
#parser.add_argument('-runData', help="Run over data", action="store_true")
#parser.add_argument('-runMC', help="Run over MC", action="store_true")
parser.add_argument('--add_mc_conv', help="Add the converter from mcparticle to mcparticle+001", action="store_true")
parser.add_argument('--add_fdd_conv', help="Add the fdd converter", action="store_true")
parser.add_argument('--add_track_prop', help="Add track propagation to the innermost layer (TPC or ITS)", action="store_true")
parser.add_argument('--logFile', help="Enable logger for both file and CLI", action="store_true")

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
groupProcess = parser.add_argument_group(title='Choice List For filterPP Process')
ingredientsProcess = groupProcess.add_argument('--process',help="Process Selection options for FilterPP --> DQ Tasks (when a value added to parameter, processSelection is converted from false to true)", nargs='*',
                 action='store_choice',metavar='PROCESS')

for key,value in dqSelections.items():
    ingredientsProcess.add_choice(key, help=value)

# d-q-filter-p-p-task
#parser.add_argument('--cfgPairCuts', help="Space separated list of pair cuts", action="store", choices=allPairCuts, nargs='*', type=str, metavar='') # run3
parser.add_argument('--cfgBarrelSels', help="Configure Barrel Selection <track-cut>:[<pair-cut>]:<n>,[<track-cut>:[<pair-cut>]:<n>],... | example jpsiO2MCdebugCuts2::1 ",choices=allSels, action="store", type=str, nargs='*', metavar='') # run2 
parser.add_argument('--cfgMuonSels', help="Configure Muon Selection <muon-cut>:[<pair-cut>]:<n> example muonQualityCuts:pairNoCut:1",choices=allSels, action="store", type=str, nargs='*', metavar='') # run 2

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
groupPID = parser.add_argument_group(title='Choice List PID options')
ingredientsPID = groupPID.add_argument('--pid',help="Pid Selection options for TPC and TOF (when a value added to parameter, pid-<type> is converted from -1 to 1)", nargs='*',
                 action='store_choice',metavar='PID')

for key,value in PIDSelections.items():
    ingredientsPID.add_choice(key, help=value)

# helper lister commands
parser.add_argument('--cutLister', help="List all of the analysis cuts from CutsLibrary.h", action="store_true")

# debug options
parser.add_argument('--debug', help="execute with debug options", action="store", choices=["NOTSET","DEBUG","INFO","WARNING","ERROR","CRITICAL"], type=str.upper, default="INFO")


# TODO: We don't have options for this values. Discuss with ionut
# tof-pid-full, tof-pid for run3 ???
parser.add_argument('--isProcessEvTime', help="tof-pid -> processEvTime : Process Selection options true or false (string)", action="store", choices=['true','false'], type=str.lower)

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
    logging.error("Your forget assign a value to for this parameters: %s", forgetParams)
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
    
    loggerFile = "filterPP.log"
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

# add prefix for extrargs.process for TableMaker and Filter PP
#if extrargs.process != None:
    #prefix_process = "process"
    #extrargs.process = [prefix_process + sub for sub in extrargs.process]

# add prefix for extrargs.pid for pid selection
if extrargs.pid != None:
    prefix_pid = "pid-"
    extrargs.pid = [prefix_pid + sub for sub in extrargs.pid]
    
######################################################################################

#commonDeps = ["o2-analysis-timestamp", "o2-analysis-event-selection", "o2-analysis-multiplicity-table", "o2-analysis-trackselection", "o2-analysis-track-propagation", "o2-analysis-pid-tof-base", "o2-analysis-pid-tof", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]
commonDeps = ["o2-analysis-timestamp", "o2-analysis-event-selection", "o2-analysis-multiplicity-table", "o2-analysis-trackselection", "o2-analysis-trackextension", "o2-analysis-pid-tof-base", "o2-analysis-pid-tof", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]
#TODO we don't have o2-analysis-trackextension? we have track-prop. track-prop should be removed because we have add_track_prop option in interface.
 #e.g from tablemaker --> barrelDeps = ["o2-analysis-trackselection", "o2-analysis-trackextension","o2-analysis-pid-tof-base", "o2-analysis-pid-tof", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]



# Make some checks on provided arguments
if len(sys.argv) < 2:
  logging.error("Invalid syntax! The command line should look like this:")
  logging.info("  ./IFilterPP.py <yourConfig.json> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
config = {}
with open(sys.argv[1]) as configFile:
  config = json.load(configFile)

taskNameInConfig = "d-q-filter-p-p-task"
taskNameInCommandLine = "o2-analysis-dq-filter-pp"

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
                
            # DQ Selections for muons and barrel tracks #todo: need transcation mang. for barrel tiny and normal process
            if value =='processSelection' and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'process': #  Only Select key for analysis
                                      
                            if key == 'd-q-barrel-track-selection':                    
                                if 'barrelTrackSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'barrelTrackSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                      
                            if key == 'd-q-muons-selection':
                                if 'muonSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'muonSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                                                               
            # DQ Selections event    
            if value =='processEventSelection' and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'process': #  Only Select key for analysis
                            
                            if key == 'd-q-event-selection-task':
                                if 'eventSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'eventSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                    
            # DQ Tiny Selection for barrel track
            if value =='processSelectionTiny' and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'process': #  Only Select key for analysis
                                      
                            if key == 'd-q-barrel-track-selection':                    
                                if 'barrelTrackSelectionTiny' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'barrelTrackSelectionTiny' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
            
            # DQ Tiny Selection for filterPP
            if value =='processFilterPPTiny' and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'process': #  Only Select key for analysis
                                      
                            if key == 'd-q-filter-p-p-task':                    
                                if 'filterPPSelectionTiny' in valueCfg:
                                    config[key][value] = 'true'
                                    config[key]["processFilterPP"] = 'false'
                                    logging.debug(" - [%s] %s : true",key,value)
                                    logging.debug(" - [%s] processFilterPP : false",key)
                                if 'filterPPSelectionTiny' not in valueCfg:
                                    config[key][value] = 'false'
                                    config[key]["processFilterPP"] = 'true'
                                    logging.debug(" - [%s] %s : false",key,value)
                                    logging.debug(" - [%s] processFilterPP : true",key)
                                                                                                          
            # Filter PP Selections        
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
                
            # DQ Cuts    
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
            if value == 'cfgMuonsCuts' and extrargs.cfgMuonsCuts:
                if type(extrargs.cfgMuonsCuts) == type(clist):
                    extrargs.cfgMuonsCuts = listToString(extrargs.cfgMuonsCuts) 
                config[key][value] = extrargs.cfgMuonsCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonsCuts) 
            
            # QA Options  
            if value == 'cfgWithQA' and extrargs.cfgWithQA:
                config[key][value] = extrargs.cfgWithQA
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgWithQA)  

                                    
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
                                                    
            # processEvTime    
            if value == 'processEvTime':
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