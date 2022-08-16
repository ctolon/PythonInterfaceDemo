import urllib.request
from urllib.request import Request, urlopen
import os
import sys
import json
from ast import parse
import argparse
import re
import ssl

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

# This script provides download to libraries from O2Physics-DQ Manually with/without Production tag

# header for github download
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

parser = argparse.ArgumentParser(description='Arguments to pass')
parser.add_argument('--version', help="Your Production tag for O2Physics example: for nightly-20220619, just enter as 20220619", action="store", type=str.lower)
parser.add_argument('--debug', help="execute with debug options", action="store_true")

extrargs = parser.parse_args()

MYPATH = os.path.abspath(os.getcwd())
#print(MYPATH)

if extrargs.version != None:
    prefix_version = "nightly-"
    extrargs.version = prefix_version + extrargs.version

urlCutsLibrary = 'https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/CutsLibrary.h'
urlMCSignalsLibrary ='https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/MCSignalLibrary.h'
urlEventMixing ='https://raw.githubusercontent.com/AliceO2Group/O2Physics/master/PWGDQ/Core/MixingLibrary.h'

if extrargs.version:
    print("[INFO] Your Version For Downloading DQ Libs From Github :", extrargs.version)
    urlCutsLibrary = 'https://raw.githubusercontent.com/AliceO2Group/O2Physics/' + extrargs.version + '/PWGDQ/Core/CutsLibrary.h'
    urlMCSignalsLibrary ='https://raw.githubusercontent.com/AliceO2Group/O2Physics/' + extrargs.version + '/PWGDQ/Core/MCSignalLibrary.h'
    urlEventMixing ='https://raw.githubusercontent.com/AliceO2Group/O2Physics/' + extrargs.version + '/PWGDQ/Core/MixingLibrary.h'
    
if extrargs.debug:
    print("CutsLibrary.h Path: ",urlCutsLibrary)
    print("MCSignalsLibrary.h Path: ",urlMCSignalsLibrary)
    print("MixingLibrary.h Path: ",urlEventMixing)
 
    
if (os.path.isfile('tempCutsLibrary.h') == False) or (os.path.isfile('tempMCSignalsLibrary.h') == False) or (os.path.isfile('tempMixingLibrary.h')) == False:
    print("[INFO] Some Libs are Missing. All DQ libs will download")
    if extrargs.debug:
        try:
            context = ssl._create_unverified_context()  # prevent ssl problems
            request = urllib.request.urlopen(urlCutsLibrary, context=context)
            request = urllib.request.urlopen(urlMCSignalsLibrary, context=context)
            request = urllib.request.urlopen(urlEventMixing, context=context)
        except urllib.error.HTTPError as error:
            print(error)
    else:
        # Dummy SSL Adder
        context = ssl._create_unverified_context()  # prevent ssl problems
        request = urllib.request.urlopen(urlCutsLibrary, context=context)
    
    # HTTP Request
    requestCutsLibrary = Request(urlCutsLibrary, headers=headers)
    requestMCSignalsLibrary = Request(urlMCSignalsLibrary, headers=headers)
    requestEventMixing  = Request(urlEventMixing , headers=headers)
    
    # Get Files With Http Requests
    htmlCutsLibrary = urlopen(requestCutsLibrary, context=context).read()
    htmlMCSignalsLibrary = urlopen(requestMCSignalsLibrary, context=context).read()
    htmlEventMixing = urlopen(requestEventMixing, context=context).read()
     
    with open('tempCutsLibrary.h', 'wb') as f:
         f.write(htmlCutsLibrary)
    with open('tempMCSignalsLibrary.h', 'wb') as f:
         f.write(htmlMCSignalsLibrary)
    with open('tempMixingLibrary.h', 'wb') as f:
        f.write(htmlEventMixing)
    

print("[INFO] Libraries downloaded successfully!")
sys.exit()