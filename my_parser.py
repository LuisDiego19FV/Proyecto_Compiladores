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
    
        self._endarg = 1
        self._startarg = 2
        self._endcode = 3
        self._startcode = 4
        self._charnumber = 5
        self._string = 6
        self._char = 7
        self._pt18 = 8
        self._pt17 = 9
        self._pt16 = 10
        self._pt15 = 11
        self._pt14 = 12
        self._pt13 = 13
        self._pt12 = 14
        self._pt11 = 15
        self._pt10 = 16
        self._pt9 = 17
        self._pt8 = 18
        self._pt7 = 19
        self._pt6 = 20
        self._pt5 = 21
        self._pt4 = 22
        self._pt3 = 23
        self._pt2 = 24
        self._pt1 = 25
        self._pt0 = 26
        self._ident = 27
        self.maxT = 28

        self.MyCOCOR()
         

    def MyCOCOR(self):
        CompilerName = ""
        EndName = ""
        self.Expect(self._pt0)
        CompilerName = self.Ident(CompilerName)
        print("Nombre Inicial del Compilador:",CompilerName)
        if(self.la.get_tok_type() == self._startcode):
            self.Codigo()
        self.Body()
        self.Expect(self._pt1)
        EndName = self.Ident(EndName)
        print("Nombre Final del Compilador:",EndName)
 

    def Body(self):
        self.Characters()
        if(self.la.get_tok_type() == self._pt7):
            self.Keywords()
        self.Tokens()
        self.Productions()
 

    def Characters(self):
        CharName = ""
        Counter = 0
        self.Expect(self._pt2)
        print("LEYENDO CHARACTERS")
        while(self.la.get_tok_type() == self._ident):
            CharName = self.Ident(CharName)
            Counter += 1
            print("Char Set "+ str(Counter) + ": " + str(CharName))
            self.Expect(self._pt3)
            self.CharSet()
            while(self.la.get_tok_type() == self._pt4 or self.la.get_tok_type() == self._pt5):
                if(self.la.get_tok_type() == self._pt4):
                    self.Expect(self._pt4)
                    self.CharSet()
                elif(self.la.get_tok_type() == self._pt5):
                    self.Expect(self._pt5)
                    self.CharSet()
            self.Expect(self._pt6)
 

    def Keywords(self):
        KeyName = ""
        StringValue = ""
        Counter = 0
        self.Expect(self._pt7)
        print("LEYENDO KEYWORDS")
        while(self.la.get_tok_type() == self._ident):
            KeyName = self.Ident(KeyName)
            Counter += 1
            print("KeyWord "+ str(Counter) + ": " + str(KeyName))
            self.Expect(self._pt3)
            StringValue = self.String(StringValue)
            self.Expect(self._pt6)
 

    def Tokens(self):
        TokenName = ""
        Counter = 0
        self.Expect(self._pt8)
        print("LEYENDO TOKENS")
        while(self.la.get_tok_type() == self._ident):
            TokenName = self.Ident(TokenName)
            Counter += 1
            print("Token "+ str(Counter) + ": " + str(TokenName))
            self.Expect(self._pt3)
            self.TokenExpr()
            if(self.la.get_tok_type() == self._pt10):
                self.ExceptKeyword()
            self.Expect(self._pt6)
 

    def Productions(self):
        Counter = 0
        self.Expect(self._pt9)
        ProdName = ""
        print("LEYENDO PRODUCTIONS")
        while(self.la.get_tok_type() == self._ident):
            ProdName = self.Ident(ProdName)
            Counter += 1
            print("Production "+ str(Counter) + ": " + str(ProdName))
            if(self.la.get_tok_type() == self._startarg):
                self.Atributos()
            self.Expect(self._pt3)
            if(self.la.get_tok_type() == self._startcode):
                self.Codigo()
            self.ProductionExpr()
            if(self.la.get_tok_type() == self._startcode):
                self.Codigo()
            self.Expect(self._pt6)
 

    def ExceptKeyword(self):
        self.Expect(self._pt10)
        self.Expect(self._pt7)
 

    def ProductionExpr(self):
        self.ProdTerm()
        while(self.la.get_tok_type() == self._pt11):
            self.Expect(self._pt11)
            self.ProdTerm()
 

    def ProdTerm(self):
        self.ProdFactor()
        while(self.la.get_tok_type() == self._string or self.la.get_tok_type() == self._char or self.la.get_tok_type() == self._ident or self.la.get_tok_type() == self._startarg or self.la.get_tok_type() == self._pt12 or self.la.get_tok_type() == self._pt14 or self.la.get_tok_type() == self._pt16 or self.la.get_tok_type() == self._startcode):
            self.ProdFactor()
 

    def ProdFactor(self):
        if(self.la.get_tok_type() == self._string or self.la.get_tok_type() == self._char or self.la.get_tok_type() == self._ident or self.la.get_tok_type() == self._startarg):
            self.SymbolProd()
        elif(self.la.get_tok_type() == self._pt12):
            self.Expect(self._pt12)
            self.ProductionExpr()
            self.Expect(self._pt13)
        elif(self.la.get_tok_type() == self._pt14):
            self.Expect(self._pt14)
            self.ProductionExpr()
            self.Expect(self._pt15)
        elif(self.la.get_tok_type() == self._pt16):
            self.Expect(self._pt16)
            self.ProductionExpr()
            self.Expect(self._pt17)
        if(self.la.get_tok_type() == self._startcode):
            self.Codigo()
 

    def SymbolProd(self):
        SV = ""
        IN = ""
        if(self.la.get_tok_type() == self._string):
            SV = self.String(SV)
            print("String en Production: ",SV)
        elif(self.la.get_tok_type() == self._char):
            self.Expect(self._char)
        if(self.la.get_tok_type() == self._ident):
            IN = self.Ident(IN)
            print("Identificador en Production: ",IN)
            if(self.la.get_tok_type() == self._startarg):
                self.Atributos()
 

    def Codigo(self):
        self.Expect(self._startcode)
        self.Any("endcode")
        self.Expect(self._endcode)
 

    def Atributos(self):
        self.Expect(self._startarg)
        self.Any("endarg")
        self.Expect(self._endarg)
 

    def TokenExpr(self):
        self.TokenTerm()
        while(self.la.get_tok_type() == self._pt11):
            self.Expect(self._pt11)
            self.TokenTerm()
 

    def TokenTerm(self):
        self.TokenFactor()
        while(self.la.get_tok_type() == self._string or self.la.get_tok_type() == self._char or self.la.get_tok_type() == self._ident or self.la.get_tok_type() == self._pt12 or self.la.get_tok_type() == self._pt14 or self.la.get_tok_type() == self._pt16):
            self.TokenFactor()
 

    def TokenFactor(self):
        if(self.la.get_tok_type() == self._string or self.la.get_tok_type() == self._char or self.la.get_tok_type() == self._ident):
            self.SimbolToken()
        elif(self.la.get_tok_type() == self._pt12):
            self.Expect(self._pt12)
            self.TokenExpr()
            self.Expect(self._pt13)
        elif(self.la.get_tok_type() == self._pt14):
            self.Expect(self._pt14)
            self.TokenExpr()
            self.Expect(self._pt15)
        elif(self.la.get_tok_type() == self._pt16):
            self.Expect(self._pt16)
            self.TokenExpr()
            self.Expect(self._pt17)
 

    def SimbolToken(self):
        IdentName = ""
        StringValue = ""
        if(self.la.get_tok_type() == self._string):
            StringValue = self.String(StringValue)
        elif(self.la.get_tok_type() == self._char):
            self.Expect(self._char)
        if(self.la.get_tok_type() == self._ident):
            IdentName = self.Ident(IdentName)
            print("Identificador en Token: ",IdentName)
 

    def CharSet(self):
        IdentName = ""
        StringValue = ""
        if(self.la.get_tok_type() == self._string):
            StringValue = self.String(StringValue)
        if(self.la.get_tok_type() == self._char or self.la.get_tok_type() == self._charnumber):
            self.Char()
        elif(self.la.get_tok_type() == self._pt18):
            self.Expect(self._pt18)
        if(self.la.get_tok_type() == self._ident):
            IdentName = self.Ident(IdentName)
            print("Identificador en CharSet: ",IdentName)
 

    def Char(self):
        if(self.la.get_tok_type() == self._char):
            self.Expect(self._char)
        elif(self.la.get_tok_type() == self._charnumber):
            self.Expect(self._charnumber)
 

    def String(self, S):
        self.Expect(self._string)
        S = self.t.get_val()
        return(S)
 

    def Ident(self, S):
        self.Expect(self._ident)
        S = self.t.get_val()
        return(S)

    
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
            s = "endarg"

        elif expected == 2:
            s = "startarg"

        elif expected == 3:
            s = "endcode"

        elif expected == 4:
            s = "startcode"

        elif expected == 5:
            s = "charnumber"

        elif expected == 6:
            s = "string"

        elif expected == 7:
            s = "char"

        elif expected == 8:
            s = "ANY"

        elif expected == 9:
            s = "}"

        elif expected == 10:
            s = "{"

        elif expected == 11:
            s = "]"

        elif expected == 12:
            s = "["

        elif expected == 13:
            s = ")"

        elif expected == 14:
            s = "("

        elif expected == 15:
            s = "|"

        elif expected == 16:
            s = "EXCEPT"

        elif expected == 17:
            s = "PRODUCTIONS"

        elif expected == 18:
            s = "TOKENS"

        elif expected == 19:
            s = "KEYWORDS"

        elif expected == 20:
            s = "."

        elif expected == 21:
            s = "-"

        elif expected == 22:
            s = "+"

        elif expected == 23:
            s = "="

        elif expected == 24:
            s = "CHARACTERS"

        elif expected == 25:
            s = "END"

        elif expected == 26:
            s = "COMPILER"

        elif expected == 27:
            s = "ident"

        print("Error: Expected " + s)
        print("Last token : " + str(self.t))
        print("Last Look-a: " + str(self.la))
        print("Scanner Pointer: " + str(self.sc.pointer))
        