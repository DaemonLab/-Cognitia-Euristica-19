#IMPORTING LIBRARIES

import re
import nltk
from nltk.corpus import stopwords
import json
stop = stopwords.words('english')


#Read input text file here
inputfile = open('Abbas- MS Dyna.txt', 'r')   #ANY FILE NAME CAN BE MENTIONED HERE 
doc = inputfile.read()  


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
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

# MAIN FUNCTION
if __name__ == '__main__':
    names = extract_names(doc)
    numbers = extract_phone_numbers(doc)
    emails = extract_email_addresses(doc)
    edu = names[-1]
    exp = names[1:-2]
    Resume = {
    "name": [names[0]],
    "email":emails,
    "phone":numbers,
        "edu":[names[-1]],
        "exp":names[1:-2]
        }
    print(json.dumps(Resume))   # output 
