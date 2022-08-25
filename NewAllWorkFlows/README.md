# NEW INTERFACE IN ALLWORKFLOWS INSTRUCTIONS

This folder contains new interface based on nightly-20220823. You can follow the instructions and you can find tutorials end of the file. see main readme file in PythonInterfaceDeme for general information (For prerequisites, Installation guide for argcomplete and Some Informations good to know)

# Instructions for IRunTableMaker.py

Add extrac tables and converters with:
1. **--add_mc_conv**: conversion from o2mcparticle to o2mcparticle_001
2. **--add_fdd_conv**: conversion o2fdd from o2fdd_001
   * If you get error like this, you should added it in your workflow 
   * `[ERROR] Exception caught: Couldn't get TTree "DF_2571958947001/O2fdd_001" from "YOURAOD.root". Please check https://aliceo2group.github.io/analysis-framework/docs/troubleshooting/treenotfound.html for more information.` 
3. **--add_track_prop**: conversion from o2track to o2track_iu ([link](https://aliceo2group.github.io/analysis-framework/docs/helperTasks/trackPropagation.html))
   * If you get error like this, you should added it in your workflow 
   * `[ERROR] Exception caught: Couldn't get TTree "DF_2660520692001/O2track" from "Datas/AO2D.root". Please check https:/aliceo2group.github.io/analysis-framework/docs/troubleshooting/treenotfoundhtml for more information.` 


* Minimum Required Parameter List:
  * `python3`
  * `IRunTableMaker.py`
  * JSON Config File
    * Example usage: Configs/configTableMakerDataRun3.json 
  *  `-run<MC|Data>` 
     *  Usage (only select one value): `-runMC` or `-runData`
  *  `--process <Value>` 
     *  Usage examples (can take several value) : `--process MuonsOnly` or `--process BarrelOnly MuonOnly BarrelOnlyWithEventFilter`

Examples(in AllWorkFlows):
- Run TableMaker on Data run3 With Minimum Commands for Barrel Only (with automation)
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerDataRun3.json -runData --process BarrelOnly --onlySelect true
  ```
- Run TableMaker on MC run3 with Minimum Commands for Barrel Only (with automation)
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --process BarrelOnly --onlySelect true
  ```
- Run TableMaker on Data run2 With Minimum Commands for Barrel Only (with automation)
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerDataRun2.json -runData --process BarrelOnly --onlySelect true
  ```
- Run TableMaker on MC run2 with Minimum Commands for Barrel Only (with automation)
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerMCRun2.json -runMC --process BarrelOnly --onlySelect true
  ```

In case of multiple configs example
  ```ruby
python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --process MuonOnlyWithCov OnlyBCs --cfgMCsignals muFromJpsi Jpsi muFromPsi2S Psi2S --onlySelect true --aod Datas/AO2D.root --cfgMuonCuts muonQualityCuts muonTightQualityCutsForTests --syst pp --onlySelect true --add_track_prop
  ```

# Available configs in IRunTableMaker Interface

* For `IRunTableMaker.py` Selections

Arg | Opt | Task | nargs |
--- | --- | --- | --- |
`-h` | No Param | all | 0 |
`--aod` | all | `internal-dpl-aod-reader` | 1 |
`--aod-memory-rate-limit` | all | `internal-dpl-aod-reader` | 1 |
`--onlySelect` | `true`</br> `false`</br>  | Special Option | 1 |
`--autoDummy` | `true`</br> `false`</br>  | Special Option | 1 |
`--process` | `Full` </br> `FullTiny`</br>  `FullWithCov`</br>  `FullWithCent`</br>  `BarrelOnlyWithV0Bits`</br>  `BarrelOnlyWithEventFilter`</br> `BarrelOnlyWithQvector` </br>  `BarrelOnlyWithCent`</br>  `BarrelOnlyWithCov`</br>  `BarrelOnly`</br>  `MuonOnlyWithCent`</br>  `MuonOnlyWithCov`</br>  `MuonOnly`</br>  `MuonOnlyWithFilter`</br> `MuonOnlyWithQvector` </br>  `OnlyBCs`</br>  | `table-maker` | * |
`--run` | `2`</br> `3`</br> | Special Option | 1 |
`-runData` | No Param | `event-selection-task`</br> Special Option | 0 |
`-runMC` |  No Param | `event-selection-task`</br> Special Option | 0 |
`--add_mc_conv` | No Param  | `o2-analysis-mc-converter`</br> Special Option | 0 |
`--add_fdd_conv` | No Param | `o2-analysis-fdd-converter`</br> Special Option | 0 |
`--add_track_prop` | No Param | `o2-analysis-track-propagation`</br> Special Option | 0 |
`--syst` | `pp`</br> `PbPb`</br> `pPb`</br> `Pbp`</br> `XeXe`</br> | `event-selection-task` | 1 |
`--muonSelection` | `0`</br> `1`</br> `2` | `event-selection-task` | 1 |
`--CustomDeltaBC` | all | `event-selection-task` | 1 |
`--isVertexZeq` | `true`</br> `false`</br>  | `multiplicity-table` | 1 |
`--isCovariance` | `true`</br> `false`</br> | `track-propagation` | 1 |
`--isWSlice` | `true`</br> `false`</br> | `tof-pid-full tof-pid` | 1 |
`--enableTimeDependentResponse` | `true`</br> `false`</br> | `tof-pid-full tof-pid` | 1 |
`--FT0` | `FT0`</br> `NOFT0`</br>`OnlyFT0`</br> `Run2` | `tof-event-time` | 1 |
`--tof-expreso` | all | `tof-pid-beta` | 1 |
`--isBarrelSelectionTiny` | `true`</br> `false`</br> | `d-q-barrel-track-selection-task` | 1 |
`--est` | `Run2V0M`</br> `Run2SPDtks`</br> `Run2SPDcls`</br> `Run2CL0`</br> `Run2CL1`</br> `FV0A`</br> `FT0M`</br> `FDDM`</br> `NTPV`</br>| `centrality-table` | | *
`--cfgWithQA` | `true`</br> `false`</br> | `d-q-barrel-track-selection-task`</br> `d-q-event-selection-task`</br> `d-q-event-selection-task`</br> `d-q-filter-p-p-task`</br>`analysis-qvector`  | 1 |
`--d_bz` | all | `v0-selector` | 1 |
`--v0cospa` | all | `v0-selector` | 1 |
`--dcav0dau` | all | `v0-selector` | 1 |
`--v0Rmin` | all | `v0-selector` | 1 |
`--v0Rmax` | all | `v0-selector` | 1 |
`--dcamin` | all | `v0-selector` | 1 |
`--dcamax` | all | `v0-selector` |  1|
`--mincrossedrows` | all | `v0-selector` | 1 |
`--maxchi2tpc` | all | `v0-selector` | 1 |
`--cfgCutPtMin` | all  | `analysis-qvector`</br>  | 1 |
`--cfgCutPtMax ` | all  | `analysis-qvector`</br> | 1 |
`--cfgCutEta ` | all  | `analysis-qvector` | 1 |
`--cfgEtaLimit` | all  | `analysis-qvector`</br>  | 1 |
`--cfgNPow` | all  | `analysis-qvector`</br> | 1 |
`--cfgEfficiency` | all  | `analysis-qvector` | 1 |
`--cfgAcceptance` | all  | `analysis-qvector`</br>  | 1 |
`--pid` | `el`</br> `mu`</br> `pi`</br> `ka`</br> `pr`</br> `de`</br> `tr`</br> `he`</br> `al`</br> | `tof-pid tpc-pid` | * |
`--isFilterPPTiny` | `true`</br>  `false`</br> | `d-q-filter-p-p-task` | 1 |
`--cfgBarrelSels` | `namespacedCuts` | `d-q-filter-p-p-task` | * |
`--cfgMuonSels` | `namespacedCuts` | `d-q-filter-p-p-task` | * |
`--cfgEventCuts` | `allCuts` | `table-maker` | * |
`--cfgBarrelTrackCuts` | `allCuts` | `table-maker` | * |
`--cfgMuonCuts` | `allCuts` | `table-maker` | * |
`--cfgMuonsCuts` | `allCuts` | `d-q-muons-selection` | * |
`--cfgBarrelLowPt` | all | `table-maker` | 1 |
`--cfgMuonLowPt` | all | `table-maker` | 1 |
`--cfgNoQA` | `true`</br> `false`</br> | `table-maker` | 1 |
`--cfgDetailedQA` | `true`</br> `false`</br> | `table-maker` | 1 |
`--cfgMinTpcSignal` | all | `table-maker` | 1 |
`--cfgMaxTpcSignal` | all | `table-maker` | 1 |
`--cfgMCsignals` | `allSignals` | `table-maker` | * |
`--cutLister` | No Param | `allCuts` | 0 |
`--MCSignalsLister` | No Param | `allSignals` | 0 |
`--debug` | `NOTSET`</br> `DEBUG`</br>`INFO`</br>`WARNING` </br> `ERROR` </br>`CRITICAL` </br>  | all  | 1 |
`--logFile` | No Param | special option  | 0 |

* Details parameters for `IRunTableMaker.py`

Arg | Ref Type| Desc | Default | Real Type
--- | --- | --- | --- | --- |
`-h` | No Param | list all helper messages for configurable command |  | *
`--aod` | String | Add your aod file with path  |  | str |
`--aod-memory-rate-limit` | String | Rate limit AOD processing based on memory |  |  str
`--onlySelect` | Boolean | An Automate parameter for keep options for only selection in process, pid and centrality table (true is highly recomended for automation)"| `false` | str.lower |
`--autoDummy` | Boolean | Dummy automize parameter (if your selection true, it automatically activate dummy process and viceversa) | `true` | str.lower |
`--process` | String | process selection for skimmed data model in tablemaker |  | str |
`--run` | Integer | Data run option for ALICE 2/3 |  | str
`-runData` | no Param |  Data Selection instead of MC |   | str
`-runMC` |  No Param | MC Selection instead of data |  | -
`--add_mc_conv` | No Param  | Conversion from o2mcparticle to o2mcparticle_001< |  | -
`--add_fdd_conv` | No Param | Conversion o2fdd from o2fdd_001 |  | -
`--add_track_prop` | No Param | Conversion from o2track to o2track_iu  |  | -
`--syst` | String | Collision system selection |  | str
`--muonSelection` | Integer | 0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts |  | str
`--CustomDeltaBC` | all |custom BC delta for FIT-collision matching |  | str
`--isVertexZeq` | Boolean  | if true: do vertex Z eq mult table |  | str.lower
`--isCovariance` | Boolean | If false, Process without covariance, If true Process with covariance related to `track-propagation` |  | str.lower
`--isWSlice` | Boolean | Process with track slices|  | str.lower
`--enableTimeDependentResponse` | Boolean | Flag to use the collision timestamp to fetch the PID Response |  | str.lower
`--FT0` | Boolean | FT0: Process with FT0, NoFT0: Process without FT0, OnlyFT0: Process only with FT0, Run2: Process with Run2 data |  | str.lower
`--tof-expreso` | Float | Expected resolution for the computation of the expected beta |  | str
`--isBarrelSelectionTiny` | Boolean | Run barrel track selection instead of normal(process func. for barrel selection must be true) |  | str.lower
`--est` | String | Produces centrality percentiles parameters | | str
`--cfgWithQA` | Boolean | If true, fill QA histograms |  | str.lower
`--d_bz` | Float | bz field |  | str
`--v0cospa` | Float | v0cospa |  | str
`--dcav0dau` | Float | DCA V0 Daughters |  | str
`--v0Rmin` | Float | V0min |  | str
`--v0Rmax` | Float | V0max|  | str
`--dcamin` | Float | dcamin  |  | str
`--dcamax` | Float | dcamax |  | str
`--mincrossedrows` | Float | Min crossed rows  |  | str
`--maxchi2tpc` | Float | max chi2/NclsTPC  |  | str
`--cfgCutPtMin` | Float | Minimal pT for tracks |  | str
`--cfgCutPtMax ` | Float | Maximal pT for tracks  |  | str
`--cfgCutEta ` | Float | Eta range for tracksselection  |  | str
`--cfgEtaLimit` | Float | Eta gap separation, only if using subEvents |  | str
`--cfgNPow` | Integer | Power of weights for Q vector  |  | str
`--cfgEfficiency` | String | CCDB path to efficiency object  |  | str
`--cfgAcceptance` | String | CCDB path to acceptance object  |  | str
`--pid` | String | Produce PID information for the particle mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1) |  | str.lower
`--isFilterPPTiny` | Boolean | Run filter tiny task instead of normal (processFilterPP must be true) |  | str.lower
`--cfgBarrelSels` | String | Configure Barrel Selection track-cut:pair-cut:n,track-cut:pair-cut:n,... example jpsiO2MCdebugCuts2::1|  | str
`--cfgMuonSels` | String | Configure Muon Selection muon-cut:[pair-cut]:n example muonQualityCuts:pairNoCut:1|  | str
`--cfgEventCuts` | String | Space separated list of event cuts |  | str
`--cfgBarrelTrackCuts` | String | Space separated list of barrel track cuts |  | str
`--cfgMuonCuts` | String | Space separated list of muon cuts in tablemaker and analysis-qvector  |  | str
`--cfgMuonsCuts` | String | Space separated list of ADDITIONAL muon track cuts  |  | str
`--cfgBarrelLowPt` | Float | Specify the lowest pt cut for electrons; used in a Partition expression to improve CPU efficiency (GeV) |  | str
`--cfgMuonLowPt` | Float | Specify the lowest pt cut for muons; used in a Partition expression to improve CPU efficiency  (GeV) |  | str
`--cfgNoQA` | Boolean | If true, no QA histograms |  | str.lower
`--cfgDetailedQA` | Boolean | If true, include more QA histograms (BeforeCuts classes and more) |  | str.lower
`--cfgMinTpcSignal` | Integer| TPC Min Signal Selection |  | str
`--cfgMaxTpcSignal` | Integer | TPC Max Signal Selection |  | str
`--cfgMCsignals` | String | Space separated list of MC signals |  | str
`--cutLister` | No Param | Lists All of the valid Analysis Cuts from CutsLibrary.h from O2Physics-DQ|  |  | -
`--MCSignalsLister` | No Param | Lists All of the valid MCSignals from MCSignalLibrary.h from O2Physics-DQ |  | -
`--debug` | String | execute with debug options  | - | str.upper |
`--logFile` | No Param | Enable logger for both file and CLI  | - | - |



# Instructions for IRunTableReader.py

* Minimum Required Parameter List:
  * `python3`
  * `IRunTableReader.py`
  * JSON Config File
    * Example For Most common usage: Configs/configAnalysisData.json  

Examples(in AllWorkFlows):
- Run TableReader on Data run3 With Minimum Commands
  ```ruby
  python3 IRunTableReader.py Configs/configAnalysisData.json
  ```

In case of multiple configs example
  ```ruby
  python3 IRunTableReader.py Configs/configAnalysisData.json --analysis eventSelection trackSelection eventMixing sameEventPairing --process JpsiToEE --cfgTrackCuts jpsiO2MCdebugCuts --aod reducedAod.root --debug debug --logFile
  ```


# Available configs in IRunTableReader Interface

Arg | Opt | Task | nargs |
--- | --- | --- | --- |
`-h` | No Param | all | 0 |
`--aod` | all | `internal-dpl-aod-reader` | 1 |
`--autoDummy` | `true`</br> `false`</br>  | Special Option | 1 |
`--reader` | all | Special Option | 1 |
`--writer` | all | Special Option | 1 |
`--analysis` | `eventSelection`</br>`trackSelection`</br>`muonSelection`</br>`eventMixing`</br>`eventMixingVn`</br> `sameEventPairing`</br> `dileptonHadronSelection`  | `analysis-event-selection`</br>`analysis-track-selection`</br>`analysis-muon-selection`</br>`analysis-event-mixing`</br>`analysis-same-event-pairing`</br>`analysis-dilepton-hadron`  | * |
`--process` | `JpsiToEE`</br>`JpsiToMuMu`</br>`JpsiToMuMuVertexing`</br>`VnJpsiToEE`</br>`VnJpsiToMuMu`</br>`ElectronMuon`</br> `All`  | `analysis-same-event-pairing` | * |
`--syst` | `pp`</br> `PbPb`</br> `pPb`</br> `Pbp`</br> `XeXe`</br> | `event-selection-task` | 1 |
`--cfgQA` |`true` </br> `false`  | `analysis-event-selection`</br> `analysis-track-selection`</br> `analysis-muon-selection`  | 1 |
`--cfgMixingVars` | `allMixingVars`  | `analysis-event-selection`</br> | * |
`--cfgEventCuts` | `allCuts`  | `analysis-event-selection`</br>  | * |
`--cfgTrackCuts` | `allCuts` | `analysis-track-selection`</br> | * |
`--cfgMuonCuts` | `allCuts` | `analysis-muon-selection` | * |
`--cfgLeptonCuts` | `true`</br> `false`</br> | `analysis-dilepton-hadron` | * |
`--cutLister` | No Param | `allCuts` | 0 |
`--mixingLister` | No Param | `allMixing` | 0 |
`--debug` | `NOTSET`</br> `DEBUG`</br>`INFO`</br>`WARNING` </br> `ERROR` </br>`CRITICAL` </br>  | all  | 1 |
`--logFile` | No Param | special option  | 0 |

* Details parameters for `IRunTableReader.py`

Arg | Ref Type| Desc | Default | Real Type
--- | --- | --- | --- | --- |
`-h` | No Param | list all helper messages for configurable command |  | *
`--aod` | String | Add your AOD File with path | - | str
`--autoDummy` | Boolean | Dummy automize parameter (if process skimmed false, it automatically activate dummy process and viceversa) | `true` | str.lower
`--reader` | String | Add your AOD Reader JSON with path | `Configs/readerConfiguration_reducedEvent.json` | str
`--writer` | String | Add your AOD Writer JSON with path | `Configs/writerConfiguration_dileptons.json` | str
`--analysis` | String | Skimmed process selections for analysis | - | str
`--process` | String | Skimmed process Selections for Same Event Pairing  | - | str |
`--isMixingEvent` | String | Event Mixing Activate or Disable Option | - | str.lower |
`--cfgQA` | Boolean | If true, fill QA histograms | - | str
`--cfgMixingVars` | String | Mixing configs separated by a space | - | str
`--cfgEventCuts` |  String | Space separated list of event cuts | - | str
`--cfgTrackCuts` | String | Space separated list of barrel track cuts | - | str
`--cfgMuonCuts` | String | Space separated list of muon cuts | - | str
`--cfgLeptonCuts` | String | Space separated list of barrel track cuts | - | str
`--cutLister` | No Param | Lists All of the valid Analysis Cuts from CutsLibrary.h from O2Physics-DQ| 0 |  | -
`--mixingLister` | No Param | Lists All of the valid event mixing selections from MixingLibrary.h from O2Physics-DQ |  | -
`--debug` | String | execute with debug options  | - | str.upper |
`--logFile` | No Param | Enable logger for both file and CLI  | - | - |
# Instructions for IRunDQEfficiency.py
* Minimum Required Parameter List:
  * `python3`
  * `IRunDQEfficiency.py`
  * JSON Config File
    * Example For Most common usage: Configs/configAnalysisMC.json  

Examples(in AllWorkFlows):
- Run DQEfficiency on Data run3 With Minimum Commands
  ```ruby
  python3 IRunDQEfficiency.py Configs/configAnalysisMC.json
  ```

In case of multiple configs example
  ```ruby
python3 IRunDQEfficiency.py Configs/configAnalysisMC.json --analysis muonSelection eventSelection sameEventPairing --aod reducedAod.root --cfgMuonCuts muonQualityCuts muonTightQualityCutsForTests --cfgMuonMCSignals muFromJpsi muFromPsi2S --cfgBarrelMCGenSignals Jpsi Psi2S --cfgBarrelMCRecSignals mumuFromJpsi mumuFromPsi2S dimuon --process JpsiToMuMu --cfgQA true


  ```

# Available configs in IRunDQEfficiency Interface

* For `IRunDQEfficiency.py` Selections

Arg | Opt | Task | nargs |
--- | --- | --- | --- |
`-h` | No Param | all | 0 |
`--aod` | all | `internal-dpl-aod-reader` | 1 |
`--autoDummy` | `true`</br> `false`</br>  | Special Option | 1 |
`--reader` | all | Special Option | 1 |
`--writer` | all | Special Option | 1 |
`--analysis` | `eventSelection`</br>`trackSelection`</br>`muonSelection`</br>`sameEventPairing`</br>`dileptonTrackDimuonMuonSelection`</br> `dileptonTrackDielectronKaonSelection`</br> | `analysis-event-selection`</br>`analysis-track-selection`</br>`analysis-muon-selection`</br>`analysis-same-event-pairing`</br>`analysis-dilepton-track` | * |
`--process` | `JpsiToEE`</br>`JpsiToMuMu`</br>`JpsiToMuMuVertexing`</br>| `analysis-same-event-pairing` | * |
`--cfgQA` |`true` </br> `false`  | `analysis-event-selection`</br> `analysis-track-selection`</br> `analysis-muon-selection` | 1 |
`--cfgEventCuts` | `allCuts` | `analysis-event-selection`</br>  | * |
`--cfgTrackCuts` | `allCuts` | `analysis-track-selection`</br> | * |
`--cfgTrackMCSignals` | `allMCSignals` | `analysis-track-selection` | * |
`--cfgMuonCuts` | `allCuts` | `analysis-muon-selection` | * |
`--cfgMuonMCSignals` | `allMCSignals` | `analysis-muon-selection` | * |
`--cfgBarrelMCRecSignals` | `allMCSignals` | `analysis-same-event-pairing` | * |
`--cfgBarrelMCGenSignals` | `allMCSignals` | `analysis-same-event-pairing` | * |
`--cfgFlatTables` | `true` </br> `false` | `analysis-same-event-pairing` | 1 | 
`--cfgLeptonCuts` | `allCuts` | `analysis-dilepton-track` | * | 
`--cfgFillCandidateTable` | `true` </br> `false` | `analysis-dilepton-track` | 1 | 
`--cfgBarrelDileptonMCRecSignals` | `allMCSignals` | `analysis-dilepton-track` | * |
`--cfgBarrelDileptonMCGenSignals` | `allMCSignals` | `analysis-dilepton-track` | * |
`--cutLister` | No Param | `allCuts` | 0 |
`--MCSignalsLister` | No Param | `allSignals` |  0 |
`--debug` | `NOTSET`</br> `DEBUG`</br>`INFO`</br>`WARNING` </br> `ERROR` </br>`CRITICAL` </br>  | all  | 1 |
`--logFile` | No Param | special option  | 0 |

* Details parameters for `IRunDQEfficiency.py`

Arg | Ref Type| Desc | Default | Real Type
--- | --- | --- | --- | --- |
`-h` | No Param | list all helper messages for configurable command |  | *
`--aod` | String | Add your AOD File with path | - | str
`--autoDummy` | Boolean | Dummy automize parameter (if process skimmed false, it automatically activate dummy process and viceversa) | `true` | str.lower
`--reader` | String | Add your AOD Reader JSON with path | `Configs/readerConfiguration_reducedEventMC.json` | str
`--writer` | String | Add your AOD Writer JSON with path | `Configs/writerConfiguration_dileptonMC.json` | str
`--analysis` | String | Skimmed process selections for analysis | - | str
`--process` | String | Skimmed process selections for Same Event Pairing | - | str
`--cfgQA` | Boolean | If true, fill QA histograms | - | str
`--cfgEventCuts` |  String | Space separated list of event cuts | - | str
`--cfgTrackCuts` | String | Space separated list of barrel track cuts | - | str
`--cfgTrackMCSignals` | String | Space separated list of MC signals | - | str
`--cfgMuonCuts` | String | Space separated list of muon cuts | - | str
`--cfgMuonMCSignals` | String | Space separated list of MC signals | - | str
`--cfgBarrelMCRecSignals` | String | Space separated list of MC signals (reconstructed) | - | str
`--cfgBarrelMCGenSignals` | String | Space separated list of MC signals (generated) | - | str
`--cfgBarrelDileptonMCRecSignals` | String | Space separated list of MC signals (reconstructed) cuts | - | str
`--cfgBarrelDileptonMCGenSignals` | String | Space separated list of MC signals (generated)cuts | - | str
`--cutLister` | No Param | Lists All of the valid Analysis Cuts from CutsLibrary.h from O2Physics-DQ|  |  | -
`--MCSignalsLister` | No Param | Lists All of the valid MCSignals from MCSignalLibrary.h from O2Physics-DQ |  | -
`--debug` | String | execute with debug options  | - | str.upper |
`--logFile` | No Param | Enable logger for both file and CLI  | - | - |

# Instructions for IFilterPP.py

Add extrac tables and converters with:
1. **--add_mc_conv**: conversion from o2mcparticle to o2mcparticle_001
2. **--add_fdd_conv**: conversion o2fdd from o2fdd_001
   * If you get error like this, you should added it in your workflow 
   * `[ERROR] Exception caught: Couldn't get TTree "DF_2571958947001/O2fdd_001" from "YOURAOD.root". Please check https://aliceo2group.github.io/analysis-framework/docs/troubleshooting/treenotfound.html for more information.` 
3. **--add_track_prop**: conversion from o2track to o2track_iu ([link](https://aliceo2group.github.io/analysis-framework/docs/helperTasks/trackPropagation.html))
   * If you get error like this, you should added it in your workflow 
   * `[ERROR] Exception caught: Couldn't get TTree "DF_2660520692001/O2track" from "Datas/AO2D.root". Please check https:/aliceo2group.github.io/analysis-framework/docs/troubleshooting/treenotfoundhtml for more information.`

* Minimum Required Parameter List:
  * `python3`
  * `IFilterPP.py`
  * JSON Config File
    * Example For usage: Configs/configFilterPPRun3.json 

Examples(in AllWorkFlows):
- Run filterPP on Data run3 With Minimum Commands
  ```ruby
  python3 IFilterPP.py Configs/configFilterPPRun3.json
  ```

- Run filterPP on Data run2 With Minimum Commands
  ```ruby
  python3 IFilterPP.py Configs/configFilterPPDataRun2.json
  ```

In case of multiple configs example
  ```ruby
python3 IFilterPP.py Configs/configFilterPPRun3.json --aod AO2D.root --syst pp --process barrelTrackSelection eventSelection --cfgBarrelSels jpsiO2MCdebugCuts2::1 --cfgEventCuts eventStandardNoINT7 --cfgBarrelTrackCuts jpsiO2MCdebugCuts2 jpsiO2MCdebugCuts2 --cfgWithQA true
  ```

# Available configs in IFilterPP Interface

* For `IFilterPP.py` Selections

Arg | Opt | Task | nargs |
--- | --- | --- | --- |
`-h` | No Param | all | 0 |
`--aod` | all | `internal-dpl-aod-reader` | 1 |
`--autoDummy` | `true`</br> `false`</br>  | Special Option | 1 |
`--process` | `barrelTrackSelection`</br>`eventSelection`</br>`muonSelection`</br>`barrelTrackSelectionTiny`</br>`filterPPSelectionTiny`| `d-q-barrel-track-selection`</br>`d-q-event-selection-task`</br>`d-q-muons-selection`| * |
`--add_mc_conv` | No Param  | `o2-analysis-mc-converter`</br> Special Option | 0 |
`--add_fdd_conv` | No Param | `o2-analysis-fdd-converter`</br> Special Option | 0 |
`--add_track_prop` | No Param | `o2-analysis-track-propagation`</br> Special Option | 0 |
`--syst` | `pp`</br> `PbPb`</br> `pPb`</br> `Pbp`</br> `XeXe`</br> | `event-selection-task` | 1 |
`--muonSelection` | `0`</br> `1`</br> `2` | `event-selection-task` | 1 |
`--CustomDeltaBC` | all | `event-selection-task` | 1 |
`--isVertexZeq` | `true`</br> `false`</br>  | `multiplicity-table` | 1 |
`--pid` | `el`</br> `mu`</br> `pi`</br> `ka`</br> `pr`</br> `de`</br> `tr`</br> `he`</br> `al`</br> | `tof-pid tpc-pid` | * |
`--isWSlice` | `true`</br> `false`</br> | `tof-pid-full tof-pid` | 1 |
`--enableTimeDependentResponse` | `true`</br> `false`</br> | `tof-pid-full tof-pid` | 1 |
`--tof-expreso` | all | `tof-pid-beta` | 1 |
`--FT0` | `FT0`</br> `NOFT0`</br>`OnlyFT0`</br> `Run2` | `tof-event-time` | 1 |
`--cfgWithQA` |`true` </br> `false`  | dq task selection</br> | 1 |
`--cfgEventCuts` | `allCuts` | `d-q-event-selection-task`</br>  | * |
`--cfgBarrelTrackCuts` | `allCuts` | `d-q-barrel-track-selection`</br> | * |
`--cfgBarrelSels` | `namespacedCuts` | `d-q-filter-p-p-task` | * |
`--cfgMuonSels` | `namespacedCuts` | `d-q-filter-p-p-task` | * |
`--cfgMuonsCuts` | `allCuts` | `d-q-muons-selection` | * |
`--cutLister` | No Param | `allCuts` | 0 |
`--debug` | `NOTSET`</br> `DEBUG`</br>`INFO`</br>`WARNING` </br> `ERROR` </br>`CRITICAL` </br>  | all  | 1 |
`--logFile` | No Param | special option  | 0 |


* Details parameters for `IFilterPP.py`

Arg | Ref Type| Desc | Default | Real Type
--- | --- | --- | --- | --- |
`-h` | No Param | list all helper messages for configurable command |  | *
`--aod` | String | Add your aod file with path  |  | str |
`--autoDummy` | Boolean | Dummy automize parameter (if process skimmed false, it automatically activate dummy process and viceversa) | `true` | str.lower
`--process` | `barrelTrackSelection`</br>`eventSelection`</br>`muonSelection`</br>`barrelTrackSelectionTiny`</br>`filterPPSelectionTiny`| dq task selection| * |
`--add_mc_conv` | No Param  | Conversion from o2mcparticle to o2mcparticle_001< |  | -
`--add_fdd_conv` | No Param | Conversion o2fdd from o2fdd_001 |  | -
`--add_track_prop` | No Param | Conversion from o2track to o2track_iu  |  | -
`--syst` | String | Collision system selection |  | str
`--muonSelection` | Integer | 0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts |  | str
`--CustomDeltaBC` | all |custom BC delta for FIT-collision matching |  | str
`--isVertexZeq` | Boolean  | if true: do vertex Z eq mult table |  | str.lower
`--pid` | String | Produce PID information for the particle mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1) |  | str.lower
`--isWSlice` | Boolean | Process with track slices|  | str.lower
`--enableTimeDependentResponse` | Boolean | Flag to use the collision timestamp to fetch the PID Response |  | str.lower
`--tof-expreso` | Float | Expected resolution for the computation of the expected beta |  | str
`--FT0` | Boolean | FT0: Process with FT0, NoFT0: Process without FT0, OnlyFT0: Process only with FT0, Run2: Process with Run2 data |  | str.lower
`--cfgWithQA` | Boolean | If true, fill QA histograms |  | str.lower
`--cfgEventCuts` | String | Space separated list of event cuts |  | str
`--cfgBarrelTrackCuts` | String | Space separated list of barrel track cuts |  | str
`--cfgBarrelSels` | String | Configure Barrel Selection track-cut:pair-cut:n,track-cut:pair-cut:n,... example jpsiO2MCdebugCuts2::1|  | str
`--cfgMuonSels` | String | Configure Muon Selection muon-cut:[pair-cut]:n example muonQualityCuts:pairNoCut:1|  | str
`--cfgMuonsCuts` | String | Space separated list of ADDITIONAL muon track cuts  |  | str
`--cutLister` | No Param | Lists All of the valid Analysis Cuts from CutsLibrary.h from O2Physics-DQ|  |  | -
`--debug` | String | execute with debug options  | - | str.upper |
`--logFile` | No Param | Enable logger for both file and CLI  | - | - |


# Instructions for IRunDQFlow.py

* Minimum Required Parameter List:
  * `python3`
  * `IRunDQFlow.py`
  * JSON Config File
    * Example For usage: Configs/configFlowDataRun3.json

Examples(in AllWorkFlows):
- Run filterPP on Data run3 With Minimum Commands
  ```ruby
  python3 IRunDQFlow.py Configs/configFlowDataRun3.json
  ```

- Run filterPP on Data run2 With Minimum Commands
  ```ruby
  python3 IRunDQFlow.py Configs/configFlowDataRun2.json
  ```

In case of multiple configs example
  ```ruby
python3 IRunDQFlow.py Configs/configFilterPPRun3.json --aod AO2D.root --syst pp --cfgTrackCuts jpsiPID1 --cfgMuonCuts muonQualityCuts --cfgWithQA true --cfgCutPtMin 1 --cfgCutPtMax 15 
  ```

# Available configs in IRunDQFlow Interface

Add extrac tables and converters with:
1. **--add_mc_conv**: conversion from o2mcparticle to o2mcparticle_001
2. **--add_fdd_conv**: conversion o2fdd from o2fdd_001
   * If you get error like this, you should added it in your workflow 
   * `[ERROR] Exception caught: Couldn't get TTree "DF_2571958947001/O2fdd_001" from "YOURAOD.root". Please check https://aliceo2group.github.io/analysis-framework/docs/troubleshooting/treenotfound.html for more information.` 
3. **--add_track_prop**: conversion from o2track to o2track_iu ([link](https://aliceo2group.github.io/analysis-framework/docs/helperTasks/trackPropagation.html))
   * If you get error like this, you should added it in your workflow 
   * `[ERROR] Exception caught: Couldn't get TTree "DF_2660520692001/O2track" from "Datas/AO2D.root". Please check https:/aliceo2group.github.io/analysis-framework/docs/troubleshooting/treenotfoundhtml for more information.`

* For `IRunDQFlow.py` Selections

Arg | Opt | Task | nargs |
--- | --- | --- | --- |
`-h` | No Param | all | 0 |
`--aod` | all | `internal-dpl-aod-reader` | 1 |
`--add_mc_conv` | No Param  | `o2-analysis-mc-converter`</br> Special Option | 0 |
`--add_fdd_conv` | No Param | `o2-analysis-fdd-converter`</br> Special Option | 0 |
`--add_track_prop` | No Param | `o2-analysis-track-propagation`</br> Special Option | 0 |
`--syst` | `pp`</br> `PbPb`</br> `pPb`</br> `Pbp`</br> `XeXe`</br> | `event-selection-task` | 1 |
`--muonSelection` | `0`</br> `1`</br> `2` | `event-selection-task` | 1 |
`--CustomDeltaBC` | all | `event-selection-task` | 1 |
`--pid` | `el`</br> `mu`</br> `pi`</br> `ka`</br> `pr`</br> `de`</br> `tr`</br> `he`</br> `al`</br> | `tof-pid tpc-pid` | * |
`--est` | `Run2V0M`</br> `Run2SPDtks`</br> `Run2SPDcls`</br> `Run2CL0`</br> `Run2CL1`</br> `FV0A`</br> `FT0M`</br> `FDDM`</br> `NTPV`</br>| `centrality-table` | | *
`--isVertexZeq` | `true`</br> `false`</br>  | `multiplicity-table` | 1 |
`--isWSlice` | `true`</br> `false`</br> | `tof-pid-full tof-pid` | 1 |
`--enableTimeDependentResponse` | `true`</br> `false`</br> | `tof-pid-full tof-pid` | 1 |
`--tof-expreso` | all | `tof-pid-beta` | 1 |
`--FT0` | `FT0`</br> `NOFT0`</br>`OnlyFT0`</br> `Run2` | `tof-event-time` | 1 |
`--cfgWithQA` |`true` </br> `false`  | `analysis-qvector`</br> | 1 |
`--cfgEventCuts` | `allCuts` | `analysis-qvector`</br>  | * |
`--cfgTrackCuts` | `allCuts` | `analysis-qvector`</br> | * |
`--cfgMuonCuts` | `allCuts` | `analysis-qvector` | * |
`--cfgCutPtMin` | all  | `analysis-qvector`</br>  | 1 |
`--cfgCutPtMax ` | all  | `analysis-qvector`</br> | 1 |
`--cfgCutEta ` | all  | `analysis-qvector` | 1 |
`--cfgEtaLimit` | all  | `analysis-qvector`</br>  | 1 |
`--cfgNPow` | all  | `analysis-qvector`</br> | 1 |
`--cfgEfficiency` | all  | `analysis-qvector` | 1 |
`--cfgAcceptance` | all  | `analysis-qvector`</br>  | 1 |
`--cutLister` | No Param | all  |  |
`--debug` | `NOTSET`</br> `DEBUG`</br>`INFO`</br>`WARNING` </br> `ERROR` </br>`CRITICAL` </br>  | all  | 1 |
`--logFile` | No Param | special option  | 0 |



* Details parameters for `IRunDQFlow.py`

Arg | Ref Type| Desc | Default | Real Type
--- | --- | --- | --- | --- |
`-h` | No Param | list all helper messages for configurable command |  | *
`--aod` | String | Add your aod file with path  |  | str |
`--add_mc_conv` | No Param  | Conversion from o2mcparticle to o2mcparticle_001< |  | -
`--add_fdd_conv` | No Param | Conversion o2fdd from o2fdd_001 |  | -
`--add_track_prop` | No Param | Conversion from o2track to o2track_iu  |  | -
`--syst` | String | Collision system selection |  | str
`--muonSelection` | Integer | 0 - barrel, 1 - muon selection with pileup cuts, 2 - muon selection without pileup cuts |  | str
`--CustomDeltaBC` | all |custom BC delta for FIT-collision matching |  | str
`--isVertexZeq` | Boolean  | if true: do vertex Z eq mult table |  | str.lower
`--isWSlice` | Boolean | Process with track slices|  | str.lower
`--enableTimeDependentResponse` | Boolean | Flag to use the collision timestamp to fetch the PID Response |  | str.lower
`--est` | String | Produces centrality percentiles parameters | | str
`--pid` | String | Produce PID information for the particle mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1) |  | str.lower
`--tof-expreso` | Float | Expected resolution for the computation of the expected beta |  | str
`--FT0` | Boolean | FT0: Process with FT0, NoFT0: Process without FT0, OnlyFT0: Process only with FT0, Run2: Process with Run2 data |  | str.lower
`--cfgWithQA` | Boolean | If true, fill QA histograms |  | str.lower
`--cfgEventCuts` | String | Space separated list of event cuts |  | str
`--cfgTrackCuts` | String | Space separated list of barrel track cuts |  | str
`--cfgMuonCuts` | String | Space separated list of muon cuts |  | str
`--cfgCutPtMin` | Float | Minimal pT for tracks |  | str
`--cfgCutPtMax ` | Float | Maximal pT for tracks  |  | str
`--cfgCutEta ` | Float | Eta range for tracksselection  |  | str
`--cfgEtaLimit` | Float | Eta gap separation, only if using subEvents |  | str
`--cfgNPow` | Integer | Power of weights for Q vector  |  | str
`--cfgEfficiency` | String | CCDB path to efficiency object  |  | str
`--cfgAcceptance` | String | CCDB path to acceptance object  |  | str
`--cutLister` | No Param | all  |  | -
`--debug` | String | execute with debug options  | - | str.upper |
`--logFile` | No Param | Enable logger for both file and CLI  | - | - |


# Tutorial Part

TODO Add details for configure parameters

Firstly, clone repository in your workspace

`git clone https://github.com/ctolon/PythonInterfaceDemo.git`

Before you start, you need to do the installations in the readme in the PythonInterfaceDemo folder (argcomplete package)).

P.S. Don't forget to install the O2 enviroment before running the scripts

Ex. `alienv enter O2Physics/latest,QualityControl/latest`

Assuming you have installed the argcomplete package, don't forget to source the bash script again in your O2 enviroment.

`source argcomplete.sh`

if you don't have time to read the documentation follow these steps:

For Linux Based System:

* `alienv enter O2Physics/latest,QualityControl/latest` (Load Your alienv, if you want you can install lxplus version without using QC)
* `pip install argcomplete` and `pip3 install argcomplete`
* `source argcomplete.sh`

For MacOS Based System:

* `brew install bash`
* `alienv enter O2Physics/latest,QualityControl/latest` (Load Your alienv, if you want you can install lxplus version without using QC)
* `pip install argcomplete` and `pip3 install argcomplete`
* `exec bash` (temporary bash shell)
* `source argcomplete.sh`

if not works:

* `sudo chsh -s /bin/bash <username>`
* `source argcomplete.sh`

if you used the command `sudo chsh -s /bin/bash <username>` after you are done with the scripts (It converts your system shell zsh to bash):

* `sudo chsh -s /bin/zsh <username>` (It converts your system shell bash to zsh)


if you used the command `exec bash` you don't need to do anything.

## MC Part

### Run tableMakerMC With IRunTableMaker.py on LHC21i3d2

You can find and download dataset from : [Click Here](https://cernbox.cern.ch/index.php/s/frDjtMYaxaY75lH) download: AO2D.root, Password: DQ

https://alimonitor.cern.ch/catalogue/index.jsp?path=%2Falice%2Fsim%2F2021%2FLHC21i3d2%2F302004#/alice/sim/2021/LHC21i3d2/302004 you can also Download file from there.

Command To Run:

```ruby
python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --process MuonOnlyWithCov OnlyBCs --cfgMCsignals muFromJpsi Jpsi --aod Datas/AO2D.root --cfgMuonCuts muonQualityCuts muonTightQualityCutsForTests --syst pp --add_track_prop --debug debug --logFile
```

 ###  Run dqEfficiency With IRunDQEfficiency.py on LHC21i3d2 DQ skimmed MC

You need to produce reducedAod.root file with tableMakerMC.

Command To Run:

```ruby
python3 IRunDQEfficiency.py Configs/configAnalysisMC.json --analysis muonSelection eventSelection sameEventPairing --process JpsiToMuMu --aod reducedAod.root --cfgMuonCuts muonQualityCuts muonTightQualityCutsForTests --cfgMuonMCSignals muFromJpsi muFromPsi2S --cfgBarrelMCGenSignals Jpsi --cfgBarrelMCRecSignals mumuFromJpsi dimuon --debug debug --logFile
```

## Data Part

### Run tableMaker With IRunTableMaker.py on LHC21i3b

You can find and download dataset from : [Click Here](https://cernbox.cern.ch/index.php/s/frDjtMYaxaY75lH) download: AO2D_LHC21i3b_prompt.root, Password: DQ

You can also find this data from DQ hands-on-session-II.

Command To Run:

```ruby
python3 IRunTableMaker.py Configs/configTableMakerDataRun3.json -runData --run 3 --process OnlyBCs BarrelOnly --aod Datas/AO2D_LHC21i3b_prompt.root --cfgBarrelTrackCuts jpsiO2MCdebugCuts --syst PbPb --debug debug --logFile --cfgWithQA true
```

### Run tableReader With IRunTableReader.py on LHC21i3b

You need to produce reducedAod.root file with tableMaker.

Command To Run:

```ruby
python3 IRunTableReader.py Configs/configAnalysisData.json --analysis eventSelection trackSelection eventMixing sameEventPairing --process JpsiToEE --cfgTrackCuts jpsiO2MCdebugCuts --aod reducedAod.root --debug debug --logFile
```
### Run filterPP With IFilterPP.py on LHC21i3b (Event trigger Only works on pp data, but you can run on PbPb, If you work on PbPb only trigger histograms will be empty, don't worry and work on pp dataset)

You can find and download dataset from : [Click Here](https://cernbox.cern.ch/index.php/s/frDjtMYaxaY75lH) download: AO2D_LHC21i3b_prompt.root, Password: DQ

You can also find this data from DQ hands-on-session-II.

Command To Run:

```ruby
python3 IFilterPP.py Configs/configFilterPPRun3.json --process barrelTrackSelection eventSelection muonSelection --cfgBarrelTrackCuts jpsiO2MCdebugCuts --cfgBarrelSels jpsiO2MCdebugCuts::3 --cfgMuonsCuts muonQualityCuts --cfgMuonSels muonQualityCuts::3 --syst PbPb --aod Datas/AO2D_LHC21i3b_prompt.root --debug debug --logFile
```

## Generic Flow Part (Only for PbPb Data)

### Run tableMaker With IRunTableMaker.py on LHC15o for Generic Flow Analysis

You can find and download dataset from : [Click Here](https://cernbox.cern.ch/index.php/s/6KLIdQdAlNXj5n1) download: AO2D.root

https://alimonitor.cern.ch/prod/jobs.jsp?t=20117&outputdir=PWGZZ/Run3_Conversion/242_20211215-1006_child_2$ you can also Download file from there.

Command To Run:

```ruby
python3 IRunTableMaker.py Configs/configTableMakerDataRun2.json -runData --process OnlyBCs FullWithCent BarrelOnlyWithQvector --aod Datas/AO2D.root --syst PbPb --debug debug --cfgWithQA true --logFile --est Run2V0M --add_fdd_conv
```
### Run tableReader With IRunTableReader.py on LHC15o for Generic Flow Analysis

You need to produce reducedAod.root file with tableMaker (For Generic Flow Analysis).

Command To Run:

```ruby
python3 IRunTableReader.py Configs/configAnalysisData.json --analysis eventSelection trackSelection eventMixingVn sameEventPairing --process VnJpsiToEE --cfgTrackCuts jpsiO2MCdebugCuts --aod reducedAod.root --debug debug --logFile --reader aodReaderTempConfig.json
```

P.S. Note that we use the `--reader` parameter here when configuring the tablereader. The reason for this is that the reducedEventQvector table is not added in the reader json configuration files prepared to read the data beforehand. With the new update, IRunTableMaker.py has the potential to generate json config file containing all tables as Input Director and this json file is given to the `--reader` parameter for this command.