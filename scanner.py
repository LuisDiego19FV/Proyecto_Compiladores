import Lexer.lexer as lex
import Lexer.automataPrinter as autPrint

class Scanner():

    def __init__(self, filename):

        # COMPILER VARIABLES
        self.tag = ""
        self.filename = filename
        self.pointer = 0
        self.buffer = ""
        self.end_buffer = False
        self.ignore_chars = ""

        # ADD FILE TO BUFFER 
        file = open(filename)

        for i in file:
            self.buffer += i

        # AUTOMATA VARIABLES
        self.separateDFAs = []
        self.mainDFA = None

        self.process_tokens()

    def process_tokens(self):
        
        # AUTOMATAS TOKENS
        nodes0 = lex.regexToDFA("(if)","if",1.1)
        self.separateDFAs.append(nodes0)
        
        nodes1 = lex.regexToDFA("(switch)","switch",1.2)
        self.separateDFAs.append(nodes1)
        
        nodes2 = lex.regexToDFA("(do)","do",1.3)
        self.separateDFAs.append(nodes2)
        
        nodes3 = lex.regexToDFA("(while)","while",1.4)
        self.separateDFAs.append(nodes3)
        
        nodes4 = lex.regexToDFA("(\r|\n|\t|\r)((\r|\n|\t|\r))*","whitetoken",0.1)
        self.separateDFAs.append(nodes4)
        
        nodes5 = lex.regexToDFA("((+|-))?(0|1|2|3|4|5|6|7|8|9)((0|1|2|3|4|5|6|7|8|9))*","signnumber",0.2)
        self.separateDFAs.append(nodes5)
        
        nodes6 = lex.regexToDFA("(0|1|2|3|4|5|6|7|8|9)((0|1|2|3|4|5|6|7|8|9))*","number",0.3)
        self.separateDFAs.append(nodes6)
        
        nodes7 = lex.regexToDFA("(0|1|2|3|4|5|6|7|8|9|A|B|C|D|E|F)((0|1|2|3|4|5|6|7|8|9|A|B|C|D|E|F))*(H)","hexnumber",2.4)
        self.separateDFAs.append(nodes7)
        
        nodes8 = lex.regexToDFA("(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*","ident",2.5)
        self.separateDFAs.append(nodes8)
        
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

    