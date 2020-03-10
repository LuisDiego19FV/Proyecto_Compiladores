from nodes import DecompositionTree as dt
from nodes import DecompositionTreeDFA as dfadt
from nodes import NFATree as nt
from nodes import DFATree as dfat

# regexToExpr(String)
# Separa cada elemento del regex en sus componentes y operadores
# Regresa un array con el regex separado en sus elementos
def regexToExpr(regex):
    expresions = []
    skips = 0

    # Se revisa cada elemento del reges
    for i in range(len(regex)):
        # permite saltear en caso de parentesis
        if skips > 0:
            skips -= 1

        # operadores
        elif regex[i] in ("*", "+", "?"):
            expresions[len(expresions) - 1] += regex[i]

        # todo dentro el parentesis cuenta como un elemento
        elif regex[i] == "(":
            counter = 0
            skip_next = 0
            for j in regex[i + 1:]:
                counter += 1
                if j == ")": 
                    if skip_next > 0:
                        skip_next -= 1
                    else:
                        break
                if j == "(":
                    skip_next += 1
            next_parenthesis = len(regex[:i]) + counter
            expresions.append(regex[i:next_parenthesis + 1])
            skips += next_parenthesis - i
        
        # letra parte del alfabeto
        else:
            expresions.append(regex[i])
        
    return expresions

# regexToAlphabet(String)
# Devuelve un array con solo los componentes en el abecedario utilizado por el lenguaje
# descrito por el regex
def regexToAlphabet(regex):
    alphabet = []

    for i in regex:
        if i not in ("(", ")", "*", "+", "?", "|"):
            alphabet.append(i)

    alphabet = list(dict.fromkeys(alphabet))
    
    return alphabet

# exprToDecompTree(Array, int)
# Pasa cada expresion a un arbol donde se separa segun elementos y operadores, todo
# bajo un orden logico
# Regresa el root de un arbol con los elementos
def exprToDecompTreeNFA(expr, cnt = 0):
    expr = expr[::-1]
    root = dt(cnt)
    tmpRoot = root
    counter = cnt
    repetitions = 0

    for i in expr:
        repetitions += 1

        # caso especial del OR
        if i == "|":
            tmpRoot.setChild(dt("|", True), 1)
            continue

        # pone el siguiente nodo en la posicion deseada
        counter += 1
        newNode = dt(counter)
        if tmpRoot.getChild()[2] == None:
            tmpRoot.setChild(newNode, 2)
        elif repetitions >= len(expr):
            tmpRoot.setChild(newNode, 0)
        else:
            newTmpRoot = dt(counter)
            tmpRoot.setChild(newTmpRoot, 0)
            tmpRoot = newTmpRoot
            tmpRoot.setChild(newNode, 2)
            counter += 1
            newNode.setValue(counter)
        
        # agrega el operando y sus nodos necesarios
        if i[len(i) - 1] in ("*", "+", "?"):
            counter += 1
            operant = i[len(i) - 1]
            tmp_newNode = dt(counter)
            newNode.setChild(dt(operant, True), 2)
            newNode.setChild(tmp_newNode, 0)
            newNode = tmp_newNode
            i = i[:len(i) - 1]

            if i[0] != "(":
                newNode.setIsComponent(True)
        
        # caso de parentesis (usa recursion)
        if i[0] == "(":
            newNode.setChild(dt("(", True), 0)
            newNode.setChild(dt(")", True), 2)

            counter += 1
            parth_expr = regexToExpr(i[1:len(i)-1])
            parth_root = exprToDecompTreeNFA(parth_expr, counter)
            newNode.setChild(parth_root, 1)
        
        # caso de letras
        else:
            newChildrenNode = dt(i, True)
            newNode.setChild(newChildrenNode, 1)
            newNode.setIsComponent(True)

    return root

# indexSetter(<Decomposition Node for DFA>, int, boolean)
# Pone los indices a los componentes
def indexSetter(root, index = 1, initial = True):
    
    # pone indices a los componentes
    children = root.getChild()
    for i in children:
        if i == None:
            continue
        else:
            index = indexSetter(i, index, False)

    # en caso que no es recursion
    if initial:
        return root

    # salida de recursion
    if root.getIsComponent() and root.getValue != "ε":
        root.setComponentIndex(index)
        index += 1

    return index

# exprToDecompTree(Array, int)
# Pasa cada expresion a un arbol donde se separa segun elementos y operadores, todo
# bajo un orden logico para armar DFAs luego
# Regresa el root de un arbol con los elementos
def exprToDecompTreeDFA(expr, reps = 0):
    miniTrees = []
    
    # quitar + y ? por sus representaciones en * y |
    newExpr = []
    for i in expr:
        last = len(i)-1
        if i[last] == "+":
            newExpr.append(i[0:last])
            newExpr.append(i[0:last] + "*")
        elif i[last] == "?":
            newExpr.append("(" + i[0:last] + "|ε)")
        else:
            newExpr.append(i)

    # regresar a utilizar la variable expr envez de newExpr
    expr = newExpr

    # se hacen los nodos para el arbol
    for i in expr:
        expresion = i[::-1]
        tmpRoot = dfadt(None)
        rootIsSet = False
        counter = 0

        for j in expresion:
            if j in ("*","?","+", "|"):
                tmpRoot.setValue(j)
                rootIsSet = True
            elif j == ")":
                last = len(expresion) - 1
                toExpr = expresion[counter + 1:last]
                tmpExpr = regexToExpr(toExpr[::-1])
                newNode = exprToDecompTreeDFA(tmpExpr, reps + 1)
                if rootIsSet:
                    tmpRoot.setChild(newNode, 1)
                else:
                    tmpRoot = newNode
                break
            else:
                if rootIsSet:
                    tmpRoot.setChild(dfadt(j, True), 1)
                else:
                    tmpRoot.setValue(j)
                    tmpRoot.setIsComponent(True)

            counter += 1

        miniTrees.append(tmpRoot)

    # se lee los nodos y se acomoda para el caso de OR
    newMiniTrees = []
    skips = 0
    for i in range(len(miniTrees)):
        if skips > 0:
            skips -= 1
        elif miniTrees[i].getValue() == "|":
            miniTrees[i].setChild(miniTrees[i-1], 0)
            miniTrees[i].setChild(miniTrees[i+1], 1)
            skips += 1
            newMiniTrees.pop(i-1)
            newMiniTrees.append(miniTrees[i])
        else:
            newMiniTrees.append(miniTrees[i])

    # se regresa a utilizar miniTrees envez de newMiniTrees
    miniTrees = newMiniTrees

    # se empieza el nuevo arbol
    root = dfadt(".")
    root.setChild(dfadt("#", True), 1)
    tmpRoot = root
    miniTrees = miniTrees[::-1]
    for i in range(len(miniTrees)):
        
        if i == len(miniTrees) - 1:
            tmpRoot.setChild(miniTrees[i], 0)
        else:
            newRoot = dfadt(".")
            tmpRoot.setChild(newRoot, 0)
            tmpRoot = newRoot

            tmpRoot.setChild(miniTrees[i], 1)
    
    # caso si se llamo en recursion
    if reps != 0:
        return root.getChild()[0]

    # pone los indices a los componentes
    root = indexSetter(root)

    return root

# rootToLeaf(<Decomposition node>)
# Encuentra el hijo menor a la izquierda dado un root
# Devuelve la utilima hoja con hijos componentes
def rootToLeaf(root):

    leaf = root
    
    for i in leaf.getChild():
        if i is None:
            continue
        if not i.getIsComponent():
            leaf = rootToLeaf(i)
            break

    return leaf

# leafToNFA(<Decomposition node>, <NFA node>[], int, boolean)
# Hace las operaciones segun el algoritmo de thompson para la formacion de un NFA
# Devuelve todos los nodos de tipo <NFA node> en el orden del NFA 
def leafToNFA(leaf, nodes = [], cnt = 0, first = True):
    counter = cnt
    nodes = nodes
    operants = []
    components = []
    hAndT = []

    # se revisa los hijos para hacer las operaciones
    for i in leaf.getChild():
        if i is None:
            continue

        # caso de operandos
        if i.getValue() in ("*", "+", "?", "|", "(", ")"):
            operants.append(i.getValue())
        
        # caso de nodos en NFA
        elif i.getDone():
            components.append(i.getHeadsAndTails())
            hAndT = i.getHeadsAndTails()
        
        # casos de componentes a aplicar Thompson
        elif i.getIsComponent():
            trans = i.getChild()[1]
            counter += 2
            new_node1 = nt("T" + str(counter - 1))
            new_node2 = nt("T" + str(counter))
            new_node1.setTransition(new_node2, trans.getValue())
            components.append((new_node1, new_node2))
            nodes.append(new_node1)
            nodes.append(new_node2)
            hAndT = (new_node1, new_node2)
        
        # caso de que una rama sea mas profunda (aplica recursion)
        else:
            tmp_leaf = rootToLeaf(i)
            tmp_nodes = leafToNFA(tmp_leaf, [], counter, False)
            nodes += tmp_nodes
            hAndT = (tmp_nodes[0], tmp_nodes[len(tmp_nodes) - 1])
            counter += len(tmp_nodes) + 2

    # aplica las reglas de thompson segun los operandos
    for operant in operants:
        # OR
        if operant == "|" and len(components) == 2:
            counter += 2
            new_node1 = nt("T" + str(counter - 1))
            new_node2 = nt("T" + str(counter))
            for i in components:
                new_node1.setTransition(i[0], "ε")
                i[::-1][0].setTransition(new_node2, "ε")
            nodes.insert(0, new_node1)
            nodes.append(new_node2)
            hAndT = [new_node1, new_node2]
        # Kleen and other
        elif operant in ("*", "+", "?"):
            counter += 2
            new_node1 = nt("T" + str(counter - 1))
            new_node2 = nt("T" + str(counter))
            component = components[0]
            new_node1.setTransition(component[0], "ε")
            if operant in ("*", "?"):
                new_node1.setTransition(new_node2, "ε")
            if operant in ("*", "+"):
                component[1].setTransition(component[0], "ε")
            component[1].setTransition(new_node2, "ε")
            nodes.insert(0, new_node1)
            nodes.append(new_node2)
            hAndT = [new_node1, new_node2]

    # junta de dos 
    if len(operants) == 0 and len(components) == 2:
        for i in components[1][0].getTransition():
            components[0][1].setTransition(i[0], i[1])
        while components[1][0] in nodes:
            nodes.remove(components[1][0])
        hAndT = [components[0][0], components[1][1]]

    # caso que ya no habra padre
    if leaf.getParent() is None:
        leaf.setDone()
        leaf.setChild(None, 0)
        leaf.setChild(None, 1)
        leaf.setChild(None, 2)
        return nodes

    # limpieza del arbol de descomposicion
    leaf.setDone()
    leaf.setStates(nodes)
    leaf.setChild(None, 0)
    leaf.setChild(None, 1)
    leaf.setChild(None, 2)

    # shhhhhh
    try:
        leaf.setHeadsAndTails(hAndT[0], hAndT[1])
    except:
        pass
    
    # recursion para acceder al padre
    nodes = leafToNFA(leaf.getParent(), nodes, counter, False)

    # renombrar la lista solo una vez
    if first:
        nodes = list(dict.fromkeys(nodes))

        # nodes en transiciones
        list_tmp = []
        for i in nodes:
            for j in i.getTransition():
                list_tmp.append(j[0])
        
        list_tmp = list(dict.fromkeys(list_tmp))

        # nodes
        nodes_tmp = []
        last_ones = []
        for i in nodes:
            if i not in list_tmp:
                nodes_tmp.insert(0, i)
            elif i.getTransition() == []:
                i.setIsAcceptanceState()
                last_ones.append(i)
            else:
                nodes_tmp.append(i)

        nodes_tmp += last_ones
        nodes = nodes_tmp

        counter = 0
        for i in nodes:
            i.setState("T" + str(counter))
            counter += 1

    return nodes

# rootToNFA(<Decomposition node>)
# Aplica rootToLeaf y luego leafToNFA con un solo metodo
# Devuelve todos los nodos de tipo <NFA node> en el orden del NFA 
def rootToNFA(root):
    leaf = rootToLeaf(root)
    return leafToNFA(leaf)

# eclosure(int[], <NFA node>[])
# Aplica eclosure segun el array de indices dados
def eclosure(nodes_pos, nodes):
    
    closure = nodes_pos

    for node_pos in nodes_pos:
        init_node = nodes[node_pos]
        for i in init_node.getTransition():
            if i[1] == "ε":
                closure.append(int(i[0].getState()[1]))
                closure += eclosure([nodes.index(i[0])], nodes)

    closure = list(dict.fromkeys(closure))
    return closure

# move(int[], char,  <NFA node>[])
# Aplica move segun el array de indices dados
def move(s, c, nodes):
    movers = []

    for i in s:
        init_node = nodes[i]
        for i in init_node.getTransition():
            if i[1] == c:
                movers.append(int(i[0].getState()[1:]))
                # movers += move([nodes.index(i[0])], c, nodes)

    movers = list(dict.fromkeys(movers))
    return movers

# fromNFAtoDFA(<NFA nodes>[], string[])
# Usando el algoritmo de subset construction se convierte un NFA a un DFA
# luego con los states y transitions se convierte a un DFA tree
def fromNFAtoDFA(nodes, alphabet):

    # SUBSET CONSTRUCTION
    dStates = [eclosure([0],nodes)]
    dStatesMarkers = [False]
    dTrans = []

    while (False in dStatesMarkers):

        # mark T and get index
        state = 0
        for i in range(len(dStatesMarkers)):
            if dStatesMarkers[i] == False:
                state = i
                dStatesMarkers[i] = True
                break

        t = dStates[state]
        
        # for each input i
        for i in alphabet:
            u = eclosure(move(t, i, nodes), nodes)
            u.sort()
            if u not in dStates:
                dStates.append(u)
                dStatesMarkers.append(False)
            dTrans.append((state, dStates.index(u), i))
    
    # FROM STATES AND TRANSITIONS TO DFA TREE
    nodes_dfa = []
    counter = 0
    for i in dStates:
        node_tmp = dfat("T" + str(counter))
        for j in i:
            if nodes[j].getIsAcceptanceState():
                node_tmp.setIsAcceptanceState()
        nodes_dfa.append(node_tmp)
        counter += 1
    
    for i in dTrans:
        who = i[0]
        to = i[1]
        by = i[2]

        nodes_dfa[who].setTransition(nodes[to],by)
    
    return nodes_dfa


# simulateNFA("string", <NFA node>[])
# se simula la corrida de un NFA por medio de un loop, eclosure y move
# se devuelve NO o SI si la palabra pertenece al lenguaje descrito por el NFA
def simulateNFA(word, nodes):
    ret = "NO"
    s = eclosure([0],nodes)

    for c in word:
        s = eclosure(move(s, c, nodes), nodes)
    
    for i in s:
        if nodes[i].getIsAcceptanceState():
            ret = "SI"

    return ret

# simulateNFA("string", <DFA node>[])
# se simula la corrida de un DFA por medio de un loop, eclosure y move
# se devuelve NO o SI si la palabra pertenece al lenguaje descrito por el NFA
def simulateDFA(word, nodes):
    ret = "NO"
    s = [0]

    for c in word:
        s = move(s, c, nodes)
    
    for i in s:
        if nodes[i].getIsAcceptanceState():
            ret = "SI"

    return ret
    


        