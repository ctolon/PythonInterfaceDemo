
## Available Configs for IRunTableMaker.py

```ruby
usage: IRunTableMaker.py [-h] [-runData] [-runMC] [--run {2,3}] [--add_mc_conv] [--add_fdd_conv] [--add_track_prop] [--aod AOD] [--onlySelect {true,false}] [--autoDummy {true,false}]
                         [--cfgEventCuts [CFGEVENTCUTS ...]] [--cfgBarrelTrackCuts [CFGBARRELTRACKCUTS ...]] [--cfgMuonCuts [CFGMUONCUTS ...]] [--cfgBarrelLowPt CFGBARRELLOWPT]
                         [--cfgMuonLowPt CFGMUONLOWPT] [--cfgNoQA {true,false}] [--cfgDetailedQA {true,false}] [--cfgMinTpcSignal CFGMINTPCSIGNAL] [--cfgMaxTpcSignal CFGMAXTPCSIGNAL]
                         [--cfgMCsignals [CFGMCSIGNALS ...]] [--process [PROCESS ...]] [--syst {PbPb,pp,pPb,Pbp,XeXe}] [--muonSelection {0,1,2}] [--customDeltaBC CUSTOMDELTABC]
                         [--isVertexZeq {true,false}] [--isWSlice {true,false}] [--enableTimeDependentResponse {true,false}] [--isCovariance {true,false}] [--tof-expreso TOF_EXPRESO]
                         [--FT0 {FT0,NoFT0,OnlyFT0,Run2}] [--isBarrelSelectionTiny {true,false}] [--cfgMuonsCuts [CFGMUONSCUT ...]] [--cfgBarrelSels [CFGBARRELSELS ...]]
                         [--cfgMuonSels [CFGMUONSELS ...]] [--isFilterPPTiny {true,false}] [--est [EST ...]] [--cfgWithQA {true,false}] [--d_bz D_BZ] [--v0cospa V0COSPA] [--dcav0dau DCAV0DAU]
                         [--v0Rmin V0RMIN] [--v0Rmax V0RMAX] [--dcamin DCAMIN] [--dcamax DCAMAX] [--mincrossedrows MINCROSSEDROWS] [--maxchi2tpc MAXCHI2TPC] [--pid [PID ...]] [--cutLister]
                         [--MCSignalsLister] [--debug {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--logFile]
                         Config.json

Arguments to pass

optional arguments:
  -h, --help            show this help message and exit
  --run {2,3}           Run Number Selection (2 or 3) (default: None)

Core configurations that must be configured:
  Config.json           config JSON file name
  -runData              Run over data (default: False)
  -runMC                Run over MC (default: False)

Additional Task Adding Options:
  --add_mc_conv         Add the converter from mcparticle to mcparticle+001 (Adds your workflow o2-analysis-mc-converter task) (default: False)
  --add_fdd_conv        Add the fdd converter (Adds your workflow o2-analysis-fdd-converter task) (default: False)
  --add_track_prop      Add track propagation to the innermost layer (TPC or ITS) (Adds your workflow o2-analysis-track-propagation task) (default: False)

Data processor options: internal-dpl-aod-reader:
  --aod AOD             Add your AOD File with path (default: None)

Automation Parameters:
  --onlySelect {true,false}
                        An Automate parameter for keep options for only selection in process, pid and centrality table (true is highly recomended for automation) (default: true)
  --autoDummy {true,false}
                        Dummy automize parameter (don't configure it, true is highly recomended for automation) (default: true)

Data processor options: table-maker/table-maker-m-c:
  --cfgEventCuts [CFGEVENTCUTS ...]
                        Space separated list of event cuts (default: None)
  --cfgBarrelTrackCuts [CFGBARRELTRACKCUTS ...]
                        Space separated list of barrel track cuts (default: None)
  --cfgMuonCuts [CFGMUONCUTS ...]
                        Space separated list of muon cuts in table-maker (default: None)
  --cfgBarrelLowPt CFGBARRELLOWPT
                        Low pt cut for tracks in the barrel (default: None)
  --cfgMuonLowPt CFGMUONLOWPT
                        Low pt cut for muons (default: None)
  --cfgNoQA {true,false}
                        If true, no QA histograms (default: None)
  --cfgDetailedQA {true,false}
                        If true, include more QA histograms (BeforeCuts classes and more) (default: None)
  --cfgMinTpcSignal CFGMINTPCSIGNAL
                        Minimum TPC signal (default: None)
  --cfgMaxTpcSignal CFGMAXTPCSIGNAL
                        Maximum TPC signal (default: None)
  --cfgMCsignals [CFGMCSIGNALS ...]
                        Space separated list of MC signals (default: None)

Data processor options: table-maker/table-maker-m-c:
  --process [PROCESS ...]
                        Process Selection options for tableMaker/tableMakerMC Data Processing and Skimming (default: None)
  Full                  Build full DQ skimmed data model, w/o centrality
  FullTiny              Build full DQ skimmed data model tiny
  FullWithCov           Build full DQ skimmed data model, w/ track and fwdtrack covariance tables
  FullWithCent          Build full DQ skimmed data model, w/ centrality
  BarrelOnly            Build barrel-only DQ skimmed data model, w/o centrality
  BarrelOnlyWithCov     Build barrel-only DQ skimmed data model, w/ track cov matrix
  BarrelOnlyWithV0Bits  Build full DQ skimmed data model, w/o centrality, w/ V0Bits
  BarrelOnlyWithEventFilter
                        Build full DQ skimmed data model, w/o centrality, w/ event filter
  BarrelOnlyWithCent    Build barrel-only DQ skimmed data model, w/ centrality
  MuonOnly              Build muon-only DQ skimmed data model
  MuonOnlyWithCov       Build muon-only DQ skimmed data model, w/ muon cov matrix
  MuonOnlyWithCent      Build muon-only DQ skimmed data model, w/ centrality
  MuonOnlyWithFilter    Build muon-only DQ skimmed data model, w/ event filter
  OnlyBCs               Analyze the BCs to store sampled lumi

Data processor options: event-selection-task:
  --syst {PbPb,pp,pPb,Pbp,XeXe}
                        Collision System Selection ex. pp (default: None)
  --muonSelection {0,1,2}
                        0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts (default: None)
  --customDeltaBC CUSTOMDELTABC
                        custom BC delta for FIT-collision matching (default: None)

Data processor options: multiplicity-table:
  --isVertexZeq {true,false}
                        if true: do vertex Z eq mult table (default: None)

Data processor options: tof-pid, tof-pid-full:
  --isWSlice {true,false}
                        Process with track slices (default: None)
  --enableTimeDependentResponse {true,false}
                        Flag to use the collision timestamp to fetch the PID Response (default: None)

Data processor options: track-propagation:
  --isCovariance {true,false}
                        track-propagation : If false, Process without covariance, If true Process with covariance (default: None)

Data processor options: tof-pid-beta:
  --tof-expreso TOF_EXPRESO
                        Expected resolution for the computation of the expected beta (default: None)

Data processor options: tof-event-time:
  --FT0 {FT0,NoFT0,OnlyFT0,Run2}
                        FT0: Process with FT0, NoFT0: Process without FT0, OnlyFT0: Process only with FT0, Run2: Process with Run2 data (default: None)

Data processor options: d-q-track barrel-task:
  --isBarrelSelectionTiny {true,false}
                        Run barrel track selection instead of normal(process func. for barrel selection must be true) (default: false)

Data processor options: d-q muons-selection:
  --cfgMuonsCuts [CFGMUONSCUT ...]
                        Space separated list of ADDITIONAL muon track cuts (default: None)

Data processor options: d-q-filter-p-p-task:
  --cfgBarrelSels [CFGBARRELSELS ...]
                        Configure Barrel Selection <track-cut>:[<pair-cut>]:<n>,[<track-cut>:[<pair-cut>]:<n>],... | example jpsiO2MCdebugCuts2::1 (default: None)
  --cfgMuonSels [CFGMUONSELS ...]
                        Configure Muon Selection <muon-cut>:[<pair-cut>]:<n> example muonQualityCuts:pairNoCut:1 (default: None)
  --isFilterPPTiny {true,false}
                        Run filter tiny task instead of normal (processFilterPP must be true) (default: None)

Data processor options: centrality-table:
  --est [EST ...]       Produces centrality percentiles parameters (default: None)
  Run2V0M               Produces centrality percentiles using V0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  Run2SPDtks            Produces Run2 centrality percentiles using SPD tracklets multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  Run2SPDcls            Produces Run2 centrality percentiles using SPD clusters multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  Run2CL0               Produces Run2 centrality percentiles using CL0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  Run2CL1               Produces Run2 centrality percentiles using CL1 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  FV0A                  Produces centrality percentiles using FV0A multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  FT0M                  Produces centrality percentiles using FT0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  FDDM                  Produces centrality percentiles using FDD multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  NTPV                  Produces centrality percentiles using number of tracks contributing to the PV. -1: auto, 0: don't, 1: yes. Default: auto (-1)

Data processor options: d-q-barrel-track-selection-task, d-q-muons-selection, d-q-event-selection-task, d-q-filter-p-p-task:
  --cfgWithQA {true,false}
                        If true, fill QA histograms (default: None)

Data processor options: v0-selector:
  --d_bz D_BZ           bz field (default: None)
  --v0cospa V0COSPA     v0cospa (default: None)
  --dcav0dau DCAV0DAU   DCA V0 Daughters (default: None)
  --v0Rmin V0RMIN       v0Rmin (default: None)
  --v0Rmax V0RMAX       v0Rmax (default: None)
  --dcamin DCAMIN       dcamin (default: None)
  --dcamax DCAMAX       dcamax (default: None)
  --mincrossedrows MINCROSSEDROWS
                        Min crossed rows (default: None)
  --maxchi2tpc MAXCHI2TPC
                        max chi2/NclsTPC (default: None)

Data processor options: tof-pid, tpc-pid-full, tof-pid-full:
  --pid [PID ...]       Produce PID information for the <particle> mass hypothesis (default: None)
  el                    Produce PID information for the Electron mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  mu                    Produce PID information for the Muon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  pi                    Produce PID information for the Pion mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  ka                    Produce PID information for the Kaon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  pr                    Produce PID information for the Proton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  de                    Produce PID information for the Deuterons mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  tr                    Produce PID information for the Triton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  he                    Produce PID information for the Helium3 mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  al                    Produce PID information for the Alpha mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)

Additional Helper Command Options:
  --cutLister           List all of the analysis cuts from CutsLibrary.h (default: False)
  --MCSignalsLister     List all of the MCSignals from MCSignalLibrary.h (default: False)
  --debug {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        execute with debug options (default: INFO)
  --logFile             Enable logger for both file and CLI (default: False)

Choice List for debug Parameters:
  NOTSET                Set Debug Level to NOTSET
  DEBUG                 Set Debug Level to DEBUG
  INFO                  Set Debug Level to INFO
  WARNING               Set Debug Level to WARNING
  ERROR                 Set Debug Level to ERROR
  CRITICAL              Set Debug Level to CRITICAL
```


## Available Configs for IRunTableReader.py

```ruby
usage: IRunTableReader.py [-h] [--add_mc_conv] [--add_fdd_conv] [--add_track_prop] [--aod AOD] [--reader READER] [--writer WRITER] [--autoDummy {true,false}] [--analysis [ANALYSIS ...]]
                          [--process [PROCESS ...]] [--cfgQA {true,false}] [--cfgMixingVars [CFGMIXINGVARS ...]] [--cfgEventCuts [CFGEVENTCUTS ...]] [--cfgMuonCuts [CFGMUONCUTS ...]]
                          [--cfgTrackCuts [CFGTRACKCUTS ...]] [--cfgLeptonCuts [CFGLEPTONCUTS ...]] [--cutLister] [--mixingLister] [--debug {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--logFile]
                          Config.json

Arguments to pass

optional arguments:
  -h, --help            show this help message and exit

Core configurations that must be configured:
  Config.json           config JSON file name

Additional Task Adding Options:
  --add_mc_conv         Add the converter from mcparticle to mcparticle+001 (Adds your workflow o2-analysis-mc-converter task) (default: False)
  --add_fdd_conv        Add the fdd converter (Adds your workflow o2-analysis-fdd-converter task) (default: False)
  --add_track_prop      Add track propagation to the innermost layer (TPC or ITS) (Adds your workflow o2-analysis-track-propagation task) (default: False)

Data processor options: internal-dpl-aod-reader:
  --aod AOD             Add your AOD File with path (default: None)
  --reader READER       Add your AOD Reader JSON with path (default: Configs/readerConfiguration_reducedEvent.json)
  --writer WRITER       Add your AOD Writer JSON with path (default: Configs/writerConfiguration_dileptons.json)

Automation Parameters:
  --autoDummy {true,false}
                        Dummy automize parameter (don't configure it, true is highly recomended for automation) (default: true)

Data processor options: analysis-event-selection, analysis-muon-selection, analysis-track-selection, analysis-event-mixing, analysis-dilepton-hadron:
  --analysis [ANALYSIS ...]
                        Skimmed process selections for Data Analysis (default: None)
  eventSelection        Run event selection on DQ skimmed events
  muonSelection         Run muon selection on DQ skimmed muons
  trackSelection        Run barrel track selection on DQ skimmed tracks
  eventMixing           Run mixing on skimmed tracks based muon and track selections
  eventMixingVn         Run vn mixing on skimmed tracks based muon and track selections
  sameEventPairing      Run same event pairing selection on DQ skimmed data
  dileptonHadron        Run dilepton-hadron pairing, using skimmed data

Data processor options: analysis-same-event-pairing:
  --process [PROCESS ...]
                        Skimmed process selections for analysis-same-event-pairing task (default: None)

Choice List for analysis-same-event-pairing task Process options (when a value added to parameter, processSkimmed value is converted from false to true):
  JpsiToEE              Run electron-electron pairing, with skimmed tracks
  JpsiToMuMu            Run muon-muon pairing, with skimmed muons
  JpsiToMuMuVertexing   Run muon-muon pairing and vertexing, with skimmed muons
  VnJpsiToEE            Run barrel-barrel vn mixing on skimmed tracks
  VnJpsiToMuMu          Run muon-muon vn mixing on skimmed tracks
  ElectronMuon          Run electron-muon pairing, with skimmed tracks/muons
  All                   Run all types of pairing, with skimmed tracks/muons

Data processor options: analysis-event-selection, analysis-muon-selection, analysis-track-selection, analysis-event-mixing:
  --cfgQA {true,false}  If true, fill QA histograms (default: None)

Data processor options: analysis-event-selection:
  --cfgMixingVars [CFGMIXINGVARS ...]
                        Mixing configs separated by a space (default: None)
  --cfgEventCuts [CFGEVENTCUTS ...]
                        Space separated list of event cuts (default: None)

Data processor options: analysis-muon-selection:
  --cfgMuonCuts [CFGMUONCUTS ...]
                        Space separated list of muon cuts (default: None)

Data processor options: analysis-track-selection:
  --cfgTrackCuts [CFGTRACKCUTS ...]
                        Space separated list of barrel track cuts (default: None)

Data processor options: analysis-dilepton-hadron:
  --cfgLeptonCuts [CFGLEPTONCUTS ...]
                        Space separated list of barrel track cuts (default: None)

Additional Helper Command Options:
  --cutLister           List all of the analysis cuts from CutsLibrary.h (default: False)
  --mixingLister        List all of the event mixing selections from MixingLibrary.h (default: False)
  --debug {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        execute with debug options (default: INFO)
  --logFile             Enable logger for both file and CLI (default: False)

Choice List for debug Parameters:
  NOTSET                Set Debug Level to NOTSET
  DEBUG                 Set Debug Level to DEBUG
  INFO                  Set Debug Level to INFO
  WARNING               Set Debug Level to WARNING
  ERROR                 Set Debug Level to ERROR
  CRITICAL              Set Debug Level to CRITICAL
```


## Available Configs for IRunDQEfficiency.py

```ruby
usage: IRunDQEfficiency.py [-h] [--add_mc_conv] [--add_fdd_conv] [--add_track_prop] [--aod AOD] [--reader READER] [--writer WRITER] [--autoDummy {true,false}] [--analysis [ANALYSIS ...]]
                           [--process [PROCESS ...]] [--cfgBarrelMCRecSignals [CFGBARRELMCRECSIGNALS ...]] [--cfgBarrelMCGenSignals [CFGBARRELMCGENSIGNALS ...]] [--cfgFlatTables {true,false}]
                           [--cfgQA {true,false}] [--cfgEventCuts [CFGEVENTCUTS ...]] [--cfgTrackCuts [CFGTRACKCUTS ...]] [--cfgTrackMCSignals [CFGTRACKMCSIGNALS ...]] [--cfgMuonCuts [CFGMUONCUTS ...]]
                           [--cfgMuonMCSignals [CFGMUONMCSIGNALS ...]] [--cfgLeptonCuts [CFGLEPTONCUTS ...]] [--cfgFillCandidateTable {true,false}]
                           [--cfgBarrelDileptonMCRecSignals [CFGBARRELDILEPTONMCRECSIGNALS ...]] [--cfgBarrelDileptonMCGenSignals [CFGBARRELDILEPTONMCRECSIGNALS ...]] [--cutLister] [--MCSignalsLister]
                           [--debug {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--logFile]
                           Config.json

Arguments to pass

optional arguments:
  -h, --help            show this help message and exit

Core configurations that must be configured:
  Config.json           config JSON file name

Additional Task Adding Options:
  --add_mc_conv         Add the converter from mcparticle to mcparticle+001 (Adds your workflow o2-analysis-mc-converter task) (default: False)
  --add_fdd_conv        Add the fdd converter (Adds your workflow o2-analysis-fdd-converter task) (default: False)
  --add_track_prop      Add track propagation to the innermost layer (TPC or ITS) (Adds your workflow o2-analysis-track-propagation task) (default: False)

Data processor options: internal-dpl-aod-reader:
  --aod AOD             Add your AOD File with path (default: None)
  --reader READER       Add your AOD Reader JSON with path (default: Configs/readerConfiguration_reducedEventMC.json)
  --writer WRITER       Add your AOD Writer JSON with path (default: Configs/writerConfiguration_dileptonMC.json)

Automation Parameters:
  --autoDummy {true,false}
                        Dummy automize parameter (don't configure it, true is highly recomended for automation) (default: true)

Data processor options: analysis-event-selection, analysis-muon-selection, analysis-track-selection, analysis-dilepton-track:
  --analysis [ANALYSIS ...]
                        Skimmed process selections for MC Analysis (default: None)
  eventSelection        Run event selection on DQ skimmed events
  muonSelection         Run muon selection on DQ skimmed muons
  trackSelection        Run barrel track selection on DQ skimmed tracks
  sameEventPairing      Run same event pairing selection on DQ skimmed data
  dileptonTrackDimuonMuonSelection
                        Run dimuon-muon pairing, using skimmed data
  dileptonTrackDielectronKaonSelection
                        Run dielectron-kaon pairing, using skimmed data

Data processor options: analysis-same-event-pairing:
  --process [PROCESS ...]
                        Skimmed process selections for analysis-same-event-pairing task (default: None)
  --cfgBarrelMCRecSignals [CFGBARRELMCRECSIGNALS ...]
                        Space separated list of MC signals (reconstructed) (default: None)
  --cfgBarrelMCGenSignals [CFGBARRELMCGENSIGNALS ...]
                        Space separated list of MC signals (generated) (default: None)
  --cfgFlatTables {true,false}
                        Produce a single flat tables with all relevant information of the pairs and single tracks (default: None)

Choice List for analysis-same-event-pairing task Process options:
  JpsiToEE              Run electron-electron pairing, with skimmed tracks
  JpsiToMuMu            Run muon-muon pairing, with skimmed muons
  JpsiToMuMuVertexing   Run muon-muon pairing and vertexing, with skimmed muons

Data processor options: analysis-event-selection, analysis-muon-selection, analysis-track-selection, analysis-event-mixing, analysis-dilepton-hadron:
  --cfgQA {true,false}  If true, fill QA histograms (default: None)

Data processor options: analysis-event-selection:
  --cfgEventCuts [CFGEVENTCUTS ...]
                        Space separated list of event cuts (default: None)

Data processor options: analysis-track-selection:
  --cfgTrackCuts [CFGTRACKCUTS ...]
                        Space separated list of barrel track cuts (default: None)
  --cfgTrackMCSignals [CFGTRACKMCSIGNALS ...]
                        Space separated list of MC signals (default: None)

Data processor options: analysis-muon-selection:
  --cfgMuonCuts [CFGMUONCUTS ...]
                        Space separated list of muon cuts (default: None)
  --cfgMuonMCSignals [CFGMUONMCSIGNALS ...]
                        Space separated list of MC signals (default: None)

Data processor options: analysis-dilepton-track:
  --cfgLeptonCuts [CFGLEPTONCUTS ...]
                        Space separated list of barrel track cuts (default: None)
  --cfgFillCandidateTable {true,false}
                        Produce a single flat tables with all relevant information dilepton-track candidates (default: None)
  --cfgBarrelDileptonMCRecSignals [CFGBARRELDILEPTONMCRECSIGNALS ...]
                        Space separated list of MC signals (reconstructed) (default: None)
  --cfgBarrelDileptonMCGenSignals [CFGBARRELDILEPTONMCRECSIGNALS ...]
                        Space separated list of MC signals (generated) (default: None)

Additional Helper Command Options:
  --cutLister           List all of the analysis cuts from CutsLibrary.h (default: False)
  --MCSignalsLister     List all of the MCSignals from MCSignalLibrary.h (default: False)
  --debug {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        execute with debug options (default: INFO)
  --logFile             Enable logger for both file and CLI (default: False)

Choice List for debug Parameters:
  NOTSET                Set Debug Level to NOTSET
  DEBUG                 Set Debug Level to DEBUG
  INFO                  Set Debug Level to INFO
  WARNING               Set Debug Level to WARNING
  ERROR                 Set Debug Level to ERROR
  CRITICAL              Set Debug Level to CRITICAL
```


## Available Configs for IRunFilterPP.py

```ruby
usage: IFilterPP.py [-h] [--add_mc_conv] [--add_fdd_conv] [--add_track_prop] [--aod AOD] [--autoDummy {true,false}] [--syst {PbPb,pp,pPb,Pbp,XeXe}] [--muonSelection {0,1,2}]
                    [--customDeltaBC CUSTOMDELTABC] [--isVertexZeq {true,false}] [--isWSlice {true,false}] [--enableTimeDependentResponse {true,false}] [--tof-expreso TOF_EXPRESO]
                    [--FT0 {FT0,NoFT0,OnlyFT0,Run2}] [--process [PROCESS ...]] [--cfgBarrelSels [CFGBARRELSELS ...]] [--cfgMuonSels [CFGMUONSELS ...]] [--cfgEventCuts [CFGEVENTCUTS ...]]
                    [--cfgBarrelTrackCuts [CFGBARRELTRACKCUTS ...]] [--cfgMuonsCuts [CFGMUONSCUT ...]] [--cfgWithQA {true,false}] [--pid [PID ...]] [--cutLister]
                    [--debug {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--logFile]
                    Config.json

Arguments to pass

optional arguments:
  -h, --help            show this help message and exit

Core configurations that must be configured:
  Config.json           config JSON file name

Additional Task Adding Options:
  --add_mc_conv         Add the converter from mcparticle to mcparticle+001 (Adds your workflow o2-analysis-mc-converter task) (default: False)
  --add_fdd_conv        Add the fdd converter (Adds your workflow o2-analysis-fdd-converter task) (default: False)
  --add_track_prop      Add track propagation to the innermost layer (TPC or ITS) (Adds your workflow o2-analysis-track-propagation task) (default: False)

Data processor options: internal-dpl-aod-reader:
  --aod AOD             Add your AOD File with path (default: None)

Automation Parameters:
  --autoDummy {true,false}
                        Dummy automize parameter (don't configure it, true is highly recomended for automation) (default: true)

Data processor options: event-selection-task:
  --syst {PbPb,pp,pPb,Pbp,XeXe}
                        Collision System Selection ex. pp (default: None)
  --muonSelection {0,1,2}
                        0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts (default: None)
  --customDeltaBC CUSTOMDELTABC
                        custom BC delta for FIT-collision matching (default: None)

Data processor options: multiplicity-table:
  --isVertexZeq {true,false}
                        if true: do vertex Z eq mult table (default: None)

Data processor options: tof-pid, tof-pid-full:
  --isWSlice {true,false}
                        Process with track slices (default: None)
  --enableTimeDependentResponse {true,false}
                        Flag to use the collision timestamp to fetch the PID Response (default: None)

Data processor options: tof-pid-beta:
  --tof-expreso TOF_EXPRESO
                        Expected resolution for the computation of the expected beta (default: None)

Data processor options: tof-event-time:
  --FT0 {FT0,NoFT0,OnlyFT0,Run2}
                        FT0: Process with FT0, NoFT0: Process without FT0, OnlyFT0: Process only with FT0, Run2: Process with Run2 data (default: None)

Data processor options: d-q-filter-p-p-task, d-q-event-selection-task, d-q-barrel-track-selection, d-q-muons-selection :
  --process [PROCESS ...]
                        DQ Tasks process Selections options (default: None)
  eventSelection        Run DQ event selection
  barrelTrackSelection  Run DQ barrel track selection
  muonSelection         Run DQ muon selection
  barrelTrackSelectionTiny
                        Run DQ barrel track selection tiny
  filterPPSelectionTiny
                        Run filter task tiny

Data processor options: d-q-filter-p-p-task:
  --cfgBarrelSels [CFGBARRELSELS ...]
                        Configure Barrel Selection <track-cut>:[<pair-cut>]:<n>,[<track-cut>:[<pair-cut>]:<n>],... | example jpsiO2MCdebugCuts2::1 (default: None)
  --cfgMuonSels [CFGMUONSELS ...]
                        Configure Muon Selection <muon-cut>:[<pair-cut>]:<n> example muonQualityCuts:pairNoCut:1 (default: None)

Data processor options: d-q-event-selection-task:
  --cfgEventCuts [CFGEVENTCUTS ...]
                        Space separated list of event cuts (default: None)

Data processor options: d-q-barrel-track-selection:
  --cfgBarrelTrackCuts [CFGBARRELTRACKCUTS ...]
                        Space separated list of barrel track cuts (default: None)

Data processor options: d-q-muons-selection:
  --cfgMuonsCuts [CFGMUONSCUT ...]
                        Space separated list of muon cuts in d-q muons selection (default: None)

Data processor options: d-q-barrel-track-selection-task, d-q-muons-selection, d-q-event-selection-task, d-q-filter-p-p-task:
  --cfgWithQA {true,false}
                        If true, fill QA histograms (default: None)

Data processor options: tof-pid, tpc-pid-full, tof-pid-full:
  --pid [PID ...]       Produce PID information for the <particle> mass hypothesis (default: None)
  el                    Produce PID information for the Electron mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  mu                    Produce PID information for the Muon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  pi                    Produce PID information for the Pion mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  ka                    Produce PID information for the Kaon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  pr                    Produce PID information for the Proton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  de                    Produce PID information for the Deuterons mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  tr                    Produce PID information for the Triton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  he                    Produce PID information for the Helium3 mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  al                    Produce PID information for the Alpha mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)

Additional Helper Command Options:
  --cutLister           List all of the analysis cuts from CutsLibrary.h (default: False)
  --debug {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        execute with debug options (default: INFO)
  --logFile             Enable logger for both file and CLI (default: False)

Choice List for debug Parameters:
  NOTSET                Set Debug Level to NOTSET
  DEBUG                 Set Debug Level to DEBUG
  INFO                  Set Debug Level to INFO
  WARNING               Set Debug Level to WARNING
  ERROR                 Set Debug Level to ERROR
  CRITICAL              Set Debug Level to CRITICAL
```


## Available Configs for IRunDQFlow.py

```ruby
usage: IRunDQFlow.py [-h] [--add_mc_conv] [--add_fdd_conv] [--add_track_prop] [--aod AOD] [--autoDummy {true,false}] [--syst {PbPb,pp,pPb,Pbp,XeXe}] [--muonSelection {0,1,2}]
                     [--customDeltaBC CUSTOMDELTABC] [--isVertexZeq {true,false}] [--isWSlice {true,false}] [--enableTimeDependentResponse {true,false}] [--tof-expreso TOF_EXPRESO]
                     [--FT0 {FT0,NoFT0,OnlyFT0,Run2}] [--cfgTrackCuts [CFGTRACKCUTS ...]] [--cfgMuonCuts [CFGMUONCUTS ...]] [--cfgEventCuts [CFGEVENTCUT ...]] [--cfgWithQA {true,false}]
                     [--cfgCutPtMin CFGCUTPTMIN] [--cfgCutPtMax CFGCUTPTMAX] [--cfgCutEta CFGCUTETA] [--cfgEtaLimit CFGETALIMIT] [--cfgNPow CFGNPOW] [--cfgEfficiency CFGEFFICIENCY]
                     [--cfgAcceptance CFGACCEPTANCE] [--ccdb-url] [--ccdbPath] [--est [EST ...]] [--pid [PID ...]] [--cutLister] [--debug {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--logFile]
                     Config.json

Arguments to pass

optional arguments:
  -h, --help            show this help message and exit

Core configurations that must be configured:
  Config.json           config JSON file name

Additional Task Adding Options:
  --add_mc_conv         Add the converter from mcparticle to mcparticle+001 (Adds your workflow o2-analysis-mc-converter task) (default: False)
  --add_fdd_conv        Add the fdd converter (Adds your workflow o2-analysis-fdd-converter task) (default: False)
  --add_track_prop      Add track propagation to the innermost layer (TPC or ITS) (Adds your workflow o2-analysis-track-propagation task) (default: False)

Data processor options: internal-dpl-aod-reader:
  --aod AOD             Add your AOD File with path (default: None)

Automation Parameters:
  --autoDummy {true,false}
                        Dummy automize parameter (don't configure it, true is highly recomended for automation) (default: true)

Data processor options: event-selection-task:
  --syst {PbPb,pp,pPb,Pbp,XeXe}
                        Collision System Selection ex. pp (default: None)
  --muonSelection {0,1,2}
                        0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts (default: None)
  --customDeltaBC CUSTOMDELTABC
                        custom BC delta for FIT-collision matching (default: None)

Data processor options: multiplicity-table:
  --isVertexZeq {true,false}
                        if true: do vertex Z eq mult table (default: None)

Data processor options: tof-pid, tof-pid-full:
  --isWSlice {true,false}
                        Process with track slices (default: None)
  --enableTimeDependentResponse {true,false}
                        Flag to use the collision timestamp to fetch the PID Response (default: None)

Data processor options: tof-pid-beta:
  --tof-expreso TOF_EXPRESO
                        Expected resolution for the computation of the expected beta (default: None)

Data processor options: tof-event-time:
  --FT0 {FT0,NoFT0,OnlyFT0,Run2}
                        FT0: Process with FT0, NoFT0: Process without FT0, OnlyFT0: Process only with FT0, Run2: Process with Run2 data (default: None)

Data processor options: analysis-qvector:
  --cfgTrackCuts [CFGTRACKCUTS ...]
                        Space separated list of barrel track cuts (default: None)
  --cfgMuonCuts [CFGMUONCUTS ...]
                        Space separated list of muon cuts in d-q muons selection (default: None)
  --cfgEventCuts [CFGEVENTCUT ...]
                        Space separated list of event cuts (default: None)
  --cfgWithQA {true,false}
                        If true, fill QA histograms (default: None)
  --cfgCutPtMin CFGCUTPTMIN
                        Minimal pT for tracks (default: None)
  --cfgCutPtMax CFGCUTPTMAX
                        Maximal pT for tracks (default: None)
  --cfgCutEta CFGCUTETA
                        Eta range for tracks (default: None)
  --cfgEtaLimit CFGETALIMIT
                        Eta gap separation, only if using subEvents (default: None)
  --cfgNPow CFGNPOW     Power of weights for Q vector (default: None)
  --cfgEfficiency CFGEFFICIENCY
                        CCDB path to efficiency object (default: None)
  --cfgAcceptance CFGACCEPTANCE
                        CCDB path to acceptance object (default: None)
  --ccdb-url            url of the ccdb repository (default: None)
  --ccdbPath            base path to the ccdb object (default: None)

Data processor options: centrality-table:
  --est [EST ...]       Produces centrality percentiles parameters (default: None)

Choice List centrality-table Parameters (when a value added to parameter, value is converted from -1 to 1):
  Run2V0M               Produces centrality percentiles using V0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  Run2SPDtks            Produces Run2 centrality percentiles using SPD tracklets multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  Run2SPDcls            Produces Run2 centrality percentiles using SPD clusters multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  Run2CL0               Produces Run2 centrality percentiles using CL0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  Run2CL1               Produces Run2 centrality percentiles using CL1 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  FV0A                  Produces centrality percentiles using FV0A multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  FT0M                  Produces centrality percentiles using FT0 multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  FDDM                  Produces centrality percentiles using FDD multiplicity. -1: auto, 0: don't, 1: yes. Default: auto (-1)
  NTPV                  Produces centrality percentiles using number of tracks contributing to the PV. -1: auto, 0: don't, 1: yes. Default: auto (-1)

Data processor options: tof-pid, tpc-pid-full, tof-pid-full:
  --pid [PID ...]       Produce PID information for the <particle> mass hypothesis (default: None)
  el                    Produce PID information for the Electron mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  mu                    Produce PID information for the Muon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  pi                    Produce PID information for the Pion mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  ka                    Produce PID information for the Kaon mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  pr                    Produce PID information for the Proton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  de                    Produce PID information for the Deuterons mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  tr                    Produce PID information for the Triton mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  he                    Produce PID information for the Helium3 mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)
  al                    Produce PID information for the Alpha mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1)

Additional Helper Command Options:
  --cutLister           List all of the analysis cuts from CutsLibrary.h (default: False)
  --debug {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        execute with debug options (default: INFO)
  --logFile             Enable logger for both file and CLI (default: False)

Choice List for debug Parameters:
  NOTSET                Set Debug Level to NOTSET
  DEBUG                 Set Debug Level to DEBUG
  INFO                  Set Debug Level to INFO
  WARNING               Set Debug Level to WARNING
  ERROR                 Set Debug Level to ERROR
```
