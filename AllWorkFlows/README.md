# Old Interface

This folder contains new interface based on [`O2DQWorkflows`](https://github.com/iarsene/O2DQworkflows)

P.S. The interface here has not been maintained. It is highly recommended to use the new interface. Many commands are missing and configurations are more complex

## Main Scripts

* Script used to run both the skimming tasks (tableMaker.cxx and tableMakerMC.cxx)
[`IRunTableMaker.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/IRunTableMaker.py).
* Analyze DQ skimmed data tables. This workflow runs a few tasks: event selection, barrel track selection, muon track selection etc.
[`IRunTableReader.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/IRunTableMaker.py).
* Which contains the tasks DQEventSelection for event selection, DQBarrelTrackSelection for barrel track selection and single track MC matching, and the DQQuarkoniumPairing for reconstructed track pairing, MC matching of the pairs and counting of generated MC signals.  
[`IRunDQEfficiency.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/IRunDQEfficiency..py).
* Produces a decision table for pp collisions. The decisions require that at least a selected pair (or just two tracks) exists for a given event. Currently up to 64 simultaneous decisions can be made, to facilitate studies for optimizing cuts. 
[`IRunFilterPP.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/IRunFilterPP.py).
* Task to compute Q vectors and other quanitites related from the generic framework. Generic framework O2 version is a port of the AliPhysics version. To be used in the DQ analyses aiming for flow measurements 
[`IRunDQFlow.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/IRunDQFlow.py).
* It provides Download needed O2-DQ Libraries (CutsLibrary, MCSignalLibrary, MixingLibrary from O2Physics) for validation and autocompletion in Manual way. You can download libs with version as nightly
[`DownloadLibs.py`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/DownloadLibs.py).

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
[`configFilterPPDataRun2.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configFilterPPDataRun2.json) | [`filterPP.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Tasks/filterPP.cxx) | run with filterPP.cxx
[`configFlowDataRun2.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configFlowDataRun2.json) | [`dqFlow.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Tasks/dqFlow.cxx) | run with dqFlow.cxx
[`configFlowDataRun3.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/configFlowDataRun3.json) | [`dqFlow.cxx`](https://github.com/AliceO2Group/O2Physics/blob/master/PWGDQ/Tasks/dqFlow.cxx) | run with dqFlow.cxx


* JSON Reader Configuations for the DQ skimmed tables

Main File | Data Model | Description
--- | --- | ---
[`readerConfiguration_reducedEvent.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/NewAllWorkFlows/Configs/readerConfiguration_reducedEvent.json) | DQ Skimmed Data Model | For Data
[`readerConfiguration_reducedEventMC.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/NewAllWorkFlows/Configs/readerConfiguration_reducedEventMC.json) | DQ Skimmed Data Model | For MC

* JSON Writer Configuations for produce extra dilepton Tables in DQ skimmed tables

Main File | Data Model | Description
--- | --- | ---
[`writerConfiguration_dileptons.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/writerConfiguration_dileptons.json) | DQ Skimmed Data Model | for data
[`writerConfiguration_dileptonMC.json`](https://github.com/ctolon/PythonInterfaceDemo/blob/main/AllWorkFlows/Configs/writerConfiguration_dileptonMC.json) | DQ Skimmed Data Model | for MC

## Repository Organization and Development Strategy

While developing, python CLIs are prepared by creating python scripts with enough functions to override configuration values in JSON only (independent of O2). Then, O2DQWorkflow files are prepared that do not contain python CLI and can run the analysis with O2, then they are integrated into the previously prepared Python CLI O2DQWorkflows.

* For O2DQWorkflow, a folder has been created for the 2nd stage tests containing python scripts to run inside O2 for each task. If the tests in the TestInteface folder pass, new developments are transferred here, where analysis tests are performed in O2.

* AllWorkFlows folder contains stable python workflow scripts with integrated Python CLI, their workflow configuration files and database files. Improvements should be moved here after done tests. 
[`AllWorkFlows`](https://github.com/ctolon/PythonInterfaceDemo/tree/main/AllWorkFlows)

# Prerequisites!!!

## Cloning repository

Clone Repository in your workspace:

`git clone https://github.com/ctolon/PythonInterfaceDemo.git`

Then go AllWorkFlows folder with `cd` commands

Since the scripts are still in development, it is recommended to update daily regularly with the following command:

`git pull --rebase`

## argcomplete - Bash tab completion for argparse

If you are using a linux based system or working on LXPLUS (like Ubuntu, Fedora CentOS), follow the instructions for Linux. If you are using a MacOS-based system, follow the instructions for MacOS.

Argcomplete provides easy, extensible command line tab completion of arguments for your Python script.

It makes two assumptions:

    You’re using bash as your shell (limited support for zsh, fish, and tcsh is available)

    You’re using argparse to manage your command line arguments/options

Argcomplete is particularly useful if your program has lots of options or subparsers, and if your program can dynamically suggest completions for your argument/option values (for example, if the user is browsing resources over the network).

Owner of Orginal Code: `Andrey Kislyuk` 
Licensed under the terms of the Apache License, Version 2.0.

Orginal Documentation:

https://kislyuk.github.io/argcomplete/index.html#

## Instalation Guide For argcomplete

### Prerequisites Before Installation argcomplete Package For Linux Based Systems and LXPLUS

Global completion requires bash support for complete -D, which was introduced in bash 4.2. Older Linux systems, you will need to update bash to use this feature. Check the shell type with `echo $SHEL`. If it's bash, Check the version of the running copy of bash with `echo $BASH_VERSION`. If your bash version older than 4.2 you need the update your bash:

Update Bash on CentOS/Redhat/Fedora Linux:

`yum update bash`

Update Bash in Ubuntu / Debian / Linux Mint:

`apt-get install --only-upgrade bash`

Also you need check your shell type with `echo $SHEL`. if your shell isn't bash you need change your shell with (if your shell type is bash you don't need to use these commands):

`exec bash` (It just changes the type of terminal you are working in, the system's main shell settings are preserved)

or

`sudo chsh -s /bin/bash <username>` or  `sudo chsh -s /bin/bash` (Converts all system shell settings to bash)

IMPORTANT P.S 1 : If you use the `exec` bash command you will need to use this command every time when you open a new terminal to for source the argcomplete.sh script.

IMPORTANT P.S 2 : If you cannot source the `argcomplete.sh` script even though you are using the `exec bash` command, use the `sudo chsh -s /bin/bash` command. This command will change the shell settings of the entire system. When you're done with O2-DQ Scripts, you can similarly use `sudo chsh -s /bin/<shelltype>` to return to your old shell system. For example, if your host's default shell configuration is `zsh`, you can restore the system with `sudo chsh -s /bin/zsh`


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

VERY IMPORTANT P.S This script must be re-sourced every time you re-enter the O2 environment!!! (For autocompletion with TAB key)

### Prerequisites Before Installation argcomplete Package For MacOS Based Systems

Global completion requires bash support for complete -D, which was introduced in bash 4.2. On OS X, you will need to install and update bash to use this feature. On OS X, install bash via Homebrew `brew install bash`, add /usr/local/bin/bash to /etc/shells, then run `exec bash` to switch bash shell temporary (temporarily applies to the terminal you are working in, does not change your shell system settings). if you still have problems with sourcing the argcomplete.sh script, use this command instead `sudo chsh -s /bin/bash` or `sudo chsh -s /bin/bash <username>`. This will change the shell settings of the whole system and for example if your system used zsh based shell before to go back, you can use the command `sudo chsh -s /bin/zsh <username>` or `sudo chsh -s /bin/zsh`.

### Local Instalation (Not Need For O2)

`brew install bash`

For Local İnstallation (If you have virtual env, disable it first)

`pip install argcomplete` or `pip3 install argcomplete` (depends on symbolic link of python. It is recommended to install with both options)
`activate-global-python-argcomplete`

### O2 Installation

Install and update your bash shell with this command:

`brew install bash`

Then check your shell with this command:

`echo $SHEL`

If your shell isn't bash (The default shell for macOS is zsh, not bash. Most likely your shell type is zsh), you need change your bash with this commands:

`exec bash` (It just changes the type of terminal you are working in, the system's main shell settings are preserved)

or

`sudo chsh -s /bin/bash <username>` or  `sudo chsh -s /bin/bash` (Converts all system shell settings to bash)

After then, Check the version of the running copy of bash with `echo $BASH_VERSION`. It must be greater than 4.2.

IMPORTANT P.S 1 : If you use the `exec` bash command you will need to use this command every time when you open a new terminal to for source the argcomplete.sh script.

IMPORTANT P.S 2 : If you cannot source the `argcomplete.sh` script even though you are using the `exec bash` command, use the `sudo chsh -s /bin/bash` command. This command will change the shell settings of the entire system. When you're done with O2-DQ Scripts, you can similarly use `sudo chsh -s /bin/<shelltype>` to return to your old shell system. For example, if your host's default shell configuration is `zsh`, you can restore the system with `sudo chsh -s /bin/zsh`

For in O2

Firstly, activate your Alienv e.g.

`alienv enter O2Physics/latest-master-o2`

Then install the package:

`pip install argcomplete` or `pip3 install argcomplete` (depends on symbolic link of python. It is recommended to install with both options)

And go your Folder which includes your run scripts with cd commands (e.g.):

`cd ~/allWorkFlows`

And then, source your argcomplete script for autocomplete:

`source argcomplete.sh`

VERY IMPORTANT P.S This script must be re-sourced every time you re-enter the O2 environment!!! (For autocompletion with TAB key)


# Instructions for TAB Autocomplete

Before proceeding to this stage, you should make sure that you activate the O2 environment with alienv, then install the argcomplete package with `pip install argcomplete` and `pip3 install argcomplete` in O2, and then source the autocomplete bash script with `source argcomplete.sh`

You can Complete this with a TAB key after each word and character you type in command line. Keep this thing in your mind.

If you have successfully installed this package and successfully sourced the script, follow these steps.

step 1: type python3 (If your symbolic link is python for python3, type python)

```ruby
python3
```

step 2: type the name of your script (eg IRunTableMaker.py)
```ruby
python3 IRunTableMaker.py
```

step 3: At this stage, since the JSON configuration files are in the Configs folder, enter the name of your JSON config file by completing it with TAB or listing the available options

for ex. if you type:

```ruby
python3 IRunTableMaker.py Configs
```

you will get this displayed options in your terminal:
```ruby
Configs/configAnalysisData.json                  Configs/configFlowDataRun3.json                  Configs/configtestFilterPPDataRun3.json          Configs/readerConfiguration_reducedEventMC.json
Configs/configAnalysisMC.json                    Configs/configTableMakerDataRun2.json            Configs/configtestFlowDataRun3.json              Configs/writerConfiguration_dileptonMC.json
Configs/configFilterPPDataRun2.json              Configs/configTableMakerDataRun3.json            Configs/configtestTableMakerDataRun3.json        Configs/writerConfiguration_dileptons.json
Configs/configFilterPPRun3.json                  Configs/configTableMakerMCRun2.json              Configs/readerConfiguration_dilepton.json        
Configs/configFlowDataRun2.json                  Configs/configTableMakerMCRun3.json              Configs/readerConfiguration_reducedEvent.json 
```

then you can complete your JSON config file (for example assuming you export configTableMakerMCRun3.json to configure tablemaker for mc run 3)

```ruby
python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json
```

P.S You can Complete this with a TAB key after each word and character you type in command line.

step 4: now when you type -- and press TAB key all parameter options in interface will be listed

```ruby
python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json --
```

if you type like this and press TAB you will see all the parameters in the interface in your terminal like this:
```ruby
--add_fdd_conv           --cfgBarrelSels          --cfgMinTpcSignal        --cfgPairCuts            --dcamin                 --isCovariance           --mincrossedrows         --syst
--add_mc_conv            --cfgBarrelTrackCuts     --cfgMuonCuts            --cfgWithQA              --dcav0dau               --isFilterPPTiny         --muonSelection          --tof-expreso
--add_track_prop         --cfgDetailedQA          --cfgMuonLowPt           --customDeltaBC          --debug                  --isProcessEvTime        --onlySelect             --v0cospa
--aod                    --cfgEventCuts           --cfgMuonsCuts           --cutLister              --est                    --logFile                --pid                    --v0Rmax
--autoDummy              --cfgMaxTpcSignal        --cfgMuonSels            --d_bz                   --help                   --maxchi2tpc             --process                --v0Rmin
--cfgBarrelLowPt         --cfgMCsignals           --cfgNoQA                --dcamax                 --isBarrelSelectionTiny  --MCSignalsLister        --run 
```

VERY IMPORTANT STEP AND P.S: When configuring the IRunTableMaker.py script, the -runData and -runMC parameters are used when configuring the tablemaker for MC or Data. Since these parameters start with a single minus, do not forget to configure the TableMaker script only at the first time, by pressing the tab and configuring it (other interfaces do not have a parameter that starts with a single minus)

```ruby
python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -
```

Then you will see -runData and -runMC in your parameters:

```ruby
--add_fdd_conv           --cfgBarrelTrackCuts     --cfgMuonLowPt           --cutLister              -h                       --maxchi2tpc             --run                    --v0Rmin
--add_mc_conv            --cfgDetailedQA          --cfgMuonsCuts           --d_bz                   --help                   --MCSignalsLister        -runData                 
--add_track_prop         --cfgEventCuts           --cfgMuonSels            --dcamax                 --isBarrelSelectionTiny  --mincrossedrows         -runMC                   
--aod                    --cfgMaxTpcSignal        --cfgNoQA                --dcamin                 --isCovariance           --muonSelection          --syst                   
--autoDummy              --cfgMCsignals           --cfgPairCuts            --dcav0dau               --isFilterPPTiny         --onlySelect             --tof-expreso            
--cfgBarrelLowPt         --cfgMinTpcSignal        --cfgWithQA              --debug                  --isProcessEvTime        --pid                    --v0cospa                
--cfgBarrelSels          --cfgMuonCuts            --customDeltaBC          --est                    --logFile                --process                --v0Rmax  
```

step 5: After entering one of these parameters (eg --cfgBarrelTrackCuts for IRunTableMaker.py) leave a space and press tab again. As a result you will see each value this parameter can take.

```ruby
python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --cfgBarrelTrackCuts
```


If you leave a space after cfgBarrelTrackCuts and press TAB:

```ruby
electronPID1                         eventStandard                        jpsiPIDshift                         matchedGlobal                        PIDCalib
electronPID1randomized               eventStandardNoINT7                  jpsiPIDworseRes                      mchTrack                             pidcalib_ele
electronPID1shiftDown                highPtHadron                         jpsiStandardKine                     muonHighPt                           PIDStandardKine
electronPID1shiftUp                  int7vtxZ5                            kaonPID                              muonLowPt                            singleDCA
electronPID2                         jpsiBenchmarkCuts                    kaonPIDnsigma                        muonQualityCuts                      standardPrimaryTrack
electronPID2randomized               jpsiKineAndQuality                   lmee_GlobalTrack                     muonTightQualityCutsForTests         TightGlobalTrack
electronPIDnsigma                    jpsiO2MCdebugCuts                    lmee_GlobalTrackRun3                 NoPID                                TightGlobalTrackRun3
electronPIDnsigmaLoose               jpsiO2MCdebugCuts2                   lmee_GlobalTrackRun3_lowPt           pairDCA                              TightTPCTrackRun3
electronPIDnsigmaOpen                jpsiO2MCdebugCuts3                   lmee_GlobalTrackRun3_TPC_ePID_lowPt  pairJpsi                             tof_electron
electronPIDnsigmaRandomized          jpsiPID1                             lmeeLowBKine                         pairJpsiLowPt1                       tof_electron_loose
electronPIDshift                     jpsiPID1Randomized                   lmeePID_TOFrec                       pairJpsiLowPt2                       tpc_electron
electronPIDworseRes                  jpsiPID1shiftDown                    lmeePID_TPChadrej                    pairMassLow                          tpc_kaon_rejection
electronStandardQuality              jpsiPID1shiftUp                      lmeePID_TPChadrejTOFrec              pairNoCut                            tpc_pion_band_rejection
electronStandardQualityBenchmark     jpsiPID2                             lmeePID_TPChadrejTOFrecRun3          pairPsi2S                            tpc_pion_rejection
electronStandardQualityForO2MCdebug  jpsiPID2Randomized                   lmeeStandardKine                     pairPtLow1                           tpc_pion_rejection_highp
eventDimuonStandard                  jpsiPIDnsigma                        lmee_TPCTrackRun3_lowPt              pairPtLow2                           tpc_proton_rejection
eventMuonStandard                    jpsiPIDnsigmaRandomized              matchedFwd                           pairUpsilon
```

step 6: after configuring the config, type space and -- again to see other parameters again and see other parameters and use autocomplete with TAB as you type

```ruby
python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --cfgBarrelTrackCuts --
```

```ruby
--add_fdd_conv           --cfgBarrelSels          --cfgMinTpcSignal        --cfgPairCuts            --dcamin                 --isCovariance           --mincrossedrows         --syst
--add_mc_conv            --cfgBarrelTrackCuts     --cfgMuonCuts            --cfgWithQA              --dcav0dau               --isFilterPPTiny         --muonSelection          --tof-expreso
--add_track_prop         --cfgDetailedQA          --cfgMuonLowPt           --customDeltaBC          --debug                  --isProcessEvTime        --onlySelect             --v0cospa
--aod                    --cfgEventCuts           --cfgMuonsCuts           --cutLister              --est                    --logFile                --pid                    --v0Rmax
--autoDummy              --cfgMaxTpcSignal        --cfgMuonSels            --d_bz                   --help                   --maxchi2tpc             --process                --v0Rmin
--cfgBarrelLowPt         --cfgMCsignals           --cfgNoQA                --dcamax                 --isBarrelSelectionTiny  --MCSignalsLister        --run 
```

After that you can similarly continue configuring your parameters with autocompletion.

VERY IMPORTANT P.S: Not every parameter in the interface has a value to configure. Some are configured as metavariable, meaning they are itself a value parameter. To explain this situation in detail, for example, `--cfgWithQA` parameter in tablemaker has to take one of two values as true or false, while `--add_track_prop` or `-runMC` is a parameter value directly and remains false when it is not added to the command line, they do not take a value. They are configured as true only when you type them on the command line.

Example:

```ruby
python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --add_track_prop
```

```ruby
python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json --cfgBarrelTrackCuts jpsiPID1 --cfgWithQA true
```

list of metavar parameters:

* `--add_track_prop`
* `--add_fdd_conv`
* `--add_mc_conv`
* `-runMC` (This parameter is only for tableMakerMC)
* `-runData` (This parameter is only for tableMaker)
* `--logFile`
* `--MCSignalsLister` (this parameter only for tableMakerMC and dqEfficiency interface)
* `--cutLister`
* `--mixingLister` (this parameter only for tableReader interface)

# Instructions for DownloadLibs.py

## Download CutsLibrary, MCSignalLibrary, MixingLibrary From Github

VERY IMPORTANT P.S: Downloading DQ libraries from Github is unstable and has a lot of issues. So use `DownloadLibs.py` script locally if you are working at local machine. It is highly recommended to skip this part directly and go to `Get CutsLibrary, MCSignalLibrary, MixingLibrary From Local Machine` (You cannot use the Local option for LXPLUS, use this part if you are working in LXPLUS).

These libraries must be downloaded for validation and autocomplete. After the argscomplete package is installed and sourced, they will be downloaded automatically if you do an one time autocomplete operation with the TAB key and the name of the script in the terminal. If you cannot provide this, the `DownloadLibs.py` script in the AllWorkFlows folder can do it manually. To run this script, simply type the following on the command line.

P.S. Don't forget source your argcomplete Before the using this script. --> `source argcomplete.sh`

`python3 DownloadLibs.py`

For tag version based download (depends your production) e.g for nightly-20220619, just enter as 20220619:

`python3 DownloadLibs.py --version 20220619`

If the libraries are downloaded successfully you will get this message:

`[INFO] Libraries downloaded successfully!`

## Get CutsLibrary, MCSignalLibrary, MixingLibrary From Local Machine

These libraries must be downloaded for validation and autocomplete. Instead of downloading libraries from github, you can configure the DownloadLibs.py script to pull the DQ libraries locally from the alice software on the existing computer. This option will not work on LXPLUS. if you are working on a local machine always use this option.

P.S. Don't forget source your argcomplete Before the using this script. --> `source argcomplete.sh`

Ex. Usage for Working Locally:

`python3 DownloadLibs.py --local`

In this configuration, the location of alice software is defaulted to `/home/<user>/alice`. If your alice software folder has a different name or is in a different location, you can configure it with the --localPath parameter. Ex. Usage for different path

`python3 DownloadLibs.py --local --localPath alice-software`

So with this configuration, your alice software path is changed to `/home/<user>/alice-software`. Another ex.

`python3 DownloadLibs.py --version 20220619 --local --localPath Software/alice`

So with this configuration, your alice software path is changed to `/home/<user>/Sofware/alice`

If the DQ libraries are pulled from local alice software successfully you will get this message:

`[INFO] DQ Libraries pulled from local alice software successfully!`

We have many logger message for this interface. If you have a problem with configuration, you can find the solution very easily by following the logger messages here. This solution is completely stable

# Available configs in DownloadLibs.py Interface

Arg | Opt | Local/Online | nargs | ex. usage
--- | --- | --- | --- | --- | 
`-h` | No Param | `Online and Local` | 0 | `python3 DownloadLibs.py -h`
`--version` | all | `Online` | 1 |  `python3 DownloadLibs.py --version  20220619`
`--debug` | `NOTSET`</br> `DEBUG`</br>`INFO`</br>`WARNING` </br> `ERROR` </br>`CRITICAL` </br>  |  `Online and Local` | 1 |  `python3 DownloadLibs.py --debug INFO`
`--local` | No Param |  `Local` | 1 |  `python3 DownloadLibs.py --local`
`--localPath` | all |  `Local` | 1 |  `python3 DownloadLibs.py --local --localPath alice-software`

* More Details for `DownloadLibs.py` interface parameters

Arg | Ref Type| Desc | Default | Real Type
--- | --- | --- | --- | --- |
`-h` | No Param | list all helper messages for configurable commands | | *
`--version` | Integer | Online: Your Production tag for O2Physics example: for nightly-20220619, just enter as 20220619 | master | str |
`--debug` | string | Online and Local: execute with debug options" | `INFO` | str.upper
`--local` | No Param |Local: Use Local Paths for getting DQ Libraries instead of online github download. If you are working LXPLUS, It will not working so don't configure with option | - | *
`--localPath` | String | Local: Configure your alice software folder name in your local home path. Default is alice. Example different configuration is --localpath alice-software --local --> home/<user>/alice-software | `alice` | str


## Technical Informations

## Helper Command Functionality

With the `python3 <scriptname> -h` command you will see a help message for all commands valid for the CLI. CLI has same formatted messages in O2-DPL. It is recommended to use this command at least once before using the interface. If you do not remember the parameters related to the interface, you can list all valid parameters and the values that these parameters can take with this command. In addition, helper messages are integrated into helper messages for all values that are valid for each very important parameter. For example, if you want to get a help message with the `python3 IRunTableMaker.py -h` command:

P.S The default values you see in the helper messages are the default values for the interface. The values you see None will directly take the default values from JSON

```ruby
usage: IRunTableMaker.py [-h] [-runData] [-runMC] [--run {2,3}]
                         [--add_mc_conv] [--add_fdd_conv] [--add_track_prop]
                         [--aod AOD] [--onlySelect ONLYSELECT]
                         [--autoDummy {true,false}]
                         [--cfgEventCuts [CFGEVENTCUTS [CFGEVENTCUTS ...]]]
                         [--cfgBarrelTrackCuts [CFGBARRELTRACKCUTS [CFGBARRELTRACKCUTS ...]]]
                         [--cfgMuonCuts [CFGMUONCUTS [CFGMUONCUTS ...]]]
                         [--cfgBarrelLowPt CFGBARRELLOWPT]
                         [--cfgMuonLowPt CFGMUONLOWPT] [--cfgNoQA CFGNOQA]
                         [--cfgDetailedQA {true,false}]
                         [--cfgMinTpcSignal CFGMINTPCSIGNAL]
                         [--cfgMaxTpcSignal CFGMAXTPCSIGNAL]
                         [--cfgMCsignals [CFGMCSIGNALS [CFGMCSIGNALS ...]]]
                         [--process [PROCESS [PROCESS ...]]]
                         [--syst {PbPb,pp,pPb,Pbp,XeXe}]
                         [--muonSelection {0,1,2}]
                         [--customDeltaBC CUSTOMDELTABC]
                         [--isCovariance {true,false}]
                         [--tof-expreso TOF_EXPRESO]
                         [--isProcessEvTime {true,false}]
                         [--isBarrelSelectionTiny {true,false}]
                         [--cfgMuonsCuts [CFGMUONSCUT [CFGMUONSCUT ...]]]
                         [--cfgPairCuts [CFGPAIRCUTS [CFGPAIRCUTS ...]]]
                         [--cfgBarrelSels [CFGBARRELSELS [CFGBARRELSELS ...]]]
                         [--cfgMuonSels [CFGMUONSELS [CFGMUONSELS ...]]]
                         [--isFilterPPTiny {true,false}]
                         [--est [EST [EST ...]]] [--cfgWithQA {true,false}]
                         [--d_bz D_BZ] [--v0cospa V0COSPA]
                         [--dcav0dau DCAV0DAU] [--v0Rmin V0RMIN]
                         [--v0Rmax V0RMAX] [--dcamin DCAMIN] [--dcamax DCAMAX]
                         [--mincrossedrows MINCROSSEDROWS]
                         [--maxchi2tpc MAXCHI2TPC] [--pid [PID [PID ...]]]
                         [--cutLister] [--MCSignalsLister] [--debug DEBUG]
                         [--logFile]
                         Config.json

Arguments to pass

optional arguments:
  -h, --help            show this help message and exit

Core configurations that must be configured:
  Config.json           config JSON file name
  -runData              Run over data (default: False)
  -runMC                Run over MC (default: False)
  --run {2,3}           Run Number Selection (2 or 3) (default: None)

Additional Task Adding Options:
  --add_mc_conv         Add the converter from mcparticle to mcparticle+001
                        (Adds your workflow o2-analysis-mc-converter task)
                        (default: False)
  --add_fdd_conv        Add the fdd converter (Adds your workflow o2-analysis-
                        fdd-converter task) (default: False)
  --add_track_prop      Add track propagation to the innermost layer (TPC or
                        ITS) (Adds your workflow o2-analysis-track-propagation
                        task) (default: False)

Data processor options: internal-dpl-aod-reader:
  --aod AOD             Add your AOD File with path (default: None)

Automation Parameters:
  --onlySelect ONLYSELECT
                        An Automate parameter for keep options for only
                        selection in process, pid and centrality table (true
                        is highly recomended for automation) (default: true)
  --autoDummy {true,false}
                        Dummy automize parameter (don't configure it, true is
                        highly recomended for automation) (default: true)

Data processor options: table-maker:
  --cfgEventCuts [CFGEVENTCUTS [CFGEVENTCUTS ...]]
                        Space separated list of event cuts (default: None)
  --cfgBarrelTrackCuts [CFGBARRELTRACKCUTS [CFGBARRELTRACKCUTS ...]]
                        Space separated list of barrel track cuts (default:
                        None)
  --cfgMuonCuts [CFGMUONCUTS [CFGMUONCUTS ...]]
                        Space separated list of muon cuts in table-maker
                        (default: None)
  --cfgBarrelLowPt CFGBARRELLOWPT
                        Low pt cut for tracks in the barrel (default: None)
  --cfgMuonLowPt CFGMUONLOWPT
                        Low pt cut for muons (default: None)
  --cfgNoQA CFGNOQA     If true, no QA histograms (default: None)
  --cfgDetailedQA {true,false}
                        If true, include more QA histograms (BeforeCuts
                        classes and more) (default: None)
  --cfgMinTpcSignal CFGMINTPCSIGNAL
                        Minimum TPC signal (default: None)
  --cfgMaxTpcSignal CFGMAXTPCSIGNAL
                        Maximum TPC signal (default: None)
  --cfgMCsignals [CFGMCSIGNALS [CFGMCSIGNALS ...]]
                        Space separated list of MC signals (default: None)

Data processor options: table-maker/table-maker-m-c:
  --process [PROCESS [PROCESS ...]]
                        Process Selection options for tableMaker/tableMakerMC
                        Data Processing and Skimming (default: None)
  Full                  Build full DQ skimmed data model, w/o centrality
  FullTiny              Build full DQ skimmed data model tiny
  FullWithCov           Build full DQ skimmed data model, w/ track and
                        fwdtrack covariance tables
  FullWithCent          Build full DQ skimmed data model, w/ centrality
  BarrelOnly            Build barrel-only DQ skimmed data model, w/o
                        centrality
  BarrelOnlyWithCov     Build barrel-only DQ skimmed data model, w/ track cov
                        matrix
  BarrelOnlyWithV0Bits  Build full DQ skimmed data model, w/o centrality, w/
                        V0Bits
  BarrelOnlyWithEventFilter
                        Build full DQ skimmed data model, w/o centrality, w/
                        event filter
  BarrelOnlyWithCent    Build barrel-only DQ skimmed data model, w/ centrality
  MuonOnly              Build muon-only DQ skimmed data model
  MuonOnlyWithCov       Build muon-only DQ skimmed data model, w/ muon cov
                        matrix
  MuonOnlyWithCent      Build muon-only DQ skimmed data model, w/ centrality
  MuonOnlyWithFilter    Build muon-only DQ skimmed data model, w/ event filter
  OnlyBCs               Analyze the BCs to store sampled lumi

Data processor options: event-selection-task:
  --syst {PbPb,pp,pPb,Pbp,XeXe}
                        Collision System Selection ex. pp (default: None)
  --muonSelection {0,1,2}
                        0 - barrel, 1 - muon selection with pileup cuts, 2 -
                        muon selection without pileup cuts (default: None)
  --customDeltaBC CUSTOMDELTABC
                        custom BC delta for FIT-collision matching (default:
                        None)

Data processor options: track-propagation:
  --isCovariance {true,false}
                        track-propagation : If false, Process without
                        covariance, If true Process with covariance (default:
                        None)

Data processor options: tof-pid-beta:
  --tof-expreso TOF_EXPRESO
                        Expected resolution for the computation of the
                        expected beta (default: None)
  --isProcessEvTime {true,false}
                        tof-pid -> processEvTime : Process Selection options
                        true or false (string) (default: None)

Data processor options: d-q-track barrel-task:
  --isBarrelSelectionTiny {true,false}
                        Run barrel track selection instead of normal(process
                        func. for barrel selection must be true) (default:
                        false)

Data processor options: d-q muons selection:
  --cfgMuonsCuts [CFGMUONSCUT [CFGMUONSCUT ...]]
                        Space separated list of muon cuts in d-q muons
                        selection (default: None)

Data processor options: d-q-filter-p-p-task:
  --cfgPairCuts [CFGPAIRCUTS [CFGPAIRCUTS ...]]
                        Space separated list of pair cuts (default: None)
  --cfgBarrelSels [CFGBARRELSELS [CFGBARRELSELS ...]]
                        Configure Barrel Selection <track-cut>:[<pair-
                        cut>]:<n>,[<track-cut>:[<pair-cut>]:<n>],... | example
                        jpsiO2MCdebugCuts2::1 (default: None)
  --cfgMuonSels [CFGMUONSELS [CFGMUONSELS ...]]
                        Configure Muon Selection <muon-cut>:[<pair-cut>]:<n>
                        example muonQualityCuts:pairNoCut:1 (default: None)
  --isFilterPPTiny {true,false}
                        Run filter tiny task instead of normal
                        (processFilterPP must be true) (default: None)

Data processor options: centrality-table:
  --est [EST [EST ...]]
                        Produces centrality percentiles parameters (default:
                        None)
  V0M                   Produces centrality percentiles using V0 multiplicity.
                        -1: auto, 0: don't, 1: yes. Default: auto (-1)
  Run2SPDtks            Produces Run2 centrality percentiles using SPD
                        tracklets multiplicity. -1: auto, 0: don't, 1: yes.
                        Default: auto (-1)
  Run2SPDcls            Produces Run2 centrality percentiles using SPD
                        clusters multiplicity. -1: auto, 0: don't, 1: yes.
                        Default: auto (-1)
  Run2CL0               Produces Run2 centrality percentiles using CL0
                        multiplicity. -1: auto, 0: don't, 1: yes. Default:
                        auto (-1)
  Run2CL1               Produces Run2 centrality percentiles using CL1
                        multiplicity. -1: auto, 0: don't, 1: yes. Default:
                        auto (-1)

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

Data processor options: tof-pid, tpc-pid, tpc-pid-full:
  --pid [PID [PID ...]]
                        Produce PID information for the <particle> mass
                        hypothesis (default: None)
  el                    Produce PID information for the Electron mass
                        hypothesis, overrides the automatic setup: the
                        corresponding table can be set off (0) or on (1)
  mu                    Produce PID information for the Muon mass hypothesis,
                        overrides the automatic setup: the corresponding table
                        can be set off (0) or on (1)
  pi                    Produce PID information for the Pion mass hypothesis,
                        overrides the automatic setup: the corresponding table
                        can be set off (0) or on (1)
  ka                    Produce PID information for the Kaon mass hypothesis,
                        overrides the automatic setup: the corresponding table
                        can be set off (0) or on (1)
  pr                    Produce PID information for the Proton mass
                        hypothesis, overrides the automatic setup: the
                        corresponding table can be set off (0) or on (1)
  de                    Produce PID information for the Deuterons mass
                        hypothesis, overrides the automatic setup: the
                        corresponding table can be set off (0) or on (1)
  tr                    Produce PID information for the Triton mass
                        hypothesis, overrides the automatic setup: the
                        corresponding table can be set off (0) or on (1)
  he                    Produce PID information for the Helium3 mass
                        hypothesis, overrides the automatic setup: the
                        corresponding table can be set off (0) or on (1)
  al                    Produce PID information for the Alpha mass hypothesis,
                        overrides the automatic setup: the corresponding table
                        can be set off (0) or on (1)

Additional Helper Command Options:
  --cutLister           List all of the analysis cuts from CutsLibrary.h
                        (default: False)
  --MCSignalsLister     List all of the MCSignals from MCSignalLibrary.h
                        (default: False)
  --debug DEBUG         execute with debug options (default: INFO)
  --logFile             Enable logger for both file and CLI (default: False)

Choice List for debug Parameters:
  NOTSET                Set Debug Level to NOTSET
  DEBUG                 Set Debug Level to DEBUG
  INFO                  Set Debug Level to INFO
  WARNING               Set Debug Level to WARNING
  ERROR                 Set Debug Level to ERROR
  CRITICAL              Set Debug Level to CRITICAL
```

You will receive a message that. also the command can likewise be added after configuring other parameters. For example:
```ruby
 python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --run 3 --process MuonOnlyWithCov OnlyBCs --cfgMCsignals muFromJpsi Jpsi muFromPsi2S Psi2S --aod Datas/AO2D -h
 ```
 
You will see helper messages again. As long as this command is added in the parameters, the script will not run and will only show a help message.

### One Minimal Bug on Error Message

it lists parameter values that do not actually need to be configured in the arguments that need to be configured. This is because the user lists the required values for some parameters while configuring the help messages and takes the explanation of these values from the dummy positional arguments.Required option of positional arguments cannot be changed.

Ex. tableMaker for help mesaage of `--process`:

```ruby
Data processor options: table-maker/table-maker-m-c:
  --process [PROCESS [PROCESS ...]]
                        Process Selection options for tableMaker/tableMakerMC
                        Data Processing and Skimming (default: None)
  Full                  Build full DQ skimmed data model, w/o centrality
  FullTiny              Build full DQ skimmed data model tiny
  FullWithCov           Build full DQ skimmed data model, w/ track and
                        fwdtrack covariance tables
  FullWithCent          Build full DQ skimmed data model, w/ centrality
  BarrelOnly            Build barrel-only DQ skimmed data model, w/o
                        centrality
  BarrelOnlyWithCov     Build barrel-only DQ skimmed data model, w/ track cov
                        matrix
  BarrelOnlyWithV0Bits  Build full DQ skimmed data model, w/o centrality, w/
                        V0Bits
  BarrelOnlyWithEventFilter
                        Build full DQ skimmed data model, w/o centrality, w/
                        event filter
  BarrelOnlyWithCent    Build barrel-only DQ skimmed data model, w/ centrality
  MuonOnly              Build muon-only DQ skimmed data model
  MuonOnlyWithCov       Build muon-only DQ skimmed data model, w/ muon cov
                        matrix
  MuonOnlyWithCent      Build muon-only DQ skimmed data model, w/ centrality
  MuonOnlyWithFilter    Build muon-only DQ skimmed data model, w/ event filter
  OnlyBCs               Analyze the BCs to store sampled lumi
```


 We can solve this as a positional argument by putting -- at the beginning of each value. But this will cause confusion in the user help message. Because they are values (Full, FullTiny, BarrelOnly...), not parameters (like --process). If you get an error like this:

```ruby
IRunTableMaker.py: error: the following arguments are required: Config.json, Full, FullTiny, FullWithCov, FullWithCent, BarrelOnly, BarrelOnlyWithCov, BarrelOnlyWithV0Bits, BarrelOnlyWithEventFilter, BarrelOnlyWithCent, MuonOnly, MuonOnlyWithCov, MuonOnlyWithCent, MuonOnlyWithFilter, OnlyBCs, V0M, Run2SPDtks, Run2SPDcls, Run2CL0, Run2CL1, el, mu, pi, ka, pr, de, tr, he, al, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
```
  
This means only your JSON config file is missing from your workflow. ignore the rest


## Debug and Logging Options for O2DQWorkflows and DownloadLibs.py

We have Debug options if you want to follow the flow in the Interface. For this, you can configure your script as `--debug` `<Level>` in the terminal. You can check which levels are valid and at which level to debug from the table. Also if you want to keep your LOG log in a file then the `--logFile` parameter should be added to the workflow.

The LOG file will be created the same as the workflow name. For example, the file that will be created for tableMaker will be `tableMaker.log`. In addition, if you work with the debug option, the old LOG file will be automatically deleted first, so that there is no confusion in the log files and it does not override. Then a new LOG file will be created.

* You can See Debug Levels in the table:
  
Level | Numeric Value |
| --- | --- |
`NOTSET` | 0 |
`DEBUG` | 10 |
`INFO` | 20 |
`WARNING` | 30 |
`ERROR` | 40 |
`CRITICAL` | 50 |

You can see the debug messages of the numeric value you selected and the level above. If you want debug with `--debug` parameter, you must select the Level you want to debug.

Example usage Logging for Both File and terminal:

```ruby 
  python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --run 3  --debug DEBUG --logFile --process MuonOnlyWithCov OnlyBCs --cfgMCsignals muFromJpsi Jpsi muFromPsi2S Psi2S --aod Datas/AO2D.root --cfgMuonCuts muonQualityCuts muonTightQualityCutsForTests --syst pp --add_track_prop
```

Example usage for only logging to terminal:

```ruby 
  python3 IRunTableMaker.py Configs/configTableMakerMCRun3.json -runMC --run 3 --debug DEBUG --process MuonOnlyWithCov OnlyBCs --cfgMCsignals muFromJpsi Jpsi muFromPsi2S Psi2S --aod Datas/AO2D.root --cfgMuonCuts muonQualityCuts muonTightQualityCutsForTests --syst pp --add_track_prop
```

For example, when the file is logged, you should see a result like this when you open the relevant file.

```ruby 
  2022-08-17 17:15:06,628 - [DEBUG]  - [internal-dpl-aod-reader] aod-file : reducedAod.root
  2022-08-17 17:15:06,628 - [DEBUG]  - [internal-dpl-aod-reader] aod-reader-json : Configs/readerConfiguration_reducedEventMC.json
  2022-08-17 17:15:06,628 - [DEBUG]  - [analysis-event-selection] processSkimmed : true
  2022-08-17 17:15:06,628 - [DEBUG]  - [analysis-track-selection] processSkimmed : false
  2022-08-17 17:15:06,628 - [DEBUG]  - [analysis-muon-selection] cfgMuonCuts : muonQualityCuts,muonTightQualityCutsForTests
  2022-08-17 17:15:06,629 - [DEBUG]  - [analysis-muon-selection] cfgMuonMCSignals : muFromJpsi,muFromPsi2S
  2022-08-17 17:15:06,629 - [DEBUG]  - [analysis-muon-selection] processSkimmed : true
  2022-08-17 17:15:06,629 - [DEBUG]  - [analysis-same-event-pairing] cfgMuonCuts : muonQualityCuts,muonTightQualityCutsForTests
  2022-08-17 17:15:06,629 - [DEBUG]  - [analysis-same-event-pairing] cfgBarrelMCRecSignals : mumuFromJpsi,mumuFromPsi2S,dimuon
  2022-08-17 17:15:06,629 - [DEBUG]  - [analysis-same-event-pairing] cfgBarrelMCGenSignals : Jpsi,Psi2S
  2022-08-17 17:15:06,629 - [DEBUG]  - [analysis-same-event-pairing] processJpsiToEESkimmed : false
  2022-08-17 17:15:06,629 - [DEBUG]  - [analysis-same-event-pairing] processJpsiToMuMuSkimmed : true
  2022-08-17 17:15:06,630 - [DEBUG]  - [analysis-same-event-pairing] processJpsiToMuMuVertexingSkimmed : false
  2022-08-17 17:15:06,630 - [DEBUG]  - [analysis-dilepton-track] processDimuonMuonSkimmed : false
  2022-08-17 17:15:06,630 - [INFO] Command to run:
  2022-08-17 17:15:06,630 - [INFO] o2-analysis-dq-efficiency --configuration json://tempConfigDQEfficiency.json -b --aod-writer-json Configs/writerConfiguration_dileptonMC.json
  2022-08-17 17:15:06,630 - [INFO] Args provided configurations List
  2022-08-17 17:15:06,631 - [INFO] --cfgFileName : Configs/configAnalysisMC.json 
  2022-08-17 17:15:06,631 - [INFO] --add_mc_conv : False 
  2022-08-17 17:15:06,631 - [INFO] --add_fdd_conv : False 
  2022-08-17 17:15:06,631 - [INFO] --add_track_prop : False 
  2022-08-17 17:15:06,631 - [INFO] --logFile : True 
  2022-08-17 17:15:06,631 - [INFO] --aod : reducedAod.root 
  2022-08-17 17:15:06,631 - [INFO] --reader : Configs/readerConfiguration_reducedEventMC.json 
  2022-08-17 17:15:06,632 - [INFO] --writer : Configs/writerConfiguration_dileptonMC.json 
  2022-08-17 17:15:06,632 - [INFO] --analysis : ['muonSelection', 'eventSelection', 'sameEventPairing'] 
  2022-08-17 17:15:06,632 - [INFO] --process : ['JpsiToMuMu'] 
  2022-08-17 17:15:06,632 - [INFO] --autoDummy : true 
  2022-08-17 17:15:06,632 - [INFO] --cfgMuonCuts : muonQualityCuts,muonTightQualityCutsForTests 
  2022-08-17 17:15:06,632 - [INFO] --cfgMuonMCSignals : muFromJpsi,muFromPsi2S 
  2022-08-17 17:15:06,633 - [INFO] --cfgBarrelMCRecSignals : mumuFromJpsi,mumuFromPsi2S,dimuon 
  2022-08-17 17:15:06,633 - [INFO] --cfgBarrelMCGenSignals : Jpsi,Psi2S 
  2022-08-17 17:15:06,633 - [INFO] --cutLister : False 
  2022-08-17 17:15:06,633 - [INFO] --MCSignalsLister : False 
  2022-08-17 17:15:06,633 - [INFO] --debug : DEBUG 
```
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
            logging.warning("--%s Not Valid Parameter. V0 Selector parameters only valid for Data, not MC. It will fixed by CLI", key)
        if key == 'cfgWithQA' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run 3, not MC and Run 2. It will fixed by CLI", key)
        if key == 'est' and extrargs.runMC:
            logging.warning("--%s Not Valid Parameter. Centrality Table parameters only valid for Data, not MC. It will fixed by CLI", key)
        if key =='isFilterPPTiny' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. Filter PP Tiny parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)
        if key == 'cfgMuonSels' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)
        if key == 'cfgBarrelSels' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)
        if key == 'cfgPairCuts' and (extrargs.runMC or extrargs.run == '3'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run2, not MC and Run3. It will fixed by CLI", key)
        #if key == 'isBarrelSelectionTiny' and (extrargs.runMC or extrargs.run == '2') and extrargs.isBarrelSelectionTiny: TODO: fix logging bug
            #print("[WARNING]","--"+key+" Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI")
        if key == 'processDummy' and (extrargs.runMC or extrargs.run == '2'):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)
        if key == 'cfgMCsignals' and extrargs.runData:
            logging.warning("--%s Not Valid Parameter. This parameter only valid for MC, not Data. It will fixed by CLI", key)
        if key == 'isProcessEvTime' and (extrargs.run == '2' or extrargs.runMC):
            logging.warning("--%s Not Valid Parameter. This parameter only valid for Data Run3, not MC and Run2. It will fixed by CLI", key)

        # TableMaker/TableMakerMC Task Checking
        if extrargs.runMC:
            try:
                if config["table-maker-m-c"]:
                    logging.info("tablemaker-m-c is in your JSON Config File")
            except:
                logging.error("JSON config does not include table-maker-m-c, It's for Data. Misconfiguration JSON File!!!")
                sys.exit()
        if extrargs.runData:
            try:
                if config["table-maker"]:
                    logging.info("tablemaker is in your JSON Config File")
            except:
                logging.error("JSON config does not include table-maker, It's for MC. Misconfiguration JSON File!!!")
                sys.exit()
        
        # AOD File Path Checking
        if extrargs.aod != None:
            if os.path.isfile(extrargs.aod) == False:
                logging.error("%s File not found in path!!!",extrargs.aod)
                sys.exit()
        elif os.path.isfile((config["internal-dpl-aod-reader"]["aod-file"])) == False:
                print("[ERROR]",config["internal-dpl-aod-reader"]["aod-file"],"File not found in path!!!")
                sys.exit()
        ```
  * For Centrality Table task
    * Centrality task only available for PbPb system selection so if we select pp over PbPb, It will give LOG messages for this issue. Message : ```Collision System pp can't be include related task about Centrality. They Will be removed in automation. Check your JSON configuration file for Tablemaker process function!!!```
      * ```python 
          if len(centSearch) != 0 and (extrargs.syst == 'pp' or (extrargs.syst == None and config["event-selection-task"]["syst"] == "pp")):
              # delete centrality-table configurations for data. If it's MC don't delete from JSON
              # Firstly try for Data then if not data it gives warning message for MC
              noDeleteNeedForCent = False
              try:
                  logging.warning("JSON file does not include configs for centrality-table task, It's for DATA. Centrality will removed because you select pp collision system.")
                  #del(config["centrality-table"])
              except:
                  if extrargs.runMC:
                      logging.warning("JSON file does not include configs for centrality-table task, It's for MC. Centrality will removed because you select pp collision system.")
              # check for is TableMaker includes task related to Centrality?
              try:
                  processCentralityMatch = [s for s in extrargs.process if "Cent" in s]
                  if len(processCentralityMatch) > 0:
                      logging.warning("Collision System pp can't be include related task about Centrality. They Will be removed in automation. Check your JSON configuration file for Tablemaker process function!!!")
                      for paramValueTableMaker in processCentralityMatch:
                          # Centrality process should be false
                          if extrargs.runMC:
                              try:       
                                  config["table-maker-m-c"][paramValueTableMaker] = 'false'
                              except:
                                  logging.error("JSON config does not include table-maker-m-c, It's for Data. Misconfiguration JSON File!!!")
                                  sys.exit()
                          if extrargs.runData:
                              try:       
                                  config["table-maker"][paramValueTableMaker] = 'false'
                              except:
                                  logging.error("JSON config does not include table-maker, It's for MC. Misconfiguration JSON File!!!")
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

## Some Notes Before The Instructions

* You don't have to configure all the parameters in the Python interface. the parameter you did not configure will remain as the value in the JSON.
* Don't forget to configure your Config JSON file in interface for each workflow and also configure extra `-run<Data|MC>` and `--run <2|3>` parameters for tablemaker workflow only
* sometimes you may need to add extra tables and transformations to your workflow to resolve the errors you get. These are related to the data model and the production tag. It is stated in the steps that they will be used when errors are received. If you get an error about these add the relevant parameter to your workflow


# OLD INTERFACE IN ALLWORKFLOWS INSTRUCTIONS
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
`-h` | No Param | all | 0 |
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
`--cfgPairCuts` | `allPairCuts` | `d-q-filter-p-p-task` | * |
`--cfgBarrelSels` | `namespacedCuts` | `d-q-filter-p-p-task` | * |
`--cfgMuonSels` | `namespacedCuts` | `d-q-filter-p-p-task` | * |
`--cfgEventCuts` | `allCuts` | `table-maker` | * |
`--cfgBarrelTrackCuts` | [`allCuts` | `table-maker` | * |
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
`--isCovariance` | Boolean | If false, Process without covariance, If true Process with covariance related to `track-propagation` |  | str.lower
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
`--cfgBarrelSels` | String | Configure Barrel Selection track-cut:pair-cut:n,track-cut:pair-cut:n,... example jpsiO2MCdebugCuts2::1|  | str
`--cfgMuonSels` | String | Configure Muon Selection muon-cut:[pair-cut]:n example muonQualityCuts:pairNoCut:1|  | str
`--cfgEventCuts` | String | Space separated list of event cuts |  | str
`--cfgBarrelTrackCuts` | String | Space separated list of barrel track cuts |  | str
`--cfgMuonCuts` | String | Space separated list of muon cuts in tablemaker  |  | str
`--cfgMuonsCuts` | String | Space separated list of muon cuts in d-q muons selection  |  | str
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
  python3 IRunTableReader.py Configs/configAnalysisData.json --aod Datas/AO2D_LHC21i3.root
  ```


TODO Add Details for multiple commands

# Available configs in IRunTableReader Interface

Arg | Opt | Task | nargs |
--- | --- | --- | --- |
`-h` | No Param | all | 0 |
`--aod` | all | `internal-dpl-aod-reader` | 1 |
`--autoDummy` | `true`</br> `false`</br>  | Special Option | 1 |
`--reader` | all | Special Option | 1 |
`--writer` | all | Special Option | 1 |
`--analysis` | `eventSelection`</br>`trackSelection`</br>`muonSelection`</br>`sameEventPairing`</br> `dileptonHadronSelection`  | `analysis-event-selection`</br>`analysis-track-selection`</br>`analysis-muon-selection`</br>`analysis-same-event-pairing`</br>`analysis-dilepton-hadron`  | * |
`--process` | `JpsiToEE`</br>`JpsiToMuMu`</br>`JpsiToMuMuVertexing`</br>`ElectronMuon`</br> `All`  | `analysis-same-event-pairing` | * |
`--add_mc_conv` | No Param  | `o2-analysis-mc-converter`</br> Special Option | 0 |
`--add_fdd_conv` | No Param | `o2-analysis-fdd-converter`</br> Special Option | 0 |
`--add_track_prop` | No Param | `o2-analysis-track-propagation`</br> Special Option | 0 |
`--syst` | `pp`</br> `PbPb`</br> `pPb`</br> `Pbp`</br> `XeXe`</br> | `event-selection-task` | 1 |
`--isMixingEvent` | `true`</br>`false`</br>  | `analysis-event-mixing-selection` | 1 |
`--cfgQA` |`true` </br> `false`  | `event-selection-task`</br> | 1 |
`--cfgMixingVars` | `allMixingVars`  | `analysis-event-selection`</br>  | * |
`--cfgEventCuts` | `allCuts`  | `analysis-event-selection`</br>  | * |
`--cfgTrackCuts` | `allCuts` | `analysis-track-selection`</br> | * |
`--cfgMuonCuts` | `allCuts` | `analysis-muon-selection` | * |
`--cfgLeptonCuts` | `true`</br> `false`</br> | `analysis-same-event-pairing` | * |
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
`--add_mc_conv` | No Param  | Conversion from o2mcparticle to o2mcparticle_001< |  | -
`--add_fdd_conv` | No Param | Conversion o2fdd from o2fdd_001 |  | -
`--add_track_prop` | No Param | Conversion from o2track to o2track_iu  |  | -
`--isMixingEvent` | String | Event Mixing Activate or Disable Option | - | str.lower |
`--cfgQA` | Boolean | If true, fill QA histograms | - | str
`--cfgMixingVars` | String | Mixing configs separated by a space | - | str
`--cfgEventCuts` |  String | Space separated list of event cuts | - | str
`--cfgTrackCuts` | String | Space separated list of barrel track cuts | - | str
`--cfgMuonCuts` | String | Space separated list of muon cuts in tablemaker | - | str
`--cfgLeptonCuts` | String | Space separated list of barrel track cuts | - | str
`--cutLister` | No Param | Lists All of the valid Analysis Cuts from CutsLibrary.h from O2Physics-DQ| 0 |  | -
`--mixingLister` | No Param | Lists All of the valid event mixing selections from MixingLibrary.h from O2Physics-DQ |  | -
`--debug` | String | execute with debug options  | - | str.upper |
`--logFile` | No Param | Enable logger for both file and CLI  | - | - |
# Instructions for IRunDQEfficiency.py

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
`--analysis` | `eventSelection`</br>`trackSelection`</br>`muonSelection`</br>`sameEventPairing`</br>`dileptonTrackSelection`</br>| `analysis-event-selection`</br>`analysis-track-selection`</br>`analysis-muon-selection`</br>`analysis-same-event-pairing`</br>`analysis-dilepton-track` | * |
`--process` | `JpsiToEE`</br>`JpsiToMuMu`</br>`JpsiToMuMuVertexing`</br>| `analysis-same-event-pairing` | * |
`--add_mc_conv` | No Param  | `o2-analysis-mc-converter`</br> Special Option | 0 |
`--add_fdd_conv` | No Param | `o2-analysis-fdd-converter`</br> Special Option | 0 |
`--add_track_prop` | No Param | `o2-analysis-track-propagation`</br> Special Option | 0 |
`--syst` | `pp`</br> `PbPb`</br> `pPb`</br> `Pbp`</br> `XeXe`</br> | `event-selection-task` | 1 |
`--cfgQA` |`true` </br> `false`  | `event-selection-task`</br> | 1 |
`--cfgEventCuts` | `allCuts` | `analysis-event-selection`</br>  | * |
`--cfgTrackCuts` | `allCuts` | `analysis-track-selection`</br> | * |
`--cfgTrackMCSignals` | `allMCSignals` | `analysis-track-selection` | * |
`--cfgMuonCuts` | `allCuts` | `analysis-muon-selection` | * |
`--cfgMuonMCSignals` | `allMCSignals` | `analysis-muon-selection` | * |
`--cfgBarrelMCRecSignals` | `allMCSignals` | `analysis-same-event-pairing` | * |
`--cfgBarrelMCGenSignals` | `allMCSignals` | `analysis-same-event-pairing` | * |
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
`--add_mc_conv` | No Param  | Conversion from o2mcparticle to o2mcparticle_001< |  | -
`--add_fdd_conv` | No Param | Conversion o2fdd from o2fdd_001 |  | -
`--add_track_prop` | No Param | Conversion from o2track to o2track_iu  |  | -
`--cfgQA` | Boolean | If true, fill QA histograms | - | str
`--cfgEventCuts` |  String | Space separated list of event cuts | - | str
`--cfgTrackCuts` | String | Space separated list of barrel track cuts | - | str
`--cfgTrackMCSignals` | String | Space separated list of MC signals | - | str
`--cfgMuonCuts` | String | Space separated list of muon cuts in tablemaker | - | str
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
`--pid` | `el`</br> `mu`</br> `pi`</br> `ka`</br> `pr`</br> `de`</br> `tr`</br> `he`</br> `al`</br> | `tof-pid tpc-pid` | * |
`--isProcessEvTime` | `true`</br> `false`</br> | `tof-pid-full tof-pid` | 1 |
`--tof-expreso` | all | `tof-pid-beta` | 1 |
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
`--pid` | String | Produce PID information for the particle mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1) |  | str.lower
`--isProcessEvTime` | Boolean | Process Event Time Selection for `tof-pid-full tof-pid` |  | str.lower
`--tof-expreso` | Float | Expected resolution for the computation of the expected beta |  | str
`--cfgWithQA` | Boolean | If true, fill QA histograms |  | str.lower
`--cfgEventCuts` | String | Space separated list of event cuts |  | str
`--cfgBarrelTrackCuts` | String | Space separated list of barrel track cuts |  | str
`--cfgBarrelSels` | String | Configure Barrel Selection track-cut:pair-cut:n,track-cut:pair-cut:n,... example jpsiO2MCdebugCuts2::1|  | str
`--cfgMuonSels` | String | Configure Muon Selection muon-cut:[pair-cut]:n example muonQualityCuts:pairNoCut:1|  | str
`--cfgMuonsCuts` | String | Space separated list of muon cuts in d-q muons selection  |  | str
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
`--tof-expreso` | all | `tof-pid-beta` | 1 |
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
`--pid` | String | Produce PID information for the particle mass hypothesis, overrides the automatic setup: the corresponding table can be set off (0) or on (1) |  | str.lower
`--tof-expreso` | Float | Expected resolution for the computation of the expected beta |  | str
`--cfgWithQA` | Boolean | If true, fill QA histograms |  | str.lower
`--cfgEventCuts` | String | Space separated list of event cuts |  | str
`--cfgTrackCuts` | String | Space separated list of barrel track cuts |  | str
`--cfgMuonCuts` | String | Space separated list of muon cuts in d-q muons selection  |  | str
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


## TODO List For Python Workflows
* `Finished` We need more meaningful explanations for argument explanations (helping comments).
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
* `Closed` JSON databases can be refactored in a more meaningful way. Now key-value pairs are equal (After Setting Naming conventions).
* `Closed` A transaction management should be written to search whether the entered aod file is in the location.
* `Closed` If a configuration entered is not in JSON, a warning message should be written with a logger for this.
* `Open` char refactor for prefixes
* `Open` Transaction management, which checks whether the parameters are entered only once, should be written, for example -process BarrelOnly BarrelOnly should throw an error or a warning message should be checked by checking that the parameters are entered as value more than once with a warning.


## Feedbacks, Suggestions and User Acceptance Test List

Date |  User | Type | Desc 
--- | --- | --- | --- |
`Aug 11, 2022` | `luca Micheletti` | `Suggestion` | Preparing a tutorial script for scripts. 
`Aug 15, 2022` | `Anastasia Merzlaya` | `User Acceptance Test` | ran the scripts successfully. Passed user acceptance tests. (only DQEfficiency) 
`Aug 19, 2022` | `Liuyao Zhang` | `User Acceptance Test` | He had trouble with the argcomplete package on his macOS-based system. We solved this problem together in the same day and it ran all the scripts without any problem. Passed user acceptance tests. Updated argcomplete package installation instructions for macOS. (argcomplete package)
`Aug 22, 2022` | `Liuyao Zhang` | `User Acceptance Test` | Reports a problem about aod checker functionality in interface. It fixed. (interface functionality)
`Aug 23, 2022` | `Liuyao Zhang` | `User Acceptance Test` | Reports a bug for SEP Process functionality, It fixed. (for tableReader and dqEfficiency)
`Aug 23, 2022` | `Liuyao Zhang` | `User Acceptance Test` | Reports a bug dilepton analysis for pp (for LHC22c). DileptonAOD.root ttres are created blank. It's not fixed now. (only for pp datas)
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
* `Aug 09, 2022` JSON Databases removed as suggested. We have compiled time solutions regarding to O2Physics (based on regex exp. and some string operations). TableMaker and DQEfficiency Workflows refactored for user friendliness. All things are discussed with Ionut.
* `Aug 10, 2022` path fix for writer configs. Transcation management added for Same Event Pairing and readme guide updated.
* `Aug 11, 2022` provide a native solution for libraries with urllib, cut and mcsignal lister added, helper messages has beauty format, for filter pp task, sels are fixed. readme update, added new script for internet based solution: `DownloadLibs.py`. Some parameter value names has refactored in DQ Efficiency, fix for dileptonTrack Selection DQ Efficiency task, fix for Same event pairing automation logger message (when you try give an process function in DQEfficiency or TableReader if you forget give a parameter value in e.g --analysis eventSelection --process JpsiToMuMu sameEventPairing value automaticaly added to analysis workflow like this (Logger Message: `"[WARNING] You forget to add sameEventPairing option to analysis for Workflow. It Automatically added by CLI."`) --> --analysis eventSelection sameEventPairing we provide this way with automation)
* `Aug 12, 2022` IFilterPP.py Interface refactored and released. `--cfgMuonsCuts` parameter added tablemaker and filterpp workflow (it's different from `--cfgMuonCuts`). listToString method impl to barrel and muon sels. Readme update for instructions and available configs in FilterPP python script.
* `Aug 13, 2022` In FilterPP, processEvTime and Tiny Options added to JSON files and python scripts, we need trans. manag for them, processDummy option added for run 3 Data in tablemaker, dummy automizer activated for dq muons selection. Protection Added to all scripts for alienv load. Transaction management protection added for cfgMuonSels and cfgBarrelSels in filterPP Task (TableMaker and FilterPP python scripts) also logger message and fix instructions added, forget to assign value to parameters transcation management carried to top of code, String to List method update, nargs fix for Sels in filter pp
* `Aug 14, 2022` `o2-analysis-mc-converter` `o2-analysis-fdd-converter` and `o2-analysis-track-propagation` task adders added to all Workflows as parameters. taskNameInConfig in dqflow is fixed. DQ Flow JSON configs fixed. `o2-analysis-track-propagation` dep removed and `o2-analysis-trackextension` added in DQ Flow as deps.
* `Aug 15, 2022` version based downloaded functionality added to DownloadLibs.py and fixed download functionality to DQ libs for all python scripts, unused comment lines deleted, metavar deleted from process function in filterpp for help messages, in filterepp `o2-analysis-trackextension` analysis task added as dep and removed `o2-analysis-track-propagation` as dep, because in before we add parameters for adding this additional tasks. filterpp tiny process selection fixed for transcation management, writer configs for dilepton analysis will bu updated, test configs added for local test, they will be removed. we should discussed some common tasks configs should deleted from json for using default params in DPL config. readme update for dqflow and others. SSL certificates added for download DQ libs due to github validation
* `Aug 17-18, 2022`  Logger Functionality implemented to O2DQWorkflows and DownloadLibs.py Some minimal fixes provided. Fix info message for centrality Table Transcation for pp. readme updated. Pretty print formatted implemented to O2DQWorkflows for helper messages (cut lister, MC signal lister and event mixing variables) lister. Interface updated for DownloadLibs.py script to get DQ libraries from local machine. All relevant Instructions have been added to the readme  
* `Aug 19-20, 2022` Temp DQ libs added to O2DQWorkflows for working LXPLUS and test. Because If you configure the DownloadLibs.py script locally, there is no problem when pulling libraries on the local machine and while it is completely stable, it has been added temporarily for some user acceptance tests because the libraries cannot be pulled locally in LXPLUS and it is not stable to download DQ libraries from github. argcomplete integrated to DownloadLibs.py, comment lines updated for functions, for important values, sub help messages added, default value viewer added to help messages, Interface predefined selections carried to top for readability, readme updated and helper message usage added to readme.
* `Aug 21, 2022` Choicer Completer Method integrated for pretty print display for auto completions, always_complete_options setted false for pretty print display with TAB, New ChoicesCompleterList Class Integrated to All Workflows for Getting choices nargs *, helper message updates in very detailed, all argparser groups has subgroups now, task adder help messages updated, some naming conventions setted for variables and code quality improved, not needed comments lines deleted for code quality, minimal fix for dqflow. Readme updated and Instructions for autocomplete added to readme, metavar explanations added to readme.
* `Aug 22, 2022` Helper Messages Updated. One minimal display bug added to readme. New interface development is ongoing with new JSON Configs.based on nightly-2022_08_23
* `Aug 23, 2022` AOD File checker fixed, Same Event Pairing process functionality fixed, centrality table fixed in new interface, new automated things provided.
* `Aug 24-26, 2022` All bugs are fixed. All functionalities provided, all scripts are tested by different users. Interface development is completed.