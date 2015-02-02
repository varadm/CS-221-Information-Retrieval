__author__ = 'varadmeru'


def compute_n_grams(token_list, n, keep_space):
    if n == 1:
        return None
    n_gram_list = []
    lower_token_list = map(lambda word: str(word).lower(), token_list)
    len_of_token_list = len(token_list)

    for i in range(len_of_token_list):
        temp = lower_token_list[i]
        for j in range(1, n):
            if (i+j) < len_of_token_list:
                if keep_space:
                    temp = temp + " " + lower_token_list[i + j]
                else:
                    temp += lower_token_list[i + j]
                n_gram_list.append(temp)
    return n_gram_list


def removes_spaces(s):
        l = s.split()
        output = ""
        for i in l:
            output += i
        print output
        return output

#s = "For example: eye is a palindrome and so is Do geese see god . malayalam bob"
#compute_n_grams(s.split(), 6, True)

#removes_spaces(s)


