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

* Database Contains configuration variables for MCSignals, Analysis Cuts, Histograms and Event Mixing Selections based on O2Physics PWG-DQ.
[`Database`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/AllWorkFlows/Database)

* JSON Database List in Table

Main File | Based on O2Physics | Description
--- | --- | ---
[`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | [`CutsLibrary.h`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/CutsLibrary.h) | Analysis Cuts in DQ
[`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | [`MCSignalLibrary.h`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/MCSignalLibrary.h) | MC Signals in DQ
`HistogramDatabase.json` | [`HistogramManager.h`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/HistogramManager.h) | Histograms in DQ
[`MixingDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MixingDatabase.json) | [`MixingLibrary.h`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Core/MixingLibrary.h) | Histograms in DQ

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

## Repository Organization and Development Strategy

While developing, python CLIs are prepared by creating python scripts with enough functions to override configuration values in JSON only (independent of O2). Then, O2DQWorkflow files are prepared that do not contain python CLI and can run the analysis with O2, then they are integrated into the previously prepared Python CLI O2DQWorkflows.

TODO: Add schema

* For O2DQWorkflow, a folder has been created for the 2nd stage tests containing python scripts to run inside O2 for each task. If the tests in the TestInteface folder pass, new developments are transferred here, where analysis tests are performed in O2.
[`TableMaker`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/TableMaker)
[`TableReader`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/TableReader)
[`DQEfficiency`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/DQEfficiency)
[`FilterPP`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/FilterPP)

* AllWorkFlows folder contains stable python workflow scripts with integrated Python CLI, their workflow configuration files and database files. Improvements should be moved here after done tests. 
[`AllWorkFlows`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/AllWorkFlows)

## argcomplete - Bash tab completion for argparse

Argcomplete provides easy, extensible command line tab completion of arguments for your Python script.

It makes two assumptions:

    You’re using bash as your shell (limited support for zsh, fish, and tcsh is available)

    You’re using argparse to manage your command line arguments/options

Argcomplete is particularly useful if your program has lots of options or subparsers, and if your program can dynamically suggest completions for your argument/option values (for example, if the user is browsing resources over the network).

Owner of Orginal Code: `Andrey Kislyuk` 
Licensed under the terms of the Apache License, Version 2.0.

Orginal Documentation:

https://kislyuk.github.io/argcomplete/index.html#

## Instalation Guide for argcomplete

### Local Instalation (Not Need For O2)

For Local İnstallation (If you have virtual env, disable it first)

`pip install argcomplete`
`activate-global-python-argcomplete`

### O2 Installation

For in O2

Firstly, activate your Alienv e.g.

`alienv enter O2Physics/latest-master-o2`

Then install the package:

`pip install argcomplete`

And go your Folder which includes your run scripts with cd commands (e.g.):

`cd ~/allWorkFlows`

And then, source your argcomplete script for autocomplete:

`source argcomplete.sh`

IMPORTANT P.S This script must be re-sourced every time you re-enter the O2 environment!!!


## Features for IRunTableMaker

### Automated Things In IRunTableMaker

* In TableMaker process function for Data Run 3, 
  * `Automate` If process contains only Barrel related value, it will automatically enable d-q-barrel-track-selection-task , d-q-event-selection-task and d-q-muons-selection task will be disabled
  * `Automate` if process contains only Muons related value, it will automatically enable d-q-muons-selection, d-q barrel-track-selection-task and d-q-event-selection-task it will disabled
  * `Automate` if process contains only BCs related value, it will automatically enable d-q-event-selection-task, d-q-muon-selection-task and d-q-barrel-track-selection-task will be disabled
  * `Automate` If process contains values ​​related to Full, then d-q-event-selection-task, d-q-muon-selection-task and d-q-barrel-track-selection-task are automatically enabled
    * `Automate` P.S: For Binary, Selections for Process Function (eg. Barrel and Muon Only), It will activate Barrel and Muon tasks and disables event selection tasks 
    * `Automate` P.S: For Three Selections for Process Function (eg. Barrel, BCs Muon Only), It will activate Barrel, Muon and BCs tasks 
  * `Automate` If process contains values ​​related to Filter, then d-q-filter-p-p-task is automatically enabled, otherwise this task will disabled
* For selections run <2|3> and run<MC|Data>
  * `Automate` if run 2 is selected, in JSON automatically processRun3 becomes false processRun2 becomes true, isRun2 becomes false
  * `Automate` if run 3 is selected, in JSON automatically processRun3 becomes true processRun2 becomes false, isRun2 becomes true
  * `Automate` if run 2 and MC selected, in JSON automatically isRun2MC becomes true, otherwise isRun2MC becomes false
  * `Automate` if MC Selected, in JSON automatically isMC becomes true. If Data Selected, isMC becomes false
* For Centrality Table Task, If collision system pp is selected or not selected but original JSON also has pp selected
  * `Automate` if runData is selected, centrality-table is deleted from JSON, if MC is deleted, centrality-table is not deleted since it is not in JSON
  * `Automate` if Table maker process function contains value related to Centrality (e.g. processMuonOnlyWithCent), Collision System pp can't be include related task about Centrality. They Will be removed in automation
  * `Automate` if Table maker process function contains value related to Centrality, Collision System pp can't be include related task about Centrality. They will be removed in automation. Also, it will not run automatically in the o2-analysis-centrality-table task. Because if the process function contains only Centrality, this task runs and in this part, the centrality values ​​are automatically set to false in the process function.
  * `Automate` if you forget configure name your output JSON with --outputjson (with overrided values), it will created as tempConfig.json. Also If you misstyped your file extension in json or if you forget this (e.g configs/ConfigTableMakerMCRun3) this will automaticly fixed to Configs/ConfigTableMakerMCRun3.json

### Logger Things In IRunTableMaker

* For TableMaker Process Function
  * If the value related to the process function is not defined in the tablemakerMC, the message that it is not defined is printed on the screen. This situation is handled automatically in the CLI and no error is thrown 
    * ```python
      print("[WARNING]", j ,"is Not valid Configurable Option for TableMaker/TableMakerMC regarding to Orginal JSON Config File!!!") 
      ```
    * ```bash
      # Example for MC Run3. commands are python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --run 3 --aod AO2D.root --outputjson ConfiguredTableMakerData2 --onlySelect true --process BarrelOnly MuonOnlyWithCent BarrelOnlyWithEventFilter --isBarrelSelectionTiny true --syst pp --cfgMCsignals eeFromSingleBandBtoC 
      [WARNING] processBarrelOnlyWithEventFilter is Not valid Configurable Option for TableMaker/TableMakerMC regarding to Orginal JSON Config File!!!
      ``` 
* Other Loggers based on parameters, MC and Data
  * If parameters in not valid for Orginal JSON, it will give a log message. You can check Avaible Loggers in below

    * ```python 
        # Parameter Checking 
        if key in V0Parameters and extrargs.runMC:
            print("[WARNING]","--"+key+" Not Valid Parameter. V0 Selector parameters only valid for Data, not MC. It will fixed by CLI")
        if key == 'cfgWithQA' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run 3, not MC and Run 2. It will fixed by CLI")
        if key == 'est' and extrargs.runMC:
            print("[WARNING]","--"+key+" Not Valid Parameter. Centrality Table parameters only valid for Data, not MC. It will fixed by CLI")
        if key =='isFilterPPTiny' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. Filter PP Tiny parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'cfgMuonSels' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'cfgBarrelSels' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'cfgPairCuts' and (extrargs.runMC or extrargs.run == '3'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run2, not MC and Run3. It will fixed by CLI")
        if key == 'isBarrelSelectionTiny' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'processDummy' and (extrargs.runMC or extrargs.run == '2'):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'cfgMCsignals' and extrargs.runData:
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for MC, not Data. It will fixed by CLI")
        if key == 'isProcessEvTime' and (extrargs.run == '2' or extrargs.runMC):
            print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI") 

        # TableMaker/TableMakerMC Task Checking
        if extrargs.runMC:
          try:
        if config["table-maker-m-c"]:
            pass
        except:
        print("[ERROR] JSON config does not include table-maker-m-c, It's for Data. Misconfiguration JSON File!!!")
        sys.exit()
        if extrargs.runData:
        try:
          if config["table-maker"]:
            pass
        except:
          print("[ERROR] JSON config does not include table-maker, It's for MC. Misconfiguration JSON File!!!")
          sys.exit()
        
        # AOD File Path Checking
        if extrargs.aod != None:
          if os.path.isfile(extrargs.aod) == False:
          print("[ERROR]",extrargs.aod,"File not found in path!!!")
          sys.exit()
        elif os.path.isfile((config["internal-dpl-aod-reader"]["aod-file"])) == False:
          print("[ERROR]",config["internal-dpl-aod-reader"]["aod-file"],"File not found in path!!!")
          sys.exit()
        ```
  * For Centrality Table task
    * Centrality task only available for PbPb system selection so if we select pp over PbPb, It will give LOG messages for this issue. Message : ```Collision System pp can't be include related task about Centrality. They Will be removed in automation. Check your JSON configuration file for Tablemaker process function!!!```
      * ```python 
          if extrargs.syst == 'pp' or  config["event-selection-task"]["syst"] == "pp":
          # delete centrality-table configurations for data. If it's MC don't delete from JSON
          # Firstly try for Data then if not data it gives warning message for MC
            try:
              del(config["centrality-table"])
            except:
                if extrargs.runMC:
                    print("[INFO] JSON file does not include configs for centrality-table task, It's for MC. Centrality will removed because you select pp collision system.")
            # check for is TableMaker includes task related to Centrality?
            processCentralityMatch = [s for s in extrargs.process if "Cent" in s]
            if len(processCentralityMatch) > 0:
                print("[WARNING] Collision System pp can't be include related task about Centrality. They Will be removed in automation. Check your JSON configuration file for Tablemaker process function!!!")
                for paramValueTableMaker in processCentralityMatch:
                    # Centrality process should be false
                    if extrargs.runMC:
                        try:       
                            config["table-maker-m-c"][paramValueTableMaker] = 'false'
                            #for key in paramValueTableMaker:
                                # TODO make print to new process
                        except:
                            print("[ERROR] JSON config does not include table-maker-m-c, It's for Data. Misconfiguration JSON File!!!")
                            sys.exit()
                    if extrargs.runData:
                        try:       
                            config["table-maker"][paramValueTableMaker] = 'false'
                            #for key in paramValueTableMaker:
                                #print(key)
                                # TODO make print to new process
                        except:
                            print("[ERROR] JSON config does not include table-maker, It's for MC. Misconfiguration JSON File!!!")
                            sys.exit()  
          ```
## Features for IRunTableReader

TODO Add Details

### Automated Things In IRunTableMaker


TODO Add Details

### Logger Things In IRunTableMaker


TODO Add Details

## Features for IRunDQEfficiency


TODO Add Details

### Automated Things In IRunDQEfficiency


TODO Add Details

### Logger Things In IRunDQEfficiency


TODO Add Details

## Some Things You Should Be Careful For Using and Development

* In JSON files, for example, when assigning a variable for the processFull argument, true or false must be
entered, if True or False like this style, it will throw an error because there is no capitalization check.
* There are also filters for some arguments. No value should be entered outside of these filters (look at the
choices).
* If the argument can take more than one value, when adding a new property choices is a list and the values
must be converted to comma-separated strings


# Instructions for IRunTableMaker.py

Add extrac tables and converters with:
1. **--add_mc_conv**: conversion from o2mcparticle to o2mcparticle_001
2. **--add_fdd_conv**: conversion o2fdd from o2fdd_001
3. **--add_track_prop**: conversion from o2track to o2track_iu ([link](https://aliceo2group.github.io/analysis-framework/docs/helperTasks/trackPropagation.html))


* Minimum Required Parameter List:
  * `python3`
  * `IRunTableMaker.py`
  * JSON Config File
    * Example usage: Configs/configTableMakerDataRun3.json 
  * `--run <2|3>`  
    * Usage (only select one value): `--run 2` or `--run 3`
  *  `-run<MC|Data>` 
     *  Usage (only select one value): `-runMC` or `-runData`
  *  `--process <Value>` 
     *  Usage examples (can take several value) : `--process MuonsOnly` or `--process BarrelOnly MuonOnly BarrelOnlyWithEventFilter`

Examples(in AllWorkFlows):
- Run TableMaker on Data run3 With Minimum Commands for Barrel Only (with automation)
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerDataRun3.json -runData --run 3 --process BarrelOnly --onlySelect true
  ```
- Run TableMaker on MC run3 with Minimum Commands for Barrel Only (with automation)
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --run 3 --process BarrelOnly --onlySelect true
  ```
- Run TableMaker on Data run2 With Minimum Commands for Barrel Only (with automation)
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerDataRun2.json -runData --run 2 --process BarrelOnly --onlySelect true
  ```
- Run TableMaker on MC run2 with Minimum Commands for Barrel Only (with automation)
  ```ruby
  python3 IRunTableMaker.py Configs/configTableMakerMCRun2.json -runMC --run 2 --process BarrelOnly --onlySelect true
  ```

In case of multiple configs example
  ```ruby
python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --run 3 --process MuonOnlyWithCov OnlyBCs --cfgMCsignals muFromJpsi Jpsi muFromPsi2S Psi2S --onlySelect true --aod Datas/AO2D.root --cfgMuonCuts muonQualityCuts muonTightQualityCutsForTests --syst pp --onlySelect true --add_track_prop
  ```

# Available configs in IRunTableMaker Interface

* For `IRunTableMaker.py` Selections

Arg | Opt | Task | nargs |
--- | --- | --- | --- |
`--aod` | all | `internal-dpl-aod-reader` | 1 |
`--onlySelect` | `true`</br> `false`</br>  | Special Option | 1 |
`--autoDummy` | `true`</br> `false`</br>  | Special Option | 1 |
`--process` | `Full` </br> `FullTiny`</br>  `FullWithCov`</br>  `FullWithCent`</br>  `BarrelOnlyWithV0Bits`</br>  `BarrelOnlyWithEventFilter`</br>  `BarrelOnlyWithCent`</br>  `BarrelOnlyWithCov`</br>  `BarrelOnly`</br>  `MuonOnlyWithCent`</br>  `MuonOnlyWithCov`</br>  `MuonOnly`</br>  `MuonOnlyWithFilter`</br>  `OnlyBCs`</br>  | `table-maker` | * |
`--run` | `2`</br> `3`</br> | Special Option | 1 |
`-runData` | No Param | `event-selection-task`</br> Special Option | 0 |
`-runMC` |  No Param | `event-selection-task`</br> Special Option | 0 |
`--add_mc_conv` | No Param  | `o2-analysis-mc-converter`</br> Special Option | 0 |
`--add_fdd_conv` | No Param | `o2-analysis-fdd-converter`</br> Special Option | 0 |
`--add_track_prop` | No Param | `o2-analysis-track-propagation`</br> Special Option | 0 |
`--syst` | `pp`</br> `PbPb`</br> `pPb`</br> `Pbp`</br> `XeXe`</br> | `event-selection-task` | 1 |
`--muonSelection` | `0`</br> `1`</br> `2` | `event-selection-task` | 1 |
`--CustomDeltaBC` | all | `event-selection-task` | 1 |
`--isCovariance` | `true`</br> `false`</br> | `track-propagation` | 1 |
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
`--isFilterPPTiny` | `true`</br>  `false`</br> | `d-q-filter-p-p-task` | 1 |
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

* Details parameters for `IRunTableMaker.py`

Arg | Ref Type| Desc | Default | Real Type
--- | --- | --- | --- | --- |
`--aod` | String | Add your aod file with path  |  | str |
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
`--processCovariance` | Boolean | If false, Process without covariance, If true Process with covariance related to `track-propagation` |  | str.lower
`--isProcessEvTime` | Boolean | Process Event Time Selection for `tof-pid-full tof-pid` |  | str.lower
`--tof-expreso` | Float | Expected resolution for the computation of the expected beta |  | str
`--processDummy` | String | Dummy function (No need If autoDummy is true) |  | str.lower
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
`--pid` | String | Produce PID information for the particle mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1) |  | str.lower
`--isFilterPPTiny` | Boolean | Run filter tiny task instead of normal (processFilterPP must be true) |  | str.lower
`--cfgPairCuts` | String | Space separated list of pair cuts |  | str
`--cfgBarrelSels` | String | Configure Barrel Selection <track-cut>:[<pair-cut>]:<n>,[<track-cut>:[<pair-cut>]:<n>],... | example jpsiO2MCdebugCuts2::1|  | str
`--cfgMuonSels` | String | Configure Muon Selection <muon-cut>:[<pair-cut>]:<n> example muonQualityCuts:pairNoCut:1|  | str
`--cfgEventCuts` | String | Space separated list of event cuts |  | str
`--cfgBarrelTrackCuts` | String | Space separated list of barrel track cuts |  | str
`--cfgMuonCuts` | String | Space separated list of muon cuts  |  | str
`--cfgBarrelLowPt` | Float | Specify the lowest pt cut for electrons; used in a Partition expression to improve CPU efficiency (GeV) |  | str
`--cfgMuonLowPt` | Float | Specify the lowest pt cut for muons; used in a Partition expression to improve CPU efficiency  (GeV) |  | str
`--cfgNoQA` | Boolean | If true, no QA histograms |  | str.lower
`--cfgDetailedQA` | Boolean | If true, include more QA histograms (BeforeCuts classes and more) |  | str.lower
`--cfgMinTpcSignal` | Integer| TPC Min Signal Selection |  | str
`--cfgMaxTpcSignal` | Integer | TPC Max Signal Selection |  | str
`--cfgMCsignals` | String | SSpace separated list of MC signals |  | str



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
  python3 IrunDQEfficiency.py Configs/configAnalysisData.json --aod Datas/AO2D_LHC21i3.root
  ```


TODO Add Details

# Available configs in IRunTableReader Interface

Arg | Opt | Task | nargs |
--- | --- | --- | --- |
`--aod` | all | `internal-dpl-aod-reader` | 1 |
`--autoDummy` | `true`</br> `false`</br>  | Special Option | 1 |
`--reader` | all | Special Option | 1 |
`--writer` | all | Special Option | 1 |
`--analysisSkimmed` | `event`</br>`track`</br>`muon`</br>`eventMixingBarrel`</br> `eventMixingMuon` </br> `eventMixingBarrelMuon` </br> `dileptonHadron`  | Special Option | * |
`--analysisAllSkimmed` | `true`</br> `false`</br>  | `table-maker` | 1 |
`--analysisDummy` |  `event`</br>`track`</br>`muon`</br>`eventMixing`</br>`sameEventPairing`</br> `dileptonHadron`  | `event-selection-task`</br> | * |
`--cfgQA` |`true` </br> `false`  | `event-selection-task`</br> | 1 |
`--cfgMixingVars` | [`MixingDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MixingDatabase.json)  | `analysis-event-selection`</br>  | * |
`--cfgEventCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json)  | `analysis-event-selection`</br>  | * |
`--cfgTrackCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `analysis-track-selection`</br> | * |
`--cfgMuonCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `analysis-muon-selection` | * |
`--processSameEventPairing` | `true`</br> `false`</br> | `analysis-same-event-pairing` | 1 |
`--isVertexing` | `true`</br> `false`</br> | `analysis-same-event-pairing` | 1 |
`--cfgLeptonCuts` | `true`</br> `false`</br> | `analysis-same-event-pairing` | * |

* Details parameters for `IRunTableReader.py`

Arg | Ref Type| Desc | Default | Real Type
--- | --- | --- | --- | --- |
`--aod` | String | Add your AOD File with path | - | str
`--autoDummy` | Boolean | Dummy automize parameter (if process skimmed false, it automatically activate dummy process and viceversa) | `true` | str.lower
`--reader` | String | Add your AOD Reader JSON with path | `Configs/readerConfiguration_reducedEvent.json` | str
`--writer` | String | Add your AOD Writer JSON with path | `Config/writerConfiguration_dileptons.json` | str
`--analysisSkimmed` | String | Skimmed process selections for analysis | - | str
`--analysisAllSkimmed` | Boolean | All Skimmed Selection as boolean | - | str.lower
`--analysisDummy` | String | Dummy Selections (if autoDummy true, you don't need it) | - | str
`--cfgQA` | Boolean | If true, fill QA histograms | - | str
`--cfgMixingVars` | String | Mixing configs separated by a space | - | str
`--cfgEventCuts` |  String | Space separated list of event cuts | - | str
`--cfgTrackCuts` | String | Space separated list of barrel track cuts | - | str
`--cfgMuonCuts` | String | Space separated list of muon cuts | - | str
`--processSameEventPairing` | Boolean | This option automatically activates  same-event-pairing based on analysis track, muon, event and event mixing | - | str.lower
`--isVertexing` | Boolean | Run muon-muon pairing and vertexing, with skimmed muons instead of Run muon-muon pairing, with skimmed muons (processJpsiToMuMuSkimmed must true for this selection) | - | str.lower
`--cfgLeptonCuts` | String | Space separated list of barrel track cuts | - | str
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
  python3 IRunDQEfficiency.py Configs/configAnalysisMC.json --analysisSkimmed muon event --aod reducedAod.root --cfgMuonCuts muonQualityCuts --cfgMuonMCSignals muFromJpsi --cfgQA true
  ```

# Available configs in IRunDQEfficiency Interface

* For `IRunDQEfficiency.py` Selections

Arg | Opt | Task | nargs |
--- | --- | --- | --- |
`--aod` | all | `internal-dpl-aod-reader` | 1 |
`--autoDummy` | `true`</br> `false`</br>  | Special Option | 1 |
`--reader` | all | Special Option | 1 |
`--writer` | all | Special Option | 1 |
`--analysisSkimmed` | `event`</br>`track`</br>`muon`</br>`dimuonMuon`</br>| Special Option | * |
`--analysisDummy` |  `event`</br>`track`</br>`muon`</br>`sameEventPairing`</br> `dilepton`  | `event-selection-task`</br> | * |
`--cfgQA` |`true` </br> `false`  | `event-selection-task`</br> | 1 |
`--cfgEventCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json)  | `analysis-event-selection`</br>  | * |
`--cfgTrackCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `analysis-track-selection`</br> | * |
`--cfgTrackMCSignals` | [`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | `analysis-track-selection` | * |
`--cfgMuonCuts` | [`AnalysisCutDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/AnalysisCutDatabase.json) | `analysis-muon-selection` | * |
`--cfgMuonMCSignals` | [`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | `analysis-muon-selection` | * |
`--processSameEventPairing` | `true`</br> `false`</br>  | `analysis-same-event-pairing` | 1 |
`--isVertexing` | `true`</br> `false`</br> | `analysis-same-event-pairing` | 1 |
`--cfgBarrelMCRecSignals` | [`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | `analysis-same-event-pairing` | * |
`--cfgBarrelMCGenSignals` | [`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | `analysis-same-event-pairing` | * |
`--cfgBarrelDileptonMCRecSignals` | [`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | `analysis-dilepton-track` | * |
`--cfgBarrelDileptonMCGenSignals` | [`MCSignalDatabase.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Database/MCSignalDatabase.json) | `analysis-dilepton-track` | * |

* Details parameters for `IRunDQEfficiency.py`

Arg | Ref Type| Desc | Default | Real Type
--- | --- | --- | --- | --- |
`--aod` | String | Add your AOD File with path | - | str
`--autoDummy` | Boolean | Dummy automize parameter (if process skimmed false, it automatically activate dummy process and viceversa) | `true` | str.lower
`--reader` | String | Add your AOD Reader JSON with path | `Configs/readerConfiguration_reducedEventMC.json` | str
`--writer` | String | Add your AOD Writer JSON with path | `Config/writerConfiguration_dileptonMC.json` | str
`--analysisSkimmed` | String | Skimmed process selections for analysis | - | str
`--analysisDummy` | String | Dummy Selections (if autoDummy true, you don't need it) | - | str
`--cfgQA` | Boolean | If true, fill QA histograms | - | str
`--cfgEventCuts` |  String | Space separated list of event cuts | - | str
`--cfgTrackCuts` | String | Space separated list of barrel track cuts | - | str
`--cfgTrackMCSignals` | String | Space separated list of MC signals | - | str
`--cfgMuonCuts` | String | Space separated list of muon cuts | - | str
`--cfgMuonMCSignals` | String | Space separated list of MC signals | - | str
`--processSameEventPairing` | Boolean | This option automatically activates same-event-pairing based on analysis track, muon and event | - | str.lower
`--isVertexing` | Boolean | Run muon-muon pairing and vertexing, with skimmed muons instead of Run muon-muon pairing, with skimmed muons (processJpsiToMuMuSkimmed must true for this selection) | - | str.lower
`----cfgBarrelMCRecSignals` | String | Space separated list of MC signals (reconstructed) | - | str
`--cfgBarrelMCGenSignals` | String | Space separated list of MC signals (generated) | - | str
`--cfgBarrelDileptonMCRecSignals` | String | Space separated list of MC signals (reconstructed) cuts | - | str
`--cfgBarrelDileptonMCGenSignals` | String | Space separated list of MC signals (generated)cuts | - | str


## TODO List For IRunTableMaker
* `Closed` We need more meaningful explanations for argument explanations (helping comments).
* `Open` The values that JSON values can take for transaction management should be classified and filtered with
choices and data types.
* `Finished` Also some JSON values are bound together (eg. if cfgRun2 is false, isRun3 variable should be true
automatically) so some error handling and automation should be done for transaction management.
* `Closed` Some configurations for MC may not be available for data configurations (eg. cfgMCsignals or vice versa, also
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
* `Open` JSON databases can be refactored in a more meaningful way. Now key-value pairs are equal (After Setting Naming conventions).
* `Closed` A transaction management should be written to search whether the entered aod file is in the location.
* `Closed` If a configuration entered is not in JSON, a warning message should be written with a logger for this.
* `Open` char refactor for prefixes
* `Open` Transaction management, which checks whether the parameters are entered only once, should be written, for example -process BarrelOnly BarrelOnly should throw an error or a warning message should be checked by checking that the parameters are entered as value more than once with a warning.


## Design Notes

* `Jul 20, 2022` Developed pythonCLI version 1 for tablemaker in its simplest form, not integrated into main task.
* `Jul 21, 2022` Fixed some important bugs.
* `Jul 22, 2022` The repository has been refactored. The CLI written for TableMaker was integrated into the task, main python scripts were prepared for TableReader, DQEfficiency, and their CLIs were developed and integrated (Faulty versions).
* `Jul 23, 2022` CLI for TableMaker for automations and transaction management has been heavily refactored and some automations imported.
* `Jul 24, 2022` In the CLI written for tableMaker, some options were refactored and automated. Version 2 released with minimal testing.
* `Jul 25, 2022` A lot of tests have been done for the CLI written for tableMaker and the necessary refactor and automation tests have been done. CLI development for TableMaker is fully completed and Integrated to python script. Writing User Manual Documentation in progress.
* `Jul 26, 2022` Readme completed for `IRunTableMaker.py` and TableReader DQEfficiency workflows CLI based v1 released. processEvTime transaction management refactoring, for pp collisionsi centrality-table o2 task and JSON configs deleting automatized. New checker for Run/MC added.
* `Jul 27, 2022` Fixed a bug for filterpp tiny selection in Tablemaker, AOD File Checker added to TableMaker, readme updated (instructions added), New Critical Transaction Managements Added, For TableMaker process Function, Workflow Decision Tree Added   
* `Jul 28, 2022` Workflows with CLI for TableReader and DQEfficiency Completed. Demo versions and Old Version Deleted. JSON path's for single workflows updated. Mixing Library added for Skimmed processes, runtime errors fixed, writer configs added to CLI, CommandToRun Fixed in TableReader in DQEfficiency, MC Rec Gen Signals fixed for dileptons in DQEfficiency, only-select automation parameter will implemnt for TableReader and DQEfficiency, installation guide for argcomplate added, Instructions and avaiable commands added readme for TableMaker DQ Efficiency
* `Jul 29, 2022` All Tests passed for workflows and development is completed. Only some parts need refactoring for clean code and readme will updated.








