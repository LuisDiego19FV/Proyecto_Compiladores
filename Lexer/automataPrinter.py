from PySimpleAutomata import automata_IO

def printAutomata(nodes, name_output):
    file = open("Automata/dotreptmp.dot","w") 

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
            if j[1] == "ε":
                file.write("    " + str(i.getState()) + " -> " + str(j[0].getState()) + " [label=\"" + str("EP") + "\"]\n")
            else:
                file.write("    " + str(i.getState()) + " -> " + str(j[0].getState()) + " [label=\"" + str(j[1]) + "\"]\n")

    file.write("}")

    file.close() 

    nfa = automata_IO.nfa_dot_importer('Automata/dotreptmp.dot')

    name_toprint = ""
    for i in name_output:
        if i == "ε":
            name_toprint += "EP"
        elif i == "*":
            name_toprint += "^"
        elif i == "|":
            name_toprint += ";"
        elif i == "?":
            name_toprint += "!"
        else:
            name_toprint += i

    automata_IO.nfa_to_dot(nfa,"Automata/" + str(name_toprint))