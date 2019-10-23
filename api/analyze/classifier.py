import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.data import load
import random
import csv
import os
import pickle

BASE = os.path.dirname(os.path.abspath(__file__))
nltk.data.path.append(os.path.join(BASE, "data/nltk_corpora"))
TOKENIZER = load("tokenizers/punkt/english.pickle")
# flake8: noqa
def strip_non_an_characters(word):
    reconstructed = ""
    for letter in word:
        if letter.isalnum():
            reconstructed += letter
    return reconstructed


def sort_by_action(element, action):
    item = element[1]
    if action not in item:
        return 0
    else:
        return item[action]


def get_top_sentences(sentences, action):
    pass
    # counts = [(sentence, get_key_word_count(sentence)) for sentence in sentences]
    # return sorted(counts, key = lambda x: 0 if action not in x else x[action],
    # reverse = True )


def get_key_word_count(sentence):
    count = {}
    for word in sentence.split():
        word = word.strip().lower()
        word = strip_non_an_characters(word)
        if word not in count:
            count[word] = 0
        count[word] += 1


def construct_corpus_from_csv(csv_data):
    corpus = []
    with open(csv_data) as data:
        reader = csv.reader(data)
        for row in reader:
            """TODO action row[0] fix it"""
            status = row[1]
            sentence = row[2]
            words = []
            for word in sentence.split():
                words.append(word)
            corpus.append((words, status))
    random.shuffle(corpus)
    return corpus


def find_features(document, word_features):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = w in words
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
    corpus = construct_corpus_from_csv(os.path.join(BASE, "data/corpus.csv"))
    all_words = get_all_words(corpus)
    return all_words


def get_word_features(all_words):
    return list(all_words.keys())


def lemmatize_all_words(all_words):
    root = {}
    lemmatizer = WordNetLemmatizer()
    for word in all_words:
        if word not in root:
            root[word] = lemmatizer.lemmatize(word, "v")
    return root


def get_word_to_sentence_mapping(text, words):
    pass


def get_tokenized_sentences(text):
    return TOKENIZER.tokenize(text)


def main():
    corpus = construct_corpus_from_csv(os.path.join(BASE, "data/delete-data.csv"))
    all_words = get_all_words(corpus)
    # lemmatize training data
    lemmatize_all_words(all_words)
    word_features = list(all_words.keys())
    feature_set = [
        (find_features(datum, word_features), status) for datum, status in corpus
    ]
    train_and_save_classier(feature_set)
    classifier = open_classifier()
    # print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier,
    #                                                             test_set)) * 100)
    print(
        classifier.prob_classify(
            find_features(
                "'When you delete your account, "
                "we delete things you have posted, "
                "such as your photos and status updates, "
                "and you won't be able to recover that information later.'",
                word_features,
            )
        ).samples()
    )
    # print(get_tokenized_sentences(TEXT))


TEXT = """
Introduction
Thanks for using our products and services ("Services"). The Services are provided by Immuto, Inc. ("Immuto"), located at 2035 Sunset Lake Road Suite B-2, Newark, DE 19702, USA.

By using our Services, you are agreeing to these terms. Please read them carefully.

Our Services are very diverse, so sometimes additional terms or product requirements (including age requirements) may apply. Additional terms will be available with the relevant Services, and those additional terms become part of your agreement with us if you use those Services.

Using our services
You must follow any policies made available to you within the Services.

Don't misuse our Services. For example, don't interfere with our Services or try to access them using a method other than the interface and the instructions that we provide. You may use our Services only as permitted by law, including applicable export and re-export control laws and regulations. We may suspend or stop providing our Services to you if you do not comply with our terms or policies or if we are investigating suspected misconduct.

Using our Services does not give you ownership of any intellectual property rights in our Services or the content you access. You may not use content from our Services unless you obtain permission from its owner or are otherwise permitted by law. These terms do not grant you the right to use any branding or logos used in our Services. Don't remove, obscure, or alter any legal notices displayed in or along with our Services.

Privacy and copyright protection
Immuto's privacy policies explain how we treat your personal data and protect your privacy when you use our Services. By using our Services, you agree that Immuto can use such data in accordance with our privacy policies.

We respond to notices of alleged copyright infringement and terminate accounts of repeat infringers according to the process set out in the U.S. Digital Millennium Copyright Act.

We provide information to help copyright holders manage their intellectual property online. If you think somebody is violating your copyrights and want to notify us, you can find information about submitting notices and Immuto's policy about responding to notices in our contact page.

Your content in our services
Some of our Services allow you to upload, submit, store, send or receive content. You retain ownership of any intellectual property rights that you hold in that content. In short, what belongs to you stays yours.

When you upload, submit, store, send or receive content to or through our Services, you give Immuto (and those we work with) a worldwide license to use, host, store, reproduce, modify, create derivative works (such as those resulting from translations, adaptations or other changes we make so that your content works better with our Services), communicate, publish, publicly perform, publicly display and distribute such content. The rights you grant in this license are for the limited purpose of operating, promoting, and improving our Services, and to develop new ones. This license continues even if you stop using our Services (for example, for a business listing you have added to Immuto Maps). Some Services may offer you ways to access and remove content that has been provided to that Service. Also, in some of our Services, there are terms or settings that narrow the scope of our use of the content submitted in those Services. Make sure you have the necessary rights to grant us this license for any content that you submit to our Services."""


def main():
    corpus = construct_corpus_from_csv(os.path.join(BASE, "data/delete-data.csv"))
    all_words = get_all_words(corpus)
    word_features = list(all_words.keys())
    feature_set = [
        (find_features(datum, word_features), status) for datum, status in corpus
    ]
    half = len(feature_set) // 2
    train_and_save_classier(feature_set[:half])
    classifier = open_classifier()
    test_set = feature_set[half:]
    print(
        "Classifier accuracy percent:",
        (nltk.classify.accuracy(classifier, test_set)) * 100,
    )


if __name__ == "__main__":
    main()
