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
        self._endpoint = 2
        self._equal = 3
        self._chardef = 4
        self._number = 5
        self._expect_key = 6
        self._end_section = 7
        self._pro_section = 8
        self._tok_section = 9
        self._key_section = 10
        self._char_seciton = 11
        self._comp_section = 12
        self._name = 13
        self._pt3 = 14
        self._pt2 = 15
        self._pt1 = 16
        self._pt0 = 17
        self.maxT = 18

        self.Parser()
         

    def Parser(self):
        self.comp_name = ""
        self.characters_vals = []
        self.characters_names = []
        self.tokens_vals = []
        self.tokens_names = []
        while(self.la.get_tok_type() == self._comp_section):
            self.Compiler_read()
        
        # Write Scanner
        file = open("Templates/scanner_template_1.txt", "r")
        part1 = file.readlines()
        file.close()
        
        file = open("Templates/scanner_template_2.txt", "r")
        part2 = file.readlines()
        file.close()
        
        file = open("my_scanner2.py", "w")
        for i in part1:
            file.write(i)
        
        for i in range(len(self.tokens_names)):
            file.write("        nodes" + str(i) + " = lex.regexToDFA(\"" + str(self.tokens_vals[i]) + "\", \"" + str(self.tokens_names[i]) + "\", " + str(i) + ")\n")
            file.write("        self.separateDFAs.append(nodes" + str(i) + ")\n\n")
        
        for i in part2:
            file.write(i)
        
        file.close()
        
        while(self.la.get_tok_type() == self._white):
            self.Expect(self._white)
        self.Expect(self._pro_section)
 

    def Compiler_read(self):
        self.Expect(self._comp_section)
        while(self.la.get_tok_type() == self._white):
            self.Expect(self._white)
        self.Expect(self._name)
        self.comp_name = str(self.t.get_val())
        self.Sections()
 

    def Sections(self):
        while(self.la.get_tok_type() == self._white):
            self.Expect(self._white)
        while(self.la.get_tok_type() == self._char_seciton or self.la.get_tok_type() == self._key_section or self.la.get_tok_type() == self._tok_section):
            declare_names = []
            declare_values = []
            if(self.la.get_tok_type() == self._char_seciton):
                self.Expect(self._char_seciton)
                #GET CHARS
                declare_names,declare_values = self.Declare_chars(declare_names, declare_values)
                #SET CHARS
                self.characters_names = declare_names
                self.characters_vals = declare_values
            elif(self.la.get_tok_type() == self._key_section):
                self.Expect(self._key_section)
                #GET KEYS
                declare_names,declare_values = self.Declare_keys(declare_names, declare_values)
                #SET KEYS
                self.tokens_names = declare_names
                self.tokens_vals = declare_values
            elif(self.la.get_tok_type() == self._tok_section):
                self.Expect(self._tok_section)
                #GET TOKS
                declare_names,declare_values = self.Declare_tokens(declare_names, declare_values)
                #SET TOKS
                self.tokens_names += declare_names
                self.tokens_vals += declare_values
 

    def Declare_chars(self, declare_names,  declare_values):
        while(self.la.get_tok_type() == self._white):
            self.Expect(self._white)
        while(self.la.get_tok_type() == self._name):
            self.Expect(self._name)
            declare_names.append(self.t.get_val())
            while(self.la.get_tok_type() == self._white):
                self.Expect(self._white)
            self.Expect(self._equal)
            self.Expect(self._pt0)
            if(self.la.get_tok_type() == self._name):
                self.Expect(self._name)
                tmp_value = str(self.t.get_val())
                declare_values.append("|".join(tmp_value[i:i+1] for i in range(0, len(tmp_value), 1)))
            elif(self.la.get_tok_type() == self._number):
                self.Expect(self._number)
                tmp_value = str(self.t.get_val())
                declare_values.append("|".join(tmp_value[i:i+1] for i in range(0, len(tmp_value), 1)))
            self.Expect(self._pt0)
            while(self.la.get_tok_type() == self._white):
                self.Expect(self._white)
            self.Expect(self._endpoint)
        return(declare_names, declare_values)
 

    def Declare_keys(self, declare_names,  declare_values):
        while(self.la.get_tok_type() == self._white):
            self.Expect(self._white)
        while(self.la.get_tok_type() == self._name):
            self.Expect(self._name)
            declare_names.append(self.t.get_val())
            while(self.la.get_tok_type() == self._white):
                self.Expect(self._white)
            self.Expect(self._equal)
            self.Expect(self._pt0)
            if(self.la.get_tok_type() == self._name):
                self.Expect(self._name)
                tmp_value = str(self.t.get_val())
                declare_values.append("|".join(tmp_value[i:i+1] for i in range(0, len(tmp_value), 1)))
            elif(self.la.get_tok_type() == self._number):
                self.Expect(self._number)
                tmp_value = str(self.t.get_val())
                declare_values.append("|".join(tmp_value[i:i+1] for i in range(0, len(tmp_value), 1)))
            self.Expect(self._pt0)
            while(self.la.get_tok_type() == self._white):
                self.Expect(self._white)
            self.Expect(self._endpoint)
        return(declare_names, declare_values)
 

    def Declare_tokens(self, declare_names,  declare_values):
        while(self.la.get_tok_type() == self._white):
            self.Expect(self._white)
        while(self.la.get_tok_type() == self._name):
            self.Expect(self._name)
            declare_names.append(self.t.get_val())
            while(self.la.get_tok_type() == self._white):
                self.Expect(self._white)
            self.Expect(self._equal)
            tmp_tok_value = ""
            while(self.la.get_tok_type() == self._name or self.la.get_tok_type() == self._pt1 or self.la.get_tok_type() == self._pt2 or self.la.get_tok_type() == self._pt3):
                if(self.la.get_tok_type() == self._name):
                    self.Expect(self._name)
                    value = str(self.t.get_val())
                    value = self.Get_value_from_chars(value)
                    tmp_tok_value += "(" + value + ")"
                elif(self.la.get_tok_type() == self._pt1):
                    self.Expect(self._pt1)
                    tmp_tok_value += "|"
                elif(self.la.get_tok_type() == self._pt2):
                    self.Expect(self._pt2)
                    tmp_tok_value += "("
                elif(self.la.get_tok_type() == self._pt3):
                    self.Expect(self._pt3)
                    tmp_tok_value += ")*"
            while(self.la.get_tok_type() == self._white):
                self.Expect(self._white)
            self.Expect(self._endpoint)
            declare_values.append(tmp_tok_value)
        return(declare_names, declare_values)
 

    def Get_value_from_chars(self, value):
        if value in self.characters_names:
            value = str(self.characters_vals[self.characters_names.index(value)])
        return(value)

    
    def Get(self):
        self.t = self.la
        self.la = self.sc.scan()
        if self.la.get_tok_type() < 0 or self.la.get_tok_type() > self.maxT:
            self.la = self.t

    def Expect(self, expected):
        if self.la.get_tok_type() == expected:
            self.Get()
        else:
            self.SymError(expected)    

    def SymError(self, expected):
        s = "Other"

        if expected == 0:
            s = "EOF"
        
        elif expected == 1:
            s = "white"

        elif expected == 2:
            s = "endpoint"

        elif expected == 3:
            s = "equal"

        elif expected == 4:
            s = "chardef"

        elif expected == 5:
            s = "number"

        elif expected == 6:
            s = "expect_key"

        elif expected == 7:
            s = "end_section"

        elif expected == 8:
            s = "pro_section"

        elif expected == 9:
            s = "tok_section"

        elif expected == 10:
            s = "key_section"

        elif expected == 11:
            s = "char_seciton"

        elif expected == 12:
            s = "comp_section"

        elif expected == 13:
            s = "name"

        elif expected == 14:
            s = "}"

        elif expected == 15:
            s = "{"

        elif expected == 16:
            s = "|"

        elif expected == 17:
            s = "\""

        print("Error: Expected " + s)
        print("Last token : " + str(self.t))
        print("Last Look-a: " + str(self.la))
        print("Scanner Pointer: " + str(self.sc.pointer))
        exit()
        