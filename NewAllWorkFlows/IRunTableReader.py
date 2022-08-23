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

readerPath = 'Configs/readerConfiguration_reducedEvent.json'
writerPath = 'Configs/writerConfiguration_dileptons.json'

analysisSelections = {
    "eventSelection" : "Run event selection on DQ skimmed events",
    "muonSelection" : "Run muon selection on DQ skimmed muons",
    "trackSelection" : "Run barrel track selection on DQ skimmed tracks",
    "eventMixingSelection" :"Run mixing on skimmed tracks based muon and track selections",
    "eventMixingVnSelection" :"Run vn mixing on skimmed tracks based muon and track selections",
    "sameEventPairing" : "Run same event pairing selection on DQ skimmed data" ,
    "dileptonHadron" :  "Run dilepton-hadron pairing, using skimmed data"
}
analysisSelectionsList = []
for k,v in analysisSelections.items():
    analysisSelectionsList.append(k)

SameEventPairingProcessSelections = {
    "JpsiToEE": "Run electron-electron pairing, with skimmed tracks",
    "JpsiToMuMu": "Run muon-muon pairing, with skimmed muons",
    "JpsiToMuMuVertexing": "Run muon-muon pairing and vertexing, with skimmed muons",
    "VnJpsiToEESkimmed": "Run barrel-barrel vn mixing on skimmed tracks",
    "VnJpsiToMuMuSkimmed": "Run muon-muon vn mixing on skimmed tracks",
    "ElectronMuon" : "Run electron-muon pairing, with skimmed tracks/muons" ,
    "All": "Run all types of pairing, with skimmed tracks/muons"
}
SameEventPairingProcessSelectionsList = []
for k,v in SameEventPairingProcessSelections.items():
    SameEventPairingProcessSelectionsList.append(k)

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


clist=[] # control list for type control
allCuts = []
allMixing = []

ANALYSIS_EVENT_SELECTED = False
ANALYSIS_TRACK_SELECTED = False
ANALYSIS_MUON_SELECTED = False
ANALYSIS_SEE_SELECTED = False
ANALYSIS_DILEPTON_HADRON_SELECTED = False

threeSelectedList = []

# Get system variables in alienv.
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
with open('tempMixingLibrary.h') as f:
    for line in f:
        stringIfSearch = [x for x in f if 'if' in x] 
        for i in stringIfSearch:
            getMixing = re.findall('"([^"]*)"', i)
            allMixing = allMixing + getMixing
    
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

########################
# Interface Parameters #
########################

# aod
groupDPLReader = parser.add_argument_group(title='Data processor options: internal-dpl-aod-reader')
groupDPLReader.add_argument('--aod', help="Add your AOD File with path", action="store", type=str)
groupDPLReader.add_argument('--reader', help="Add your AOD Reader JSON with path", action="store", default=readerPath, type=str)
groupDPLReader.add_argument('--writer', help="Add your AOD Writer JSON with path", action="store", default=writerPath, type=str)

# automation params
groupAutomations = parser.add_argument_group(title='Automation Parameters')
groupAutomations.add_argument('--autoDummy', help="Dummy automize parameter (don't configure it, true is highly recomended for automation)", action="store", default='true', type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# Skimmed processes for SEE and Analysis Selections
groupAnalysisSelections = parser.add_argument_group(title='Data processor options: analysis-event-selection, analysis-muon-selection, analysis-track-selection, analysis-event-mixing, analysis-dilepton-hadron')
groupAnalysisSelections.add_argument('--analysis', help="Skimmed process selections for Data Analysis", action="store", nargs='*', type=str, metavar='ANALYSIS', choices=analysisSelectionsList).completer = ChoicesCompleterList(analysisSelectionsList)

for key,value in analysisSelections.items():
    groupAnalysisSelections.add_argument(key, help=value, action='none')

groupProcessSEESelections = parser.add_argument_group(title='Data processor options: analysis-same-event-pairing')    
groupProcessSEESelections.add_argument('--process', help="Skimmed process selections for analysis-same-event-pairing task", action="store", nargs='*', type=str, metavar='PROCESS', choices=SameEventPairingProcessSelectionsList).completer = ChoicesCompleterList(SameEventPairingProcessSelectionsList)
groupProcess = parser.add_argument_group(title='Choice List for analysis-same-event-pairing task Process options (when a value added to parameter, processSkimmed value is converted from false to true)')

for key,value in SameEventPairingProcessSelections.items():
    groupProcess.add_argument(key, help=value, action='none')

# cfg for QA
groupQASelections = parser.add_argument_group(title='Data processor options: analysis-event-selection, analysis-muon-selection, analysis-track-selection, analysis-event-mixing')
groupQASelections.add_argument('--cfgQA', help="If true, fill QA histograms", action="store", type=str.lower, choices=booleanSelections).completer = ChoicesCompleter(booleanSelections)

# analysis-event-selection
groupAnalysisEventSelection = parser.add_argument_group(title='Data processor options: analysis-event-selection')
groupAnalysisEventSelection.add_argument('--cfgMixingVars', help="Mixing configs separated by a space", nargs='*', action="store", type=str, metavar='CFGMIXINGVARS', choices=allMixing).completer = ChoicesCompleterList(allMixing)
groupAnalysisEventSelection.add_argument('--cfgEventCuts', help="Space separated list of event cuts", nargs='*', action="store", type=str, metavar='CFGEVENTCUTS', choices=allCuts).completer = ChoicesCompleterList(allCuts)

# analysis-muon-selection
groupAnalysisMuonSelection = parser.add_argument_group(title='Data processor options: analysis-muon-selection')
groupAnalysisMuonSelection.add_argument('--cfgMuonCuts', help="Space separated list of muon cuts", nargs='*', action="store", type=str, metavar='CFGMUONCUTS', choices=allCuts).completer = ChoicesCompleterList(allCuts)

# analysis-track-selection
groupAnalysisTrackSelection = parser.add_argument_group(title='Data processor options: analysis-track-selection')
groupAnalysisTrackSelection.add_argument('--cfgTrackCuts', help="Space separated list of barrel track cuts", nargs='*', action="store", type=str, metavar='CFGTRACKCUTS', choices=allCuts).completer = ChoicesCompleterList(allCuts)

# analysis-dilepton-hadron
groupAnalysisDileptonHadron = parser.add_argument_group(title='Data processor options: analysis-dilepton-hadron')
groupAnalysisDileptonHadron.add_argument('--cfgLeptonCuts', help="Space separated list of barrel track cuts", nargs='*', action="store", type=str, metavar='CFGLEPTONCUTS', choices=allCuts).completer = ChoicesCompleterList(allCuts)

# helper lister commands
groupAdditionalHelperCommands = parser.add_argument_group(title='Additional Helper Command Options')
groupAdditionalHelperCommands.add_argument('--cutLister', help="List all of the analysis cuts from CutsLibrary.h", action="store_true")
groupAdditionalHelperCommands.add_argument('--mixingLister', help="List all of the event mixing selections from MixingLibrary.h", action="store_true")

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
    
    loggerFile = "tableReader.log"
    if os.path.isfile(loggerFile) == True:
        os.remove(loggerFile)
    
    fh = handlers.RotatingFileHandler(loggerFile, maxBytes=(1048576*5), backupCount=7, mode='w')
    fh.setFormatter(format)
    log.addHandler(fh)


# Make some checks on provided arguments
if len(sys.argv) < 2:
  logging.error("Invalid syntax! The command line should look like this:")
  logging.info("  ./IRunTableReader.py <yourConfig.json> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
config = {}
with open(sys.argv[1]) as configFile:
  config = json.load(configFile)


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
        
    print("\n====================\nEvent Mixing Selections :")
    print("====================")
    counter = 0
    temp = ''
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
    
if extrargs.mixingLister:
    counter = 0
    temp = ''
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
            temp = ''
            counter = 0
    for list_ in threeSelectedList:
        print('{:<40s} {:<40s} {:<40s}'.format(*list_))  
    sys.exit()

#############################
# Start Interface Processes #
#############################

for key, value in config.items():
    if type(value) == type(config):
        for value, value2 in value.items():

            #aod
            if value =='aod-file' and extrargs.aod:
                config[key][value] = extrargs.aod
                logging.debug(" - [%s] %s : %s",key,value,extrargs.aod)
            # reader    
            if value =='aod-reader-json' and extrargs.reader:
                config[key][value] = extrargs.reader
                logging.debug(" - [%s] %s : %s",key,value,extrargs.reader)
                
            # analysis-event-selection, analysis-track-selection, analysis-muon-selection, analysis-same-event-pairing
            if value =='processSkimmed' and extrargs.analysis:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-selection':
                                if 'eventSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                    ANALYSIS_EVENT_SELECTED = True
                                if 'eventSelection' not in valueCfg:
                                    logging.warning("YOU MUST ALWAYS CONFIGURE eventSelection value in --analysis parameter!! It is Missing and this issue will fixed by CLI")
                                    config[key][value] = 'true' 
                                    logging.debug(" - [%s] %s : true",key,value)
                                   
                            if key == 'analysis-track-selection':                  
                                if 'trackSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                    ANALYSIS_TRACK_SELECTED = True
                                if 'trackSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                        
                            if key == 'analysis-muon-selection':
                                if 'muonSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                    ANALYSIS_MUON_SELECTED = True
                                if 'muonSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)                                                                               
                            if key == 'analysis-dilepton-hadron':
                                if 'dileptonHadronSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    ANALYSIS_DILEPTON_HADRON_SELECTED = True
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'dileptonHadronSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                                       
                            if 'sameEventPairing' in valueCfg:
                                ANALYSIS_SEE_SELECTED = True
                            if 'sameEventPairing' not in valueCfg:
                                ANALYSIS_SEE_SELECTED = False
                                    
            # Analysis-event-mixing
            if value == 'processBarrelSkimmed' and extrargs.analysis:                        
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-mixing':                             
                                if 'trackSelection' in valueCfg and 'eventMixingSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'eventMixingSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                                        
            if value == 'processMuonSkimmed' and extrargs.analysis:                        
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-mixing':                                       
                                if 'muonSelection' in valueCfg and 'eventMixingSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'eventMixingSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                                        
            if value == 'processBarrelMuonSkimmed' and extrargs.analysis:                        
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-mixing':                                                             
                                if 'trackSelection' in valueCfg and 'muonSelection' in valueCfg and 'eventMixingSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'eventMixingSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                    
            if value == 'processBarrelVnSkimmed' and extrargs.analysis:                        
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-mixing':                             
                                if 'trackSelection' in valueCfg and 'eventMixingVnSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'eventMixingVnSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                                        
            if value == 'processMuonVnSkimmed' and extrargs.analysis:                        
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-mixing':                                        
                                if 'muonSelection' in valueCfg and 'eventMixingVnSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'eventMixingVnSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                 
            # QA selections  
            if value =='cfgQA' and extrargs.cfgQA:
                config[key][value] = extrargs.cfgQA
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgQA)
                                              
            # analysis-event-selection
            if value == 'cfgMixingVars' and extrargs.cfgMixingVars:
                if type(extrargs.cfgMixingVars) == type(clist):
                    extrargs.cfgMixingVars = listToString(extrargs.cfgMixingVars) 
                config[key][value] = extrargs.cfgMixingVars
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMixingVars)
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts) 
                config[key][value] = extrargs.cfgEventCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgEventCuts)

            # analysis-track-selection
            if value =='cfgTrackCuts' and extrargs.cfgTrackCuts:
                if type(extrargs.cfgTrackCuts) == type(clist):
                    extrargs.cfgTrackCuts = listToString(extrargs.cfgTrackCuts) 
                config[key][value] = extrargs.cfgTrackCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgTrackCuts)
                
            # analysis-muon-selection
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                if type(extrargs.cfgMuonCuts) == type(clist):
                    extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts) 
                config[key][value] = extrargs.cfgMuonCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgMuonCuts)
                
            # analysis-dilepton-hadron
            if value =='cfgLeptonCuts' and extrargs.cfgLeptonCuts:
                if type(extrargs.cfgLeptonCuts) == type(clist):
                    extrargs.cfgLeptonCuts = listToString(extrargs.cfgLeptonCuts) 
                config[key][value] = extrargs.cfgLeptonCuts
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgLeptonCuts)
            
            # analysis-same-event-pairing
            if key == 'analysis-same-event-pairing' and extrargs.process:
                for keyCfg,valueCfg in configuredCommands.items():
                    if keyCfg == 'process': # Select process keys
                        if(valueCfg != None): # Skipped None types, because can't iterate in None type

                            if ANALYSIS_SEE_SELECTED == False:
                                logging.warning("You forget to add sameEventPairing option to analysis for Workflow. It Automatically added by CLI.")
                                ANALYSIS_SEE_SELECTED = True
                            if 'JpsiToEE' in valueCfg and value == "processJpsiToEESkimmed":
                                if ANALYSIS_TRACK_SELECTED == True:
                                    config[key]["processJpsiToEESkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if ANALYSIS_TRACK_SELECTED == False:
                                    logging.error("trackSelection not found in analysis for processJpsiToEESkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'JpsiToEE' not in valueCfg and value == "processJpsiToEESkimmed":
                                    config[key]["processJpsiToEESkimmed"] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                    
                            if 'JpsiToMuMu' in valueCfg and value == "processJpsiToMuMuSkimmed":
                                if ANALYSIS_MUON_SELECTED == True:
                                    config[key]["processJpsiToMuMuSkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if ANALYSIS_MUON_SELECTED == False:
                                    logging.error("muonSelection not found in analysis for processJpsiToMuMuSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'JpsiToMuMu' not in valueCfg and value == "processJpsiToMuMuSkimmed":
                                config[key]["processJpsiToMuMuSkimmed"] = 'false'
                                logging.debug(" - [%s] %s : false",key,value)
   
                            if 'JpsiToMuMuVertexing' in valueCfg and value == "processJpsiToMuMuVertexingSkimmed":
                                if ANALYSIS_MUON_SELECTED == True:
                                    config[key]["processJpsiToMuMuVertexingSkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if ANALYSIS_MUON_SELECTED == False:
                                    logging.error("muonSelection not found in analysis for processJpsiToMuMuVertexingSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'JpsiToMuMuVertexing' not in valueCfg and value == "processJpsiToMuMuVertexingSkimmed":
                                config[key]["processJpsiToMuMuVertexingSkimmed"] = 'false'
                                logging.debug(" - [%s] %s : false",key,value)
                                
                            if 'VnJpsiToEE' in valueCfg and value == "processVnJpsiToEESkimmed":
                                if ANALYSIS_TRACK_SELECTED == True:
                                    config[key]["processVnJpsiToEESkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if ANALYSIS_TRACK_SELECTED == False:
                                    logging.error("trackSelection not found in analysis for processVnJpsiToEESkimmed -> analysis-same-event-pairing")
                                    sys.exit()

                            if 'VnJpsiToEE' not in valueCfg and value == "processVnJpsiToEESkimmed":
                                    config[key]["processVnJpsiToEESkimmed"] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                    
                            if 'VnJpsiToMuMu' in valueCfg and value == "processVnJpsiToMuMuSkimmed":
                                if ANALYSIS_MUON_SELECTED == True:
                                    config[key]["processVnJpsiToMuMuSkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if ANALYSIS_MUON_SELECTED == False:
                                    logging.error("muonSelection not found in analysis for processVnJpsiToMuMuSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                                    
                            if 'VnJpsiToMuMu' not in valueCfg and value == "processVnJpsiToMuMuSkimmed":
                                config[key]["processVnJpsiToMuMuSkimmed"] = 'false'
                                logging.debug(" - [%s] %s : false",key,value)
                                
                            if 'ElectronMuon' in valueCfg and value == "processElectronMuonSkimmed":
                                if ANALYSIS_TRACK_SELECTED == True and ANALYSIS_MUON_SELECTED == True:
                                    config[key]["processElectronMuonSkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                else:
                                    logging.error("trackSelection and muonSelection not found in analysis for processElectronMuonSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'ElectronMuon' not in valueCfg and value == "processElectronMuonSkimmed":
                                config[key]["processElectronMuonSkimmed"] = 'false'
                                logging.debug(" - [%s] %s : false",key,value)
                                
                            if 'All' in valueCfg and value == "processAllSkimmed":
                                if ANALYSIS_EVENT_SELECTED == True and ANALYSIS_MUON_SELECTED == True and ANALYSIS_TRACK_SELECTED == True:
                                    config[key]["processAllSkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                else:
                                    logging.debug("eventSelection, trackSelection and muonSelection not found in analysis for processAllSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'All' not in valueCfg and value == "processAllSkimmed":
                                config[key]["processAllSkimmed"] = 'false'
                                logging.debug(" - [%s] %s : false",key,value)
                                
                        if key == 'analysis-same-event-pairing' and extrargs.process == None and ANALYSIS_SEE_SELECTED == False:
                            config[key]["processJpsiToEESkimmed"] = 'false'
                            config[key]["processJpsiToMuMuSkimmed"] = 'false'
                            config[key]["processJpsiToMuMuVertexingSkimmed"] = 'false'
                            config[key]["processVnJpsiToEESkimmed"] = 'false'
                            config[key]["processVnJpsiToMuMuSkimmed"] = 'false'
                            config[key]["processElectronMuonSkimmed"] = 'false'
                            config[key]["processAllSkimmed"] = 'false'
            
            # Dummy automizer
            if value == 'processDummy' and extrargs.autoDummy:
                
                if config["analysis-event-selection"]["processSkimmed"] == "true":
                    config["analysis-event-selection"]["processDummy"] = "false"
                if config["analysis-event-selection"]["processSkimmed"] == 'false':
                    config["analysis-event-selection"]["processDummy"] = "true"
                    
                if config["analysis-muon-selection"]["processSkimmed"] == "true":
                    config["analysis-muon-selection"]["processDummy"] = "false"
                if config["analysis-muon-selection"]["processSkimmed"] == 'false':
                    config["analysis-muon-selection"]["processDummy"] = "true"
                    
                if config["analysis-track-selection"]["processSkimmed"] == "true":
                    config["analysis-track-selection"]["processDummy"] = "false"
                if config["analysis-track-selection"]["processSkimmed"] == "false":
                    config["analysis-track-selection"]["processDummy"] = "true"
                    
                if config["analysis-event-mixing"]["processBarrelSkimmed"] == "true" or config["analysis-event-mixing"]["processMuonSkimmed"] == "true" or config["analysis-event-mixing"]["processBarrelMuonSkimmed"] == "true":
                    config["analysis-event-mixing"]["processDummy"] = "false"
                if config["analysis-event-mixing"]["processBarrelSkimmed"] == "false" and config["analysis-event-mixing"]["processMuonSkimmed"] == "false" and config["analysis-event-mixing"]["processBarrelMuonSkimmed"] == "false":
                    config["analysis-event-mixing"]["processDummy"] = "true"  
                    
                if config["analysis-same-event-pairing"]["processJpsiToEESkimmed"] == "true" or config["analysis-same-event-pairing"]["processJpsiToMuMuSkimmed"] == "true" or config["analysis-same-event-pairing"]["processJpsiToMuMuVertexingSkimmed"] == "true" or config["analysis-same-event-pairing"]["processVnJpsiToEESkimmed"] == "true" or config["analysis-same-event-pairing"]["processVnJpsiToMuMuSkimmed"] == "true" or config["analysis-same-event-pairing"]["processElectronMuonSkimmed"] == "true" or config["analysis-same-event-pairing"]["processAllSkimmed"] == "true":
                    config["analysis-same-event-pairing"]["processDummy"] = "false"
                            
                if config["analysis-same-event-pairing"]["processJpsiToEESkimmed"] == "false" and config["analysis-same-event-pairing"]["processJpsiToMuMuSkimmed"] == "false" and config["analysis-same-event-pairing"]["processJpsiToMuMuVertexingSkimmed"] == "false" and config["analysis-same-event-pairing"]["processVnJpsiToEESkimmed"] == "false" and config["analysis-same-event-pairing"]["processVnJpsiToMuMuSkimmed"] == "false" and config["analysis-same-event-pairing"]["processElectronMuonSkimmed"] == "false" and config["analysis-same-event-pairing"]["processAllSkimmed"] == "false":
                    config["analysis-same-event-pairing"]["processDummy"] = "true"
                    
                if config["analysis-dilepton-hadron"]["processSkimmed"] == "true":
                    config["analysis-dilepton-hadron"]["processDummy"] = "false"
                if config["analysis-dilepton-hadron"]["processSkimmed"] == "false":
                    config["analysis-dilepton-hadron"]["processDummy"] = "true"
                            
# AOD and JSON Reader File Checker
                
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
        
if extrargs.reader != None:
    if os.path.isfile(extrargs.reader) == False:
        logging.error("%s File not found in path!!!",extrargs.reader)
        sys.exit()
elif os.path.isfile((config["internal-dpl-aod-reader"]["aod-reader-json"])) == False:
        print("[ERROR]",config["internal-dpl-aod-reader"]["aod-reader-json"],"File not found in path!!!")
        sys.exit()
 
###########################
# End Interface Processes #
###########################              


# Write the updated configuration file into a temporary file
updatedConfigFileName = "tempConfigTableReader.json"

with open(updatedConfigFileName,'w') as outputFile:
  json.dump(config, outputFile ,indent=2)
      
#commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " -b"
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --aod-writer-json " + extrargs.writer + " -b"

#TODO: need check
#if ANALYSIS_DILEPTON_HADRON_SELECTED == True:
    #commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --aod-writer-json " + extrargs.writer + " -b"

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
