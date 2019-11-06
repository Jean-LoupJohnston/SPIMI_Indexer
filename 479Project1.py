from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
from bs4 import BeautifulSoup
import json


positionalNum = 0
dictionary = {}
articleNumber = 1
diskNum = 1
wroteToDisk = False
allwords = []

stopwords150 = []
for x in range(150):
    stopwords150.append(stopwords.words('english')[x])
stopwords150 = set(stopwords150)

# go through all sgm files in reuters corpus
for root, dirs, files in os.walk("C:/Users/Jean-Loup/Downloads/reuters21578/","r"):

    for file in files: 
     if file.endswith('.sgm'):
       f = open(os.path.join(root,file))
       soup = BeautifulSoup(f, 'html.parser')

#open each file, remove unneeded tags, tokenize,remove #s,case fole, remove stop words, stem
       text = soup.get_text()
       text = ''.join(c for c in text if not c.isdigit())
       text = text.lower()
       text = word_tokenize(text)
       text = [w for w in text if not w in stopwords150] 
       positionalNum += len(text)
       i =0;
       
# go through data, add tokens to dictionary. Count article number. write to disk every 500
       while i <= len(text)-1:
           if text[i] == "\x03":
               articleNumber += 1
               wroteToDisk = False;
               
           if  (articleNumber % 500 == 0 and not wroteToDisk ):
               wroteToDisk = True
               diskWrite= open("C:/Users/Jean-Loup/Desktop/DISK/BLOCK"+str(diskNum)+".txt","w+")
               diskWrite.write(json.dumps(dictionary,sort_keys=True))
               diskWrite.close()
               diskNum += 1
               dictionary = {}
           if text[i] not in allwords:
               allwords.append(text[i])
               
           if text[i] not in dictionary.keys():
               dictionary[text[i]] = [articleNumber]
           elif articleNumber not in dictionary[text[i]]:
               dictionary[text[i]].append(articleNumber)
               
           i += 1
           

       f.close()
       
# write final dictionary to disk because it didnt get to % 500
diskWrite= open("C:/Users/Jean-Loup/Desktop/DISK/BLOCK"+str(diskNum)+".txt","w+")
diskWrite.write(json.dumps(dictionary,sort_keys=True))
diskWrite.close()

print(positionalNum)

allwords.sort()

for i in range(len(allwords)):
    if (i % 25000 ==0):
        print(allwords[i])
    





