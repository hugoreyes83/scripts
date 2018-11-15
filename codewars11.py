from collections import Counter
def duplicate_encode(word):
    new_string = []
    number_of_times = Counter(word.lower())
    for i in word.lower():
        if number_of_times[i] > 1:
            new_string.append(')')
        else:
            new_string.append('(')
    return ''.join(new_string)

result = duplicate_encode("Success")
print(result)
