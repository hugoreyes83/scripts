def decrypt(encrypted_text, n):
    if n <= 0 or encrypted_text == "":
        return encrypted_text
    else:
        while n > 0:
            even_char = []
            odd_char = []
            final_string = []
            for idx,char in enumerate(encrypted_text,1):
                if idx%2 == 0:
                    even_char.append(char)
                else:
                    odd_char.append(char)
            for x,y in zip(even_char,odd_char):
                final_string.append(x)
                final_string.append(y)
            n -= 1
            return ''.join(final_string)



def encrypt(text, n):
    if n <= 0 or text == "":
        return text
    else:
        last_run = text
        while n > 0:
            grab_each_third_letter = []
            grab_each_second_letter = []
            for idx,char in enumerate(last_run,1):
                if idx%2 ==0:
                    grab_each_second_letter.append(char)
                else:
                    grab_each_third_letter.append(char)
            n -= 1
            final_string = grab_each_second_letter+grab_each_third_letter
            last_run = ''.join(final_string)
        return ''.join(final_string)

result = encrypt("This kata is very interesting!",1)
result2 = decrypt("hskt svr neetn!Ti aai eyitrsig",1)
print(result)
print(result2)

'''
Test.assert_equals(encrypt("This is a test!", 0), "This is a test!")
Test.assert_equals(encrypt("This is a test!", 1), "hsi  etTi sats!")
Test.assert_equals(encrypt("This is a test!", 2), "s eT ashi tist!")
Test.assert_equals(encrypt("This is a test!", 3), " Tah itse sits!")
Test.assert_equals(encrypt("This is a test!", 4), "This is a test!")
Test.assert_equals(encrypt("This is a test!", -1), "This is a test!")
'''
