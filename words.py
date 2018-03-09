import random
from nltk.corpus import words

words_list = words.words()
var = 'zepri'
list1 = []

for i in var:
    list1.append(i)


for i in range(1,500,1):
    random.shuffle(list1)
    match_word = ''.join(list1)
    if match_word in words_list:
        print '{} word in list'.format(match_word)
        break
    else:
        continue
