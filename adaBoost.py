import decisionTree
import math
import random
import sys

classification = {'n': 1, 'e': -1}

def stump(examples, attributes):
    """
    given an input data set and list of attributes, it returns aa decision stump.
    :param examples: input data set
    :param attributes: list of attributes
    :return: decision stump
    """
    sol = []
    max = -1
    attr = None
    for i in attributes:
        temp = decisionTree.importance(i, examples)
        if temp > max:
            max = temp
            attr = i
    v, c = decisionTree.class_count(attr, examples)
    for i in v:
        exs = []
        sol.append([attr, i])
        for e in examples:
            if e[attr] == i:
                exs.append(e)
        sol.append(decisionTree.plurality_val(exs))
    return sol

def normalize(w):
    """
    given a list of value, this methods normalizes the values,
    such that sum of all values = 1.
    :param w: list of weights
    :return: list of normalized weights
    """
    wt = 0
    for i in w:
        wt += i
    for i in range(len(w)):
        w[i] /= wt
    return w


def weightedMajority(h, z, ip):
    """
    for a given ip, it runs it through ada boost model built and returns prediction
    by calculating the weighted majority.
    :param h: hypothesis
    :param z: amount of say
    :param ip: input
    :return: classification
    """
    total = 0
    for i in range(len(h)):
        total += classification[decisionTree.prediction(ip,h[i])[0]] * z[i]
    if total >= 0:
        return 'nl'
    else:
        return 'en'

def correct(ip, h, z):
    """
    given a sample data set, list of hypothesis and amount of say
    this method prints the prediction for each sample.
    :param ip: sample data set
    :param h: list of hypothesis
    :param z: list of amount of say
    """
    for i in ip:
        cl = weightedMajority(h,z,i)
        print(cl)


def newSamples(examples, w):
    """
    given sample data set and weights of samples, this method generates a
    new sample data set by giving importance to samples with larger weight.
    :param examples: sample data set
    :param w: list of weights
    :return: new sample set
    """
    new = []
    n = len(examples)
    i = 0
    while len(new)<n:
        i+=1
        r = random.random()
        ra = 0
        for j in range(len(w)):
            if r >= ra and r < ra+w[j]:
                new.append(examples[j])
            ra += w[j]
    return new


def ada(examples, k, attributes):
    """
    given input examples, it prepares a training model and returns amt of say, list of classifiers
    i.e decision stumps created.
    :param examples: sample data set
    :param k: no od classifiers
    :param attributes: list of attributes
    :return: list of classifiers and their amount of say
    """
    w = []
    h = []
    z = []
    n = len(examples)
    fsize = len(examples[0])-1
    for i in range(n):
        w.append(1/n)
    for i in range(k):
        h.append(stump(examples,attributes))
        error = 0.0000000000000001
        for j in range(n):
            if decisionTree.prediction(examples[j], h[i]) != examples[j][fsize][0]:
                error += w[j]
        z.append(0.5 * math.log((1-error)/error))
        for j in range(n):
            if decisionTree.prediction(examples[j], h[i]) != examples[j][fsize][0]:
                w[j] = w[j] * math.e ** z[i]
            else:
                w[j] = w[j] * math.e ** -z[i]
        w = normalize(w)
        examples = newSamples(examples, w)
    return h, z

def adaHelper(examplesFilename, hypothesisFilename):
    """
    this is a helper function which calls ada() on given input and writes the
    generated training model onto the given file.
    :param examplesFilename: sample data set
    :param hypothesisFilename: filename of hypothesis

    """
    hypothesisFilename = hypothesisFilename
    ip = examplesFilename
    l = list(range(len(ip[0])-1))
    h, z = ada(ip, 3, l)
    with open(hypothesisFilename, 'x') as hfile:
        hfile.write('adaboost\n')
        hfile.write('hypothesis\n')
        for i in h:
            for j in i:
                for k in j:
                    hfile.write(str(k))
                    hfile.write(',')
                hfile.write(" ")
            hfile.write('\n')
        hfile.write('amt\n')
        for i in z:
            hfile.write(str(i))
            hfile.write('\n')




