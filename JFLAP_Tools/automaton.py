import xml.etree.ElementTree as et
import random

class Automaton:

    def __init__(self):

        self._transitions = [] #('set', from, to)
        self._recognized = [] # nodes that are recognized as final states
        self._rowStartNodes = []

        self._numStates = 0
        self._nextToState = 0 # The next state that should be pointed to

        self._matchManyFrom = -1

    def addTransition(self, matchingSet: str):

        if len(self._transitions) > 0:

            self._transitions += [(matchingSet, self._numStates, self._nextToState)]
            self._nextToState = self._numStates

            self._numStates += 1

        else:

            self._recognized += [0]
            self._transitions += [(matchingSet, 1, 0)]
            self._nextToState = 1
            self._numStates += 2

    def addLambdaTransition(self):

        self._rowStartNodes += [self._nextToState]

        self._nextToState = self._numStates
        self._numStates += 1

        self._recognized += [self._nextToState]

    def startMatchMany(self):
        self._matchManyFrom = self._nextToState

    def endMatchMany(self):

        lastTransition = self._transitions[-1]
        self._transitions[-1] = (lastTransition[0], self._matchManyFrom, lastTransition[2])

        self._nextToState = self._matchManyFrom
        self._numStates -= 1

    def finish(self):

        self._rowStartNodes += [self._numStates-1]

        newTransitions = []

        # Expand the sets into many transitions
        for set, fromState, toState in self._transitions: 

            for c in set:
                newTransitions += [(c, fromState, toState)]

        # Lambda transitions are not needed at all if there is only one recognized state
        if not len(self._recognized) == 1:

            for state in self._recognized:
                newTransitions += [('', state, self._numStates)]

            self._recognized = [self._numStates]
            self._numStates += 1

            for state in self._rowStartNodes:
                newTransitions += [('', self._numStates, state)]

            self._start = self._numStates
            self._numStates += 1

        else:
            self._start = self._numStates - 1

        self._transitions = newTransitions

    def toXML(self)->str:

        root = et.Element('structure')
        et.SubElement(root, 'type').text = 'fa'
        automaton = et.SubElement(root, 'automaton')

        for x in range(self._numStates):

            currId = self._numStates - x - 1 # Make the first state be 0

            state = et.SubElement(automaton, 'state', {'id': str(currId), 'name':f'q{x}'})
            et.SubElement(state, 'x').text = '50'
            et.SubElement(state, 'y').text = '50'

            if currId == self._start:
                et.SubElement(state, 'initial')

            if currId in self._recognized:
                et.SubElement(state, 'final')
        
        for character, fromNode, toNode in self._transitions:
            
            transition = et.SubElement(automaton, 'transition')
            et.SubElement(transition, 'from').text = str(fromNode)
            et.SubElement(transition, 'to').text = str(toNode)
            et.SubElement(transition, 'read').text = str(character)

        et.indent(root)

        return et.tostring(root, encoding='unicode', xml_declaration=True)