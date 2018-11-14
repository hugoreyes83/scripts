from collections import Counter
def duplicate_count(text):
    # Your code goes here
    occurences = Counter(text.lower())
    counter = 0
    for i in occurences:
        if occurences[i] > 1:
            counter += 1
    return counter

result = duplicate_count("Indivisibilities")
print(result)

#duplicate_count("abcdea")
