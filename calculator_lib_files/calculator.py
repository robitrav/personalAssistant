"""
Travis Robinson
Oregon State
Computer Science
travisrobinson2006@gmail.com
robitrav@oregonstate.edu
"""

"""
Calculator module for Victoria. Contains functions for converting numbers as text to numbers, as well as doing the calculations that are needed
"""

#import modules
import math
from collections import deque

#operators--made global so it can be referenced by other modules--operators_english used as part of converting from text to math-ready values--'end' is a flag signaling termination of
#the equation
operators = ['+','-','x','/','end']
operators_english1 = ['plus','minus','times','divide']
operators_english2 = ['add','subtract','multuple','divided']
operators_english = [operators_english1,operators_english2]

scale_units = ['thousand','million','billion','trillion','quadrillion']

"""
Description: receives a list containing ints and words, converts it into a single value
Input: a number as a mix of ints and strings (ie 6 "billion")
Output: a single value (ie 6000000000)
Note:Found that speech recognizer has numbers as strings, not ints, "6" not 6--should rewrite this to take care of converting "6" to 6--as stands this is done in calling function
"""
def word_to_num(word):
    invalid_number = result_negative = 0 #flags used to check for negative or invalid numbers
    current = 0 #use this to hold input digits to multiply by scale values (million, billion, etc); add to result after this is done
    result = 0 #accumulator for final result

    for i in word:
        if word.index(i)==(len(word)-1) and isinstance(i,(int,long)):#if last number, add it to result; case where number doesn't end in 0 (ie last word entered is not million, etc)
            result = result+i
        elif isinstance(i,(int,long)) and current != 0:
            return "invalidNumber"
        elif isinstance(i,(int,long)):
            current = i
        elif i in scale_units:
            current = current*math.pow(10,(scale_units.index(i)+1)*3) #multiply current value by scale value, determined by location location of scale in list
            result = result + current #add current to result and reset-do here so as not to add scale coefficient to result
            current = 0
        elif word.index(i) == 0 and i == 'negative': #check to see if negative flag needs setting
            result_negative = 1
        else:
            return "invalidNumber"
    if result_negative == 1:
        result = result * -1
    return result


"""
Description: converts a user given infix expression to postfix
Input: an equation using infix notation
Output: an equation using postfix notation
"""
def infix_to_postfix(equation):
    marker_begin = marker_end = 0
    stack = []
    postfix = deque([])
#    operators = ['+','-','*','/','sqrt','end']
    equation.append('end')#used to mark the end of the list, retrieving proper values
    for i in equation:#convert to postfix
        if i in operators or equation.index(i)+1 == len(equation):#sort through using operators as a delimiter from converting values
            postfix.append(word_to_num(equation[marker_begin:marker_end]))#append to postfix the number converted from list of strings to a single value
            if len(stack) == 0:#is stack empty operator goes on
                stack.append(i)
            elif operators.index(stack[-1]) > operators.index(i):#affix operators in correct order using pemdas--pop higher tier operators from stack to postfix before placing lower tier on stack
                postfix.append(stack[-1])
                stack.pop()
                stack.append(i)
            else:#lower tier operator stays on stack, higher tier placed on top
                stack.append(i)
            marker_begin = equation.index(i)+1
            marker_end = marker_begin
        else:#adjust marker so we know what words to send to word_to_num
            marker_end = marker_end + 1
    stack.pop() #remove end marker from stack
    while len(stack) != 0:
        postfix.append(stack[-1])
        stack.pop()
    return postfix

"""
Description: solves postfix equations
Input: a postfix equation
Output: an answer
"""
def solve_postfix(postfix):
    stack = []
    while len(postfix) != 0:#solve postfix,go through pushing values onto stack--when operator found, remove top two values and apply operator, pushing result onto stack
        if postfix[0] == '+':
            postfix.popleft()
            val_two = stack[-1]
            stack.pop()
            val_one = stack[-1]
            stack.pop()
            stack.append(val_one+val_two)
        elif postfix[0] == '-':
            postfix.popleft()
            val_two = stack[-1]
            stack.pop()
            val_one = stack[-1]
            stack.pop()
#            print val_one
 #           print val_two
            stack.append(val_one-val_two)
        elif postfix[0] == 'x':
            postfix.popleft()
            val_two = stack[-1]
            stack.pop()
            val_one = stack[-1]
            stack.pop()
            stack.append(val_one*val_two)
        elif postfix[0] == '/':
            postfix.popleft()
            val_two = stack[-1]
            stack.pop()
            val_one = stack[-1]
            stack.pop()
            stack.append(val_one/val_two)
        else:
            stack.append(postfix[0])
            postfix.popleft()
    return stack[0]#stack at end will only contain final value, return as number

"""
Description: wrapper function, accepts an equation from user, solves it
Input: an infix equation full of words
Output: the value of the equation
"""
def calculate(equation):
    return solve_postfix(infix_to_postfix(equation))
