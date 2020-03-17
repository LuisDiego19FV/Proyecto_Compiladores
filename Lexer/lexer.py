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
        if i not in ("(", ")", "*", "+", "?", "|", "ε"):
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
    if root.getIsComponent() and root.getValue() != "ε":
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
                    tmpRoot.setChild(newNode, 0)
                else:
                    tmpRoot = newNode
                break
            else:
                if rootIsSet:
                    tmpRoot.setChild(dfadt(j, True), 0)
                else:
                    tmpRoot.setValue(j)
                    tmpRoot.setIsComponent(True)

            counter += 1

        miniTrees.append(tmpRoot)

    # se lee los nodos y se acomoda para el caso de OR
    if "|" in expr:
        newMiniTrees = []
        skips = 0
        for i in range(len(miniTrees)):
            if skips > 0:
                skips -= 1
            elif miniTrees[i].getValue() == "|" and len(miniTrees) >= 3 and i % 2 == 1:
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
def eclosure(nodes_pos, nodes, closure_recursive = []):
    
    closure = nodes_pos

    if closure_recursive == []:
        closure_recursive = nodes_pos

    for node_pos in nodes_pos:
        init_node = nodes[node_pos]
        for i in init_node.getTransition():
            if i[1] == "ε":
                state = int(i[0].getState()[1:])
                if state not in closure_recursive:
                    closure.append(state)
                    closure_recursive.append(state)
                    closure += eclosure([nodes.index(i[0])], nodes, closure_recursive)

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

        nodes_dfa[who].setTransition(nodes_dfa[to],by)
    
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

# nullableTree(<Decomposition node dfa>, Bool, Bool)
# se calcula el nullable para cada hoja del arbol
def nullableTree(root, first = True, stopOn = None):

    # first cases
    if first:
        leaf = rootToLeaf(root)
    else:
        leaf = root

    # components
    children = leaf.getChild()
    for i in children:
        if i == None:
            continue 
        elif i.getIsComponent():
            if i.getValue() == "ε":
                i.setIsNullable(True)
            else:
                i.setIsNullable(False)
        elif i.getIsNullable() != None:
            continue
        else:
            leaf = rootToLeaf(i)
            nullableTree(leaf, False, i)

    # operators
    if leaf.getValue() == "|":
        valToSet = children[0].getIsNullable() or children[1].getIsNullable()
        leaf.setIsNullable(valToSet)
    elif leaf.getValue() == ".":
        valToSet = children[0].getIsNullable() and children[1].getIsNullable()
        leaf.setIsNullable(valToSet)
    else:
        leaf.setIsNullable(True)

    # recursion
    parent = leaf.getParent()

    # return condition
    if leaf == stopOn or parent == None:
        return 0
    else:
        nullableTree(parent, False)

# firstposTree(<Decomposition node dfa>, Bool, Bool)
# se calcula el firstpos para cada hoja del arbol
def firstposTree(root, first = True, stopOn = None):

    # first cases
    if first:
        leaf = rootToLeaf(root)
    else:
        leaf = root

    # components
    children = leaf.getChild()
    for i in children:
        if i == None:
            continue 
        elif i.getIsComponent():
            if i.getValue() == "ε":
                i.setFirstpos([])
            else:
                i.setFirstpos([i.getComponentIndex()])
        elif i.getFirstpos() != []:
            continue
        else:
            tmpLeaf = rootToLeaf(i)
            firstposTree(tmpLeaf, False, i)

    # operants
    if leaf.getValue() == "|":
        valToSet = children[0].getFirstpos() + children[1].getFirstpos()
        leaf.setFirstpos(valToSet)
    elif leaf.getValue() == ".":
        if children[0].getIsNullable():
            valToSet = children[0].getFirstpos() + children[1].getFirstpos()
            leaf.setFirstpos(valToSet)
        else:
            valToSet = children[0].getFirstpos()
            leaf.setFirstpos(valToSet)
    else:
        leaf.setFirstpos(children[0].getFirstpos())

    # recursion
    parent = leaf.getParent()

    # return condition
    if leaf == stopOn or parent == None:
        return 0
    else:
        firstposTree(parent, False)

# lastposTree(<Decomposition node dfa>, Bool, Bool)
# se calcula el lastpos para cada hoja del arbol
def lastposTree(root, first = True, stopOn = None):

    # first cases
    if first:
        leaf = rootToLeaf(root)
    else:
        leaf = root

    # components
    children = leaf.getChild()
    for i in children:
        if i == None:
            continue 
        elif i.getIsComponent():
            if i.getValue() == "ε":
                i.setLastpos([])
            else:
                i.setLastpos([i.getComponentIndex()])
        elif i.getLastpos() != []:
            continue
        else:
            tmpLeaf = rootToLeaf(i)
            lastposTree(tmpLeaf, False, i)

    # operants
    if leaf.getValue() == "|":
        valToSet = children[0].getLastpos() + children[1].getLastpos()
        leaf.setLastpos(valToSet)
    elif leaf.getValue() == ".":
        if children[1].getIsNullable():
            valToSet = children[0].getLastpos() + children[1].getLastpos()
            leaf.setLastpos(valToSet)
        else:
            valToSet = children[1].getLastpos()
            leaf.setLastpos(valToSet)
    else:
        leaf.setLastpos(children[0].getLastpos())

    # recursion
    parent = leaf.getParent()

    # return condition
    if leaf == stopOn or parent == None:
        return 0
    else:
        lastposTree(parent, False)

# nodesOfPos(<Decomposition node dfa>)
# pone indices a cada componente del arbol de decomposicion
def nodesOfPos(root):
    nodes = []

    # pone indices a los componentes
    children = root.getChild()
    for i in children:
        if i == None:
            continue
        else:
            if i.getIsComponent() and i.getValue() != "ε":
                nodes.append(i)
            elif i.getValue() != "ε":
                nodes += nodesOfPos(i)

    return nodes
# notComponentNodes(<Decomposition node dfa>)
# devuelve todos los nodos que no son componentes
def notComponentNodes(root):
    nodes = [root]

    children = root.getChild()
    for i in children:
        if i == None or i.getIsComponent():
            continue
        else:
            nodes += notComponentNodes(i)

    return nodes

# followpos(<Decomposition node dfa>)
# se calcula el followpos para cada hoja del arbol
def followpos(root):

    # get nodespos
    nodesPos = nodesOfPos(root)
    notComponents = notComponentNodes(root)

    # calculate for all operants
    for i in notComponents:
        if i.getValue() == ".":
            children = i.getChild()
            for j in children[0].getLastpos():
                valToSet = nodesPos[j-1].getFollowpos() + children[1].getFirstpos()
                nodesPos[j-1].setFollowpos(valToSet)
        elif i.getValue() == "*":
            for j in i.getLastpos():
                valToSet = nodesPos[j-1].getFollowpos() + i.getFirstpos()
                nodesPos[j-1].setFollowpos(valToSet)

    # for each node
    for i in nodesPos:
        valToSet = i.getFollowpos()
        valToSet.sort()
        i.setFollowpos(valToSet)

# rootToDFA(<Decomposition node dfa>[], [])
# Hace las operaciones segun el algoritmo de conversion directa a DFA.
# Devuelve todos los nodos de tipo <DFA node> en el orden del DFA 
def rootToDFA(root, alphabet):

    # calculos para el arbol
    nullableTree(root)
    firstposTree(root)
    lastposTree(root)
    followpos(root)

    # estados y transiciones
    dStates = [root.getFirstpos()]
    dStatesMarkers = [False]
    dTrans = []

    nodesPos = nodesOfPos(root)

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
            u = []
            for j in t:
                if nodesPos[j-1].getValue() == i:
                    u += nodesPos[j-1].getFollowpos()

            u = list(dict.fromkeys(u))
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
            if j == len(nodesPos):
                node_tmp.setIsAcceptanceState()
        nodes_dfa.append(node_tmp)
        counter += 1
    
    for i in dTrans:
        who = i[0]
        to = i[1]
        by = i[2]

        nodes_dfa[who].setTransition(nodes_dfa[to],by)
    
    return nodes_dfa

