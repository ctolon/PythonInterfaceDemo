#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*- 
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

# Orginal Task: https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Tasks/filterPP.cxx

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

# For filterPP, Filter PP Process should always true. So you don"t need configure it
dqSelections = {
    "eventSelection": "Run DQ event selection",
    "barrelTrackSelection": "Run DQ barrel track selection",
    "muonSelection": "Run DQ muon selection",
    "barrelTrackSelectionTiny": "Run DQ barrel track selection tiny",
    "filterPPSelectionTiny": "Run filter task tiny"
}
dqSelectionsList = []
for k, v in dqSelections.items():
    dqSelectionsList.append(k)

ft0Selections = ["FT0", "NoFT0", "OnlyFT0", "Run2"]

ft0Parameters = ["processFT0", "processNoFT0", "processOnlyFT0", "processRun2"]

V0SelectorParameters = [
    "d_bz",
    "v0cospa",
    "dcav0dau",
    "v0RMin",
    "v0Rmax",
    "dcamin",
    "dcamax,mincrossedrows",
    "maxchi2tpc"
]

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

processDummySelections = ["filter", "event", "barrel"]

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

processDummySelections = ["filter", "event", "barrel"]

clist = []  # control list for type control
allValuesCfg = []  # counter for provided args
allAnalysisCuts = []  # all analysis cuts
allPairCuts = []  # only pair cuts
nAddedallAnalysisCutsList = []  # e.g. muonQualityCuts:2
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

# Get system variables in alienv. In alienv we don"t have cuts and signal library!!! We need discuss this thing
O2DPG_ROOT = os.environ.get("O2DPG_ROOT")
QUALITYCONTROL_ROOT = os.environ.get("QUALITYCONTROL_ROOT")
O2_ROOT = os.environ.get("O2_ROOT")
O2PHYSICS_ROOT = os.environ.get("O2PHYSICS_ROOT")

threeSelectedList = []

################################
# Download DQ Libs From Github #
################################

# It works on for only master branch

# header for github download
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}

URL_CUTS_LIBRARY = "https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/CutsLibrary.h?raw=true"
URL_MCSIGNALS_LIBRARY = "https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/MCSignalLibrary.h?raw=true"
URL_MIXING_LIBRARY = "https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/MixingLibrary.h?raw=true"

 
# Github Links for CutsLibrary and MCSignalsLibrary from PWG-DQ --> download from github
# This condition solves performance issues    
if not (os.path.isfile("tempCutsLibrary.h") or os.path.isfile("tempMCSignalsLibrary.h") or os.path.isfile("tempMixingLibrary.h")):
    print("[INFO] Some Libs are Missing. They will download.")
    
    # Dummy SSL Adder
    context = ssl._create_unverified_context()  # prevent ssl problems
    request = urllib.request.urlopen(URL_CUTS_LIBRARY, context=context)
    
    # HTTP Request
    requestCutsLibrary = Request(URL_CUTS_LIBRARY, headers=headers)
    requestMCSignalsLibrary = Request(URL_MCSIGNALS_LIBRARY, headers=headers)
    requestMixingLibrary  = Request(URL_MIXING_LIBRARY , headers=headers)
    
    # Get Files With Http Requests
    htmlCutsLibrary = urlopen(requestCutsLibrary, context=context).read()
    htmlMCSignalsLibrary = urlopen(requestMCSignalsLibrary, context=context).read()
    htmlMixingLibrary = urlopen(requestMixingLibrary, context=context).read()
    
   # Save Disk to temp DQ libs  
    with open("tempCutsLibrary.h", "wb") as f:
         f.write(htmlCutsLibrary)
    with open("tempMCSignalsLibrary.h", "wb") as f:
         f.write(htmlMCSignalsLibrary)
    with open("tempMixingLibrary.h", "wb") as f:
        f.write(htmlMixingLibrary)

# Read Cuts, Signals, Mixing vars from downloaded files            
with open("tempCutsLibrary.h") as f:
    for line in f:
        stringIfSearch = [x for x in f if 'if' in x]  # get lines only includes if string
        for i in stringIfSearch:
            getAnalysisCuts = re.findall('"([^"]*)"', i)  # get in double quotes string value with regex exp.
            getPairCuts = [y for y in getAnalysisCuts         # get pair cuts
                        if "pair" in y] 
            if getPairCuts: # if pair cut list is not empty
                allPairCuts = allPairCuts + getPairCuts # Get Only pair cuts from CutsLibrary.h
                namespacedPairCuts = [x + oneColon for x in allPairCuts] # paircut:
            allAnalysisCuts = allAnalysisCuts + getAnalysisCuts # Get all Cuts from CutsLibrary.h
            nameSpacedallAnalysisCuts = [x + oneColon for x in allAnalysisCuts] # cut:
            nameSpacedallAnalysisCutsTwoDots = [x + doubleColon for x in allAnalysisCuts]  # cut::

# in Filter PP Task, sels options for barrel and muon uses namespaces e.g. "<track-cut>:[<pair-cut>]:<n> and <track-cut>::<n> For Manage this issue:
for k in range (1,10):
    nAddedallAnalysisCuts = [x + str(k) for x in nameSpacedallAnalysisCutsTwoDots]
    nAddedallAnalysisCutsList = nAddedallAnalysisCutsList + nAddedallAnalysisCuts
    nAddedPairCuts = [x + str(k) for x in namespacedPairCuts]
    nAddedPairCutsList = nAddedPairCutsList + nAddedPairCuts
    
# Style 1 <track-cut>:[<pair-cut>]:<n>:
for i in nAddedPairCutsList:
    Style1 = [x + i for x in nameSpacedallAnalysisCuts]
    selsWithOneColon = selsWithOneColon + Style1
      
# Style 2 <track-cut>:<n> --> nAddedallAnalysisCutsList

# Merge All possible styles for Sels (cfgBarrelSels and cfgMuonSels) in FilterPP Task
allSels = selsWithOneColon + nAddedallAnalysisCutsList


###################
# Main Parameters #
###################
    
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description="Arguments to pass")
groupCoreSelections = parser.add_argument_group(title="Core configurations that must be configured")
groupCoreSelections.add_argument("cfgFileName", metavar="Config.json", default="config.json", help="config JSON file name")
parser.register("action", "none", NoAction)
parser.register("action", "store_choice", ChoicesAction)
groupTaskAdders = parser.add_argument_group(title="Additional Task Adding Options")
groupTaskAdders.add_argument("--add_mc_conv", help="Add the converter from mcparticle to mcparticle+001 (Adds your workflow o2-analysis-mc-converter task)", action="store_true")
groupTaskAdders.add_argument("--add_fdd_conv", help="Add the fdd converter (Adds your workflow o2-analysis-fdd-converter task)", action="store_true")
groupTaskAdders.add_argument("--add_track_prop", help="Add track propagation to the innermost layer (TPC or ITS) (Adds your workflow o2-analysis-track-propagation task)", action="store_true")

##################
# Interface Part #
##################

# aod
groupDPLReader = parser.add_argument_group(title="Data processor options: internal-dpl-aod-reader")
groupDPLReader .add_argument("--aod", help="Add your AOD File with path", action="store", type=str)

groupAutomations = parser.add_argument_group(title="Automation Parameters")
groupAutomations.add_argument("--autoDummy", help="Dummy automize parameter (don't configure it, true is highly recomended for automation)", action="store", default="true", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
groupAutomations.add_argument("--onlySelect", help="If false JSON Overrider Interface If true JSON Additional Interface", action="store", default="true", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# event-selection-task
groupEventSelection = parser.add_argument_group(title="Data processor options: event-selection-task")
groupEventSelection.add_argument("--syst", help="Collision System Selection ex. pp", action="store", type=str, choices=collisionSystemSelections).completer = ChoicesCompleter(collisionSystemSelections)
groupEventSelection.add_argument("--muonSelection", help="0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts", action="store", type=str, choices=eventMuonSelections).completer = ChoicesCompleter(eventMuonSelections)
groupEventSelection.add_argument("--customDeltaBC", help="custom BC delta for FIT-collision matching", action="store", type=str)

# multiplicity-table
groupMultiplicityTable = parser.add_argument_group(title="Data processor options: multiplicity-table")
groupMultiplicityTable.add_argument("--isVertexZeq", help="if true: do vertex Z eq mult table", action="store", type=str.lower, choices=(booleanSelections)).completer = ChoicesCompleter(booleanSelections)

# tof-pid, tof-pid-full
groupTofPid = parser.add_argument_group(title="Data processor options: tof-pid, tof-pid-full")
groupTofPid.add_argument("--isWSlice", help="Process with track slices", action="store",type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
groupTofPid.add_argument("--enableTimeDependentResponse", help="Flag to use the collision timestamp to fetch the PID Response", action="store",type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

#tof-pid-beta
groupTofPidBeta = parser.add_argument_group(title="Data processor options: tof-pid-beta")
groupTofPidBeta.add_argument("--tof-expreso", help="Expected resolution for the computation of the expected beta", action="store", type=str)

# tof-event-time
groupTofEventTime = parser.add_argument_group(title="Data processor options: tof-event-time")
groupTofEventTime.add_argument("--FT0", help="FT0: Process with FT0, NoFT0: Process without FT0, OnlyFT0: Process only with FT0, Run2: Process with Run2 data", action="store", type=str, choices=ft0Selections).completer = ChoicesCompleter(ft0Selections)

# DQ Task Selections
groupProcessFilterPP= parser.add_argument_group(title="Data processor options: d-q-filter-p-p-task, d-q-event-selection-task, d-q-barrel-track-selection, d-q-muons-selection ")
groupProcessFilterPP.add_argument("--process",help="DQ Tasks process Selections options", action="store", type=str, nargs="*", metavar="PROCESS", choices=dqSelectionsList).completer = ChoicesCompleterList(dqSelectionsList)

for key,value in dqSelections.items():
    groupProcessFilterPP.add_argument(key, help=value, action="none")

# d-q-filter-p-p-task
groupDQFilterPP = parser.add_argument_group(title="Data processor options: d-q-filter-p-p-task")
groupDQFilterPP.add_argument("--cfgBarrelSels", help="Configure Barrel Selection <track-cut>:[<pair-cut>]:<n>,[<track-cut>:[<pair-cut>]:<n>],... | example jpsiO2MCdebugCuts2::1 ", action="store", type=str,nargs="*", metavar="CFGBARRELSELS", choices=allSels).completer = ChoicesCompleterList(allSels)
groupDQFilterPP.add_argument("--cfgMuonSels", help="Configure Muon Selection <muon-cut>:[<pair-cut>]:<n> example muonQualityCuts:pairNoCut:1", action="store", type=str,nargs="*", metavar="CFGMUONSELS", choices=allSels).completer = ChoicesCompleterList(allSels)

## d-q-event-selection-task
groupDQEventSelection = parser.add_argument_group(title="Data processor options: d-q-event-selection-task")
groupDQEventSelection.add_argument("--cfgEventCuts", help="Space separated list of event cuts", nargs="*", action="store", type=str, metavar="CFGEVENTCUTS", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)

## d-q-barrel-track-selection
groupDQBarrelTrackSelection = parser.add_argument_group(title="Data processor options: d-q-barrel-track-selection")
groupDQBarrelTrackSelection.add_argument("--cfgBarrelTrackCuts", help="Space separated list of barrel track cuts", nargs="*", action="store", type=str, metavar="CFGBARRELTRACKCUTS", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)

## d-q-muons-selection
groupDQMuonsSelection = parser.add_argument_group(title="Data processor options: d-q-muons-selection")
groupDQMuonsSelection.add_argument("--cfgMuonsCuts", help="Space separated list of muon cuts in d-q muons selection", action="store", nargs="*", type=str, metavar="CFGMUONSCUT", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)

#all d-q tasks and selections
groupQASelections = parser.add_argument_group(title="Data processor options: d-q-barrel-track-selection-task, d-q-muons-selection, d-q-event-selection-task, d-q-filter-p-p-task")
groupQASelections.add_argument("--cfgWithQA", help="If true, fill QA histograms", action="store", type=str.lower, choices=(booleanSelections)).completer = ChoicesCompleter(booleanSelections)

# pid
groupPID = parser.add_argument_group(title="Data processor options: tpc-pid-full, tof-pid-full")
groupPID.add_argument("--pid", help="Produce PID information for the <particle> mass hypothesis", action="store", nargs="*", type=str.lower, metavar="PID", choices=pidSelectionsList).completer = ChoicesCompleterList(pidSelectionsList)

for key,value in pidSelections.items():
    groupPID.add_argument(key, help=value, action = "none")
    
# helper lister commands
groupAdditionalHelperCommands = parser.add_argument_group(title="Additional Helper Command Options")
groupAdditionalHelperCommands.add_argument("--cutLister", help="List all of the analysis cuts from CutsLibrary.h", action="store_true")

# debug options
groupAdditionalHelperCommands.add_argument("--debug", help="execute with debug options", action="store", type=str.upper, default="INFO", choices=debugLevelSelectionsList).completer = ChoicesCompleterList(debugLevelSelectionsList)
groupAdditionalHelperCommands.add_argument("--logFile", help="Enable logger for both file and CLI", action="store_true")
groupDebug= parser.add_argument_group(title="Choice List for debug Parameters")

for key,value in debugLevelSelections.items():
    groupDebug.add_argument(key, help=value, action="none")

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
    logging.error("Your forget assign a value to for this parameters: %s", forgetParams)
    sys.exit()
    
# Debug Settings
if extrargs.debug and (not extrargs.logFile):
    DEBUG_SELECTION = extrargs.debug
    numeric_level = getattr(logging, DEBUG_SELECTION.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % DEBUG_SELECTION)
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=DEBUG_SELECTION)
    
if extrargs.logFile and extrargs.debug:
    log = logging.getLogger("")
    level = logging.getLevelName(extrargs.debug)
    log.setLevel(level)
    format = logging.Formatter("%(asctime)s - [%(levelname)s] %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(format)
    log.addHandler(ch)
    
    loggerFile = "filterPP.log"
    if os.path.isfile(loggerFile):
        os.remove(loggerFile)
    
    fh = handlers.RotatingFileHandler(loggerFile, maxBytes=(1048576*5), backupCount=7, mode="w")
    fh.setFormatter(format)
    log.addHandler(fh)

###################
# HELPER MESSAGES #
###################

if extrargs.cutLister:
    counter = 0
    print("Analysis Cut Options :")
    print("====================")
    temp = ""  
    for i in allAnalysisCuts:
        if len(temp) == 0:
            temp = temp + i
        else:
            temp = temp + "," + i
        counter = counter + 1
        if counter == 3:
            temp = stringToList(temp)
            threeSelectedList.append(temp)
            temp = ""
            counter = 0
    for list_ in threeSelectedList:
        print("{:<40s} {:<40s} {:<40s}".format(*list_))      
    sys.exit()

######################
# PREFIX ADDING PART #
###################### 

# add prefix for extrargs.pid for pid selection
if extrargs.pid != None:
    prefix_pid = "pid-"
    extrargs.pid = [prefix_pid + sub for sub in extrargs.pid]
    
# add prefix for extrargs.FT0 for tof-event-time
if extrargs.FT0 != None:
    prefix_process = "process"
    extrargs.FT0 = prefix_process + extrargs.FT0
    
######################################################################################

commonDeps = [
    "o2-analysis-timestamp",
    "o2-analysis-event-selection",
    "o2-analysis-multiplicity-table",
    "o2-analysis-trackselection",
    "o2-analysis-trackextension",
    "o2-analysis-pid-tof-base",
    "o2-analysis-pid-tof",
    "o2-analysis-pid-tof-full",
    "o2-analysis-pid-tof-beta",
    "o2-analysis-pid-tpc-full"
]

# Make some checks on provided arguments
if len(sys.argv) < 2:
  logging.error("Invalid syntax! The command line should look like this:")
  logging.info("  ./runFilterPP.py <yourConfig.json> --param value ...")
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
        logging.info("  ./runFilterPP.py<yourConfig.json> <-runData|-runMC> --param value ...")
        sys.exit()
        
except FileNotFoundError:
    isConfigJson = sys.argv[1].endswith(".json")
    if not isConfigJson:
            logging.error("Invalid syntax! After the script you must define your json configuration file!!! The command line should look like this:")
            logging.info(" ./runFilterPP.py <yourConfig.json> --param value ...")
            sys.exit()
    logging.error("Your JSON Config File found in path!!!")
    sys.exit()

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

logging.info("Only Select Configured as %s", extrargs.onlySelect)
if extrargs.onlySelect == "true":
    logging.info("INTERFACE MODE : JSON Overrider")
if extrargs.onlySelect == "false":
    logging.info("INTERFACE MODE : JSON Additional")

for key, value in config.items():
    if type(value) == type(config):
        for value, value2 in value.items():
                       
            # aod
            if value =="aod-file" and extrargs.aod:
                config[key][value] = extrargs.aod
                logging.debug(" - [%s] %s : %s",key,value,extrargs.aod)
                
            # DQ Selections for muons and barrel tracks
            if value =="processSelection" and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can"t iterate in None type
                        if keyCfg == "process": #  Only Select key for analysis
                                      
                            if key == "d-q-barrel-track-selection":                    
                                if "barrelTrackSelection" in valueCfg:
                                    config[key][value] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                if "barrelTrackSelection" not in valueCfg and extrargs.onlySelect == "true":
                                    config[key][value] = "false"
                                    logging.debug(" - [%s] %s : false",key,value)
                                                      
                            if key == "d-q-muons-selection":
                                if "muonSelection" in valueCfg:
                                    config[key][value] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                if "muonSelection" not in valueCfg and extrargs.onlySelect == "true":
                                    config[key][value] = "false"
                                    logging.debug(" - [%s] %s : false",key,value)
                                                                                               
            # DQ Selections event    
            if value =="processEventSelection" and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can"t iterate in None type
                        if keyCfg == "process": #  Only Select key for analysis
                            
                            if key == "d-q-event-selection-task":
                                if "eventSelection" in valueCfg:
                                    config[key][value] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                if "eventSelection" not in valueCfg:
                                    logging.warning("YOU MUST ALWAYS CONFIGURE eventSelection value in --process parameter!! It is Missing and this issue will fixed by CLI")
                                    config[key][value] = "true" 
                                    logging.debug(" - [%s] %s : true",key,value)
                                    
            # DQ Tiny Selection for barrel track
            if value =="processSelectionTiny" and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can"t iterate in None type
                        if keyCfg == "process": #  Only Select key for analysis
                                      
                            if key == "d-q-barrel-track-selection":                    
                                if "barrelTrackSelectionTiny" in valueCfg:
                                    config[key][value] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                if "barrelTrackSelectionTiny" not in valueCfg and extrargs.onlySelect == "true":
                                    config[key][value] = "false"
                                    logging.debug(" - [%s] %s : false",key,value)
            
            # DQ Tiny Selection for filterPP
            if value =="processFilterPPTiny" and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can"t iterate in None type
                        if keyCfg == "process": #  Only Select key for analysis
                                      
                            if key == "d-q-filter-p-p-task":                    
                                if "filterPPSelectionTiny" in valueCfg:
                                    config[key][value] = "true"
                                    config[key]["processFilterPP"] = "false"
                                    logging.debug(" - [%s] %s : true",key,value)
                                    logging.debug(" - [%s] processFilterPP : false",key)
                                if "filterPPSelectionTiny" not in valueCfg and extrargs.onlySelect == "true":
                                    config[key][value] = "false"
                                    config[key]["processFilterPP"] = "true"
                                    logging.debug(" - [%s] %s : false",key,value)
                                    logging.debug(" - [%s] processFilterPP : true",key)
                                                                                                          
            # Filter PP Selections        
            if value == "cfgBarrelSels" and extrargs.cfgBarrelSels:
                if type(extrargs.cfgBarrelSels) == type(clist):
                    extrargs.cfgBarrelSels = listToString(extrargs.cfgBarrelSels) 
                config[key][value] = extrargs.cfgBarrelSels
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgBarrelSels)
            if value == "cfgMuonSels" and extrargs.cfgMuonSels:
                if type(extrargs.cfgMuonSels) == type(clist):
                    extrargs.cfgMuonSels = listToString(extrargs.cfgMuonSels) 
                config[key][value] = extrargs.cfgMuonSels
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonSels)
                
            # DQ Cuts    
            if value == "cfgEventCuts" and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts)
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgEventCuts = actualConfig + "," + extrargs.cfgEventCuts 
                config[key][value] = extrargs.cfgEventCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgEventCuts)  
            if value == "cfgBarrelTrackCuts" and extrargs.cfgBarrelTrackCuts:
                if type(extrargs.cfgBarrelTrackCuts) == type(clist):
                    extrargs.cfgBarrelTrackCuts = listToString(extrargs.cfgBarrelTrackCuts)
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgBarrelTrackCuts = actualConfig + "," + extrargs.cfgBarrelTrackCuts 
                config[key][value] = extrargs.cfgBarrelTrackCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgBarrelTrackCuts)   
            if value =="cfgMuonsCuts" and extrargs.cfgMuonsCuts:
                if type(extrargs.cfgMuonsCuts) == type(clist):
                    extrargs.cfgMuonsCuts = listToString(extrargs.cfgMuonsCuts)
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgMuonsCuts = actualConfig + "," + extrargs.cfgMuonsCuts                  
                config[key][value] = extrargs.cfgMuonsCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonsCuts) 
            
            # QA Options  
            if value == "cfgWithQA" and extrargs.cfgWithQA:
                config[key][value] = extrargs.cfgWithQA
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgWithQA)  
                  
            # PID Selections
            if  (value in pidParameters) and extrargs.pid and key != "tof-pid":
                if value in extrargs.pid:
                    value2 = "1"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)  
                elif extrargs.onlySelect == "true":
                    value2 = "-1"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)  
            
            # event-selection
            if value == "syst" and extrargs.syst:
                config[key][value] = extrargs.syst
                logging.debug(" - [%s] %s : %s",key,value,extrargs.syst)  
            if value =="muonSelection" and extrargs.muonSelection:
                config[key][value] = extrargs.muonSelection
                logging.debug(" - [%s] %s : %s",key,value,extrargs.muonSelection)  
            if value == "customDeltaBC" and extrargs.customDeltaBC:
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
            if value == "tof-expreso" and extrargs.tof_expreso:
                config[key][value] = extrargs.tof_expreso
                logging.debug(" - [%s] %s : %s",key,value,extrargs.tof_expreso)
                
            # tof-event-time
            if  (value in ft0Parameters) and extrargs.FT0 and key == "tof-event-time":
                if value  == extrargs.FT0:
                    value2 = "true"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)  
                elif value != extrargs.FT0:
                    value2 = "false"
                    config[key][value] = value2
                    logging.debug(" - [%s] %s : %s",key,value,value2)     
                                                    
                                                  
            if value == "processDummy" and extrargs.autoDummy:            
                if config["d-q-barrel-track-selection"]["processSelection"] == "true":
                    config["d-q-barrel-track-selection"]["processDummy"] = "false"
                if config["d-q-barrel-track-selection"]["processSelection"] == "false":
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
                

# ================================================================
# Transcation Management for barrelsels and muonsels in filterPP 
# ================================================================

for key,value in configuredCommands.items():
    if(value != None):
        if key == "cfgMuonsCuts":
            muonCutList.append(value)
        if key == "cfgBarrelTrackCuts":
            barrelTrackCutList.append(value)
        if key == "cfgBarrelSels":
            barrelSelsList.append(value)
        if key == "cfgMuonSels":
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
            logging.info("For example, if cfgMuonCuts is muonLowPt,muonHighPt, then the cfgMuonSels has to be something like: muonLowPt::1,muonHighPt::1,muonLowPt:pairNoCut:1")  
            sys.exit()
                            
    for i in muonCut:    
        if i in muonSelsListAfterSplit:
            continue
        else:
            print("====================================================================================================================")
            logging.error("--cfgMuonsCut <value>: %s not in --cfgMuonSels %s ",i,muonSelsListAfterSplit)
            logging.info("[INFO] For fixing this issue, you should have the same number of cuts (and in the same order) provided to the cfgMuonsCuts from dq-selection as those provided to the cfgMuonSels in the DQFilterPPTask.") 
            logging.info("For example, if cfgMuonCuts is muonLowPt,muonHighPt,muonLowPt then the cfgMuonSels has to be something like: muonLowPt::1,muonHighPt::1,muonLowPt:pairNoCut:1")  
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
            logging.info("For example, if cfgBarrelTrackCuts is jpsiO2MCdebugCuts,jpsiO2MCdebugCuts2,jpsiO2MCdebugCuts then the cfgBarrelSels has to be something like: jpsiO2MCdebugCuts::1,jpsiO2MCdebugCuts2::1,jpsiO2MCdebugCuts:pairNoCut:1") 
            sys.exit()
                            
    for i in barrelTrackCut:    
        if i in barrelSelsListAfterSplit:
            continue
        else:
            print("====================================================================================================================")
            logging.error("--cfgBarrelTrackCuts <value>: %s not in --cfgBarrelSels %s",i,barrelSelsListAfterSplit)
            logging.info("For fixing this issue, you should have the same number of cuts (and in the same order) provided to the cfgBarrelTrackCuts from dq-selection as those provided to the cfgBarrelSels in the DQFilterPPTask.") 
            logging.info("For example, if cfgBarrelTrackCuts is jpsiO2MCdebugCuts,jpsiO2MCdebugCuts2,jpsiO2MCdebugCuts then the cfgBarrelSels has to be something like: jpsiO2MCdebugCuts::1,jpsiO2MCdebugCuts2::1,jpsiO2MCdebugCuts:pairNoCut:1")      
            sys.exit()

  
# AOD File Checker
if extrargs.aod != None:
    argProvidedAod =  extrargs.aod
    textAodList = argProvidedAod.startswith("@")
    endsWithRoot = argProvidedAod.endswith(".root")
    endsWithTxt = argProvidedAod.endswith("txt") or argProvidedAod.endswith("text") 
    if textAodList and endsWithTxt:
        argProvidedAod = argProvidedAod.replace("@","")
        logging.info("You provided AO2D list as text file : %s",argProvidedAod)
        if not os.path.isfile(argProvidedAod):
            logging.error("%s File not found in path!!!", argProvidedAod)
            sys.exit()
        else:
            logging.info("%s has valid File Format and Path, File Found", argProvidedAod)
         
    elif endsWithRoot:
        logging.info("You provided single AO2D as root file  : %s",argProvidedAod)
        if not os.path.isfile(argProvidedAod):
            logging.error("%s File not found in path!!!", argProvidedAod)
            sys.exit()
        else:
            logging.info("%s has valid File Format and Path, File Found", argProvidedAod)
                    
    else:
        logging.error("%s Wrong formatted File, check your file!!!", argProvidedAod)
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
    commonDeps.remove("o2-analysis-trackextension")     
    logging.info("o2-analysis-trackextension is not valid dep for run 3, It will deleted from your workflow.")
        
###########################
# End Interface Processes #
###########################

# Write the updated configuration file into a temporary file
updatedConfigFileName = "tempConfigFilterPP.json"

with open(updatedConfigFileName,"w") as outputFile:
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