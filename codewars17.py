def create_phone_number(n):
    first_part = '(' + str(n[0])+ str(n[1])+ str(n[2]) + ') '
    second_part = str(n[3]) + str(n[4]) + str(n[5]) + '-'
    third_part = str(n[6]) + str(n[7]) + str(n[8]) + str(n[9])
    phone_number = first_part + second_part + third_part
    return phone_number
result = create_phone_number([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
print result
