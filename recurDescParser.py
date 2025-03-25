import re
from functools import *

"""

A LL(1) recursive descent parser for validating simple expressions.

# Part A:
You would need to first write the grammar rules (non-terminals) in EBNF 
according to the token patterns and grammar rules specified in the prompt,
put the rules in a separate PDF file, see prompt. 

# Part B:
You would then write the recursive descent parsing procedures for 
validating expressions according to the rules from Part A. 
(Refer to the recursive descent parsing algorithm in lecture slides)

It implements one parsing procedure for each one of the 
non-terminals (grammar rules), starting from the top of the parse tree, 
then drilling into lower hierachical levels.

The procedures work together to handle all combinations of the grammar 
rules, and they automatically handle the nested compositions of terms 
with multi-level priority brackets. 

----------------------------------------------------------------------------
Usage (Refer to the prompt for more examples - both positive and negative cases)

r = recDecsent('7 - 17')
print(r.validate()) # will print True as '7 - 17' is a valid expression

r = recDecsent('7 - ')
print(r.validate()) # will print False as '7 - ' is an invalid expression

----------------------------------------------------------------------------
Follows are examples of valid expressions based on the expression patterns specified above:
•	7 - 17
•	> 90
•	(1 - 100 and not 50) or > 200
•	(7 - 17) or > 90
•	> 50 or == 20
•	1 - 100 and != 50
•	(5 - 100) and (not 50) or (>= 130 or (2 - 4))

Examples of invalid expressions:
•	>
•	2 - - 4
•	- 7
•	7 -
•	= 6
•	(!= 5) and
•	2 - 4 and >< 300
•	>= 5) nand < 10

"""

class recDescent:

    # IMPORTANT:
    # You MUST NOT change the signatures of 
    # the constructor, lex(self) and validate(self)
    # Otherwise, autograding tests will FAIL

    # constructor to initialize and set class level variables
    def __init__(self, expr = ""):

        # string to be parsed
        self.expr = expr

        # tokens from lexer tokenization of the expression
        self.tokens = []

        # position of current token being examined
        self.position = 0

    # lex - tokenize the expression into a list of tokens
    # the tokens are stored in a list which can be accessed by self.tokens
    # do NOT edit any piece of code in this function

    def lex(self):
        self.tokens = re.findall("[-\(\)]|[!<>=]=|[<>]|\w+|[^ +]\W+", self.expr)
        # transform tokens to lower case, and filter out possible spaces in the tokens
        self.tokens = list(filter((lambda x: len(x)), 
                           list(map((lambda x: x.strip().lower()), self.tokens))))    
    
    # parser - determine if the input expression is valid or not
    def parser(self):
        return self.expression()

    # validate() function will return True if the expression is valid, False otherwise 
    # do NOT change the method signature 

    def validate(self):
        # Using the tokens from lex() tokenization,
        # this validate would first call lex() to tokenize the expression,
        # then call the top level parsing procedure for the outermost rule
        # and go from there
        
        self.lex()
        
        # TODO: call the topmost parsing procedure and go from there
        return self.parser()

    # TODO: Write your parsing procedures corresponding to the grammar rules - follow Figure 5.17
    
    # move position to next token
    def nextToken(self):
        self.position += 1

    # check for an open parentheses, then advance and begin to check again
    # def parenthesis_open(self):
        
    def expression(self):
        if self.tokens[self.position] == '(':
            self.nextToken() # go to next position after open parenthesis
            self.parser() # begin parsing / validating the upcoming term

            if self.position+1 < len(self.tokens): # There is more to do
                # Continue checking additional terms
                if self.parser():
                
                    # upon exiting the additional parsing
                    if self.tokens[self.position] == ')':
                        # There is also no guarantee that the closing parentheses is the end. You may need to check for other tokens trailing the closing parenthesis
                        if self.position+1 < len(self.tokens):
                            self.nextToken()
                            return self.parser() # There is more to do
                        else:
                        # The last token is indeed the final closing parenthesis
                            return True
                elif self.tokens[self.position] == ')':
                    # if closing parenthesis, and not end of token list
                    self.nextToken() # advance
                    return self.parser() # continue parsing
                else:
                    return False
            
            # If you have reached the end of the token list, check for closing parenthesis
            elif self.tokens[self.position] == ')':
                return True
            else:
                return False # otherwise, return False if the end of the token list is reached without detecting a closing parenthesis
        else:
        # then, start evaluating the expression
            return self.evaluate()

    def evaluate(self):
        relops = ["<", ">", "<=", ">=", "==", "!=", "not"]
        logicOps = ["and", "or", "nand"]
        
        # option 1: int - int
        if self.tokens[self.position].isdigit():
            return self.dashTerm()
        
        # option 2: relop int
        elif self.tokens[self.position] in relops:
            return self.relopTerm()
        
        # option 3: logical operator
        elif self.tokens[self.position] in logicOps:
            return self.logicalTerm()
        
        # Lastly, not a valid term
        else:
            return False
    
    # Evaluate whether the term matches the dash operator, binary infix, form
    # Note that '=6' tokenizes to just the number 6 ONLY.
    def dashTerm(self):
        
        self.nextToken()
        # Check if there is a next term
        if self.position < len(self.tokens):
            # go to next term, which SHOULD BE A DASH
            if self.tokens[self.position] == "-":
                pass
            else:
                return False
        else:
            return False
        
        # go to next term after the dash, which should be a integer!
        self.nextToken()

        # First check if there is even a term that comes after
        if self.position < len(self.tokens):
            if self.tokens[self.position].isdigit():
                self.nextToken()
                return True
                # end up at the next token for evaluation
            else:
                return False
        else:
            return False

    # Evaluate whether the term matches the relational operator, unary prefix form
    def relopTerm(self):
        # go to next term, which SHOULD BE A INT
        self.nextToken()
        # First check if there is even a term that comes after
        if self.position < len(self.tokens):
            if self.tokens[self.position].isdigit():
                self.nextToken()
                return True
                # end up at the next token for evaluation
            else:
                return False # the term after the relational operator was invalid
        else:
            return False # there was a relational term with nothing after it
    
    # Evaluate whether the term matches the logical operator, binary infix, form
    def logicalTerm(self):
        if self.position < len(self.tokens):
                self.nextToken() # advance to next after logic operator and begin evaluation
                # TODO - the code is failing for the test case where there is a logic operator at the end (e.g. (!=5) and)
                self.parser()
                return True
        else:
            return False


# sample test code, use examples from the prompt for more testing 
# positive tests: validation of the expression returns True

r = recDescent('7-17')
print(r.validate()) # should return True

r = recDescent('>90')
print(r.validate()) # should return True

r = recDescent('(1 - 100 and not 50) or > 200')
print(r.validate()) # should return True

r = recDescent('(7 - 17) or > 90')
print(r.validate()) # should return True

r = recDescent('> 50 or == 20')
print(r.validate()) # should return True

r = recDescent('1 - 100 and != 50')
print(r.validate()) # should return True

r = recDescent('(5 - 100) and (not 50) or (>= 130 or (2 - 4))')
print(r.validate()) # should return True

#####################
# negative tests: validation of the expression returns False  
r = recDescent('>')
print(r.validate()) # should return False

r = recDescent('2--4')
print(r.validate()) # should return False

r = recDescent('-7')
print(r.validate()) # should return False

r = recDescent('7-')
print(r.validate()) # should return False

r = recDescent('=6')
print(r.validate()) # should return False

r = recDescent('(!=5) and')
print(r.validate()) # should return False

r = recDescent('2-4 and ><300')
print(r.validate()) # should return False

r = recDescent('>= 5) nand < 10')
print(r.validate()) # should return False