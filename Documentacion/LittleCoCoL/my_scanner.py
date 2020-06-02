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

        nodes0 = lex.regexToDFA("(>)","endarg",1)
        self.separateDFAs.append(nodes0)
        
        nodes1 = lex.regexToDFA("(<)","startarg",2)
        self.separateDFAs.append(nodes1)
        
        nodes2 = lex.regexToDFA("(.))","endcode",3)
        self.separateDFAs.append(nodes2)
        
        nodes3 = lex.regexToDFA("((.)","startcode",4)
        self.separateDFAs.append(nodes3)
        
        nodes4 = lex.regexToDFA("(CHR)(0|1|2|3|4|5|6|7|8|9)((0|1|2|3|4|5|6|7|8|9))*","charnumber",5)
        self.separateDFAs.append(nodes4)
        
        nodes5 = lex.regexToDFA("(\")(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9))*(\")","string",6)
        self.separateDFAs.append(nodes5)
        
        nodes6 = lex.regexToDFA("(')((\))*(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)(')","char",7)
        self.separateDFAs.append(nodes6)
        
        nodes7 = lex.regexToDFA("ANY","pt18",8)
        self.separateDFAs.append(nodes7)

        nodes8 = lex.regexToDFA("}","pt17",9)
        self.separateDFAs.append(nodes8)

        nodes9 = lex.regexToDFA("{","pt16",10)
        self.separateDFAs.append(nodes9)

        nodes10 = lex.regexToDFA("]","pt15",11)
        self.separateDFAs.append(nodes10)

        nodes11 = lex.regexToDFA("[","pt14",12)
        self.separateDFAs.append(nodes11)

        nodes12 = lex.regexToDFA(")","pt13",13)
        self.separateDFAs.append(nodes12)

        nodes13 = lex.regexToDFA("(","pt12",14)
        self.separateDFAs.append(nodes13)

        nodes14 = lex.regexToDFA("|","pt11",15)
        self.separateDFAs.append(nodes14)

        nodes15 = lex.regexToDFA("EXCEPT","pt10",16)
        self.separateDFAs.append(nodes15)

        nodes16 = lex.regexToDFA("PRODUCTIONS","pt9",17)
        self.separateDFAs.append(nodes16)

        nodes17 = lex.regexToDFA("TOKENS","pt8",18)
        self.separateDFAs.append(nodes17)

        nodes18 = lex.regexToDFA("KEYWORDS","pt7",19)
        self.separateDFAs.append(nodes18)

        nodes19 = lex.regexToDFA(".","pt6",20)
        self.separateDFAs.append(nodes19)

        nodes20 = lex.regexToDFA("-","pt5",21)
        self.separateDFAs.append(nodes20)

        nodes21 = lex.regexToDFA("+","pt4",22)
        self.separateDFAs.append(nodes21)

        nodes22 = lex.regexToDFA("=","pt3",23)
        self.separateDFAs.append(nodes22)

        nodes23 = lex.regexToDFA("CHARACTERS","pt2",24)
        self.separateDFAs.append(nodes23)

        nodes24 = lex.regexToDFA("END","pt1",25)
        self.separateDFAs.append(nodes24)

        nodes25 = lex.regexToDFA("COMPILER","pt0",26)
        self.separateDFAs.append(nodes25)

        nodes26 = lex.regexToDFA("(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*","ident",27)
        self.separateDFAs.append(nodes26)
        
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

        #IF NO TOKEN FOUND
        if token == "":
            characters = self.buffer[self.pointer: counter + len(tokens) - 1]
            self.pointer = counter + len(tokens) - 1
            return cls_token("non_token", characters, -1)
        
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