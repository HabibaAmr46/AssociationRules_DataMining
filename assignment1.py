import pandas as pd

data = pd.read_csv("retail_dataset.csv", header=None)
data = data.iloc[1: , 1:] #remove first row and first column in excel
init = pd.unique(data.values.ravel('K')) #Flattened array containing Unique items
init = init[~pd.isnull(init)]
print(sorted(init))
min_support = int(input("Enter Min Support"))
min_conf = float(input("Enter Min Confidence"))
Sup_Count={}         #Dictionary (key:itemset value:supportCount for all frequent terms generated in L1,L2,L3,.. To Use in Confidence)
from collections import Counter
c = Counter() #key:itemset value:counts
#Get Unique Terms Only in Items To generate C1
for i in init:
    for d in data.values:
        if(i in d):
            c[i]+=1
print("C1:")
for i in c:
    print(str([i])+": "+str(c[i]))
print()
l = Counter()
for i in c:
    if(c[i] >= min_support):
        l[frozenset([i])]=c[i]
print("L1:")
for i in l:
    print(str(list(i))+": "+str(l[i])) #convert frozen set into list for output
    Sup_Count[frozenset(i)] = l[i]
print()
pl = l
pos = 1 #1-itemset
for count in range (2,1000):
    nc = set() #avoid duplicates
    temp = list(l)
    for i in range(0,len(temp)): #make all different combinations #By taking each element and next elements
        for j in range(i+1,len(temp)):
            t = temp[i].union(temp[j])
            if(len(t) == count): #count iteration number(itemset)
                nc.add(temp[i].union(temp[j]))
    nc = list(nc)
    c = Counter()
    for i in nc:
        c[i] = 0
        for q in data.values:
            if(i.issubset(q)):
                c[i]+=1
    if(len(c)==0): #Check length of C list
        break;
    print("C"+str(count)+":")
    for i in c:
        print(str(list(i))+": "+str(c[i]))
    print()
    l = Counter()
    for i in c:
        if(c[i] >= min_support):
            l[i]=c[i]
    if (len(l) == 0): #Check length of L after validating min support
        break
    print("L"+str(count)+":")
    for i in l:
        print(str(list(i))+": "+str(l[i]))
        Sup_Count[frozenset(i)] = l[i]
    print()
    pl = l
    pos = count

#pl contains last frequentset achieved
print("Result: ")
print("L"+str(pos)+":")
for i in pl:
    print(str(list(i))+": "+str(pl[i]))
print()


from itertools import combinations
Frequent_items=list(pl) #Contain a list of last frequent itemsets

print()
print()
for i in range(0,len(Frequent_items)): #Iterate over each set in last frequent
    for j in range(1,len(Frequent_items[i])):
        #Generate Combinations of size j
        sub = list(combinations(Frequent_items[i],j))
        for k in range(0,len(sub)): #antecedent and subsequent
            ant = frozenset(sub[k])
            con = Frequent_items[i] - ant
            if(((Sup_Count[Frequent_items[i]] / Sup_Count[ant])*100) >= min_conf):
                print(list(ant),"->",list(con))
                print(str(round(Sup_Count[Frequent_items[i]]/Sup_Count[ant]*100, 2)),"%") #round to the nearst two places
