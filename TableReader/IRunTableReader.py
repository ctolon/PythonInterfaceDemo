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

# TODO: This arguments seems no needed. Because TableReader only works on data. Check them.
#parser.add_argument('-runData', help="Run over data", action="store_true")
#parser.add_argument('-runMC', help="Run over MC", action="store_true")

##################
# Interface Part #
##################

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

#commonDeps = ["o2-analysis-timestamp", "o2-analysis-event-selection", "o2-analysis-multiplicity-table", "o2-analysis-trackselection", "o2-analysis-track-propagation", "o2-analysis-pid-tof-base", "o2-analysis-pid-tof", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]

# Make some checks on provided arguments
if len(sys.argv) < 2:
  print("ERROR: Invalid syntax! The command line should look like this:")
  print("  ./IRunTableReader.py <yourConfig.json> [task|param|value] ...")
  sys.exit()

# Load the configuration file provided as the first parameter
#TODO: Config file gerçekten pathimizde var mı? bunun için transacation management yaz.
config = {}
with open(sys.argv[1]) as configFile:
  config = json.load(configFile)
  

#TODO: Don't need for TableReader. Check it.
"""
# Check whether we run over data or MC
if not ((sys.argv[2] == "runMC") or (sys.argv[2] == "runData")):
  print("ERROR: You have to specify either runMC or runData !")
  sys.exit()
"""

runOverMC = False
"""
if sys.argv[2] == "runMC":
  runOverMC = True
"""

"""
# Get all the user required modifications to the configuration file
for count in range(3, len(sys.argv)):
  param = sys.argv[count].split(":")
  if len(param) != 3:
    print("ERROR: Wrong parameter syntax: ", param)
    sys.exit()
  config[param[0]][param[1]] = param[2]
"""

#taskNameInConfig = "d-q-filter-p-p-task"
taskNameInCommandLine = "o2-analysis-dq-table-reader"
if runOverMC == True:
  #taskNameInConfig = "d-q-filter-p-p-task"
  taskNameInCommandLine = "o2-analysis-dq-table-reader"
"""
if not taskNameInConfig in config:
  print("ERROR: Task to be run not found in the configuration file!")
  sys.exit()
"""

for key, value in config.items():
    #print("key List = ", key)
    #print("value List = ", value)
    #print(type(value))
    if type(value) == type(config):
        #print(value, type(value))
        for value, value2 in value.items():
            #print(value)
            #aod
            if value =='aod-file' and extrargs.aod:
                config[key][value] = extrargs.aod                
            # analysis-event-selection
            if value == 'cfgMixingVars' and extrargs.cfgMixingVars:
                extrargs.cfgEventCuts = ",".join(extrargs.cfgMixingVars)
                config[key][value] = extrargs.cfgMixingVars
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                extrargs.cfgEventCuts = ",".join(extrargs.cfgEventCuts)
                config[key][value] = extrargs.cfgEventCuts
            if value =='cfgQA' and extrargs.cfgQA:
                config[key][value] = extrargs.cfgQA
            if value == 'processSkimmed' and extrargs.processSkimmed:
                config[key][value] = extrargs.processSkimmed
            if value == 'processDummy' and extrargs.processDummy:
                config[key][value] = extrargs.processDummy
            # analysis-muon-selection
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                config[key][value] = extrargs.cfgMuonCuts
            if value == 'cfgMuonMCSignals' and extrargs.cfgMuonMCSignals:
                extrargs.cfgMuonMCSignals = ",".join(extrargs.cfgMuonMCSignals)
                config[key][value] = extrargs.cfgMuonMCSignals
            if value == 'cfgQA' and extrargs.cfgQA:
                config[key][value] = extrargs.cfgQA
            if value =='processSkimmed' and extrargs.processSkimmed:
                config[key][value] = extrargs.processSkimmed
            if value == 'processDummy' and extrargs.processDummy:
                config[key][value] = extrargs.processDummy
            # analysis-track-selection
            if value =='cfgTrackCuts' and extrargs.cfgTrackCuts:
                extrargs.cfgTrackCuts = ",".join(extrargs.cfgTrackCuts)
                config[key][value] = extrargs.cfgTrackCuts
            if value == 'cfgTrackMCSignals' and extrargs.cfgTrackMCSignals:
                extrargs.cfgTrackMCSignals = ",".join(extrargs.cfgTrackMCSignals)
                config[key][value] = extrargs.cfgTrackMCSignals
            if value == 'cfgQA' and extrargs.cfgQA:
                config[key][value] = extrargs.cfgQA
            if value =='processSkimmed' and extrargs.processSkimmed:
                config[key][value] = extrargs.processSkimmed
            if value == 'processDummy' and extrargs.processDummy:
                config[key][value] = extrargs.processDummy
            # analysis-event-mixing ONLY FOR DATA
            if value == 'cfgTrackCuts' and extrargs.cfgTrackCuts:                   
                extrargs.cfgTrackCuts = ",".join(extrargs.cfgTrackCuts)
                config[key][value] = extrargs.cfgTrackCuts
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                config[key][value] = extrargs.cfgMuonCuts
            if value == 'processBarrelSkimmed' and extrargs.processBarrelSkimmed:
                config[key][value] = extrargs.processBarrelSkimmed
            if value == 'processMuonSkimmed' and extrargs.processMuonSkimmed:
                config[key][value] = extrargs.processMuonSkimmed
            if value == 'processBarrelMuonSkimmed' and extrargs.processBarrelMuonSkimmed:
                config[key][value] = extrargs.processBarrelMuonSkimmed
            if value == 'processDummy' and extrargs.processDummy:
                config[key][value] = extrargs.processDummy
            # analysis-same-event-pairing TODO: CCDB parts Can be added
            if value == 'cfgTrackCuts' and extrargs.cfgTrackCuts:                   
                extrargs.cfgTrackCuts = ",".join(extrargs.cfgTrackCuts)
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
            if value == 'cfgBarrelMCRecSignals' and extrargs.cfgBarrelMCRecSignals:
                extrargs.cfgBarrelMCRecSignals = ",".join(extrargs.cfgBarrelMCRecSignals)
                config[key][value] = extrargs.cfgBarrelMCRecSignals
            if value == 'cfgBarrelMCGenSignals' and extrargs.cfgBarrelMCGenSignals:
                extrargs.cfgBarrelMCGenSignals = ",".join(extrargs.cfgBarrelMCGenSignals)
                config[key][value] = extrargs.cfgBarrelMCGenSignals
            if value =='processJpsiToEESkimmed' and extrargs.processJpsiToEESkimmed:
                config[key][value] = extrargs.processJpsiToEESkimmed
            if value == 'processJpsiToMuMuSkimmed' and extrargs.processJpsiToMuMuSkimmed:
                config[key][value] = extrargs.processJpsiToMuMuSkimmed
            if value == 'processJpsiToMuMuVertexingSkimmed' and extrargs.processJpsiToMuMuVertexingSkimmed:
                config[key][value] = extrargs.processJpsiToMuMuVertexingSkimmed
            if value =='processElectronMuonSkimmed' and extrargs.processElectronMuonSkimmed:
                config[key][value] = extrargs.processElectronMuonSkimmed
            if value == 'processAllSkimmed' and extrargs.processAllSkimmed:
                config[key][value] = extrargs.processAllSkimmed
            # analysis-dilepton-hadron ONLY FOR DATA
            if value == 'cfgLeptonCuts' and extrargs.cfgLeptonCuts:
                extrargs.cfgLeptonCuts = ",".join(extrargs.cfgLeptonCuts)
                config[key][value] = extrargs.cfgLeptonCuts
            if value == 'processSkimmed' and extrargs.processSkimmed:
                config[key][value] = extrargs.Skimmed
            if value == 'processDummy' and extrargs.processDummy:
                config[key][value] = extrargs.processDummy
            # analysis-dilepton-track ONLY FOR MC
            if value == 'cfgBarrelMCRecSignals' and extrargs.cfgBarrelMCRecSignals:
                extrargs.cfgBarrelMCRecSignals = ",".join(extrargs.cfgBarrelMCRecSignals)
                config[key][value] = extrargs.cfgBarrelMCRecSignals
            if value == 'cfgBarrelMCGenSignals' and extrargs.cfgBarrelMCGenSignals:
                extrargs.cfgBarrelMCGenSignals = ",".join(extrargs.cfgBarrelMCGenSignals)
                config[key][value] = extrargs.cfgBarrelMCGenSignals
            if value == 'processSkimmed' and extrargs.processSkimmed:
                config[key][value] = extrargs.Skimmed
            if value == 'processDummy' and extrargs.processDummy:
                config[key][value] = extrargs.processDummy

# Write the updated configuration file into a temporary file
#TODO: Config file json outputunu demodaki gibi transcation management yap.
updatedConfigFileName = "tempConfig.json"
with open(updatedConfigFileName,'w') as outputFile:
  json.dump(config, outputFile)

# Check which dependencies need to be run
"""
depsToRun = {}
for dep in commonDeps:
  depsToRun[dep] = 1
"""
      
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --severity error --shm-segment-size 12000000000 -b"
"""
for dep in depsToRun.keys():
  commandToRun += " | " + dep + " --configuration json://" + updatedConfigFileName + " -b"
"""

print("====================================================================================================================")
print("Command to run:")
print(commandToRun)
print("====================================================================================================================")
os.system(commandToRun)
