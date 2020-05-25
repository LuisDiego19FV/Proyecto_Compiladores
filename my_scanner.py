import Lexer.lexer as lex
from Lexer.nodes import Token as cls_token

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

        nodes0 = lex.regexToDFA("(\r|\n|\t| )((\r|\n|\t| ))*","white",1)
        self.separateDFAs.append(nodes0)
        
        nodes1 = lex.regexToDFA("(.)((\r|\n|\t| ))*","endpoint",2)
        self.separateDFAs.append(nodes1)
        
        nodes2 = lex.regexToDFA("(=)((\r|\n|\t| ))*","equal",3)
        self.separateDFAs.append(nodes2)
        
        nodes3 = lex.regexToDFA("(CHR)","chardef",4)
        self.separateDFAs.append(nodes3)
        
        nodes4 = lex.regexToDFA("(0|1|2|3|4|5|6|7|8|9)((0|1|2|3|4|5|6|7|8|9))*","number",5)
        self.separateDFAs.append(nodes4)
        
        nodes5 = lex.regexToDFA("(EXCEPT KEYWORDS)","expect_key",6)
        self.separateDFAs.append(nodes5)

        nodes6 = lex.regexToDFA("(END)","end_section",7)
        self.separateDFAs.append(nodes6)

        nodes7 = lex.regexToDFA("(PRODUCTIONS)","pro_section",8)
        self.separateDFAs.append(nodes7)

        nodes8 = lex.regexToDFA("(TOKENS)","tok_section",9)
        self.separateDFAs.append(nodes8)

        nodes9 = lex.regexToDFA("(KEYWORDS)","key_section",10)
        self.separateDFAs.append(nodes9)

        nodes10 = lex.regexToDFA("(CHARACTERS)","char_seciton",11)
        self.separateDFAs.append(nodes10)

        nodes11 = lex.regexToDFA("(COMPILER)","comp_section",12)
        self.separateDFAs.append(nodes11)

        nodes12 = lex.regexToDFA("(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)((a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z))*","name",13)
        self.separateDFAs.append(nodes12)

        nodes13 = lex.regexToDFA("}","pt3",14)
        self.separateDFAs.append(nodes13)

        nodes14 = lex.regexToDFA("{","pt2",15)
        self.separateDFAs.append(nodes14)

        nodes15 = lex.regexToDFA("|","pt1",16)
        self.separateDFAs.append(nodes15)

        nodes16 = lex.regexToDFA("\"","pt0",17)
        self.separateDFAs.append(nodes16)
        
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
            return cls_token("end_token", characters, -3)

        # IMIDATE NOT A TOKEN
        if tmp_token.get_tok_type() == -1:
            if self.pointer >= len(self.buffer):
                return cls_token("end_token", characters, -3)
            else:
                self.pointer += 1
                return tmp_token

        tokens.append(tmp_token)

        # GET TOKEN UNTIL NOT A TOKEN
        while tmp_token.get_tok_type() != -1 and counter <= len(self.buffer):
            counter += 1
            characters = self.buffer[self.pointer: counter]

            # remove unecessary chars
            for i in self.ignore_chars:
                characters = characters.replace(i,'')

            tmp_token = lex.simulateDFA(characters, self.mainDFA)

            if tmp_token.get_tok_type() != -1:
                tokens.append(tmp_token)

        # GET LAST TOKEN
        tokens = tokens[::-1]
        for i in tokens:
            if i.get_tok_type() != -2:
                token = i
                break
            else:
                counter -= 1

        #IF NOT TOKEN FOUND
        if token == "":
            characters = self.buffer[self.pointer: counter + len(tokens) - 1]
            self.pointer = counter + len(tokens) - 1
            return cls_token("end_token", characters, -3)
        
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

        return token
    
    # BUFFER RESET
    def reset_buffer(self):
        self.end_buffer = False