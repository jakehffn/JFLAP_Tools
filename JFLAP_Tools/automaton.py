import xml.etree.ElementTree as et
import random

class Automaton:

    def __init__(self):

        self._transitions = []
        self._recognized = [0]
        self._lambdaTos = []

        self._numStates = 1
        self._preferedHead = -1

        self._matchManyFrom = 0
        self._lastSet = None
        self._skipNode = False

        self._start = None

    def addTransition(self, matchingSet: str|None):

        if not self._lastSet is None:

            for c in self._lastSet:

                if not self._preferedHead == -1:
                    self._transitions += [(c, self._numStates, self._preferedHead)]

                    self._preferedHead = -1
                else:
                    self._transitions += [(c, self._numStates, self._numStates-1)]
                
            if self._skipNode:

                self._numStates += 2
                self._skipNode = False

            else:
                self._numStates += 1

        self._lastSet = matchingSet

    def addLambdaTransition(self):

        self._lambdaTos += [self._numStates]

        self._skipNode = True # Causes new 'path' to be made
        self._recognized += [self._numStates+1]


    def startMatchMany(self):
        self.addTransition(None)
        self._matchManyFrom = self._numStates - 1

    def endMatchMany(self):

        for c in self._lastSet:
            self._transitions += [(c, self._matchManyFrom, self._numStates - 1)] # self._matchManyStart holds the start of the transition

        self._preferedHead = self._matchManyFrom 

        self._lastSet = None

    def cleanup(self):

        self.addTransition(None)        
        self._start = self._numStates -1 if self._preferedHead == -1 else self._preferedHead

        if len(self._lambdaTos) > 0:

            self._lambdaTos += [self._numStates - 1]

            self._start = self._numStates

            self._numStates += 1

        for lambdaTo in self._lambdaTos:
            self._transitions += [('', self._numStates - 1, lambdaTo)]


    def toXML(self)->str:

        root = et.Element('structure')
        et.SubElement(root, 'type').text = 'fa'
        automaton = et.SubElement(root, 'automaton')

        for x in range(self._numStates):

            currId = self._numStates - x - 1 # I want it to read logically left to right

            xPos = random.randint(10,500)
            yPos = random.randint(10,500)

            state = et.SubElement(automaton, 'state', {'id': str(currId), 'name':f'q{x}'})
            et.SubElement(state, 'x').text = str(xPos)
            et.SubElement(state, 'y').text = str(yPos)    

            if currId == self._start:
                et.SubElement(state, 'initial')

            if currId in self._recognized:
                et.SubElement(state, 'final')
        
        for character, fromNode, toNode in self._transitions:

            transition = et.SubElement(automaton, 'transition')
            et.SubElement(transition, 'from').text = str(fromNode)
            et.SubElement(transition, 'to').text = str(toNode)
            et.SubElement(transition, 'read').text = str(character)

        # tree = et.ElementTree(root)
        et.indent(root)

        return et.tostring(root, encoding='unicode', xml_declaration=True)