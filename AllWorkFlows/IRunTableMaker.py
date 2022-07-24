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

"""
argcomplete - Bash tab completion for argparse
Documentation https://kislyuk.github.io/argcomplete/
Instalation Steps
pip install argcomplete
sudo activate-global-python-argcomplete
Only Works On Local not in O2
"""
#import argcomplete  
#from argcomplete.completers import ChoicesCompleter

#################################
# JSON Database Read and Upload #
#################################
"""
Predefined Analysis Cuts, MCSignals and Histograms From O2-DQ Framework.
TODO: Add Info
info
Parameters
------------------------------------------------
analysisCutDatabaseJSON: JSON
    analysisCutDatabaseJSON
    
analysisCutDatabase : list
    analysisCutDatabase List

MCSignalDatabaseJSON: JSON
    MCSignalDatabaseJSON
    
MCSignalDatabase: list
    MCSignalDatabase List
"""
analysisCutDatabaseJSON = json.load(open('Database/AnalysisCutDatabase.json'))
MCSignalDatabaseJSON = json.load(open('Database/MCSignalDatabase.json'))
analysisCutDatabase = []
MCSignalDatabase =[]

# control list for type control
clist=[]

# Cut Database
for key, value in analysisCutDatabaseJSON.items():
    analysisCutDatabase.append(value)

# MCSignal Database
for key, value in MCSignalDatabaseJSON.items():
    MCSignalDatabase.append(value)
    

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
    
###################################
# Interface Predefined Selections #
###################################

# todo: set naming conventions for all predefined selections    

tablemakerProcessAllSelections = ["Full","FullTiny","FullWithCov","FullWithCent",
        "BarrelOnlyWithV0Bits","BarrelOnlyEventFilter","BarrelOnlyWithCent","BarrelOnlyWithCov","BarrelOnly",
        "MuonOnlyWithCent","MuonOnlyWithCov","MuonOnly","MuonOnlyWithFilter",
        "OnlyBCs"]
tablemakerProcessFullSelections = ["Full","FullTiny","FullWithCov","FullWithCent"]
tablemakerProcessBarrelSelections = ["BarrelOnlyWithV0Bits","BarrelOnlyEventFilter","BarrelOnlyWithCent","BarrelOnlyWithCov","BarrelOnly"]
tablemakerProcessMuonSelections = ["MuonOnlyWithCent","MuonOnlyWithCov","MuonOnly","MuonOnlyWithFilter"]
tablemakerProcessBCsSelections = ["OnlyBCs"]

tablemakerProcessAllParameters = ["processFull","processFullTiny","processFullWithCov","processFullWithCent",
        "processBarrelOnlyWithV0Bits","processBarrelOnlyEventFilter","processBarrelOnlyWithCent","processBarrelOnlyWithCov","processBarrelOnly",
        "processMuonOnlyWithCent","processMuonOnlyWithCov","processMuonOnly","processMuonOnlyWithFilter",
        "processOnlyBCs"]
tablemakerProcessFullParameters = ["processFull","processFullTiny","processFullWithCov","processFullWithCent"]
tablemakerProcessBarrelParameters = ["processBarrelOnlyWithV0Bits","processBarrelOnlyEventFilter","processBarrelOnlyWithCent","processBarrelOnlyWithCov","processBarrelOnly"]
tablemakerProcessMuonParameters = ["processMuonOnlyWithCent","processMuonOnlyWithCov","processMuonOnly","processMuonOnlyWithFilter"]
tablemakerProcessBCsParameters = ["processOnlyBCs"]

centralityTableSelections = ["V0M", "Run2SPDtks","Run2SPDcls","Run2CL0","Run2CL1"]
centralityTableParameters = ["estV0M", "estRun2SPDtks","estRun2SPDcls","estRun2CL0","estRun2CL1"]

PIDSelections = ["el","mu","pi","ka","pr","de","tr","he","al"]
PIDParameters = ["pid-el","pid-mu","pid-pi","pid-ka","pid-pr","pid-de","pid-tr","pid-he","pid-al"]

processFilterPPSelections = ["FilterPP","FilterPPTiny"]
processDummySelections =["filter","event","barrel"]

track_prop = ["Standart","Covariance"]

###################
# Main Parameters #
###################

parser = argparse.ArgumentParser(description='Arguments to pass')
parser.add_argument('cfgFileName', metavar='text', default='config.json', help='config file name')
parser.add_argument('-runData', help="Run over data", action="store_true")
parser.add_argument('-runMC', help="Run over MC", action="store_true")
#parser.add_argument('analysisString', metavar='text', help='my analysis string', required=False) # optional interface
parser.add_argument('--add_mc_conv', help="Add the converter from mcparticle to mcparticle+001", action="store_true")
parser.add_argument('--add_fdd_conv', help="Add the fdd converter", action="store_true")
parser.add_argument('--add_track_prop', help="Add track propagation to the innermost layer (TPC or ITS)", action="store_true")

coreArgs = ["cfgFileName","runData","runMC","add_mc_conv","add_fdd_conv","add_track_prop"]

########################
# Interface Parameters #
########################


# aod
parser.add_argument('--aod', help="Add your AOD File with path", action="store", type=str)

# json output
parser.add_argument('--outputjson', help="Your Output JSON Config Fİle", action="store", type=str)

# only select
parser.add_argument('--onlySelect', help="Activate only selected JSON configs", action="store",choices=["true","false"], default="false", type=str.lower)

# table-maker cfg
parser.add_argument('--cfgEventCuts', help="Configure Cuts with commas", choices=analysisCutDatabase, nargs='*', action="store", type=str)
parser.add_argument('--cfgBarrelTrackCuts', help="Configure Cuts with commas", choices=analysisCutDatabase,nargs='*', action="store", type=str)
parser.add_argument('--cfgMuonCuts', help="Configure Cuts with commas", action="store", choices=analysisCutDatabase, nargs='*', type=str)
parser.add_argument('--cfgBarrelLowPt', help="Input type number", action="store", type=str)
parser.add_argument('--cfgMuonLowPt', help="Input type number", action="store", type=str)
parser.add_argument('--cfgNoQA', help="QA Selection true or false", action="store", choices=["true","false"], type=str)
parser.add_argument('--cfgDetailedQA', help="QA Detail Selection true or false", action="store", choices=["true","false"], type=str)
#parser.add_argument('--cfgIsRun2', help="Run selection true or false", action="store", choices=["true","false"], type=str) # no need
parser.add_argument('--cfgMinTpcSignal', help="Input type number", action="store", type=str)
parser.add_argument('--cfgMaxTpcSignal', help="Input type number", action="store", type=str)
parser.add_argument('--cfgMCsignals', help="Configure MCSignals with commas", action="store",choices=MCSignalDatabase, nargs='*', type=str)

# table-maker process
parser.add_argument('--process', help="Process Selection options true or false (string)", action="store", choices=tablemakerProcessAllSelections, nargs='*', type=str)

# Run Selection : event-selection-task ,bc-selection-task, multiplicity-table, track-extension no refactor
parser.add_argument('--run', help="Run Selection", action="store", choices=['2','3'], type=str, required=True)
#parser.add_argument('--processRun2', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) # no need
#parser.add_argument('--processRun3', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) # no need

# event-selection-task
parser.add_argument('--syst', help="Collision System Selection Input pp or PbPb", action="store", choices=['pp','PbPb'], type=str)
parser.add_argument('--muonSelection', help="Muon Selection Input Type Number", action="store", type=str)
parser.add_argument('--customDeltaBC', help="CustomDeltaBC Input Type Number", action="store", type=str)
#parser.add_argument('--isMC', help="Is it Monte Carlo options true or false", action="store", choices=["true","false"],default="false", type=str, required=True) # no need

# track-propagation
parser.add_argument('--processStandard', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processCovariance', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# tof-pid-full, tof-pid for run3 ???
parser.add_argument('--isProcessEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
#parser.add_argument('--processEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #no need
#parser.add_argument('--processNoEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)#no need

#tof-pid-beta
parser.add_argument('--tof-expreso', help="Tof expreso Input Type Number", action="store", type=str)

#parser.add_argument('--processSelection', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #d-q barrel and d-q muon selection no need automatic with process tablemaker
#parser.add_argument('--processSelectionTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #only d-q barrel no need automatic with process tablemaker

# dummies
parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=processDummySelections, nargs='*', type=str) #event selection, barel track task, filter task

# d-q-track barrel-task

parser.add_argument('--isBarrelSelectionTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #d-q barrel and d-q muon selection
# d-q event selection task
#parser.add_argument('--processEventSelection', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) # no need

# d-q-filter-p-p-task
parser.add_argument('--cfgPairCuts', help="Configure Cuts with commas", action="store", choices=analysisCutDatabase, nargs='*', type=str) # run3
parser.add_argument('--cfgBarrelSels', help="Configure Barrel Selection example jpsiO2MCdebugCuts2::1 ", action="store", type=str) # run2 
parser.add_argument('--cfgMuonSels', help="Configure Muon Selection example muonHighPt::1", action="store", type=str) # run 2
parser.add_argument('--isFilterPPTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
#parser.add_argument('--processFilterPP', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3 no need
#parser.add_argument('--processFilterPPTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3 no need

# centrality-table
parser.add_argument('--est', help="Configure to centrality Table", action="store", choices=centralityTableSelections,nargs="*", type=str)

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
parser.add_argument('--pid', help="pid selection input", action="store", choices=PIDSelections, nargs='*', type=str)


"""Activate For Autocomplete. See to Libraries for Info"""
#argcomplete.autocomplete(parser)
extrargs = parser.parse_args()

configuredCommands = vars(extrargs) # for get extrargs



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
    
######################################################################################

commonDeps = ["o2-analysis-timestamp", "o2-analysis-event-selection", "o2-analysis-multiplicity-table"]
barrelDeps = ["o2-analysis-trackselection", "o2-analysis-trackextension","o2-analysis-pid-tof-base", "o2-analysis-pid-tof", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]
specificDeps = {
  "processFull" : [],
  "processFullTiny" : [],
  "processFullWithCov" : [],
  "processFullWithCent" : ["o2-analysis-centrality-table"],
  "processBarrelOnly" : [],
  "processBarrelOnlyWithCov" : [],
  "processBarrelOnlyWithV0Bits" : ["o2-analysis-dq-v0-selector", "o2-analysis-weak-decay-indices"],
  "processBarrelOnlyWithEventFilter" : ["o2-analysis-dq-filter-pp"],
  "processBarrelOnlyWithCent" : ["o2-analysis-centrality-table"],
  "processMuonOnly" : [],
  "processMuonOnlyWithCov" : [],
  "processMuonOnlyWithCent" : ["o2-analysis-centrality-table"],
  "processMuonOnlyWithFilter" : ["o2-analysis-dq-filter-pp"]
  #"processFullWithCentWithV0Bits" : ["o2-analysis-centrality-table","o2-analysis-dq-v0-selector", "o2-analysis-weak-decay-indices"],
  #"processFullWithEventFilterWithV0Bits" : ["o2-analysis-dq-filter-pp","o2-analysis-dq-v0-selector", "o2-analysis-weak-decay-indices"],
} 

# Definition of all the tables we may write
tables = {
  "ReducedEvents" : {"table": "AOD/REDUCEDEVENT/0", "treename": "ReducedEvents"},
  "ReducedEventsExtended" : {"table": "AOD/REEXTENDED/0", "treename": "ReducedEventsExtended"},
  "ReducedEventsVtxCov" : {"table": "AOD/REVTXCOV/0", "treename": "ReducedEventsVtxCov"},
  "ReducedMCEventLabels" : {"table": "AOD/REMCCOLLBL/0", "treename": "ReducedMCEventLabels"},
  "ReducedMCEvents" : {"table": "AOD/REMC/0", "treename": "ReducedMCEvents"},
  "ReducedTracks" : {"table": "AOD/REDUCEDTRACK/0", "treename": "ReducedTracks"},
  "ReducedTracksBarrel" : {"table": "AOD/RTBARREL/0", "treename": "ReducedTracksBarrel"},
  "ReducedTracksBarrelCov" : {"table": "AOD/RTBARRELCOV/0", "treename": "ReducedTracksBarrelCov"},
  "ReducedTracksBarrelPID" : {"table": "AOD/RTBARRELPID/0", "treename": "ReducedTracksBarrelPID"},
  "ReducedTracksBarrelLabels" : {"table": "AOD/RTBARRELLABELS/0", "treename": "ReducedTracksBarrelLabels"},
  "ReducedMCTracks" : {"table": "AOD/RTMC/0", "treename": "ReducedMCTracks"},
  "ReducedMuons" : {"table": "AOD/RTMUON/0", "treename": "ReducedMuons"},
  "ReducedMuonsExtra" : {"table": "AOD/RTMUONEXTRA/0", "treename": "ReducedMuonsExtra"},
  "ReducedMuonsCov" : {"table": "AOD/RTMUONCOV/0", "treename": "ReducedMuonsCov"},
  "ReducedMuonsLabels" : {"table": "AOD/RTMUONSLABELS/0", "treename": "ReducedMuonsLabels"}
}
# Tables to be written, per process function
commonTables = ["ReducedEvents", "ReducedEventsExtended", "ReducedEventsVtxCov"]
barrelCommonTables = ["ReducedTracks","ReducedTracksBarrel","ReducedTracksBarrelPID"]
muonCommonTables = ["ReducedMuons", "ReducedMuonsExtra"]
specificTables = {
  "processFull" : [],
  "processFullTiny" : [],
  "processFullWithCov" : ["ReducedTracksBarrelCov", "ReducedMuonsCov"],
  "processFullWithCent" : [],
  "processBarrelOnly" : [],
  "processBarrelOnlyWithCov" : ["ReducedTracksBarrelCov"],
  "processBarrelOnlyWithV0Bits" : [],
  "processBarrelOnlyWithEventFilter" : [],
  "processBarrelOnlyWithCent" : [],
  "processMuonOnly" : [],
  "processMuonOnlyWithCov" : ["ReducedMuonsCov"],
  "processMuonOnlyWithCent" : [],
  "processMuonOnlyWithFilter" : []
}

# Make some checks on provided arguments
if len(sys.argv) < 3:
  print("ERROR: Invalid syntax! The command line should look like this:")
  print("  ./IRunTableMaker.py <yourConfig.json> <runData|runMC> --param value [task:param:value] ...")
  sys.exit()

# Load the configuration file provided as the first parameter
#TODO: Config file gerçekten pathimizde var mı? bunun için transacation management yaz.
config = {}
cfgFileName = 'configTableMakerDataRun3.json'
with open(extrargs.cfgFileName) as configFile:
  config = json.load(configFile)

# Check whether we run over data or MC
if not (extrargs.runMC or extrargs.runData):
  print("ERROR: You have to specify either runMC or runData !")
  sys.exit()

runOverMC = False
if (extrargs.runMC):
  runOverMC = True

print("runOverMC ",runOverMC)

# Optional Interface
"""
if extrargs.analysisString != "":
  args = [line.split(':') for line in extrargs.analysisString.split(',') if line]
  for arg in args:
    config[arg[0]][arg[1]] = arg[2]
"""



tasksInDataRun3 = ["internal-dpl-clock, internal-dpl-aod-reader, internal-dpl-aod-spawner, internal-dpl-aod-index-builder, timestamp-task, track-propagation, tof-pid-full, tpc-pid-full, bc-selection-task, multiplicity-table, centrality-table, tof-signal, track-extension, weak-decay-indices-v0, tof-pid, event-selection-task, tof-pid-beta, tof-event-time, track-selection, weak-decay-indices-cascades, v0-selector, d-q-barrel-track-selection-task, d-q-muons-selection, d-q-event-selection-task, d-q-filter-p-p-task, track-pid-qa, v0-gamma-qa, table-maker, internal-dpl-aod-global-analysis-file-sink, internal-dpl-aod-writer"]
tasksInDataRun2 = ["internal-dpl-clock, internal-dpl-aod-reader, internal-dpl-aod-spawner, internal-dpl-aod-index-builder, timestamp-task, tof-pid-full, tpc-pid-full, bc-selection-task, multiplicity-table, centrality-table, tof-signal, track-extension, weak-decay-indices-v0, tof-pid, event-selection-task, tof-pid-beta, track-selection, weak-decay-indices-cascades, v0-selector, d-q-barrel-track-selection-task, d-q-muons-selection, d-q-event-selection-task, d-q-filter-p-p-task, track-pid-qa, v0-gamma-qa, table-maker, internal-dpl-aod-global-analysis-file-sink, internal-dpl-aod-writer"]
tasksInMCRun3 = ["internal-dpl-clock, internal-dpl-aod-reader, internal-dpl-aod-spawner, internal-dpl-aod-index-builder, mc-converter, timestamp-task, track-propagation, tof-pid-full, tpc-pid-full, bc-selection-task, tof-signal, track-extension, tof-pid, event-selection-task, tof-pid-beta, track-selection, table-maker-m-c, multiplicity-table, internal-dpl-aod-global-analysis-file-sink, internal-dpl-aod-writer"]
tasksInMCRun2 = ["internal-dpl-clock, internal-dpl-aod-reader, internal-dpl-aod-spawner, internal-dpl-aod-index-builder, mc-converter, timestamp-task, tof-pid-full, tpc-pid-full, bc-selection-task, multiplicity-table, tof-signal, track-extension, tof-pid, event-selection-task, tof-pid-beta, track-selection, table-maker-m-c, internal-dpl-aod-global-analysis-file-sink, internal-dpl-aod-writer"]
taskNameInConfig = "table-maker"
taskNameInCommandLine = "o2-analysis-dq-table-maker"
if runOverMC == True:
  taskNameInConfig = "table-maker-m-c"
  taskNameInCommandLine = "o2-analysis-dq-table-maker-mc"

"""
Transaction Management TODO
"""
if not taskNameInConfig in config:
  print("ERROR: Task to be run not found in the configuration file!")
  sys.exit()
  
"""
if not tasksInDataRun3 in config:
  print("ERROR: Task to be run not found in the configuration file!")
  sys.exit()
if not tasksInDataRun2 in config:
  print("ERROR: Task to be run not found in the configuration file!")
  sys.exit()
if not tasksInMCRun3 in config:
  print("ERROR: Task to be run not found in the configuration file!")
  sys.exit()
if not tasksInMCRun2 in config:
  print("ERROR: Task to be run not found in the configuration file!")
  sys.exit()
"""

# List for config JSON values
configValueList=[]
#print(configuredCommands)

for key, value in config.items():
    if type(value) == type(config):
        for value,value2 in value.items():
            configValueList += [value]  
"""
for key, value in configuredCommands.items():
    #print(type(value))
    if value != None and (not key in coreArgs):
        print(key)
"""
                

###
for key, value in config.items():
    #print("key List = ", key)
    #print("value List = ", value)
    #print(type(value))
    if type(value) == type(config):
        #print(value, type(value))
        for value, value2 in value.items():
            #print(value)
            
            # aod
            if value =='aod-file' and extrargs.aod:
                config[key][value] = extrargs.aod
                
            # Process Table Maker
            if (value in tablemakerProcessAllParameters) and extrargs.process:
                if value in extrargs.process:
                    value2 = "true"
                    config[key][value] = value2
                    
                    # check extraargs is contain Full Barrel Muon or Bcs
                    full_search = [s for s in extrargs.process if "Full" in s]
                    barrel_search = [s for s in extrargs.process if "Barrel" in s]
                    muon_search = [s for s in extrargs.process if "Muon" in s]
                    bcs_search = [s for s in extrargs.process if "BCs" in s]   
                    
                    
                    
                                        
                    # Automatic Activate and Disable regarding to process func. in tablemaker
                    # todo: dq-barrel ve muon taskı içeride var mı kontrol için if statement yaz
                    if len(full_search) > 0 and extrargs.runData:
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                            config["d-q-muons-selection"]["processSelection"] = "true"
                            config["d-q-event-selection-task"]["processEventSelection"] = "true"
                                   
                    if len(barrel_search) > 0 and extrargs.runData:
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "true"
                    if len(barrel_search) == 0 and len(full_search) == 0 and extrargs.runData:
                            config["d-q-barrel-track-selection-task"]["processSelection"] = "false"
                            
                    if len(muon_search) > 0 and extrargs.runData:
                            config["d-q-muons-selection"]["processSelection"] = "true"
                    if len(muon_search) == 0 and len(full_search) == 0 and extrargs.runData:
                            config["d-q-muons-selection"]["processSelection"] = "false"
                            
                    if len(bcs_search) > 0 and extrargs.runData:
                            config["d-q-event-selection-task"]["processEventSelection"] = "true"
                    if len(bcs_search) == 0 and len(full_search) == 0 and extrargs.runData:
                            config["d-q-event-selection-task"]["processEventSelection"] = "false"

                                                                                
                elif extrargs.onlySelect == "true":
                    value2 = "false"
                    config[key][value] = value2
                    
            if value =='cfgPairCuts' and extrargs.cfgPairCuts:
                if type(extrargs.cfgPairCuts) == type(clist):
                    extrargs.cfgPairCuts = listToString(extrargs.cfgPairCuts) 
                config[key][value] = extrargs.cfgPairCuts
            if value == 'cfgBarrelSels' and extrargs.cfgBarrelSels:
                config[key][value] = extrargs.cfgBarrelSels
            if value == 'cfgMuonSels' and extrargs.cfgMuonSels:
                config[key][value] = extrargs.cfgMuonSels
            if value =='processFilterPPTiny' and extrargs.isFilterPPTiny == True:
                config[key][value] = True
                config[key]["processFilterPP"] = False
            elif value =='processFilterPPTiny' and extrargs.isFilterPPTiny == False:
                config[key][value] = False
                config[key]["processFilterPP"] = True         
                    
            # Run 2/3 and MC/DATA Selection  Automations      
            
            if extrargs.run == "2":
                if value == 'isRun3':
                    config[key][value] = "false"
                if value == 'processRun3':
                    config[key][value] = "false"
                if value == 'processRun2':
                    config[key][value] = "true"
            if extrargs.run == "3":
                if value == 'isRun3':
                    config[key][value] = "true"
                if value == 'processRun3':
                    config[key][value] = "true"
                if value == 'processRun2':
                    config[key][value] = "false"
            
            if extrargs.run == '2' and extrargs.runMC:
                if value == 'isRun2MC':
                    config[key][value] = "true"
            if extrargs.run != '2' and extrargs.runData:
                if value == 'isRun2MC':
                    config[key][value] = "false"
                                            
            if value == "isMC" and extrargs.runMC:
                    config[key][value] = "true"
            if value == "isMC" and extrargs.runData:
                    config[key][value] = "false"                        
                
            
            
                
            # PID Selections
            if  (value in PIDParameters) and extrargs.pid:
                if value in extrargs.pid:
                    value2 = "1"
                    config[key][value] = value2
                elif extrargs.onlySelect == "true":
                    value2 = "-1"
                    config[key][value] = value2
                    
            # v0-selector
            if value =='d_bz' and extrargs.d_bz:
                config[key][value] = extrargs.d_bz
            if value == 'v0cospa' and extrargs.v0cospa:
                config[key][value] = extrargs.v0cospa
            if value == 'dcav0dau' and extrargs.dcav0dau:
                config[key][value] = extrargs.dcav0dau
            if value =='v0Rmin' and extrargs.v0Rmin:
                config[key][value] = extrargs.v0Rmin
            if value == 'v0Rmax' and extrargs.v0Rmax:
                config[key][value] = extrargs.v0Rmax
            if value == 'dcamin' and extrargs.dcamin:
                config[key][value] = extrargs.dcamin
            if value == 'dcamax' and extrargs.dcamax:
                config[key][value] = extrargs.dcamax
            if value =='mincrossedrows' and extrargs.mincrossedrows:
                config[key][value] = extrargs.mincrossedrows
            if value == 'maxchi2tpc' and extrargs.maxchi2tpc:
                config[key][value] = extrargs.maxchi2tpc
                
            # centrality table
            if (value in centralityTableParameters) and extrargs.est:
                if value in extrargs.est:
                    value2 = "1"
                    config[key][value] = value2
                elif extrargs.onlySelect == "true":
                    value2 = "-1"
                    config[key][value] = value2
                    
            # cfg in TableMaker
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                if type(extrargs.cfgEventCuts) == type(clist):
                    extrargs.cfgEventCuts = listToString(extrargs.cfgEventCuts)
                config[key][value] = extrargs.cfgEventCuts
            if value == 'cfgBarrelTrackCuts' and extrargs.cfgBarrelTrackCuts:
                if type(extrargs.cfgBarrelTrackCuts) == type(clist):
                    extrargs.cfgBarrelTrackCuts = listToString(extrargs.cfgBarrelTrackCuts)
                config[key][value] = extrargs.cfgBarrelTrackCuts
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                if type(extrargs.cfgMuonCuts) == type(clist):
                    extrargs.cfgMuonCuts = listToString(extrargs.cfgMuonCuts)                
                config[key][value] = extrargs.cfgMuonCuts
            if value == 'cfgBarrelLowPt' and extrargs.cfgBarrelLowPt:
                config[key][value] = extrargs.cfgBarrelLowPt
            if value == 'cfgMuonLowPt' and extrargs.cfgMuonLowPt:
                config[key][value] = extrargs.cfgMuonLowPt
            if value =='cfgNoQA' and extrargs.cfgNoQA:
                config[key][value] = extrargs.cfgNoQA
            if value == 'cfgDetailedQA' and extrargs.cfgDetailedQA:
                config[key][value] = extrargs.cfgDetailedQA
            if value == 'cfgIsRun2' and extrargs.run == "2":
                config[key][value] = "true"
            if value =='cfgMinTpcSignal' and extrargs.cfgMinTpcSignal:
                config[key][value] = extrargs.cfgMinTpcSignal
            if value == 'cfgMaxTpcSignal' and extrargs.cfgMaxTpcSignal:
                config[key][value] = extrargs.cfgMaxTpcSignal
            if value == 'cfgMCsignals' and extrargs.cfgMCsignals:
                if type(extrargs.cfgMCsignals) == type(clist):
                    extrargs.cfgMCsignals = listToString(extrargs.cfgMCsignals)                     
                #extrargs.cfgMCsignals = ",".join(extrargs.cfgMCsignals)
                config[key][value] = extrargs.cfgMCsignals

            # event-selection
            if value == 'syst' and extrargs.syst:
                config[key][value] = extrargs.syst
            if value =='muonSelection' and extrargs.muonSelection:
                config[key][value] = extrargs.muonSelection
            if value == 'customDeltaBC' and extrargs.customDeltaBC:
                config[key][value] = extrargs.customDeltaBC
                
            # tof-pid-beta
            if value == 'tof-expreso' and extrargs.tof_expreso:
                config[key][value] = extrargs.tof_expreso
                
            # tof-pid-full, tof-pid for run3
            if value == 'processEvTime' and extrargs.isProcessEvTime == True:
                config[key][value] = True
                config[key]["processNoEvTime"] = False
            elif value == 'processEvTime' and extrargs.isProcessEvTime == False:
                config[key][value] = False
                config[key]["processNoEvTime"] = True
                    
            # all d-q tasks and selections TODO Eğer TableMakerdakiyle aynı şeyi isterlerse refactor
            if value == 'cfgWithQA' and extrargs.cfgWithQA:
                config[key][value] = extrargs.cfgWithQA                  
            # track-propagation
            if value =='processStandard' and extrargs.processStandard:
                config[key][value] = extrargs.processStandard
            if value == 'processCovariance' and extrargs.processCovariance:
                config[key][value] = extrargs.processCovariance
            # dq-barrel-track-selection-task
            if value =='processSelectionTiny' and extrargs.isBarrelSelectionTiny == True:
                config[key][value] = extrargs.isBarrelSelectionTiny
                config[key]["processSelection"] = False
                
            # dummy selection
            if value == 'processDummy' and extrargs.processDummy and extrargs.runData:
                if extrargs.processDummy == "event":
                    config['d-q-event-selection-task']['processDummy'] = True
                if extrargs.processDummy == "filter":
                    config['d-q-filter-p-p-task']['processDummy'] = True
                if extrargs.processDummy == "barrel":
                    config['d-q-barrel-track-selection-task']['processDummy'] = True

###



# Write the updated configuration file into a temporary file
updatedConfigFileName = "tempConfig.json"
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
depsToRun = {}
for dep in commonDeps:
  depsToRun[dep] = 1

for processFunc in specificDeps.keys():
  if not processFunc in config[taskNameInConfig].keys():
    continue        
  if config[taskNameInConfig][processFunc] == "true":      
    if "processFull" in processFunc or "processBarrel" in processFunc:
      for dep in barrelDeps:
        depsToRun[dep] = 1
    for dep in specificDeps[processFunc]:
      depsToRun[dep] = 1

# Check which tables are required in the output
tablesToProduce = {}
for table in commonTables:
  tablesToProduce[table] = 1

if runOverMC == True:
  tablesToProduce["ReducedMCEvents"] = 1
  tablesToProduce["ReducedMCEventLabels"] = 1
  
for processFunc in specificDeps.keys():
  if not processFunc in config[taskNameInConfig].keys():
    continue          
  if config[taskNameInConfig][processFunc] == "true":
    print("processFunc ========")
    print(processFunc)
    if "processFull" in processFunc or "processBarrel" in processFunc:
      print("common barrel tables==========")      
      for table in barrelCommonTables:
        print(table)      
        tablesToProduce[table] = 1
      if runOverMC == True:
        tablesToProduce["ReducedTracksBarrelLabels"] = 1
    if "processFull" in processFunc or "processMuon" in processFunc:
      print("common muon tables==========")      
      for table in muonCommonTables:
        print(table)
        tablesToProduce[table] = 1
      if runOverMC == True:
        tablesToProduce["ReducedMuonsLabels"] = 1  
    if runOverMC == True:
      tablesToProduce["ReducedMCTracks"] = 1
    print("specific tables==========")      
    for table in specificTables[processFunc]:
      print(table)      
      tablesToProduce[table] = 1

# Generate the aod-writer output descriptor json file
writerConfig = {}
writerConfig["OutputDirector"] = {
  "debugmode": True,
  "resfile": "reducedAod",
  "resfilemode": "RECREATE",
  "ntfmerge": 1,
  "OutputDescriptors": []
}
iTable = 0
for table in tablesToProduce.keys():
  writerConfig["OutputDirector"]["OutputDescriptors"].insert(iTable, tables[table])
  iTable += 1
  
writerConfigFileName = "aodWriterTempConfig.json"
with open(writerConfigFileName,'w') as writerConfigFile:
  json.dump(writerConfig, writerConfigFile, indent=2)  
  
print(writerConfig)
#sys.exit()
      
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --severity error --shm-segment-size 12000000000 --aod-writer-json " + writerConfigFileName + " -b"
for dep in depsToRun.keys():
  commandToRun += " | " + dep + " --configuration json://" + updatedConfigFileName + " -b"

if extrargs.add_mc_conv:
    commandToRun += " | o2-analysis-mc-converter --configuration json://" + updatedConfigFileName + " -b"

if extrargs.add_fdd_conv:
    commandToRun += " | o2-analysis-fdd-converter --configuration json://" + updatedConfigFileName + " -b"

if extrargs.add_track_prop:
    commandToRun += " | o2-analysis-track-propagation --configuration json://" + updatedConfigFileName + " -b"

print("====================================================================================================================")
print("Command to run:")
print(commandToRun)
print("====================================================================================================================")
print("Tables to produce:")
print(tablesToProduce.keys())
print("====================================================================================================================")
#sys.exit()

# Listing Added Commands
print("Args provided configurations List")
print("====================================================================================================================")
for key,value in configuredCommands.items():
    if(value != None):
        if type(value) == type(clist):
            listToString(value)
        print("--"+key,":", value)

os.system(commandToRun)
