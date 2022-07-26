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

# Orginal Task: https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Tasks/tableReader.cxx

from ast import parse
import sys
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from logging import handlers
import json
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

readerPath = "Configs/readerConfiguration_reducedEvent.json"
writerPath = "Configs/writerConfiguration_dileptons.json"

analysisSelections = {
    "eventSelection": "Run event selection on DQ skimmed events",
    "muonSelection": "Run muon selection on DQ skimmed muons",
    "trackSelection": "Run barrel track selection on DQ skimmed tracks",
    "eventMixing": "Run mixing on skimmed tracks based muon and track selections",
    "eventMixingVn": "Run vn mixing on skimmed tracks based muon and track selections",
    "sameEventPairing": "Run same event pairing selection on DQ skimmed data",
    "dileptonHadron": "Run dilepton-hadron pairing, using skimmed data"
}
analysisSelectionsList = []
for k, v in analysisSelections.items():
    analysisSelectionsList.append(k)

sameEventPairingProcessSelections = {
    "JpsiToEE": "Run electron-electron pairing, with skimmed tracks",
    "JpsiToMuMu": "Run muon-muon pairing, with skimmed muons",
    "JpsiToMuMuVertexing": "Run muon-muon pairing and vertexing, with skimmed muons",
    "VnJpsiToEE": "Run barrel-barrel vn mixing on skimmed tracks",
    "VnJpsiToMuMu": "Run muon-muon vn mixing on skimmed tracks",
    "ElectronMuon": "Run electron-muon pairing, with skimmed tracks/muons",
    "All": "Run all types of pairing, with skimmed tracks/muons"
}
sameEventPairingProcessSelectionsList = []
for k, v in sameEventPairingProcessSelections.items():
    sameEventPairingProcessSelectionsList.append(k)

booleanSelections = ["true", "false"]

mixingSelections = {
    "Barrel": "Run barrel-barrel mixing on skimmed tracks",
    "Muon": "Run muon-muon mixing on skimmed muons",
    "BarrelMuon": "Run barrel-muon mixing on skimmed tracks/muons",
    "BarrelVn": "Run barrel-barrel vn mixing on skimmed tracks",
    "MuonVn": "Run muon-muon vn mixing on skimmed tracks"
}
mixingSelectionsList = []
for k, v in mixingSelections.items():
    mixingSelectionsList.append(k)

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


clist = []  # control list for type control
allAnalysisCuts = []
allMixing = []

isAnalysisEventSelected = True
isAnalysisTrackSelected = True
isAnalysisMuonSelected = True
isAnalysisSameEventPairingSelected = True
isAnalysisDileptonHadronSelected = True

threeSelectedList = []

# List for Selected skimmed process functions for dummy automizer
skimmedListEventSelection = []
skimmedListTrackSelection = []
skimmedListMuonSelection = []
skimmedListEventMixing = []
skimmedListSEP = []
skimmedListDileptonHadron = []

# Get system variables in alienv.
O2DPG_ROOT = os.environ.get("O2DPG_ROOT")
QUALITYCONTROL_ROOT = os.environ.get("QUALITYCONTROL_ROOT")
O2_ROOT = os.environ.get("O2_ROOT")
O2PHYSICS_ROOT = os.environ.get("O2PHYSICS_ROOT")

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
with open("tempMixingLibrary.h") as f:
    for line in f:
        stringIfSearch = [x for x in f if "if" in x] 
        for i in stringIfSearch:
            getMixing = re.findall('"([^"]*)"', i)
            allMixing = allMixing + getMixing
    
with open("tempCutsLibrary.h") as f:
    for line in f:
        stringIfSearch = [x for x in f if "if" in x] 
        for i in stringIfSearch:
            getAnalysisCuts = re.findall('"([^"]*)"', i)
            allAnalysisCuts = allAnalysisCuts + getAnalysisCuts

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

########################
# Interface Parameters #
########################

# aod
groupDPLReader = parser.add_argument_group(title="Data processor options: internal-dpl-aod-reader")
groupDPLReader.add_argument("--aod", help="Add your AOD File with path", action="store", type=str)
groupDPLReader.add_argument("--reader", help="Add your AOD Reader JSON with path", action="store", default=readerPath, type=str)
groupDPLReader.add_argument("--writer", help="Add your AOD Writer JSON with path", action="store", default=writerPath, type=str)

# automation params
groupAutomations = parser.add_argument_group(title="Automation Parameters")
groupAutomations.add_argument("--onlySelect", help="If false JSON Overrider Interface If true JSON Additional Interface", action="store", default="true", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
groupAutomations.add_argument("--autoDummy", help="Dummy automize parameter (don't configure it, true is highly recomended for automation)", action="store", default="true", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# Skimmed processes for SEE and Analysis Selections
groupAnalysisSelections = parser.add_argument_group(title="Data processor options: analysis-event-selection, analysis-muon-selection, analysis-track-selection, analysis-event-mixing, analysis-dilepton-hadron")
groupAnalysisSelections.add_argument("--analysis", help="Skimmed process selections for Data Analysis", action="store", nargs="*", type=str, metavar="ANALYSIS", choices=analysisSelectionsList).completer = ChoicesCompleterList(analysisSelectionsList)

for key,value in analysisSelections.items():
    groupAnalysisSelections.add_argument(key, help=value, action="none")

groupProcessSEESelections = parser.add_argument_group(title="Data processor options: analysis-same-event-pairing")    
groupProcessSEESelections.add_argument("--process", help="Skimmed process selections for analysis-same-event-pairing task", action="store", nargs="*", type=str, metavar="PROCESS", choices=sameEventPairingProcessSelectionsList).completer = ChoicesCompleterList(sameEventPairingProcessSelectionsList)
groupProcess = parser.add_argument_group(title="Choice List for analysis-same-event-pairing task Process options (when a value added to parameter, processSkimmed value is converted from false to true)")

for key,value in sameEventPairingProcessSelections.items():
    groupProcess.add_argument(key, help=value, action="none")
    
# analysis-event-mixing
groupAnalysisEventMixing = parser.add_argument_group(title="Data processor options: analysis-event-mixing")
groupAnalysisEventMixing.add_argument("--mixing", help="Skimmed process selections for Event Mixing manually", nargs='*', action="store", type=str, choices=mixingSelectionsList).completer = ChoicesCompleterList(mixingSelectionsList)

# cfg for QA
groupQASelections = parser.add_argument_group(title="Data processor options: analysis-event-selection, analysis-muon-selection, analysis-track-selection, analysis-event-mixing")
groupQASelections.add_argument("--cfgQA", help="If true, fill QA histograms", action="store", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# analysis-event-selection
groupAnalysisEventSelection = parser.add_argument_group(title="Data processor options: analysis-event-selection")
groupAnalysisEventSelection.add_argument("--cfgMixingVars", help="Mixing configs separated by a space", nargs="*", action="store", type=str, metavar="CFGMIXINGVARS", choices=allMixing).completer = ChoicesCompleterList(allMixing)
groupAnalysisEventSelection.add_argument("--cfgEventCuts", help="Space separated list of event cuts", nargs="*", action="store", type=str, metavar="CFGEVENTCUTS", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)

# analysis-muon-selection
groupAnalysisMuonSelection = parser.add_argument_group(title="Data processor options: analysis-muon-selection")
groupAnalysisMuonSelection.add_argument("--cfgMuonCuts", help="Space separated list of muon cuts", nargs="*", action="store", type=str, metavar="CFGMUONCUTS", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)

# analysis-track-selection
groupAnalysisTrackSelection = parser.add_argument_group(title="Data processor options: analysis-track-selection")
groupAnalysisTrackSelection.add_argument("--cfgTrackCuts", help="Space separated list of barrel track cuts", nargs="*", action="store", type=str, metavar="CFGTRACKCUTS", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)

# analysis-dilepton-hadron
groupAnalysisDileptonHadron = parser.add_argument_group(title="Data processor options: analysis-dilepton-hadron")
groupAnalysisDileptonHadron.add_argument("--cfgLeptonCuts", help="Space separated list of barrel track cuts", nargs="*", action="store", type=str, metavar="CFGLEPTONCUTS", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)

# helper lister commands
groupAdditionalHelperCommands = parser.add_argument_group(title="Additional Helper Command Options")
groupAdditionalHelperCommands.add_argument("--cutLister", help="List all of the analysis cuts from CutsLibrary.h", action="store_true")
groupAdditionalHelperCommands.add_argument("--mixingLister", help="List all of the event mixing selections from MixingLibrary.h", action="store_true")

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
    
# Get Some cfg values provided from --param
for keyCfg,valueCfg in configuredCommands.items():
    if(valueCfg != None): # Skipped None types, because can"t iterate in None type
        if keyCfg == "analysis":
            if type(valueCfg) == type("string"):
                valueCfg = stringToList(valueCfg)
            analysisCfg = valueCfg
        if keyCfg == "mixing":
            if type(valueCfg) == type("string"):
                valueCfg = stringToList(valueCfg)
            mixingCfg = valueCfg
        if keyCfg == "process":
            if type(valueCfg) == type("string"):
                valueCfg = stringToList(valueCfg)
            processCfg = valueCfg

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
    
    loggerFile = "tableReader.log"
    if os.path.isfile(loggerFile):
        os.remove(loggerFile)
    
    fh = handlers.RotatingFileHandler(loggerFile, maxBytes=(1048576*5), backupCount=7, mode="w")
    fh.setFormatter(format)
    log.addHandler(fh)


# Make some checks on provided arguments
if len(sys.argv) < 2:
  logging.error("Invalid syntax! The command line should look like this:")
  logging.info("  ./runTableReader.py <yourConfig.json> --param value ...")
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
        logging.info("  ./runTableReader.py <yourConfig.json> <-runData|-runMC> --param value ...")
        sys.exit()
        
except FileNotFoundError:
    isConfigJson = sys.argv[1].endswith(".json")
    if not isConfigJson:
            logging.error("Invalid syntax! After the script you must define your json configuration file!!! The command line should look like this:")
            logging.info(" ./runTableReader.py <yourConfig.json> --param value ...")
            sys.exit()
    logging.error("Your JSON Config File found in path!!!")
    sys.exit()


taskNameInCommandLine = "o2-analysis-dq-table-reader"

# Check alienv
if O2PHYSICS_ROOT == None:
   logging.error("You must load O2Physics with alienv")
   sys.exit()

###################
# HELPER MESSAGES #
###################
    
if extrargs.cutLister and extrargs.mixingLister:
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
        
    print("\n====================\nEvent Mixing Selections :")
    print("====================")
    counter = 0
    temp = ""
    threeSelectedList.clear()    
    for i in allMixing:
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
    
if extrargs.mixingLister:
    counter = 0
    temp = ""
    print("Event Mixing Selections :")
    print("====================")  
    for i in allMixing:
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

            #aod
            if value =="aod-file" and extrargs.aod:
                config[key][value] = extrargs.aod
                logging.debug(" - [%s] %s : %s",key,value,extrargs.aod)
            # reader    
            if value =="aod-reader-json" and extrargs.reader:
                config[key][value] = extrargs.reader
                logging.debug(" - [%s] %s : %s",key,value,extrargs.reader)
                
            # analysis-event-selection, analysis-track-selection, analysis-muon-selection, analysis-same-event-pairing
            if value =="processSkimmed" and extrargs.analysis:
          
                if key == "analysis-event-selection":
                    if "eventSelection" in analysisCfg:
                        config[key][value] = "true"
                        logging.debug(" - [%s] %s : true",key,value)
                        isAnalysisEventSelected = True
                    if "eventSelection" not in analysisCfg:
                        logging.warning("YOU MUST ALWAYS CONFIGURE eventSelection value in --analysis parameter!! It is Missing and this issue will fixed by CLI")
                        config[key][value] = "true" 
                        logging.debug(" - [%s] %s : true",key,value)
                        
                if key == "analysis-track-selection":                  
                    if "trackSelection" in analysisCfg:
                        config[key][value] = "true"
                        logging.debug(" - [%s] %s : true",key,value)
                        isAnalysisTrackSelected = True
                    if "trackSelection" not in analysisCfg and extrargs.onlySelect == "true":
                        config[key][value] = "false"
                        logging.debug(" - [%s] %s : false",key,value)
                                            
                if key == "analysis-muon-selection":
                    if "muonSelection" in analysisCfg:
                        config[key][value] = "true"
                        logging.debug(" - [%s] %s : true",key,value)
                        isAnalysisMuonSelected = True
                    if "muonSelection" not in analysisCfg and extrargs.onlySelect == "true":
                        config[key][value] = "false"
                        logging.debug(" - [%s] %s : false",key,value)                                                                               
                if key == "analysis-dilepton-hadron":
                    if "dileptonHadron" in analysisCfg:
                        config[key][value] = "true"
                        isAnalysisDileptonHadronSelected = True
                        logging.debug(" - [%s] %s : true",key,value)
                    if "dileptonHadron" not in analysisCfg and extrargs.onlySelect == "true":
                        config[key][value] = "false"
                        logging.debug(" - [%s] %s : false",key,value)
                                                            
                if "sameEventPairing" in analysisCfg:
                    isAnalysisSameEventPairingSelected = True
                if "sameEventPairing" not in analysisCfg:
                    isAnalysisSameEventPairingSelected = False
                                    
            # Analysis-event-mixing with automation
            if extrargs.mixing == None:
                if value == "processBarrelSkimmed" and extrargs.analysis:                        
          
                    if key == "analysis-event-mixing":                             
                        if "trackSelection" in analysisCfg and "eventMixing" in analysisCfg:
                            config[key][value] = "true"
                            logging.debug(" - [%s] %s : true",key,value)
                        if "eventMixing" not in analysisCfg and extrargs.onlySelect == "true":
                            config[key][value] = "false"
                            logging.debug(" - [%s] %s : false",key,value)
                        if "eventMixing" in analysisCfg and ("trackSelection" not in analysisCfg and "muonSelection" not in analysisCfg):
                            logging.error("For Configuring eventMixing, You have to specify either trackSelection or muonSelection in --analysis parameter!")
                            sys.exit()
                                                                            
                if value == "processMuonSkimmed" and extrargs.analysis:                        

                    if key == "analysis-event-mixing":                                       
                        if "muonSelection" in analysisCfg and "eventMixing" in analysisCfg:
                            config[key][value] = "true"
                            logging.debug(" - [%s] %s : true",key,value)
                        if "eventMixing" not in analysisCfg and extrargs.onlySelect == "true":
                            config[key][value] = "false"
                            logging.debug(" - [%s] %s : false",key,value)
                        if "eventMixing" in analysisCfg and ("trackSelection" not in analysisCfg and "muonSelection" not in analysisCfg):
                            logging.error("For Configuring eventMixing, You have to specify either trackSelection or muonSelection in --analysis parameter!")
                            sys.exit()
                                                                            
                if value == "processBarrelMuonSkimmed" and extrargs.analysis:                        

                    if key == "analysis-event-mixing":                                                             
                        if "trackSelection" in analysisCfg and "muonSelection" in analysisCfg and "eventMixing" in analysisCfg:
                            config[key][value] = "true"
                            logging.debug(" - [%s] %s : true",key,value)
                        if "eventMixing" not in analysisCfg and extrargs.onlySelect == "true":
                            config[key][value] = "false"
                            logging.debug(" - [%s] %s : false",key,value)
                        if "eventMixing" in analysisCfg and ("trackSelection" not in analysisCfg and "muonSelection" not in analysisCfg):
                            logging.error("For Configuring eventMixing, You have to specify either trackSelection or muonSelection in --analysis parameter!")
                            sys.exit()
                                        
                if value == "processBarrelVnSkimmed" and extrargs.analysis:                        

                    if key == "analysis-event-mixing":                             
                        if "trackSelection" in analysisCfg and "eventMixingVn" in analysisCfg:
                            config[key][value] = "true"
                            logging.debug(" - [%s] %s : true",key,value)
                        if "eventMixingVn" not in analysisCfg and extrargs.onlySelect == "true":
                            config[key][value] = "false"
                            logging.debug(" - [%s] %s : false",key,value)
                        if "eventMixingVn" in analysisCfg and ("trackSelection" not in analysisCfg and "muonSelection" not in analysisCfg):
                            logging.error("For Configuring eventMixingVn, You have to specify either trackSelection or muonSelection in --analysis parameter!")
                            sys.exit()
                                                                            
                if value == "processMuonVnSkimmed" and extrargs.analysis:                        
       
                    if key == "analysis-event-mixing":                                        
                        if "muonSelection" in analysisCfg and "eventMixingVn" in analysisCfg:
                            config[key][value] = "true"
                            logging.debug(" - [%s] %s : true",key,value)
                        if "eventMixingVn" not in analysisCfg and extrargs.onlySelect == "true":
                            config[key][value] = "false"
                            logging.debug(" - [%s] %s : false",key,value)
                        if "eventMixingVn" in analysisCfg and ("trackSelection" not in analysisCfg and "muonSelection" not in analysisCfg):
                            logging.error("For Configuring eventMixingVn, You have to specify either trackSelection or muonSelection in --analysis parameter!")
                            sys.exit()
                                        
            # Analysis-event-mixing selection manually
            if extrargs.mixing != None:
                if value == "processBarrelSkimmed" and extrargs.analysis:                        

                    if key == "analysis-event-mixing":                             
                        if "trackSelection" in analysisCfg and "eventMixing" in analysisCfg and "Barrel" in mixingCfg:
                            config[key][value] = "true"
                            logging.debug(" - [%s] %s : true",key,value)
                        if "trackSelection" in analysisCfg and "Barrel" not in mixingCfg and extrargs.onlySelect == "true":
                            config[key][value] = "false"
                            logging.debug(" - [%s] %s : false",key,value)
                        if "eventMixing" not in analysisCfg and "Barrel" in mixingCfg:
                            logging.error("When configuring analysis-event-mixing for Barrel, you must configure eventMixing within the --analysis parameter!")
                            sys.exit()
                        if "Barrel" in mixingCfg and "trackSelection" not in analysisCfg:
                            logging.error("When configuring analysis-event-mixing for Barrel, you must configure trackSelection within the --analysis parameter!")
                            sys.exit()
                        if "eventMixing" in analysisCfg and ("trackSelection" not in analysisCfg and "muonSelection" not in analysisCfg):
                            logging.error("For Configuring eventMixing, You have to specify either trackSelection or muonSelection in --analysis parameter!")
                            sys.exit()
                                                                            
                if value == "processMuonSkimmed" and extrargs.analysis:                        
          
                    if key == "analysis-event-mixing":                                       
                        if "muonSelection" in analysisCfg and "eventMixing" in analysisCfg and "Muon" in mixingCfg:
                            config[key][value] = "true"
                            logging.debug(" - [%s] %s : true",key,value)
                        if "muonSelection" in analysisCfg and "Muon" not in mixingCfg and extrargs.onlySelect == "true":
                            config[key][value] = "false"
                            logging.debug(" - [%s] %s : false",key,value)
                        if "eventMixing" not in analysisCfg and "Muon" in mixingCfg:
                            logging.error("When configuring analysis-event-mixing for Muon, you must configure eventMixing within the --analysis parameter!")
                            sys.exit()
                        if "Muon" in mixingCfg and "muonSelection" not in analysisCfg:
                            logging.error("When configuring analysis-event-mixing for Muon, you must configure muonSelection within the --analysis parameter!")
                            sys.exit()
                        if "eventMixing" in analysisCfg and ("trackSelection" not in analysisCfg and "muonSelection" not in analysisCfg):
                            logging.error("For Configuring eventMixing, You have to specify either trackSelection or muonSelection in --analysis parameter!")
                            sys.exit()
                                                                            
                if value == "processBarrelMuonSkimmed" and extrargs.analysis:                        

                    if key == "analysis-event-mixing":                                                             
                        if "trackSelection" in analysisCfg and "muonSelection" in analysisCfg and "eventMixing" in analysisCfg and "BarrelMuon" in mixingCfg:
                            config[key][value] = "true"
                            logging.debug(" - [%s] %s : true",key,value)
                        if "trackSelection" in analysisCfg and "muonSelection" in analysisCfg and "BarrelMuon" not in mixingCfg and extrargs.onlySelect == "true":
                            config[key][value] = "false"
                            logging.debug(" - [%s] %s : false",key,value)
                        if "eventMixing" not in analysisCfg and "BarrelMuon" in mixingCfg:
                            logging.error("When configuring analysis-event-mixing for BarrelMuon, you must configure eventMixing within the --analysis parameter!")
                            sys.exit()
                        if "BarrelMuon" in mixingCfg and ("muonSelection" not in analysisCfg or "trackSelection" not in analysisCfg):
                            logging.error("When configuring analysis-event-mixing for BarrelMuon, you must configure both of muonSelection and trackSelection within the --analysis parameter!")
                            sys.exit()                                                                            
                        if "eventMixing" in analysisCfg and ("trackSelection" not in analysisCfg and "muonSelection" not in analysisCfg):
                            logging.error("For Configuring eventMixing, You have to specify either trackSelection or muonSelection in --analysis parameter!")
                            sys.exit()
                                        
                if value == "processBarrelVnSkimmed" and extrargs.analysis:                        

                    if key == "analysis-event-mixing":                             
                        if "trackSelection" in analysisCfg and "eventMixingVn" in analysisCfg and "BarrelVn" in mixingCfg:
                            config[key][value] = "true"
                            logging.debug(" - [%s] %s : true",key,value)
                        if "trackSelection" in analysisCfg and "BarrelVn" not in mixingCfg and extrargs.onlySelect == "true":
                            config[key][value] = "false"
                            logging.debug(" - [%s] %s : false",key,value)
                        if "eventMixingVn" not in analysisCfg and "BarrelVn" in mixingCfg:
                            logging.error("When configuring analysis-event-mixing for BarrelVn, you must configure eventMixingVn within the --analysis parameter!")
                            sys.exit()
                        if "BarrelVn" in mixingCfg and "trackSelection" not in analysisCfg:
                            logging.error("When configuring analysis-event-mixing for BarrelVn, you must configure trackSelection within the --analysis parameter!")
                            sys.exit()
                        if "eventMixingVn" in analysisCfg and ("trackSelection" not in analysisCfg and "muonSelection" not in analysisCfg):
                            logging.error("For Configuring eventMixingVn, You have to specify either trackSelection or muonSelection in --analysis parameter!")
                            sys.exit()
                                                                            
                if value == "processMuonVnSkimmed" and extrargs.analysis:                        

                    if key == "analysis-event-mixing":                                        
                        if "muonSelection" in analysisCfg and "eventMixingVn" in analysisCfg and "MuonVn" in mixingCfg:
                            config[key][value] = "true"
                            logging.debug(" - [%s] %s : true",key,value)
                        if "muonSelection" in analysisCfg and "MuonVn" not in mixingCfg and extrargs.onlySelect == "true":
                            config[key][value] = "false"
                            logging.debug(" - [%s] %s : false",key,value)
                        if "eventMixingVn" not in analysisCfg and "MuonVn" in mixingCfg:
                            logging.error("When configuring analysis-event-mixing for MuonVn, you must configure eventMixingVn within the --analysis parameter!")
                            sys.exit()
                        if "MuonVn" in mixingCfg and "muonSelection" not in analysisCfg:
                            logging.error("When configuring analysis-event-mixing for MuonVn, you must configure muonSelection within the --analysis parameter!")
                            sys.exit()
                        if "eventMixingVn" in analysisCfg and ("trackSelection" not in analysisCfg and "muonSelection" not in analysisCfg):
                            logging.error("For Configuring eventMixingVn, You have to specify either trackSelection or muonSelection in --analysis parameter!")
                            sys.exit()
                 
            # QA selections  
            if value =="cfgQA" and extrargs.cfgQA:
                config[key][value] = extrargs.cfgQA
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgQA)
                                              
            # analysis-event-selection
            if value == "cfgMixingVars" and extrargs.cfgMixingVars:
                if type(extrargs.cfgMixingVars) == type(clist):
                    extrargs.cfgMixingVars = listToString(extrargs.cfgMixingVars)
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgMixingVars = actualConfig + "," + extrargs.cfgMixingVars   
                config[key][value] = extrargs.cfgMixingVars
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMixingVars)
            if value == "cfgEventCuts" and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts)
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgEventCuts = actualConfig + "," + extrargs.cfgEventCuts   
                config[key][value] = extrargs.cfgEventCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgEventCuts)

            # analysis-track-selection
            if value =="cfgTrackCuts" and extrargs.cfgTrackCuts:
                if type(extrargs.cfgTrackCuts) == type(clist):
                    extrargs.cfgTrackCuts = listToString(extrargs.cfgTrackCuts)
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgTrackCuts = actualConfig + "," + extrargs.cfgTrackCuts   
                config[key][value] = extrargs.cfgTrackCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgTrackCuts)
                
            # analysis-muon-selection
            if value =="cfgMuonCuts" and extrargs.cfgMuonCuts:
                if type(extrargs.cfgMuonCuts) == type(clist):
                    extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts)
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgMuonCuts = actualConfig + "," + extrargs.cfgMuonCuts
                config[key][value] = extrargs.cfgMuonCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonCuts)
                
            # analysis-dilepton-hadron
            if value =="cfgLeptonCuts" and extrargs.cfgLeptonCuts:
                if type(extrargs.cfgLeptonCuts) == type(clist):
                    extrargs.cfgLeptonCuts = listToString(extrargs.cfgLeptonCuts)
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgLeptonCuts = actualConfig + "," + extrargs.cfgLeptonCuts 
                config[key][value] = extrargs.cfgLeptonCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgLeptonCuts)
            
            # analysis-same-event-pairing
            if key == "analysis-same-event-pairing" and extrargs.process:

                if not isAnalysisSameEventPairingSelected:
                    logging.warning("You forget to add sameEventPairing option to analysis for Workflow. It Automatically added by CLI.")
                    isAnalysisSameEventPairingSelected = True
                if "JpsiToEE" in processCfg and value == "processJpsiToEESkimmed":
                    if isAnalysisTrackSelected:
                        config[key]["processJpsiToEESkimmed"] = "true"
                        logging.debug(" - [%s] %s : true",key,value)
                    if not isAnalysisTrackSelected:
                        logging.error("trackSelection not found in analysis for processJpsiToEESkimmed -> analysis-same-event-pairing")
                        sys.exit()
                if "JpsiToEE" not in processCfg and value == "processJpsiToEESkimmed" and extrargs.onlySelect == "true":
                        config[key]["processJpsiToEESkimmed"] = "false"
                        logging.debug(" - [%s] %s : false",key,value)
                        
                if "JpsiToMuMu" in processCfg and value == "processJpsiToMuMuSkimmed":
                    if isAnalysisMuonSelected:
                        config[key]["processJpsiToMuMuSkimmed"] = "true"
                        logging.debug(" - [%s] %s : true",key,value)
                    if not isAnalysisMuonSelected:
                        logging.error("muonSelection not found in analysis for processJpsiToMuMuSkimmed -> analysis-same-event-pairing")
                        sys.exit()
                if "JpsiToMuMu" not in processCfg and value == "processJpsiToMuMuSkimmed" and extrargs.onlySelect == "true":
                    config[key]["processJpsiToMuMuSkimmed"] = "false"
                    logging.debug(" - [%s] %s : false",key,value)

                if "JpsiToMuMuVertexing" in processCfg and value == "processJpsiToMuMuVertexingSkimmed":
                    if isAnalysisMuonSelected:
                        config[key]["processJpsiToMuMuVertexingSkimmed"] = "true"
                        logging.debug(" - [%s] %s : true",key,value)
                    if not isAnalysisMuonSelected:
                        logging.error("muonSelection not found in analysis for processJpsiToMuMuVertexingSkimmed -> analysis-same-event-pairing")
                        sys.exit()
                if "JpsiToMuMuVertexing" not in processCfg and value == "processJpsiToMuMuVertexingSkimmed" and extrargs.onlySelect == "true":
                    config[key]["processJpsiToMuMuVertexingSkimmed"] = "false"
                    logging.debug(" - [%s] %s : false",key,value)
                    
                if "VnJpsiToEE" in processCfg and value == "processVnJpsiToEESkimmed":
                    if isAnalysisTrackSelected:
                        config[key]["processVnJpsiToEESkimmed"] = "true"
                        logging.debug(" - [%s] %s : true",key,value)
                    if not isAnalysisTrackSelected:
                        logging.error("trackSelection not found in analysis for processVnJpsiToEESkimmed -> analysis-same-event-pairing")
                        sys.exit()
                if "VnJpsiToEE" not in processCfg and value == "processVnJpsiToEESkimmed" and extrargs.onlySelect == "true":
                        config[key]["processVnJpsiToEESkimmed"] = "false"
                        logging.debug(" - [%s] %s : false",key,value)
                        
                if "VnJpsiToMuMu" in processCfg and value == "processVnJpsiToMuMuSkimmed":
                    if isAnalysisMuonSelected:
                        config[key]["processVnJpsiToMuMuSkimmed"] = "true"
                        logging.debug(" - [%s] %s : true",key,value)
                    if not isAnalysisMuonSelected:
                        logging.error("muonSelection not found in analysis for processVnJpsiToMuMuSkimmed -> analysis-same-event-pairing")
                        sys.exit()                                   
                if "VnJpsiToMuMu" not in processCfg and value == "processVnJpsiToMuMuSkimmed" and extrargs.onlySelect == "true":
                    config[key]["processVnJpsiToMuMuSkimmed"] = "false"
                    logging.debug(" - [%s] %s : false",key,value)
                    
                if "ElectronMuon" in processCfg and value == "processElectronMuonSkimmed":
                    if isAnalysisTrackSelected and isAnalysisMuonSelected:
                        config[key]["processElectronMuonSkimmed"] = "true"
                        logging.debug(" - [%s] %s : true",key,value)
                    else:
                        logging.error("trackSelection and muonSelection not found in analysis for processElectronMuonSkimmed -> analysis-same-event-pairing")
                        sys.exit()
                if "ElectronMuon" not in processCfg and value == "processElectronMuonSkimmed" and extrargs.onlySelect == "true":
                    config[key]["processElectronMuonSkimmed"] = "false"
                    logging.debug(" - [%s] %s : false",key,value)
                    
                if "All" in processCfg and value == "processAllSkimmed":
                    if isAnalysisEventSelected and isAnalysisMuonSelected and isAnalysisTrackSelected:
                        config[key]["processAllSkimmed"] = "true"
                        logging.debug(" - [%s] %s : true",key,value)
                    else:
                        logging.debug("eventSelection, trackSelection and muonSelection not found in analysis for processAllSkimmed -> analysis-same-event-pairing")
                        sys.exit()
                if "All" not in processCfg and value == "processAllSkimmed" and extrargs.onlySelect == "true":
                    config[key]["processAllSkimmed"] = "false"
                    logging.debug(" - [%s] %s : false",key,value)
   
            # If no process function is provided, all SEP process functions are pulled false (for JSON Overrider mode)                 
            if key == "analysis-same-event-pairing" and extrargs.process == None and isAnalysisSameEventPairingSelected == False and extrargs.onlySelect == "true":
                config[key]["processJpsiToEESkimmed"] = "false"
                config[key]["processJpsiToMuMuSkimmed"] = "false"
                config[key]["processJpsiToMuMuVertexingSkimmed"] = "false"
                config[key]["processVnJpsiToEESkimmed"] = "false"
                config[key]["processVnJpsiToMuMuSkimmed"] = "false"
                config[key]["processElectronMuonSkimmed"] = "false"
                config[key]["processAllSkimmed"] = "false"
                     
            if extrargs.autoDummy:
                """ 
                value.endswith("Skimmed") --> get all skimmed process functions without dummy
                if "true" in skimmedListEventSelection ... else ... --> # if no skimmed process true, processDummy true else processDummy false
                """
                                 
                if key == "analysis-event-selection": 
                    if value.endswith("Skimmed"):
                        if config[key][value] == "true":
                            skimmedListEventSelection.append("true")
                        if config[key][value] == "false":
                            skimmedListEventSelection.append("false")               
                    if "true" in skimmedListEventSelection:
                        config[key]["processDummy"] = "false"
                    else:
                        config[key]["processDummy"] = "true" 
                        
                if key == "analysis-muon-selection":
                    if value.endswith("Skimmed"):
                        if config[key][value] == "true":
                            skimmedListMuonSelection.append("true")
                        if config[key][value] == "false":
                            skimmedListMuonSelection.append("false")     
                    if "true" in skimmedListMuonSelection:
                        config[key]["processDummy"] = "false"
                    else:
                        config[key]["processDummy"] = "true"
                        
                if key == "analysis-track-selection":
                    if value.endswith("Skimmed"):
                        if config[key][value] == "true":
                            skimmedListTrackSelection.append("true")
                        if config[key][value] == "false":
                            skimmedListTrackSelection.append("false")        
                    if "true" in skimmedListTrackSelection:
                        config[key]["processDummy"] = "false"
                    else:
                        config[key]["processDummy"] = "true"
                        
                if key == "analysis-event-mixing":
                    if value.endswith("Skimmed"):
                        if config[key][value] == "true":
                            skimmedListEventMixing.append("true")
                        if config[key][value] == "false":
                            skimmedListEventMixing.append("false")                         
                    if "true" in skimmedListEventMixing:
                        config[key]["processDummy"] = "false"
                    else:
                        config[key]["processDummy"] = "true"
                        
                if key == "analysis-same-event-pairing":
                    if value.endswith("Skimmed"):
                        if config[key][value] == "true":
                            skimmedListSEP.append("true")
                        if config[key][value] == "false":
                            skimmedListSEP.append("false")           
                    if "true" in skimmedListSEP:
                        config[key]["processDummy"] = "false"
                    else:
                        config[key]["processDummy"] = "true" 
                        
                if key == "analysis-dilepton-hadron":
                    if value.endswith("Skimmed"):
                        if config[key][value] == "true":
                            skimmedListDileptonHadron.append("true")
                        if config[key][value] == "false":
                            skimmedListDileptonHadron.append("false")            
                    if "true" in skimmedListDileptonHadron:
                        config[key]["processDummy"] = "false"
                    else:
                        config[key]["processDummy"] = "true"
                                       
                            
# AOD File and Reader-Writer Checker  
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
        
if extrargs.reader != None:
    if not os.path.isfile(extrargs.reader):
        logging.error("%s File not found in path!!!",extrargs.reader)
        sys.exit()
elif not os.path.isfile((config["internal-dpl-aod-reader"]["aod-reader-json"])):
        print("[ERROR]",config["internal-dpl-aod-reader"]["aod-reader-json"],"File not found in path!!!")
        sys.exit()
 
###########################
# End Interface Processes #
###########################              

# Write the updated configuration file into a temporary file
updatedConfigFileName = "tempConfigTableReader.json"

with open(updatedConfigFileName,"w") as outputFile:
  json.dump(config, outputFile ,indent=2)
      
#commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " -b"
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --aod-writer-json " + extrargs.writer + " -b"

if extrargs.writer == "false":
    commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " -b"

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