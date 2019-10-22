import time

filename = input("Enter name of file: ")
for k in range(1):
    #encoder
    start = time.time()
    file = open(filename,"rb")
    contents = file.read()
    triples = []
    W = 1000
    L = 100
    if len(contents)>0:
        triples.append([0,0,contents[0]])#first char
        counter = 1
        while counter<len(contents):
            triples.append([])
            check = 0 #triple not found
            if counter+L<len(contents):# if counter+L within bounds
                num = L
            else:
                num = len(contents)-counter #lookahead section is rest of contents
            if counter<W:#not enough space for window
                const = counter #look at all prev sequences length l
            else:
                const = W #enough space for window
            for i in range(num):
                l = num-i #try largest sequence first
                lookup = contents[counter:counter+l]
                for j in range(const-l+1): #look at all previous sequences length l
                    if contents[counter-l-j:counter-j] == lookup:
                        triples[-1].append(l+j) #add dist
                        triples[-1].append(l) #add length
                        if counter+l>=len(contents):
                            triples[-1].append("-")
                        else:
                            triples[-1].append(contents[counter+l])
                        counter+=l+1
                        check = 1 #triple found
                        break
                if check == 1: #triple found, stop looking
                    break
            if check == 0: #if first occurrence of char
                triples[-1].append(0)
                triples[-1].append(0)
                triples[-1].append(contents[counter])
                counter+=1       
        end = time.time()
        diff = end-start
        print("It took",str(round(diff,2)),"seconds to encode")
        
    file.close()
    #writing to compressed file
    file = open("compressed.txt","w+") 

    for i in range(len(triples)): #write triples to compressed file
        file.write("(")
        file.write(str(triples[i][0]))
        file.write(",")
        file.write(str(triples[i][1]))
        file.write(",")
        file.write(str(triples[i][2]))
        file.write(")")
        
    file.close()
    #decoder
    file = open("compressed.txt","r")

    start = time.time()
    contents = file.read()
    contents = contents.replace('(',"") #turn triples into one list
    contents = contents.replace(')',",")
    contents = contents.split(",")
    del contents[-1]
    f = open("output.txt","wb+") #rename output.png/.gif etc for type of file being decoded
    output = bytearray() #turn output into bytearray
    for i in range(int(len(contents)/3)): #for each triple
        if contents[3*i] == "0": #if first occurrence of char
            output.append(int(contents[(3*i)+2]))
        else:
            if (-int(contents[3*i])+int(contents[(3*i)+1])) == 0: #if repeated sequence is previous few character
                output+=output[-int(contents[3*i]):] #add repeated sequence
            else:
                output+=output[-int(contents[3*i]):-int(contents[3*i])+int(contents[(3*i)+1])]
            if contents[(3*i)+2] != "-": #if not end of file
                output.append(int(contents[(3*i)+2])) #add next letter
    end = time.time()
    diff = end-start
    print("It took",str(round(diff,2)),"seconds to decode")
    f.write(output) #write output to file
    f.close()
    file.close()
