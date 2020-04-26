import copy
try:
    from nodes import DecompositionTreeDFA as dfadt
    from nodes import DFATree as dfat
except:
    from Lexer.nodes import DecompositionTreeDFA as dfadt
    from Lexer.nodes import DFATree as dfat

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
        elif regex[i] in ("*", "?"):
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
        if i not in ("(", ")", "*", "?", "|", "ε"):
            alphabet.append(i)

    alphabet = list(dict.fromkeys(alphabet))
    
    return alphabet

# exprToAlphabet(array)
# Devuelve un array con solo los componentes en el abecedario utilizado por el lenguaje
# descrito por el regex
def exprToAlphabet(expr):
    alphabet = []

    for i in expr:
        for j in i:
            if j not in ("(", ")", "*", "?", "|", "ε", "@"):
                alphabet.append(j)

    alphabet = list(dict.fromkeys(alphabet))
    
    return alphabet

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
        if i[last] == "?":
            newExpr.append("(" + i[:last] + "|ε)")
        else:
            newExpr.append(i)

    # regresar a utilizar la variable expr envez de newExpr
    expr = newExpr

    # se hacen los nodos para el arbol
    for i in expr:

        # creacion del resto de nodos
        expresion = i[::-1]
        tmpRoot = dfadt(None)
        rootIsSet = False
        counter = 0

        for j in expresion:
            if j in ("*", "|"):
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
                miniTrees[i].setChild(newMiniTrees[0], 0)
                miniTrees[i].setChild(miniTrees[i+1], 1)
                skips += 1
                newMiniTrees.pop(len(newMiniTrees) - 1)
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

# move(int[], char,  <DFA node>[])
# Aplica move segun el array de indices dados
def move(s, c, nodes):
    movers = []

    for i in s:
        init_node = nodes[i]
        for i in init_node.getTransition():
            if i[1] == c:
                movers.append(int(i[0].getState()[1:]))

    movers = list(dict.fromkeys(movers))
    return movers

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

# set the tag of the states
def setTags(nodes, tag):
    for i in nodes:
        i.setTag(tag)

# set the priority to acceptance states
def setPriorities(nodes, priority):
    for i in nodes:
        if i.getIsAcceptanceState():
            i.setPriority(priority)

def removeUseless(nodes):

    new_nodes = []

    for i in nodes:
        
        if i.getIsAcceptanceState():
            new_nodes.append(i)
            continue
        
        add = False
        transitions = i.getTransition()
        for j in transitions:
            if j[0] != i:
                add = True

        if add:
            new_nodes.append(i)
    
    for i in new_nodes:
        transitions = i.getTransition()
        new_transitions= []

        for j in transitions:
            if j[0] not in new_nodes:
                continue
            else:
                new_transitions.append(j)
        
        i.setAllTransitions(new_transitions)

    counter = 0
    for i in new_nodes:
        i.setState("T" + str(counter))
        counter += 1

    return new_nodes

        
def regexToDFA(regex, tag, priority):
    # Paso 1: Leer regex
    expr = regexToExpr(regex)
    alphabet = exprToAlphabet(expr)

    # Paso 2: Descomponer la expresion en arboles
    rootDFA = exprToDecompTreeDFA(expr)

    # Paso 3: DFA
    nodes_dfa = rootToDFA(rootDFA, alphabet)
    nodes_dfa = removeUseless(nodes_dfa)
    setTags(nodes_dfa, tag)
    setPriorities(nodes_dfa, priority)

    return nodes_dfa

# simulateNFA("string", <DFA node>[])
# se simula la corrida de un DFA por medio de un loop, eclosure y move
# se devuelve NO o SI si la palabra pertenece al lenguaje descrito por el NFA
def simulateDFA(word, nodes):
    s = [0]

    for c in word:
        s = move(s, c, nodes)

    # caso que no pertenesca
    if s == [] or s == [0]:
        return "not_a_token"
    
    # estados de aceptacion 
    acceptanceStates = []
    for i in s:
        if nodes[i].getIsAcceptanceState():
            acceptanceStates.append(nodes[i])

    # sorteo por prioridad
    if len(acceptanceStates) == 1:
        return acceptanceStates[0].getTag()

    elif len(acceptanceStates) > 1:

        singleState = None
        priority = 99999
        for i in acceptanceStates:
            if i.getPriority() < priority:
                singleState = i
                priority = i.getPriority()

        return singleState.getTag()

    # default return
    return "keep_going"