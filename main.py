import re

takeInput = True
print("Enter end to end giving grammar input")
variables = []
terminals = []
language = {}
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
                variables.append(char)
            if char.islower() and char not in terminals and char != 'e':
                terminals.append(char)
    if not splitGrammar[0] in language:
        language[splitGrammar[0]] = []
    for char in rightHandSide:
        language[splitGrammar[0]].append(char)
print("terminals are:", terminals, "variables are:", variables)
print(language)


# def sort_by_values_len(dict):
#     dict_len = {key: len(value) for key, value in dict.items()}
#     import operator
#     sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
#     sorted_dict = [{item[0]: dict[item[0]]} for item in sorted_key_list]
#     return sorted_dict


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
                        print(temp)
                        print("l is", l, l not in generating, key)
                        if l not in generating:
                            key = 0
                            break
                    if key == 1:
                        generating.append(char)
                        changes = True
                        break
                    else:
                        print(char)
    print("generating symbols are", generating)
    print("non generating symbols are eliminated")


def eliminate_non_reachable():
    reachable = ["S"]
    current = ["S"]
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
    for ter in terminals:
        if ter not in reachable:
            terminals.remove(ter)

    print("non-reachable symbols are eliminated")


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
    temp = []
    temp.extend(language[each])
    temp.extend(language[char])
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
            print("temp is:", temp)
            global key
            key = 1
            print(char,
                  "--------------------------------------------------------------------------------------------------------------------------------------------vvvv")
            curr = language[char]
            print("curr is ", curr)
            for each in curr:
                print("each is:", each)
                print(curr)
                if each.isupper() and len(each) == 1 and char != each:
                    key = 0
                    # print("type of curr is:", type(each), type(char))
                    print(char, " ", each)
                    # print(language[char],language[each])
                    print("appending ",char," to ",each)
                    appendTo(char, each)
                    changes = True
            if key == 1:
                print("removed char", char)
                removable.extend(char)
            print("temp is:", temp)




def nullable_variables():
    nullable = []
    changes = True
    while changes:
        changes = False
        for temp in variables:
            if temp in language.keys():
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
                            changes = True
                    print("i is:", i)
                    print(nullable)
    return nullable


def eliminate_null_productions():
    temp = nullable_variables()
    for char in temp:
        if len(language[char]) == 1:
            global key
            key = 1
        for var in variables:
            curr = language[var]
            count = 0
            for l in curr:
                if char in l and len(l) != 1:
                    temporary = [m.start() for m in re.finditer(char, l)]
                    index_count = len(temporary)
                    count += index_count
                    for i in range(1, index_count + 1):
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


eliminate_unit_productions()
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

# print(language["S"])
eliminate_null_productions()
print(language)

# print(nullable_variables())
