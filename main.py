from bs4 import BeautifulSoup
import urllib.request
from nltk import tokenize
from nltk.corpus import stopwords
from bs4.element import Comment

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

login_url = 'https://signup.heroku.com/login'

response = urllib.request.urlopen(login_url)

html = response.read()

soup = BeautifulSoup(html)

links = soup.find_all('a') # Find all links on page
privacy_links = [s for s in links if 'privacy' in str(s)]

privacy_policy_link = privacy_links[0]['href']


response = urllib.request.urlopen(privacy_policy_link)
html = response.read()

text = text_from_html(html)
sentences = tokenize.sent_tokenize(text)


# Find all deletes in privacy policy, grab the sentences that each
# are apart of
deletion_sentences = [s for s in sentences if 'delete' in str(s)]

print(deletion_sentences)

# Match the string ratio against the known strings in the database
# to give us a confidence ratio, then need to have a datapoint
# in DB that gives us grade value of statement


# Figure out if this company has been verified by the pyllama team in knowing that 
