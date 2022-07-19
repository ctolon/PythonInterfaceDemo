import json
import sys
import logging
from ast import parse
import os
import argparse

parser = argparse.ArgumentParser(description='Arguments to pass')

parser.add_argument('--cfgPairCuts', help="Add track propagation to the innermost layer (TPC or ITS)", action="store", type=str)
extrargs = parser.parse_args()

#Open JSON File
json_dict = json.load(open('data.json'))

json_dict_new = json_dict


def get_key(json_dict_new):
    for key, value in json_dict_new.items():
        #print("key List = ", key)
        #print("value List = ", value)
        #print(type(value))
        if type(value) == type(json_dict):
            #print(value, type(value))
            for value, value2 in value.items():
                #print(value)
                if extrargs.cfgPairCuts and value =='cfgPairCuts':
                   print(extrargs.cfgPairCuts)
                   print(value2)

                   #print(value,":",value2)
                   #print(value2)
get_key(json_dict_new)