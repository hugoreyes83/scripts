def decoratestring(s):
    top = ' {}'.format('-'*(len(s)+2))
    middle = '{}{}{}'.format('| ',s,' |')
    bottom = ' {}'.format('-'*(len(s)+2))
    return top,middle,bottom

for i in decoratestring('this is some text'):print(i)
for i in decoratestring('this is not a test'):print(i)


def decoratetext(t):
    list1 = []
    top = ' {}'.format('-'*len(max([ i for i in t], key = lambda x: len(x))))
    pattern = '| %%-%ds |'% len(max([ i for i in t], key = lambda x: len(x)))
    middle= [pattern %i for i in t]
    bottom = ' {}'.format('-'*len(max([ i for i in t], key = lambda x: len(x))))
    list1.append(top)
    list1.extend(middle)
    list1.append(bottom)
    return list1

multilinetext ='first line\nsecond line\nthird line\nfourth line\nthis is of course the fifth line'

for i in decoratetext(multilinetext): print(i)
