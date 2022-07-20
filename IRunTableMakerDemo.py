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

#Open JSON File
json_dict = json.load(open('dataMC.json'))

json_dict_new = json_dict


def get_key(json_dict_new):
    json_dict = json.load(open('dataMC.json'))
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
                if value =='aod' and extrargs.aod:
                   json_dict[key][value] = extrargs.aod                
                # tablemaker cfg
                if value == 'cfgEventCuts' and extrargs.cfgEventCuts:
                    extrargs.cfgEventCuts = ",".join(extrargs.cfgEventCuts)
                    json_dict[key][value] = extrargs.cfgEventCuts
                if value == 'cfgBarrelTrackCuts' and extrargs.cfgBarrelTrackCuts:
                    extrargs.cfgBarrelTrackCuts = ",".join(extrargs.cfgBarrelTrackCuts)
                    json_dict[key][value] = extrargs.cfgBarrelTrackCuts
                if value =='cfgMuonCuts' and extrargs.cfgMuonCuts:
                   extrargs.cfgMuonCuts = ",".join(extrargs.cfgMuonCuts)
                   json_dict[key][value] = extrargs.cfgMuonCuts
                if value == 'cfgBarrelLowPt' and extrargs.cfgBarrelLowPt:
                    json_dict[key][value] = extrargs.cfgBarrelLowPt
                if value == 'cfgMuonLowPt' and extrargs.cfgMuonLowPt:
                    json_dict[key][value] = extrargs.cfgMuonLowPt
                if value =='cfgNoQA' and extrargs.cfgNoQA:
                   json_dict[key][value] = extrargs.cfgNoQA
                if value == 'cfgDetailedQA' and extrargs.cfgDetailedQA:
                    json_dict[key][value] = extrargs.cfgDetailedQA
                if value == 'cfgIsRun2' and extrargs.cfgIsRun2:
                    json_dict[key][value] = extrargs.cfgIsRun2
                if value =='cfgMinTpcSignal' and extrargs.cfgMinTpcSignal:
                   json_dict[key][value] = extrargs.cfgMinTpcSignal
                if value == 'cfgMaxTpcSignal' and extrargs.cfgMaxTpcSignal:
                    json_dict[key][value] = extrargs.cfgMaxTpcSignal
                if value == 'cfgMCsignals' and extrargs.cfgMCsignals:                   
                    extrargs.cfgMCsignals = ",".join(extrargs.cfgMCsignals)
                    json_dict[key][value] = extrargs.cfgMCsignals
                # process
                if value =='processFull' and extrargs.processFull:
                   json_dict[key][value] = extrargs.processFull
                if value == 'processFullTiny' and extrargs.processFullTiny:
                    json_dict[key][value] = extrargs.processFullTiny
                if value == 'processFullWithCov' and extrargs.processFullWithCov:
                    json_dict[key][value] = extrargs.processFullWithCov
                if value =='processFullWithCent' and extrargs.processFullWithCent:
                   json_dict[key][value] = extrargs.processFullWithCent
                if value == 'processBarrelOnlyWithV0Bits' and extrargs.processBarrelOnlyWithV0Bits:
                    json_dict[key][value] = extrargs.processBarrelOnlyWithV0Bits
                if value == 'processBarrelOnlyEventFilter' and extrargs.processBarrelOnlyEventFilter:
                    json_dict[key][value] = extrargs.processBarrelOnlyEventFilter
                if value =='processBarrelOnlyWithCent' and extrargs.processBarrelOnlyWithCent:
                   json_dict[key][value] = extrargs.processBarrelOnlyWithCent
                if value == 'processBarrelOnlyWithCov' and extrargs.processBarrelOnlyWithCov:
                    json_dict[key][value] = extrargs.processBarrelOnlyWithCov
                if value == 'processBarrelOnly' and extrargs.processBarrelOnly:
                    json_dict[key][value] = extrargs.processBarrelOnly
                if value =='processMuonOnlyWithCent' and extrargs.processMuonOnlyWithCent:
                   json_dict[key][value] = extrargs.processMuonOnlyWithCent
                if value == 'processMuonOnlyWithCov' and extrargs.processMuonOnlyWithCov:
                    json_dict[key][value] = extrargs.processMuonOnlyWithCov
                if value == 'processMuonOnly' and extrargs.processMuonOnly:
                    json_dict[key][value] = extrargs.processMuonOnly
                if value =='processMuonOnlyWithFilter' and extrargs.processMuonOnlyWithFilter:
                   json_dict[key][value] = extrargs.processMuonOnlyWithFilter
                if value == 'processOnlyBCs' and extrargs.processOnlyBCs:
                    json_dict[key][value] = extrargs.processOnlyBCs
                # event-selection-task ,bc-selection-task, multiplicity-table, track-extension
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
                # track-propagation
                if value =='processStandard' and extrargs.processStandard:
                   json_dict[key][value] = extrargs.processStandard
                if value == 'processCovariance' and extrargs.processCovariance:
                    json_dict[key][value] = extrargs.processCovariance
                # tof-pid-full, tof-pid for run3
                if value == 'processEvTime' and extrargs.processEvTime:
                    json_dict[key][value] = extrargs.processEvTime
                if value =='processNoEvTime' and extrargs.processNoEvTime:
                   json_dict[key][value] = extrargs.processNoEvTime
                # tof-pid-beta
                if value == 'tof-expreso' and extrargs.tof_expreso:
                    json_dict[key][value] = extrargs.tof_expreso
                # need refactoring part
                if value == 'processSelection' and extrargs.processSelection:
                    json_dict[key][value] = extrargs.processSelection
                if value =='processSelectionTiny' and extrargs.processSelectionTiny:
                   json_dict[key][value] = extrargs.processSelectionTiny
                if value == 'processDummy' and extrargs.processDummy:
                    json_dict[key][value] = extrargs.processDummy
                # d-q-event-selection-task
                if value == 'processEventSelection' and extrargs.processEventSelection:
                    json_dict[key][value] = extrargs.processEventSelection
                #d-q-filter-p-p-task
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
                # centrality-table
                if value =='estV0M' and extrargs.estV0M:
                   json_dict[key][value] = extrargs.estV0M
                if value == 'estRun2SPDtks' and extrargs.estRun2SPDtks:
                    json_dict[key][value] = extrargs.estRun2SPDtks
                if value == 'estRun2SPDcls' and extrargs.estRun2SPDcls:
                    json_dict[key][value] = extrargs.estRun2SPDcls
                if value =='estRun2CL0' and extrargs.estRun2CL0:
                   json_dict[key][value] = extrargs.estRun2CL0
                if value == 'estRun2CL1' and extrargs.estRun2CL1:
                    json_dict[key][value] = extrargs.estRun2CL1
                # timestamp-task
                if value =='isRun2MC' and extrargs.isRun2MC:
                   json_dict[key][value] = extrargs.isRun2MC
                # track-selection
                if value == 'isRun3' and extrargs.isRun3:
                    json_dict[key][value] = extrargs.isRun3
                # all d-q tasks and selections
                if value == 'cfgWithQA' and extrargs.cfgWithQA:
                    json_dict[key][value] = extrargs.cfgWithQA
                if value =='estRun2CL0' and extrargs.estRun2CL0:
                   json_dict[key][value] = extrargs.estRun2CL0
                if value == 'estRun2CL1' and extrargs.estRun2CL1:
                    json_dict[key][value] = extrargs.estRun2CL1
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
                
            
    dosya = open('ConfiguredTableMakerData.json','w')
    dosya.write(json.dumps(json_dict, indent= 2))
    
get_key(json_dict_new)         
configured_commands = vars(extrargs) # for get extrargs

#TODO: Fix The Style

# Listing Added Commands
print("Args provided configurations List")
print("========================================")
for key,value in configured_commands.items():
    if(value != None):
        print("--"+key,":", value)


