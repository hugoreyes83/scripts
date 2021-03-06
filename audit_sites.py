import difflib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--region', help='specify region')
args = parser.parse_args()

#Reading files
devices = ['dummyrouter']
results = []
def compare_files(file1,file2,fromfile,tofile):
    for diff in  difflib.context_diff(file1,file2,fromfile,tofile):
        return diff

for routers in devices:
    firstfile = 'GRU/'+str(routers)+'_current.conf'
    secondfile =  'GRU/'+str(routers)+'_expected.conf'
    with open(firstfile, 'r') as f1, open(secondfile, 'r') as f2:
        file1 = f1.readlines()
        file2 = f2.readlines()
        diff = compare_files(file1,file2,firstfile,secondfile)
        print diff
        if diff == None:
            results.append(('GRU', routers, 'IN SYNC'))
        else:
            results.append(('GRU', routers, 'NOT IN SYNC'))

print "{0:<12} {1:^24} {2:24}".format("Region", "Device", "Status")
print "-"*46
for element in results:
    print "{0:12} {1:^24} {2:24}".format(element[0],element[1],element[2])

