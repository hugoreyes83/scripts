def order(sentence):
    split_sentence = sentence.split()
    split_sentence.sort(key=lambda x: min(x))
    return ' '.join(split_sentence)

result = order("is2 Thi1s T4est 3a")
print(result)
