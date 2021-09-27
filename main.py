import string
import sys
import decisionTree
import adaBoost


def trainingsetProcess(filename):
    """
    given a filename, this method creates a list of samples
    and their classifications to be used for training the model.
    :param filename: filename of training data
    :return: list of samples and their classifications
    """
    samples = []
    op = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            l = line.split('|')
            op.append(l[0])
            samples.append(l[1])
    return samples, op


def testProcess(filename):
    """
    given a testing file name, this method creates a processed list of
    samples in the file.
    :param filename: testing file name
    :return: processed list of samples
    """
    s = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            s.append(line)
    return s


def check(s, l):
    """
    given a word s and a list l, the method returns true if
    s is in l, else false.
    :param s: word
    :param l: list
    :return: True or False

    """
    if s in l:
        return True
    else:
        return False


def checkk(s1, s2, l):
    """
    given 2 words and a list, this method returns true if one of the words
    is in the list. It returns false when both values are not in the list.
    :param s1: word1
    :param s2: word2
    :param l: list
    :return: True or False
    """
    if s1 in l or s2 in l:
        return True
    else:
        return False


def avgLen(l):
    """
    given a sentence l, this method returns True if avg word length
    is greater than 4; else False
    :param l: sentence
    :return: True or False
    """

    avg = 0
    p = string.punctuation
    for word in l:
        for c in p:
            word = word.replace(c, '')
        avg += len(word)
    if avg / len(l) > 4:
        return True
    else:
        return False


def features(samples):
    """
    given a lit of sample data, this method processes the data based on
    predetermined features for the data.
    :param samples: sample data set
    :return: feature map
    """
    f = []
    for line in samples:
        entry = []
        l = line.split(" ")
        entry.append(check('de', l))
        entry.append(check('to', l))
        entry.append(check('und', l))
        entry.append(check('and', l))
        entry.append(check('aan', l))
        entry.append(checkk('a', 'an', l))
        entry.append(checkk('en', 'een', l))
        entry.append(check('the', l))
        entry.append(avgLen(l))
        f.append(entry)
    return f


def adaboosthyp(filename):
    """
    given a hypothesis file for adaboost, this method extracts the list of
    classifiers and amount of say from the file
    :param filename: hypothesis file
    :return: the list of classifiers and amount of say
    """
    h = []
    z = []
    with open(filename) as f:
        f.readline()
        f.readline()
        for line in f:
            if line.strip() == 'amt':
                break
            ex = line.strip().split(" ")
            new = []
            for i in range(len(ex)):
                l = ex[i].split(',')
                new.append(l[0:len(l) - 1])
            h.append(new)
        for line in f:
            z.append(float(line.strip()))
        return h, z


def decisionhyp(filename):
    """
    given a hypothesis file for decision tree, this method extracts the decision tree from the file
    :param filename: hypothesis file
    :return: decision tree
    """

    sol = []
    with open(filename) as f:
        f.readline()
        for line in f:
            ex = line.strip().split(" ")
            sol.append(ex)
    return sol


def processHypothesis(ip, filename):
    """
    given testing data set and hypothesis file, this method
    identifies the type of learning and extracts the training model
    in order to make the predictions.
    :param ip: testing data set
    :param filename: hypothesis file
    """
    with open(filename) as f:
        line = f.readline()
        if line.strip() == 'adaboost':
            h, z = adaboosthyp(filename)
            adaBoost.correct(ip, h, z)
        else:
            sol = decisionhyp(filename)
            decisionTree.correct(ip, sol)


if __name__ == '__main__':
    args = sys.argv
    if args[1] == 'train':
        examplesFilename = args[2]
        hypothesisFilename = args[3]
        learningType = args[4]
        s, o = trainingsetProcess(examplesFilename)
        f = features(s)
        for i in range(len(f)):
            f[i].append(o[i][0])
        if learningType == 'dt':
            decisionTree.decisionHelper(f, hypothesisFilename)
        else:
            adaBoost.adaHelper(f, hypothesisFilename)
    else:
        hypothesisFilename = args[2]
        testFilename = args[3]
        s = testProcess(testFilename)
        f = features(s)
        processHypothesis(f, hypothesisFilename)
