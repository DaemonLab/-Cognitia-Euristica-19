# Euristica-2019
Simple Rule Based and pattern matching based idea to extract
name, email, phone number, skills, education qualifications from a resume.

##### Usage:
- ```python <path to resume in .txt format>```
- The output file will be created in ```./out/``` directory with the name ```<file name>.json```
##### Requirements:
- Python 3.5+
- spacy and spacy xx model
  - Install spacy using ```pip install spacy```
  - Install spacy xx model using ```python -m spacy download xx```
 
##### Idea:
- Preprocessing: I only did basic preprocessing such as removal of some punctuations, lowercasing, replacing multiple space with a single space. Removed unnecessary sections such as **[image]** etc. using pattern matching.
- For extracting email and phone number, I used regular expression. This extraction is pretty straightforward.
- For extraction of names, I used spacy's Named Entity Recognizer. I feed each line to the NER and if NER returns any tokens with label "PERSON", I am returning those tokens. I stop when ever I find the tokens with label "PERSON".
- Extraction of educational qualifications was done in the following way:
  - I am searching for line which contains the section called "education" and/or "qualifications" and/or "certifications". Let the line number is i. One observation here is that, educational qualifications would be listed using bullet points, etc. So from line i + 1 to end if the current line has same prefix as with line i + 1 and that prefix is not alpha numeral, I am considering that line as educational qualification.
- For skills extraction, I already have hard coded skill set. So if I am considering all the skills that are both present in my hard coded skill set and in resume. This hard coded skill set could be found in config.py

##### Sample outputs:
- Sample outputs for the given sample resumes could be found in ```./out/``` folder.
