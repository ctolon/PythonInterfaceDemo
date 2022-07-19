import json
import sys
import logging
from ast import parse
import os
import argparse
def json_load(args, logger):
    """
    Load JSON file into object (args)
    :param args: args object from arg parser "
    :param logger: logger handler
    :return: None (args object is updated)
    """
    logger = logging.getLogger()
    
    # Setting the threshold of logger to DEBUG
    #logger.setLevel(logging.DEBUG)
 
    # Test messages
    #logger.debug("Harmless debug Message")
    #logger.info("Just an information")
    #logger.warning("Its a Warning")
    #logger.error("Did you try to divide by zero")
    #logger.critical("Internet is down")
    
    
    json_file_dict = args.json_file
    json_keys = args.json_keys
    logger.info("Processing file %s" % json_file_dict)
    if not json_keys:
        logger.error('--json_load : no keys specified in line for file %s ' % json_file_dict)
        sys.exit(1)
    try:
        json_dict = json.load(open(json_file_dict))
    except FileNotFoundError:
        logger.error('--json_load : file not found %s ' % json_file_dict)
        sys.exit(1)
    for json_key in json_keys:
        logger.info("Processing key %s" % json_key)
        if json_key not in json_dict:
            logger.error('Key %s does not exist in %s' % (json_key, json_file_dict))
            logger.error('Valid keys are :%s ' % (','.join(json_dict)))
            sys.exit(1)
        vars(args).update(json_dict[json_key])
        
print("PROGRAM WORKS!")

json_dict = json.load(open('data.json'))

#print(json_dict)

program_name = os.path.basename(sys.argv[0])
parser = argparse.ArgumentParser(prog=program_name, description='Generate a mini-synthesis script')
parser.add_argument('--in_list', help='File list by write RTL command', default='in.vhdl')
#parser.add_argument('--top_module', help='Top module', required=True)
#parser.add_argument('--out_script', help='Output synthesis script', required=True)
args = parser.parse_args()

with open(args.in_list, 'w') as wfh:
    print(wfh)


#json_load(args,logger="")