
# coding: utf-8

# In[1]:


import json
import os
import re


# In[2]:


a = [i for i in os.listdir() if ".txt" in i]
print(a)


# In[7]:


for file in a:
    with open(file,'r') as f:
        try:
            rr = f.read()
            match = re.search(r'[\w\.-]+@[\w\.-]+',rr )
            ll = [i for i in re.findall(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?', rr)]
            print(ll)
            data = {
            'email':[match.group(0)],
            'phone':ll
            }
            with open(file[:-4]+'.json', 'w') as outfile:
                json.dump(data, outfile,indent=2)

        except:
            print("email not found")

