import difflib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file1', help='first file to compare')
parser.add_argument('--file2', help='second file to compare')
args = parser.parse_args()

with open(args.file1, 'r') as f1, open(args.file2, 'r') as f2:
    file1 = f1.readlines()
    file2 = f2.readlines()

def compare_files(first_file,second_file,fromfile=args.file1,tofile=args.file2):
    for diff in difflib.context_diff(first_file,second_file,fromfile=fromfile,tofile=tofile):
        print diff,

compare_files(file1,file2)
