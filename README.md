# Interfaced O2/DQ Workflows
Python CLI Development and implematation Repository for Contains O2/DQ workflow json configuration files and python scripts to run them

## Contact
Ionut Christian Arsene (Owner of [`O2DQWorkflows`](https://github.com/iarsene/O2DQworkflows))

Cevat Batuhan Tolon

Ida

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
* test script for Interfaced IRunFilterPP.py
[`IRunFilterPPDemo.h`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/TestInterface/IFilterPPDemo.py).
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
* We need more meaningful explanations for argument explanations (helping comments).
* The values that JSON values can take for transaction management should be classified and filtered with
choices and data types.
* Also some JSON values are bound together (eg. if cfgRun2 is false, isRun3 variable should be true
automatically) so some error handling and automation should be done for transaction management.
* Some configurations for MC may not be available for data configurations (eg. cfgMCsignals or vice versa, also
valid for Run2 Run3 options). Therefore, when we configure this variable for data, it does not throw an error or
make any changes. For this, the python script should be configured.
* Python CLI only works by overriding values, so some of the unattached configurations should be integrated
into the TableMaker JSONs (Config MCRun2,MCRun3,DataRun2,Data Run3) in the O2DQWorkflows
repository as default or null values.
* Some Tasks arguments need to be refactored.
* For faster development, the auto completion feature should be implemented for arguments with the tab like
bash.
* After the developments are finished, the user manual should be prepared.
* For new feature tests, the ability to append new key-value pairs to JSONs should be implemented.
* JSON databases can be refactored in a more meaningful way. Now key-value pairs are equal.

# Instructions

TODO: Add Details

Param | Opt | Task | Desc | Automate | nargs | Default | Only
--- | --- | --- | --- | --- | --- | --- | --- |
`--aod` | No Restrications | `internal-dpl-aod-reader` | |
`--outputjson` | No Restrications | Special Option | |
`--onlySelect` | true false | Special Option | |
`--process` | `Full` `FullTiny` `FullWithCov` `FullWithCent` `BarrelOnlyWithV0Bits` `BarrelOnlyEventFilter` `BarrelOnlyWithCent` `BarrelOnlyWithCov` `BarrelOnly` `MuonOnlyWithCent` `MuonOnlyWithCov` `MuonOnly` `MuonOnlyWithFilter` `OnlyBCs` | `table-maker` | |
`--run` | `2` `3` | Special Option | |
`--isMC` | `true` `false` | `event-selection-task` | |
`--` | No Restrications | `internal-dpl-aod-reader` | |
`--syst` | `pp` `PbPb` | `event-selection-task` | |
`--muonSelection` | `0` `1` | `event-selection-task` | |
`--CustomDeltaBC` | No Restrications | `event-selection-task` | |
`--processStandart` | `true` `false` | `track-propagation` | |
`--processCovariance` | `true` `false` | `track-propagation` | |
`--isProcessEvTime` | `true` `false` | `tof-pid-full tof-pid` | |
`--tof-expreso` | No Restrications | `tof-pid-beta` | |
`--processDummy` | Not Integrated Yet! | `internal-dpl-aod-reader` | |
`--isBarrelSelectionTiny` | `true` `false` | `d-q-barrel-track-selection-task` | |
`--est` | `VOM` `Run2SPDtks` `Run2SPDcls` `Run2CL0` `Run2CL1`| `centrality-table` | |
`--cfgWithQA` | `true` `false` | `internal-dpl-aod-reader` | |
`--d_bz` | No Restrications | `v0-selector` | |
`--v0cospa` | No Restrications | `v0-selector` | |
`--dcav0dau` | No Restrications | `v0-selector` | |
`--v0Rmin` | No Restrications | `v0-selector` | |
`--v0Rmax` | No Restrications | `v0-selector` | |
`--dcamin` | No Restrications | `v0-selector` | |
`--dcamax` | No Restrications | `v0-selector` | |
`--mincrossedrows` | No Restrications | `v0-selector` | |
`--maxchi2tpc` | No Restrications | `v0-selector` | |
`--pid'` | `el` `mu` `pi` `ka` `pr` `de` `tr` `he` `al` | `tof-pid tpc-pid` | |
`--isFilterPPTiny` | `true` `false` | `d-q-filter-p-p-task` | |
`--cfgPairCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `internal-dpl-aod-reader` | |
`--cfgBarrelSels` | No Restrications | `internal-dpl-aod-reader` | |
`--cfgPairCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `internal-dpl-aod-reader` | |
`--cfgEventCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | |
`--cfgBarrelTrackCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | |
`--cfgMuonCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `table-maker` | |
`--cfgBarrelLowPt` | No Restrications | `table-maker` | |
`--cfgMuonLowPt` | No Restrications | `table-maker` | |
`--cfgNoQA` | `true` `false` | `table-maker` | |
`--cfgDetailedQA` | `true` `false` | `table-maker` | |
`--cfgMinTpcSignal` | No Restrications | `table-maker` | |
`--cfgMaxTpcSignal` | No Restrications | `table-maker` | |
`--cfgMCsignals` | [`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | `table-maker` | |





Main File | Data Model | Description
--- | --- | ---
[`readerConfiguration_reducedEvent.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configTableMakerDataRun2.json) | DQ Skimmed Data Model | for data
[`readerConfiguration_reducedEventMC.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configTableMakerDataRun3.json) | DQ Skimmed Data Model | for MC

TO BE ADDED

# Available configs in Interface

TO BE ADDED
