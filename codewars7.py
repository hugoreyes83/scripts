def expanded_form(num):
    num_length = len(str(num))
    if num_length > 1:
        zeros = num_length -1
        final_num = ""
        for i in str(num):
            if i in ('1','2','3','4','5','6','7','8','9'):
                final_num = final_num + " + " + i + str(0)*zeros
                zeros = zeros - 1
            else:
                zeros = zeros - 1
        return final_num[3:].strip()
    else:
        return str(num)

result = expanded_form(70304)
print(result)
