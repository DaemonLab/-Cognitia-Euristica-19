# information-extraction.py

import re
import nltk
from nltk.corpus import stopwords
import json

stop = stopwords.words('english')

string = """
Hey,
This week has been crazy. Attached is my report on IBM. Can you give it a quick read and provide some feedback.
Also, make sure you reach out to Claire (claire@xyz.com).
You're the best.
Cheers,
George W.
212-555-1234
"""

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
#     print(sentences)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

if __name__ == '__main__':
    #Pass the name of text file in argument of open
    f=open('Abbas- MS Dyna.txt')
    raw=f.read()
    f.close()
    numbers = extract_phone_numbers(raw)
    emails = extract_email_addresses(raw)
    names = extract_names(raw)
    data={}
    data['name']=[names[0]]
    data['email']=emails
    data['phone']=numbers
    #This will create output json file containing name, email and phone from CV 
    with open('output.json', 'w') as outfile:  
        json.dump(data, outfile)
