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
termFrequencies = {}
docLengths = {}
docLength = 0

stopwords = stopwords.words('english')

# go through all sgm files in reuters corpus
# insert path to reuters below
for root, dirs, files in os.walk("./DISK/reuters21578/","r"):

    for file in files: 
     if file.endswith('.sgm'):
       f = open(os.path.join(root,file))
       soup = BeautifulSoup(f, 'html.parser')

#open each file, remove unneeded tags, tokenize,remove #s,case fole, remove stop words, stem
       text = soup.get_text()
       text = ''.join(c for c in text if not c.isdigit())
       text = text.lower()
       text = word_tokenize(text)
       text = [w for w in text if not w in stopwords] 
       positionalNum += len(text)
       i =0;

       
       
# go through data, add tokens to dictionary. Count article number. 
       while i <= len(text)-1:
           docLength += 1
           if text[i] == "\x03":
               docLengths[articleNumber] = docLength # keep track of document lengths 
               docLength  = 0
               articleNumber += 1
               wroteToDisk = False;
               
           if  (articleNumber % 500 == 0 and not wroteToDisk ): #write to disk every 500
               wroteToDisk = True
               diskWrite= open("./DISK/BLOCK"+str(diskNum)+".txt","w+")
               diskWrite.write(json.dumps(dictionary,sort_keys=True))
               diskWrite.close()
               diskNum += 1
               dictionary = {}

               
           if text[i] not in dictionary.keys():
               dictionary[text[i]] = [articleNumber]
            
           elif articleNumber not in dictionary[text[i]]:
               dictionary[text[i]].append(articleNumber)
 
           
           if str(articleNumber)+text[i] not in termFrequencies.keys():
               termFrequencies[str(articleNumber)+text[i]]=1  # keep dictionary of docId concatenated with the term, and frequency
           else:
               termFrequencies[str(articleNumber)+text[i]] += 1
               
               
           i += 1
           

       f.close()
       
# write final dictionary to disk because it didnt get to % 500
diskWrite= open("./DISK/BLOCK"+str(diskNum)+".txt","w+")
diskWrite2= open("./DISK/DocumentLengths.txt","w+") # write document lengths to disk
diskWrite3= open("./DISK/termFrequencies.txt","w+") # write termFrequencies to disk 
diskWrite.write(json.dumps(dictionary,sort_keys=True))
diskWrite2.write(json.dumps(docLengths))
diskWrite3.write(json.dumps(termFrequencies))
diskWrite.close()
diskWrite2.close()
diskWrite3.close()

#find average doc length
total = 0
for l in docLengths:
    total += docLengths[l]

print (total/len(docLengths))



    





