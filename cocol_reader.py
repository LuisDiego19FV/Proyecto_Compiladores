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
        self.comp_producs = []
        self.comp_producs_toks = []
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
                    components.append(")*")
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
                    if j[1] == "\"":
                        component += "(\\\")"
                    else:
                        component += "(" + j[1] + ")"
                    included = True
            
            if not included:
                component += i


        return (component, priority)

    def checkProductionEnd(self, line):

        line = line[::-1]

        for i in line:
            if ord(i) in (9, 10, 13, 32):
                continue

            if i == ".":
                return True

            else:
                return False

    def getProductionName(self, line):
        name = ""
        tmp_arg = ""
        arguments = []

        state = 0

        for i in line:
            if i == '<':
                 state = 1
                 continue

            elif i == ',' and state == 1:
                arguments.append(tmp_arg)
                tmp_arg = ""
                continue

            elif i == '>':
                if tmp_arg != "":
                    arguments.append(tmp_arg)
                break
            
            if state == 0:
                if i != " ":
                    name += i
            else:
                tmp_arg += i

        return (name, arguments)

    def getCleanProductions(self, production):

        clean_production = []

        # Remove front spaces
        for i in production:
            start = True
            tmp_section = ""
            for j in i:
                if start == True and  j == " ":
                    continue
                else:
                    start = False
                    tmp_section += j

            finnish = True
            k = tmp_section[::-1]
            tmp_section = ""
            for j in k:
                if finnish == True and  j == " ":
                    continue
                else:
                    finnish = False
                    tmp_section += j

            clean_production.append(tmp_section[::-1])

        # Remove empties
        clean_production = list(filter(lambda a: a != '', clean_production))

        return clean_production



    def getProduction(self, lines):
        
        new_lines = ""

        for i in lines:
            if i not in ("\n", "\t"):
                new_lines += i


        curr_section = ""
        sections = []
        in_proccess = False
        in_quote = False
        end_if_cycle = False
        end_cycle_counter = 0

        for i in new_lines:

            # Expresions
            if i in ("|", "{", "}", "\"") and curr_section != "" and not in_proccess:
                sections.append(curr_section)
                curr_section = ""
    
            curr_section += i

            if curr_section[::-1][:2] == ".(" and len(curr_section) > 2 and not in_proccess:
                sections.append(curr_section[:len(curr_section)-2])
                curr_section = "(."

            # Simbols and new tokens
            if curr_section == "(." and not in_proccess:
                in_proccess = True
                continue
            elif curr_section[::-1][:2] == ")." and in_proccess:
                in_proccess = False
                sections.append(curr_section)
                curr_section = ""
                continue
            elif len(curr_section) >= 2 and curr_section[len(curr_section)-2] == '(' and not in_proccess:
                sections.append('(')
                curr_section = curr_section[curr_section.index('(')+1:]
                continue
            elif curr_section[::-1][0] == ")" and not in_proccess:
                sections.append(curr_section[:len(curr_section)-1])

                if end_if_cycle:
                    end_if_cycle = False
                    sections.append("ENDI")

                sections.append(')')
                curr_section = ""
                continue
            elif curr_section == "|" and not in_proccess:
                if end_if_cycle:
                    end_if_cycle = False
                    sections.append("ENDI")

                counter = 0
                last_j = ""
                parenthesis_count = 0
                for j in sections[::-1]:
                    if j in ('}',")"):
                        parenthesis_count += 1
                    elif j in ('{','(') and parenthesis_count != 0:
                        parenthesis_count -= 1
                    elif j in ("{","(", "ENDI"):
                        last_j = j
                        break
                    counter += 1

                if last_j != "ENDI":
                    sections.insert(len(sections) - counter, "if")
                    sections.append("ENDI")

                sections.append('elif')
                end_if_cycle = True

                curr_section = ""
                continue
            elif curr_section == "{" and not in_proccess and not in_quote:
                sections.append("{")
                curr_section = ""
                continue
            elif curr_section == "}" and not in_proccess and not in_quote:
                if end_if_cycle:
                    end_if_cycle = False
                    sections.append("ENDI")
                sections.append("ENDW")
                curr_section = ""
                continue
            elif "[" in curr_section and not in_quote:
                sections.append("if")
                curr_section = ""
                continue
            elif curr_section == "]" and not in_quote:
                sections.append("ENDI")
                curr_section = ""
                continue
            elif curr_section == "\"" and not in_proccess:
                in_quote = True
                in_proccess = True
                continue
            elif curr_section[::-1][0] == "\"" and curr_section[::-1][1] != "\\" and in_proccess and in_quote:
                in_proccess = False
                in_quote = False

                new_pt_val = curr_section[1:][:len(curr_section)-2]

                new_pt_name = ""
                in_pt_tokens = False
                for i in self.comp_producs_toks:
                    if new_pt_val == i[1]:
                        in_pt_tokens = True
                        new_pt_name = i[0]
                        break
                
                if not in_pt_tokens:
                    new_pt_name = "pt" + str(len(self.comp_producs_toks))
                    self.comp_producs_toks.append((new_pt_name,new_pt_val))

                sections.append("self.Expect(self._" + new_pt_name + ")")
                curr_section = ""

                continue
            
            # End condition
            if curr_section[::-1][0] == "." and not in_proccess:
                sections.append(curr_section[:len(curr_section)-1])
                break

        sections = self.getCleanProductions(sections)

        return sections

    def repoccessProductions(self):
        all_prod_names = []
        for i in self.comp_producs:
            all_prod_names.append(i[0])

        if self.comp_name not in all_prod_names:
            print("ERROR 3-0: Missing production named after the compiler")
            print("PRODUCTIONS section")
            exit(0)

        all_tokens_names = []
        for i in (self.comp_tokens + self.comp_keywords):
            all_tokens_names.append(i[0])

        for i in self.comp_producs:
            productions = i[2]
            for j in range(len(productions)):
                if '<' in productions[j] and '>' in productions[j]:
                    tmp_prod = productions[j]
                    args = tmp_prod[tmp_prod.index('<') + 1:tmp_prod.index('>')].split(',')
                    tmp_prod = tmp_prod[:tmp_prod.index('<')]

                    if tmp_prod not in all_prod_names:
                        continue

                    new_prod = ""
                    args_str = ""

                    for k in args:
                        if "ref " in k:
                            k = k.replace('ref ', '')
                            k = k.replace(' ', '')
                            if new_prod == "":
                                new_prod += k
                            else:
                                new_prod += "," + k

                        if args_str == "":
                            args_str = k
                        else: 
                            args_str += ', ' + k 

                    if new_prod != "":
                        new_prod += " = "
                    
                    new_prod += "self." + tmp_prod + "(" + args_str + ")"
                    productions[j] = new_prod
                
                elif productions[j] in all_prod_names:
                    productions[j] = "self." + str(productions[j]) + "()"
                
                elif productions[j] in  all_tokens_names:
                    productions[j] = "self.Expect(self._" + str(productions[j]) + ")"
        
    def calFirstsProductions(self):
        all_prod_names = []
        all_prod_first = []

        for i in self.comp_producs:
            all_prod_names.append(i[0])

        for i in self.comp_producs:
            self.calFirstIfs(all_prod_names, i[2])
            self.calFirstWhiles(all_prod_names, i[2])
        
        for i in self.comp_producs:
            all_prod_first.append(self.calFirstProds(all_prod_names, i[2]))

        all_prod_names = all_prod_names[::-1]
        all_prod_first = all_prod_first[::-1]

        for i in range(len(all_prod_first)):
            if "FIRST:" in all_prod_first[i]:
                while "FIRST:" in all_prod_first[i]:
                    p_prod = all_prod_first[i]
                    p_prod = p_prod[p_prod.index("FIRST:") + 6:]
                    if " " in p_prod:
                        p_prod = p_prod[:p_prod.index(" ")]

                    p_index = all_prod_names.index(p_prod)

                    all_prod_first[i] = all_prod_first[i].replace("FIRST:" + p_prod, all_prod_first[p_index])

        for i in self.comp_producs:
            for j in range(len(i[2])):
                if "FIRST:" in i[2][j]:
                    while "FIRST:" in i[2][j]:
                        p_prod = i[2][j]
                        p_prod = p_prod[p_prod.index("FIRST:") + 6:]
                        if " " in p_prod:
                            p_prod = p_prod[:p_prod.index(" ")]
                        elif ")" in p_prod:
                            p_prod = p_prod[:p_prod.index(")")]
                        
                        p_index = all_prod_names.index(p_prod)

                        i[2][j] = i[2][j].replace("FIRST:" + p_prod, all_prod_first[p_index])

        all_prod_names = all_prod_names[::-1]
        all_prod_first = all_prod_first[::-1]

    def calFirstIfs(self, all_prod_names, prods):
        cal = False
        cal_index = 0
        for i in range(len(prods)):
            if prods[i] == "if" or prods[i] == "[" or prods[i] == "elif":
                cal = True
                cal_index = i
            
            elif cal and "Expect(" in prods[i]:
                tmp_first = prods[i][prods[i].index("Expect(") + 7: prods[i].index(")")]
                if prods[cal_index] in ("if","["):
                    prods[cal_index] = "if(self.la.get_tok_type() == " + tmp_first + ")"
                else:
                    prods[cal_index] = "elif(self.la.get_tok_type() == " + tmp_first + ")"
                cal = False
            
            elif cal and "self." in prods[i]:
                tmp_first = prods[i][prods[i].index("self.") + 5: prods[i].index("(")]
                if tmp_first in all_prod_names:
                    prods[cal_index] ="if(FIRST:" + tmp_first + ")"
                cal = False
    
    def calFirstWhiles(self, all_prod_names, prods):
        cal = False
        same = False
        in_while = False
        other_c = 0
        cal_index = 0
        conditions = []
        for i in range(len(prods)):

            if prods[i] == "{" and not cal and not same and not in_while:
                cal = True
                same = True
                in_while = True
                cal_index = i

            elif (prods[i] == "{" or "while(" in prods[i]) and in_while:
                other_c += 1

            elif cal and ("if(" in prods[i] or "elif(" in prods[i]):
                same = False
                tmp_first = prods[i][prods[i].index("if(") + 3: len(prods[i]) - 1]
                conditions.append(tmp_first)
            
            elif cal and not same and prods[i] == "ENDI":
                same = True

            elif cal and same and "Expect(" in prods[i]:
                tmp_first = prods[i][prods[i].index("Expect(") + 7: prods[i].index(")")]
                conditions.append("self.la.get_tok_type() == " + tmp_first)
                cal = False
            
            elif cal and same and "self." in prods[i]:
                tmp_first = prods[i][prods[i].index("self.") + 5: prods[i].index("(")]
                if tmp_first in all_prod_names:
                    conditions.append("FIRST:" + tmp_first)
                    cal = False

            elif prods[i] == "ENDW" and other_c != 0 and in_while:
                other_c -= 1

            elif prods[i] == "ENDW" and in_while:
                new_conditions = ""
                for j in conditions:
                    if new_conditions == "":
                        new_conditions += "(" + j
                    else:
                        new_conditions += " or " + j

                if new_conditions == "":
                    new_conditions += "("

                new_conditions += ")"
                prods[cal_index] = "while" + new_conditions 

                cal = False
                same = False
                in_while = False

                other_c = 0
                cal_index = 0
                conditions = []

        if "{" in prods:
            self.calFirstWhiles(all_prod_names, prods)

    def calFirstProds(self, all_prod_names, prods):

        ifs = False
        conditions = []
        for i in prods:
            if "if(" in i:
                tmp_first = i[i.index("if(") + 3: len(i) - 1]
                conditions.append(tmp_first)
                ifs = True

            elif "ENDI" in i and not ifs:
                ifs = False

            elif "while(" in i and not ifs:
                tmp_first = i[i.index("while(") + 6: len(i) - 1]
                conditions.append(tmp_first)

            elif "Expect(" in i and not ifs:
                tmp_first = i[i.index("Expect(") + 7: i.index(")")]
                return("self.la.get_tok_type() == " + tmp_first)

            elif "self." in i and not ifs:
                tmp_first = i[i.index("self.") + 5: i.index("(")]
                if tmp_first in all_prod_names:
                    return("FIRST:" + tmp_first)

        one_cond = ""
        for i in conditions:
            if one_cond == "":
                one_cond += i
            else:
                one_cond += " or " + i

        return one_cond





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

        # Production variables
        on_pruduction = False
        curr_pruduction = []
        curr_pruduction_lines = ""

        # Reader
        for i in file:
            
            # Check header
            if counter == 0:
                if "COMPILER " in i: 
                    self.comp_name = i[9:].replace("\n",'')
                    self.comp_name = self.comp_name.replace(' ', '')
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
                if "CHARACTERS" in i and curr_section != "PRO":
                    old_sections.append(curr_section)
                    curr_section = "CHA"
                elif "KEYWORDS" in i and curr_section != "PRO":
                    old_sections.append(curr_section)
                    curr_section = "KEY"
                elif "TOKENS" in i and curr_section != "PRO":
                    old_sections.append(curr_section)
                    curr_section = "TOK"
                elif "PRODUCTIONS" in i and curr_section != "PRO":
                    old_sections.append(curr_section)
                    curr_section = "PRO"
                elif "END" in i and self.comp_name in i:
                    break

            # Read characters, keywords and tokens
            if curr_section in ("CHA","KEY","TOK") and "=" in i:

                new_name = i[:i.index("=")]
                new_val = i[i.index("=") + 1:]
                counter = 0

                # Remove spaces in name of name
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


            # Read production
            elif curr_section == "PRO" and not on_pruduction and "=" in i: 
                new_name = i[:i.index("=")]
                new_line = i[i.index("=") + 1:]
                new_name, new_args = self.getProductionName(new_name)

                curr_pruduction.append(new_name)
                curr_pruduction.append(new_args)

                if self.checkProductionEnd(new_line):
                    curr_pruduction.append(self.getProduction(new_line))
                    self.comp_producs.append(curr_pruduction)

                    curr_pruduction = []

                else:
                    curr_pruduction_lines += " " + new_line
                    on_pruduction = True
            
            elif curr_section == "PRO" and on_pruduction:
                curr_pruduction_lines += " " + i

                if self.checkProductionEnd(i):
                    curr_pruduction.append(self.getProduction(curr_pruduction_lines))
                    self.comp_producs.append(curr_pruduction)

                    curr_pruduction = []
                    curr_pruduction_lines = ""
                    on_pruduction = False

            # Counter
            counter += 1

        self.repoccessProductions()
        self.calFirstsProductions()

        file.close()

