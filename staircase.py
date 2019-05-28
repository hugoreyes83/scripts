import time


def num_ways(n):
    '''function that return number of ways to go up an staircase
    of n steps taking either 1 or 2 steps at a time'''
    if n == 0 or n == 1:
        return 1
    else:
        return num_ways(n-1) + num_ways(n-2)

def num_ways_bottom_up(n):
    if n == 0 or n == 1:
        return 1
    else:
        nums = []
        nums.insert(0,1)
        nums.insert(1,1)
        for i in range(2,n+1):
            nums_sum = nums[i-1] + nums[i-2]
            nums.insert(i,nums_sum)
        return nums[n]

start1 = time.time()
first = num_ways(7)
end1 = time.time()
total_time1 = end1 - start1

start2 = time.time()
second = num_ways_bottom_up(7)
end2 = time.time()
total_time2 = end2 - start2

print('{} {}'.format(first,total_time1))
print('{} {}'.format(second,total_time2))
