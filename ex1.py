def find_missing_letter(chars):
    n = 0
    while ord(chars[n]) == ord(chars[n+1]) -1:
        n += 1
    return chr(1+ord(chars[n]))

result = find_missing_letter(['a','b','c','d','f'])
#result2 = find_missing_letter(['O','Q','R','S'])

print(result[0])
#print(result2[0])
