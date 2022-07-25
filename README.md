# Interfaced O2/DQ Workflows
Python Automated CLI and Task Manager Development and implematation Repository for Contains O2/DQ workflow json configuration files and python scripts to run them (TableMaker, TableReader, DQEfficiency, FilterPP)

## Contact
Ionut Christian Arsene (Owner of [`O2DQWorkflows`](https://github.com/iarsene/O2DQworkflows))

Cevat Batuhan Tolon


## Main Scripts

* Script used to run both the skimming tasks (tableMaker.cxx and tableMakerMC.cxx)
[`IRunTableMaker.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/IRunTableMaker.py).
* Analyze DQ skimmed data tables. This workflow runs a few tasks: event selection, barrel track selection, muon track selection etc.
[`IRunTableReader.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/IRunTableMaker.py).
* Which contains the tasks DQEventSelection for event selection, DQBarrelTrackSelection for barrel track selection and single track MC matching, and the DQQuarkoniumPairing for reconstructed track pairing, MC matching of the pairs and counting of generated MC signals.  
[`IRunDQEfficiency.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/IRunDQEfficiency..py).
* Produces a decision table for pp collisions. The decisions require that at least a selected pair (or just two tracks) exists for a given event. Currently up to 64 simultaneous decisions can be made, to facilitate studies for optimizing cuts. 
[`IRunFilterPP.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/IRunFilterPP.py).

## JSON Databases

MC signals, analysis cuts and histograms, which are configuration variables for analysis are kept in JSON files. This is for transaction management and autocompletion suggestion in Python CLI.

* Database Contains configuration variables for MCSignals, Analysis Cuts and Histograms based on O2Physics
[`Database`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/AllWorkFlows/Database)

* JSON Database List in Table

Main File | Based on O2Physics | Description
--- | --- | ---
[`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | [`CutsLibrary.h`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/CutsLibrary.h) | Analysis Cuts in DQ
[`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | [`MCSignalLibrary.h`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/MCSignalLibrary.h) | MC Signals in DQ
`HistogramDatabase.json` | [`HistogramManager.h`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/HistogramManager.h) | Histograms in DQ

## Config Files

* Contains workflow configuration files
[`Configs`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/AllWorkFlows/Configs)


* JSON workflow configuration files List in Table

Main File | Related Task on O2Physics | Description
--- | --- | ---
[`configTableMakerDataRun2.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configTableMakerDataRun2.json) | [`TableMaker.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/TableProducer/tableMaker.cxx) | run over Run-2 converted data
[`configTableMakerDataRun3.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configTableMakerDataRun3.json) | [`TableMaker.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/TableProducer/tableMaker.cxx) | run over Run-3 data
[`configTableMakerMCRun2.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configTableMakerMCRun2.json) | [`TableMakerMC.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/TableProducer/tableMakerMC.cxx) | run over Run-2 converted MC
[`configTableMakerMCRun3.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configTableMakerMCRun3.json) | [`TableMakerMC.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/TableProducer/tableMakerMC.cxx) | run over Run-3 MC
[`configAnalysisData.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configAnalysisData.json) | [`TableReader.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Tasks/tableReader.cxx) | run with tableReader.cxx
[`configAnalysisMC.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configAnalysisMC.json) | [`dqEfficiency.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Tasks/dqEfficiency.cxx) | run with dqEfficiency.cxx
[`configFilterPPRun3.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configFilterPPRun3.json) | [`filterPP.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Tasks/filterPP.cxx) | run with filterPP.cxx
[`configFilterPPDataRun2.`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configFilterPPDataRun2.json) | [`filterPP.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Tasks/filterPP.cxx) | run with filterPP.cxx

* JSON Reader Configuations for the DQ skimmed tables

Main File | Data Model | Description
--- | --- | ---
[`readerConfiguration_reducedEvent.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configTableMakerDataRun2.json) | DQ Skimmed Data Model | for data
[`readerConfiguration_reducedEventMC.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configTableMakerDataRun3.json) | DQ Skimmed Data Model | for MC

* JSON Writer Configuations for the DQ skimmed tables

Main File | Data Model | Description
--- | --- | ---
[`writerConfiguration_dileptons.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/writerConfiguration_dileptons.json) | DQ Skimmed Data Model | for data
[`writerConfiguration_dileptonMC.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/writerConfiguration_dileptonMC.json) | DQ Skimmed Data Model | for MC

## Test Python Scripts

xxxDemo.py python scripts only overrides JSON level 2 values. They are creating for QA and user acceptane tests before Implementation to O2DQWorkflows. With these prepared scripts, it enables to control whether the configuration values in JSON are manipulated correctly without running O2. It does not need O2 or analysis to run. It just override values in JSON files. They are contains only the Python CLI part.

* Contains test python scripts for only Interface
[`TestInterface`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/TestInterface)

* Test Script for Interfaced IRunTableMaker.py
[`IRunTableMakerDemo.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/TestInterface/IRunTableMakerDemo.py).
* Test Script for Interfaced IRunTableReader.py 
[`IRunTableReaderDemo.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/TestInterface/IRunTableReaderDemo.py).
* Test Script for Interfaced IRunDQEfficiency.py  
[`IRunDQEfficiencyDemo.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/TestInterface/IRunDQEfficiencyDemo.py).
* Test script for Interfaced IRunFilterPP.py
[`IRunFilterPPDemo.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/TestInterface/IFilterPPDemo.py).
* Config and database files are also added in this folder.

## Repository Organization and Development Strategy

While developing, python CLIs are prepared by creating python scripts with enough functions to override configuration values in JSON only (independent of O2). Then, O2DQWorkflow files are prepared that do not contain python CLI and can run the analysis with O2, then they are integrated into the previously prepared Python CLI O2DQWorkflows.

TODO: Add schema

* Contains test python scripts for only Interface.After the tests are done here, new developments should be implemented in level 2 folders where single tasks are located.
[`TestInterface`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/TestInterface)

* For O2DQWorkflow, a folder has been created for the 2nd stage tests containing python scripts to run inside O2 for each task. If the tests in the TestInteface folder pass, new developments are transferred here, where analysis tests are performed in O2.
[`TableMaker`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/TableMaker)
[`TableReader`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/TableReader)
[`DQEfficiency`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/DQEfficiency)
[`FilterPP`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/FilterPP)

* AllWorkFlows folder contains stable python workflow scripts with integrated Python CLI, their workflow configuration files and database files. Improvements should be moved here after done tests. 
[`AllWorkFlows`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/AllWorkFlows)

* Old Versions should be versioned and can found in [`OldVersions`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/OldVersions/v1)

## Features

TO BE ADDED

## Some Things You Should Be Careful For Using and Development

* In JSON files, for example, when assigning a variable for the processFull argument, true or false must be
entered, if True or False like this style, it will throw an error because there is no capitalization check.
* There are also filters for some arguments. No value should be entered outside of these filters (look at the
choices).
* If the argument can take more than one value, when adding a new property choices is a list and the values
must be converted to comma-separated strings

## TODO List
* `Open` We need more meaningful explanations for argument explanations (helping comments).
* `Open` The values that JSON values can take for transaction management should be classified and filtered with
choices and data types.
* `Finished` Also some JSON values are bound together (eg. if cfgRun2 is false, isRun3 variable should be true
automatically) so some error handling and automation should be done for transaction management.
* `Open` Some configurations for MC may not be available for data configurations (eg. cfgMCsignals or vice versa, also
valid for Run2 Run3 options). Therefore, when we configure this variable for data, it does not throw an error or
make any changes. For this, the python script should be configured.
* `Open` Python CLI only works by overriding values, so some of the unattached configurations should be integrated
into the TableMaker JSONs (Config MCRun2,MCRun3,DataRun2,Data Run3) in the O2DQWorkflows
repository as default or null values.
* `Finished` Some Tasks arguments need to be refactored.
* `Finished` For faster development, the auto completion feature should be implemented for arguments with the tab like
bash (Already Integrated for local).
* `Finished` After the developments are finished, the user manual should be prepared.
* `Open` For new feature tests, the ability to append new key-value pairs to JSONs should be implemented.
* `Open` JSON databases can be refactored in a more meaningful way. Now key-value pairs are equal.
* `Open` A transaction management should be written to search whether the entered aod file is in the location.
* `Open` If a configuration entered is not in JSON, a warning message should be written with a logger for this.
* `Open` char refactor for prefixes
* `Open` Transaction management, which checks whether the parameters are entered only once, should be written, for example -process BarrelOnly BarrelOnly should throw an error or a message should be checked by checking that the parameters are entered as value more than once with a warning.



# Instructions

Add extrac tables and converters with:
1. **--add_mc_conv**: conversion from o2mcparticle to o2mcparticle_001
2. **--add_fdd_conv**: conversion o2fdd from o2fdd_001
3. **--add_track_prop**: conversion from o2track to o2track_iu ([link](https://aliceo2group.github.io/analysis-framework/docs/helperTasks/trackPropagation.html))



Examples(in AllWorkFlows):
- Run TableMaker on Data run3 With Minimum Commands
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerDataRun3.json -runData --run 3
  ```
- Run TableMaker on MC run3 with Minimum Commands
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --run 3
  ```

In case of multiple configs example
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerDataRun3.json -runData --aod aodff --outputjson ConfiguredTableMakerData2 --onlySelect true --process BarrelOnly BarrelOnlyWithV0Bits --run 3 --syst PbPb --muonSelection 1 --processStandard false --isProcessEvTime false --processDummy barrel --isBarrelSelectionTiny false --cfgWithQA false --pid el mu --cfgPairCuts jpsiPIDnsigma electronPID2  --cfgEventCuts jpsiPIDnsigma --cfgBarrelTrackCuts jpsiPIDnsigma --cfgMuonCuts jpsiPIDnsigma --cfgNoQA false --cfgDetailedQA true --cfgMCsignals alicePrimary eeFromCC
  ```



TODO: Add Details


# Available configs in Interface

* For `IRunTableMaker.py`

Arg | Opt | Task | nargs |
--- | --- | --- | --- |
`--aod` | all | `internal-dpl-aod-reader` | 1 |
`--outputjson` | all | Special Option | 1 |
`--onlySelect` | `true`</br> `false`</br>  | Special Option | 1 |
`--process` | `Full` </br> `FullTiny`</br>  `FullWithCov`</br>  `FullWithCent`</br>  `BarrelOnlyWithV0Bits`</br>  `BarrelOnlyEventFilter`</br>  `BarrelOnlyWithCent`</br>  `BarrelOnlyWithCov`</br>  `BarrelOnly`</br>  `MuonOnlyWithCent`</br>  `MuonOnlyWithCov`</br>  `MuonOnly`</br>  `MuonOnlyWithFilter`</br>  `OnlyBCs`</br>  | `table-maker` | * |
`--run` | `2`</br> `3`</br> | Special Option | 1 |
`-runData` | No Param | `event-selection-task`</br> Special Option | 0 |
`-runMC` |  No Param | `event-selection-task`</br> Special Option | 0 |
`--add_mc_conv` | No Param  | `o2-analysis-mc-converter`</br> Special Option | 0 |
`--add_fdd_conv` | No Param | `o2-analysis-fdd-converter`</br> Special Option | 0 |
`--add_track_prop` | No Param | `o2-analysis-track-propagation`</br> Special Option | 0 |
`--syst` | `pp`</br> `PbPb`</br> | `event-selection-task` | 1 |
`--muonSelection` | `0`</br> `1`</br> | `event-selection-task` | 1 |
`--CustomDeltaBC` | all | `event-selection-task` | 1 |
`--processStandart` | `true`</br> `false`</br> | `track-propagation` | 1 |
`--processCovariance` | `true`</br> `false`</br> | `track-propagation` | 1 |
`--isProcessEvTime` | `true`</br> `false`</br> | `tof-pid-full tof-pid` | 1 |
`--tof-expreso` | all | `tof-pid-beta` | 1 |
`--processDummy` | `barrel`</br> `muon`</br> `event`</br> | `d-q-barrel-track-selection-task`</br> `d-q-muons-selection`</br> `d-q-event-selection-task`</br>  | * |
`--isBarrelSelectionTiny` | `true`</br> `false`</br> | `d-q-barrel-track-selection-task` | 1 |
`--est` | `VOM`</br> `Run2SPDtks`</br> `Run2SPDcls`</br> `Run2CL0`</br> `Run2CL1`</br>| `centrality-table` | |
`--cfgWithQA` | `true`</br> `false`</br> | `d-q-barrel-track-selection-task`</br> `d-q-event-selection-task`</br> `d-q-event-selection-task`</br> | 1 |
`--d_bz` | all | `v0-selector` | 1 |
`--v0cospa` | all | `v0-selector` | 1 |
`--dcav0dau` | all | `v0-selector` | 1 |
`--v0Rmin` | all | `v0-selector` | 1 |
`--v0Rmax` | all | `v0-selector` | 1 |
`--dcamin` | all | `v0-selector` | 1 |
`--dcamax` | all | `v0-selector` |  1|
`--mincrossedrows` | all | `v0-selector` | 1 |
`--maxchi2tpc` | all | `v0-selector` | 1 |
`--pid` | `el`</br> `mu`</br> `pi`</br> `ka`</br> `pr`</br> `de`</br> `tr`</br> `he`</br> `al`</br> | `tof-pid tpc-pid` | * |
`--FilterPP` | `full`</br> `tiny`</br>  `false`</br> | `d-q-filter-p-p-task` | 1 |
`--cfgPairCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `d-q-filter-p-p-task` | * |
`--cfgBarrelSels` | all | `d-q-filter-p-p-task` | * |
`--cfgMuonSels` | all | `d-q-filter-p-p-task` | * |
`--cfgEventCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | * |
`--cfgBarrelTrackCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | * |
`--cfgMuonCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | * |
`--cfgBarrelLowPt` | all | `table-maker` | 1 |
`--cfgMuonLowPt` | all | `table-maker` | 1 |
`--cfgNoQA` | `true`</br> `false`</br> | `table-maker` | 1 |
`--cfgDetailedQA` | `true`</br> `false`</br> | `table-maker` | 1 |
`--cfgMinTpcSignal` | all | `table-maker` | 1 |
`--cfgMaxTpcSignal` | all | `table-maker` | 1 |
`--cfgMCsignals` | [`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | `table-maker` | * |

* Details For `IRunTableMaker.py` (TODO Refactor)

Arg | Automate | Desc | Only | Type | default
--- | --- | --- | --- | --- | --- |
`--aod` | no | Add your aod file with path  | 1 | str | - |
`--outputjson` | no |  | 1 | str | `tempConfig.json` |
`--onlySelect` | Main parameter for automate  | Special Option | 1 | str.lower | `false` |
`--process` | d-q tasks activate/disable | `table-maker` | * | str |
`--run` | `2` `3` | no| 1 |
`-runData` | | `event-selection-task`</br> Special Option | 0 |
`-runMC` |  No Param | `event-selection-task`</br> Special Option | 0 |
`--add_mc_conv` | No Param  | `o2-analysis-mc-converter`</br> Special Option | 0 |
`--add_fdd_conv` | No Param | `o2-analysis-fdd-converter`</br> Special Option | 0 |
`--add_track_prop` | No Param | `o2-analysis-track-propagation`</br> Special Option | 0 |
`--syst` | `pp` `PbPb` | `event-selection-task` | 1 |
`--muonSelection` | `0` `1` | `event-selection-task` | 1 |
`--CustomDeltaBC` | all | `event-selection-task` | 1 |
`--processStandart` | `true` `false` | `track-propagation` | 1 |
`--processCovariance` | `true` `false` | `track-propagation` | 1 |
`--isProcessEvTime` | `true` `false` | `tof-pid-full tof-pid` | 1 |
`--tof-expreso` | all | `tof-pid-beta` | 1 |
`--processDummy` | `barrel` `muon` `event` | `d-q-barrel-track-selection-task`</br> `d-q-muons-selection`</br> `d-q-event-selection-task`</br>  | * |
`--isBarrelSelectionTiny` | `true` `false` | `d-q-barrel-track-selection-task` | 1 |
`--est` | `VOM` `Run2SPDtks` `Run2SPDcls` `Run2CL0` `Run2CL1`| `centrality-table` | |
`--cfgWithQA` | `true` `false` | `d-q-barrel-track-selection-task`</br> `d-q-event-selection-task`</br> `d-q-event-selection-task`</br> | 1 |
`--d_bz` | all | `v0-selector` | 1 |
`--v0cospa` | all | `v0-selector` | 1 |
`--dcav0dau` | all | `v0-selector` | 1 |
`--v0Rmin` | all | `v0-selector` | 1 |
`--v0Rmax` | all | `v0-selector` | 1 |
`--dcamin` | all | `v0-selector` | 1 |
`--dcamax` | all | `v0-selector` |  1|
`--mincrossedrows` | all | `v0-selector` | 1 |
`--maxchi2tpc` | all | `v0-selector` | 1 |
`--pid` | `el` `mu` `pi` `ka` `pr` `de` `tr` `he` `al` | `tof-pid tpc-pid` | * |
`--FilterPP` | `full` `tiny`  `false` | `d-q-filter-p-p-task` | 1 |
`--cfgPairCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `d-q-filter-p-p-task` | * |
`--cfgBarrelSels` | all | `d-q-filter-p-p-task` | * |
`--cfgMuonSels` | all | `d-q-filter-p-p-task` | * |
`--cfgEventCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | * |
`--cfgBarrelTrackCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | * |
`--cfgMuonCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | * |
`--cfgBarrelLowPt` | all | `table-maker` | 1 |
`--cfgMuonLowPt` | all | `table-maker` | 1 |
`--cfgNoQA` | `true` `false` | `table-maker` | 1 |
`--cfgDetailedQA` | `true` `false` | `table-maker` | 1 |
`--cfgMinTpcSignal` | all | `table-maker` | 1 |
`--cfgMaxTpcSignal` | all | `table-maker` | 1 |
`--cfgMCsignals` | [`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | `table-maker` | * |

* Visual Descriptions (TODO Refactor)


Arg | Option | JSON |
--- | --- | --- | 
`--aod` | no | Add your aod file with path  | 1 | str | - |
`--outputjson` | no |  | 1 | str | `tempConfig.json` |
`--onlySelect` | Main parameter for automate  | Special Option | 1 | str.lower | `false` |
`--process` | d-q tasks activate/disable | `table-maker` | * | str |
`--run` | `2` `3` | no| 1 |
`-runData` | | `event-selection-task`</br> Special Option | 0 |
`-runMC` |  No Param | `event-selection-task`</br> Special Option | 0 |
`--add_mc_conv` | No Param  | `o2-analysis-mc-converter`</br> Special Option | 0 |
`--add_fdd_conv` | No Param | `o2-analysis-fdd-converter`</br> Special Option | 0 |
`--add_track_prop` | No Param | `o2-analysis-track-propagation`</br> Special Option | 0 |
`--syst` | `pp` `PbPb` | `event-selection-task` | 1 |
`--muonSelection` | `0` `1` | `event-selection-task` | 1 |
`--CustomDeltaBC` | all | `event-selection-task` | 1 |
`--processStandart` | `true` `false` | `track-propagation` | 1 |
`--processCovariance` | `true` `false` | `track-propagation` | 1 |
`--isProcessEvTime` | `true` `false` | `tof-pid-full tof-pid` | 1 |
`--tof-expreso` | all | `tof-pid-beta` | 1 |
`--processDummy` | `barrel` `muon` `event` | `d-q-barrel-track-selection-task`</br> `d-q-muons-selection`</br> `d-q-event-selection-task`</br>  | * |
`--isBarrelSelectionTiny` | `true` `false` | `d-q-barrel-track-selection-task` | 1 |
`--est` | `VOM` `Run2SPDtks` `Run2SPDcls` `Run2CL0` `Run2CL1`| `centrality-table` | |
`--cfgWithQA` | `true` `false` | `d-q-barrel-track-selection-task`</br> `d-q-event-selection-task`</br> `d-q-event-selection-task`</br> | 1 |
`--d_bz` | all | `v0-selector` | 1 |
`--v0cospa` | all | `v0-selector` | 1 |
`--dcav0dau` | all | `v0-selector` | 1 |
`--v0Rmin` | all | `v0-selector` | 1 |
`--v0Rmax` | all | `v0-selector` | 1 |
`--dcamin` | all | `v0-selector` | 1 |
`--dcamax` | all | `v0-selector` |  1|
`--mincrossedrows` | all | `v0-selector` | 1 |
`--maxchi2tpc` | all | `v0-selector` | 1 |
`--pid` | `el` `mu` `pi` `ka` `pr` `de` `tr` `he` `al` | `tof-pid tpc-pid` | * |
`--FilterPP` | `full` `tiny`  `false` | `d-q-filter-p-p-task` | 1 |
`--cfgPairCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `d-q-filter-p-p-task` | * |
`--cfgBarrelSels` | all | `d-q-filter-p-p-task` | * |
`--cfgMuonSels` | all | `d-q-filter-p-p-task` | * |
`--cfgEventCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | * |
`--cfgBarrelTrackCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | * |
`--cfgMuonCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | * |
`--cfgBarrelLowPt` | all | `table-maker` | 1 |
`--cfgMuonLowPt` | all | `table-maker` | 1 |
`--cfgNoQA` | `true` `false` | `table-maker` | 1 |
`--cfgDetailedQA` | `true` `false` | `table-maker` | 1 |
`--cfgMinTpcSignal` | all | `table-maker` | 1 |
`--cfgMaxTpcSignal` | all | `table-maker` | 1 |
`--cfgMCsignals` | [`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | `table-maker` | * |

## Design Notes

* `Jul 20, 2022` Developed pythonCLI version 1 for tablemaker in its simplest form, not integrated into main task.
* `Jul 21, 2022` Fixed some important bugs.
* `Jul 22, 2022` The repository has been refactored. The CLI written for TableMaker was integrated into the task, main python scripts were prepared for TableReader, DQEfficiency, and their CLIs were developed and integrated (Faulty versions).
* `Jul 23, 2022` CLI for TableMaker for automations and transaction management has been heavily refactored and some automations imported.
* `Jul 24, 2022` In the CLI written for tableMaker, some options were refactored and automated. Version 2 released with minimal testing.
* `Jul 25, 2022` A lot of tests have been done for the CLI written for tableMaker and the necessary refactor and automation tests have been done. CLI development for TableMaker is fully completed and Integrated to python script. Writing User Manual Documentation in progress.







