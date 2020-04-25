class DecompositionTreeDFA():

    def __init__(self, value, isComponent = False, componetIndex = None):
        self.value = value
        self.parent = None
        self.children = [None, None]
        self.isComponent = isComponent
        self.componetIndex = componetIndex
        self.isNullable = None
        self.firstpos = []
        self.lastpos = []
        self.followpos = []
    
    def setValue(self, value):
        self.value = value
    
    def getValue(self):
        return self.value
    
    def setParent(self, parent, setAgain = True):
        if type(parent) == type(self) and setAgain:
            parent.setChild(self, 0, False)

        self.parent = parent
    
    def getParent(self):
        return self.parent

    def setChild(self, child, pos = 0, setAgain = True):
        if type(child) == type(self) and setAgain:
            child.setParent(self, False)

        self.children[pos] = child
    
    def getChild(self):
        return self.children
    
    def setIsComponent(self, isComponent = True):
        self.isComponent = isComponent
    
    def getIsComponent(self):
        return self.isComponent

    def setComponentIndex(self, index = 0):
        self.componetIndex = index

    def getComponentIndex(self):
        return self.componetIndex

    def setIsNullable(self, value = True):
        self.isNullable = value

    def getIsNullable(self):
        return self.isNullable

    def setFirstpos(self, pos):
        self.firstpos = pos

    def getFirstpos(self):
        return self.firstpos

    def setLastpos(self, pos):
        self.lastpos = pos

    def getLastpos(self):
        return self.lastpos

    def setFollowpos(self, pos):
        self.followpos = pos

    def getFollowpos(self):
        return self.followpos

    def getLastposTree(self, level=0):
        ret = "-- "*level + self.value + " " + repr(self.lastpos)+"\n"
        for child in self.children:
            if type(child) == type(self):
                ret += child.getLastposTree(level + 1)
        return ret

    def getFirstposTree(self, level=0):
        ret = "-- "*level + self.value + " " + repr(self.firstpos)+"\n"
        for child in self.children:
            if type(child) == type(self):
                ret += child.getFirstposTree(level + 1)
        return ret

    def getNullableTree(self, level=0):
        ret = "-- "*level + self.value + " " + repr(self.isNullable)+"\n"
        for child in self.children:
            if type(child) == type(self):
                ret += child.getNullableTree(level + 1)
        return ret

    def __str__(self, level=0):
        if self.componetIndex == None:
            ret = "-- "*level+repr(self.value)+"\n"
        else:
            ret = "-- "*level+repr(self.value) + repr(self.componetIndex)+"\n"
        for child in self.children:
            if type(child) == type(self):
                ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        if self.componetIndex == None:
            return '<Decomposition node dfa>'
        else:
            return '<Decomposition node dfa index-' + str(self.componetIndex) + '>'

class DFATree():
    state = None
    transitions = []

    def __init__(self, state = None):
        self.state = state
        self.transitions = []
        self.isAcceptanceState = False
        self.tag = ""
        self.priority = 3
    
    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state
    
    def setTransition(self, to, by):
        self.transitions.append((to,by))

    def setAllTransitions(self, transitions):
        self.transitions = transitions
    
    def getTransition(self):
        return self.transitions

    def setIsAcceptanceState(self, value = True):
        self.isAcceptanceState = value
    
    def getIsAcceptanceState(self):
        return self.isAcceptanceState
    
    def setTag(self, tag):
        self.tag = tag
    
    def getTag(self):
        return self.tag

    def setPriority(self, priority):
        self.priority = priority
    
    def getPriority(self):
        return self.priority

    def __repr__(self):
        return '<DFA node> ' + str(self.state)

    
