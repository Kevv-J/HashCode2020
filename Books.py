from statistics import variance
import sys
import math

def bookTuple(books,bookscore):
    newbooks = []
    for x in books:
        newbooks.append((x,bookscore[x]))
    return sorted(newbooks,key= lambda x: x[1],reverse=True)

def getInfo(path):
    f = open(path)
    a = [int(x) for x in f.readline().split()]
    b = [int(x) for x in f.readline().split()]
    bookscore = {}
    for i,x in enumerate(b):
        bookscore[i] = x
    ln = a[1]
    libs = []
    count = 0 
    while ln:
        ln-=1
        l1 = [int(x) for x in f.readline().split()] # meta data
        l2 = [int(x) for x in f.readline().split()] # books
        lib = {}
        lib['index'] = count
        count += 1
        lib['signup'] = l1[1]
        lib['bookrate'] = l1[2]
        lib['books'] = bookTuple(l2,bookscore)
        # lib['books'] = sorted(lib['books'],key= lambda x: x[1],reverse=True)
        # print(lib['books'])
        libs.append(lib)
    f.close()
    return bookscore,libs,a[2]

def findBestLib(libs,days):
    bestLibScore = 0
    bestLib = -1
    bestUsedBooks = {}
    for i,lib in enumerate(libs):
        usedBooks = {}
        noOfBooks = (days-lib['signup']) * lib['bookrate']
        score = 0
        for x in lib['books'][:noOfBooks]:
            score += x[1]
            usedBooks[x[0]] = 1
        lst = lib['books'][:noOfBooks]
        lst = [x[1] for x in lst]
        # print(i,lib)
        if len(lst) < 2:
            var = 100
        else:
            var = variance(lst)
        var = 1
        # print(score/var)
        try:
            score = score*score/(lib["signup"]*noOfBooks*var) #Heuristic
        except ZeroDivisionError:
            score = score*50
        if score > bestLibScore:
            bestLib = i
            bestLibScore = score
            bestUsedBooks = usedBooks
    
    return bestLib,bestUsedBooks

def removeBookFromLib(libs,usedBooks):
    libIndex = []
    
    for lib in libs:
        books = lib['books'].copy()
        for x in books:
            if x[0] in usedBooks:
                lib['books'].remove(x)


bookscore,libs,days = getInfo(sys.argv[1])
# print(bookscore,libs,days)
selectedLibs = []

while days > 0 and len(libs) > 0:
    print(days)
    bestLib,usedBooks = (findBestLib(libs,days))
    # print(usedBooks)
    if len(usedBooks) > 0:
        selectedLibs.append((libs[bestLib]['index'],usedBooks))
    days -= libs[bestLib]['signup']
    del libs[bestLib]

    removeBookFromLib(libs,usedBooks)
    # print(libs)
# print(selectedLibs)

f = open("output_" + sys.argv[1],"w")
f.write(str(len(selectedLibs)))
f.write("\n")
for lib in selectedLibs:
    # if len(lib[1]) == 0:
    #     continue
    f.write(str(lib[0])+" "+str(len(lib[1])))
    f.write("\n")
    for x in lib[1]:
        f.write(str(x)+" ")
    f.write("\n")
f.close()
