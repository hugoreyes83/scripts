from collections import Counter
def find_it(seq):
    number_of_occurrences = Counter(seq)
    for i in number_of_occurrences:
        odd_or_even = number_of_occurrences[i] % 2
        if odd_or_even != 0:
            return i





result = find_it([20,1,-1,2,-2,3,3,5,5,1,2,4,20,4,-1,-2,5])
print(result)
