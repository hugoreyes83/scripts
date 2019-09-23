import json
import yaml
import ast
import argparse
import re
import logging
from functools import reduce
# from cerberus import Validator,SchemaError,DocumentError
from itertools import product

'''Setting up logging'''
LOG_FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format = LOG_FORMAT)

_lever_matching_pattern = r'[a-z]{3}[0-9]\-[0-9]+\-lv\-eng\-sw[0-9]+' #RE for matching lever boxes
_lbe_matching_pattern = r'[a-z]{3}[0-9]+\-br\-lbe\-[a-z][0-9]+\-r[1-9]\_?\d?'#RE for matching br-lbe devices
_catzilla_matching_pattern = r'[a-z]{3}[0-9]+\-br\-ctz\-f1b[0-9]+\-t1\-r[1-9]+'
_lbe_pattern = r'[a-z]{3}\-br\-lbe\-j[1-9]+\-r[0-9]'
_ctz_pattern = r'[a-z]{3}\-[1-9]+\-br\-ctz\-f[1-9]b[1-9]+\-t1\-r[1-9]'
_interface_pattern = r'^xe\-\d\/\d\/[0-9]+\:?[0-9]?'
_first_half_lever_stripe = [1,2,3,4]
_second_half_lever_stripe = [5,6,7,8]
_full_lever_rack = [1,2,3,4,5,6,7,8]
_valid_stripes = range(1,9)
_lever_stripe = [4,8]# A lever rack contains 8 boxes, which makes up two stripes, 4 boxes equals 1 stripe
_lever_neighbor = r'^[a-z{3}[1-9]+\-[1-9]+'
_lever_neighbor_rack_id = r'([0-9]+)0[0-9]+$'#RE for matching the rack id of a lever rack

banner = '''
 _                         __   __              _
| |    _____   _____ _ __  \ \ / /_ _ _ __ ___ | |
| |   / _ \ \ / / _ \ '__|  \ V / _` | '_ ` _ \| |
| |__|  __/\ V /  __/ |      | | (_| | | | | | | |
|_____\___| \_/ \___|_|      |_|\__,_|_| |_| |_|_|

__     __    _ _     _       _
\ \   / /_ _| (_) __| | __ _| |_ ___  _ __
 \ \ / / _` | | |/ _` |/ _` | __/ _ \| '__|
  \ V / (_| | | | (_| | (_| | || (_) | |
   \_/ \__,_|_|_|\__,_|\__,_|\__\___/|_|

'''

def get_parameters_from_cli():
    parser = argparse.ArgumentParser(description="Validate local lever site config file")
    parser.add_argument(
        "-f", "--file", action="store", required=True, help="the path of local site yaml file"
    )
    parser.add_argument(
        "-r", "--racks", action="store", required=True, help="racks to check on yaml file, e.g --racks 15,16,17,18"
    )
    return parser.parse_args()

class ReadError(Exception):
    pass

class StripeValueError(Exception):
    pass

class UnknownRack(Exception):
    pass

class Result():
    '''class object to store results'''
    def __init__(self):
        self.results = []

    def add_to_results(self,result):
        self.results.append(result)

class ObjectLbe(object):
    def __new__(cls,d,name):
        try:
            cls.name = name
            cls.breakout_positions = d['breakout_positions']
            cls.port_group = d['port_group']
            cls.positions = d['positions']
            cls.remote_edge_interfaces = d['remote_edge_interfaces']
            cls.interface_names = d['remote_edge_interfaces'][0]
            cls.stripes = d['stripes']
            instance = super(ObjectLbe, cls).__new__(cls)
            return instance
        except KeyError as e:
            logging.info('{} does not contain {}'.format(cls.name,e))
            return None

    def __init__(self,d,name):
        self.name = name
        self.breakout_positions = d['breakout_positions']
        self.port_group = d['port_group']
        self.positions = d['positions']
        self.remote_edge_interfaces = d['remote_edge_interfaces']
        self.interface_names = d['remote_edge_interfaces'][0]['interface_names']
        self.stripes = d['stripes']

    def validate_breakout(self):
        return self.breakout_positions == [1,2,3,4]

    def validate_port_group(self):
        return self.port_group == 'unsecured'

    def validate_unique_interfaces(self):
        return is_different(self.interface_names)

    def validate_positions(self):
        if not len(self.positions) == 1:
            return False
        if not isinstance(self.positions[0],int):
            return False
        else:
            return True

    def validate_remote_edge_interfaces(self):
        return len(self.interface_names) == len(self.breakout_positions)

    def validate_interfaces(self):
        return check_results(list(map(is_interface, self.interface_names)))

    def validate_unique_interfaces(self):
        return is_different(self.interface_names)

    def validate_stripes(self):
        if not len(self.stripes) == 1:
            logging.info('Stripe in {} can only contain one integer'.format(self.name))
            return False
        if not isinstance(self.stripes[0],int):
            return False
        if not self.stripes[0] in range(1,9):
            return False
        else:
            return True

    def run_all_checks(self):
        return self.validate_breakout(),\
               self.validate_port_group(),\
               self.validate_unique_interfaces(),\
               self.validate_positions(),\
               self.validate_remote_edge_interfaces(),\
               self.validate_interfaces(),\
               self.validate_stripes()

    def __str__(self):
        return self.name

class ObjectCtz(object):
    def __new__(cls,d,name):
        try:
            cls.name = name
            cls.breakout_positions = d['breakout_positions']
            cls.port_group = d['port_group']
            cls.positions = d['positions']
            cls.remote_edge_interfaces = d['remote_edge_interfaces']
            cls.interface_names = d['remote_edge_interfaces'][0]
            cls.stripes = d['stripes']
            instance = super(ObjectCtz, cls).__new__(cls)
            return instance
        except KeyError as e:
            logging.info('{} does not contain {}'.format(cls.name,e))
            return None

    def __init__(self,d,name):
        self.name = name
        self.breakout_positions = d['breakout_positions']
        self.port_group = d['port_group']
        self.positions = d['positions']
        self.remote_edge_interfaces = d['remote_edge_interfaces']
        self.interface_names = d['remote_edge_interfaces'][0]['interface_names']
        self.stripes = d['stripes']

    def validate_breakout_positions(self):
        return self.breakout_positions == [1,2,3,4]

    def validate_port_group(self):
        return self.port_group == 'unsecured'

    def validate_unique_interfaces(self):
        return is_different(self.interface_names)

    def validate_positions(self):
        return (self.positions == len(set(self.interface_names)))//len(self.breakout_positions)

    def validate_remote_edge_interfaces(self):
        return self.positions == self.interface_names//len(self.breakout_positions)

    def validate_interfaces(self):
        return check_results(list(map(is_interface, self.interface_names)))

    def validate_stripes(self):
        if not isinstance(self.stripes[0],int):
            return False
        elif not len(self.stripes) == 1:
            logging.info('Stripe in {} can only contain one integer'.format(self.name))
            return False
        elif not self.stripes[0] in range(1,9):
            return False
        else:
            return True

    def run_all_checks(self):
        return self.validate_breakout_positions(),\
               self.validate_port_group(),\
               self.validate_unique_interfaces(),\
               self.validate_positions(),\
               self.validate_remote_edge_interfaces(),\
               self.validate_interfaces(),\
               self.validate_stripes()

    def __str__(self):
        return self.name

class ObjectLever(object):
    def __new__(cls,d,name):
        try:
            cls.name = name
            cls.port_group = d['port_group']
            cls.stripes = d['stripes']
            instance = super(ObjectLever, cls).__new__(cls)
            return instance
        except KeyError as e:
            logging.info('{} does not contain {}'.format(cls.name,e))
            return None

    def __init__(self,d,name):
        self.name = name
        self. port_group = d['port_group']
        self.stripes = d['stripes']

    def validate_port_group(self):
        return self.port_group == 'secured'

    def is_valid_lever(self):
        return bool(re.search(_lever_matching_pattern,self.name))

    def validate_stripes(self):
        if not isinstance(self.stripes[0],int):
            return False
        elif not len(self.stripes) == 1:
            logging.info('Stripe in {} can only contain one integer'.format(self.name))
            return False
        elif not self.stripes[0] in range(1,9):
            return False
        else:
            return True

    def run_all_checks(self):
        return self.validate_port_group(),\
               self.validate_stripes(),\
               self.is_valid_lever()

    def __str__(self):
        return self.name

class ObjectRack(object):
    def __init__(self,rack):
        self.rack = rack

def generate_rack_object(d):
    dict_of_rack_objects = {}
    for rack in d['racks']:
        dict_of_rack_objects[rack] = ObjectRack(rack)
        for item in d.get('racks').get(rack):
            dict_of_rack_objects[rack]['os_stage'] = d.get('racks').get(rack).get(item)

    return dict_of_rack_objects

def is_lever(device):
    '''returns True is device is an lever box'''
    return bool(re.search(_lever_matching_pattern, device))

def is_lbe(device):
    '''returns True is device is an lbe router'''
    return bool(re.search(_lbe_matching_pattern, device))

def is_ctz(device):
    '''returns True if device is a catzilla router'''
    return bool(re.search(_catzilla_matching_pattern, device))

def is_valid_lever(device):
    return bool(re.search(r'[0-8]$',device))

def is_same(lst):
    return len(set(lst)) == 1

def is_interface(i):
    return bool(re.match(_interface_pattern,i))

def is_same_lever_rack(list_lever_boxes_in_rack):
    return is_same(map(get_site_from_lever_rack, list_lever_boxes_in_rack))

def is_lever_rack_two_stripes(list_lever_boxes_in_rack):
    return is_two_racks(map(get_site_from_lever_rack, list_lever_boxes_in_rack))

def get_site_from_lever_rack(lever_router):
    return re.search(_lever_neighbor,lever_router).group()

def check_results(lst_results):
    #make sure lst_results is a list
    assert type(lst_results) is list, 'Results is not list'
    #check lst_results is not an empty list
    assert lst_results, 'Results list is empty'
    for i in lst_results:
        if int(i) == 1:
            continue
        elif int(i) == 0:
            return False
    return True

def is_different(l):
    seen = set()
    for item in l:
        if item in seen:
            return False
        seen.add(item)
    return True

def open_file(input_file,formatting):
    '''function to open file, results depends if file is json as opposed to yaml'''
    try:
        if formatting == 'yaml':
            logging.info('Trying to open "{}"'.format(input_file))
            with open(input_file) as f:
                return yaml.safe_load(f)
        elif formatting == 'json':
            logging.info('Trying to open Json Schema File "{}"'.format(input_file))
            with open(input_file) as f:
                return ast.literal_eval(f.read())
        else:
            raise OpenFailed('Unknown format to open {}'.format(input_file))
    except:
        raise OpenFailed('Could not open {}'.format(input_file))

def generate_device_objects(y_data,rack):
    dict_of_device_objects = {}
    dict_of_device_objects[rack] = {}
    for device in y_data['racks'][rack]['neighbors']:
        if is_lever(device) and device not in dict_of_device_objects[rack].keys():
            dict_of_device_objects[rack][device] = ObjectLever(y_data['racks'][rack]['neighbors'][device],device)
        elif is_ctz(device) and device not in dict_of_device_objects[rack].keys():
            dict_of_device_objects[rack][device] = ObjectCtz(y_data['racks'][rack]['neighbors'][device],device)
        elif is_lbe(device) and device not in dict_of_device_objects[rack].keys():
            dict_of_device_objects[rack][device] = ObjectLbe(y_data['racks'][rack]['neighbors'][device],device)
    return dict_of_device_objects

def filter_lever_per_rack(rack_dict,r_name):
    dict_lever_per_rack = {}
    dict_lever_per_rack[r_name] = {}
    for device in rack_dict:
        if 'lv-eng' in device and device not in dict_lever_per_rack[r_name]:
            dict_lever_per_rack[r_name][device] = rack_dict[device]['stripes'][0]
    return dict_lever_per_rack

def filter_lbe_per_rack(rack_dict,r_name):
    dict_lbe_per_rack = {}
    dict_lbe_per_rack[r_name] = {}
    for device in rack_dict:
        if 'br-lbe' in device and device not in dict_lbe_per_rack[r_name]:
            dict_lbe_per_rack[r_name][device] = rack_dict[device]['stripes'][0]
    return dict_lbe_per_rack

def filter_ctz_per_rack(rack_dict,r_name):
    dict_ctz_per_rack = {}
    dict_ctz_per_rack[r_name] = {}
    for device in rack_dict:
        if 'br-ctz' in device and device not in dict_ctz_per_rack[r_name]:
            dict_ctz_per_rack[r_name][device] = rack_dict[device]['stripes'][0]
    return dict_ctz_per_rack

def validate_stripes_per_lbe_rack(rack_dict,r_name):
    list_of_detected_lbe_stripes = []
    list_of_detected_lever_stripes = []
    get_lever_router_per_rack = filter_lever_per_rack(rack_dict,r_name)
    for device in rack_dict:
        list_of_detected_lbe_stripes.append(rack_dict[device]['stripes'][0])
    for lever in get_lever_router_per_rack[r_name]:
        list_of_detected_lever_stripes.append(get_lever_router_per_rack[r_name][lever])
    # logging.info('{} - {}'.format(list(set(list_of_detected_lbe_stripes)),list_of_detected_lever_stripes))
    return list(set(list_of_detected_lbe_stripes)) == sorted(list_of_detected_lever_stripes)

def validate_stripes_per_ctz_rack(rack_dict,r_name):
    list_of_detected_ctz_stripes = []
    list_of_detected_lever_stripes = []
    get_lever_router_per_rack = filter_lever_per_rack(rack_dict,r_name)
    for device in rack_dict:
        list_of_detected_ctz_stripes.append(rack_dict['neighbors'][device]['stripes'][0])
    for lever in get_lever_router_per_rack[r_name]:
        list_of_detected_lever_stripes.append(get_lever_router_per_rack[r_name][lever])
    return list(set(list_of_detected_ctz_stripes)) == sorted(list_of_detected_lever_stripes)

def get_stripes_ctz_rack(rack_dict,r_name):
    racks_into_stripes = {}
    racks_into_stripes[r_name] = {}
    racks_into_stripes[r_name]['first_stripe'] = []
    racks_into_stripes[r_name]['second_stripe'] = []
    for device in rack_dict:
        if is_ctz(device) and rack_dict[device]['stripes'][0] in _first_half_lever_stripe:
            racks_into_stripes[r_name]['first_stripe'].append(len(rack_dict[device]['positions']))
        elif is_ctz(device) and rack_dict[device]['stripes'][0] in _second_half_lever_stripe:
            racks_into_stripes[r_name]['second_stripe'].append(len(rack_dict[device]['positions']))
    return racks_into_stripes

def get_stripes_lbe_rack(rack_dict,r_name):
    racks_into_stripes = {}
    racks_into_stripes[r_name] = {}
    racks_into_stripes[r_name]['first_stripe'] = []
    racks_into_stripes[r_name]['second_stripe'] = []
    for device in rack_dict:
        if is_lbe(device) and rack_dict[device]['stripes'][0] in _first_half_lever_stripe:
            racks_into_stripes[r_name]['first_stripe'].append(device)
        elif is_lbe(device) and rack_dict[device]['stripes'][0] in _second_half_lever_stripe:
            racks_into_stripes[r_name]['second_stripe'].append(device)
    return racks_into_stripes

def compare_stripes_across_lbe_to_ctz(local_rack_dict,remote_rack_dict,local_rack,remote_rack):
    ctz_stripes = get_stripes_ctz_rack(remote_rack_dict,remote_rack)
    lbe_stripes = get_stripes_lbe_rack(local_rack_dict,local_rack)
    if is_half_or_full_lever_rack(local_rack_dict,local_rack) == 'Full':
        available_stripes = ['first_stripe','second_stripe']
    elif is_half_or_full_lever_rack(local_rack_dict,local_rack) == 'Half':
        available_stripes = ['first_stripe']
    else:
        return False
    results_compare_stripes = Result()
    logging.info('Comparing {} to {}'.format(local_rack,remote_rack))
    for stripe in available_stripes:
        logging.info('lbe {} {} positions / ctz {} {} positions'.format\
        	(stripe,len(lbe_stripes[local_rack][stripe]),stripe,sum(ctz_stripes[remote_rack][stripe])))
        results_compare_stripes.add_to_results\
        (len(lbe_stripes[local_rack][stripe]) == sum(ctz_stripes[remote_rack][stripe]))
    return check_results(results_compare_stripes.results)

def compare_stripes_across_ctz_to_lbe(local_rack_dict,remote_rack_dict,local_rack,remote_rack):
    ctz_stripes = get_stripes_ctz_rack(local_rack_dict,local_rack)
    print(ctz_stripes)
    lbe_stripes = get_stripes_lbe_rack(remote_rack_dict,remote_rack)
    if is_half_or_full_lever_rack(local_rack_dict,local_rack) == 'Full':
        available_stripes = ['first_stripe','second_stripe']
    elif is_half_or_full_lever_rack(local_rack_dict,local_rack) == 'Half':
        available_stripes = ['first_stripe']
    else:
        return False
    results_compare_stripes = Result()
    logging.info('Comparing {} to {}'.format(local_rack,remote_rack))
    for stripe in available_stripes:
        logging.info('lbe {} {} positions / ctz {} {} positions'.format\
        	(stripe,len(lbe_stripes[remote_rack][stripe]),stripe,sum(ctz_stripes[local_rack][stripe])))
        results_compare_stripes.add_to_results\
        (len(lbe_stripes[remote_rack][stripe]) == sum(ctz_stripes[local_rack][stripe]))
    return check_results(results_compare_stripes.results)

def is_half_or_full_lever_rack(rack_dict,r_name):
    list_of_detected_lever_stripes = []
    get_lever_router_per_rack = filter_lever_per_rack(rack_dict,r_name)
    for lever in get_lever_router_per_rack[r_name]:
        list_of_detected_lever_stripes.append(get_lever_router_per_rack[r_name][lever])
    if len(list_of_detected_lever_stripes) == 4 and list_of_detected_lever_stripes\
         == _first_half_lever_stripe or list_of_detected_lever_stripes \
         == _second_half_lever_stripe:
        return 'Half'
    elif len(list_of_detected_lever_stripes) == 8 and sorted(list_of_detected_lever_stripes) == _full_lever_rack:
        return 'Full'
    else:
        return None

def validate_number_of_lever_racks(yamldict):
    #make sure there is at least one rack in yaml fle
    assert yamldict.get('racks'),'Racks dictionary cannot be empty'
    racks = [i for i in yamldict.get('racks',None)]
    rack_results = Result()
    for rack in racks:
        logging.info('Validating Lever Racks defined inside {}...'.format(rack))
        assert yamldict.get('racks').get(rack).get('neighbors'),'Neighbors dictionary cannot be empty'
        rack_results.add_to_results(check_lever_rack(yamldict.get('racks').get(rack).get('neighbors',None)))
        #rack_results.add_to_results(validate_lever_rack(yaml['racks'][rack]['neighbors']))
        logging.info('Checks {} on {}'.format('PASSED' \
        	if check_lever_rack(yamldict.get('racks').get(rack).get('neighbors',None)) else 'FAILED',rack))
    return check_results(rack_results.results)

def validate_neighbors(yamldict):
    '''function to validate that neighbors listed in racks dictionary are also to be found inside the main neighbors dictionary'''
    assert yamldict.get('neighbors'),'Neighbors dictionary cannot be empty'
    list_of_neighbors = []
    neighbors_results = Result()
    neighbors_dict = yamldict.get('neighbors',None)
    list_of_devices_separated_per_rack = separate_devices_from_rack(yamldict)
    for rack in list_of_devices_separated_per_rack:
        logging.info('Validating neighbors in {} exist in Neighbors Dictionary'.format(rack))
        list_of_neighbors_per_rack = list_of_devices_separated_per_rack[rack]
        neighbors_results.add_to_results(check_rack_neighbors_in_neighbors(neighbors_dict, list_of_neighbors_per_rack))
        logging.info('Neighbor Check in {} {}'.format(rack, 'PASSED' \
        	if check_rack_neighbors_in_neighbors(neighbors_dict, list_of_neighbors_per_rack) else 'FAILED'))
        list_of_neighbors += list_of_neighbors_per_rack
    logging.info('Validating that Neighbors exist in Racks Dictionaries')
    neighbors_results.add_to_results(check_neighbors_in_rack_neighbors(neighbors_dict, list_of_neighbors))
    logging.info('Neighbors Check {}'.format('PASSED' \
    	if check_neighbors_in_rack_neighbors(neighbors_dict, list_of_neighbors) else 'FAILED'))
    return check_results(neighbors_results.results)

def check_structure_yaml(yaml,schema):
    try:
        validate_file = Validator(schema)
        validate_file.validate(yaml)
        if not validate_file.errors:
            return True
        else:
            return False

    except DocumentError as e:
        print(e)

    except SchemaError as e:
        print(e)

    except ValidationFailed as e:
        print(e)

def validate_provided_racks_exists_in_yaml(input_racks,input_yaml_file):
    for rack in input_racks:
        if rack not in input_yaml_file.get('racks'):
            logging.info('{} does not exist in yaml file'.format(rack))
            return False
    return True

def check_lever_rack(rack):
    '''function to check if at least one stripe is listed, values can be either 4(half stripe) or 8(full stripe)'''
    lever_boxes_in_rack = [lever_box for lever_box in rack if is_lever(lever_box)]
    all_lever = check_results(list(map(is_lever, lever_boxes_in_rack)))
    valid_lever = check_results(list(map(is_valid_lever, lever_boxes_in_rack)))#a valid lever box should end in a number between 1 and 8
    valid_number_of_lever = len(set(lever_boxes_in_rack)) in _lever_stripe
    if all_lever and valid_lever and valid_number_of_lever:#if this is true, that means all lever boxes in list are actually lever boxes(passed re check)
        return True
    else:
        return False

def separate_devices_from_rack(yamldict):
    '''A yaml file can contain a combination of lever racks with br-lbe or lever racks with -br-ctz so \
     this function is to tell racks apart as they both need different set of checks to be run'''
    dict_devices_per_rack = {}
    for rack in yamldict.get('racks'):
        for device in yamldict.get('racks').get(rack).get('neighbors',None):
            # match_lever_pattern = re.search(_lever_matching_pattern,device)
            # if not match_lever_pattern:
            if rack in dict_devices_per_rack.keys():
                dict_devices_per_rack[rack].append(device)
            else:
                dict_devices_per_rack[rack] = []
                dict_devices_per_rack[rack].append(device)
    return dict_devices_per_rack

def check_rack_neighbors_in_neighbors(neighbors_dict,list_of_neighbors_per_rack):
    list_of_results = Result()
    for neighbor in list_of_neighbors_per_rack:
        list_of_results.add_to_results(neighbor in neighbors_dict)
    return check_results(list_of_results.results)

def check_neighbors_in_rack_neighbors(neighbors_dict,list_of_neighbors):
    list_of_neighbors_results = Result()
    for neighbor in neighbors_dict:
        list_of_neighbors_results.add_to_results(neighbor in list_of_neighbors)
    return check_results(list_of_neighbors_results.results)

def find_all_lever_files_and_racks(dict_lever_devices_only):
    '''this funtion returns a dictionary that contains each rack and its corresponding remote file and remote rack'''
    if not dict_lever_devices_only:
        return False
    dict_remote_lever_yaml_per_rack = {}
    for rack in dict_lever_devices_only:
        dict_remote_lever_yaml_per_rack[rack] = {}
        dict_remote_lever_yaml_per_rack[rack]['remote_file'] = {}
        dict_remote_lever_yaml_per_rack[rack]['remote_rack'] = {}
        if is_same_lever_rack(dict_lever_devices_only.get(rack)):
            for device in dict_lever_devices_only.get(rack,None):
                other_yaml_lever_file = '{}{}'.format(re.match(_lever_neighbor,device).group(),'-lv-eng.yaml')
                id_lever_rack = '{}{}'.format('rack',str(re.search(_lever_neighbor_rack_id, device).groups()[0]))
                if not other_yaml_lever_file in dict_remote_lever_yaml_per_rack.get(rack,None).get('remote_file',None):
                    dict_remote_lever_yaml_per_rack[rack]['remote_file'] = '{}'.format(other_yaml_lever_file)
                    dict_remote_lever_yaml_per_rack[rack]['remote_rack'] = '{}'.format(id_lever_rack)
        elif is_lever_rack_two_stripes(dict_lever_devices_only.get(rack)):#lever rack connects to two different sites
            dict_remote_lever_yaml_per_rack[rack]['remote_file'] = []
            dict_remote_lever_yaml_per_rack[rack]['remote_rack'] = []
            for site_id in dict_lever_devices_only.get(rack,None):
                other_yaml_lever_file = '{}{}'.format(re.match(_lever_neighbor,site_id).group(),'-lv-eng.yaml')
                id_lever_rack = '{}{}'.format('rack',str(re.search(_lever_neighbor_rack_id, site_id).groups()[0]))
                if not other_yaml_lever_file in dict_remote_lever_yaml_per_rack.get(rack,None).get('remote_file',None):
                    dict_remote_lever_yaml_per_rack[rack]['remote_file'].append('{}'.format(other_yaml_lever_file))
                    dict_remote_lever_yaml_per_rack[rack]['remote_rack'].append('{}'.format(id_lever_rack))
        else:
            raise StripingError('A lever rack can only connect to up to two different racks')
    return dict_remote_lever_yaml_per_rack

def lever_devices_only(yamldict,rack):
    '''funtion to extract all devices from the racks dictionaries'''
    dict_lever_devices_only = {}
    for device in yamldict.get('racks').get(rack).get('neighbors',None):
        if rack in dict_lever_devices_only.keys() and is_lever(device):
            dict_lever_devices_only[rack].append(device)
        elif is_lever(device):
            dict_lever_devices_only[rack] = []
            dict_lever_devices_only[rack].append(device)
    return dict_lever_devices_only

def extract_lbe_or_catzilla(yamldict,rack):
    '''A yaml file can contain a combination of lever racks with br-lbe or lever racks with -br-ctz so \
     this function is to tell racks apart as they both need different set of checks to be run'''
    dict_devices_lbe_or_catzilla= {}
    for device in yamldict.get('racks').get(rack).get('neighbors',None):
        match_lever_pattern = re.search(_lever_matching_pattern,device)
        if not match_lever_pattern:
            if rack in dict_devices_lbe_or_catzilla.keys():
                dict_devices_lbe_or_catzilla[rack].append(device)
            else:
                dict_devices_lbe_or_catzilla[rack] = []
                dict_devices_lbe_or_catzilla[rack].append(device)
    return dict_devices_lbe_or_catzilla

def is_lbe_or_catzilla(dict_devices_per_rack):
    '''this function defines what tests to run on a per rack basis'''
    assert dict_devices_per_rack,'dict_devices_per_rack is empty'
    dict_checks = {}
    for rack in dict_devices_per_rack:
        if check_results(list(map(is_lbe,dict_devices_per_rack[rack]))):
            dict_checks[rack] = 'lbe'
        elif check_results(list(map(is_ctz,dict_devices_per_rack[rack]))):
            dict_checks[rack] = 'ctz'
    return dict_checks

def main():
    print(banner)
    get_inputs = get_parameters_from_cli()
    input_yaml_file = open_file(get_inputs.file,'yaml')
    # input_schema_file = open_file('lib/schema.json','json')
    local_racks = ['rack'+rack_id for rack_id in get_inputs.racks.split(',')]
    #make sure provided racks actually exists in yaml file
    if not validate_provided_racks_exists_in_yaml(local_racks,input_yaml_file):
        raise UnknownRack('One or more provided racks do not exist in yaml file, cannot proceed')
    #run initial_checks on  yaml
    final_results = Result()
    # if check_structure_yaml(input_yaml_file,input_schema_file):
        # logging.info('Structure yaml check on {} {}'.format(get_inputs.file,'PASSED'))
        # final_results.add_to_results(check_structure_yaml(input_yaml_file,input_schema_file))
    # else:
        # logging.info('Structure yaml check on {} {}'.format(get_inputs.file,'FAILED'))
        # final_results.add_to_results(check_structure_yaml(input_yaml_file,input_schema_file))
    checks_to_run = {
                     'check1':validate_number_of_lever_racks,
                     'check2':validate_neighbors
                     }
    # run rest of the checks
    for check in checks_to_run:
        final_results.add_to_results(checks_to_run[check](input_yaml_file))
    #generate local device objects
    for rack in local_racks:
        local_rack_objects = generate_device_objects(input_yaml_file,rack)
        # print(local_rack_objects)
        for device in local_rack_objects[rack]:
            logging.info('Running checks on devices found in {}'.format(rack))
            logging.info('Checks on  {} {}'.format(device, 'PASSED' \
            	if check_results(list(local_rack_objects[rack][device].run_all_checks())) else 'FAILED'))
            final_results.add_to_results(check_results(list(local_rack_objects[rack][device].run_all_checks())))
    #below are checks on remote rack
    logging.info('Found the following remote racks')
    for rack in local_racks:
        get_remote_racks = find_all_lever_files_and_racks(lever_devices_only(input_yaml_file,rack))#TODO
        remote_lever_rack_dict = open_file(get_remote_racks[rack]['remote_file'],'yaml')['racks'][get_remote_racks[rack]['remote_rack']]['neighbors']
        remote_lever_rack = get_remote_racks[rack]['remote_rack']
        local_lever_rack = input_yaml_file['racks'][rack]['neighbors']
        # print(get_remote_racks)
        logging.info('{} in {}'.format(get_remote_racks[rack]['remote_rack'],get_remote_racks[rack]['remote_file']))
        run_is_lbe_or_catzilla_remote_rack = is_lbe_or_catzilla(extract_lbe_or_catzilla\
        	(open_file(get_remote_racks[rack]['remote_file'],'yaml'),get_remote_racks[rack]['remote_rack']))
        # print(run_is_lbe_or_catzilla_remote_rack[get_remote_racks[rack]['remote_rack']])
        if run_is_lbe_or_catzilla_remote_rack.get(get_remote_racks[rack]['remote_rack']) == 'lbe':
            #compare_stripes_across_ctz_to_lbe
            compare_stripes_across_ctz_to_lbe(local_lever_rack,remote_lever_rack_dict,rack,remote_lever_rack)
        elif run_is_lbe_or_catzilla_remote_rack.get(get_remote_racks[rack]['remote_rack']) == 'ctz':
            #compare_stripes_across_lbe_to_ctz
            compare_stripes_across_lbe_to_ctz(local_lever_rack,remote_lever_rack_dict,rack,remote_lever_rack)
    logging.info('All tests have been completed. Below are the final result:')
    # print(final_results.results)
    logging.info('Final Result ===== {}'.format('PASSED' if check_results(final_results.results) else 'FAILED'))
if __name__ == '__main__':
    main()