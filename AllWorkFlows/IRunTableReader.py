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

# defination for binary check TODO: Need to be integrated
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

readerPath = 'Configs/readerConfiguration_reducedEvent.json'
writerPath = 'Configs/writerConfiguration_dileptons.json'

clist=[] # control list for type control
allCuts = []
allMixing = []

isEventSelection = False
isTrackSelection = False
isMuonSelection = False
isSameEventPairing = False
isDileptonHadronAnalysis = False



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
    
parser = argparse.ArgumentParser(description='Arguments to pass')
parser.add_argument('cfgFileName', metavar='text', default='config.json', help='config file name')
parser.add_argument('--add_mc_conv', help="Add the converter from mcparticle to mcparticle+001", action="store_true")
parser.add_argument('--add_fdd_conv', help="Add the fdd converter", action="store_true")
parser.add_argument('--add_track_prop', help="Add track propagation to the innermost layer (TPC or ITS)", action="store_true")
parser.add_argument('--logFile', help="Enable logger for both file and CLI", action="store_true")

########################
# Interface Parameters #
########################

# aod
parser.add_argument('--aod', help="Add your AOD File with path", action="store", type=str)
parser.add_argument('--reader', help="Add your AOD Reader JSON with path", action="store", default=readerPath, type=str)
parser.add_argument('--writer', help="Add your AOD Writer JSON with path", action="store", default=writerPath, type=str)

#json output
#parser.add_argument('--outputjson', help="Your Output JSON Config Fİle", action="store", type=str)

# Skimmed processes and Dummy Selections for analysis
parser.add_argument('--analysis', help="Skimmed process selections for analysis", action="store", choices=['eventSelection','muonSelection','trackSelection','sameEventPairing','dileptonHadron'], nargs='*', type=str)
parser.add_argument('--process', help="Skimmed process selections for same event pairing", action="store", choices=['JpsiToEE','JpsiToMuMu','JpsiToMuMuVertexing','ElectronMuon','All'], nargs='*', type=str)
parser.add_argument('--isMixingEvent', help="analysis-event-mixing: process function activate for event mixing", action="store", choices=['true','false'], type=str.lower)
#parser.add_argument('--analysisDummy', help="Dummy Selections (if autoDummy true, you don't need it)", action="store", choices=['eventSelection','muonSelection','trackSelection','eventMixing','sameEventPairing','dileptonHadron'], nargs='*', type=str)
parser.add_argument('--autoDummy', help="Dummy automize parameter (if process skimmed false, it automatically activate dummy process and viceversa)", action="store", choices=["true","false"], default='true', type=str.lower)
#parser.add_argument('--analysisAllSkimmed', help="All Skimmed Selection as boolean", action="store", choices=["true","false"], default=["false"], type=str.lower)

# cfg for QA
parser.add_argument('--cfgQA', help="If true, fill QA histograms", action="store", choices=["true","false"], type=str.lower)

# analysis-event-selection
parser.add_argument('--cfgMixingVars', help="Mixing configs separated by a space", choices=allMixing, nargs='*', action="store", type=str, metavar='')
parser.add_argument('--cfgEventCuts', help="Space separated list of event cuts", choices=allCuts,nargs='*', action="store", type=str, metavar='')

# analysis-muon-selection
parser.add_argument('--cfgMuonCuts', help="Space separated list of muon cuts", choices=allCuts, nargs='*', action="store", type=str, metavar='')

# analysis-track-selection
parser.add_argument('--cfgTrackCuts', help="Space separated list of barrel track cuts", choices=allCuts,nargs='*', action="store", type=str, metavar='')

# analysis-event-mixing
# see in skimmed options and cuts are configured in muon and track selection

# analysis-same-event-pairing
#parser.add_argument('--processSameEventPairing', help="This option automatically activates same-event-pairing based on analysis track, muon, event and event mixing", action="store", choices=['true','false'], default='true', type=str.lower)
#parser.add_argument('--isVertexing', help="Run muon-muon pairing and vertexing, with skimmed muons instead of Run muon-muon pairing, with skimmed muons (processJpsiToMuMuSkimmed must true for this selection)", action="store", choices=['true','false'], type=str.lower)


# analysis-dilepton-hadron
parser.add_argument('--cfgLeptonCuts', help="Space separated list of barrel track cuts", choices=allCuts,nargs='*', action="store", type=str, metavar='')

# helper lister commands
parser.add_argument('--cutLister', help="List all of the analysis cuts from CutsLibrary.h", action="store_true")
parser.add_argument('--mixingLister', help="List all of the event mixing selections from MixingLibrary.h", action="store_true")

# debug options
parser.add_argument('--debug', help="execute with debug options", action="store", choices=["NOTSET","DEBUG","INFO","WARNING","ERROR","CRITICAL"], type=str.upper, default="INFO")

"""Activate For Autocomplete. See to Libraries for Info"""
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

#TODO: Provide a Table format for print option       
if extrargs.cutLister and extrargs.mixingLister:
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
        
    print("\n====================\nEvent Mixing Selections :")
    print("====================")
    counter = 0
    for i in allMixing:
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
    
if extrargs.mixingLister:
    counter = 0
    print("Event Mixing Selections :")
    print("====================")
    for i in allMixing:   
        print(i,end="\t")
        counter += 1
        if counter == 5:
            print("\n")
            counter = 0
    print("\n")
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
                
            # analysis-skimmed-selections
            if value =='processSkimmed' and extrargs.analysis:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-selection':
                                if 'eventSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                    isEventSelection = True
                                if 'eventSelection' not in valueCfg:
                                    config[key][value] = 'false' 
                                    logging.debug(" - [%s] %s : false",key,value)
                                   
                            if key == 'analysis-track-selection':                  
                                if 'trackSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                    isTrackSelection = True
                                if 'trackSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                        
                            if key == 'analysis-muon-selection':
                                if 'muonSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                    isMuonSelection = True
                                if 'muonSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)                                                                               
                            if key == 'analysis-dilepton-hadron':
                                if 'dileptonHadronSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    isDileptonHadronAnalysis = True
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'dileptonHadronSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                                       
                            if 'sameEventPairing' in valueCfg:
                                isSameEventPairing = True
                            if 'sameEventPairing' not in valueCfg:
                                isSameEventPairing = False
                                    
            # Analysis Event Mixing Selections
            if value == 'processBarrelSkimmed' and extrargs.isMixingEvent:                        
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-mixing' and extrargs.isMixingEvent == 'true':                             
                                if 'trackSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'trackSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                                        
            if value == 'processMuonSkimmed' and extrargs.isMixingEvent:                        
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-mixing' and extrargs.isMixingEvent == 'true':                                        
                                if 'muonSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'muonSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                                                        
            if value == 'processBarrelMuonSkimmed' and extrargs.isMixingEvent:                        
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-mixing' and extrargs.isMixingEvent == 'true':                                                             
                                if 'trackSelection' in valueCfg and 'muonSelection' in valueCfg:
                                    config[key][value] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if 'trackSelection' not in valueCfg or 'muonSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                           
            # analysis-dummy-selections (We have automated thins so not need most of time)
            """
            if value =='processDummy' and extrargs.analysisDummy:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'analysisDummy': #  Only Select key for dummies
                        
                            if key == 'analysis-event-selection':
                                if 'event' in valueCfg:
                                    config[key][value] = 'true'
                                if 'event' not in valueCfg:
                                    config[key][value] = 'false' 
                                   
                            if key == 'analysis-track-selection':                      
                                if 'track' in valueCfg:
                                    config[key][value] = 'true'
                                if 'track' not in valueCfg:
                                    config[key][value] = 'false'
                                                        
                            if key == 'analysis-muon-selection':
                                if 'muon' in valueCfg:
                                    config[key][value] = 'true'
                                if 'muon' not in valueCfg:
                                    config[key][value] = 'false'
                                        
                            if key == 'analysis-event-mixing':
                                if 'eventMixing' in valueCfg:
                                    config[key][value] = 'true'
                                if 'eventMixing' not in valueCfg:
                                    config[key][value] = 'false'
                                    
                            if key == 'analysis-same-event-pairing':
                                if 'sameEventPairing' in valueCfg:
                                    config[key][value] = 'true'
                                if 'sameEventPairing' not in valueCfg:
                                    config[key][value] = 'false'
                                        
                            if key == 'analysis-dilepton-hadron':
                                if 'dileptonHadron' in valueCfg:
                                    config[key][value] = 'true'
                                if 'dileptonHadron' not in valueCfg:
                                    config[key][value] = 'false'
            """
                 
            # QA selections  
            if value =='cfgQA' and extrargs.cfgQA:
                config[key][value] = extrargs.cfgQA
                logging.debug(" - [%s] %s : %s",key,value,extrargs.cfgQA)
                
            # Process All Skimmed Selection
            #if value =='processAllSkimmed' and extrargs.analysisAllSkimmed:
                #config[key][value] = extrargs.analysisAllSkimmed
                              
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

                            if isSameEventPairing == False:
                                logging.warning("You forget to add sameEventPairing option to analysis for Workflow. It Automatically added by CLI.")
                                isSameEventPairing = True
                            if 'JpsiToEE' in valueCfg and value == "processJpsiToEESkimmed":
                                if isTrackSelection == True:
                                    config[key]["processJpsiToEESkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if isTrackSelection == False:
                                    logging.error("trackSelection not found in analysis for processJpsiToEESkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'JpsiToEE' not in valueCfg and value == "processJpsiToEESkimmed":
                                    config[key]["processJpsiToEESkimmed"] = 'false'
                                    logging.debug(" - [%s] %s : false",key,value)
                                    
                            if 'JpsiToMuMu' in valueCfg and value == "processJpsiToMuMuSkimmed":
                                if isMuonSelection == True:
                                    config[key]["processJpsiToMuMuSkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if isMuonSelection == False:
                                    logging.error("muonSelection not found in analysis for processJpsiToMuMuSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'JpsiToMuMu' not in valueCfg and value == "processJpsiToMuMuSkimmed":
                                config[key]["processJpsiToMuMuSkimmed"] = 'false'
                                logging.debug(" - [%s] %s : false",key,value)
   
                            if 'JpsiToMuMuVertexing' in valueCfg and value == "processJpsiToMuMuVertexingSkimmed":
                                if isMuonSelection == True:
                                    config[key]["processJpsiToMuMuVertexingSkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                if isMuonSelection == False:
                                    logging.error("muonSelection not found in analysis for processJpsiToMuMuVertexingSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'JpsiToMuMuVertexing' not in valueCfg and value == "processJpsiToMuMuVertexingSkimmed":
                                config[key]["processJpsiToMuMuVertexingSkimmed"] = 'false'
                                logging.debug(" - [%s] %s : false",key,value)
                                
                            if 'ElectronMuon' in valueCfg and value == "processElectronMuonSkimmed":
                                if isTrackSelection == True and isMuonSelection == True:
                                    config[key]["processElectronMuonSkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                else:
                                    logging.error("trackSelection and muonSelection not found in analysis for processElectronMuonSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'ElectronMuon' not in valueCfg and value == "processElectronMuonSkimmed":
                                config[key]["processElectronMuonSkimmed"] = 'false'
                                logging.debug(" - [%s] %s : false",key,value)
                                
                            if 'All' in valueCfg and value == "processAllSkimmed":
                                if isEventSelection == True and isMuonSelection == True and isTrackSelection == True:
                                    config[key]["processAllSkimmed"] = 'true'
                                    logging.debug(" - [%s] %s : true",key,value)
                                else:
                                    logging.debug("eventSelection, trackSelection and muonSelection not found in analysis for processAllSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'All' not in valueCfg and value == "processAllSkimmed":
                                config[key]["processAllSkimmed"] = 'false'
                                logging.debug(" - [%s] %s : false",key,value)
                                
                        if key == 'analysis-same-event-pairing' and extrargs.process == None and isSameEventPairing == False:
                            config[key]["processJpsiToEESkimmed"] = 'false'
                            config[key]["processJpsiToMuMuSkimmed"] = 'false'
                            config[key]["processJpsiToMuMuVertexingSkimmed"] = 'false'
                            config[key]["processElectronMuonSkimmed"] = 'false'
                            config[key]["processAllSkimmed"] = 'false'
                            
  
            
            """
            if extrargs.processSameEventPairing == 'true': # Automate activated
                
                # Track automate
                if config["analysis-track-selection"]["processSkimmed"] == 'true':
                    config["analysis-same-event-pairing"]["processJpsiToEESkimmed"] = 'true'  
                                
                if config["analysis-track-selection"]["processSkimmed"] == 'false':
                    config["analysis-same-event-pairing"]["processJpsiToEESkimmed"] = 'false'    
                    
                # Muon automate     
                if config["analysis-muon-selection"]["processSkimmed"] == 'true':
                    config["analysis-same-event-pairing"]["processJpsiToMuMuSkimmed"] = 'true'
                    config["analysis-same-event-pairing"]["processJpsiToMuMuVertexingSkimmed"] = 'false'
                    if extrargs.isVertexing == 'true':
                        config["analysis-same-event-pairing"]["processJpsiToMuMuSkimmed"] = 'false'
                        config["analysis-same-event-pairing"]["processJpsiToMuMuVertexingSkimmed"] = 'true'
                                
                if config["analysis-muon-selection"]["processSkimmed"] == 'false':
                    config["analysis-same-event-pairing"]["processJpsiToMuMuSkimmed"] = 'false'
                    config["analysis-same-event-pairing"]["processJpsiToMuMuVertexingSkimmed"] = 'false'
                    
                # Event Mixing automate
                if config["analysis-event-mixing"]["processBarrelMuonSkimmed"] == 'true':
                    config["analysis-same-event-pairing"]["processElectronMuonSkimmed"] = 'true'  
                  
                if config["analysis-event-mixing"]["processBarrelMuonSkimmed"] == 'false':
                     config["analysis-same-event-pairing"]["processElectronMuonSkimmed"] = 'false'  
                                
            if extrargs.processSameEventPairing == 'false': # Automate disabled
                continue
            """
            
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
                    
                if config["analysis-same-event-pairing"]["processJpsiToEESkimmed"] == "true" or config["analysis-same-event-pairing"]["processJpsiToMuMuSkimmed"] == "true" or config["analysis-same-event-pairing"]["processJpsiToMuMuVertexingSkimmed"] == "true" or config["analysis-same-event-pairing"]["processElectronMuonSkimmed"] == "true" or config["analysis-same-event-pairing"]["processAllSkimmed"] == "true":
                    config["analysis-same-event-pairing"]["processDummy"] = "false"
                            
                if config["analysis-same-event-pairing"]["processJpsiToEESkimmed"] == "false" and config["analysis-same-event-pairing"]["processJpsiToMuMuSkimmed"] == "false" and config["analysis-same-event-pairing"]["processJpsiToMuMuVertexingSkimmed"] == "false" and config["analysis-same-event-pairing"]["processElectronMuonSkimmed"] == "false" and config["analysis-same-event-pairing"]["processAllSkimmed"] == "false":
                    config["analysis-same-event-pairing"]["processDummy"] = "true"
                    
                if config["analysis-dilepton-hadron"]["processSkimmed"] == "true":
                    config["analysis-dilepton-hadron"]["processDummy"] = "false"
                if config["analysis-dilepton-hadron"]["processSkimmed"] == "false":
                    config["analysis-dilepton-hadron"]["processDummy"] = "true"
                            
# AOD and JSON Reader File Checker
                
if extrargs.aod != None:
    if os.path.isfile(extrargs.aod) == False:
        logging.error("%s File not found in path!!!",extrargs.aod)
        sys.exit()
elif os.path.isfile((config["internal-dpl-aod-reader"]["aod-file"])) == False:
        print("[ERROR]",config["internal-dpl-aod-reader"]["aod-file"],"File not found in path!!!")
        sys.exit()
        
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
#if isDileptonHadronAnalysis == True:
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
