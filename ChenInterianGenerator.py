import secrets
import copy


def get_sample(source, number):
    choices = []
    sourceCopy = copy.deepcopy(list(source))
    for i in range(number):
        choice = secrets.choice(sourceCopy)
        sourceCopy.remove(choice)
        choices.append(choice)
    return choices


def create_formula( instance, parameters):

    first_tuple = parameters[0]
    second_tuple = parameters[1]
    ratio = parameters[2]
    existentials = second_tuple[1::2]
    universals = first_tuple[0::2]
    number_of_clauses = int(ratio * sum(existentials))
    file = open('ratio{}_{}'.format(ratio, instance), 'w')


    list_of_quantifier_sets = generate_quantifier_sets(second_tuple)

    listOfClauses = []
    listOfUsedVariables = []

    for i in second_tuple:
        listOfUsedVariables.append(set())

    for i in range(number_of_clauses):
        clause = []
        for num,  literalsFromSet in enumerate(first_tuple):
            variables = get_sample(list_of_quantifier_sets[num], literalsFromSet)
            for var in variables:
                listOfUsedVariables[num].add(var)
            for number in variables:
                sign = secrets.choice([0, 1])
                if sign == 1:
                    clause.append(-number)
                else:
                    clause.append(number)
        listOfClauses.append(clause)

    write_to_file(number_of_clauses,  listOfUsedVariables, file, listOfClauses)


def read_input():
    parameter = []
    input_first_tuple = input("First Tuple:").split()
    input_map_first_tuple = map(int, input_first_tuple)
    parameter.append(tuple(input_map_first_tuple))

    input_second_tuple = input("Second Tuple:").split()
    input_map_second_tuple = map(int, input_second_tuple)
    parameter.append(tuple(input_map_second_tuple))

    input_ratio = input("Ratio:").split()
    parameter.append(float((input_ratio.pop())))

    input_number_formulas = input("Number of formulas:").split()
    parameter.append((int(input_number_formulas.pop())))

    if len(parameter[0]) != len(parameter[1]):
        print("Tuples must be of the same length!")
        raise
    return parameter


def write_to_file(number_of_clauses,  list_of_used_variables_per_set, file, clause_list):
    number_of_variables = 0
    for variable_set in list_of_used_variables_per_set:
        number_of_variables += len(variable_set)

    file.write("p cnf {} {} \n".format(number_of_variables, number_of_clauses))
    existentialSwitch = False
    for quantifierSet in list_of_used_variables_per_set:
        setString = str(quantifierSet)[1:-1].replace(",", "")
        if existentialSwitch:
            file.write("e {} 0\n".format(setString))
        else:
            file.write("a {} 0\n".format(setString))
        existentialSwitch = not existentialSwitch
    for clause in clause_list:
        clauseString = str(clause)[1:-1].replace(",", "")
        file.write("{} 0\n".format(clauseString))


def generate_quantifier_sets(tup):
    counter = 1
    quantifier_sets = []
    for i in range(len(tup)):
        sets = []
        for j in range(tup[i]):
            sets.append(counter)
            counter += 1
        quantifier_sets.append(sets)
    return quantifier_sets

# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    input_parameters = read_input()
    for i in range(input_parameters[3]):
        create_formula(i, input_parameters)




