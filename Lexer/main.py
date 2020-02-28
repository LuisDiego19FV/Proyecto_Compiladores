import lexer as lex
import automataPrinter as autPrint

print("Regex to NFA")
regex = input("Ingrese regex: ")

# Paso 1: leer regex
expr = lex.regexToExpr(regex)
# Paso 2: descomponer la expresion en un arbol
root = lex.exprToDecompTree(expr)
# Paso 3: arbol a NFA
nodes = lex.rootToNFA(root)
autPrint.printNFA(nodes, regex + "_nfa")

print("nfa completado")

# Prueba del NFA
while True:
    word = input("Ingrese palabra a verificar con el NFA: ")
    if word == "quit":
        break
    if len(word) > 0:
        result = lex.simulateNFA(word,nodes)
    else:
        reult = "NO"
    print("Pertenece L: " + result)
    
