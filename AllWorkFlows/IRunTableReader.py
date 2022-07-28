#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
#############################################################################
##  © Copyright CERN 2018. All rights not expressly granted are reserved.  ## 
#               Author: cevat.batuhan.tolon@cern.ch                        ##
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
    
mixingDatabase: list
    mixingDatabase is a List for take Event Mixing Selections from JSON database    
"""
json_cut_database = json.load(open('Database/AnalysisCutDatabase.json'))
json_mcsignal_database = json.load(open('Database/MCSignalDatabase.json'))
json_mixing_database = json.load(open('Database/MixingDatabase.json'))
cut_database = []
mcsignal_database =[]
mixing_database = []

# control list for type control
clist=[]

# Cut Database
for key, value in json_cut_database.items():
    cut_database.append(value)

# MCSignal Database
for key, value in json_mcsignal_database.items():
    mcsignal_database.append(value)
    
# Event Mixing Selection Database
for key, value in json_mixing_database.items():
    mixing_database.append(value)
    
    
    
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

readerPath = 'Configs/readerConfiguration_reducedEvent.json'
writerPath = 'Config/writerConfiguration_dileptons.json'

eventMixingSkimmedList = ["processBarrelSkimmed", "processMuonSkimmed", "processBarrelMuonSkimmed" ]
eventMixingSkimmedfalseCounter = 0 # We have 3 Skimmed process for event mixing. We count all false values for automate
    
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
parser.add_argument('--writer', help="Add your AOD Reader JSON with path", action="store", default=writerPath, type=str)

#json output
parser.add_argument('--outputjson', help="Your Output JSON Config Fİle", action="store", type=str)

# Skimmed processes and Dummy Selections for analysis
parser.add_argument('--analysisSkimmed', help="Process Selection options true or false (string)", action="store", choices=['event','muon','track','eventMixingBarrel','eventMixingMuon','eventMixingBarrelMuon','dileptonHadron'], nargs='*', type=str)
parser.add_argument('--analysisDummy', help="Process Selection options true or false (string)", action="store", choices=['event','muon','track','eventMixing','sameEventPairing','dileptonHadron'], nargs='*', type=str)
parser.add_argument('--analysisAllSkimmed', help="QA Selection true or false", action="store", choices=["true","false"], default=["false"], type=str.lower)

# cfg for QA
parser.add_argument('--cfgQA', help="QA Selection true or false", action="store", choices=["true","false"], type=str.lower)

# analysis-event-selection
parser.add_argument('--cfgMixingVars', help="Configure Cuts with spaces", choices=mixing_database, nargs='*', action="store", type=str)
parser.add_argument('--cfgEventCuts', help="Configure Cuts with spaces", choices=cut_database,nargs='*', action="store", type=str)

# analysis-muon-selection
parser.add_argument('--cfgMuonCuts', help="Configure Cuts with spaces", choices=cut_database,nargs='*', action="store", type=str)

# analysis-track-selection
parser.add_argument('--cfgTrackCuts', help="Configure Cuts with spaces", choices=cut_database,nargs='*', action="store", type=str)

# analysis-event-mixing
# see in skimmed options and cuts are configured in muon and track selection

# analysis-same-event-pairing TODO: CCDB parts Can be added
parser.add_argument('--processSameEventPairing', help="Process Selection options true or false (string)", action="store", choices=['true','false'], default='true', type=str.lower)
parser.add_argument('--isVertexing', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str.lower)


# analysis-dilepton-hadron
parser.add_argument('--cfgLeptonCuts', help="Configure Cuts with spaces", choices=cut_database,nargs='*', action="store", type=str)


"""Activate For Autocomplete. See to Libraries for Info"""
#argcomplete.autocomplete(parser)
extrargs = parser.parse_args()

configuredCommands = vars(extrargs) # for get extrargs


# Make some checks on provided arguments
if len(sys.argv) < 2:
  print("ERROR: Invalid syntax! The command line should look like this:")
  print("  ./IRunTableReader.py <yourConfig.json> --param value ...")
  sys.exit()

# Load the configuration file provided as the first parameter
#TODO: Config file gerçekten pathimizde var mı? bunun için transacation management yaz.
config = {}
with open(sys.argv[1]) as configFile:
  config = json.load(configFile)


taskNameInCommandLine = "o2-analysis-dq-table-reader"







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
                                                                                
                            if key == 'analysis-dilepton-hadron':
                                if 'dileptonHadron' in valueCfg:
                                    config[key][value] = 'true'
                                if 'dileptonHadron' not in valueCfg:
                                    config[key][value] = 'false'
                                    
            # Analysis Event Mixing Selections #TODO :Refactor
            if value == 'processBarrelSkimmed' or value == 'processMuonSkimmed' or value == 'processBarrelMuonSkimmed' and extrargs.analysisSkimmed:                        
                for keyCfg,valueCfg in configuredCommands.items():
                    if(valueCfg != None): # Cleaning None types, because can't iterate in None type
                        if keyCfg == 'analysisSkimmed': #  Only Select key for skimmed
                            
                            if key == 'analysis-event-mixing':
                                if 'eventMixingBarrel' in valueCfg:
                                    config[key]["processBarrelSkimmed"] = 'true'
                                    #print("Key: ",key," Value: ", value)
                                if 'eventMixingBarrel' not in valueCfg:
                                    config[key]["processBarrelSkimmed"] = 'false:'
                                    
                                if 'eventMixingMuon' in valueCfg:
                                    config[key]["processMuonSkimmed"] = 'true'
                                if 'eventMixingMuon' not in valueCfg:
                                    config[key]["processMuonSkimmed"] = 'false'
                                    
                                if 'eventMixingBarrelMuon' in valueCfg:
                                    config[key]["processBarrelMuonSkimmed"] = 'true'
                                if 'eventMixingBarrelMuon' not in valueCfg:
                                    config[key]["processBarrelMuonSkimmed"] = 'false'
                                           
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
                 
            # QA selections  
            if value =='cfgQA' and extrargs.cfgQA:
                config[key][value] = extrargs.cfgQA
                
            # Process All SKimmed Selection
            if value =='processAllSkimmed' and extrargs.analysisAllSkimmed:
                config[key][value] = extrargs.analysisAllSkimmed
                              
            # analysis-event-selection
            if value == 'cfgMixingVars' and extrargs.cfgMixingVars:
                extrargs.cfgMixingVars = ",".join(extrargs.cfgMixingVars)
                config[key][value] = extrargs.cfgMixingVars
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                extrargs.cfgEventCuts = ",".join(extrargs.cfgEventCuts)
                config[key][value] = extrargs.cfgEventCuts

            # analysis-track-selection
            if value =='cfgTrackCuts' and extrargs.cfgTrackCuts:
                extrargs.cfgTrackCuts = ",".join(extrargs.cfgTrackCuts)
                config[key][value] = extrargs.cfgTrackCuts
                
            # analysis-muon-selection
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                config[key][value] = extrargs.cfgMuonCuts
                
            # analysis-dilepton-hadron
            if value =='cfgLeptonCuts' and extrargs.cfgLeptonCuts:
                extrargs.cfgLeptonCuts = ",".join(extrargs.cfgLeptonCuts)
                config[key][value] = extrargs.cfgLeptonCuts
            
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
                    
                # Event Mixing automate
                if config["analysis-event-mixing"]["processBarrelMuonSkimmed"] == 'true':
                    config["analysis-same-event-pairing"]["processElectronMuonSkimmed"] = 'true'  
                  
                if config["analysis-event-mixing"]["processBarrelMuonSkimmed"] == 'false':
                     config["analysis-same-event-pairing"]["processElectronMuonSkimmed"] = 'false'  
                                
            if extrargs.processSameEventPairing == 'false': # Automate disabled
                continue
                            
# AOD and JSON Reader File Checker #TODO: add .root checker like jsons
                
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
