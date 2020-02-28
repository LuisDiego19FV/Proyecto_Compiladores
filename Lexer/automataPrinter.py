from PySimpleAutomata import automata_IO

def printNFA(nodes, name_output):
    file = open("cache/nfadotrep.dot","w") 

    file.write('''digraph {
    fake0 [style=invisible]
    T0 [root=true]
    fake0 -> T0 [style=bold]\n''')

    for i in range(len(nodes)):
        if nodes[i].getIsAcceptanceState():
            file.write("    " + str(nodes[i].getState()) + " [shape=doublecircle]\n")
        else:
            file.write("    " + str(nodes[i].getState()) + "\n")
    for i in nodes:
        for j in i.getTransition():
            file.write("    " + str(i.getState()) + " -> " + str(j[0].getState()) + " [label=\"" + str(j[1]) + "\"]\n")

    file.write("}")

    file.close() 

    nfa = automata_IO.nfa_dot_importer('cache/nfadotrep.dot')

    name_toprint = ""
    for i in name_output:
        if i == "*":
            name_toprint += "^"
        elif i == "|":
            name_toprint += ";"
        elif i == "?":
            name_toprint += "!"
        else:
            name_toprint += i

    automata_IO.nfa_to_dot(nfa, "output/" + str(name_toprint))