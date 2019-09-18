import json
import yaml
import argparse
import re

_lever_pattern = r'[a-z]{3}[1-9]\-[1-9]+\-lv\-eng\-sw[0-9]+'
_lbe_pattern = r'[a-z]{3}\-br\-lbe\-j[1-9]+\-r[0-9]'
_ctz_pattern = r'[a-z]{3}\-[1-9]+\-br\-ctz\-f[1-9]b[1-9]+\-t1\-r[1-9]'
_interface_pattern = r'^xe\-\d\/\d\/[0-9]+\:?[0-9]?'
def parse_args():
    #setting up argparser
    parser = argparse.ArgumentParser(description='tool')
    parser.add_argument('--file',required=True, help='enter local yaml file')
    args = parser.parse_args()
    return args

class ReadError(Exception):
    pass

class StripeValueError(Exception):
    pass

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
            print('{} does not contain {}'.format(cls.name,e))
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
        return check_results(map(is_interface, self.interface_names))

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
               self.validate_positions(),\
               self.validate_remote_edge_interfaces(),\
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
            print('{} does not contain {}'.format(cls.name,e))
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
        return check_results(map(is_interface, self.interface_names))

    def validate_stripes(self):
        if not isinstance(self.stripes[0],int):
            return False
        elif not len(self.stripes) == 1:
            logging.info('Stripe in {} can only contain one integer'.format(self.name))
            return False
        elif not self.stripes[0] in range(1,9):
            return False
        else:
            return False
    
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
            print('{} does not contain {}'.format(cls.name,e))
            return None

    def __init__(self,d,name):
        self.name = name
        self. port_group = d['port_group']
        self.stripes = d['stripes']

    def validate_port_group(self):
        return self.port_group == 'secured'

    def is_valid_lever(self):
    	return bool(re.search(_lever_pattern,self.name))

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

def is_lever(d):
    return 'lv-eng' in d

def is_ctz(d):
    return 'br-ctz' in d

def is_lbe(d):
    return 'br-lbe' in d

def is_interface(i):
    return bool(re.match(_interface_pattern,i))

def is_different(l):
    seen = set()
    for item in l:
        if item in seen:
            return False
        seen.add(item)
    return True

def open_file(f):
    try:
        with open(f) as f:
            f_read = yaml.safe_load(f)
            return f_read
    except:
        raise ReadError('File cound not be read')

def generate_device_objects(y_data):
    dict_of_device_objects = {}
    for rack in y_data['racks']:
        dict_of_device_objects[rack] = {}
        for device in y_data['racks'][rack]['neighbors']:
            if is_lever(device) and device not in dict_of_device_objects[rack].keys():
                dict_of_device_objects[rack][device] = ObjectLever(y_data['racks'][rack]['neighbors'][device],device)
            elif is_ctz(device) and device not in dict_of_device_objects[rack].keys():
                dict_of_device_objects[rack][device] = ObjectCtz(y_data['racks'][rack]['neighbors'][device],device)
            elif is_lbe(device) and device not in dict_of_device_objects[rack].keys():
                dict_of_device_objects[rack][device] = ObjectLbe(y_data['racks'][rack]['neighbors'][device],device)
    return dict_of_device_objects

def filter_lever_per_rack(rack,r_name):
	dict_lever_per_rack = {}
	dict_lever_per_rack[r_name] = {}
	for device in rack:
		if 'lv-eng' in device and device not in dict_lever_per_rack[r_name]:
			dict_lever_per_rack[r_name][device] = rack[device]['stripes']
	return dict_lever_per_rack

def filter_lbe_per_rack(rack,r_name):
	dict_lbe_per_rack = {}
	dict_lbe_per_rack[r_name] = {}
	for device in rack:
		if 'br-lbe' in device and device not in dict_lbe_per_rack[r_name]:
			dict_lbe_per_rack[r_name][device] = rack[device]['stripes']
	return dict_lbe_per_rack

def filter_ctz_per_rack(rack,r_name):
	dict_ctz_per_rack = {}
	dict_ctz_per_rack[r_name] = {}
	for device in rack:
		if 'br-ctz' in device and device not in dict_ctz_per_rack[r_name]:
			dict_ctz_per_rack[r_name][device] = rack[device]['stripes']
	return dict_ctz_per_rack

def main():
    get_args = parse_args()
    open_yaml_file = open_file(get_args.file)
    run_generate_device_objects = generate_device_objects(open_yaml_file)
    for rack in run_generate_device_objects:
        for device in run_generate_device_objects[rack]:
            if is_lbe(device):
                print('{}-{}'.format(device,run_generate_device_objects[rack][device].run_all_checks()))
            elif is_ctz(device):
                print('{}-{}'.format(device,run_generate_device_objects[rack][device].run_all_checks()))
            elif is_lever(device):
                print('{}-{}'.format(device,run_generate_device_objects[rack][device].run_all_checks()))
if __name__ == '__main__':
    main()