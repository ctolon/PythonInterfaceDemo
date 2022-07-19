import sys
import json
import os

# isRun2
# isMC
#cfg cuts tablemaker
#aod file
#event selection
"""
"aod-file"

"isRun2MC":
"processRun2"
"processRun3"

"syst"
"muonSelection"
"customDeltaBC"
"isMC"
"processRun2"
"processRun3"

"isRun3": "false"

"cfgEventCuts"
"cfgBarrelTrackCuts"
"cfgMuonCuts": "muonQualityCuts,muonTightQualityCutsForTests",
"cfgBarrelLowPt": "1.0",
"cfgMuonLowPt": "1.0",
"cfgMinTpcSignal": "30",
"cfgMaxTpcSignal": "300",
"cfgMCsignals": "eFromJpsi,muFromJpsi,Jpsi,phiMeson",
"cfgIsRun2": "true",
"cfgNoQA": "false",
"cfgDetailedQA": "true",




"""
run_configs = []

#MCRun2 TableMaker
internal_dpl_aod_reader_configs = ["aod-file"]
TimestampTask_configs = ["isRun2MC"]
bmt_configs = ["processRun2", "processRun3"]

event_selection_task_configs = ["syst","muonSelection","isMC","processRun2","processRun3"]
track_selection_configs = ["isRun3"]



test2 = {}

json_file = sys.argv[1]
key_1 = sys.argv[2]
key_2 = sys.argv[3]

value = sys.argv[4]

#print(json_file,key_1, key_2)

with open(json_file) as f:
    test = json.load(f)
    test[key_1][key_2] = value
    
dosya = open('data.json','w')
dosya.write(json.dumps(test))

print(test.get(key_1).get(key_2))

