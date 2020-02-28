class DecompositionTree():

    def __init__(self, value, isComponent = False):
        self.value = value
        self.parent = None
        self.children = [None, None, None]
        self.isComponent = isComponent
        self.done = False
        self.headAndTail = [None, None]
        self.states = []
    
    def setValue(self, value):
        self.value = value
    
    def getValue(self):
        return self.value
    
    def setParent(self, parent, setAgain = True):
        if type(parent) == type(self) and setAgain:
            parent.setChild(self, 1, False)

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
    
    def setDone(self, value = True):
        self.done = value

    def getDone(self):
        return self.done
    
    def setHeadsAndTails(self, head, tail):
        self.headAndTail = [head, tail]
    
    def getHeadsAndTails(self):
        return self.headAndTail
    
    def setStates(self, states):
        self.states = states

    def getStates(self):
        return self.states

    def __str__(self, level=0):
        ret = "-- "*level+repr(self.value)+"\n"
        for child in self.children:
            if type(child) == type(self):
                ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<Decomposition node>'


class NFATree():
    state = None
    transitions = []

    def __init__(self, state = None):
        self.state = state
        self.transitions = []
        self.isAcceptanceState = False
    
    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state
    
    def setTransition(self, to, by):
        self.transitions.append((to,by))
    
    def getTransition(self):
        return self.transitions

    def setIsAcceptanceState(self, value = True):
        self.isAcceptanceState = value
    
    def getIsAcceptanceState(self):
        return self.isAcceptanceState

    def __repr__(self):
        return '<NFA node> ' + str(self.state)

    
