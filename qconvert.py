import sys, os, re

#class to hold all formatting functions to change into 'ready-to-write' formats
class formatting:

    #for explanations
    def formatexp(self, q) :
        temp = []
        for i in q:
            spaceI, nextI = 10000000000, 1000000000
            t=''.join(map(str,i)).strip() #converting list element to string
            if(t!=''): #if not an empty line
                if(" " in t):
                    spaceI=t.index(" ")
                if("\n" in t):
                    nextI=t.index("\n")
                splitI=min(spaceI, nextI)
                temp.append(t[splitI+1:].strip()) #append the part after the description & space
        return temp
    #for the correct answer
    def formatans(self, z):
        correct=[]
        i=len(z)
        if('A) '==z[0][:3]): #special case 
            for i in range(i):
                correct.append(z[i][3].upper())
        else:
            for j in range(i):
                z[j]=z[j].rstrip() #removing whitespace
                x=len(z[j])
                y=[z[j][x-1],z[j][x-2]][z[j][x-1]==')'] #choosing between Answer: option and Answer: Option option
                correct.append(y.upper())
        return correct
    #for questions
    def formatquestions(self, q):
        temp = []
        for i in q:
            spaceI, nextI = 10000000000, 1000000000
            t=''.join(map(str,i)).strip() #converting list element to string
            if(t!=''): #if not an empty line
                if(" " in t):
                    spaceI=t.index(" ")
                if("\n" in t):
                    nextI=t.index("\n")
                splitI=min(spaceI, nextI)
                temp.append(t[splitI+1:].strip()) #append the part after the question number & space
        return temp
    #for options
    def formatoptions(self, x):
        temp=[]
        for i in x:
            sub=[]
            if(i==[]): #dummy
                continue
            for j in i:
                j=j.strip() #removing whitespace
                if(j!='' and j!='.' and j!=')'): #if not an empty line
                    sub.append(j.capitalize())
            temp.append(sub)
        return temp


#class to hold all components of the file - writables, regexes, and utility elements
class myfile:
    def __init__(self):
        self.optiondelim = ""
        self.quesdelim = ""
        self.optionreg = ""
        self.quesreg = ""
        self.questions = []
        self.options = []
        self.correct = []
        self.exp = []
        self.expindex = []

    def getdelim(self, a):
        odreg = re.compile(r'(?<=\n)(\()?[abcdABCD](\.|\))(.|\s)*')
        y=getiterable(a, odreg)
        self.optiondelim = y[0][:3].strip()

        qdreg = re.compile(r'\d+(\.|\)|\:)\s*([ -~]|")*')
        y=getiterable(a, qdreg)
        self.quesdelim = y[0][:3].strip()

        self.setreg()

    #setting regexes for option list and question markers
    def setreg(self):

        #for options
        if(self.optiondelim == 'A)'):
            self.optionreg = '[ABCDEF](\))'
        if(self.optiondelim == 'A.'):
            self.optionreg = '[ABCDEF](\.)'
        if(self.optiondelim == 'a)'):
            self.optionreg = '[abcdef](\))'
        if(self.optiondelim == 'a.'):
            self.optionreg = '[abcdef](\.)'
        if(self.optiondelim == '(a)'):
            self.optionreg = '\([abcdef]\)'

        #for questions
        if(self.quesdelim == '1:'):
            self.quesreg = '\d+:'
        if(self.quesdelim == '1)'):
            self.quesreg = '\d+\)'
        if(self.quesdelim == '1.'):
            self.quesreg = '\d+\.'

    #separate the list of block options 'y' into individual options
    def getoptions(self, y):
        temp = []
        for i in y:
            sub=re.split(fr'{self.optionreg} ', i)
            for j in sub:
                if((self.optiondelim=='(a)') and (j[:2]=='A)')): #special case for sample 3
                    sub.remove(j)
                j=j.strip() #removing whitespace
                if(j=='.' or j==')' or j==''): #garbage
                    sub.remove(j)
            temp.append(sub)
        return temp

    #use the options block 'y' as 'delimiter' to extract questions from the file-content 'a' and return a list of such questions 'temp'
    def getquestions(self, y, a):
        start=a
        t=[]
        sliceq= re.compile(fr'{self.quesreg}\s+(.|\s)+') #regex to extract the question
        for i in range (0, len(y)):
            temp=start.split(y[i],1) #text before option block
            start=temp[1] #text after the option block
            temp2=getiterable(temp[0],sliceq) #extracts the question from temp
            t.append(temp2)
        return t

    #getting question numbers + 1 for which explanations are given
    def getexpindex(self, e, a):
        for i in e:
            #find ending index of explanation
            index = a.index(i) + len(i)
            myreg = re.compile(r'\d+') #finding next question
            myoutput = myreg.search(a[index:])
            if(myoutput==None): #explanation for last question
                self.expindex.append(-1)
            else:
                num = myoutput.group().strip()
                self.expindex.append(int(num))
    
    #writing final elements into the file
    def write(self, f):
        outputf=open("output.txt", "w") #creating output file
        n=len(self.correct) 
        bullet=['A. ','B. ','C. ','D. ','E. ','F. '] #list markers for options
        ei=0 #explanation index

        for i in range(n): #for each question
            outputf.write(self.questions[i].lstrip()+"\n")
            k = len(self.options[i])

            for j in range(k): #for each option
                outputf.write(bullet[j]+self.options[i][j]+"\n")

            outputf.write("ANSWER: "+self.correct[i]+"\n")

            if(f==1 and self.exp!=[] and ei<len(self.exp)):
                if((i+1 == self.expindex[ei]-1) or (i==n-1 and self.expindex[ei]==-1)): 
                    outputf.write("EXPLANATION: "+self.exp[ei]+"\n")
                    ei+=1
            outputf.write("\n")

#utility - returns a callable iterable object containing all matches of pattern 'reg' in string 'a'
def getiterable(a, reg):
    obj=reg.finditer(a)
    return getstr(obj)

#utility - converts the callable iterable object 't' to a list of string matches 's'
def getstr(t):
    s=[]
    for x in t:
        s.append(x.group())
    return s

#main parsing logic
def parse(a, f):

    #replacing stylised quotes
    a = a.replace('“','"').replace('”','"').replace('‘','\'').replace('’','\'')

    obj = myfile() 
    form = formatting()

    obj.getdelim(a)  #setting delimiters

    #for options
    oreg= re.compile(fr'((?<![a-zA-Z.]){obj.optionreg}\s+[ -~]*(\s)*)+')
    y = getiterable(a,oreg)
    #for correct answers
    ansreg = re.compile(r'(Answer: (Option )?\w)|(A\) \w\n)|(A\) \w$)|(((\d+)\. [ABCD]\) )+)')
    z = getiterable(a, ansreg)
    #for explanations
    exreg = re.compile(fr'(Explanation:|Solution:)\s*.*(\n)?.*?(?=({obj.quesreg}|\n))')
    e=getiterable(a, exreg)

    #for questions
    temp2 = obj.getquestions(y,a)
    obj.questions = form.formatquestions(temp2)

    #split options and format
    temp = obj.getoptions(y)
    obj.options = form.formatoptions(temp)

    #format answer
    obj.correct = form.formatans(z)

    #set explanation question index and format
    obj.getexpindex(e, a)
    obj.exp = form.formatexp(e)

    #write to file
    obj.write(f)

#checking commandline arguments
def cla_errors(args):
    length=len(args)
    if(length<2 or length>3):
        print("Argument count is invalid!")
        return False

    if(length==3) :
        if(args[1]!='-f'):
            print("Invalid option!")
            return False
    
    filename=args[length-1]
    if(os.path.isfile(os.getcwd()+'/'+filename)==False):
        print("Invalid file name!")
        return False

    return True

#program entry point
if(cla_errors(sys.argv)): #if there are no command line argument errors
    filename = sys.argv[len(sys.argv)-1] 

    f=[0,1][sys.argv[1]=='-f'] #setting flag for explanations
    parse(open(filename).read().strip()+"\n", f)




