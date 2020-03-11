import lexer as lex
import automataPrinter as autPrint

# Paso 0: Input
print("Regex to Automatas")
regex = input("Ingrese regex: ")

# Paso 1: Leer regex
expr = lex.regexToExpr(regex)
alphabet = lex.regexToAlphabet(regex) 
# Paso 2: Descomponer la expresion en arboles
rootNFA = lex.exprToDecompTreeNFA(expr)
rootDFA = lex.exprToDecompTreeDFA(expr)
# Paso 3: Arbol a NFA
nodes_nfa1 = lex.rootToNFA(rootNFA)
autPrint.printNFA(nodes_nfa1, regex + "_nfa_1")
print("NFA 1 completado")
# Paso 4: NFA to DFA
nodes_dfa1 = lex.fromNFAtoDFA(nodes_nfa1, alphabet)
autPrint.printNFA(nodes_dfa1, regex + "_dfa_1")
print("DFA 1 completado")
# Paso 5: Arbol a DFA
nodes_dfa2 = lex.rootToDFA(rootDFA, alphabet)
autPrint.printNFA(nodes_dfa2, regex + "_dfa_2")
print("DFA 2 completado")

# Prueba del Automatas
while True:
    word = input("Ingrese palabra a verificar: ")
    if word == "quit":
        break
    result1 = lex.simulateNFA(word, nodes_nfa1)
    result2 = lex.simulateDFA(word, nodes_dfa1)
    result3 = lex.simulateDFA(word, nodes_dfa2)
    print("Segun el nfa 1 " + result1 + " pertenece.")
    print("Segun el dfa 1 " + result2 + " pertenece.")
    print("Segun el dfa 2 " + result3 + " pertenece.")
    
