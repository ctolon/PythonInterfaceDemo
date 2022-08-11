import urllib.request
import os
import sys

#############################################################################
##  © Copyright CERN 2018. All rights not expressly granted are reserved.  ##
##                   author:cevat.batuhan.tolon@.cern.ch                   ##
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

# This script provides download to libraries from O2Physics-DQ Manually

urlCutsLibrary = 'https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/CutsLibrary.h'
urlMCSignalsLibrary ='https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/MCSignalLibrary.h'
urlEventMixing ='https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/MixingLibrary.h'

urllib.request.urlretrieve(urlCutsLibrary,"tempCutsLibrary.h")
urllib.request.urlretrieve(urlMCSignalsLibrary,"tempMCSignalsLibrary.h")
urllib.request.urlretrieve(urlEventMixing,"tempMixingLibrary.h")

print("[INFO] Libraries downloaded successfully!")
sys.exit()