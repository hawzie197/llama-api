from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from api.analyze.classifier import (
    open_classifier,
    get_words,
    get_word_features,
    find_features,
    lemmatize_all_words,
    get_tokenized_sentences,
    get_top_sentences,
    find_features,
)
from urllib.parse import urlsplit
import os
import csv
from fuzzywuzzy import fuzz
import scrapy

# flake8: noqa
BASE = os.path.dirname(os.path.abspath(__file__))
classifier = open_classifier()
ALL_WORDS = get_words()
ROOT = lemmatize_all_words(ALL_WORDS)


def load_fuzzy_corpus():
    fuzzy_data = []
    with open(os.path.join(BASE, "data/corpus.csv")) as fcp:

        reader = csv.reader(fcp)
        for row in reader:
            # action = row[0]
            data = row[2]
            fuzzy_data.append(data)
    return fuzzy_data


def test_corpus(corpus, check):
    sum_ = 0
    best = ""
    max_ratio = -1
    ratios = []
    for line in corpus:
        ratio = fuzz.ratio(check, line)  # normalize(line)
        ratios.append(ratio)
    return ratios


def tag_visible(element):
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
    ]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    """
    Gets all raw text from html, removing all tags.

    :param body: html
    :return: str
    """
    soup = BeautifulSoup(body, "html.parser")
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)


def normalize_link(link, base_url):
    """
    Break the base_uri and piracy policy path apart and rebuild
    the link to ensure it contains all the necessary http elements.
    
    :param link:  html link tag w/ href
    :param split_url: split url  (urlib.parse)
    :return: string
    """
    split_url = urlsplit(base_url)
    protocol = split_url.scheme + "://"
    netloc = split_url.netloc
    final_url = ""
    if not protocol in link:  # Protocol doesn't exists, lets make sure that gets added.
        final_url += protocol
    if not netloc in link:
        final_url += netloc + "/"

    if link.startswith("/"):
        final_url += link[1:]
    else:
        final_url += link

    return final_url


def find_privacy_policy_url(resp, url):
    """
    Find the privacy policy url for the page. If no
    policy url is found, return None
    :param url: str
    :return: str or None
    """
    html = driver.page_source
    soup = BeautifulSoup(html)
    links = soup.find_all("a", href=True)
    policies = dict()
    for link in links:
        comparisons = ("Privacy Policy", "Data Policy")
        ratios = [fuzz.token_sort_ratio(link.text, c) for c in comparisons]
        policies[max(ratios)] = link["href"]

    best_match = policies[max(policies, key=int)]
    return normalize_link(best_match, url)


def load_keywords():
    """
    Load in all keywords from a text file.
    :return: set()
    """
    keywords = set()
    with open(os.path.join(BASE, "data/keywords.txt")) as fp:
        for line in fp:
            keywords.add(line.strip().lower())
    return keywords


def load_actions_key(action):
    """
    Load in all actions from text file.
    :return: set()
    """
    actions = set()
    with open(os.path.join(BASE, "data/actions/" + action + ".txt")) as fp:
        for line in fp:
            actions.add(line.strip().lower())
            actions.add(line.strip().lower().capitalize())
    return actions


def load_actions():
    """
    Load in all actions from text file.
    :return: set()
    """
    actions = set()
    with open(os.path.join(BASE, "data/actionable_keywords.txt")) as fp:
        for line in fp:
            actions.add(line.strip().lower())
    return actions


def load_delete_corpus():
    """
    Load in the delete corpus.
    """
    corpus = set()  # set<list<action, status, sentence>>
    with open(os.path.join(BASE, "data/corpus.csv")) as fp:
        for line in fp:
            corpus.add(line.split(","))
    return corpus


def get_classifier_result(action, text):
    all_words = get_words()
    features = get_word_features(all_words)

    keywords = load_keywords()
    all_actions = dict()
    all_actions[action] = load_actions_key(action)
    results = get_data(text, keywords, all_actions[action])
    classified = []
    for word in results:
        classifier_result = verify_statement(results[word], features)
        classified.append((" ".join(results[word]), classifier_result))
    return classified


def get_fuzzy_result(action, text):
    all_actions = {}
    action_map = {}

    all_actions[action] = load_actions_key(action)
    for act in all_actions[action]:
        action_map[act] = action
    result = get_data(text, all_actions[action], action)
    data = load_fuzzy_corpus()
    best_statement = ""
    best_ratio = -1
    all_lines = {}
    action = action_map[action]

    for index in range(len(result[action])):
        line = result[action][index]

        ratios = test_corpus(data, line)
        if max(ratios) > best_ratio:
            best_statement = line
            best_ratio = max(ratios)
        all_lines[line] = ratios
    features = get_word_features(ALL_WORDS)
    classifier_result = verify_statement(best_statement, features)
    action_map = dict(
        type=action.title(),
        quote=best_statement,
        confidence=best_ratio,
        classification=classifier_result,
    )

    return action_map


def verify_statement(statement, featureset):
    feature = find_features(statement, featureset)
    result = classifier.classify(feature)
    # TODO if result is 1 maybe add to training data
    return result


def get_data(text, actions, action):
    all_sentences = get_tokenized_sentences(text)
    all_words = []
    sentence_map = defaultdict(list)
    for idx, sentence in enumerate(all_sentences):
        for word in sentence.split():
            all_words.append(word)
            sentence_map[word].append(idx)

    wnl = WordNetLemmatizer()
    index = 0
    end = len(all_words)
    # action_idx = [] # TODO tolerance calculations
    results = defaultdict(list)
    actions = load_actions_key(action)
    used = set()
    actions = set(actions)
    for index in range(len(all_words)):
        word = all_words[index]
        if word not in actions:
            continue
        if word not in ROOT:
            ROOT[word] = wnl.lemmatize(word, "v")
        root = ROOT[word]
        #
        # back = max(0, index - tolerance)
        # # TODO tolerance value should be calculated based on existing data sets
        # front = min(len(all_words) - 1, index + tolerance)
        # sentence_containing_action = " ".join(all_words[back:front+1])
        if word not in used or root not in used:
            for idx in sentence_map[word]:
                results[action].append(all_sentences[idx])
            # results[root].append(sentence_containing_action)
            used.add(word)
            # used.add(root)
    # ranked = rank_results(results)
    return results


def rank_results(results):
    ranked = None
    for word in results:
        ranked = get_top_sentences(results[word], word)
    return ranked
