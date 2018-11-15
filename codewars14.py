from collections import Counter
def valid_parentheses(string):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    count_string = Counter(string)
    need_closing = 0
    if count_string['('] != count_string[')']:
        return False
    else:
        for i in string:
            if i in alphabet:
                continue
            if i == '(':
                need_closing += 1
            elif i == ')' and need_closing > 0:
                need_closing -= 1
            else:
                return False
        if need_closing != 0:
            return False
        else:
            return True




result = valid_parentheses("hi()()()")
print(result)
