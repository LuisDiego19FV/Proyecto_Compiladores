from nodes import DecompositionTree as dt
from nodes import NFATree as nt

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

# exprToDecompTree(Array, int)
# Pasa cada expresion a un arbol donde se separa segun elementos y operadores, todo
# bajo un orden logico
# Regresa el root de un arbol con los elementos
def exprToDecompTree(expr, cnt = 0):
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
            parth_root = exprToDecompTree(parth_expr, counter)
            newNode.setChild(parth_root, 1)
        
        # caso de letras
        else:
            newChildrenNode = dt(i, True)
            newNode.setChild(newChildrenNode, 1)
            newNode.setIsComponent(True)

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
            counter += len(tmp_nodes)

    # aplica las reglas de thompson segun los operandos
    for operant in operants:
        # OR
        if operant == "|":
            counter += 2
            new_node1 = nt("T" + str(counter - 1))
            new_node2 = nt("T" + str(counter))
            for i in components:
                new_node1.setTransition(i[0], "Ep")
                i[::-1][0].setTransition(new_node2, "Ep")
                nodes.insert(0, new_node1)
                nodes.append(new_node2)
            hAndT = [new_node1, new_node2]
        # Kleen and other
        elif operant in ("*", "+", "?"):
            counter += 2
            new_node1 = nt("T" + str(counter - 1))
            new_node2 = nt("T" + str(counter))
            component = components[0]
            new_node1.setTransition(component[0], "Ep")
            if operant in ("*", "?"):
                new_node1.setTransition(new_node2, "Ep")
            if operant in ("*", "+"):
                component[1].setTransition(component[0], "Ep")
            component[1].setTransition(new_node2, "Ep")
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
        counter = 0
        for i in nodes:
            i.setState("T" + str(counter))
            counter += 1
        nodes[len(nodes)-1].setIsAcceptanceState()

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
            if i[1] == "Ep":
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
                movers += move([nodes.index(i[0])], c, nodes)

    movers = list(dict.fromkeys(movers))
    return movers

# simulateNFA("string", <NFA node>[])
# se simula la corrida de un NFA por medio de un loop, eclosure y move
# se devuelve NO o YES si la palabra pertenece al lenguaje descrito por el NFA
def simulateNFA(word, nodes):
    ret = "NO"
    s = eclosure([0],nodes)

    for c in word:
        s = eclosure(move(s, c, nodes), nodes)
    
    for i in s:
        if nodes[i].getIsAcceptanceState():
            ret = "YES"

    return ret