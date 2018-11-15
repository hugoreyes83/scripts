from collections import Counter
def find_uniq(arr):
    count_items = Counter(arr)
    for i in count_items:
        if count_items[i] == 1:
            return i
        else:
            continue

result = find_uniq([ 0, 0, 0.55, 0, 0 ])
print(result)
