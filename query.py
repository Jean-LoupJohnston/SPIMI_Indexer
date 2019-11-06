import json

    

file1 = open("C:/Users/Jean-Loup/Desktop/DISK/InvertedIndex1.txt","r")
index1 = json.load(file1)
file2 = open("C:/Users/Jean-Loup/Desktop/DISK/InvertedIndex2.txt","r")
index2 = json.load(file2)
file3 = open("C:/Users/Jean-Loup/Desktop/DISK/InvertedIndex3.txt","r")
index3 = json.load(file3)

# intersection of 2 lists
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
# implementation of AND query for n terms in 'q'
def ANDquery(q):
    words = q.split()

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

    for i in range(numLists):
        lists[0] = intersection(lists[0],lists[i])
        
    return lists[0]
# implementation of OR query for n terms in 'q'
def ORquery(q):
    words = q.split()
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

    stringReturn = ""
    for key in (sorted(ORdict, key=lambda x: ORdict[x],reverse = True)):
        stringReturn+=(key+": "+str(ORdict[key])+", ")
        

    return (stringReturn)


 # take user input and query   
while(True):                   
    inp = input("Select Query type(1 = AND, 2 = OR) ")
    if (inp == "1"):
        while(True):
            inp = input("Enter a query : ").lower()
            print(ANDquery(inp))
    elif (inp == "2"):
        while(True):
            inp = input("Enter a query : ")
            print(ORquery(inp))
    else:
        print("Invalid selection")







