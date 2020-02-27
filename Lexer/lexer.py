from nodes import DecompositionTree as dt
from nodes import NFATree as nt

def regexToExpr(regex):
    expresions = []
    skips = 0

    for i in range(len(regex)):
        if skips > 0:
            skips -= 1
        elif regex[i] in ("*", "+", "?"):
            expresions[len(expresions) - 1] += regex[i]
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
        else:
            expresions.append(regex[i])
        
    return expresions

def exprToDecompTree(expr, cnt = 0):
    expr = expr[::-1]
    root = dt(cnt)
    tmpRoot = root
    counter = cnt
    repetitions = 0

    for i in expr:
        repetitions += 1

        # Caso especial del OR
        if i == "|":
            tmpRoot.setChild(dt("|", True), 1)
            continue

        # Pone el siguiente nodo en la posicion deseada
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
        
        # Agrega el operando y sus nodos necesarios
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
        
        # Caso de parentesis (usa recursion)
        if i[0] == "(":
            newNode.setChild(dt("(", True), 0)
            newNode.setChild(dt(")", True), 2)

            counter += 1
            parth_expr = regexToExpr(i[1:len(i)-1])
            parth_root = exprToDecompTree(parth_expr, counter)
            newNode.setChild(parth_root, 1)
        
        # Caso de letras
        else:
            newChildrenNode = dt(i, True)
            newNode.setChild(newChildrenNode, 1)
            newNode.setIsComponent(True)

    return root

def rootToLeaf(root):

    leaf = root
    
    for i in leaf.getChild():
        if i is None:
            continue
        if not i.getIsComponent():
            leaf = rootToLeaf(i)
            break

    return leaf

def leafToNFA(leaf, nodes = [], cnt = 0, first = True):
    counter = cnt
    nodes = nodes
    operants = []
    components = []
    hAndT = []

    for i in leaf.getChild():
        if i is None:
            continue

        if i.getValue() in ("*", "+", "?", "|", "(", ")"):
            operants.append(i.getValue())
        elif i.getDone():
            components.append(i.getHeadsAndTails())
            hAndT = i.getHeadsAndTails()
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
        else:
            tmp_leaf = rootToLeaf(i)
            tmp_nodes = leafToNFA(tmp_leaf, [], counter, False)
            nodes += tmp_nodes
            hAndT = (tmp_nodes[0], tmp_nodes[len(tmp_nodes) - 1])
            counter += len(tmp_nodes)

    for operant in operants:
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

    
    if len(operants) == 0 and len(components) == 2:
        for i in components[1][0].getTransition():
            components[0][1].setTransition(i[0], i[1])
        while components[1][0] in nodes:
            nodes.remove(components[1][0])
        hAndT = [components[0][0], components[1][1]]

    if leaf.getParent() is None:
        leaf.setDone()
        leaf.setChild(None, 0)
        leaf.setChild(None, 1)
        leaf.setChild(None, 2)
        return nodes

    leaf.setDone()
    leaf.setStates(nodes)
    leaf.setChild(None, 0)
    leaf.setChild(None, 1)
    leaf.setChild(None, 2)

    try:
        leaf.setHeadsAndTails(hAndT[0], hAndT[1])
    except:
        pass

    nodes = leafToNFA(leaf.getParent(), nodes, counter, False)

    if first:
        nodes = list(dict.fromkeys(nodes))
        counter = 0
        for i in nodes:
            i.setState("T" + str(counter))
            counter += 1

    return nodes

def rootToNFA(root):
    leaf = rootToLeaf(root)
    return leafToNFA(leaf)