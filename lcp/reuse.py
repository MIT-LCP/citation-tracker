"""
Utilities for tracking reuse of LCP resources
"""

def helloworld():

    a = ['h','l','o','o','l']
    b = ['e','l',' w','r','d']
    c = ''
    
    for i in zip(a,b):
        c = c + i[0] + i[1]
    
    return c



