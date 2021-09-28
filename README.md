# Language-Classifier #

## LEKHYA RAO MUMMAREDDY ##
Description of the algorithms used in this problem.

***1. Decision Tree:***
this algorithm takes as input-
- Sample data set: which consists of boolean values for each attribute and the
corresponding classification for each sample in the data set.
-Atrributes: List of attributes, based on which the sample data set is created.
These attributes help in the classification of a given dataset.
- Parent examples: List of examples classified according to the parent of the
current attribute.
The algorithm performs the following stepsin order to generate a training model
i.e a decision tree.
(i) from the list of available attributes, pick one that helps seggregate the samples
the most. This attribute can be identified by calculating the information gain of
all attributes. The attribute with the maximum value of information gain is
selected.

***Gain(A) = B( p/p+n) − Remainder (A)*** .

***Remainder (A) =summation(pk+nk/p+n * B( pk/pk+nk)*** .
where k ranges from 0 to no. of values of attribute A.

***B(q)=−(q log2 q + (1 − q) log2(1 − q))***
and B is the entropy of a boolean variable.

(ii) based on the values of the attribute, create a subset of samples according to
the corresponding value of the selected attribute.
(iii) perform the alorithm recursively to form the decision tree
(iv) the above steps are repeated until one of the following situations occurs:
all the remaing examples belong to the same classification, in this case, the
classification is returned.
there are no more samples left to further enhance the decision tree, in this
case, the majority of the parent attributes' classifications is returned.
there are no more attributes left, in this case again the majority of the
parent attributes' classifications is returned.
- The decision tree is saved in the form of a list. The list is traversed in the manner
decsribed below in order to predict the classification for a given input.
Starting at beginning of the list, the first atrribute's value is checked in the given
input, if this values is not the same as given in the list , then we search down the
list until we find an entry which has the given attribute and the corresponding
value that matches that of given input.
Once a match is found, we continue traversing the list. This process is repeated,
until an entry is found such that it contains a classification. This represents a leaf
node in the tree.
The path from an entry till the classication represents the subtree with the start
entry as the root node.
This way, classifcation for a given input can be predicted once the decision tree is
bulit.

***2. Ada Boost:***
This algorithm is based on building multiple weak classifiers, also known as
decision stumps which are decision trees of depth 
1. Each classifer is assigned
some significance(amount of say) and the majority of the weighted sum of the
predictions of the classifiers in accordance to their amout of say is used to
determine the final prediction.
This is done using the following steps:
(i) The input to he algorithms is
- examples: data set to build the training model
- L: learning algorithm to generate the decision stumps.
- k: no. of classifiers.

(ii) initially, the error is zero and the weights of the sample are initialized to 1/no.
of samples.

(iii) using the decision tree algorith, a decision tree of depth 1 is generated.

(iv) for each sample, the prediction of the classifier is obtained and this is
compared with the actual classification specified.

(v) error is updated to sum of weights of incorrectly classified samples.

(vi) the amount of say for the classifier is computed using:
z = log((1-error)/error)

(vii) the weights of incorrectly classified samples are increased to
wj = wj· e^z where 0<j<size of sample set
                            
(viii) the weights of correctly classified samples are decreased to
wj = wj· e^-z where 0<j<size of sample set
                             
(ix) a new sample set of same size as the original sample set is created by
randomly selecting a number between 0 and 1 and picking the sample which lies
in this range. Due to the higher weight of the incorrectly classified samples, their
range is wider and hence they have a greater chance of being included in the new
sample set.
                             
(x) based on the new weights and the new sample set, the entire process is
repeated again. for k times where k is the number of classifiers.
It can be observed that eachclassifier is built on the basis of the performance of
the previous classifier.
                             
The list of classifiers and their corresponding amout of say represents the training
model of this algorithm.
- In order to make a prediction, for a given sample the predictions of all classifiers
are computed and scaled to integer factors. In this case, german is considered as 1
(positive) and english is considered as -1 (negative).
The sum of products of these prediction values and amount of say each classifiers
is them checked for proximity between 1 and -1. The value it is closer to
represents the classification of the sample.
In this way, predictions can be made for given input.

***Feature List:***
This algorithm makes use of the following features:
1. Does the sentence contain the word 'de' : which translates to the word 'the' in
Dutch. This is one of the most commonly used words in a language and is not
used in English. Hence it can be used to differentiate between the wo languages.
2. Does the sentence contain the word 'the': this word is very frequently used in
english and is not present in Dutch. Hence it can be used to differentiate between
the two languages.
3.Does the sentence contain the word 'and': a commonly used word in English and
not in German.
4. Does the sentence contain the word 'und' ( and in German) commonly used in
German.
5. Does the sentence contain the word 'to': commonly used in English English
and not in German.
6. Does the sentence contain the word 'an' or 'a': commonly used in English
English and not in German.
7.Does the sentence contain the word 'en' or 'een' : commonly used in German
and not in English.
8. Does the sentence contain the word 'aan': commonly used in German
commonly used in German and not in English.
9. Average length of words greater than 4?: the average length of words is
generally higher in German than in English. Here, if the average word length for a
sentence is greater than 4, it is considered to be German, otherwise English.
Each feature is assignmed a value True or False for each sample and this feature
set acts as an input to the two algorithms inorder to train the prediction models.
