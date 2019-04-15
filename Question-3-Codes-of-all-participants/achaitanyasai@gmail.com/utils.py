import re
import spacy
import config

resume_file_name = None

def fread(fname, clean=True):
    def clean_line(line):

        def all_upper(word):
            return word == word.upper()
        
        def toLower(word, pref=1):
            res_pref = word.upper()[:pref]
            res_suf = word.lower()[pref:]
            return res_pref + res_suf
        line = re.sub(r'\[.*\]', '', line)
        line = re.sub(' +', ' ', line)
        res = []
        line = line.lstrip().rstrip().split()
        for word in line:
            if len(word) >= 4 and '.' not in word and all_upper(word):
                res.append(toLower(word, pref=1))
            else:
                res.append(word)
        return ' '.join(res)
    
    f = open(fname)
    x = f.read().strip()
    f.close()
    noise = '|%^?!~`'
    if clean:
        # x = x.replace('\n', ' ')
        x = x.replace('\t', ' ')
        x = x.replace('    ', ' ')
        x = re.sub(' +', ' ', x)
        for i in noise:
            x = x.replace(i, '')
        x = x.split('\n')
        res = []
        for line in x:
            res.append(clean_line(line))
    else:
        return x
    return '\n'.join(res)

def extract_phone_number(s):

    def count_numbers(s):
        res = 0
        for i in s:
            if i >= '0' and i <= '9':
                res += 1
        return res

    patterns = [
        r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',
        r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?',
        r'\+[-()\s\d]+?(?=\s*[+<])',
        r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
    ]

    ignore = '|)(%^&|:/?<>'
    _res = []
    for pat in patterns:
        _res += re.findall(pat, s.lower())
    res = []
    for i in _res:
        cur = i
        for j in ignore:
            try:
                cur = cur.replace(j, '')
            except Exception:
                pass
        if type(cur) == type(''):
            res.append(cur)
    s = s.split()
    actual_res = set()
    for i in res:
        for j in s:
            if i in j and count_numbers(j) >= 9:
                actual_res.add(j)
    return list(actual_res)

def extract_email(s):
    patterns = [
        r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    ]

    ignore = '|)(%^&|:/?<>'
    _res = []
    for pat in patterns:
        _res += re.findall(pat, s.lower())
    res = []
    for i in _res:
        cur = i
        for j in ignore:
            cur = cur.replace(j, '')
        res.append(cur)
    return res

def extract_names(r1):
    nlp = spacy.load('xx')
    for line in r1.split('\n'):
        doc = nlp(line)
        for ent in doc.ents:
            if(ent.label_ == 'PER'):
                return ent.text
    #TODO
    return ''

def get_education(content):
    def is_education_title(x):
        x = x.lower()
        ignore = '!@#$%^&*()_+=-<>,.?/:;{[]}~`\t'
        for i in ignore:
            x = x.replace(i, '')
        x = x.lstrip().rstrip()
        if 'education' in x:
            x = x.split()
            if len(x) <= 2:
                return True
        else:
            return False
    
    def is_alphanumeric(c):
        a = 'abcdefghijklmnopqrstuvwxyz0123456789'
        return c in a
        
    def get_prefix(x):
        x = x.lower()
        res = ''
        L = len(x)
        i = 0
        while i < L:
            if is_alphanumeric(x[i]):
                break
            else:
                res += x[i]
            i += 1
        return res
    
    def same_prefix(pref, x):
        x = x.lower()
        if x.startswith(pref):
            return True
        return False
    
    def check(x):
        x = x.lower()
        if len(x) == 0:
            return False
        c = x[0]
        if is_alphanumeric(c):
            return True
        return False
    
    content = content.split('\n')
    L = len(content)
    i = 0
    res = []
    while i < L:
        if is_education_title(content[i]):
            j = i + 1
            if j >= L:
                break
            pref = get_prefix(content[j])
            while j < L and same_prefix(pref, content[j]):
                if check(content[j].replace(pref, '')):
                    res.append(content[j].replace(pref, ''))
                j += 1
            break
        else:
            i += 1
    return res

def get_skills(content):

    def check(s):
        s = s.lower().lstrip().rstrip()
        s = s.split('-')
        for i in s:
            if i in config.skills:
                return True
        return False

    content = content.split()
    res = set()
    done = set()
    for i in content:
        if check(i):
            if i.lower() in done:
                pass
            else:
                res.add(i)
                done.add(i.lower())
    return list(res)