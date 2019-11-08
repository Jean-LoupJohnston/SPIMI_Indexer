import json
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
    

file1 = open("./DISK/InvertedIndex1.txt","r")
index1 = json.load(file1)
file2 = open("./DISK/InvertedIndex2.txt","r")
index2 = json.load(file2)
file3 = open("./DISK/InvertedIndex3.txt","r")
index3 = json.load(file3)
file4 = open("./DISK/DocumentFrequency.txt","r")
docFreq = json.load(file4)
file5 = open("./DISK/DocumentLengths.txt","r")
L = json.load(file5)
file6 = open("./DISK/TermFrequencies.txt","r")
freq = json.load(file6)
stopwords = stopwords.words('english')

#bm25 values:
N = 25000
k = 5
b = 0.5
Lavg = 118

# intersection of 2 lists
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3
#takes list of retrieved docuemnts and a query, returns ranked list of docuemnts
def bm25Rank(docList,query):

    scores = {}
    
    for doc in docList:
        scores[doc] = 0
        for term in query:
           f = 0 # term frequency
           if str(doc)+term in freq:   # make sure document has term
                f= freq[str(doc)+term]
           temp = (N/docFreq[term])
           
           scores[doc] += math.log(temp,10)* (((k+1)*f)/(k*((1-b)+b*(L[doc]/Lavg))+f))
    return sorted(scores, key=scores.get, reverse=True)#return scores dictionary sorted by value
    
# implementation of AND query for n terms in 'q'
def ANDquery(q):
    words = q

    lists = []
    for word in words:
         if word >= "montagne" and word in index3:
            lists.append(index3[word])
         elif word >= "braatz" and word < "montagne" and word in index2:
            lists.append(index2[word])
         elif word in index1:
            lists.append(index1[word])
         else:
             return "Not found"

    numLists = len(lists)

    for i in range(numLists):#intersection on i lists
        lists[0] = intersection(lists[0],lists[i])
        
    return lists[0]
# implementation of OR query for n terms in 'q'
def ORquery(q):
    words = q
    ORdict = {}

    if not words:
        return "Invalid query"
    
    for word in words:
         if word >= "montagne" and word in index3:
            for doc in index3[word]:
                if doc not in ORdict:
                    ORdict[doc]= 1
                else:
                    ORdict[doc] = ORdict[doc]+1
         elif word >= "braatz" and word < "montagne" and word in index2:
            for doc in index2[word]:
                if doc not in ORdict:
                    ORdict[doc]= 1
                else:
                    ORdict[doc] = ORdict[doc]+1
         elif word in index1:
            for doc in index1[word]:
                if doc not in ORdict:
                    ORdict[doc]= 1
                else:
                    ORdict[doc] = ORdict[doc]+1

    return sorted(ORdict, key=lambda x: ORdict[x],reverse = True)


 # take user input and query   
while(True):                   
    inp = input("Select Query type(1 = AND, 2 = OR) ")
    if (inp == "1"):
# process the input the same way as the documents, then query
        while(True):
            inp = input("Enter a query : ").lower()
            inp = ''.join(c for c in inp if not c.isdigit())
            inp = word_tokenize(inp)
            inp = [w for w in inp if not w in stopwords] 
            print(bm25Rank(ANDquery(inp),inp))
    elif (inp == "2"):
        while(True):
            inp = input("Enter a query : ").lower()
            inp = ''.join(c for c in inp if not c.isdigit())
            inp = word_tokenize(inp)
            inp = [w for w in inp if not w in stopwords] 
            print(bm25Rank(ORquery(inp),inp))
    else:
        print("Invalid selection")







