import itertools

base_64_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z',26:'a',27:'b',28:'c',29:'d',30:'e',31:'f',32:'g',33:'h',34:'i',35:'j',36:'k',37:'l',38:'m',39:'n',40:'o',41:'p',42:'q',43:'r',44:'s',45:'t',46:'u',47:'v',48:'w',49:'x',50:'y',51:'z',52:'0',53:'1',54:'2',55:'3',56:'4',57:'5',58:'6',59:'7',60:'8',61:'9',62:'+',63:'/'}

def str_to_bin(s):
    return [format(ord(i),'08b') for i in s]

def bin_to_groups_of_6(b):
    var = ''.join(b)
    counter_eight = itertools.count(0,8)
    counter_six = itertools.count(0,6)
    if len(var)%6 == 0:
        return [var[next(counter_six):i] for i in range(6,len(var)+6,6)]
    else:
        var = var + '0'*(6-divmod(len(var),6)[1])
        return [var[next(counter_six):i] for i in range(6,len(var)+6,6)]

def convert_bin_to_ascii(n):
    return ''.join([base_64_dict[int(i,2)] for i in n])

def from_str_to_bin(l):
    ivd = dict([(v,k) for (k,v) in base_64_dict.items()])
    return ''.join([format(ivd[i],'06b') for i in l])

def from_bin_to_str(l):
    mylist = chop_up_str(l,8)
    return ''.join([chr(int(i,2)) for i in mylist])

def chop_up_str(string,slice):
    counter_eight = itertools.count(0,8)
    counter_six = itertools.count(0,6)
    return [string[next(counter_eight):i] for i in range(slice,len(string)+slice,slice)]

def to_base_64(string):
    encode_str_to_bin = str_to_bin(string)
    encode_bin_to_bin_group = bin_to_groups_of_6(encode_str_to_bin)
    encode_str_to_ascii = convert_bin_to_ascii(encode_bin_to_bin_group)
    return encode_str_to_ascii

def from_base_64(string):
    decode_ascii_to_bin = from_str_to_bin(string)
    decode_bin_to_str = from_bin_to_str(decode_ascii_to_bin)
    return decode_bin_to_str.rstrip('\x00')

'''
encode = to_base_64('1234567890  ')
decode = from_base_64('MTIzNDU2Nzg5MCAg')
print(encode)
print(decode)


tests = [["this is a string!!","dGhpcyBpcyBhIHN0cmluZyEh"],
  ["this is a test!","dGhpcyBpcyBhIHRlc3Qh"],
  ["now is the time for all good men to come to the aid of their country.","bm93IGlzIHRoZSB0aW1lIGZvciBhbGwgZ29vZCBtZW4gdG8gY29tZSB0byB0aGUgYWlkIG9mIHRoZWlyIGNvdW50cnku"],
  ["1234567890  ", "MTIzNDU2Nzg5MCAg"],
  ["ABCDEFGHIJKLMNOPQRSTUVWXYZ ", "QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVog"],
  ["the quick brown fox jumps over the white fence. ","dGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIHRoZSB3aGl0ZSBmZW5jZS4g"],
  ["dGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIHRoZSB3aGl0ZSBmZW5jZS4","ZEdobElIRjFhV05ySUdKeWIzZHVJR1p2ZUNCcWRXMXdjeUJ2ZG1WeUlIUm9aU0IzYUdsMFpTQm1aVzVqWlM0"],
  ["VFZSSmVrNUVWVEpPZW1jMVRVTkJaeUFna","VkZaU1NtVnJOVVZXVkVwUFpXMWpNVlJWVGtKYWVVRm5h"],
  ["TVRJek5EVTJOemc1TUNBZyAg","VFZSSmVrNUVWVEpPZW1jMVRVTkJaeUFn"]]
'''

tests = [['z','eg']]
n = 0
l = 1
for i in tests:
    try:
        encode = to_base_64(i[n])
        decode = from_base_64(i[l])
        print('Testing {} and {}'.format(i[n],i[l]))
        print('Result is {} and {}'.format(encode,decode))
        if i[l] == encode and i[n] == decode.strip('\x00'):
            print('Test Successful')
        else:
            print('Test Failed')
    except:
        print('something went wrong')


CODES = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
def to_base_64(string):
    padding = 3 - len(string) % 3 if len(string) % 3 else 0
    binary = ''.join(format(ord(i),'08b') for i in string) + '00'*padding
    return ''.join(CODES[int(binary[i:i+6], 2)] for i in range(0, len(binary), 6))

def from_base_64(string):
    binary = ''.join(format(CODES.find(i),'06b') for i in string)
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)).rstrip('\x00')
