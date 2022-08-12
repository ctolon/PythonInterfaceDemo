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
import json
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
    
mixingDatabaseJSON: JSON
    mixingDatabaseJSON is a JSON file for take the event mixing selection parameters
    
mixingDatabase: list
    mixingDatabase is a List for take Event Mixing Selections from JSON database    

analysisCutDatabaseJSON = json.load(open('Database/AnalysisCutDatabase.json'))
MCSignalDatabaseJSON = json.load(open('Database/MCSignalDatabase.json'))
mixingDatabaseJSON = json.load(open('Database/MixingDatabase.json'))
analysisCutDatabase = []
MCSignalDatabase =[]
mixingDatabase = []

# control list for type control
clist=[]

# Cut Database
for key, value in analysisCutDatabaseJSON.items():
    analysisCutDatabase.append(value)

# MCSignal Database
for key, value in MCSignalDatabaseJSON.items():
    MCSignalDatabase.append(value)
    
# Event Mixing Selection Database
for key, value in mixingDatabaseJSON.items():
    mixingDatabase.append(value)
    
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

isSameEventPairing = False

readerPath = 'Configs/readerConfiguration_reducedEvent.json'
writerPath = 'Configs/writerConfiguration_dileptons.json'

# Github Links for CutsLibrary and MCSignalsLibrary from PWG-DQ --> download from github
# This condition solves performance issues
if (os.path.isfile('tempCutsLibrary.h') == False) or (os.path.isfile('tempMixingLibrary.h') == False):
    urlCutsLibrary = 'https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/CutsLibrary.h'
    urlEventMixing ='https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/MixingLibrary.h'

    urllib.request.urlretrieve(urlCutsLibrary,"tempCutsLibrary.h")
    urllib.request.urlretrieve(urlEventMixing,"tempMixingLibrary.h")


clist=[] # control list for type control
allValuesCfg = [] # counter for provided args
allCuts = []
allMixing = []

#AnalysisCutsPath = os.path.expanduser("~/alice/O2Physics/PWGDQ/Core/CutsLibrary.h")
#EventMixingPath = os.path.expanduser("~/alice/O2Physics/PWGDQ/Core/MixingLibrary.h")

O2DPG_ROOT=os.environ.get('O2DPG_ROOT')
QUALITYCONTROL_ROOT=os.environ.get('QUALITYCONTROL_ROOT')
O2_ROOT=os.environ.get('O2_ROOT')
O2PHYSICS_ROOT=os.environ.get('O2PHYSICS_ROOT')

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

"""
with open(EventMixingPath) as f:
    for line in f:
        stringIfSearch = [x for x in f if 'if' in x] 
        for i in stringIfSearch:
            getMixing = re.findall('"([^"]*)"', i)
            allMixing = allMixing + getMixing
    
with open(AnalysisCutsPath) as f:
    for line in f:
        stringIfSearch = [x for x in f if 'if' in x] 
        for i in stringIfSearch:
            getAnalysisCuts = re.findall('"([^"]*)"', i)
            allCuts = allCuts + getAnalysisCuts

"""

#print(allCuts)
#print(allMixing)
    
###################
# Main Parameters #
###################
    
parser = argparse.ArgumentParser(description='Arguments to pass')
parser.add_argument('cfgFileName', metavar='text', default='config.json', help='config file name')

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
parser.add_argument('--isMixingEvent', help="analysis-event-mixing: process function activate for event mixing", action="store", choices=['true','false'], default='true', type=str.lower)
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


"""Activate For Autocomplete. See to Libraries for Info"""
argcomplete.autocomplete(parser)
extrargs = parser.parse_args()

configuredCommands = vars(extrargs) # for get extrargs


# Make some checks on provided arguments
if len(sys.argv) < 2:
  print("ERROR: Invalid syntax! The command line should look like this:")
  print("  ./IRunTableReader.py <yourConfig.json> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
config = {}
with open(sys.argv[1]) as configFile:
  config = json.load(configFile)


taskNameInCommandLine = "o2-analysis-dq-table-reader"

# Check alienv
if O2PHYSICS_ROOT == None:
   print("[ERROR] You must load O2Physics with alienv")
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
            # reader    
            if value =='aod-reader-json' and extrargs.reader:
                config[key][value] = extrargs.reader
                
            # analysis-skimmed-selections
            if value =='processSkimmed' and extrargs.analysis:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-selection':
                                if 'eventSelection' in valueCfg:
                                    config[key][value] = 'true'
                                if 'eventSelection' not in valueCfg:
                                    config[key][value] = 'false' 
                                   
                            if key == 'analysis-track-selection':                  
                                if 'trackSelection' in valueCfg:
                                    config[key][value] = 'true'
                                if 'trackSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                                        
                            if key == 'analysis-muon-selection':
                                if 'muonSelection' in valueCfg:
                                    config[key][value] = 'true'
                                if 'muonSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                                                                
                            if key == 'analysis-dilepton-hadron':
                                if 'dileptonHadronSelection' in valueCfg:
                                    config[key][value] = 'true'
                                if 'dileptonHadronSelection' not in valueCfg:
                                    config[key][value] = 'false'
                                    
                            if 'sameEventPairing' in valueCfg:
                                isSameEventPairing = True
                            if 'sameEventPairing' not in valueCfg:
                                isSameEventPairing = False
                                    
            # Analysis Event Mixing Selections
            if value == 'processBarrelSkimmed' or value == 'processMuonSkimmed' or value == 'processBarrelMuonSkimmed' and extrargs.isMixingEvent:                        
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Skipped None types, because can't iterate in None type
                        if keyCfg == 'analysis': #  Only Select key for analysis
                            
                            if key == 'analysis-event-mixing' and extrargs.isMixingEvent == 'true':                             
                                if 'trackSelection' in valueCfg:
                                    config[key]["processBarrelSkimmed"] = 'true'
                                if 'trackSelection' not in valueCfg:
                                    config[key]["processBarrelSkimmed"] = 'false'
                                    
                                if 'muonSelection' in valueCfg:
                                    config[key]["processMuonSkimmed"] = 'true'
                                if 'muonSelection' not in valueCfg:
                                    config[key]["processMuonSkimmed"] = 'false'
                                    
                                if 'trackSelection' in valueCfg and 'muonSelection' in valueCfg:
                                    config[key]["processBarrelMuonSkimmed"] = 'true'
                                if 'trackSelection' not in valueCfg or 'muonSelection' not in valueCfg:
                                    config[key]["processBarrelMuonSkimmed"] = 'false'
                                           
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
                
            # Process All Skimmed Selection
            #if value =='processAllSkimmed' and extrargs.analysisAllSkimmed:
                #config[key][value] = extrargs.analysisAllSkimmed
                              
            # analysis-event-selection
            if value == 'cfgMixingVars' and extrargs.cfgMixingVars:
                if type(extrargs.cfgMixingVars) == type(clist):
                    extrargs.cfgMixingVars = listToString(extrargs.cfgMixingVars) 
                config[key][value] = extrargs.cfgMixingVars
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts) 
                config[key][value] = extrargs.cfgEventCuts

            # analysis-track-selection
            if value =='cfgTrackCuts' and extrargs.cfgTrackCuts:
                if type(extrargs.cfgTrackCuts) == type(clist):
                    extrargs.cfgTrackCuts = listToString(extrargs.cfgTrackCuts) 
                config[key][value] = extrargs.cfgTrackCuts
                
            # analysis-muon-selection
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                if type(extrargs.cfgMuonCuts) == type(clist):
                    extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts) 
                config[key][value] = extrargs.cfgMuonCuts
                
            # analysis-dilepton-hadron
            if value =='cfgLeptonCuts' and extrargs.cfgLeptonCuts:
                if type(extrargs.cfgLeptonCuts) == type(clist):
                    extrargs.cfgLeptonCuts = listToString(extrargs.cfgLeptonCuts) 
                config[key][value] = extrargs.cfgLeptonCuts
            
            # analysis-same-event-pairing
            for keyCfg,valueCfg in configuredCommands.items():
                if(valueCfg != None): # Skipped None types, because can't iterate in None type
                    if keyCfg == 'process' or keyCfg == 'analysis': # Select analysis and process keys
                        if key == 'analysis-same-event-pairing' and extrargs.process:
                            if isSameEventPairing == False:
                                print("[WARNING] You forget to add sameEventPairing option to analysis for Workflow. It Automatically added by CLI.")
                                isSameEventPairing = True
                            allValuesCfg = allValuesCfg + valueCfg # Merge process and analysis arguments provided options as a list
                    
                            if 'JpsiToEE' in valueCfg:
                                if 'trackSelection' in allValuesCfg:
                                    config[key]["processJpsiToEESkimmed"] = 'true'
                                if 'trackSelection' not in allValuesCfg:
                                    print("[ERROR] trackSelection not found in analysis for processJpsiToEESkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'JpsiToEE' not in valueCfg:
                                    config[key]["processJpsiToEESkimmed"] = 'false'
                                    
                            if 'JpsiToMuMu' in valueCfg:
                                if 'muonSelection' in allValuesCfg:
                                    config[key]["processJpsiToMuMuSkimmed"] = 'true'
                                if 'muonSelection' not in allValuesCfg:
                                    print("[ERROR] muonSelection not found in analysis for processJpsiToMuMuSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'JpsiToMuMu' not in valueCfg:
                                config[key]["processJpsiToMuMuSkimmed"] = 'false'
   
                            if 'JpsiToMuMuVertexing' in valueCfg:
                                if 'muonSelection' in allValuesCfg:
                                    config[key]["processJpsiToMuMuVertexingSkimmed"] = 'true'
                                if 'muonSelection' not in allValuesCfg:
                                    print("[ERROR] muonSelection not found in analysis for processJpsiToMuMuVertexingSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'JpsiToMuMuVertexing' not in valueCfg:
                                config[key]["processJpsiToMuMuVertexingSkimmed"] = 'false'
                                
                            if 'ElectronMuon' in valueCfg:
                                if 'muonSelection' in allValuesCfg and 'trackSelection' in allValuesCfg:
                                    config[key]["processElectronMuonSkimmed"] = 'true'
                                if 'muonSelection' not in allValuesCfg and 'trackSelection' not in allValuesCfg:
                                    print("[ERROR] trackSelection and muonSelection not found in analysis for processElectronMuonSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'ElectronMuon' not in valueCfg:
                                config[key]["processElectronMuonSkimmed"] = 'false'
                                
                            if 'All' in valueCfg:
                                if 'muonSelection' in allValuesCfg and 'trackSelection' in allValuesCfg and 'eventSelection' in allValuesCfg:
                                    config[key]["processAllSkimmed"] = 'true'
                                if 'muonSelection' not in allValuesCfg and 'trackSelection' not in allValuesCfg and 'eventSelection' not in allValuesCfg:
                                    print("[ERROR] eventSelection, trackSelection and muonSelection not found in analysis for processAllSkimmed -> analysis-same-event-pairing")
                                    sys.exit()
                            if 'All' not in valueCfg:
                                config[key]["processAllSkimmed"] = 'false'
                                
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
        print("[ERROR]",extrargs.aod,"File not found in path!!!")
        sys.exit()
elif os.path.isfile((config["internal-dpl-aod-reader"]["aod-file"])) == False:
        print("[ERROR]",config["internal-dpl-aod-reader"]["aod-file"],"File not found in path!!!")
        sys.exit()
        
if extrargs.reader != None:
    if os.path.isfile(extrargs.reader) == False:
        print("[ERROR]",extrargs.reader,"File not found in path!!!")
        sys.exit()
elif os.path.isfile((config["internal-dpl-aod-reader"]["aod-reader-json"])) == False:
        print("[ERROR]",config["internal-dpl-aod-reader"]["aod-reader-json"],"File not found in path!!!")
        sys.exit()

###########################
# End Interface Processes #
###########################              


# Write the updated configuration file into a temporary file
updatedConfigFileName = "tempConfigTableReader.json"

"""
Transaction Management for Json File Name

if(extrargs.outputjson == None):       
    config_output_json = open(updatedConfigFileName,'w')
    config_output_json.write(json.dumps(config, indent= 2))
    print("[WARNING] Forget to Give output JSON name. Output JSON will created as tempConfig.json")
elif(extrargs.outputjson[-5:] == ".json"):
    updatedConfigFileName = extrargs.outputjson
    config_output_json = open(updatedConfigFileName,'w')
    config_output_json.write(json.dumps(config, indent= 2))
elif(extrargs.outputjson[-5:] != ".json"):
    if '.' in extrargs.outputjson:
        print("[ERROR] Wrong formatted input for JSON output!!! Script will Stopped.")
        sys.exit()
    temp = extrargs.outputjson
    temp = temp+'.json'
    updatedConfigFileName = temp
    config_output_json = open(updatedConfigFileName,'w')
    config_output_json.write(json.dumps(config, indent= 2))
else:
    print("Logical json input error. Report it!!!")
       
"""
with open(updatedConfigFileName,'w') as outputFile:
  json.dump(config, outputFile ,indent=2)
      
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --aod-writer-json " + extrargs.writer + " -b"

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
