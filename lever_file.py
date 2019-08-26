import yaml

class Result():
    def __init__(self):
        self.results = []
    def addtoresults(self,result):
        self.result = result
        self.results.append(self.result)

def validate_lever_rack(rack_dict):
    '''function to check if at least one stripe is listed, values can be either 4(half stripe) or 8(full stripe)'''
    lever_stripe = [4,8]
    lever_racks = [i for i in rack_dict if 'lv-eng' in i]
    return len(set(lever_racks)) in lever_stripe

def validate_lbes(rack_dict):
    '''function to validate lbes defined in yaml file'''
    lbe_routers = [i for i in rack_dict if '-br-lbe-' in i and '_' not in i]
    result = Result()
    for router in lbe_routers:
        for id in range(2,5,1):
            result.addtoresults(check_dummy_devices(router+'{}{}'.format('_',id),rack_dict))
    print(result.results)
    return all(result.results)

def check_dummy_devices(lbe,rack_dict):
    return lbe in rack_dict

def open_file(file):
    with open(file) as f:
        yaml_file = yaml.safe_load(f)
        return yaml_file

def get_racks_from_yaml(yaml):
    racks = [i for i in yaml['racks']]
    return len(set(racks)) == yaml['main']['number_of_racks']

def get_rack_from_racks(yaml):
    racks = [i for i in yaml['racks']]
    for i in racks:
        rack_lbe(yaml['racks'][i]['neighbors'])

def main():
    open_yaml_file = open_file('iad7-132-lv-eng.yaml')
    print(get_racks_from_yaml(open_yaml_file))
    print(validate_lever_rack(open_yaml_file['racks']['rack1']['neighbors']))
    print(validate_lbes(open_yaml_file['racks']['rack1']['neighbors']))


if __name__ == '__main__':
    main()
