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

    # lex - tokenize the expression into a list of tokens
    # the tokens are stored in a list which can be accessed by self.tokens
    # do NOT edit any piece of code in this function

    def lex(self):
        self.tokens = re.findall("[-\(\)]|[!<>=]=|[<>]|\w+|[^ +]\W+", self.expr)
        # transform tokens to lower case, and filter out possible spaces in the tokens
        self.tokens = list(filter((lambda x: len(x)), 
                           list(map((lambda x: x.strip().lower()), self.tokens))))    
    
    # parser - determine if the input expression is valid or not
    # delete tokens after parsing so they do not get parsed again
    def parser(self, operation):
        #TODO
        pass

    # validate() function will return True if the expression is valid, False otherwise 
    # do NOT change the method signature 

    def validate(self):
        # Using the tokens from lex() tokenization,
        # this validate would first call lex() to tokenize the expression,
        # then call the top level parsing procedure for the outermost rule
        # and go from there
        
        self.lex()

        # TODO: call the topmost parsing procedure and go from there
        valid_parenthesis = self.parenthesis()
        valid_dash = self.dash()
        valid_ops = self.operators()
        validity_logs = self.logicals()
        if (valid_parenthesis and valid_dash and valid_ops and validity_logs):
            return True
        else:
            return False

    # TODO: Write your parsing procedures corresponding to the grammar rules - follow Figure 5.17
    
    # I think the methodology here is bad. Maybe we want to just use recursion to return only the expressions, and then perform all the checks in validate()
    # Or remove the tokens after parsing to ensure they don't get checked again?? Maybe there should be a parser function that accepts the term and
    # returns false or true depending on whether it's a valid statement
    # When tokens are deleted and replaced, the initial loop to obtain positions no longer works and can become out of bounds

    def parenthesis(self):
        found_parentheses = False
        # arrays to monitor locations of parentheses
        parentheses_open = []
        parentheses_close = []
        # loop through to find all instances of parentheses
        for index, token in enumerate(self.tokens):
            if token == '(':
                parentheses_open.append(index)
                found_parentheses = True
            if token == ')':
                parentheses_close.append(index)
                found_parentheses = True

        # parentheses must be found
        if found_parentheses:
            # number of parentheses must match or expression is false
            if len(parentheses_close) != len(parentheses_open):
                return False
            else:
                # the first open parenthesis (index 0 + 1) should be terminated by the last closing parenthesis (index -1 to get last detected instance)
                # add +1 to omit the first open parenthesis and start building from between the parentheses
                # new_expr is all the contents between the parentheses
                new_expr = " ".join(self.tokens[i] for i in range(parentheses_open[0]+1, parentheses_close[-1]))
                del self.tokens[parentheses_open[0]:parentheses_close[-1]+1]
                # self.tokens.insert(parentheses_open[0],'term')
                recurs = recDescent(new_expr)
                return recurs.validate()
        else:
            # default return True if no errors found with parsing parentheses
            return True
    
    # All dash operators and relational operators have the same precedence
    # Define them here
    def dash(self):
        operator_dash = "-"

    def operators(self):
        
        
        operator_relational = ["<", "<=", ">", ">=", "==", "!=", "not"]
        # arrays to monitor instances and locations of operators
        dashOps = []
        relOps = []
        #loop through tokens list and find all operators
        for index, token in enumerate(self.tokens):
            if token in operator_dash:
                dashOps.append(index)
            if token in operator_relational:
                relOps.append(index)
        
        # dash operator found. check validity.
        if dashOps:
            for i in range(len(dashOps)):
                # dash operator must be of form term dash term, so there must be at least three terms
                if len(self.tokens) < 3:
                    del self.tokens[dashOps[0]-1:dashOps[0]+2]
                    return False
                # the terms to the left and right of the dash operator must be numbers. Check if can be converted to digits
                elif not self.tokens[dashOps[i]-1].isdigit() or not self.tokens[dashOps[i]+1].isdigit():
                    del self.tokens[dashOps[0]-1:dashOps[0]+2]
                    return False
            del self.tokens[dashOps[0]-1:dashOps[0]+2]
        # relational operator found. check validity.
        if relOps:
            for i in range(len(relOps)):
                # dash operator must be of form relop int, so there must be only two terms
                if len(self.tokens) < 2:
                    del self.tokens[relOps[0]:relOps[0]+2]
                    return False
                # the term to the right of the relational operator must be a number. Check if can be converted to digits
                elif not self.tokens[relOps[i]+1].isdigit():
                    del self.tokens[relOps[0]:relOps[0]+2]
                    return False
            # Remove tokens after parsing
            del self.tokens[relOps[0]:relOps[0]+2]
        # Otherwise, the expression should be true
        return True
    def logicals(self):
        # TODO
        operator_logical = ["and", "or", "nand"]
        logOps = []
        for index, token in enumerate(self.tokens):
            if token in operator_logical:
                logOps.append(index)
        
        #if any logical operators found
        if logOps:
            # TODO
            pass
        # default return True if no logical operators found
        return True

# sample test code, use examples from the prompt for more testing 
# positive tests: validation of the expression returns True
# negative tests: validation of the expression returns False  

r = recDescent('(5 - 100)') 
print(r.validate()) # should return True

r = recDescent('5 - ') 
print(r.validate()) # should return False

r = recDescent('> 90')
print(r.validate()) # should return True

r = recDescent('(1 - 100 and not 50) or > 200')
print(r.validate()) # should return True