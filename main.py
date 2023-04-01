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
            if char.isupper() and char not in variables:
                variables.append(char)
            if char.islower() and char not in terminals:
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
                        print("l is",l,l not in generating,key)
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
eliminate_non_generating()
