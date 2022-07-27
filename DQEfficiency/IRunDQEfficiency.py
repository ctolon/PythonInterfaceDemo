#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
#############################################################################
##  © Copyright CERN 2018. All rights not expressly granted are reserved.  ##
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

"""
argcomplete - Bash tab completion for argparse
Documentation https://kislyuk.github.io/argcomplete/
Instalation Steps
pip install argcomplete
sudo activate-global-python-argcomplete
Only Works On Local not in O2
Activate libraries in below and activate #argcomplete.autocomplete(parser) line
"""
#import argcomplete  
#from argcomplete.completers import ChoicesCompleter

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
"""
json_cut_database = json.load(open('AnalysisCutDatabase.json'))
json_mcsignal_database = json.load(open('MCSignalDatabase.json'))
cut_database = []
mcsignal_database =[]

# control list for type control
clist=[]

# Cut Database
for key, value in json_cut_database.items():
    cut_database.append(value)

# MCSignal Database
for key, value in json_mcsignal_database.items():
    mcsignal_database.append(value)
    
    
    
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
    
def stringToList(string):
    li = list(string.split(" "))
    return li

readerPath = 'Configs/readerConfiguration_reducedEventMC.json'
    
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


# json output
parser.add_argument('--outputjson', help="Your Output JSON Config Fİle", action="store", type=str)

# Skimmed process Dummy Selections for analysis
# todo: add skimmed for same event and dilepton
parser.add_argument('--analysisSkimmed', help="Process Selection options true or false (string)", action="store", choices=['event','track','muon','dimuonMuon'], nargs='*', type=str)
parser.add_argument('--analysisDummy', help="Process Selection options true or false (string)", action="store", choices=['event','track','muon','sameEventPairing','dilepton'], nargs='*', type=str)

# cfg for QA
parser.add_argument('--cfgQA', help="QA Selection true or false", action="store", choices=["true","false"], type=str.lower)

# analysis-event-selection
parser.add_argument('--cfgEventCuts', help="Configure Cuts with spaces", choices=cut_database,nargs='*', action="store", type=str)

# analysis-track-selection
parser.add_argument('--cfgTrackCuts', help="Configure Cuts with spaces", choices=cut_database,nargs='*', action="store", type=str)
parser.add_argument('--cfgTrackMCSignals', help="Configure Cuts with spaces", choices=mcsignal_database,nargs='*', action="store", type=str)

# analysis-muon-selection
parser.add_argument('--cfgMuonCuts', help="Configure Cuts with spaces", choices=cut_database,nargs='*', action="store", type=str)
parser.add_argument('--cfgMuonMCSignals', help="Configure Cuts with spaces", choices=mcsignal_database,nargs='*', action="store", type=str)

# analysis-same-event-pairing
parser.add_argument('--processSameEventPairing', help="Process Selection options true or false (string)", action="store", choices=['true','false'], default='true', type=str.lower)
parser.add_argument('--isVertexing', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str.lower)

parser.add_argument('--cfgBarrelMCRecSignals', help="Configure Cuts with spaces", choices=mcsignal_database,nargs='*', action="store", type=str)
parser.add_argument('--cfgBarrelMCGenSignals', help="Configure Cuts with spaces", choices=mcsignal_database,nargs='*', action="store", type=str)


# analysis-dilepton-track ONLY FOR MC TODO: cfgLeptoncuts and cfgFillCandidateTable can be added.

parser.add_argument('--cfgBarrelDileptonMCRecSignals', help="Configure Cuts with spaces", choices=mcsignal_database,nargs='*', action="store", type=str)
parser.add_argument('--cfgBarrelDileptonMCGenSignals', help="Configure Cuts with spaces", choices=mcsignal_database,nargs='*', action="store", type=str)

"""Activate For Autocomplete. See to Libraries for Info"""
#argcomplete.autocomplete(parser)
extrargs = parser.parse_args()

configuredCommands = vars(extrargs) # for get extrargs



#commonDeps = ["o2-analysis-timestamp", "o2-analysis-event-selection", "o2-analysis-multiplicity-table", "o2-analysis-trackselection", "o2-analysis-track-propagation", "o2-analysis-pid-tof-base", "o2-analysis-pid-tof", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]

# Make some checks on provided arguments
if len(sys.argv) < 2:
  print("ERROR: Invalid syntax! The command line should look like this:")
  print("  ./IRunDQEfficiency.py <yourConfig.json> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
#TODO: Config file gerçekten pathimizde var mı? bunun için transacation management yaz.
config = {}
with open(sys.argv[1]) as configFile:
  config = json.load(configFile)

taskNameInCommandLine = "o2-analysis-dq-efficiency"

"""
if not taskNameInConfig in config:
  print("ERROR: Task to be run not found in the configuration file!")
  sys.exit()
"""

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
            if value =='processSkimmed' and extrargs.analysisSkimmed:
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'analysisSkimmed': #  Only Select key for skimmed
                            
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
                                    
                            if key == 'analysis-dilepton-track':
                                if 'dimuonMuon' in valueCfg:
                                    config[key][value] = 'true'
                                if 'dimuonMuon' not in valueCfg:
                                    config[key][value] = 'false' 
                                            
            # analysis-dummy-selections
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
                                    
                            if key == 'analysis-same-event-pairing':
                                if 'sameEventPairing' in valueCfg:
                                    config[key][value] = 'true'
                                if 'sameEventPairing' not in valueCfg:
                                    config[key][value] = 'false'  

                            if key == 'analysis-dilepton-track':
                                if 'dilepton' in valueCfg:
                                    config[key][value] = 'true'
                                if 'dilepton' not in valueCfg:
                                    config[key][value] = 'false' 
                 
            # QA selections  
            if value =='cfgQA' and extrargs.cfgQA:
                config[key][value] = extrargs.cfgQA
                              
            # analysis-event-selection
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                extrargs.cfgEventCuts = ",".join(extrargs.cfgEventCuts)
                config[key][value] = extrargs.cfgEventCuts

            # analysis-track-selection
            if value =='cfgTrackCuts' and extrargs.cfgTrackCuts:
                extrargs.cfgTrackCuts = ",".join(extrargs.cfgTrackCuts)
                config[key][value] = extrargs.cfgTrackCuts
            if value == 'cfgTrackMCSignals' and extrargs.cfgTrackMCSignals:
                extrargs.cfgTrackMCSignals = ",".join(extrargs.cfgTrackMCSignals)
                config[key][value] = extrargs.cfgTrackMCSignals
                
            # analysis-muon-selection
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                config[key][value] = extrargs.cfgMuonCuts
            if value == 'cfgMuonMCSignals' and extrargs.cfgMuonMCSignals:
                extrargs.cfgMuonMCSignals = ",".join(extrargs.cfgMuonMCSignals)
                config[key][value] = extrargs.cfgMuonMCSignals
            
            # analysis-same-event-pairing
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
                
            if extrargs.processSameEventPairing == 'false': # Automate disabled
                continue

            # MC Signals For Same Event Pairing
            if key == 'analysis-same-event-pairing':
                if value == 'cfgBarrelMCRecSignals' and extrargs.cfgBarrelMCRecSignals:
                    extrargs.cfgBarrelMCRecSignals = ",".join(extrargs.cfgBarrelMCRecSignals)
                    config[key][value] = extrargs.cfgBarrelMCRecSignals
                if value == 'cfgBarrelMCGenSignals' and extrargs.cfgBarrelMCGenSignals:
                    extrargs.cfgBarrelMCGenSignals = ",".join(extrargs.cfgBarrelMCGenSignals)
                    config[key][value] = extrargs.cfgBarrelMCGenSignals
                
            # MC Signals For Dilepton Tracks
            if key == 'analysis-dilepton-track':
                if value == 'cfgDileptonBarrelMCRecSignals' and extrargs.cfgDileptonBarrelMCRecSignals:
                    extrargs.cfgBarrelDileptonMCRecSignals = ",".join(extrargs.cfgBarrelDileptonMCRecSignals)
                    config[key][value] = extrargs.cfgBarrelDileptonMCRecSignals
                if value == 'cfgBarrelMCGenSignals' and extrargs.cfgDileptonBarrelMCGenSignals:
                    extrargs.cfgBarrelDileptonMCGenSignals = ",".join(extrargs.cfgBarrelDileptonMCGenSignals)
                    config[key][value] = extrargs.cfgDileptonBarrelMCGenSignals
        
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
updatedConfigFileName = "tempConfig.json"

"""
#Transaction Management for Json File Name
"""
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
    
#with open(updatedConfigFileName,'w') as outputFile:
  #json.dump(config, outputFile ,indent=2)

# Check which dependencies need to be run

#depsToRun = {}
#for dep in commonDeps:
  #depsToRun[dep] = 1

      
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " -aod-memory-rate-limit 1000000000" + " --aod-reader-json://" + extrargs.reader + " -b"

#for dep in depsToRun.keys():
#commandToRun += " | " + dep + " --configuration json://" + updatedConfigFileName + " -b"


print("====================================================================================================================")
print("Command to run:")
print(commandToRun)
print("====================================================================================================================")
os.system(commandToRun)

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
