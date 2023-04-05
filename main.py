import re
import random as rand

takeInput = True
print("Enter end to end giving grammar input")
variables = []
terminals = []
language = {}
startState = "S"
startStateChange = False
global key
while takeInput:
    grammar = input()
    if grammar == "end":
        takeInput = False
        break
    splitGrammar = grammar.split("->")
    rightHandSide = splitGrammar[1].split("|")
    for i in range(0, 2):
        for char in splitGrammar[i]:
            if char.isupper() and char not in variables and char != 'e':
                variables.append(char.strip())
            if char.islower() and char not in terminals and char != 'e':
                terminals.append(char.strip())
            if char.isnumeric():
                print("Please enter only alphabets. Numbers and special characters are not accepted by the grammar")
                exit()
    if not splitGrammar[0] in language:
        language[splitGrammar[0]] = []
    for char in rightHandSide:
        if "S" in char.strip() and startState == "S":
            startState = "S1"
            language["S1"] = ["S"]
            startStateChange = True
            variables.append("S1")
        language[splitGrammar[0]].append(char.strip())
# print("terminals are:", terminals, "variables are:", variables)
# print(language)


# def sort_by_values_len(dict):
#     dict_len = {key: len(value) for key, value in dict.items()}
#     import operator
#     sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
#     sorted_dict = [{item[0]: dict[item[0]]} for item in sorted_key_list]
#     return sorted_dict


def eliminate_non_generating():
    # print(language)
    # print(
    #     "eliminating non-generating symbols-------------------------------------------------------------------")
    # print(language)
    # print(variables)
    changes = True
    non_generating = []
    for char in variables:
        if char not in language.keys():
            # print(char, "not in dictionary")
            non_generating.append(char)
    generating = terminals
    while changes:
        changes = False
        for char in variables:
            if char not in non_generating and char not in generating:
                global key
                temp = language[char]
                for k in temp:
                    key = 1
                    for l in k:
                        # print(temp)
                        # print("l is", l, l not in generating, key)
                        if l not in generating:
                            key = 0
                            break
                    if key == 1:
                        generating.append(char)
                        changes = True
                        break

    for i in non_generating:
        if i in variables:
            variables.remove(i)
    # print("generating symbols are", generating)
    # print("non-generating symbols are", non_generating)
    # print("non generating symbols are eliminated")
    for char in variables:
        curr = language[char]
        for temp in curr:
            for i in temp:
                if i in non_generating:
                    curr.remove(temp)
                    break


def eliminate_non_reachable():
    reachable = [startState]
    current = [startState]
    while current:
        temp = language[current.pop()]
        for char in temp:
            for k in char:
                if k not in reachable:
                    if k in language.keys():
                        current.append(k)
                    reachable.append(k)
    for var in variables:
        if var not in reachable:
            if var in language.keys():
                del language[var]
            variables.remove(var)
        if var in language.keys():
            char = language[var]
            for temp in char:
                key = 1
                for l in temp:
                    if l not in reachable:
                        key = 0
                if key == 0:
                    language[var].remove(temp)

    for ter in terminals:
        if ter not in reachable:
            terminals.remove(ter)

    # print("non-reachable symbols are eliminated")


# eliminate_non_reachable()
# print("After removing unreachable symbols, the terminals are,", variables, terminals)
# eliminate_non_generating()


def removeDuplicates(char):
    temp = []
    for i in language[char]:
        if i not in temp:
            temp.append(i)
    language[char] = temp


def appendTo(char, each):
    # print(language[char])
    # print(language[each])
    temp = []
    temp.extend(language[each])
    temp.extend(language[char])
    # print(temp)
    for i in range(0, temp.count(each)):
        temp.remove(each)
    # print(each)
    # print("in append function")
    # print(temp)
    if char in temp:
        temp.remove(char)
    language[char] = temp
    removeDuplicates(char)


def eliminate_unit_productions():
    changes = True
    temp = []
    removable = []
    temp.extend(variables)
    while changes:
        changes = False
        for char in temp:
            # print("temp is:", temp)
            global key
            key = 1
            # print(char,
            #       "--------------------------------------------------------------------------------------------------------------------------------------------vvvv")
            curr = language[char]
            # print("curr is ", curr)
            for each in curr:
                # print("each is:", each)
                # print(curr)
                if each.isupper() and len(each) == 1 and char != each:
                    key = 0
                    # print("type of curr is:", type(each), type(char))
                    # print(char, " ", each)
                    # print(language[char],language[each])
                    if char in language.keys() and each in language.keys():
                        # print("appending ", char, " to ", each)
                        appendTo(char, each)
                        changes = True
            if key == 1:
                # print("removed char", char)
                # temp.remove(char)
                removable.extend(char)
            # print("temp is:", temp)


def nullable_variables():
    nullable = []
    changes = True
    while changes:
        # print("Changes = True")
        changes = False
        for temp in variables:
            # print(variables)
            if temp in language.keys() and temp not in nullable:
                curr = language[temp]
                if 'e' in curr:
                    if temp not in nullable:
                        nullable.append(temp)
                        changes = True
                        # print("changes are made true 1")
                for i in curr:
                    global key
                    key = 1
                    for l in i:
                        # print("l is", l)
                        if l not in nullable:
                            key = 0
                            # print("key = 0")
                    if key == 1:
                        if temp not in nullable:
                            nullable.append(temp)
                            # changes = True
                            print("changes are made True 2")
                            # break
                    # print("i is:", i)
                    # print(nullable)
                    # print("variables are :", variables)
    # print("nullable variables are",nullable)
    return nullable


def eliminate_null_productions():
    temp = nullable_variables()
    for char in temp:
        if len(language[char]) == 1:
            global key
            key = 1
        for var in variables:
            if var in language.keys():
                curr = language[var]
                count = 0
                for l in curr:
                    if char in l and len(l) != 1:
                        temporary = [m.start() for m in re.finditer(char, l)]
                        index_count = len(temporary)
                        count += index_count
                        for i in range(1, index_count):
                            character = l.replace(char, "", i)
                            if character not in curr:
                                curr.append(character)
                        for i in temporary:
                            character = l[:i] + "" + l[i + 1:]
                            if character not in curr:
                                curr.append(character)

                if count == 0 and curr.count(char):
                    language[var].append('e')
        if 'e' in language[char]:
            language[char].remove('e')
        if len(language[char]) == 0:
            del language[char]
    if startState in temp and 'e' not in language[startState]:
        language[startState].append("e")


# def eliminate_null_productions():
#     temp = nullable_variables()
#     for char in temp:
#         if len(language[char]) == 1:
#             global key
#             key = 1
#         for var in variables:
#             if var in language.keys():
#                 curr = language[var]
#                 count = 0
#                 for l in curr:
#                     # print("hello")
#                     if char in l and len(l) != 1:
#                         temporary = [m.start() for m in re.finditer(char, l)]
#                         index_count = len(temporary)
#                         count += index_count
#                         for i in range(1, index_count + 1):
#                             character = l.replace(char, "", i)
#                             if character not in curr:
#                                 curr.append(character)
#                         for i in temporary:
#                             character = l[:i] + "" + l[i + 1:]
#                             if character not in curr:
#                                 curr.append(character)
#
#                     if count == 0 and curr.count(char):
#                         language[var].append('e')
#         if 'e' in language[char]:
#             language[char].remove('e')
#         if len(language[char]) == 0:
#             del language[char]
#     if "" in language["S"]:
#         language["S"].remove("")
#         language["S"].append("e")


def random_alphabet():
    change = True
    while change:
        num = rand.randint(65, 90)
        char = chr(num)
        if char not in variables:
            change = False
    return char


def conversion_to_chomsky_normal_form():
    # print("converting to chomsky normal form")
    addedPairs = {}
    change = True
    while change:
        change = False
        for i in language.copy():
            char = language[i]
            for i in char:
                char.remove(i)
                char.append(i.strip())
            for temp in char:
                if len(temp) > 2 and temp.isupper():
                    # print("condition 1 satisfied")
                    while len(temp) != 2:
                        # print("length of temp is not 2", temp, len(temp), temp[0], temp[1], temp[2], "hello")
                        curr = random_alphabet()
                        j = temp[0:2]
                        if j not in addedPairs:
                            addedPairs[j] = curr
                            char.remove(temp)
                            temp = curr + temp[2:]
                            char.append(temp)
                            language[curr] = [j]
                            variables.append(curr)
                        else:
                            char.remove(temp)
                            temp = addedPairs[j] + temp[2:]
                            char.append(temp)
                        # print(char, temp)
                    change = True
                elif (len(temp) > 2 and not temp.isupper()) or (len(temp) == 2 and not temp.isupper()):
                    # print("condition 2 satisfied")
                    # print(temp)
                    for i in range(0, len(temp)):
                        curr = random_alphabet()
                        if temp[i].islower():
                            if temp[i] not in addedPairs:
                                char.remove(temp)
                                j = temp[i]
                                temp = temp[:i] + curr + temp[i + 1:]
                                char.append(temp)
                                # print("added curr ", curr)
                                addedPairs[j] = curr
                                language[curr] = [j]
                                variables.append(curr)
                            else:
                                char.remove(temp)
                                temp = temp[:i] + addedPairs[temp[i]] + temp[i + 1:]
                                char.append(temp)
                    change = True
    for keys in language.keys():
        temp = language[keys]
        if keys in temp:
            temp.remove(keys)

    # print(addedPairs)


# eliminate_unit_productions()
# appendTo("F","I")
# appendTo("F","E")
# appendTo("E","T")
# appendTo("T","F")
# print(type("T"),type("F"))
# print(language)
# print("variables are", variables)


# print(nullable_variables())

# for var in temp:
#     for char in variables:
#         curr = language[char]
#         for l in curr:
#             if var in l and len(l) != 1:
#                 # print("type of l is:",type(l))
#                 curr.append(l.replace(var, ""))
#             print("hello world")


# For i = 1 to n:
#   For each variable A:
#      We check if A -> b is a rule and b = wi for some i:
#         If so, we place A in cell (i, i) of our table.
# For l = 2 to n:
#   For i = 1 to n-l+1:
#        j = i+l-1
#         For k = i to j-1:
#            For each rule A -> BC:
#         We check if (i, k) cell contains B and (k + 1, j) cell contains C:
#              If so, we put A in cell (i, j) of our table.
# We check if S is in (1, n):
#   If so, we accept the string
#   Else, we reject.

def cykAlgorithm(string):
    lang = {}
    for i in variables:
        curr = language[i]
        for var in curr:
            if var.isupper() and len(var) == 2:
                if i in lang.keys():
                    lang[i].append(var)
                else:
                    lang[i] = [var]
    strlen = len(string)
    Matrix = [["" for x in range(strlen)] for y in range(strlen)]

    for j in range(0, strlen):
        for var in variables:
            character = string[j]
            curr = language[var]
            if character in curr:
                Matrix[j][j] += var
        for i in range(j, -1, -1):
            for k in range(i, j):
                for temp in lang.keys():
                    curr = lang[temp]
                    for var in curr:
                        print(k)
                        if var[0] in Matrix[i][k] and var[1] in Matrix[k + 1][j]:
                            print("success!")
                            if temp not in Matrix[i][j]:
                                Matrix[i][j] += temp

    if 'S' in Matrix[0][strlen - 1]:
        print("string is present in the grammar")

    print("In cyk algo:")
    for i in range(0, strlen):
        j = strlen - i - 1
        temp = ""
        for k in range(0, i + 1):
            temp = temp + Matrix[k][j + k] + " "
        print(temp)

        # temp = temp + Matrix[i][j] + " "
        # print(temp)


def print_language():
    if startStateChange:
        print("The new Start State is:", startState)
    else:
        print("The start state is:", startState)
    print("The grammar after converting to chomsky normal form is:")
    print(language)


# print(language["S"])
eliminate_null_productions()
eliminate_non_generating()
eliminate_non_reachable()
print("eliminating unit productions:-----------------------------------------------------")
# print(language)
eliminate_unit_productions()
# appendTo("A","S")
# print(language)
# print(language)
print("Before converting to chomsky normal form -----------------------------------------------------")
conversion_to_chomsky_normal_form()
# eliminate_unit_productions()
# conversion_to_chomsky_normal_form()
# print(random_alphabet()).
print_language()
# print(variables)
# print(nullable_variables())
cykAlgorithm("b")

# print("printing language")
# for i in language.keys():
#     curr = language[i]
#     for j in curr:
#         print(i, "->", j, " ", len(j))
