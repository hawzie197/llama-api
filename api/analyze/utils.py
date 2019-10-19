from bs4 import BeautifulSoup
import urllib.request
from bs4.element import Comment
from fuzzywuzzy import fuzz
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.summarization import summarize
from collections import defaultdict
from api.analyze.classifier import open_classifier, get_words, get_word_features, find_features
import os


BASE = os.path.dirname(os.path.abspath(__file__))
classifier = open_classifier()

ALL_WORDS = None #TODO in memory or shared?

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


def get_site_html(url: str):
    """
    Parses a url and downloads all html from the page.

    :param url: str
    :return: html
    """
    response = urllib.request.urlopen(url)
    return response.read()


def get_site_tags(html, tags=["a"]):
    """
    Build out a list of all html tags containing only tags
    existing in the tags parameter.

    :param: html: str
    :param: tags: list<str>
    """
    soup = BeautifulSoup(html)

    # For each of the wanted tags, parse out the tags from the web-page
    links = list()
    for t in tags:
        links.extend(soup.find_all(t))
    return links


def find_privacy_link(links):
    """
    Find the link with the highest chance of matching Privacy Policy. If the
    link does not contain Privacy or policy in it, it definitely is not a privacy policy

    :param links: list<str>
    :return: Link or None
    """
    policies = dict()
    for link in links:
        link_contents = link.contents
        if len(link_contents) > 0:
            ratio1 = fuzz.token_sort_ratio(link_contents[0], "Privacy Policy")
            ratio2 = fuzz.token_sort_ratio(link_contents[0], "Data Policy")
            if ratio1 > ratio2:
                policies[ratio1] = link
            else:
                policies[ratio2] = link

    link = policies[max(policies, key=int)]
    privacy_exists = all([t in str(link).lower() for t in ("privacy",)])
    data_policy_exists = all([t in str(link).lower() for t in ("data", "policy")])
    if not any([privacy_exists, data_policy_exists]):
        return None
    return link


def get_privacy_policy_url(url):
    """
    Find the privacy policy url for the page. If no
    policy url is found, return None
    :param url: str
    :return: str or None
    """
    html = get_site_html(url=url)  # Find page html
    links = get_site_tags(html=html, tags=["a"])  # Get all links on page
    privacy_policy_link = find_privacy_link(
        links=links
    )  # Find privacy link, if None, research on homepage
    return privacy_policy_link.get("href", None)


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

def load_delete_actions():
    """
    Load in all actions from text file.
    :return: set()
    """
    actions = set()
    with open(os.path.join(BASE, "data/delete.txt")) as fp:
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
    with open(os.path.join(BASE, "data/delete-data.csv")) as fp:
        for line in fp:
            corpus.add(line.split(","))
    return corpus


def load_other_keywords():
    """
    Load in all other keywords
    :return:
    """
    keywords = set()
    with open(os.path.join(BASE, "data/why_keywords.txt")) as fp:
        for line in fp:
            keywords.add(line.strip().lower())
    return keywords

def get_classifier_result(text):
    all_words = get_words()
    features = get_word_features(all_words)

    tolerance = 60
    actions = load_actions() #TODO
    keywords = load_keywords()
    all_actions = {}
    all_actions["delete"] = load_delete_actions()
    results = get_data(text, keywords, all_actions["delete"], tolerance)
    classified = []
    for word in results:
        classifier_result = verify_statement(results[word], features)
        classified.append((" ".join(results[word]), classifier_result))
    return classified

def parse_main_points(text):
    all_words = get_words()
    features = get_word_features(all_words)

    tolerance = 60
    actions = load_actions()
    keywords = load_keywords()
    # sally = find_sally(text, keywords)
    results = back_an_forth(text, keywords, actions, tolerance, {})
    return format_results(results)

def verify_statement(statement, featureset):
    feature = find_features(statement, featureset)
    result = classifier.classify(feature)
    #TODO if result is 1 maybe add to training data
    return result

def get_data(text, keywords, actions, tolerance):
    all_words = text.split()
    wnl = WordNetLemmatizer()
    index = 0
    end = len(all_words)
    action_idx = []
    results = defaultdict(list)
    while index < end:
        word = all_words[index]
        root = WordNetLemmatizer.lemmatize(word, "v")
        back = max(0, index - tolerance)  # TODO tolerance value should be calculated based on existing data sets
        front = min(len(all_words) - 1, index + tolerance)
        sentence_containing_action = " ".join(all_words[back:front+1])
        if word in actions:
           results[word].append(sentence_containing_action)
        elif root in actions:
            results[root].append(sentence_containing_action)
        index += 1
    return results

def back_an_forth(text, keywords, actions, tolerance, sally):
    score = 0
    index = 0
    all_words = text.split()

    results = {}
    wnl = WordNetLemmatizer()

    for word in all_words:
        if word in actions:
            back = max(0, index - tolerance)
            front = min(len(all_words) - 1, index + tolerance)
            spot = back
            while spot <= front:
                check = all_words[spot]
                if check in keywords:
                    # print(word + ':' + check)
                    key = wnl.lemmatize(word, "v")
                    if (key, check) not in results:
                        results[key, check] = True
                    dist = abs(index - spot)
                    weight = sally.get(check, 0)
                    score = score + ((1 / dist) * weight)
                elif check + "s" in keywords:
                    # print(word + ':' + check + 's')
                    key = wnl.lemmatize(word, "v")
                    if (key, check) not in results:
                        results[key, check] = True

                    dist = abs(index - spot)
                    weight = sally.get(check, 0)
                    score = score + ((1 / dist) * weight)
                spot = spot + 1
        index = index + 1
    return results


def format_results(results):
    """
    Format the results to be more human readable.

    :param results: dict
    :return: dict
    """
    formatted = dict()
    for key in results:
        if key[0] not in formatted:
            formatted[key[0]] = list()
        insert_val = expand_keyword(key[1])
        formatted[key[0]].append(insert_val)
    return formatted


def expand_keyword(keyword):
    """
    May a keyword to a general phrase to expand the term.

    :param keyword: str
    :return: str
    """

    key_phrases = dict(
        credit="credit card information",
        debit="debit card information",
        mobile="mobile device information",
        third="to third party apps",
        ip="IP address",
        computer="computer information",
        transaction="transaction data",
        preferences="user preferences",
        photo="photo(s)",
        device="device information",
        phone="phone specs",
        cookie="cookies",
        sex="gender",
        passport="passport information",
    )
    if keyword in key_phrases.keys():
        return key_phrases[keyword]
    return ""


def parse_summary(text):

    keywords = load_other_keywords()
    part = int(len(text) / 5)
    text = text[part:]
    no_header_text = text.lower()
    why = list()
    for key in keywords:
        key = key.strip("\n")
        if no_header_text.find(key) != -1:
            print(key)
            position = no_header_text.index(key)
            split_list = (text[position - 1 :]).split(".")
            f = ""
            for sentence in split_list[:7]:
                sentence = sentence.strip()
                f += f"{sentence}. "
            why.append(summarize(f))

    final = ""
    for sentence in why:
        final += f"{sentence} "  # Keep space

    if not final or final == "":
        return "We cannot provide a summary for this website's privacy policy."

    return final


# def find_sally(text, keywords):
#     keywords = buildKeywords()
#     language_client = language.LanguageServiceClient()
#
#     document = language.types.Document(
#         content=text, type=language.enums.Document.Type.PLAIN_TEXT
#     )
#
#     entities = language_client.analyze_entities(document).entities
#     sally = {}
#     for entity in entities:
#         word = entity.name.lower()
#         if word in keywords or word + "s" in keywords:
#             score = sally.get(word, 0)
#             score += entity.salience
#             sally[word] = score
#
#     return sally
