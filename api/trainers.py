# flake8: noqa

from flask import Flask, jsonify, request
from datetime import datetime
import requests
from google.cloud import language, storage
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from bs4 import BeautifulSoup
from gensim.summarization import summarize

import urllib.request

app = Flask(__name__)


@app.before_first_request
def startup():
    nltk.download("wordnet")
    storage.Client.from_service_account_json("./PlainPrivacyGoogle.json")


@app.route("/")
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400" />
    """.format(
        time=the_time
    )


# @app.route('/parse', methods=['GET'])
# def main():
#     url = request.args['url']
#     html = readUrl(url)
#     language_client = language.LanguageServiceClient()
#
#     document = language.types.Document(
#         content=html,
#         type=language.enums.Document.Type.HTML)
#
#     entities = language_client.analyze_entities(document).entities
#     sally = {}
#     for entity in entities:
#         word = entity.name.lower()
#         score = sally.get(word, 0)
#         score += entity.salience
#         sally[word] = score
#
#     sorted_sally = sorted(sally.items(), key=operator.itemgetter(1), reverse=True)
#
#     # for word, score in sorted_sally:
#     #     print('=' * 20)
#     #     print(u'{:<16}: {}'.format('name', word))
#     #     print(u'{:<16}: {}'.format('score', score))
#
#     return jsonify(sorted_sally[:3])


@app.route("/analyzeUrl")
def analyzeUrl():
    # print("begin analysis...")
    # request.args["url"]
    text = readUrl(request.args["url"])
    # print("received text...")
    if not text:
        text = readUrl2(request.args["url"])
        if not text:
            formattedResults = "We are unable to run our analysis on this website"
        else:
            formattedResults = collectResults(text)
    else:
        formattedResults = collectResults(text)
    # print("received results...")

    summary = findPhrase(text)

    compiledResults = {"results": formattedResults, "summary": summary}
    return jsonify(compiledResults)


def readUrl2(urlString):
    try:
        urlFile = urllib.request.urlopen(urlString)
        bytesHtml = urlFile.read()
        htmlString = bytesHtml.decode("utf8")
        soup = BeautifulSoup(htmlString)
        text = soup.get_text()
        return text
    except Exception:
        return False


def readUrl(urlString):
    resp = requests.get(urlString)
    if resp.ok:
        soup = BeautifulSoup(resp.text)
        return soup.get_text()
    else:
        return False


# builds keywords set from text file
def buildKeywords():
    keywords = set()
    with open("keywords.txt") as fp:
        for line in fp:
            keywords.add(line.strip().lower())
    return keywords


# builds actions set from text file
def buildActions():
    actions = set()
    with open("actionable_keywords.txt") as fp:
        for line in fp:
            actions.add(line.strip().lower())
    return actions


# not being used at the moment
def findOccurences(docText, keywords, actions):
    wordToList = {}
    index = 0
    for word in docText.split():
        if word in keywords or word in actions:
            occurs = wordToList.get(word, [])
            occurs.append(index)
            wordToList[word] = occurs
        index = index + 1
    return wordToList


def backAndForth(docText, keywords, actions, tolerance, sally):
    score = 0
    index = 0
    allWords = docText.split()

    results = {}
    wnl = WordNetLemmatizer()

    for word in allWords:
        if word in actions:
            back = max(0, index - tolerance)
            front = min(len(allWords) - 1, index + tolerance)
            spot = back
            while spot <= front:
                check = allWords[spot]
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


def find_sally(text, keywords):
    keywords = buildKeywords()
    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text, type=language.enums.Document.Type.PLAIN_TEXT
    )

    entities = language_client.analyze_entities(document).entities
    sally = {}
    for entity in entities:
        word = entity.name.lower()
        if word in keywords or word + "s" in keywords:
            score = sally.get(word, 0)
            score += entity.salience
            sally[word] = score

    return sally


def collectResults(text):
    tolerance = 60
    actions = buildActions()
    keywords = buildKeywords()
    # sally = find_sally(text, keywords)
    results = backAndForth(text, keywords, actions, tolerance, {})
    return formatResults(results)


def formatResults(result):
    formatted = {}
    for key in result:
        if key[0] not in formatted:
            formatted[key[0]] = []
        insertVal = mapKeyword(key[1])
        formatted[key[0]].append(insertVal)
    return formatted


def mapKeyword(keyword):
    if keyword == "credit":
        return "credit card information"
    elif keyword == "debit":
        return "debit card information"
    elif keyword == "mobile":
        return "mobile device information"
    elif keyword == "third":
        return "to third party apps"
    elif keyword == "ip":
        return "IP address"
    elif keyword == "computer":
        return "computer information"
    elif keyword == "transaction":
        return "transaction data"
    elif keyword == "preferences":
        return "user preferences"
    elif keyword == "photo":
        return "photo(s)"
    elif keyword == "device":
        return "device information"
    elif keyword == "phone":
        return "phone specs"
    elif keyword == "cookie":
        return "cookies"
    elif keyword == "sex":
        return "gender"
    elif keyword == "passport":
        return "passport information"

    return keyword


def buildOtherKeywords():
    keywords = set()
    with open("WhyKeywords.txt") as fp:
        for line in fp:
            keywords.add(line.strip().lower())
    return keywords


def findPhrase(docText):
    keywords = buildOtherKeywords()
    part = int(len(docText) / 5)
    docText = docText[part:]
    noHeaderText = docText.lower()
    whyList = []
    for key in keywords:
        key = key.strip("\n")
        if noHeaderText.find(key) != -1:
            print(key)
            position = noHeaderText.index(key)
            splitList = (docText[position - 1 :]).split(".")
            finalString = ""
            for sentence in splitList[:7]:
                sentence = sentence.strip()
                finalString = finalString + sentence + ". "
            whyList.append(summarize(finalString))

    finalString = ""
    for sentence in whyList:
        finalString = finalString + sentence + " "

    if finalString == "":
        finalString = "We cannot provide a summary for this website's privacy policy."

    return finalString


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
