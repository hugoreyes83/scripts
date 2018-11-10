def find_missing_letter(chars):
    if chars[0].islower():
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        grab_beginning = ord(chars[0]) - 97
        grab_ending = len(chars) + 1
        grab_slice = alphabet[grab_beginning:grab_ending+grab_beginning]
        compare_slice = list(set(grab_slice) - set(chars))
        return compare_slice[0]
    else:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        grab_beginning = ord(chars[0]) - 65
        grab_ending = len(chars) + 1
        grab_slice = alphabet[grab_beginning:grab_ending+grab_beginning]
        compare_slice = list(set(grab_slice) - set(chars))
        return compare_slice[0]

result = find_missing_letter(['a','b','c','d','f'])
result2 = find_missing_letter(['O','Q','R','S'])
print(result[0])
print(result2[0])
