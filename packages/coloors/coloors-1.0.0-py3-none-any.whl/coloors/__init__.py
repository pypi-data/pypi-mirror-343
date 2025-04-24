from .bcolors import bcolors


def printp(s):
    """Print in Purple or Rose depending on your color blindness"""
    if not isinstance(s, str):
        s = str(s)
    print(bcolors.HEADER + s + bcolors.ENDC)

 

def printb(s):
    """Print in Blue"""
    if not isinstance(s, str):
        s = str(s)
    print(bcolors.OKBLUE + s + bcolors.ENDC)

 

def printc(s):
    """Print in Cyan"""
    if not isinstance(s, str):
        s = str(s)
    print(bcolors.OKCYAN + s + bcolors.ENDC)

 

def printg(s):
    """Print in Green"""
    if not isinstance(s, str):
        s = str(s)
    print(bcolors.OKGREEN + s + bcolors.ENDC)

 

def printy(s):
    """Print in Yellow"""
    if not isinstance(s, str):
        s = str(s)
    print(bcolors.WARNING + s + bcolors.ENDC)
def printr(s):
    """Print in Red"""
    if not isinstance(s, str):
        s = str(s)
    print(bcolors.FAIL + s + bcolors.ENDC)
def printu(s):
    """Print in Underlined"""
    if not isinstance(s, str):
        s = str(s)
    print(bcolors.UNDERLINE + s + bcolors.ENDC)

 

def printbld(s):
    """Print in BOLD"""
    if not isinstance(s, str):
        s = str(s)
    print(bcolors.BOLD + s + bcolors.ENDC)

 

 

def r(s):
    """return string in red"""
    if not isinstance(s, str):
        s = str(s)
    return bcolors.FAIL + s + bcolors.ENDC

 

def b(s):
    """return string in blue"""
    if not isinstance(s, str):
        s = str(s)
    return bcolors.OKBLUE + s + bcolors.ENDC

 

def g(s):
    """return string in green"""
    if not isinstance(s, str):
        s = str(s)
    return bcolors.OKGREEN + s + bcolors.ENDC

 

def p(s):
    """return string in purple"""
    if not isinstance(s, str):
        s = str(s)
    return bcolors.HEADER + s + bcolors.ENDC

 

def c(s):
    """return string in cyan"""
    if not isinstance(s, str):
        s = str(s)
    return bcolors.OKCYAN + s + bcolors.ENDC

 

def bld(s):
    """return string in bold"""
    if not isinstance(s, str):
        s = str(s)
    return bcolors.BOLD + s + bcolors.ENDC

 

 

def u(s):
    """return string in underline"""
    if not isinstance(s, str):
        s = str(s)
    return bcolors.UNDERLINE + s + bcolors.ENDC

 

 

def ye(s):
    """string in Yellow, named ye instead of y since, we use 'y' a lot as a variable name in Ai"""
    if not isinstance(s, str):
        s = str(s)
    return bcolors.WARNING + s + bcolors.ENDC

if __name__ == '__main__':
    printu("hey")