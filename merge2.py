import json


files = []
diskNum = 44


#open all BLOCK files
for x in range(0, diskNum):
    files.append(open("./DISK/BLOCK"+str(x+1)+".txt","r"))

index1 = {}
index2 = {}
index3 = {}
while files:
    for file in files:
        readChar = file.read(1)
        while readChar:

                
                
# read file one character at a time, if we read a quotation mark, get word inside
            if (readChar == '"'):
                token = ""
                readChar = file.read(1)
                while readChar != '"':
                    token += readChar
                    readChar = file.read(1)
                if token not in index1.keys() and token not in index2.keys() and token not in index3.keys() :
                    if token >= "montagne":
                        index3[token] =[]
                    elif token >= "braatz" and token < "montagne":
                        index2[token] =[]
                    else:
                        index1[token] =[]
                    
                        
                        
#if we read '[', read all numbers inside, append to postings list, break after every ] so we read one word at a time per file
                isWord = False
                while(True):
                    if (readChar == '['):
                        isWord =True
                        num = ""
                        readChar = file.read(1)
                        while readChar != ']':
                            num += readChar
                            readChar = file.read(1)
                        if token in index3:
                            for value in num.split(','):
                                index3[token].append(value.strip())
                        elif token in index2:
                            for value in num.split(','):
                                index2[token].append(value.strip())
                        else:
                            for value in num.split(','):
                                index1[token].append(value.strip())
                        break
                    readChar = file.read(1)
                if(isWord):
                    break
# if end of document is reached, close and remove file from files list
            if (readChar == '}'):
                file.close()
                files.remove(file)
                break
 
            else :
                readChar = file.read(1)

# get document frequency of terms
freq = {}
for term in index1:
    freq[term] = len(index1[term])
for term in index2:
    freq[term] = len(index2[term])
for term in index3:
    freq[term] = len(index3[term])



       
diskWrite1= open("./DISK/InvertedIndex1.txt","w+")
diskWrite2= open("./DISK/InvertedIndex2.txt","w+")
diskWrite3= open("./DISK/InvertedIndex3.txt","w+")
diskWrite4= open("./DISK/DocumentFrequency.txt","w+")
diskWrite1.write(json.dumps(index1,sort_keys=True))
diskWrite2.write(json.dumps(index2,sort_keys=True))
diskWrite3.write(json.dumps(index3,sort_keys=True))
diskWrite4.write(json.dumps(freq,sort_keys=True))
diskWrite1.close()
diskWrite2.close()
diskWrite3.close()
diskWrite4.close()


        
    
