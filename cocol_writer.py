# cocol_writer.py
# By: Luis Diego Fernandez

class CocolWriter():

    def __init__(self, compiler_name = "Compiler", file_name_scanner = "my_scanner.py", file_name_parser = "my_parser.py"):
        # file specifications
        self.compiler_name = compiler_name
        self.file_name_scanner = file_name_scanner
        self.file_name_parser = file_name_parser
        self.keywords= []
        self.tokens = []
        self.ignore_chars = ""
        self.productions = []
        self.ptokens = []

    def setKeywords(self, keywords):
        self.keywords = keywords

    def setTokens(self, tokens):
        self.tokens = tokens

    def setIgnoreChars(self, chars):
        self.ignore_chars = chars

    def setProductions(self, productions):
        self.productions = productions

    def setProductionsTokens(self, ptokens):
        self.ptokens = ptokens

    def startWritingScanner(self):
        file = open("Templates/scanner_template_1.txt", "r")
        part1 = file.readlines()
        file.close()

        file = open("Templates/scanner_template_2.txt", "r")
        part2 = file.readlines()
        file.close()

        file = open(self.file_name_scanner, "w")

        for i in part1:
            if "self.ignore_chars =" in i and self.ignore_chars != "":
                file.write("        self.ignore_chars = " + str(self.ignore_chars) )
            else:
                file.write(i)

        # Write tokens priority 0
        counter = 0
        priority = 0
        tokens = self.tokens[::-1]
        for i in tokens:

            if i[2] == 2:
                continue

            priority += 1

            # White spaces restriccions
            regex = i[1].replace("\n", "\\n")
            regex = regex.replace("\r", "\\r")
            regex = regex.replace("\t", "\\t")

            # Write token
            file.write('''
        nodes''' + str(counter) + \
            ''' = lex.regexToDFA("''' + regex + '''","''' + str(i[0]) + '''",''' + str(priority)  + ''')
        self.separateDFAs.append(nodes''' + str(counter) + ''')
        ''')
            counter += 1

        # Write keywords
        keys = self.keywords[::-1]
        for i in keys:

            priority += 1

            # White spaces restriccions
            regex = i[1].replace("\n", "\\n")
            regex = regex.replace("\r", "\\r")
            regex = regex.replace("\t", "\\t")

            # Write token
            file.write('''
        nodes''' + str(counter) + \
            ''' = lex.regexToDFA("''' + regex + '''","''' + str(i[0]) + '''",''' + str(priority) + ''')
        self.separateDFAs.append(nodes''' + str(counter) + ''')
''')
            counter += 1

        # Write tokens priority 2
        for i in tokens:

            if i[2] == 0:
                continue

            priority += 1

            # White spaces restriccions
            regex = i[1].replace("\n", "\\n")
            regex = regex.replace("\r", "\\r")
            regex = regex.replace("\t", "\\t")

            # Write token
            file.write('''
        nodes''' + str(counter) + \
            ''' = lex.regexToDFA("''' + regex + '''","''' + str(i[0]) + '''",''' + str(priority)  + ''')
        self.separateDFAs.append(nodes''' + str(counter) + ''')
''')
            counter += 1
        
        ptokens = self.ptokens[::-1]

        # Write tokens declare in productions
        for i in ptokens:

            priority += 1

            # White spaces restriccions
            regex = i[1].replace("\n", "\\n")
            regex = regex.replace("\r", "\\r")
            regex = regex.replace("\t", "\\t")

            # Write token
            file.write('''
        nodes''' + str(counter) + \
            ''' = lex.regexToDFA("''' + regex + '''","''' + str(i[0]) + '''",''' + str(priority)  + ''')
        self.separateDFAs.append(nodes''' + str(counter) + ''')
''')
            counter += 1

        for i in part2:
            file.write(i)

    def startWritingParser(self):
        file = open(self.file_name_parser, "w")
        scanner = self.file_name_scanner
        scanner = scanner[:scanner.index(".")]

        file.write(
'''import Lexer.lexer as lex
import Lexer.automataPrinter as autPrint
from ''' + scanner + ''' import Scanner as scanner 

class Parser():

    def __init__(self, filename):
        self.filename = filename
        self.sc = scanner(filename)

        self.t = self.sc.scan()
        self.la = self.t

        self._EOF = 0
    ''')
        tokens = self.tokens[::-1]
        keywords = self.keywords[::-1]
        ptokens = self.ptokens[::-1]
        priority = 0

        expected = []

        # Write tokens priority 0
        for i in tokens:
            if i[2] == 2:
                continue

            priority += 1

            file.write('''
        self._''' + str(i[0]) + ''' = ''' + str(priority))

            expected.append((priority,str(i[0])))

        # Write keywords
        for i in keywords:
            priority += 1

            file.write('''
        self._''' + str(i[0]) + ''' = ''' + str(priority))

            expected.append((priority,str(i[0])))

        # Write tokens priority 2
        for i in tokens:
            if i[2] == 0:
                continue

            priority += 1

            file.write('''
        self._''' + str(i[0]) + ''' = ''' + str(priority))

            expected.append((priority,str(i[0])))

        # Write ptoken
        for i in ptokens:
            priority += 1

            file.write('''
        self._''' + str(i[0]) + ''' = ''' + str(priority))

            expected.append((priority,str(i[1])))

        file.write('''
        self.maxT = ''' + str(priority + 1) + '''

        self.''' + str(self.compiler_name) + "()" + '''
        ''')

        # Write productions
        for i in self.productions:
            file.write(''' 

    def ''' + str(i[0]) + '''(self''')
            # Write parameters
            to_return = ""
            for j in i[1]:
                param = str(j)
                if 'ref ' in param:
                    param = param.replace('ref ','')
                    to_return += "," + param

                file.write(", " + param)
        
            file.write("):\n")

            # Write the production
            tabs = 2
            for j in i[2]:

                if j == "{":
                    file.write("    " * tabs + "while(True):\n")
                    tabs += 1
                elif j == "[":
                    file.write("    " * tabs + "if(True):\n")
                    tabs += 1
                elif j == "if":
                    file.write("    " * tabs + "if(True):\n")
                    tabs += 1
                elif "if(" in j or "while(" in j:
                    file.write("    " * tabs + j + ":\n")
                    tabs += 1
                elif j == "ENDW" or j == "ENDI":
                    tabs -= 1
                    continue
                elif j[:2] == "(.":
                    file.write("    " * tabs + j[2:][:len(j)-4] + "\n")
                elif j in ('(', ')'):
                    continue
                else:
                    file.write("    " * tabs + j + '\n')

            # Write return
            if to_return != "":
                file.write("        return(" + to_return[1:] + ")\n")
        
        # Write funcitons Get & Expect
        file.write('''
    
    def Get(self):
        self.t = self.la
        self.la = self.sc.scan()
        if self.la.get_tok_type() < 0 or self.la.get_tok_type() > self.maxT:
            self.la = self.t

    def Expect(self, expected):
        if self.la.get_tok_type() == expected:
            self.Get()
        else:
            self.SymError(expected)   ''')

        # Write funciton SymError
        file.write(''' 

    def SymError(self, expected):
        s = "Other"

        if expected == 0:
            s = "EOF"
        ''')

        for i in expected:

            file.write('''
        elif expected == ''' + str(i[0]) + ''':
            s = "''' + str(i[1]) + "\"\n")
        
        file.write('''
        print("Error: Expected " + s)
        print("Last token : " + str(self.t))
        print("Last Look-a: " + str(self.la))
        print("Scanner Pointer: " + str(self.sc.pointer))
        exit()
        ''')


                
        
