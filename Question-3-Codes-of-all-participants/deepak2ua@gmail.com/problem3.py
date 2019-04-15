# importing libraries
import re
import io
import json

# path for resume file (should be in .txt format)
resume_path = "../resumes/Arup_Kumar_H1 B_NC.txt"


File = io.open(resume_path, 'r', encoding='utf-8')
string = File.read()
string = re.sub('[/|%|+]', '', string)


# function to extact contact number
def contact_no_extraction(string):
    r = re.compile(r'\d{3}[-]\d{3}[-]\d{4}')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

# function to extract email id


def email_id_extraction(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)


if __name__ == '__main__':
    # reads the resume file (should be in .txt)
    with open(resume_path) as f:
        file = f.read()

    # extracting contact numbers and email ids
    c_nos = contact_no_extraction(file)
    email_ids = email_id_extraction(file)

    data = {}
    data['email'] = email_ids
    data['phone'] = c_nos
    # Creation of json file which contains extracted email ids and contact numbers from the given resume file
    with open('output.json', 'w') as outfile:
        json.dump(data, outfile)
