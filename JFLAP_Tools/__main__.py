from REToJFLAPFA import REToJFLAPFA
from automaton import Automaton

import argparse

def createParser()->argparse.ArgumentParser:


    parser = argparse.ArgumentParser(
        prog='REToJFLAPFA',
        description="""Convert a regular expression to a JFLAP Finite Automaton.
        
Sets are designated using square brackets, such as '[abcd]' to represent the transition containing each 'a', 'b', 'c', and 'd'.
Sets can also contain a range of values from 'a' to '9' by using a '-'. 
    Ex. "[a-d]" for 'a', 'b', 'c', 'd' or "[a-cZ-1]" for 'a', 'b', 'c', 'Z', '0', '1'

Parenthesis can be used to designate a group for repeating.
    Ex. "(abc)*" represents '', 'abc', 'abcabc', ...

Pipe is used to represent an OR operation (lambda transition).
    Ex. "a*|[bc]" represent 'a', 'aa', 'aaa', ... , 'b', or 'c'

Nested repeaters, such as "(ab*cd)*", are not currently supported.""",
        epilog='Not providing an outfile will output to terminal',
        formatter_class=argparse.RawTextHelpFormatter)
    
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

