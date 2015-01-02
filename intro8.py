import sys
#1.

def fun1(x):
    assert x > 0
    a = 5/x
    print (a)

    #If you run the program with a negative number you will have an AssertionError
    
#2.

def fun2 (a,b):
    if type(a)!= list and type( b ) != list:
        return -1
   

#3. 
def func3 (a, b):
    if isinstance(a, int) and isinstance(b, int):
        return "Integer!!!"
 
#4. 

def read(text):
    try:
        te= open (text, "r")
    except FileNotFoundError:
        print("The file don't exist, error:", sys.exc_info()[0])


#5. Explain why it does not make sense to put a try...except clause around a function definition.
#Also explain why it may make sense to put it around a function call.
