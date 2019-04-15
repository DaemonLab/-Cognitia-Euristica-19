import os
import sys
import utils
import json

if not os.path.exists('./out'):
    os.makedirs('./out')
fname = sys.argv[1]
utils.resume_file_name = fname.split('/')[-1]
print('Reading: %s' % fname)
print('Output will be written to: %s' % ('./out/' + utils.resume_file_name + '.json'))

content = utils.fread(fname, clean=True)
raw_content = utils.fread(fname, clean=False)

phone_numbers = utils.extract_phone_number(content)

emails = utils.extract_email(content)

names = utils.extract_names(content)

education = utils.get_education(raw_content)

skills = utils.get_skills(raw_content)

res = {
    'name': names,
    'email': emails,
    'phone': phone_numbers,
    'education': education,
    'skills': skills
}

with open('./out/' + utils.resume_file_name + '.json', 'w') as f:
    json.dump(res, f)

print('Done')