import csv
def open_file(file):
    with open(file,'r') as f:
        reader = csv.reader(f)
    return reader

def main():
    excel_file = 'Cutsheet.xlsx'
    read_file = open_file(excel_file)
    for i in read_file:
        print i


if __name__ == '__main__':
    main()
