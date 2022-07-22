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

import json
import sys
import logging
from ast import parse
import os
import argparse
#import argcomplete  
#from argcomplete.completers import ChoicesCompleter

# DEMO Python Interface for runTableMaker.py

# Function to convert 
def listToString(s):
    if len(s) > 1:
        # initialize an empty string
        str1 =" "
   
        # return string 
        return (str1.join(s))
    else:
        str1 = " "
        
        return (str1.join(s))

json_cut_database = json.load(open('AnalysisCutDatabase.json'))
json_mcsignal_database = json.load(open('MCSignalDatabase.json'))
cut_database = []
mcsignal_database =[]

# Cut Database
for key, value in json_cut_database.items():
    cut_database.append(value)

# MCSignal Database
for key, value in json_mcsignal_database.items():
    mcsignal_database.append(value)
    


parser = argparse.ArgumentParser(description='Arguments to pass')

# aod
parser.add_argument('--aod', help="Add your AOD File with path", action="store", type=str)

#json output
parser.add_argument('--outputjson', help="Your Output JSON Config Fİle", action="store", type=str)

# analysis-event-selection
## For Only Data
parser.add_argument('--cfgMixingVars', help="Configure Cuts with commas", choices=cut_database, nargs='*', action="store", type=str)
## For Both MC And Data
parser.add_argument('--cfgEventCuts', help="Configure Cuts with commas", choices=cut_database,nargs='*', action="store", type=str)
parser.add_argument('--cfgQA', help="QA Selection true or false", action="store", choices=["true","false"], type=str)
parser.add_argument('--processSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# analysis-muon-selection
## For Both MC And Data
parser.add_argument('--cfgMuonCuts', help="Configure Cuts with commas", choices=cut_database,nargs='*', action="store", type=str)
## For MC
parser.add_argument('--cfgMuonMCSignals', help="Configure Cuts with commas", choices=mcsignal_database,nargs='*', action="store", type=str)
## For Both MC And Data
#parser.add_argument('--cfgQA', help="QA Selection true or false", action="store", choices=["true","false"], type=str)
#parser.add_argument('--processSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
#parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# analysis-track-selection
## For Both MC And Data
parser.add_argument('--cfgTrackCuts', help="Configure Cuts with commas", choices=cut_database,nargs='*', action="store", type=str)
## For MC
parser.add_argument('--cfgTrackMCSignals', help="Configure Cuts with commas", choices=mcsignal_database,nargs='*', action="store", type=str)
## For Both MC And Data
#parser.add_argument('--cfgQA', help="QA Selection true or false", action="store", choices=["true","false"], type=str)
#parser.add_argument('--processSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
#parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# analysis-event-mixing ONLY FOR DATA
#parser.add_argument('--cfgTrackCuts', help="Configure Cuts with commas", choices=cut_database, nargs='*', action="store", type=str)
#parser.add_argument('--cfgMuonCuts', help="Configure Cuts with commas", choices=cut_database,nargs='*', action="store", type=str)
parser.add_argument('--processBarrelSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processMuonSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processBarrelMuonSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
#parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# analysis-same-event-pairing TODO: CCDB parts Can be added
## For Both MC And Data
#parser.add_argument('--cfgTrackCuts', help="Configure Cuts with commas", choices=cut_database, nargs='*', action="store", type=str)
#parser.add_argument('--cfgMuonCuts', help="Configure Cuts with commas", choices=cut_database,nargs='*', action="store", type=str)
## FOR MC
parser.add_argument('--cfgBarrelMCRecSignals', help="Configure Cuts with commas", choices=mcsignal_database,nargs='*', action="store", type=str)
parser.add_argument('--cfgBarrelMCGenSignals', help="Configure Cuts with commas", choices=mcsignal_database,nargs='*', action="store", type=str)
## For Both MC And Data
parser.add_argument('--processJpsiToEESkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processJpsiToMuMuSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processJpsiToMuMuVertexingSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
## For Data
parser.add_argument('--processElectronMuonSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processAllSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
## For Both MC And Data
#parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# analysis-dilepton-hadron ONLY FOR DATA
parser.add_argument('--cfgLeptonCuts', help="Configure Cuts with commas", choices=cut_database,nargs='*', action="store", type=str)
#parser.add_argument('--processSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
#parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# analysis-dilepton-track ONLY FOR MC
#parser.add_argument('--cfgBarrelMCRecSignals', help="Configure Cuts with commas", choices=mcsignal_database,nargs='*', action="store", type=str)
#parser.add_argument('--cfgBarrelMCGenSignals', help="Configure Cuts with commas", choices=mcsignal_database,nargs='*', action="store", type=str)
#parser.add_argument('--processSkimmed', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
#parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

extrargs = parser.parse_args()

#Open JSON File
json_dict = json.load(open('configAnalysisData.json'))

json_dict_new = json_dict


def get_key(json_dict_new):
    my_json = 'ConfiguredTableReaderData.json'
    json_dict = json.load(open('configAnalysisData.json'))
    #json_dict = json.load(open('data.json'))
    json_dict_new = json_dict
    for key, value in json_dict_new.items():
        #print("key List = ", key)
        #print("value List = ", value)
        #print(type(value))
        if type(value) == type(json_dict):
            #print(value, type(value))
            for value, value2 in value.items():
                #print(value)
                #aod
                if value =='aod-file' and extrargs.aod:
                   json_dict[key][value] = extrargs.aod                
                # analysis-event-selection
                if value == 'cfgMixingVars' and extrargs.cfgMixingVars:
                    extrargs.cfgEventCuts = ",".join(extrargs.cfgMixingVars)
                    json_dict[key][value] = extrargs.cfgMixingVars
                if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                    extrargs.cfgEventCuts = ",".join(extrargs.cfgEventCuts)
                    json_dict[key][value] = extrargs.cfgEventCuts
                if value =='cfgQA' and extrargs.cfgQA:
                   json_dict[key][value] = extrargs.cfgQA
                if value == 'processSkimmed' and extrargs.processSkimmed:
                    json_dict[key][value] = extrargs.processSkimmed
                if value == 'processDummy' and extrargs.processDummy:
                    json_dict[key][value] = extrargs.processDummy
                # analysis-muon-selection
                if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                   extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                   json_dict[key][value] = extrargs.cfgMuonCuts
                if value == 'cfgMuonMCSignals' and extrargs.cfgMuonMCSignals:
                    extrargs.cfgMuonMCSignals = ",".join(extrargs.cfgMuonMCSignals)
                    json_dict[key][value] = extrargs.cfgMuonMCSignals
                if value == 'cfgQA' and extrargs.cfgQA:
                    json_dict[key][value] = extrargs.cfgQA
                if value =='processSkimmed' and extrargs.processSkimmed:
                   json_dict[key][value] = extrargs.processSkimmed
                if value == 'processDummy' and extrargs.processDummy:
                    json_dict[key][value] = extrargs.processDummy
                # analysis-track-selection
                if value =='cfgTrackCuts' and extrargs.cfgTrackCuts:
                   extrargs.cfgTrackCuts = ",".join(extrargs.cfgTrackCuts)
                   json_dict[key][value] = extrargs.cfgTrackCuts
                if value == 'cfgTrackMCSignals' and extrargs.cfgTrackMCSignals:
                    extrargs.cfgTrackMCSignals = ",".join(extrargs.cfgTrackMCSignals)
                    json_dict[key][value] = extrargs.cfgTrackMCSignals
                if value == 'cfgQA' and extrargs.cfgQA:
                    json_dict[key][value] = extrargs.cfgQA
                if value =='processSkimmed' and extrargs.processSkimmed:
                   json_dict[key][value] = extrargs.processSkimmed
                if value == 'processDummy' and extrargs.processDummy:
                    json_dict[key][value] = extrargs.processDummy
                # analysis-event-mixing ONLY FOR DATA
                if value == 'cfgTrackCuts' and extrargs.cfgTrackCuts:                   
                    extrargs.cfgTrackCuts = ",".join(extrargs.cfgTrackCuts)
                    json_dict[key][value] = extrargs.cfgTrackCuts
                if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                   extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                   json_dict[key][value] = extrargs.cfgMuonCuts
                if value == 'processBarrelSkimmed' and extrargs.processBarrelSkimmed:
                    json_dict[key][value] = extrargs.processBarrelSkimmed
                if value == 'processMuonSkimmed' and extrargs.processMuonSkimmed:
                    json_dict[key][value] = extrargs.processMuonSkimmed
                if value == 'processBarrelMuonSkimmed' and extrargs.processBarrelMuonSkimmed:
                    json_dict[key][value] = extrargs.processBarrelMuonSkimmed
                if value == 'processDummy' and extrargs.processDummy:
                    json_dict[key][value] = extrargs.processDummy
                # analysis-same-event-pairing TODO: CCDB parts Can be added
                if value == 'cfgTrackCuts' and extrargs.cfgTrackCuts:                   
                    extrargs.cfgTrackCuts = ",".join(extrargs.cfgTrackCuts)
                if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                   extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                if value == 'cfgBarrelMCRecSignals' and extrargs.cfgBarrelMCRecSignals:
                    extrargs.cfgBarrelMCRecSignals = ",".join(extrargs.cfgBarrelMCRecSignals)
                    json_dict[key][value] = extrargs.cfgBarrelMCRecSignals
                if value == 'cfgBarrelMCGenSignals' and extrargs.cfgBarrelMCGenSignals:
                    extrargs.cfgBarrelMCGenSignals = ",".join(extrargs.cfgBarrelMCGenSignals)
                    json_dict[key][value] = extrargs.cfgBarrelMCGenSignals
                if value =='processJpsiToEESkimmed' and extrargs.processJpsiToEESkimmed:
                   json_dict[key][value] = extrargs.processJpsiToEESkimmed
                if value == 'processJpsiToMuMuSkimmed' and extrargs.processJpsiToMuMuSkimmed:
                    json_dict[key][value] = extrargs.processJpsiToMuMuSkimmed
                if value == 'processJpsiToMuMuVertexingSkimmed' and extrargs.processJpsiToMuMuVertexingSkimmed:
                    json_dict[key][value] = extrargs.processJpsiToMuMuVertexingSkimmed
                if value =='processElectronMuonSkimmed' and extrargs.processElectronMuonSkimmed:
                   json_dict[key][value] = extrargs.processElectronMuonSkimmed
                if value == 'processAllSkimmed' and extrargs.processAllSkimmed:
                    json_dict[key][value] = extrargs.processAllSkimmed
                # analysis-dilepton-hadron ONLY FOR DATA
                if value == 'cfgLeptonCuts' and extrargs.cfgLeptonCuts:
                    extrargs.cfgLeptonCuts = ",".join(extrargs.cfgLeptonCuts)
                    json_dict[key][value] = extrargs.cfgLeptonCuts
                if value == 'processSkimmed' and extrargs.processSkimmed:
                    json_dict[key][value] = extrargs.Skimmed
                if value == 'processDummy' and extrargs.processDummy:
                    json_dict[key][value] = extrargs.processDummy
                # analysis-dilepton-track ONLY FOR MC
                if value == 'cfgBarrelMCRecSignals' and extrargs.cfgBarrelMCRecSignals:
                    extrargs.cfgBarrelMCRecSignals = ",".join(extrargs.cfgBarrelMCRecSignals)
                    json_dict[key][value] = extrargs.cfgBarrelMCRecSignals
                if value == 'cfgBarrelMCGenSignals' and extrargs.cfgBarrelMCGenSignals:
                    extrargs.cfgBarrelMCGenSignals = ",".join(extrargs.cfgBarrelMCGenSignals)
                    json_dict[key][value] = extrargs.cfgBarrelMCGenSignals
                if value == 'processSkimmed' and extrargs.processSkimmed:
                    json_dict[key][value] = extrargs.Skimmed
                if value == 'processDummy' and extrargs.processDummy:
                    json_dict[key][value] = extrargs.processDummy

                
    if(extrargs.outputjson == None):
        #print("1")          
        config_output_json = open(my_json,'w')
        config_output_json.write(json.dumps(json_dict, indent= 2))
        print("Forget to Give output JSON name. Default Config")
    elif(extrargs.outputjson[-5:] == ".json"):
        #print("2")
        my_json = extrargs.outputjson
        config_output_json = open(my_json,'w')
        config_output_json.write(json.dumps(json_dict, indent= 2))
    elif(extrargs.outputjson[-5:] != ".json"):
        if '.' in extrargs.outputjson:
            print("Wrong formatted input for JSON output!!! Script will Stopped.")
            return
        temp = extrargs.outputjson
        temp = temp+'.json'
        my_json = temp
        config_output_json = open(my_json,'w')
        config_output_json.write(json.dumps(json_dict, indent= 2))
    else:
        print("Logical json input error. Report it!!!")
        
        
get_key(json_dict_new)       
       
configured_commands = vars(extrargs) # for get extrargs
# Listing Added Commands
print("Args provided configurations List")
print("========================================")
for key,value in configured_commands.items():
    if(value != None):
        print("--"+key,":", value)


