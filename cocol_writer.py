# cocol_writer.py
# By: Luis Diego Fernandez

class CocolWriter():

    def __init__(self, file_name = "test.py"):
        # file specifications
        self.file_name = file_name
        self.keywords= []
        self.tokens = []
        self.ignore_chars = ""

    def setKeywords(self, keywords):
        self.keywords = keywords

    def setTokens(self, tokens):
        self.tokens = tokens

    def setIgnoreChars(self, chars):
        self.ignore_chars = chars

    def startWriting(self):
        file = open(self.file_name, "w")

        file.write(
'''import Lexer.lexer as lex
import Lexer.automataPrinter as autPrint

class Scanner():

    def __init__(self, filename):

        # COMPILER VARIABLES
        self.tag = ""
        self.filename = filename
        self.pointer = 0
        self.buffer = ""
        self.end_buffer = False
        self.ignore_chars = "''' + str(self.ignore_chars) + '''"

        # ADD FILE TO BUFFER 
        file = open(filename)

        for i in file:
            self.buffer += i

        # AUTOMATA VARIABLES
        self.separateDFAs = []
        self.mainDFA = None

        self.process_tokens()

    def process_tokens(self):
        
        # AUTOMATAS TOKENS''')

        # Write keywords
        counter = 0
        priorityAdder = 0
        keys = self.keywords[::-1]
        for i in keys:

            # Priority
            priorityAdder += 1
            if priorityAdder % 10 == 0:
                priorityAdder = int("9" * (len(str(priorityAdder)) - 1) + "1")

            # White spaces restriccions
            regex = i[1].replace("\n", "\\n")
            regex = regex.replace("\r", "\\r")
            regex = regex.replace("\t", "\\t")

            # Write token
            file.write('''
        nodes''' + str(counter) + \
            ''' = lex.regexToDFA("''' + regex + '''","''' + str(i[0]) + '''",''' + str(i[2]) + '''.''' 
            + str(priorityAdder) + ''')
        self.separateDFAs.append(nodes''' + str(counter) + ''')
        ''')
            counter += 1

        # Write tokens
        priorityAdder = 0
        tokens = self.tokens[::-1]
        for i in tokens:

            # Priority
            priorityAdder += 1
            if priorityAdder % 10 == 0:
                priorityAdder = int("9" * (len(str(priorityAdder)) - 1) + "1")

            # White spaces restriccions
            regex = i[1].replace("\n", "\\n")
            regex = regex.replace("\r", "\\r")
            regex = regex.replace("\t", "\\t")

            # Write token
            file.write('''
        nodes''' + str(counter) + \
            ''' = lex.regexToDFA("''' + regex + '''","''' + str(i[0]) + '''",''' + str(i[2]) + '''.''' 
            + str(priorityAdder) + ''')
        self.separateDFAs.append(nodes''' + str(counter) + ''')
        ''')
            counter += 1

        file.write('''
        # MAIN DFA
        nodes = nodes0
        counter = 0
        for i in self.separateDFAs:
            transitions = i[0].getTransition()
            for j in range(len(transitions)):
                to = transitions[j][0]
                by = transitions[j][1]
                nodes[0].setTransition(to, by)
            
            nodes += i[1:]

        counter = 0
        for node in nodes:
            node.setState("T" + str(counter))
            counter += 1

        autPrint.printAutomata(nodes,"test")
        
        self.mainDFA = nodes

    # COMPONER
    def scan(self):
        # TOKEN VARIABLES
        token = ""
        tokens = []
        characters = self.buffer[self.pointer: self.pointer + 1]
        tmp_token = lex.simulateDFA(characters, self.mainDFA)

        # COUNTER
        counter = self.pointer

        # IMIDATE END OF BUFFER
        if self.end_buffer:
            return (0 ,"end_token")

        # IMIDATE NOT A TOKEN
        if tmp_token == "not_a_token":
            if self.pointer >= len(self.buffer):
                return (1 ,"end_token")
            else:
                self.pointer += 1
                return (characters, "not_a_token")

        tokens.append(tmp_token)

        # GET TOKEN UNTIL NOT A TOKEN
        while tmp_token != "not_a_token" and counter <= len(self.buffer):
            counter += 1
            characters = self.buffer[self.pointer: counter]

            # remove unecessary chars
            for i in self.ignore_chars:
                characters = characters.replace(i,'')

            tmp_token = lex.simulateDFA(characters, self.mainDFA)

            if tmp_token != "not_a_token":
                tokens.append(tmp_token)

        # GET LAST TOKEN
        tokens = tokens[::-1]
        for i in tokens:
            if i != "keep_going":
                token = i
                break
            else:
                counter -= 1

        # IF NOT TOKEN FOUND
        if token == "":
            characters = self.buffer[self.pointer: counter + len(tokens) - 1]
            self.pointer = counter + len(tokens) - 1
            return (characters, "not_a_token")
        
        # TOKEN LENGHT CONDITION
        if self.pointer == counter - 1:
            characters = self.buffer[self.pointer: counter]

            # remove unecessary chars
            for i in self.ignore_chars:
                characters = characters.replace(i,'')

            self.pointer = counter
        else:
            characters = self.buffer[self.pointer: counter - 1]

            # remove unecessary chars
            for i in self.ignore_chars:
                characters = characters.replace(i,'')

            self.pointer = counter - 1

        # END CONDITION
        if self.pointer == len(self.buffer):
            self.end_buffer = True

        return (characters, token)
    
    # BUFFER RESET
    def reset_buffer(self):
        self.end_buffer = False

    ''')
        
