import lexer as lex
import automataPrinter as autPrint

print("Regex to Automatas")
regex = input("Ingrese regex: ")

# Paso 1: Leer regex
expr = lex.regexToExpr(regex)
alphabet = lex.regexToAlphabet(regex) 
# Paso 2: Descomponer la expresion en un arbol
root = lex.exprToDecompTree(expr)
# Paso 3: Arbol a NFA
nodes_nfa = lex.rootToNFA(root)
autPrint.printNFA(nodes_nfa, regex + "_nfa")
print("NFA completado")
# Paso 4: NFA to DFA
nodes_dfa = lex.fromNFAtoDFA(nodes_nfa, alphabet)
autPrint.printNFA(nodes_dfa, regex + "_dfa")
print("DFA completado")

# Prueba del Automatas
while True:
    word = input("Ingrese palabra a verificar: ")
    if word == "quit":
        break
    result1 = lex.simulateNFA(word, nodes_nfa)
    result2 = lex.simulateDFA(word, nodes_dfa)
    print("Segun el nfa " + result1 + " pertenece.")
    print("Segun el dfa " + result2 + " pertenece.")
    
