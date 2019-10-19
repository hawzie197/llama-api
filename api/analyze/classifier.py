import nltk
import random
import csv
import os
import pickle
BASE = os.path.dirname(os.path.abspath(__file__))
#ALL_WORDS = get_words()
def construct_corpus_from_csv(csv_data):
    corpus = []
    with open(csv_data) as data:
        reader = csv.reader(data)
        for row in reader:
            action = row[0]
            status = row[1]
            sentence = row[2]
            words = []
            for word in sentence.split():
                words.append(word)
            corpus.append((words, status))
    #random.shuffle(corpus)
    #print(corpus[0])
    return corpus

def find_features(document, word_features):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

def get_all_words(corpus):
    words = []
    for datum in corpus:
        for word in datum[0]:
            words.append(word)

    all_words = nltk.FreqDist(words)
    return all_words
def train_and_save_classier(feature_set):
    classifier = nltk.NaiveBayesClassifier.train(feature_set)
    save_classifier = open(os.path.join(BASE, "data/classifier.pickle"), "wb")
    pickle.dump(classifier, save_classifier)
    save_classifier.close()


def open_classifier():
    classifier_file = open(os.path.join(BASE, "data/classifier.pickle"), "rb")
    classifier = pickle.load(classifier_file)
    classifier_file.close()
    return classifier

def get_words():
    corpus = construct_corpus_from_csv(os.path.join(BASE, "data/delete-data.csv"))
    all_words = get_all_words(corpus)
    return all_words

def get_word_features(all_words):
    return list(all_words.keys())

def main():
    corpus = construct_corpus_from_csv(os.path.join(BASE, "data/delete-data.csv"))
    all_words = get_all_words(corpus)
    word_features = list(all_words.keys())
    feature_set = [(find_features(datum,word_features), status) for datum, status in corpus]
    train_and_save_classier(feature_set)



    # result = classifier.classify(find_features(list("We won't do anything".split()), word_features))
    # print((result))
    #print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier, test_set)) * 100)
    #print(classifier.show_most_informative_features(15))


if __name__ == "__main__":
    main()