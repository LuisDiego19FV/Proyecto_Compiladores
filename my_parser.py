import Lexer.lexer as lex
import Lexer.automataPrinter as autPrint
from my_scanner import Scanner as scanner 

class Parser():

    def __init__(self, filename):
        self.filename = filename
        self.sc = scanner(filename)

        self.t = self.sc.scan()
        self.la = self.t

        self._EOF = 0
    
        self._white = 1
        self._number = 2
        self._pt7 = 3
        self._pt6 = 4
        self._pt5 = 5
        self._pt4 = 6
        self._pt3 = 7
        self._pt2 = 8
        self._pt1 = 9
        self._pt0 = 10
        self._switch = 11
        self._do = 12
        self._while = 13
        self._ident = 14
        self.maxT = 15

        self.Aritmetica()
         

    def Aritmetica(self):
        while(self.la.get_tok_type() == self._pt3 or self.la.get_tok_type() == self._number or self.la.get_tok_type() == self._pt6):
            self.Stat()
            self.Expect(self._pt0)
            while(self.la.get_tok_type() == self._white):
                self.Expect(self._white)
        self.Expect(self._pt1)
 

    def Stat(self):
        value = 0
        value = self.Expression(value)
        print(str(value))
 

    def Expression(self, result):
        result1 = 0
        result2 = 0
        result1 = self.Term(result1)
        while(self.la.get_tok_type() == self._pt2 or self.la.get_tok_type() == self._pt3):
            if(self.la.get_tok_type() == self._pt2):
                self.Expect(self._pt2)
                result2 = self.Term(result2)
                result1+=result2
            elif(self.la.get_tok_type() == self._pt3):
                self.Expect(self._pt3)
                result2 = self.Term(result2)
                result1-=result2
        result = result1
        return(result)
 

    def Term(self, result):
        result1 = 0
        result2 = 0
        result1 = self.Factor(result1)
        while(self.la.get_tok_type() == self._pt4 or self.la.get_tok_type() == self._pt5):
            if(self.la.get_tok_type() == self._pt4):
                self.Expect(self._pt4)
                result2 = self.Factor(result2)
                result1*=result2
            elif(self.la.get_tok_type() == self._pt5):
                self.Expect(self._pt5)
                result2 = self.Factor(result2)
                result1/=result2
        result=result1
        return(result)
 

    def Factor(self, result):
        signo = 1
        if(self.la.get_tok_type() == self._pt3):
            self.Expect(self._pt3)
            signo = -1
        if(self.la.get_tok_type() == self._number):
            result = self.Number(result)
        elif(self.la.get_tok_type() == self._pt6):
            self.Expect(self._pt6)
            result = self.Expression(result)
            self.Expect(self._pt7)
        result *= signo
        return(result)
 

    def Number(self, result):
        self.Expect(self._number)
        result = int(self.t.get_val())
        return(result)

    
    def Get(self):
        self.t = self.la
        self.la = self.sc.scan()

        while self.la.get_tok_type() == -1:
            self.la = self.sc.scan()

        if self.t.get_tok_type() == -3:
            print("END REACHED")
            exit()

    def Any(self, stop):
        while self.la.get_name() != stop:
            self.Get()

    def Expect(self, expected):
        if self.la.get_tok_type() == expected:
            self.Get()
        else:
            self.SymError(expected)   
            self.Get()
            self.Expect(expected) 

    def SymError(self, expected):
        s = "Other"

        if expected == 0:
            s = "EOF"
        
        elif expected == 1:
            s = "white"

        elif expected == 2:
            s = "number"

        elif expected == 3:
            s = ")"

        elif expected == 4:
            s = "("

        elif expected == 5:
            s = "/"

        elif expected == 6:
            s = "*"

        elif expected == 7:
            s = "-"

        elif expected == 8:
            s = "+"

        elif expected == 9:
            s = "."

        elif expected == 10:
            s = ";"

        elif expected == 11:
            s = "switch"

        elif expected == 12:
            s = "do"

        elif expected == 13:
            s = "while"

        elif expected == 14:
            s = "ident"

        print("Error: Expected " + s)
        print("Last token : " + str(self.t))
        print("Last Look-a: " + str(self.la))
        print("Scanner Pointer: " + str(self.sc.pointer))
        