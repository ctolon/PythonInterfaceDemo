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

# cfg list
## all d-q tasks and selections
parser.add_argument('--cfgWithQA', help="Selection Configure QA options true or false", action="store", choices=['true','false'], type=str)
## d-q-event-selection
parser.add_argument('--cfgEventCuts', help="Configure Cuts with commas", choices=cut_database, nargs='*', action="store", type=str)
parser.add_argument('--processEventSelection', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
## d-q-event-selection and d-q-muons-selection
parser.add_argument('--processSelection', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
## d-q-barrel-track-selection
parser.add_argument('--cfgBarrelTrackCuts', help="Configure Cuts with commas", choices=cut_database, nargs='*', action="store", type=str)
## d-q-muons-selection
parser.add_argument('--cfgMuonsCuts', help="Configure Cuts with commas", choices=cut_database, nargs='*', action="store", type=str)
## d-q-filter-p-p-task
parser.add_argument('--cfgPairCuts', help="Configure Cuts with commas", action="store", choices=cut_database, nargs='*', type=str) # run3
parser.add_argument('--cfgBarrelSels', help="Configure Barrel Selection example jpsiO2MCdebugCuts2::1 ", action="store", type=str) # run2 
parser.add_argument('--cfgMuonSels', help="Configure Muon Selection example muonHighPt::1", action="store", type=str) # run 2
parser.add_argument('--processFilterPP', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3
parser.add_argument('--processFilterPPTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3

# timestamp-task
parser.add_argument('--isRun2MC', help="Selection the Process is MC or Not", action="store", choices=['true','false'], type=str)

# pid
parser.add_argument('--pid-el', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-mu', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-pi', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-ka', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-pr', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-de', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-tr', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-he', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-al', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)

# process list not in d-q tasks
parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #event selection, barel track task, filter task
parser.add_argument('--processRun2', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processRun3', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# event-selection-task
parser.add_argument('--syst', help="Collision System Selection Input pp or PbPb", action="store", choices=['pp','PbPb'], type=str)
parser.add_argument('--muonSelection', help="Muon Selection Input Type Number", action="store", type=str)
parser.add_argument('--customDeltaBC', help="CustomDeltaBC Input Type Number", action="store", type=str)
parser.add_argument('--isMC', help="Is it Monte Carlo options true or false", action="store", choices=["true","false"], type=str)

#tof-pid-beta
parser.add_argument('--tof-expreso', help="Tof expreso Input Type Number", action="store", type=str)

#track-selection
parser.add_argument('--isRun3', help="Selection the Process is MC or Not", action="store", choices=['true','false'], type=str)



# tof-pid-full, tof-pid for run3
# TODO: BU GÜNCEL O2DE EKSİK OLABİLİR TABLEMAKERDAKİ FİLTER PP'DE VAR TOPLANTIDA SOR CHECK ET.
parser.add_argument('--processEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processNoEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

extrargs = parser.parse_args()

#Open JSON File
json_dict = json.load(open('configFilterPPRun3.json'))

json_dict_new = json_dict


def get_key(json_dict_new):
    my_json = 'ConfiguredFilterPPData.json'
    json_dict = json.load(open('configFilterPPRun3.json'))
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
                # aod
                if value =='aod-file' and extrargs.aod:
                   json_dict[key][value] = extrargs.aod   
                # d-q tasks
                if value == 'cfgWithQA' and extrargs.cfgWithQA:
                   json_dict[key][value] = extrargs.cfgWithQA 
                if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                   extrargs.cfgEventCuts = ",".join(extrargs.cfgEventCuts)
                   json_dict[key][value] = extrargs.cfgEventCuts
                if value == 'processEventSelection' and extrargs.processEventSelection:
                   json_dict[key][value] = extrargs.processEventSelection
                if value == 'processSelection' and extrargs.processSelection:
                   json_dict[key][value] = extrargs.processSelection
                if value == 'cfgBarrelTrackCuts' and extrargs.cfgBarrelTrackCuts:
                   extrargs.cfgBarrelTrackCuts = ",".join(extrargs.cfgBarrelTrackCuts)
                   json_dict[key][value] = extrargs.cfgBarrelTrackCuts
                if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                   extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                   json_dict[key][value] = extrargs.cfgMuonCuts
                if value =='cfgPairCuts' and extrargs.cfgPairCuts:
                    extrargs.cfgPairCuts = ",".join(extrargs.cfgPairCuts)
                    json_dict[key][value] = extrargs.cfgPairCuts      
                if value == 'cfgBarrelSels' and extrargs.cfgBarrelSels:
                    json_dict[key][value] = extrargs.cfgBarrelSels
                if value == 'cfgMuonSels' and extrargs.cfgMuonSels:
                    json_dict[key][value] = extrargs.cfgMuonSels
                if value =='processFilterPP' and extrargs.processFilterPP:
                   json_dict[key][value] = extrargs.processFilterPP
                if value == 'processFilterPPTiny' and extrargs.processFilterPPTiny:
                    json_dict[key][value] = extrargs.processFilterPPTiny
                # Timestamp
                if value =='isRun2MC' and extrargs.isRun2MC:
                   json_dict[key][value] = extrargs.isRun2MC
                # pid
                if value == 'pid-el' and extrargs.pid_el:
                    json_dict[key][value] = extrargs.pid_el
                if value == 'pid-mu' and extrargs.pid_mu:
                    json_dict[key][value] = extrargs.pid_mu
                if value == 'pid-pi' and extrargs.pid_pi:
                    json_dict[key][value] = extrargs.pid_pi
                if value == 'pid-ka' and extrargs.pid_ka:
                    json_dict[key][value] = extrargs.pid_ka
                if value == 'pid-pr' and extrargs.pid_pr:
                    json_dict[key][value] = extrargs.pid_pr
                if value == 'pid-de' and extrargs.pid_de:
                    json_dict[key][value] = extrargs.pid_de
                if value == 'pid-tr' and extrargs.pid_tr:
                    json_dict[key][value] = extrargs.pid_tr
                if value == 'pid-he' and extrargs.pid_he:
                    json_dict[key][value] = extrargs.pid_he
                if value == 'pid-al' and extrargs.pid_al:
                    json_dict[key][value] = extrargs.pid_al    
                # process list not in d-q tasks
                if value == 'processDummy' and extrargs.processDummy:
                    json_dict[key][value] = extrargs.processDummy
                if value =='processRun2' and extrargs.processRun2:
                   json_dict[key][value] = extrargs.processRun2
                if value == 'processRun3' and extrargs.processRun3:
                    json_dict[key][value] = extrargs.processRun3  
                # event-selection-task
                if value == 'syst' and extrargs.syst:
                    json_dict[key][value] = extrargs.syst
                if value =='muonSelection' and extrargs.muonSelection:
                   json_dict[key][value] = extrargs.muonSelection
                if value == 'customDeltaBC' and extrargs.customDeltaBC:
                    json_dict[key][value] = extrargs.customDeltaBC
                if value == 'isMC' and extrargs.isMC:
                    json_dict[key][value] = extrargs.isMC
                # tof-pid-beta
                if value == 'tof-expreso' and extrargs.tof_expreso:
                    json_dict[key][value] = extrargs.tof_expreso
                # track-selection
                if value == 'isRun3' and extrargs.isRun3:
                    json_dict[key][value] = extrargs.isRun3
                # tof-pid-full, tof-pid for run3
                if value == 'processEvTime' and extrargs.processEvTime:
                    json_dict[key][value] = extrargs.processEvTime
                if value =='processNoEvTime' and extrargs.processNoEvTime:
                   json_dict[key][value] = extrargs.processNoEvTime

                
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


