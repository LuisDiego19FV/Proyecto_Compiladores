import lexer as lex
import automataPrinter as autPrint

print("Regex to NFA")
regex = input("Ingrese regex:")
print("...")

# Paso 1: leer regex
expr = lex.regexToExpr(regex)
# Paso 2: descomponer la expresion en un arbol
root = lex.exprToDecompTree(expr)
# Paso 3: arbol a NFA
nodes = lex.rootToNFA(root)
autPrint.printNFA(nodes)

print("DONE")
