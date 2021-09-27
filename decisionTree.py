import math

sol = []

def class_count(attr, examples):
    """
    given a set of exam ples, it finds the count of distinct values of
    the goal attribute.
    :param examples: example set
    :return: values: list of distinct goal attribute values
             count : counts of these values
    """
    values = []
    count = []
    for i in examples:
        val = i[attr]
        if val not in values:
            values.append(val)
            count.append(1)
        else:
            count[values.index(val)] += 1
    return values,count

def plurality_val(parent_examples):
    """
    Given a set of examples, this method returns the most common output
    value amongst them.
    :param parent_examples: set of examples
    :return: most common output value
    """
    t = len(parent_examples[0])-1
    values, count = class_count(t, parent_examples)
    return values[count.index(max(count))]

def p_n(examples):
    """
    given a set of examples, this method returns the no. of positive and
    negative outputs.
    :param examples: set of examples
    :return: p: no. of positive examples
             n: no. of negative examples
    """
    p=0
    n=0
    t = len(examples[0])-1
    values, count = class_count(t, examples)
    if values[0] =='n':
        p = count[0]
        n = count[1]
    else:
        p = count[1]
        n = count[0]
    return p, n


def entropy(n):
    """
    returns the entropy of a given value n
    :param n: value
    :return: entropy of n
    """
    if n == 0 or n == 1:
        return 0
    return -((n * math.log(n, 2)) + ((1 - n) * math.log((1 - n), 2)))


def remainder(attr, examples, p, n):
    """
    this method calculates the remainder value for an attribute.
    :param attr: attribute
    :param examples: input data set
    :param p: no. of positive classifications
    :param n: no. of negative classifications
    :return: remainder
    """
    values = []
    count = []
    rem=0
    t = p + n
    l = len(examples[0])-1
    for i in examples:
        if i[attr] not in values:
            values.append(i[attr])
            count.append([0, 0])
        ind = values.index(i[attr])
        if i[l] == 'n':
            count[ind][0] += 1
        else:
            count[ind][1] += 1
    for i in range(len(values)):
        tk = (count[i][0] + count [i][1])
        rem += (tk/t) * (entropy(count[i][0]/ tk))
    return rem

def importance(attr, examples):
    """
    this method calculates the information gain for a given attribute.
    :param attr: attribute
    :param examples: input data set
    :return: information gain
    """
    p, n = p_n(examples)
    return entropy(p/(p+n)) - remainder(attr, examples, p, n)

def decision_tree(examples, attributes, parent_examples):
    """
    given an input data set, this method creates a decision tree in
    the form of a list
    :param examples: input data set
    :param attributes: list of attributes
    :param parent_examples: examples of parent node in the tree
    :return:
    """
    t =len(examples[0])-1
    values, count = class_count(t, examples)
    if len(examples) == 0:
        sol.append(plurality_val(parent_examples))
        return plurality_val(parent_examples)
    elif len(attributes) == 0:
        sol.append(plurality_val(examples))
        return plurality_val(examples)
    elif len(values) == 1:
        sol.append(values[0])
        return values[0]
    else:
        max = -1
        attr = None
        for i in attributes:
            temp = importance(i,examples)
            if temp > max:
                max = temp
                attr = i
        v, c = class_count(attr, examples)
        for i in v:
            t_attributes = attributes.copy()
            exs = []
            for e in examples:
                if e[attr] == i:
                    exs.append(e)
            if attr in t_attributes:
                t_attributes.remove(attr)
            sol.append([attr, i])
            decision_tree(exs, t_attributes, examples)

def prediction(test, sol):
    """
    given an input, it predicts the classification using the decision tree built.
    :param test: input
    :return: classification
    """
    t = test
    found = 0
    i = 0
    while found == 0:
        if(len(sol[i]) > 1):
            #current attribute
            attr = sol[i][0]
            if str(t[int(sol[i][0])])!= str(sol[i][1]):
                #if current attribute value does not match given input
                #find index at which value matches.
                # print('no match')
                for j in sol:
                    if j[0] == attr and j[1] == t[int(j[0])]:
                        i = sol.index(j)
                        break
            if str(t[int(sol[i][0])]) == str(sol[i][1]):
                #if current attribute value matches with given input
                # and next value is a classification,
                #print classification.
                if len(sol[i + 1]) == 1:
                    return sol[i+1]
        i += 1


def decisionHelper(examplesFilename, hypothesisFilename ):
    """
    this is a helper function that calls a function to create a decision
    tree and stores it in the given file.
    :param examplesFilename: processed input data
    :param hypothesisFilename: file where decision tree is saved
    """
    ip = examplesFilename
    l = list(range(len(ip[0])-1))
    decision_tree(ip, l, ip)
    with open(hypothesisFilename, 'x') as hfile:
        hfile.write('decisiontree\n')
        for i in sol:
            for j in i:
                hfile.write(str(j))
                hfile.write(' ')
            hfile.write("\n")


def correct(ip, sol):
    """
    given an input data set and the decision tree, it prints the predictions
    for each sample
    :param ip: input data set
    :param sol: decision tree

    """
    for i in ip:
        cl = prediction(i, sol)
        if cl[0] == 'n':
            print('nl')
        else:
            print('en')


