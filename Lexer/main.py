import time
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
print("NFA 1 completado (Thompson)")
# Paso 4: NFA to DFA
nodes_dfa1 = lex.fromNFAtoDFA(nodes_nfa1, alphabet)
autPrint.printNFA(nodes_dfa1, regex + "_dfa_1")
print("DFA 1 completado (NFA->DFA)")
# Paso 5: Arbol a DFA
nodes_dfa2 = lex.rootToDFA(rootDFA, alphabet)
autPrint.printNFA(nodes_dfa2, regex + "_dfa_2")
print("DFA 2 completado (Directo)")
# Paso 6: DFA a DFA Optimo
nodes_dfa3 = lex.minimization(nodes_dfa1)
autPrint.printNFA(nodes_dfa3, regex + "_dfa_3")
print("DFA 3 completado (Optimizacion)")


# Prueba del Automatas
while True:
    word = input("\nIngrese palabra a verificar: ")
    if word == "quit":
        break
    # NFA 1
    start1 = time.time()
    result1 = lex.simulateNFA(word, nodes_nfa1)
    end1 = time.time()
    # DFA 1
    start2 = time.time()
    result2 = lex.simulateDFA(word, nodes_dfa1)
    end2 = time.time()
    # DFA 2
    start3 = time.time()
    result3 = lex.simulateDFA(word, nodes_dfa2)
    end3 = time.time()
    # DFA 3
    start4 = time.time()
    result4 = lex.simulateDFA(word, nodes_dfa3)
    end4 = time.time()
    print("Segun el nfa 1 " + result1 + " pertenece. Time: " + str(end1 - start1) + "s")
    print("Segun el dfa 1 " + result2 + " pertenece. Time: " + str(end2 - start2) + "s")
    print("Segun el dfa 2 " + result3 + " pertenece. Time: " + str(end3 - start3) + "s")
    print("Segun el dfa 3 " + result4 + " pertenece. Time: " + str(end4 - start4) + "s")
    
