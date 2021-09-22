import sys
import pickle
import json

###
# Load logic
###
clf = None
count = None
fractions = None
tf_transformer = None

with open("../training/export/export_count.dat", "rb") as handle:
    count = pickle.load(handle)

with open("../training/export/export_tfidf.dat", "rb") as handle:
    tf_transformer = pickle.load(handle)

with open("../training/export/export_clf.dat", "rb") as handle:
    clf = pickle.load(handle)

with open("../training/export/export_fractions.dat", "rb") as handle:
    fractions = pickle.load(handle)


def predict(tweet):
    # Predict: vectorize
    features = tf_transformer.transform(
        count.transform({tweet})).toarray()
    prediction = clf.predict_proba(features)
    results = {}

    for key, value in fractions.items():
        # Python's range is specified with exclusive upper bound
        for i in range(0, len(clf.classes_) - 1 + 1):
            if clf.classes_[i] == value:
                results[key] = prediction[0][i]
    return results


# Only executed when called manually
if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print('Illegal arguments!')
        exit()

    tweet = sys.argv[1]
    print(json.dumps(predict(tweet)))
