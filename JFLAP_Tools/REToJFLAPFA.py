# Tool for generating finite automata for JFLAP

from automaton import Automaton


selectionString = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def REToJFLAPFA(regex: str)->Automaton:

    automaton = Automaton()

    i = len(regex) - 1
    matchManyParenthesisLevel = -1
    parenthesisLevel = 0

    while(i >= 0):

        currSet = ''

        c = regex[i]

        if c == '|':
            automaton.addLambdaTransition()

        elif c == ')':
            parenthesisLevel += 1

        elif c == '(':
            parenthesisLevel -= 1

        elif c == '*':

            matchManyParenthesisLevel = parenthesisLevel
            automaton.startMatchMany()

            i -= 1

            if i < 0:

                raise Exception('Bad *')
            
            continue

        elif c == '[':

            raise Exception('Malformed Set: "[" without matching "]"')

        elif c == ']':

            i -= 1
            c = regex[i]

            while not c == "[":

                if i == 0:
                    raise Exception('Malformed Set: "]" without matching "["')
                
                currSet += c

                i -= 1
                c = regex[i]

            while  ('-' in currSet):

                selection = currSet.index('-')

                startIndex = selection - 1
                endIndex = selection + 1

                if startIndex < 0 or endIndex == len(currSet):
                    raise Exception('Malformed set: "-" has missing bounds')

                start = currSet[startIndex]
                end = currSet[endIndex]
                
                if not start in selectionString:
                    raise Exception(f'Malformed set: "{start}" not valid selector')
                
                if not end in selectionString:
                    raise Exception(f'Malformed set: "{end}" not valid selector')
                
                lowIndex = selectionString.index(start)
                highIndex = selectionString.index(end)

                lowIndex, highIndex = (highIndex, lowIndex) if lowIndex > highIndex else (lowIndex, highIndex)
                
                currSet = currSet[:startIndex] + selectionString[lowIndex:highIndex+1] + currSet[endIndex + 1:]

        else:
            currSet = c

        if currSet != '':
            automaton.addTransition(currSet)

        if matchManyParenthesisLevel == parenthesisLevel:
            automaton.endMatchMany()
            matchManyParenthesisLevel = -1

        i -= 1

    automaton.finish()

    return automaton