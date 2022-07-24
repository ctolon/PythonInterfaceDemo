#!/usr/bin/env python3

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

#################################
# JSON Database Read and Upload #
#################################

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
parser.add_argument('cfgFileName', metavar='text', default='config.json', help='config file name')
parser.add_argument('-runData', help="Run over data", action="store_true")
parser.add_argument('-runMC', help="Run over MC", action="store_true")
#parser.add_argument('analysisString', metavar='text', help='my analysis string')
parser.add_argument('--add_mc_conv', help="Add the converter from mcparticle to mcparticle+001", action="store_true")
parser.add_argument('--add_fdd_conv', help="Add the fdd converter", action="store_true")
parser.add_argument('--add_track_prop', help="Add track propagation to the innermost layer (TPC or ITS)", action="store_true")

##################
# Interface Part #
##################

# aod
parser.add_argument('--aod', help="Add your AOD File with path", action="store", type=str)

#json output
parser.add_argument('--outputjson', help="Your Output JSON Config Fİle", action="store", type=str)

# table-maker cfg
parser.add_argument('--cfgEventCuts', help="Configure Cuts with commas", choices=cut_database, nargs='*', action="store", type=str)
parser.add_argument('--cfgBarrelTrackCuts', help="Configure Cuts with commas", choices=cut_database,nargs='*', action="store", type=str)
parser.add_argument('--cfgMuonCuts', help="Configure Cuts with commas", action="store", choices=cut_database, nargs='*', type=str)
parser.add_argument('--cfgBarrelLowPt', help="Input type number", action="store", type=str)
parser.add_argument('--cfgMuonLowPt', help="Input type number", action="store", type=str)
parser.add_argument('--cfgNoQA', help="QA Selection true or false", action="store", choices=["true","false"], type=str)
parser.add_argument('--cfgDetailedQA', help="QA Detail Selection true or false", action="store", choices=["true","false"], type=str)
parser.add_argument('--cfgIsRun2', help="Run selection true or false", action="store", choices=["true","false"], type=str)
parser.add_argument('--cfgMinTpcSignal', help="Input type number", action="store", type=str)
parser.add_argument('--cfgMaxTpcSignal', help="Input type number", action="store", type=str)
parser.add_argument('--cfgMCsignals', help="Configure MCSignals with commas", action="store",choices=mcsignal_database,nargs='*', type=str)

# table-maker process
parser.add_argument('--processFull', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processFullTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processFullWithCov', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processFullWithCent', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processBarrelOnlyWithV0Bits', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processBarrelOnlyEventFilter', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processBarrelOnlyWithCent', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processBarrelOnlyWithCov', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processBarrelOnly', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processMuonOnlyWithCent', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processMuonOnlyWithCov', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processMuonOnly', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processMuonOnlyWithFilter', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processOnlyBCs', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# event-selection-task ,bc-selection-task, multiplicity-table, track-extension no refactor
parser.add_argument('--processRun2', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processRun3', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# event-selection-task
parser.add_argument('--syst', help="Collision System Selection Input pp or PbPb", action="store", choices=['pp','PbPb'], type=str)
parser.add_argument('--muonSelection', help="Muon Selection Input Type Number", action="store", type=str)
parser.add_argument('--customDeltaBC', help="CustomDeltaBC Input Type Number", action="store", type=str)
parser.add_argument('--isMC', help="Is it Monte Carlo options true or false", action="store", choices=["true","false"], type=str)

# track-propagation
parser.add_argument('--processStandard', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processCovariance', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

# tof-pid-full, tof-pid for run3
parser.add_argument('--processEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)
parser.add_argument('--processNoEvTime', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str)

#tof-pid-beta
parser.add_argument('--tof-expreso', help="Tof expreso Input Type Number", action="store", type=str)

# need refactoring part
parser.add_argument('--processSelection', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #d-q barrel and d-q muon selection
parser.add_argument('--processSelectionTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #only d-q barrel
parser.add_argument('--processDummy', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #event selection, barel track task, filter task

#d-q-event-selection-task
parser.add_argument('--processEventSelection', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #d-q barrel and d-q muon selection

# d-q-filter-p-p-task
parser.add_argument('--cfgPairCuts', help="Configure Cuts with commas", action="store", choices=cut_database, nargs='*', type=str) # run3
parser.add_argument('--cfgBarrelSels', help="Configure Barrel Selection example jpsiO2MCdebugCuts2::1 ", action="store", type=str) # run2 
parser.add_argument('--cfgMuonSels', help="Configure Muon Selection example muonHighPt::1", action="store", type=str) # run 2
parser.add_argument('--processFilterPP', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3
parser.add_argument('--processFilterPPTiny', help="Process Selection options true or false (string)", action="store", choices=['true','false'], type=str) #run 3

# centrality-table
parser.add_argument('--estV0M', help="Input 1 or -1", action="store", choices=["-1","1"], type=str)
parser.add_argument('--estRun2SPDtks', help="Input 1 or -1", action="store", choices=["-1","1"], type=str)
parser.add_argument('--estRun2SPDcls', help="Input 1 or -1", action="store", choices=["-1","1"], type=str)
parser.add_argument('--estRun2CL0', help="Input 1 or -1", action="store", choices=["-1","1"], type=str)
parser.add_argument('--estRun2CL1', help="Input 1 or -1", action="store", choices=["-1","1"], type=str)

# timestamp-task
parser.add_argument('--isRun2MC', help="Selection the Process is MC or Not", action="store", choices=['true','false'], type=str)

# track-selection
parser.add_argument('--isRun3', help="Add track propagation to the innermost layer (TPC or ITS)", action="store", choices=['true','false'], type=str)

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
parser.add_argument('--pid-el', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-mu', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-pi', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-ka', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-pr', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-de', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-tr', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-he', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)
parser.add_argument('--pid-al', help="pid selection input 1 or -1", action="store", choices=["1","-1"], type=str)

extrargs = parser.parse_args()

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
  print("  ./IRunTableMaker.py <yourConfig.json> <runData|runMC> [task:param:value] ...")
  sys.exit()

# Load the configuration file provided as the first parameter
#TODO: Config file gerçekten pathimizde var mı? bunun için transacation management yaz.
config = {}
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

#Disabled Part
"""
if extrargs.analysisString != "":
  args = [line.split(':') for line in extrargs.analysisString.split(',') if line]
  for arg in args:
    config[arg[0]][arg[1]] = arg[2]
"""

taskNameInConfig = "table-maker"
taskNameInCommandLine = "o2-analysis-dq-table-maker"
if runOverMC == True:
  taskNameInConfig = "table-maker-m-c"
  taskNameInCommandLine = "o2-analysis-dq-table-maker-mc"

if not taskNameInConfig in config:
  print("ERROR: Task to be run not found in the configuration file!")
  sys.exit()
  
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
                # tablemaker cfg
                if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                    extrargs.cfgEventCuts = ",".join(extrargs.cfgEventCuts)
                    config[key][value] = extrargs.cfgEventCuts
                if value == 'cfgBarrelTrackCuts' and extrargs.cfgBarrelTrackCuts:
                    extrargs.cfgBarrelTrackCuts = ",".join(extrargs.cfgBarrelTrackCuts)
                    config[key][value] = extrargs.cfgBarrelTrackCuts
                if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                   extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                   config[key][value] = extrargs.cfgMuonCuts
                if value == 'cfgBarrelLowPt' and extrargs.cfgBarrelLowPt:
                    config[key][value] = extrargs.cfgBarrelLowPt
                if value == 'cfgMuonLowPt' and extrargs.cfgMuonLowPt:
                    config[key][value] = extrargs.cfgMuonLowPt
                if value =='cfgNoQA' and extrargs.cfgNoQA:
                   config[key][value] = extrargs.cfgNoQA
                if value == 'cfgDetailedQA' and extrargs.cfgDetailedQA:
                    config[key][value] = extrargs.cfgDetailedQA
                if value == 'cfgIsRun2' and extrargs.cfgIsRun2:
                    config[key][value] = extrargs.cfgIsRun2
                if value =='cfgMinTpcSignal' and extrargs.cfgMinTpcSignal:
                   config[key][value] = extrargs.cfgMinTpcSignal
                if value == 'cfgMaxTpcSignal' and extrargs.cfgMaxTpcSignal:
                    config[key][value] = extrargs.cfgMaxTpcSignal
                if value == 'cfgMCsignals' and extrargs.cfgMCsignals:                   
                    extrargs.cfgMCsignals = ",".join(extrargs.cfgMCsignals)
                    config[key][value] = extrargs.cfgMCsignals
                # process
                if value =='processFull' and extrargs.processFull:
                   config[key][value] = extrargs.processFull
                if value == 'processFullTiny' and extrargs.processFullTiny:
                    config[key][value] = extrargs.processFullTiny
                if value == 'processFullWithCov' and extrargs.processFullWithCov:
                    config[key][value] = extrargs.processFullWithCov
                if value =='processFullWithCent' and extrargs.processFullWithCent:
                   config[key][value] = extrargs.processFullWithCent
                if value == 'processBarrelOnlyWithV0Bits' and extrargs.processBarrelOnlyWithV0Bits:
                    config[key][value] = extrargs.processBarrelOnlyWithV0Bits
                if value == 'processBarrelOnlyEventFilter' and extrargs.processBarrelOnlyEventFilter:
                    config[key][value] = extrargs.processBarrelOnlyEventFilter
                if value =='processBarrelOnlyWithCent' and extrargs.processBarrelOnlyWithCent:
                   config[key][value] = extrargs.processBarrelOnlyWithCent
                if value == 'processBarrelOnlyWithCov' and extrargs.processBarrelOnlyWithCov:
                    config[key][value] = extrargs.processBarrelOnlyWithCov
                if value == 'processBarrelOnly' and extrargs.processBarrelOnly:
                    config[key][value] = extrargs.processBarrelOnly
                if value =='processMuonOnlyWithCent' and extrargs.processMuonOnlyWithCent:
                   config[key][value] = extrargs.processMuonOnlyWithCent
                if value == 'processMuonOnlyWithCov' and extrargs.processMuonOnlyWithCov:
                    config[key][value] = extrargs.processMuonOnlyWithCov
                if value == 'processMuonOnly' and extrargs.processMuonOnly:
                    config[key][value] = extrargs.processMuonOnly
                if value =='processMuonOnlyWithFilter' and extrargs.processMuonOnlyWithFilter:
                   config[key][value] = extrargs.processMuonOnlyWithFilter
                if value == 'processOnlyBCs' and extrargs.processOnlyBCs:
                    config[key][value] = extrargs.processOnlyBCs
                # event-selection-task ,bc-selection-task, multiplicity-table, track-extension
                if value =='processRun2' and extrargs.processRun2:
                   config[key][value] = extrargs.processRun2
                if value == 'processRun3' and extrargs.processRun3:
                    config[key][value] = extrargs.processRun3
                # event-selection-task
                if value == 'syst' and extrargs.syst:
                    config[key][value] = extrargs.syst
                if value =='muonSelection' and extrargs.muonSelection:
                   config[key][value] = extrargs.muonSelection
                if value == 'customDeltaBC' and extrargs.customDeltaBC:
                    config[key][value] = extrargs.customDeltaBC
                if value == 'isMC' and extrargs.isMC:
                    config[key][value] = extrargs.isMC
                # track-propagation
                if value =='processStandard' and extrargs.processStandard:
                   config[key][value] = extrargs.processStandard
                if value == 'processCovariance' and extrargs.processCovariance:
                    config[key][value] = extrargs.processCovariance
                # tof-pid-full, tof-pid for run3
                if value == 'processEvTime' and extrargs.processEvTime:
                    config[key][value] = extrargs.processEvTime
                if value =='processNoEvTime' and extrargs.processNoEvTime:
                   config[key][value] = extrargs.processNoEvTime
                # tof-pid-beta
                if value == 'tof-expreso' and extrargs.tof_expreso:
                    config[key][value] = extrargs.tof_expreso
                # need refactoring part
                if value == 'processSelection' and extrargs.processSelection:
                    config[key][value] = extrargs.processSelection
                if value =='processSelectionTiny' and extrargs.processSelectionTiny:
                   config[key][value] = extrargs.processSelectionTiny
                if value == 'processDummy' and extrargs.processDummy:
                    config[key][value] = extrargs.processDummy
                # d-q-event-selection-task
                if value == 'processEventSelection' and extrargs.processEventSelection:
                    config[key][value] = extrargs.processEventSelection
                #d-q-filter-p-p-task
                if value =='cfgPairCuts' and extrargs.cfgPairCuts:
                    extrargs.cfgPairCuts = ",".join(extrargs.cfgPairCuts)
                    config[key][value] = extrargs.cfgPairCuts
                if value == 'cfgBarrelSels' and extrargs.cfgBarrelSels:
                    config[key][value] = extrargs.cfgBarrelSels
                if value == 'cfgMuonSels' and extrargs.cfgMuonSels:
                    config[key][value] = extrargs.cfgMuonSels
                if value =='processFilterPP' and extrargs.processFilterPP:
                   config[key][value] = extrargs.processFilterPP
                if value == 'processFilterPPTiny' and extrargs.processFilterPPTiny:
                    config[key][value] = extrargs.processFilterPPTiny
                # centrality-table
                if value =='estV0M' and extrargs.estV0M:
                   config[key][value] = extrargs.estV0M
                if value == 'estRun2SPDtks' and extrargs.estRun2SPDtks:
                    config[key][value] = extrargs.estRun2SPDtks
                if value == 'estRun2SPDcls' and extrargs.estRun2SPDcls:
                    config[key][value] = extrargs.estRun2SPDcls
                if value =='estRun2CL0' and extrargs.estRun2CL0:
                   config[key][value] = extrargs.estRun2CL0
                if value == 'estRun2CL1' and extrargs.estRun2CL1:
                    config[key][value] = extrargs.estRun2CL1
                # timestamp-task
                if value =='isRun2MC' and extrargs.isRun2MC:
                   config[key][value] = extrargs.isRun2MC
                # track-selection
                if value == 'isRun3' and extrargs.isRun3:
                    config[key][value] = extrargs.isRun3
                # all d-q tasks and selections
                if value == 'cfgWithQA' and extrargs.cfgWithQA:
                    config[key][value] = extrargs.cfgWithQA
                if value =='estRun2CL0' and extrargs.estRun2CL0:
                   config[key][value] = extrargs.estRun2CL0
                if value == 'estRun2CL1' and extrargs.estRun2CL1:
                    config[key][value] = extrargs.estRun2CL1
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
                # pid
                if value == 'pid-el' and extrargs.pid_el:
                    config[key][value] = extrargs.pid_el
                if value == 'pid-mu' and extrargs.pid_mu:
                    config[key][value] = extrargs.pid_mu
                if value == 'pid-pi' and extrargs.pid_pi:
                    config[key][value] = extrargs.pid_pi
                if value == 'pid-ka' and extrargs.pid_ka:
                    config[key][value] = extrargs.pid_ka
                if value == 'pid-pr' and extrargs.pid_pr:
                    config[key][value] = extrargs.pid_pr
                if value == 'pid-de' and extrargs.pid_de:
                    config[key][value] = extrargs.pid_de
                if value == 'pid-tr' and extrargs.pid_tr:
                    config[key][value] = extrargs.pid_tr
                if value == 'pid-he' and extrargs.pid_he:
                    config[key][value] = extrargs.pid_he
                if value == 'pid-al' and extrargs.pid_al:
                    config[key][value] = extrargs.pid_al

###

# Write the updated configuration file into a temporary file
#TODO: Config file json outputunu demodaki gibi transcation management yap.
updatedConfigFileName = "tempConfig.json"
with open(updatedConfigFileName,'w') as outputFile:
  json.dump(config, outputFile ,indent=2)

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
  json.dump(writerConfig, writerConfigFile)  
  
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

os.system(commandToRun)
