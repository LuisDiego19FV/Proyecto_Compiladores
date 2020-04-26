# cocol_writer.py
# By: Luis Diego Fernandez

class CocolReader():    

    def __init__(self, file_name = "test.txt"):
        # file specifications
        self.file_name = file_name

        # Compiler specifications
        self.comp_name  = ""
        self.comp_chars = []
        self.comp_keywords = []
        self.comp_tokens = []
        self.comp_ignore = ""

    
    # getValChar(String)
    # Used for reading a string in the CHARACTERS section of a cocol/R file and storing
    # the new stablished characters.
    def getValChar(self, s):

        other_chars = self.comp_chars
    
        # Components of the character
        components = []
        tmp_component = ""

        # Booleans for the loop
        string_stater = True
        char_starter = True
        second_point = False

        # Read letter by letter
        for i in s:
            # Skip blanks
            if i == " " and string_stater and char_starter:
                continue

            # point counter and exit
            if i != "." and second_point:
                break
            elif i == "." and second_point:
                second_point = False

                if tmp_component != "":
                    components.append(tmp_component)

                components.append("..")
                tmp_component = ""
                continue

            tmp_component += i

            # Case of a string
            if i == "\"":
                if string_stater:
                    if len(tmp_component) > 1:
                        components.append(tmp_component)
                        tmp_component = ""
                    string_stater = False
                else:
                    string_stater = True
                    components.append(tmp_component)
                    tmp_component = ""

            # Case of a char
            elif i == "\'":
                if char_starter:
                    if len(tmp_component) > 1:
                        components.append(tmp_component)
                        tmp_component = ""
                    char_starter = False
                else:
                    char_starter = True
                    components.append(tmp_component)
                    tmp_component = ""

            # Case of an operant
            elif i in ("+","-") and string_stater and char_starter:
                if len(tmp_component) > 1:
                    components.append(tmp_component[:tmp_component.index(i)])
                    tmp_component = i
                components.append(tmp_component * 3)
                tmp_component = ""

            # Case of point and double point
            elif i == "." and string_stater and char_starter:
                tmp_component = tmp_component[:len(tmp_component) - 1]
                second_point = not second_point

        # Apend last component if needed
        if tmp_component != "":
            components.append(tmp_component)
        
        # Check for use of other characters
        for i in range(len(components)):
            for j in other_chars:
                if components[i] == j[0]:
                    components[i] = j[1]

        # Remove quotes after character check
        new_components = []
        for i in components:
            comp = i
            comp = comp.replace("\"","")
            comp = comp.replace("\'","")

            if comp[:4] == "CHR(":
                comp = comp.lower()
                comp = chr(int(comp[comp.index("(") + 1: comp.index(")")]))
 
            new_components.append(comp)

        components = new_components

        # check for double points
        new_components = []
        skiper = False
        for i in range(len(components)):
            if skiper:
                skiper = False
                continue

            # Case of from char to char
            if components[i] == "..":
                new_comp = ""

                for i in range(ord(components[i-1]), ord(components[i+1])+1):
                    new_comp += chr(i)

                new_components[len(new_components) - 1] = new_comp
                skiper = True

            else:
                new_components.append(components[i])

        components = new_components

        # Check for use of operants + or -
        component = components[0]
        skiper = False
        for i in range(len(components)):

            if skiper:
                skiper = False
                continue
            
            # Caes of union
            if components[i] == "+++":
                component += components[i+1]
                skiper = True

            # Case of exclusion
            elif components[i] == "---":
                new_comp = ""
        
                for j in component:
                    j_in_k = False

                    for k in components[i+1]:
                        if j == k:
                            j_in_k = True

                    if not j_in_k:
                        new_comp += j
                
                component = new_comp
                skiper = True

        # Add ors for the regex
        val = ""
        for j in component:
            if j != "|":
                val +=  str(j) + "|"
        
        val = val[:len(val) - 1]

        # It should only return the union of every component
        return val

    # getValToken(String)
    # Used for reading a string in the TOKEN section of a cocol/R file and storing
    # the new stablished characters.
    def getValToken(self, s):
        
        component = ""
        components = []
        priority = 0
        char_stater = False
        string_stater = False

        for i in s:
            # Skip blanks
            if i == " " and not char_stater and not string_stater:
                continue

            # Case of a string
            if i == "\"":
                if string_stater:
                    components.append("(" + component + ")")
                    component = ""
                string_stater = not string_stater

            elif string_stater:
                component += i

            # Case of a char
            elif i == "\'":
                if string_stater:
                    components.append(component)
                    component = ""
                string_stater = not char_stater

            elif char_stater:
                component += i

            elif i in ("|", "{", "}","[","]","(",")"):
                components.append(component)
                component = ""

                if i == "{":
                    components.append("(")
                elif i == "}":
                    components.append(")*")
                elif i == "[":
                    components.append("(")
                elif i == "]":
                    components.append(")?")
                elif i == "|":
                    components.append("|")
                

            elif i == ".":
                components.append(component)
                break
            
            else:
                component += i

        component = ""

        # Check use  of characters or chars
        for i in components:

            if "EXCEPTKEYWORDS" in i:
                i = i.replace("EXCEPTKEYWORDS", '')
                priority = 2

            if i[:4] == "CHR(":
                comp = comp.lower()
                comp = chr(int(comp[comp.index("(") + 1: comp.index(")")]))
                component += comp
                continue
                
            included = False
            for j in self.comp_chars:
                if i == j[0]:
                    component += "(" + j[1] + ")"
                    included = True
            
            if not included:
                component += i


        return (component, priority)

    # startReading()
    # Used for starting the reading process of the specified file. Allowing to read the 
    # components of the cocol/R file.
    def startReading(self):
        # file
        file = open(self.file_name, "r")

        # Loop variables
        curr_section = "None"
        old_sections = []
        counter = 0

        # Reader
        for i in file:
            
            # Check header
            if counter == 0:
                if "COMPILER " in i: 
                    self.comp_name = i[9:]
                    curr_section = "COM"
                else:
                    print("ERROR 0-0: Missing Header")
                    print("Line 1")
                    exit(0)

            if "IGNORE" in i:
                print(i[6:])
                setIgnore = i[6:]
                new_val = self.getValChar(setIgnore)
                self.comp_ignore = new_val[0]
            
            # Check and change section
            if "." not in i and "=" not in i:
                if "CHARACTERS" in i:
                    old_sections.append(curr_section)
                    curr_section = "CHA"
                elif "KEYWORDS" in i:
                    old_sections.append(curr_section)
                    curr_section = "KEY"
                elif "TOKENS" in i:
                    old_sections.append(curr_section)
                    curr_section = "TOK"
                elif "PRODUCTIONS" in i:
                    old_sections.append(curr_section)
                    curr_section = "PRO"
                elif "END" in i and self.comp_name in i:
                    break

            # Read characters
            if curr_section in ("CHA","KEY","TOK") and "=" in i:

                new_name = i[:i.index("=")]
                new_val = i[i.index("=") + 1:]
                counter = 0

                # Remove spaces in name of char
                tmp_name = ""
                for j in new_name:
                    if j != " ":
                        tmp_name += j
                
                new_name = tmp_name

                if curr_section == "CHA":
                    new_val = self.getValChar(new_val)
                    self.comp_chars.append((new_name,new_val,i))
                
                elif curr_section == "KEY":
                    new_val = self.getValToken(new_val)
                    self.comp_keywords.append((new_name,new_val[0],1,i))
                
                elif curr_section == "TOK":
                    new_val = self.getValToken(new_val)
                    self.comp_tokens.append((new_name,new_val[0], new_val[1],i))

            # Counter
            counter += 1
        
        file.close()

