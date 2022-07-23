#!/usr/bin/env python
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

import json
import sys
import logging
from ast import parse
import os
import argparse
import argcomplete  
from argcomplete.completers import ChoicesCompleter

# DEMO Python Interface for runTableMaker.py

# List to String --> Function to convert 

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

json_cut_database = json.load(open('Database/AnalysisCutDatabase.json'))
json_mcsignal_database = json.load(open('Database/MCSignalDatabase.json'))
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
    
###################################
# Interface Predefined Selections #
###################################
    
# process options in table maker
tablemaker_all_process = ["Full","FullTiny","FullWithCov","FullWithCent",
        "BarrelOnlyWithV0Bits","BarrelOnlyEventFilter","BarrelOnlyWithCent","BarrelOnlyWithCov","BarrelOnly",
        "MuonOnlyWithCent","MuonOnlyWithCov","MuonOnly","MuonOnlyWithFilter",
        "OnlyBCs"]
tablemaker_full = ["Full","FullTiny","FullWithCov","FullWithCent"]
tablemaker_barrel = ["BarrelOnlyWithV0Bits","BarrelOnlyEventFilter","BarrelOnlyWithCent","BarrelOnlyWithCov","BarrelOnly"]
tablemaker_muon = ["MuonOnlyWithCent","MuonOnlyWithCov","MuonOnly","MuonOnlyWithFilter"]
tablemaker_bcs = ["OnlyBCs"]

# with full name
tablemaker_all_process_pre = ["processFull","processFullTiny","processFullWithCov","processFullWithCent",
        "processBarrelOnlyWithV0Bits","processBarrelOnlyEventFilter","processBarrelOnlyWithCent","processBarrelOnlyWithCov","processBarrelOnly",
        "processMuonOnlyWithCent","processMuonOnlyWithCov","processMuonOnly","processMuonOnlyWithFilter",
        "processOnlyBCs"]
tablemaker_full_pre = ["processFull","processFullTiny","processFullWithCov","processFullWithCent"]
tablemaker_barrel_pre = ["processBarrelOnlyWithV0Bits","processBarrelOnlyEventFilter","processBarrelOnlyWithCent","processBarrelOnlyWithCov","processBarrelOnly"]
tablemaker_muon_pre = ["processMuonOnlyWithCent","processMuonOnlyWithCov","processMuonOnly","processMuonOnlyWithFilter"]
tablemaker_bcs_pre = ["processOnlyBCs"]



#process run options
run_options = ["2","3"]

#mc or data
mc_data = ["MC","Data"]

#isrun2mc, mc ve is run3 processe göre belirlenecek.

#centrality table options
centrality_table_options = ["V0M", "Run2SPDtks","Run2SPDcls","Run2CL0","Run2CL1"]

#with full name

centrality_table_options_pre = ["estV0M", "estRun2SPDtks","estRun2SPDcls","estRun2CL0","estRun2CL1"]


#pid options
pid_options = ["el","mu","pi","ka","pr","de","tr","he","al"]

pid_options_pre = ["pid-el","pid-mu","pid-pi","pid-ka","pid-pr","pid-de","pid-tr","pid-he","pid-al"]

#tof pid and pid-full process opts
tpo = ["EvTime","NoEvTime"]

#filter pp options
# = ["BarrelSels","MuonSels"]
filter_PP_process = ["FilterPP","FilterPPTiny"]


# dq Task Selection Options for event selection
event_selection = ["true","false"]

# dummy selection
process_dummies =["filter","event","muons","barrel"]

#track prop select.
track_prop = ["Standart","Covariance"]
    

########################
# Interface Parameters #
########################


parser = argparse.ArgumentParser(description='Arguments to pass')

# aod
parser.add_argument('--aod', help="Add your AOD File with path", action="store", type=str)

# json output
parser.add_argument('--outputjson', help="Your Output JSON Config Fİle", action="store", type=str)

# only select
parser.add_argument('--onlySelect', help="Activate only selected JSON configs", action="store",choices=["true","false"], default="false", type=str.lower)

# table-maker cfg
parser.add_argument('--cfgEventCuts', help="Configure Cuts with commas", choices=cut_database, nargs='*', action="store", type=str)
parser.add_argument('--cfgBarrelTrackCuts', help="Configure Cuts with commas", choices=cut_database,nargs='*', action="store", type=str)
parser.add_argument('--cfgMuonCuts', help="Configure Cuts with commas", action="store", choices=cut_database, nargs='*', type=str)
parser.add_argument('--cfgBarrelLowPt', help="Input type number", action="store", type=str)
parser.add_argument('--cfgMuonLowPt', help="Input type number", action="store", type=str)
parser.add_argument('--cfgNoQA', help="QA Selection true or false", action="store", choices=["true","false"], type=str)
parser.add_argument('--cfgDetailedQA', help="QA Detail Selection true or false", action="store", choices=["true","false"], type=str)
#parser.add_argument('--cfgIsRun2', help="Run selection true or false", action="store", choices=["true","false"], type=str) # no need
parser.add_argument('--cfgMinTpcSignal', help="Input type number", action="store", type=str)
parser.add_argument('--cfgMaxTpcSignal', help="Input type number", action="store", type=str)
parser.add_argument('--cfgMCsignals', help="Configure MCSignals with commas", action="store",choices=mcsignal_database, nargs='*', type=str)

# table-maker process
parser.add_argument('--process', help="Process Selection options true or false (string)", action="store", choices=tablemaker_all_process, nargs='*', type=str)

# Run Selection : event-selection-task ,bc-selection-task, multiplicity-table, track-extension no refactor
parser.add_argument('--run', help="Run Selection", action="store", choices=['2','3'], type=str, required=True)
#parser.add_argument('--processRun2', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) # no need
#parser.add_argument('--processRun3', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) # no need

# event-selection-task
parser.add_argument('--syst', help="Collision System Selection Input pp or PbPb", action="store", choices=['pp','PbPb'], type=str)
parser.add_argument('--muonSelection', help="Muon Selection Input Type Number", action="store", type=str)
parser.add_argument('--customDeltaBC', help="CustomDeltaBC Input Type Number", action="store", type=str)
parser.add_argument('--isMC', help="Is it Monte Carlo options true or false", action="store", choices=["true","false"],default="false", type=str, required=True)

# track-propagation
parser.add_argument('--processStandard', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processCovariance', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# tof-pid-full, tof-pid for run3 ???
parser.add_argument('--isProcessEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
#parser.add_argument('--processEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #no need
#parser.add_argument('--processNoEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)#no need

#tof-pid-beta
parser.add_argument('--tof-expreso', help="Tof expreso Input Type Number", action="store", type=str)

# need refactoring part
#parser.add_argument('--processSelection', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #d-q barrel and d-q muon selection no need automatic with process tablemaker
#parser.add_argument('--processSelectionTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #only d-q barrel no need automatic with process tablemaker
# TODO: Bunu nasıl entegre edicem?
parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #event selection, barel track task, filter task

#d-q-event-selection-task
parser.add_argument('--isBarrelSelectionTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #d-q barrel and d-q muon selection
#parser.add_argument('--processEventSelection', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #no need TODO entegrasyonu yapılmamış olabilir

# d-q-filter-p-p-task
parser.add_argument('--cfgPairCuts', help="Configure Cuts with commas", action="store", choices=cut_database, nargs='*', type=str) # run3
parser.add_argument('--cfgBarrelSels', help="Configure Barrel Selection example jpsiO2MCdebugCuts2::1 ", action="store", type=str) # run2 
parser.add_argument('--cfgMuonSels', help="Configure Muon Selection example muonHighPt::1", action="store", type=str) # run 2
parser.add_argument('--isFilterPPTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
#parser.add_argument('--processFilterPP', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3 no need
#parser.add_argument('--processFilterPPTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3 no need

# centrality-table
parser.add_argument('--est', help="Configure to centrality Table", action="store", choices=centrality_table_options,nargs="*", type=str)

# timestamp-task
#parser.add_argument('--isRun2MC', help="Selection the Process is MC or Not", action="store", choices=['true','false'], type=str)

# track-selection
#parser.add_argument('--isRun3', help="Add track propagation to the innermost layer (TPC or ITS)", action="store", choices=['true','false'], type=str)

#all d-q tasks and selections
parser.add_argument('--cfgWithQA', help="Selection Configure QA options true or false", action="store", choices=['true','false'], type=str)

# v0-selector
parser.add_argument('--d_bz', help="Input Type Number", action="store", type=str)
parser.add_argument('--v0cospa', help="Input Type Number", action="store", type=str)
parser.add_argument('--dcav0dau', help="Input Type Number", action="store", type=str)
parser.add_argument('--v0Rmin', help="Input Type Number", action="store", type=str)
parser.add_argument('--v0Rmax', help="Input Type Number", action="store", type=str)
parser.add_argument('--dcamin', help="Input Type Number", action="store", type=str)
parser.add_argument('--dcamax', help="Input Type Number", action="store", type=str)
parser.add_argument('--mincrossedrows', help="Input Type Number", action="store", type=str)
parser.add_argument('--maxchi2tpc', help="Input Type Number", action="store", type=str)

# pid
parser.add_argument('--pid', help="pid selection input", action="store", choices=pid_options, nargs='*', type=str)


argcomplete.autocomplete(parser)
extrargs = parser.parse_args()

######################
# PREFIX ADDING PART #
###################### 

# add prefix for extrargs.process for TableMaker and Filter PP
if extrargs.process != None:
    prefix_process = "process"
    extrargs.process = [prefix_process + sub for sub in extrargs.process]

# add prefix for extrargs.pid for pid selection
if extrargs.pid != None:
    prefix_pid = "pid-"
    extrargs.pid = [prefix_pid + sub for sub in extrargs.pid]
    
# add prefix for extrargs.est for centrality table
if extrargs.est != None:
    prefix_est = "est"
    extrargs.est = [prefix_est + sub for sub in extrargs.est]
    



#Open JSON File
json_dict = json.load(open('Configs/configTableMakerDataRun3.json'))

json_dict_new = json_dict


def get_key(json_dict_new):
    my_json = 'ConfiguredTableMakerData.json'
    json_dict = json.load(open('Configs/configTableMakerDataRun3.json'))
    #json_dict = json.load(open('data.json'))
    json_dict_new = json_dict
    for key, value in json_dict_new.items():
        #print("key List = ", key)
        #print("value List = ", value)
        #print(type(value))
        if type(value) == type(json_dict):
            print(value, type(value))
            for value, value2 in value.items():
                #print(value)
                
                # aod
                if value =='aod-file' and extrargs.aod:
                   json_dict[key][value] = extrargs.aod
                   
                # Process Table Maker
                if (value in tablemaker_all_process_pre) and extrargs.process:
                    if value in extrargs.process:
                        value2 = "true"
                        json_dict[key][value] = value2
                        
                        # check extraargs is contain Full Barrel Muon or Bcs
                        full_search = [s for s in extrargs.process if "Full" in s]
                        barrel_search = [s for s in extrargs.process if "Barrel" in s]
                        muon_search = [s for s in extrargs.process if "Muon" in s]
                        bcs_search = [s for s in extrargs.process if "Bcs" in s]    
                                          
                        # Automatic Activate and Disable regarding to process func. in tablemaker
                        # todo: dq-barrel ve muon taskı içeride var mı kontrol için if statement yaz
                        if len(full_search) > 0 and extrargs.isMC == False:
                            if json_dict["d-q-barrel-track-selection-task"]["processSelection"] != None and json_dict["d-q-muons-selection"]["processSelection"] != None:
                                json_dict["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                                json_dict["d-q-muons-selection"]["processSelection"] = "true"
                        if len(barrel_search) > 0 and len(muon_search) < 0 and len(full_search) <0 and extrargs.isMC == False:
                            if json_dict["d-q-barrel-track-selection-task"]["processSelection"] != None:
                                json_dict["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                            if json_dict["d-q-muons-selection"]["processSelection"] != None:
                                json_dict["d-q-muons-selection"]["processSelection"] = "false"     
                        if len(muon_search) > 0 and len(barrel_search) < 0 and len(full_search) <0 and extrargs.isMC == False:
                            if json_dict["d-q-barrel-track-selection-task"]["processSelection"] != None:
                                json_dict["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                            if json_dict["d-q-muons-selection"]["processSelection"] != None:
                                json_dict["d-q-muons-selection"]["processSelection"] = "true"
                                                        
                    elif extrargs.onlySelect == "true":
                        value2 = "false"
                        json_dict[key][value] = value2
                        #print(value)
                        #print("Key :",key,"Value:",value,"Value 2 :",value2)
                        
                # Filter PP Task TODO Entegre et
                # TODO: Bu catların listToStringini fixle
                if value =='cfgPairCuts' and extrargs.cfgPairCuts:
                    extrargs.cfgPairCuts = ",".join(extrargs.cfgPairCuts)
                    json_dict[key][value] = extrargs.cfgPairCuts
                if value == 'cfgBarrelSels' and extrargs.cfgBarrelSels:
                    json_dict[key][value] = extrargs.cfgBarrelSels
                if value == 'cfgMuonSels' and extrargs.cfgMuonSels:
                    json_dict[key][value] = extrargs.cfgMuonSels
                if value =='processFilterPPTiny' and extrargs.isFilterPPTiny == True:
                    json_dict[key][value] = True
                    json_dict[key]["processFilterPP"] = False
                elif value =='processFilterPPTiny' and extrargs.isFilterPPTiny == False:
                    json_dict[key][value] = False
                    json_dict[key]["processFilterPP"] = True         
                        
                # Run 2/3 and MC/DATA Selection  Automations      
                
                if extrargs.run == "2":
                    if value == 'cfgIsRun2':
                        json_dict[key][value] = "true"
                    if value == 'isRun3':
                        json_dict[key][value] = "false"
                    if value == 'processRun3':
                        json_dict[key][value] = "false"
                if extrargs.run == "3":
                    if value == 'cfgIsrun2':
                        json_dict[key][value] = "false"
                    if value == 'isRun3':
                        json_dict[key][value] = "true"
                    if value == 'processRun3':
                        json_dict[key][value] = "true"
                
                if extrargs.run == '2' and extrargs.run == 'MC':
                    if value == 'isRun2MC':
                        json_dict[key][value] = "true"
                if extrargs.run != '2' and extrargs.run != 'MC':
                    if value == 'isRun2MC':
                        json_dict[key][value] = "false"
                        
                        
                if extrargs.run == "MC":
                    if value == 'isMC':
                        json_dict[key][value] = "true"
                if extrargs.run == "Data":
                    if value == 'isMC':
                        json_dict[key][value] = "false"
                
                
                    
                # Pid Selections
                if  (value in pid_options_pre) and extrargs.pid:
                    if value in extrargs.pid:
                        value2 = "1"
                        json_dict[key][value] = value2
                    elif extrargs.onlySelect == "true":
                        value2 = "-1"
                        json_dict[key][value] = value2
                        
                # v0-selector
                if value =='d_bz' and extrargs.d_bz:
                   json_dict[key][value] = extrargs.d_bz
                if value == 'v0cospa' and extrargs.v0cospa:
                    json_dict[key][value] = extrargs.v0cospa
                if value == 'dcav0dau' and extrargs.dcav0dau:
                    json_dict[key][value] = extrargs.dcav0dau
                if value =='v0Rmin' and extrargs.v0Rmin:
                   json_dict[key][value] = extrargs.v0Rmin
                if value == 'v0Rmax' and extrargs.v0Rmax:
                    json_dict[key][value] = extrargs.v0Rmax
                if value == 'dcamin' and extrargs.dcamin:
                    json_dict[key][value] = extrargs.dcamin
                if value == 'dcamax' and extrargs.dcamax:
                    json_dict[key][value] = extrargs.dcamax
                if value =='mincrossedrows' and extrargs.mincrossedrows:
                   json_dict[key][value] = extrargs.mincrossedrows
                if value == 'maxchi2tpc' and extrargs.maxchi2tpc:
                    json_dict[key][value] = extrargs.maxchi2tpc
                    
                # centrality table
                if (value in centrality_table_options_pre) and extrargs.est:
                    if value in extrargs.est:
                        value2 = "1"
                        json_dict[key][value] = value2
                    elif extrargs.onlySelect == "true":
                        value2 = "-1"
                        json_dict[key][value] = value2
                        
                # cfg in TableMaker
                if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                    if type(extrargs.cfgEventCuts) == type(clist):
                        extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts)
                    json_dict[key][value] = extrargs.cfgEventCuts
                if value == 'cfgBarrelTrackCuts' and extrargs.cfgBarrelTrackCuts:
                    if type(extrargs.cfgBarrelTrackCuts) == type(clist):
                        extrargs.cfgBarrelTrackCuts = listToString(extrargs.cfgBarrelTrackCuts)
                    json_dict[key][value] = extrargs.cfgBarrelTrackCuts
                if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                    if type(extrargs.cfgBarrelTrackCuts) == type(clist):
                        extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts)                
                    json_dict[key][value] = extrargs.cfgMuonCuts
                if value == 'cfgBarrelLowPt' and extrargs.cfgBarrelLowPt:
                    json_dict[key][value] = extrargs.cfgBarrelLowPt
                if value == 'cfgMuonLowPt' and extrargs.cfgMuonLowPt:
                    json_dict[key][value] = extrargs.cfgMuonLowPt
                if value =='cfgNoQA' and extrargs.cfgNoQA:
                   json_dict[key][value] = extrargs.cfgNoQA
                if value == 'cfgDetailedQA' and extrargs.cfgDetailedQA:
                    json_dict[key][value] = extrargs.cfgDetailedQA
                if value == 'cfgIsRun2' and extrargs.run == "3":
                    json_dict[key][value] = "true"
                if value =='cfgMinTpcSignal' and extrargs.cfgMinTpcSignal:
                   json_dict[key][value] = extrargs.cfgMinTpcSignal
                if value == 'cfgMaxTpcSignal' and extrargs.cfgMaxTpcSignal:
                    json_dict[key][value] = extrargs.cfgMaxTpcSignal
                if value == 'cfgMCsignals' and extrargs.cfgMCsignals:
                    if type(extrargs.cfgMCsignals) == type(clist):
                        extrargs.cfgMCsignals = listToString(extrargs.cfgMCsignals)                     
                    extrargs.cfgMCsignals = ",".join(extrargs.cfgMCsignals)
                    json_dict[key][value] = extrargs.cfgMCsignals

                # event-selection
                if value == 'syst' and extrargs.syst:
                    json_dict[key][value] = extrargs.syst
                if value =='muonSelection' and extrargs.muonSelection:
                   json_dict[key][value] = extrargs.muonSelection
                if value == 'customDeltaBC' and extrargs.customDeltaBC:
                    json_dict[key][value] = extrargs.customDeltaBC
                    
                # tof-pid-beta
                if value == 'tof-expreso' and extrargs.tof_expreso:
                    json_dict[key][value] = extrargs.tof_expreso
                    
                # tof-pid-full, tof-pid for run3
                if value == 'processEvTime' and extrargs.isProcessEvTime == True:
                    json_dict[key][value] = True
                    json_dict[key]["processNoEvTime"] = False
                elif value == 'processEvTime' and extrargs.isProcessEvTime == False:
                    json_dict[key][value] = False
                    json_dict[key]["processNoEvTime"] = True
                     
                # all d-q tasks and selections TODO Eğer TableMakerdakiyle aynı şeyi isterlerse refactor
                if value == 'cfgWithQA' and extrargs.cfgWithQA:
                    json_dict[key][value] = extrargs.cfgWithQA                  
                # track-propagation
                if value =='processStandard' and extrargs.processStandard:
                   json_dict[key][value] = extrargs.processStandard
                if value == 'processCovariance' and extrargs.processCovariance:
                    json_dict[key][value] = extrargs.processCovariance
                # dq-barrel-track-selection-task
                if value =='processSelectionTiny' and extrargs.isBarrelSelectionTiny == True:
                    json_dict[key][value] = extrargs.isBarrelSelectionTiny
                    json_dict[key]["processSelection"] = False
                
                        
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
        
                          
get_key(json_dict)

configured_commands = vars(extrargs) # for get extrargs
# Listing Added Commands
print("Args provided configurations List")
print("========================================")
for key,value in configured_commands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
        print("--"+key,":", value)


