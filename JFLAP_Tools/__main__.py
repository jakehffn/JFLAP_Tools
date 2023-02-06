from REToJFLAPFA import REToJFLAPFA
from automaton import Automaton

import argparse

def createParser()->argparse.ArgumentParser:


    parser = argparse.ArgumentParser(
        prog='REToJFLAPFA',
        description='Convert a regular expression to a JFLAP Finite Automaton')
    
    parser.add_argument('regex')
    parser.add_argument('-o', '--outfile')

    return parser

if __name__ == '__main__':

    parser = createParser()

    args = parser.parse_args()

    automaton = REToJFLAPFA(args.regex)
    xml = automaton.toXML()

    if args.outfile == None:
        print(xml)
    else:
        with open(args.outfile, 'w') as f:
            f.write(xml)

