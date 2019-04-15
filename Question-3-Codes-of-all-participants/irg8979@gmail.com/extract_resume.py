import re
import json
import sys

if len(sys.argv) < 2:
  print("Give filename in argument!")
  exit(0)
resume_file = sys.argv[1]

with open(resume_file) as f:
  resume = f.read().lower()
  
  # I use regex to find e-mails
  email = re.compile(r'[\w\.-]+@[\w\.-]+')
  emails = email.findall(resume)

  # I use regex again to find phone numbers
  phone = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
  phones = [re.sub(r'\D', '', num) for num in phone.findall(resume)]

  # for technologies I search for major keywords in the resume
  tech = []
  # list in not exhaustive
  keywords = ["python", "java", "c", "c++", ".net", "sql", "mysql",
  "asp.net", "html", "javascript", "ruby", "ruby on rails", "css",
  "matlab", "php", "ajax", "c#", "azure", "github", "bitbucket",
  "bitbucket", "asp", "vb script", "ms access", "ms office",
  "windows", "mac", "linux", "unix", "dos", "ibm", "jython", "blockchain",
  ]
  for key in keywords:
    if key in resume:
      tech.append(key)
  
  ext = {}
  # for name, its usually present in the first line
  # So, extracting just first line should work in most cases
  for line in open(resume_file):
    ext["name"] = " ".join(line.strip().lower().split()[:2])
    break
  ext['email'] = emails
  ext['phone'] = phones
  ext["exp"] = tech
  print(ext)
  with open('extracted_cv.json', 'w') as f:  
    json.dump(ext, f)
