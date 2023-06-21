import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

# doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')
# print([(X.text, X.label_) for X in doc.ents])

from bs4 import BeautifulSoup
import requests
import re
def url_to_string(url):
    res= requests.get(url)
    html= res.text
    soup= BeautifulSoup(html,'html5lib')
    for script in soup(["script","style",'aside']):
        script.extract()
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))
ny_bb= url_to_string('https://www.bbc.com/news/world-us-canada-45173015')
print(ny_bb)
article = nlp(ny_bb)
# print(len(article.ents))
# labels = [x.label_ for x in article.ents]
# print(Counter(labels))

sentences = [x for x in article.sents]
print(sentences[20])
displacy.render(nlp(str(sentences [20])), jupyter= True, style='ent')
