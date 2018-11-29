import xlsxwriter
import argparse
from itertools import product

parser = argparse.ArgumentParser(description='Script for generating cutsheet for SJLB deployments')
parser.add_argument('--first_gaggle',required=True)
parser.add_argument('--last_gaggle',required=True)
parser.add_argument('--dc',required=True)
parser.add_argument('--output',required=True)
args = parser.parse_args()

routers = []
current_id = 0
current_gaggle = int(args.first_gaggle)
for i in range(int(args.first_gaggle),int(args.last_gaggle)+1,1):
    router1 = '{}{}{}{}{}'.format(args.dc,'-br-lbe-j',current_gaggle,'-r',current_id+1)
    router2 = '{}{}{}{}{}'.format(args.dc,'-br-lbe-j',current_gaggle,'-r',current_id+2)
    router3 = '{}{}{}{}{}'.format(args.dc,'-br-lbe-j',current_gaggle,'-r',current_id+3)
    routers.append(router1)
    routers.append(router2)
    routers.append(router3)
    current_gaggle +=1


interfaces = ['xe-0/0/24','xe-0/0/25','xe-0/0/26','xe-0/0/27','xe-0/0/28','xe-0/0/29','xe-0/0/30',
'xe-0/0/31','xe-0/0/32','xe-0/0/33','xe-0/0/34','xe-0/0/35','xe-0/0/36','xe-0/0/37','xe-0/0/38','xe-0/0/39']


def main():
    workbook = xlsxwriter.Workbook(args.output)
    worksheet = workbook.add_worksheet(args.dc)
    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 20)
    row = 1
    for router,interface in product(routers,interfaces):
        # Write values, with row/column notation.
        worksheet.write(row, 0, router)
        worksheet.write(row, 1, interface)
        row += 1

    workbook.close()


if __name__ == '__main__':
    main()
