import re
import random as rand

takeInput = True
variables = []
terminals = []
language = {}
startState = input("Mention the start state with only uppercase:")
while not startState.isupper():
    startState = input("Wrong start state,please re-enter the start state containing only upper-case alphabets:")

print("Enter e for null production and Enter end to end giving grammar input")
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
        if startState in char.strip() and not startStateChange:
            language["S1"] = [startState]
            startState = "S1"
            startStateChange = True
            variables.append("S1")
        language[splitGrammar[0]].append(char.strip())


def eliminate_non_generating():
    changes = True
    non_generating = []
    for char in variables:
        if char not in language.keys():
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


def removeDuplicates(char):
    temp = []
    for i in language[char]:
        if i not in temp:
            temp.append(i)
    language[char] = temp


def appendTo(char, each):
    temp = []
    temp.extend(language[each])
    temp.extend(language[char])
    for i in range(0, temp.count(each)):
        temp.remove(each)
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
            global key
            key = 1
            curr = language[char]
            for each in curr:
                if each.isupper() and len(each) == 1 and char != each:
                    key = 0
                    if char in language.keys() and each in language.keys():
                        appendTo(char, each)
                        changes = True
            if key == 1:
                removable.extend(char)


def nullable_variables():
    nullable = []
    changes = True
    while changes:
        changes = False
        for temp in variables:
            if temp in language.keys() and temp not in nullable:
                curr = language[temp]
                if 'e' in curr:
                    if temp not in nullable:
                        nullable.append(temp)
                        changes = True
                for i in curr:
                    global key
                    key = 1
                    for l in i:
                        if l not in nullable:
                            key = 0
                    if key == 1:
                        if temp not in nullable:
                            nullable.append(temp)
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


def random_alphabet():
    change = True
    while change:
        num = rand.randint(65, 90)
        char = chr(num)
        if char not in variables:
            change = False
    return char


def conversion_to_chomsky_normal_form():
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
                    while len(temp) != 2:
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
                    change = True
                elif (len(temp) > 2 and not temp.isupper()) or (len(temp) == 2 and not temp.isupper()):
                    for i in range(0, len(temp)):
                        curr = random_alphabet()
                        if temp[i].islower():
                            if temp[i] not in addedPairs:
                                char.remove(temp)
                                j = temp[i]
                                temp = temp[:i] + curr + temp[i + 1:]
                                char.append(temp)
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


def cykAlgorithm(string):
    strlen = len(string)
    if not strlen > 0 or string.isnumeric():
        print("Please Enter valid String that contains only alphabets")
        exit()
    lang = {}
    for i in variables:
        curr = language[i]
        for var in curr:
            if var.isupper() and len(var) == 2:
                if i in lang.keys():
                    lang[i].append(var)
                else:
                    lang[i] = [var]

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
                        if var[0] in Matrix[i][k] and var[1] in Matrix[k + 1][j]:
                            if temp not in Matrix[i][j]:
                                Matrix[i][j] += temp

    if strlen > 0 and 'S' in Matrix[0][strlen - 1]:
        print("string is present in the grammar")
    else:
        print("String is not present in the grammar")

    # print("Printing the matrix:")
    # for i in range(0, strlen):
    #     j = strlen - i - 1
    #     temp = ""
    #     for k in range(0, i + 1):
    #         temp = temp + Matrix[k][j + k] + " "
    #     print(temp)


def print_language():
    if startStateChange:
        print("The new Start State is:", startState)
    else:
        print("The start state is:", startState)
    print("The grammar after converting to chomsky normal form is:")
    for var in language.keys():
        temp = language[var]
        production = var + "->"
        for curr in temp:
            production = production + curr + "|"
        print(production[:len(production) - 1])


eliminate_null_productions()
eliminate_non_generating()
eliminate_non_reachable()
eliminate_unit_productions()
conversion_to_chomsky_normal_form()
print_language()
string = input("Enter any string to check if it is present in the language or not:")
cykAlgorithm(string)
