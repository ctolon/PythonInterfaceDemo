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

##################
# Interface Part #
##################

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

commonDeps = ["o2-analysis-timestamp", "o2-analysis-event-selection", "o2-analysis-multiplicity-table", "o2-analysis-trackselection", "o2-analysis-track-propagation", "o2-analysis-pid-tof-base", "o2-analysis-pid-tof", "o2-analysis-pid-tof-full", "o2-analysis-pid-tof-beta", "o2-analysis-pid-tpc-full"]

# Make some checks on provided arguments
if len(sys.argv) < 3:
  print("ERROR: Invalid syntax! The command line should look like this:")
  print("  ./IFilterPPFull.py <yourConfig.json> <runData|runMC> [task|param|value] ...")
  sys.exit()

# Load the configuration file provided as the first parameter
#TODO: Config file gerçekten pathimizde var mı? bunun için transacation management yaz.
config = {}
with open(sys.argv[1]) as configFile:
  config = json.load(configFile)

# Check whether we run over data or MC
if not ((sys.argv[2] == "runMC") or (sys.argv[2] == "runData")):
  print("ERROR: You have to specify either runMC or runData !")
  sys.exit()

runOverMC = False
if sys.argv[2] == "runMC":
  runOverMC = True

# Get all the user required modifications to the configuration file
"""
for count in range(3, len(sys.argv)):
  param = sys.argv[count].split(":")
  if len(param) != 3:
    print("ERROR: Wrong parameter syntax: ", param)
    sys.exit()
  config[param[0]][param[1]] = param[2]
"""


taskNameInConfig = "d-q-filter-p-p-task"
taskNameInCommandLine = "o2-analysis-dq-filter-pp"
if runOverMC == True:
  taskNameInConfig = "d-q-filter-p-p-task"
  taskNameInCommandLine = "o2-analysis-dq-filter-pp"

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
            # d-q tasks
            if value == 'cfgWithQA' and extrargs.cfgWithQA:
                config[key][value] = extrargs.cfgWithQA 
            if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                extrargs.cfgEventCuts = ",".join(extrargs.cfgEventCuts)
                config[key][value] = extrargs.cfgEventCuts
            if value == 'processEventSelection' and extrargs.processEventSelection:
                config[key][value] = extrargs.processEventSelection
            if value == 'processSelection' and extrargs.processSelection:
                config[key][value] = extrargs.processSelection
            if value == 'cfgBarrelTrackCuts' and extrargs.cfgBarrelTrackCuts:
                extrargs.cfgBarrelTrackCuts = ",".join(extrargs.cfgBarrelTrackCuts)
                config[key][value] = extrargs.cfgBarrelTrackCuts
            if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                config[key][value] = extrargs.cfgMuonCuts
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
            # Timestamp
            if value =='isRun2MC' and extrargs.isRun2MC:
                config[key][value] = extrargs.isRun2MC
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
            # process list not in d-q tasks
            if value == 'processDummy' and extrargs.processDummy:
                config[key][value] = extrargs.processDummy
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
            # tof-pid-beta
            if value == 'tof-expreso' and extrargs.tof_expreso:
                config[key][value] = extrargs.tof_expreso
            # track-selection
            if value == 'isRun3' and extrargs.isRun3:
                config[key][value] = extrargs.isRun3
            # tof-pid-full, tof-pid for run3
            if value == 'processEvTime' and extrargs.processEvTime:
                config[key][value] = extrargs.processEvTime
            if value =='processNoEvTime' and extrargs.processNoEvTime:
                config[key][value] = extrargs.processNoEvTime
###

# Write the updated configuration file into a temporary file
#TODO: Config file json outputunu demodaki gibi transcation management yap.
updatedConfigFileName = "tempConfig.json"
with open(updatedConfigFileName,'w') as outputFile:
  json.dump(config, outputFile)

# Check which dependencies need to be run
depsToRun = {}
for dep in commonDeps:
  depsToRun[dep] = 1
      
commandToRun = taskNameInCommandLine + " --configuration json://" + updatedConfigFileName + " --severity error --shm-segment-size 12000000000 -b"
for dep in depsToRun.keys():
  commandToRun += " | " + dep + " --configuration json://" + updatedConfigFileName + " -b"

print("====================================================================================================================")
print("Command to run:")
print(commandToRun)
print("====================================================================================================================")
os.system(commandToRun)