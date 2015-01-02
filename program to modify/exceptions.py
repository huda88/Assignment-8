import sys

try:
    #import file
    y = int(input("Choose a denominator: ")) #ValueError if not number
    f = open('file.txt')                #FileNotFound
    i = int(len(f.readline().strip())) #(len(f.readline().strip()))
    result = i / y                      #ZeroDivisionError
    print(result)
except ImportError:
    print("Error: Can't find the file", sys.exc_info()[0])
    raise
except FileNotFoundError:
    print ("File don't found, create one:",sys.exc_info()[0])
    raise
except ValueError:
    print ("Impossible to convert text in number like this:",sys.exc_info()[0])
    raise 
except ZeroDivisionError:
    print ("Is not possible divide by zero:"sys.exc_info()[0])
    raise
