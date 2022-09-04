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

# Orginal Task: https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Tasks/dqEfficiency.cxx

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

readerPath = "Configs/readerConfiguration_reducedEventMC.json"
writerPath = "Configs/writerConfiguration_dileptonMC.json"

analysisSelections = {
    "eventSelection": "Run event selection on DQ skimmed events",
    "muonSelection": "Run muon selection on DQ skimmed muons",
    "trackSelection": "Run barrel track selection on DQ skimmed tracks",
    "sameEventPairing": "Run same event pairing selection on DQ skimmed data",
    "dileptonTrackDimuonMuonSelection": "Run dimuon-muon pairing, using skimmed data",
    "dileptonTrackDielectronKaonSelection": "Run dielectron-kaon pairing, using skimmed data"
}
analysisSelectionsList = []
for k, v in analysisSelections.items():
    analysisSelectionsList.append(k)

sameEventPairingProcessSelections = {
    "JpsiToEE": "Run electron-electron pairing, with skimmed tracks",
    "JpsiToMuMu": "Run muon-muon pairing, with skimmed muons",
    "JpsiToMuMuVertexing": "Run muon-muon pairing and vertexing, with skimmed muons"
}
sameEventPairingProcessSelectionsList = []
for k, v in sameEventPairingProcessSelections.items():
    sameEventPairingProcessSelectionsList.append(k)

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

isAnalysisEventSelected = False
isAnalysisTrackSelected = False
isAnalysisMuonSelected = False
isAnalysisSameEventPairingSelected = False

clist = []  # control list for type control
allValuesCfg = []  # counter for provided args
allAnalysisCuts = []
allMCSignals = []

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

URL_CUTS_LIBRARY = "https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/CutsLibrary.h"
URL_MCSIGNALS_LIBRARY = "https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/MCSignalLibrary.h"
URL_MIXING_LIBRARY = "https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/MixingLibrary.h"

 
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
with open("tempMCSignalsLibrary.h") as f:
    for line in f:
        stringIfSearch = [x for x in f if "if" in x] 
        for i in stringIfSearch:
            getSignals = re.findall('"([^"]*)"', i)
            allMCSignals = allMCSignals + getSignals
    
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
parser.register("action", "none", NoAction)
parser.register("action", "store_choice", ChoicesAction)
groupCoreSelections = parser.add_argument_group(title="Core configurations that must be configured")
groupCoreSelections.add_argument("cfgFileName", metavar="Config.json", default="config.json", help="config JSON file name")

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
groupAutomations.add_argument("--autoDummy", help="Dummy automize parameter (don't configure it, true is highly recomended for automation)", action="store", default="true", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
groupAutomations.add_argument("--onlySelect", help="If false JSON Overrider Interface If true JSON Additional Interface", action="store", default="true", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# Skimmed processes for SEE and Analysis Selections
groupAnalysisSelections = parser.add_argument_group(title="Data processor options: analysis-event-selection, analysis-muon-selection, analysis-track-selection, analysis-dilepton-track")
groupAnalysisSelections.add_argument("--analysis", help="Skimmed process selections for MC Analysis", action="store", nargs="*", type=str, metavar="ANALYSIS", choices=analysisSelectionsList).completer = ChoicesCompleterList(analysisSelectionsList)

for key,value in analysisSelections.items():
    groupAnalysisSelections.add_argument(key, help=value, action="none")

groupProcessSEESelections = parser.add_argument_group(title="Data processor options: analysis-same-event-pairing")    
groupProcessSEESelections.add_argument("--process", help="Skimmed process selections for analysis-same-event-pairing task", action="store", nargs="*", type=str, metavar="PROCESS", choices= sameEventPairingProcessSelectionsList).completer = ChoicesCompleterList(sameEventPairingProcessSelectionsList)
groupProcessSEESelections.add_argument("--cfgBarrelMCRecSignals", help="Space separated list of MC signals (reconstructed)", nargs="*", action="store", type=str, metavar="CFGBARRELMCRECSIGNALS", choices=allMCSignals).completer = ChoicesCompleterList(allMCSignals)
groupProcessSEESelections.add_argument("--cfgBarrelMCGenSignals", help="Space separated list of MC signals (generated)", nargs="*", action="store", type=str, metavar="CFGBARRELMCGENSIGNALS", choices=allMCSignals).completer = ChoicesCompleterList(allMCSignals)
groupProcessSEESelections.add_argument("--cfgFlatTables", help="Produce a single flat tables with all relevant information of the pairs and single tracks", action="store", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
groupProcess = parser.add_argument_group(title="Choice List for analysis-same-event-pairing task Process options")

for key,value in sameEventPairingProcessSelections.items():
    groupProcess.add_argument(key, help=value, action="none")

# cfg for QA
groupQASelections = parser.add_argument_group(title="Data processor options: analysis-event-selection, analysis-muon-selection, analysis-track-selection, analysis-event-mixing, analysis-dilepton-hadron")
groupQASelections.add_argument("--cfgQA", help="If true, fill QA histograms", action="store", type=str.lower, choices=(booleanSelections)).completer = ChoicesCompleter(booleanSelections)

# analysis-event-selection
groupAnalysisEventSelection = parser.add_argument_group(title="Data processor options: analysis-event-selection")
groupAnalysisEventSelection.add_argument("--cfgEventCuts", help="Space separated list of event cuts", nargs="*", action="store", type=str, metavar="CFGEVENTCUTS", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)

# analysis-track-selection
groupAnalysisTrackSelection = parser.add_argument_group(title="Data processor options: analysis-track-selection")
groupAnalysisTrackSelection.add_argument("--cfgTrackCuts", help="Space separated list of barrel track cuts", nargs="*", action="store", type=str, metavar="CFGTRACKCUTS", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)
groupAnalysisTrackSelection.add_argument("--cfgTrackMCSignals", help="Space separated list of MC signals", nargs="*", action="store", type=str, metavar="CFGTRACKMCSIGNALS", choices=allMCSignals).completer = ChoicesCompleterList(allMCSignals)

# analysis-muon-selection
groupAnalysisMuonSelection = parser.add_argument_group(title="Data processor options: analysis-muon-selection")
groupAnalysisMuonSelection.add_argument("--cfgMuonCuts", help="Space separated list of muon cuts", nargs="*", action="store", type=str, metavar="CFGMUONCUTS", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)
groupAnalysisMuonSelection.add_argument("--cfgMuonMCSignals", help="Space separated list of MC signals", nargs="*", action="store", type=str, metavar="CFGMUONMCSIGNALS", choices=allMCSignals).completer = ChoicesCompleterList(allMCSignals)


# analysis-dilepton-track
groupAnalysisDileptonTrack = parser.add_argument_group(title="Data processor options: analysis-dilepton-track")
groupAnalysisDileptonTrack.add_argument("--cfgLeptonCuts", help="Space separated list of barrel track cuts", nargs="*", action="store", type=str, metavar="CFGLEPTONCUTS", choices=allAnalysisCuts).completer = ChoicesCompleterList(allAnalysisCuts)
groupAnalysisDileptonTrack.add_argument("--cfgFillCandidateTable", help="Produce a single flat tables with all relevant information dilepton-track candidates", action="store", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)
groupAnalysisDileptonTrack.add_argument("--cfgBarrelDileptonMCRecSignals", help="Space separated list of MC signals (reconstructed)", nargs="*", action="store", type=str, metavar="CFGBARRELDILEPTONMCRECSIGNALS", choices=allMCSignals).completer = ChoicesCompleterList(allMCSignals)
groupAnalysisDileptonTrack.add_argument("--cfgBarrelDileptonMCGenSignals", help="Space separated list of MC signals (generated)", nargs="*", action="store", type=str, metavar="CFGBARRELDILEPTONMCRECSIGNALS", choices=allMCSignals).completer = ChoicesCompleterList(allMCSignals)

# helper lister commands
groupAdditionalHelperCommands = parser.add_argument_group(title="Additional Helper Command Options")
groupAdditionalHelperCommands.add_argument("--cutLister", help="List all of the analysis cuts from CutsLibrary.h", action="store_true")
groupAdditionalHelperCommands.add_argument("--MCSignalsLister", help="List all of the MCSignals from MCSignalLibrary.h", action="store_true")

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
    logging.error("Your forget assign a value to for this parameters: ", forgetParams)
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
    
    loggerFile = "dqEfficiency.log"
    if os.path.isfile(loggerFile):
        os.remove(loggerFile)
    
    fh = handlers.RotatingFileHandler(loggerFile, maxBytes=(1048576*5), backupCount=7, mode="w")
    fh.setFormatter(format)
    log.addHandler(fh)
    
# Make some checks on provided arguments
if len(sys.argv) < 2:
  logging.error("Invalid syntax! The command line should look like this:")
  logging.info(" ./runDQEfficiency.py <yourConfig.json> --param value ...")
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
        logging.info("  ./runDQEfficiency.py <yourConfig.json> <-runData|-runMC> --param value ...")
        sys.exit()
        
except FileNotFoundError:
    isConfigJson = sys.argv[1].endswith(".json")
    if not isConfigJson:
            logging.error("Invalid syntax! After the script you must define your json configuration file!!! The command line should look like this:")
            logging.info(" ./runDQEfficiency.py <yourConfig.json> --param value ...")
            sys.exit()
    logging.error("Your JSON Config File found in path!!!")
    sys.exit()

taskNameInCommandLine = "o2-analysis-dq-efficiency"

# Check alienv
if O2PHYSICS_ROOT == None:
   logging.error("You must load O2Physics with alienv")
   sys.exit()

###################
# HELPER MESSAGES #
###################

      
if extrargs.cutLister and extrargs.MCSignalsLister:
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
        
    counter = 0
    print("MC Signals :")
    print("====================")
    temp = ""
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
    
if extrargs.MCSignalsLister:
    counter = 0
    print("MC Signals :")
    print("====================")
    temp = ""  
    for i in allMCSignals:
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
                
            # analysis-skimmed-selections
            if value =="processSkimmed" and extrargs.analysis:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can"t iterate in None type
                        if keyCfg == "analysis": #  Only Select key for analysis
                            
                            if key == "analysis-event-selection":
                                if "eventSelection" in valueCfg:
                                    config[key][value] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                    isAnalysisEventSelected = True
                                if "eventSelection" not in valueCfg:
                                    logging.warning("YOU MUST ALWAYS CONFIGURE eventSelection value in --analysis parameter!! It is Missing and this issue will fixed by CLI")
                                    config[key][value] = "true" 
                                    logging.debug(" - [%s] %s : true",key,value)
                                   
                            if key == "analysis-track-selection":                  
                                if "trackSelection" in valueCfg:
                                    config[key][value] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                    isAnalysisTrackSelected = True
                                if "trackSelection" not in valueCfg and extrargs.onlySelect == "true":
                                    config[key][value] = "false"
                                    logging.debug(" - [%s] %s : false",key,value)
                                                        
                            if key == "analysis-muon-selection":
                                if "muonSelection" in valueCfg:
                                    config[key][value] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                    isAnalysisMuonSelected = True
                                if "muonSelection" not in valueCfg and extrargs.onlySelect == "true":
                                    config[key][value] = "false"
                                    logging.debug(" - [%s] %s : false",key,value)   
                                                            
                            if "sameEventPairing" in valueCfg:
                                isAnalysisSameEventPairingSelected = True
                            if "sameEventPairing" not in valueCfg:
                                isAnalysisSameEventPairingSelected = False
                                    
            if value =="processDimuonMuonSkimmed" and extrargs.analysis:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can"t iterate in None type
                        if keyCfg == "analysis": #  Only Select key for analysis
                            
                            if key == "analysis-dilepton-track":
                                if "dileptonTrackDimuonMuonSelection" in valueCfg:
                                    config[key][value] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                if "dileptonTrackDimuonMuonSelection" not in valueCfg and extrargs.onlySelect == "true":
                                    config[key][value] = "false" 
                                    logging.debug(" - [%s] %s : false",key,value)
                                    
            if value =="processDielectronKaonSkimmed" and extrargs.analysis:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can"t iterate in None type
                        if keyCfg == "analysis": #  Only Select key for analysis
                            
                            if key == "analysis-dilepton-track":
                                if "dileptonTrackDielectronKaonSelection" in valueCfg:
                                    config[key][value] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                if "dileptonTrackDielectronKaonSelection" not in valueCfg and extrargs.onlySelect == "true":
                                    config[key][value] = "false" 
                                    logging.debug(" - [%s] %s : false",key,value)
                                                                           
            # QA selections  
            if value =="cfgQA" and extrargs.cfgQA:
                config[key][value] = extrargs.cfgQA
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgQA)
                              
            # analysis-event-selection
            if value == "cfgEventCuts" and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts)
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgEventCuts = actualConfig + "," + extrargs.cfgEventCuts 
                config[key][value] = extrargs.cfgEventCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgEventCuts)

            # analysis-track-selection
            if value == "cfgTrackCuts" and extrargs.cfgTrackCuts:
                if type(extrargs.cfgTrackCuts) == type(clist):
                    extrargs.cfgTrackCuts = listToString(extrargs.cfgTrackCuts) 
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgTrackCuts = actualConfig + "," + extrargs.cfgTrackCuts 
                config[key][value] = extrargs.cfgTrackCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgTrackCuts)
            if value == "cfgTrackMCSignals" and extrargs.cfgTrackMCSignals:
                if type(extrargs.cfgTrackMCSignals) == type(clist):
                    extrargs.cfgTrackMCSignals = listToString(extrargs.cfgTrackMCSignals)
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgTrackMCSignals = actualConfig + "," + extrargs.cfgTrackMCSignals 
                config[key][value] = extrargs.cfgTrackMCSignals
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgTrackMCSignals)
                
            # analysis-muon-selection
            if value == "cfgMuonCuts" and extrargs.cfgMuonCuts:
                if type(extrargs.cfgMuonCuts) == type(clist):
                    extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts)  
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgMuonCuts = actualConfig + "," + extrargs.cfgMuonCuts               
                config[key][value] = extrargs.cfgMuonCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonCuts) 
            if value == "cfgMuonMCSignals" and extrargs.cfgMuonMCSignals:
                if type(extrargs.cfgMuonMCSignals) == type(clist):
                    extrargs.cfgMuonMCSignals = listToString(extrargs.cfgMuonMCSignals) 
                if extrargs.onlySelect == "false":
                    actualConfig = config[key][value]
                    extrargs.cfgMuonMCSignals = actualConfig + "," + extrargs.cfgMuonMCSignals 
                config[key][value] = extrargs.cfgMuonMCSignals
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonMCSignals)
                
            # analysis-same-event-pairing
            if key == "analysis-same-event-pairing" and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if keyCfg == "process": # Select process keys
                        if(valueCfg != None): # Skipped None types, because can"t iterate in None type

                            if not isAnalysisSameEventPairingSelected:
                                logging.warning("You forget to add sameEventPairing option to analysis for Workflow. It Automatically added by CLI.")
                                isAnalysisSameEventPairingSelected = True
                    
                            if "JpsiToEE" in valueCfg and value == "processJpsiToEESkimmed":
                                if isAnalysisTrackSelected:
                                    config[key]["processJpsiToEESkimmed"] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                if not isAnalysisTrackSelected:
                                    logging.error("trackSelection not found in analysis for processJpsiToEESkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if "JpsiToEE" not in valueCfg and value == "processJpsiToEESkimmed" and extrargs.onlySelect == "true":
                                    config[key]["processJpsiToEESkimmed"] = "false"
                                    logging.debug(" - [%s] %s : false",key,value)
                                    
                            if "JpsiToMuMu" in valueCfg and value == "processJpsiToMuMuSkimmed":
                                if isAnalysisMuonSelected:
                                    config[key]["processJpsiToMuMuSkimmed"] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                if not isAnalysisMuonSelected:
                                    logging.error("muonSelection not found in analysis for processJpsiToMuMuSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if "JpsiToMuMu" not in valueCfg and value == "processJpsiToMuMuSkimmed" and extrargs.onlySelect == "true":
                                config[key]["processJpsiToMuMuSkimmed"] = "false"
                                logging.debug(" - [%s] %s : false",key,value)
   
                            if "JpsiToMuMuVertexing" in valueCfg and value == "processJpsiToMuMuVertexingSkimmed":
                                if isAnalysisMuonSelected:
                                    config[key]["processJpsiToMuMuVertexingSkimmed"] = "true"
                                    logging.debug(" - [%s] %s : true",key,value)
                                if not isAnalysisMuonSelected:
                                    logging.error("muonSelection not found in analysis for processJpsiToMuMuVertexingSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if "JpsiToMuMuVertexing" not in valueCfg and value == "processJpsiToMuMuVertexingSkimmed" and extrargs.onlySelect == "true":
                                config[key]["processJpsiToMuMuVertexingSkimmed"] = "false"
                                logging.debug(" - [%s] %s : false",key,value)
                                
            if key == "analysis-same-event-pairing" and extrargs.process == None and isAnalysisSameEventPairingSelected == False and extrargs.onlySelect == "true":
                config[key]["processJpsiToEESkimmed"] = "false"
                config[key]["processJpsiToMuMuSkimmed"] = "false"
                config[key]["processJpsiToMuMuVertexingSkimmed"] = "false"
            
            # analysis-same-event-pairing
            if key == "analysis-same-event-pairing":
                if value == "cfgBarrelMCRecSignals" and extrargs.cfgBarrelMCRecSignals:
                    if type(extrargs.cfgBarrelMCRecSignals) == type(clist):
                        extrargs.cfgBarrelMCRecSignals = listToString(extrargs.cfgBarrelMCRecSignals) 
                    if extrargs.onlySelect == "false":
                        actualConfig = config[key][value]
                        extrargs.cfgBarrelMCRecSignals = actualConfig + "," + extrargs.cfgBarrelMCRecSignals 
                    config[key][value] = extrargs.cfgBarrelMCRecSignals
                    logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgBarrelMCRecSignals)
                           
                if value == "cfgBarrelMCGenSignals" and extrargs.cfgBarrelMCGenSignals:
                    if type(extrargs.cfgBarrelMCGenSignals) == type(clist):
                        extrargs.cfgBarrelMCGenSignals = listToString(extrargs.cfgBarrelMCGenSignals)
                    if extrargs.onlySelect == "false":
                        actualConfig = config[key][value]
                        extrargs.cfgBarrelMCGenSignals = actualConfig + "," + extrargs.cfgBarrelMCGenSignals  
                    config[key][value] = extrargs.cfgBarrelMCGenSignals
                    logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgBarrelMCGenSignals)
                    
                if value == "cfgFlatTables" and extrargs.cfgFlatTables:
                    config[key][value] = extrargs.cfgFlatTables
                    logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgFlatTables)
                
            # analysis-dilepton-track
            if key == "analysis-dilepton-track":
                if value == "cfgBarrelMCRecSignals" and extrargs.cfgBarrelDileptonMCRecSignals:
                    if type(extrargs.cfgBarrelDileptonMCRecSignals) == type(clist):
                        extrargs.cfgBarrelDileptonMCRecSignals = listToString(extrargs.cfgBarrelDileptonMCRecSignals)
                    if extrargs.onlySelect == "false":
                        actualConfig = config[key][value]
                        extrargs.cfgBarrelDileptonMCRecSignals = actualConfig + "," + extrargs.cfgBarrelDileptonMCRecSignals   
                    config[key][value] = extrargs.cfgBarrelDileptonMCRecSignals
                    logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgBarrelDileptonMCRecSignals)
                    
                if value == "cfgBarrelMCGenSignals" and extrargs.cfgBarrelDileptonMCGenSignals:
                    if type(extrargs.cfgBarrelDileptonMCGenSignals) == type(clist):
                        extrargs.cfgBarrelDileptonMCGenSignals = listToString(extrargs.cfgBarrelDileptonMCGenSignals)
                    if extrargs.onlySelect == "false":
                        actualConfig = config[key][value]
                        extrargs.cfgBarrelDileptonMCGenSignals = actualConfig + "," + extrargs.cfgBarrelDileptonMCGenSignals   
                    config[key][value] = extrargs.cfgBarrelDileptonMCRecSignals
                    logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgBarrelDileptonMCGenSignals)            
                if value == "cfgLeptonCuts" and extrargs.cfgLeptonCuts:
                    if type(extrargs.cfgLeptonCuts) == type(clist):
                        extrargs.cfgLeptonCuts = listToString(extrargs.cfgLeptonCuts)
                    if extrargs.onlySelect == "false":
                        actualConfig = config[key][value]
                        extrargs.cfgLeptonCuts = actualConfig + "," + extrargs.cfgLeptonCuts 
                    config[key][value] = extrargs.cfgLeptonCuts
                    logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgLeptonCuts)
                    
                if value == "cfgFillCandidateTable" and extrargs.cfgFillCandidateTable:
                    config[key][value] = extrargs.cfgFillCandidateTable
                    logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgFillCandidateTable)
                    
            # Dummy automizer
            if value == "processDummy" and extrargs.autoDummy:
                
                if config["analysis-event-selection"]["processSkimmed"] == "true":
                    config["analysis-event-selection"]["processDummy"] = "false"
                if config["analysis-event-selection"]["processSkimmed"] == "false":
                    config["analysis-event-selection"]["processDummy"] = "true"
                    
                if config["analysis-track-selection"]["processSkimmed"] == "true":
                    config["analysis-track-selection"]["processDummy"] = "false"
                if config["analysis-track-selection"]["processSkimmed"] == "false":
                    config["analysis-track-selection"]["processDummy"] = "true"
                    
                if config["analysis-muon-selection"]["processSkimmed"] == "true":
                    config["analysis-muon-selection"]["processDummy"] = "false"
                if config["analysis-muon-selection"]["processSkimmed"] == "false":
                    config["analysis-muon-selection"]["processDummy"] = "true"
                    
                if config["analysis-same-event-pairing"]["processJpsiToEESkimmed"] == "true" or config["analysis-same-event-pairing"]["processJpsiToMuMuSkimmed"] == "true" or config["analysis-same-event-pairing"]["processJpsiToMuMuVertexingSkimmed"] == "true":
                    config["analysis-same-event-pairing"]["processDummy"] = "false"                    
                if config["analysis-same-event-pairing"]["processJpsiToEESkimmed"] == "false" and config["analysis-same-event-pairing"]["processJpsiToMuMuSkimmed"] == "false" and config["analysis-same-event-pairing"]["processJpsiToMuMuVertexingSkimmed"] == "false":
                    config["analysis-same-event-pairing"]["processDummy"] = "true"
                    
                if config["analysis-dilepton-track"]["processDimuonMuonSkimmed"] == "true":
                    config["analysis-dilepton-track"]["processDummy"] = "false"
                if config["analysis-dilepton-track"]["processDimuonMuonSkimmed"] == "false":
                    config["analysis-dilepton-track"]["processDummy"] = "true"
                    
                if config["analysis-dilepton-track"]["processDielectronKaonSkimmed"] == "true":
                    config["analysis-dilepton-track"]["processDummy"] = "false"
                if config["analysis-dilepton-track"]["processDielectronKaonSkimmed"] == "false":
                    config["analysis-dilepton-track"]["processDummy"] = "true"

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
updatedConfigFileName = "tempConfigDQEfficiency.json"
    
with open(updatedConfigFileName,"w") as outputFile:
  json.dump(config, outputFile ,indent=2)

commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " -b" + " --aod-writer-json " + extrargs.writer
if extrargs.writer == "false":
    commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " -b"

print("====================================================================================================================")
logging.info("Command to run:")
logging.info(commandToRun)
print("====================================================================================================================")

# Listing Added Commands

# Listing Added Commands
logging.info("Args provided configurations List")
print("====================================================================================================================")
for key,value in configuredCommands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
        logging.info("--%s : %s ",key,value)


os.system(commandToRun)