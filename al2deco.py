from collections import Counter
import re
library = {'module' : 'module', 'rising' : 'always' , 'falling' : 'always', 'endmodule' : 'endmodule', 'reg':'reg', 'wire':'wire', 'edge' : 'flipflop', 'always':'always','end':'end' }
#print (library['group'])
##symbols = {'=' :'equal'}



''' 
The syntax is very user friendly and easy to understand
For eg just write:
module add
c = a + b
and it will convert the code to

module (input a,input b, output c);
wire a,b,c;
assign c = a + b;
endmodule

'''



##############################################################
##########Module Defined######################################
##############################################################

def module(words):
    global finalPort
    global moduleCount
    global portRelation
    global moduleName
    
    portRelation = {} # input output names as dictionary
    print ("module enter")
    index = words.index('module')
    moduleName = words[index + 1]
    fileName = moduleName + ".v"
    w = open(fileName, 'w+')
    print ("this is my module name {}".format(moduleName))
    j = 2
    moduleCount = moduleCount+1
    length = len(words)
    print (length)
    finalPort = []
    key = "input"
    error = 0
    portType = []
                
    while length > 0:
        if words[j] == "":
            length = length -1
            print ("extra space")
            j = j+1
        elif words[j] == "(" :
            length = length-1
            while (length-1 > 1):
                print ("loop printed")
                length = length -1
                j = j+1
                if words[j] == ")":
                    print ("port list ends")
                    error = 1
                elif words[j] == ":":
                    key = "output"
                    print ("Now the {} list starts ".format(key))
                else:
                    if error == 1:
                        print ("syntax error near port list")
                    else :
                        print ("there re still few names left")
                        portList.append(words[j])
                        print ("does it get appended here {}".format(portList))
                        portRelation.update({words[j]:key})
                        variableList.update({words[j]:'wire'})
            finalPort.append(portList)
            print (finalPort)
            
                    
        elif words[j] == ")":
            print ("port list ends")
            print ("############################################################## {}".format(portRelation))
        
            return
        else:
            print("Syntax error, check line containing word {},.".format(words[j]))
            return
        
        

##############################################################
##########    ALWAYS BLOCK Defined   #########################
##############################################################

def always(words):
    global firstLine
    global lastLine
    lastLine = 0
    firstLine =1
    
    print("/*/*/*/*/*/*/*/*/*/*/*/*/ {}".format(portRelation))
    print("variables {}{}".format(portList,variableList))
    print("these are the words in always block {}".format(words))
    count = len(words)
    position = 0
    value1 = ''
    edge =0
    always =0
    rising = 0
    falling = 0
    sensitivity = 0
    print("this is final port list in {}".format(finalPort))
##    print("thie is always length {}".format(countWords))
    for countWords in range(0,count):
        
        print("atleast this pronts {}".format(words[countWords]))
        print (countWords)
        if words[countWords] == 'edge':
            edge = 1
            print('edge')
        elif words[countWords] == 'always':
            always =1
            print('always')
        elif words[countWords] == 'rising':
            rising =1
            print('rising')
            edgeCount = countWords
            value1 = 'posedge'
        elif words[countWords] == 'falling':
            falling = countWords
            print('falling')
            edgeCount = countWords
            value1 = 'negedge'
        elif words[countWords] in portList:
            sensitivity = 1
            print("hell#############################o")
            position = countWords
        elif words[countWords] in variableList:
            sensitivity = 1
            print("atleast this pronts 111")
            position = countWords+1
        else:
            print ("use 'always' for * sensitivity")
    if (edge):
        print('always @ ({0} {1}) \nbegin '.format(value1,words[position]))
    elif (always):
        print('always @(*) begin')
    else:
        print("check syntax")



##############################################################
#########    ENDMODULE Defined     ############################
##############################################################

def endmodule(words):
##    countEnd = completeFile.count(['endmodule'])
##    countStart = completeFile.count(['module'])
##    print ("Endmodule occurs {} times".format(countEnd))
##    print ("Module occurs {} times".format(countStart))
    print ("Module ends at this point")


##############################################################
#########    REGISTER Defined     ############################
##############################################################

def reg(words):
    print ("this is a register defined")
    print ("These words are defined as regsiters {}".format(words))
    for letters in words:
        if letters in portRelation:
            if portRelation[letters] == "input":
                print ("{} cannot be assigned as register, it is an input".format(letters))
            elif portRelation[letters] == "output":
                print("assigning register ")
            else:
                print("error")
        else:
            if letters in variableList:
                print ("a new register {} is defined".format(letters))
            else:
                continue
                
            
            


##############################################################
#########    WIRE Defined         ############################
##############################################################



def wire (words):
    print ("Wires found")





##############################################################
#########    END for always block Defined     ################
##############################################################
def end(words):
    global lastLine
    if (lastLine):
        print("check whether you hve started always block, or is it twice end")
    else:
        print ("I have read end line of a$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$lway block")

    lastLine = 1
    print (lastLine)









##############################################################
##########READ FUNCTION Defined###############################
##############################################################

def readin(fn):
    global lastLine
    global finalPort
    global variableList
    global portList
    global completeFile
    global moduleCount
    global words
    lastLine = 0
    completeFile = []
    r = open(fn,'r')
    variableList ={}
    portList =[]
    blank = 0
    moduleCount = 0

    for line in r:
        words = line.split()
        words = ",".join(words)
##        print ("this is , extended words {}".format(words))
        words = words.split(",")
        print ("this is final list with no commas --------------> {}".format(words))

        completeFile.append(words)
        lineSize = len(words)
##        print ("the length of this line is {}".format(len(words)))
        if lineSize >0:
            blank = 0
            print ("check what are words {}".format(words))
            if words[0] in library:
                print ("first word of the line is {}".format(words[0]))
                first = library[words[0]]
##                if first == 'always':
##                    globals()[first](words,variableList,portList)
##                else:
                globals()[first](words)
            elif words[0] == '#':
                print ("ignore that line, its a comment")
                pass
            else:
                analyse(words)
                        
    
        else:
            blank = blank +1
            if blank <20:
                print ("this is {} blank line".format(blank))
            else:
                return
    print ("readin {}{}".format(variableList, portList))        
    print (r)
    print (completeFile)


##############################################################
##########    MANAGE FUNCTION DefineD    #####################
##############################################################

def manage(words):
    

    print ("these are the words without dictionary")
    i = len(words)
    while i >0:
        i = i-1
        print (words[i])
        if words[i] in finalPort:
            print ("input or output")
        else:
            print ("operation")
        
##############################################################
##########     EQUATION FUNCTION Defined        ##############
##############################################################



def equation(a):
    global variables
    a = "".join(a)
    a= a.replace(" ","")
    
    ######
    s =[]
    variables = []
    comment = re.split(r'\#',a)
    print ('This part {}'.format(comment))
    x = re.split(r'[\*\+\|\-\,\=]',comment[0])
    y = re.findall(r'[\*\+\|\-\,\=]',comment[0])

    print (y)
    for k in y:
        if k == '=':
            pointer= (y.index(k))
            if pointer > 0:
                print("there is an error, you cannot operate two variables on LHS")
            else:
                pass
            print(pointer)
    for i in x:
        i = i.replace(' ', '')
        print (i)
        s.append(i)

    full = []
    for m in s:
        sizeStr = re.findall(r'\d+\:\d+',m)
        print (sizeStr)
        print(m)
        finalString = "variable {} is {}".format(m,sizeStr)
        full.append(finalString)

    print(full)
        
        
                       
    print (x)
    print (s)
    for words in s:
        new = (re.split(r'\[',words))
        variables.append(new[0])

    ########
    print(variables)
    LHS = variables[0]
    print (LHS)
    print (" gaAAAAAAAAAAAND MARAAAA {}".format(LHS))
    j=0
    print (firstLine)
    print ("this is lasrtline value {}".format(lastLine))
    for extra in variables:
                j += 1
                print ("New loop to look {}".format(extra))
                print(variableList)
                if extra in variableList:
                    print("this is an existing variable")
                else:
                    if extra in LHS:
                        if firstLine == 1 and lastLine ==1:
                            print("assign 121222222222222222222222222222222222222222222222222222222222222222222222{}".format(variables[0]))
                            variableList[variables[0]] = 'wire'
                              
                        else:
                            print ("wtf84848484848484848484848484848484 {}".format(variables[0]))
                            variableList[variables[0]] = 'reg'
                            
                    else:
                        print("it doesnt matter, {} these are on RHS".format(extra))
                        variableList.update({extra:'wire'})
                        
##                        variableList[variables
                        
    if variables[0] in variableList or portList:
        print ("i should know which variable is being read {}".format([variables[0]]))
        if variableList[variables[0]] == 'wire' and portRelation[variables[0]] == 'output':
            print("sounds good")
            print ("this is the value of last line! {}".format(lastLine))
            if firstLine == 1 and lastLine != 1:
                print ("this {} is in always block and should be a register".format(variables[0]))
                variableList[variables[0]] = 'reg'
            else:
                print("assign {}".format(variables[0]))
                variableList[variables[0]] = 'wire'
        elif variableList[variables[0]] == 'wire' and portRelation[variables[0]] == 'input':
            if firstLine == 1 and lastLine != 1:
                print ("input could not be a register, fatal error $$$$$$$$$$$")
            else:
                print("assign should be used")
        elif variableList[variables[0]] == 'wire' not in portRelation:
            if firstLine == 1 and lastLine != 1:
                print ("this is in always block and should be a register")
                variableList[variables[0]] = 'reg'
            else:
                print("assign {}".format(variables[0]))
        elif variableList[variables[0]] == 'reg'  not in portRelation:
            if firstLine == 1 and lastLine != 1:
                print ("this is in always block and should be a register")
                variableList[variables[0]] = 'reg'
            else:
                print("This should be under always blocks. We cannot assign value to register outside always blocks {}".format(variables[0]))
        
            
    else:
        for extra in variables:
            print(extra)
            j += 1
            if extra in variableList:
                print("this is an existing variable")
            else:
                if extra in LHS:
                    if firstLine == 1 and lastLine != 1:
                        print ("this needs to be defined as reg")
                        variableList.update({extra:'reg'})
                    else:
                        variableList.update({extra:'wire'})
                    print("need to add this variable")
                    
            
    return

##############################################################
########## ANALYSE FUNCTION Defined           ################
##############################################################

        
def analyse(words):
    
    print ("Entering analyse function {}".format(words))
    i = 0
    symbols = set('=/*+-&^|!')
    count = len(words)
    
    a = "".join(words)
    a= a.replace(" ","")

    if any((c in symbols for c in a)):
    
        print("these are the words {}".format(words))
        print("this is an equation")
        equation(words)
        print("this is {}".format(variables))
    
    
    while count>0:
        #print ("this is count {}".format(words[count]))
        count -= 1
        
        for letter in words:
            for char in letter:
                if char in operation:
                    print ("enter operation mode {}".format(char))
                    first = operation()[char](letter,words)
                    globals()
                else:
                    print("check next character {}".format(char))
                    
            print("lets first check what is a letter {}".format(letter))
            if letter in operation:
                print("operation mode")
            
            # lets find if the word is declared earlier or is it for the 1st time
            if letter in portRelation:
                print ("input output variables")
            elif letter == '#':
                print ("ignore that line, its a comment")
                break
                    
            elif "." in letter:
                print ("could be in or out")
                position = letter.find('.')
                variableSize = letter[position+1:]
                variableName = letter[0:position]
                if variableName in portRelation:
                    if variableName in variableList:
                        if ":" in letter:
                            print ("Check both the bits")
                            rangePosition = letter.find(':')
                            if letter[rangePosition-1] <= variableList[variableName]:
                                print("size is okay")
                            else:
                                print("size has some issues")
                            print ("the range is from {0} to {1}".format(letter[rangePosition-1], letter[rangePosition+1]))
                        else:
                            print("only that particular bit mentioned is to be used")
                    else:
                        variableList.update({variableName:variableSize})
                    print("the input/output size is defined which is {}--> {}".format(variableName, variableSize))
                else:
                    if variableName in variableList:
                        if ":" in letter:
                            print ("maybe partial bits or range is to be used are to be used")
                        else:
                            print("only specific bit needs to be addressed")

                        print ("maybe partial bits are to be used, compare the sizes")
                    else:
                        variableList.update({variableName:variableSize})
                        print ("new variable size is defined")
                        print ("the variable name is {}".format(variableName))
                        print ("the variable size is {}".format(variableSize))
                        print("it is at  {0} position . chatacter in {1}".format(letter,letter.find('.')))
                        print ("this is a letter defined {}".format(letter))
                print ("this is the first character of each word {}".format(letter[0]))
            else:
                 
                print("This is a letter or a number{}".format(letter))
                i = i+1
                
    
    

            

#This is the file with ASIC Language ( named it as ASIC Language )
readin ("al.txt")

print ("file read complete")
print (portRelation)
print(portList)
print(finalPort)
print (variableList)
