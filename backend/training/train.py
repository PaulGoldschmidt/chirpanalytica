#############################
#       TRAINING OF         #
#      CHIRPANALYTICA       #   
#############################

DATA_SIZE = 200000
L2_PENALTY = 1e-3
LEARNING_RATE_INIT = 1e-3
ITERATIONS = 500
LAYER = (1000, 500, 500)
SOLVER = "adam" # adam and lbfgs are recommended
TEST_SIZE = 1/3


# Import all the needed Libs
import csv # Import CSV for reading the tweets
from pathlib import Path # pathlib makes it easier to work with paths
import random
import time
import numpy as np
from datetime import datetime

print("Begin training of neural network for Chirpanalytica. Time of execution: ", end='')
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
starttime = time.perf_counter() # Save time for execution time stats

# read the CSV and create object with tweets
tweets = [] # here are the tweets stored
fractions = [] # and here the fractions

data_folder = Path("data/") # this is the location of the data for training

tweetpath = data_folder / "tweets.csv"

with open(tweetpath, newline='') as data:
    csv_reader = csv.reader(data, delimiter=',')
    line_count = 0 #variable to store the iteration of read lines
    for row in csv_reader:
        fractions.append(row[1])
        tweets.append(row[4])
        line_count += 1
        print("Just read the following tweet: " + row[4])
    print("Read in total " + str(line_count) + " Lines of CSV. " + str(len(tweets)) + " Tweets have been loaded into the system.")


# shuffle data
shuffler = list(zip(fractions, tweets))
random.shuffle(shuffler)
fractions, tweets = zip(*shuffler)

# pick first DATA_SIZE tweets
DATA_SIZE = min(DATA_SIZE, len(fractions))
fractions = fractions[0:DATA_SIZE]
tweets = tweets[0:DATA_SIZE]

data_raw = np.asarray(tweets)
print(str(len(data_raw)) + " tweets loaded!")

import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# Create Bag-Of-Words
print("\nFitting CountVectorizer... ", end='')
count_vect = CountVectorizer()
data_counts = count_vect.fit_transform(data_raw)
print("OK!")


# Create term frequency times inverse document frequency (tf-idf)
print("Fitting Tfidf-Vectorizer... ", end='')
tf_transformer = TfidfTransformer()
data_tf = tf_transformer.fit_transform(data_counts)
print("OK, final data shape: " + str(data_tf.shape))


###
### Convert fractions from str to int
###
labels = []
fractionset = set(fractions) # get unique fractions
fractionsdict = dict() # prepare dictionary
i = 0
for fraction in fractionset: # iterate over unique entrys
	fractionsdict.update({fraction: i}) # insert new dict entry str -> int
	i += 1

for fraction in fractions: 
	labels.append(fractionsdict[fraction]) # change entry in original dataset to int classes

print("Data ready for training.")

###
### Train MLPclassifier
###
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Take 33% of the data for testing
X_train, X_test, y_train, y_test = train_test_split(data_tf, labels, test_size=TEST_SIZE, random_state=42)

# Note that another 10% of the taining data is used as validation data for early_stopping
# Doing so allows the usage of an adaptive learning rate

print("Creating MLPClassifier...")
clf = MLPClassifier(solver=SOLVER, activation='tanh', verbose=True, early_stopping=False,
					hidden_layer_sizes=LAYER, max_iter=ITERATIONS, alpha=L2_PENALTY, learning_rate_init=LEARNING_RATE_INIT)

print("Training ANN (max. " + str(ITERATIONS) + " itr.)...")
clf.fit(X_train, y_train)

###
### Export data
###
import pickle

print("\nExporting data structures:")

print(" -> CountVectorizer")
with open("export/export_count.dat", "wb+") as handle:
	pickle.dump(count_vect, handle)

print(" -> Tf-idf Transformer")
with open("export/export_tfidf.dat", "wb+") as handle:
	pickle.dump(tf_transformer, handle)

print(" -> MLPClassifier")
with open("export/export_clf.dat", "wb+") as handle:
	pickle.dump(clf, handle)

print(" -> Fractions")
with open("export/export_fractions.dat", "wb+") as handle:
	pickle.dump(fractionsdict, handle)


#####################
### Visualization ###
#####################
import itertools
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.  
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, round(cm[i, j], 3),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

###
### Evaluating performance
###
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Naive test error
print("Evaluating performance...")
print("Evaluating performance...", file=open("export/evaluation.txt", "w"))
p_train = clf.predict(X_train)
p_test = clf.predict(X_test)
e_train = np.mean( p_train != y_train )
e_test = np.mean( p_test != y_test )

print("Training error: " + str(e_train))
print("Training error: " + str(e_train), file=open("export/evaluation.txt", "a"))
print("Test error: " + str(e_test))
print("Test error: " + str(e_test), file=open("export/evaluation.txt", "a"))

# Advanced performance analzsis
print("\nTraining data:")
print("\nTraining data:", file=open("export/evaluation.txt", "a"))
print(metrics.classification_report(y_train, p_train, target_names=list(fractionset)))
print(metrics.classification_report(y_train, p_train, target_names=list(fractionset)), file=open("export/evaluation.txt", "a"))
print("\nTest data:")
print("\nTest data:", file=open("export/evaluation.txt", "a"))
print(metrics.classification_report(y_test, p_test, target_names=list(fractionset)))
print(metrics.classification_report(y_test, p_test, target_names=list(fractionset)), file=open("export/evaluation.txt", "a"))
print()
# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test, p_test)
np.set_printoptions(precision=2)

# Plot normalized confusion matrix
print("Creating confusion matrix...") 
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=list(fractionset), normalize=True,
                      title='Normalized confusion matrix (test data)')

plt.savefig("export/confuson.png")


print("End of training. The script took " + str(time.perf_counter() - starttime) + " seconds to execute. \nExiting script.")