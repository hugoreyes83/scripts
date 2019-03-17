import openpyxl
import yaml
import re
import argparse
import logging
from tqdm import tqdm

parser = argparse.ArgumentParser(description='python script for generating yaml files')
parser.add_argument('--input',help='Enter input file')
parser.add_argument('--output',help='Enter output file')
parser.add_argument('--sheet',help='Enter sheet name')
args=parser.parse_args()

#setting up logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def position_check(s):
    return (int(s.split('-')[0][3:])+1)//2

def stripe_check(s):
    return s[-1:]

def get_interfaces(idx,sheet):
    #Grab interfaces
    return [sheet.cell(row=i,column=2).value for i in range(idx,idx+4,1)]

def validate_file(sheet):
    lines_read = 0
    lines_ignored = 0
    list_of_lbes = []
    lbe_pattern = re.compile(r"\w+\d+\-br\-\w+\-j\d+\-r\d+")
    my_dict = {}
    id = 2
    for i in tqdm(range(1,sheet.max_row+1,1)):
        lbe_router = sheet.cell(row=i,column=1).value
        match_lbe = lbe_pattern.match(lbe_router)
        if not match_lbe:
            lines_ignored += 1
            continue
        else:
            lines_read += 1
            if lbe_router in list_of_lbes:
                continue
            else:
                list_of_lbes.append(lbe_router)
    logging.info('{} lines have been read'.format(lines_read))
    logging.info('{} lines have been ignored'.format(lines_ignored))
    logging.info('{} LBEs have been detected'.format(len(list_of_lbes)))
    return sorted(list_of_lbes)

def open_file(file):
    #Open excel file
    try:
        wb = openpyxl.load_workbook(file)
    except:
        print('Could not open {}'.format(file))

def write_yaml_file(data,output_file):
    #Write to file
    try:
        with open(output_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, indent=4)
    except:
        print('Something went wrong, {} could not be opened for writing'.format(output_file))

def main():
    open_file(args.input)
    wb = openpyxl.load_workbook(args.input)
    sheet = wb[args.sheet]
    lbe_routers_list = validate_file(sheet)
    my_dict = {}
    for i in range(1,sheet.max_row+1,4):
        lbe_get_interfaces = get_interfaces(i,sheet)
        lbe_router = sheet.cell(row=i,column=1).value
        my_dict[lbe_router]['breakout_positions'] = '[1, 2, 3, 4]'
        my_dict[lbe_router]['port_group'] = 'unsecured'
        my_dict[lbe_router]['remote_edge_interfaces'] = '[{}{}{}{}]'.format

if __name__ == '__main__':
    main()
