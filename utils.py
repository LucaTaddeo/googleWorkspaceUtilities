from constants import maxRowLength

def printBoxAndAskUser(title, label):
    printTitle(title)
    choice = input("| "+label+": ")
    printClosure()
    return choice

def printTitle(title):
    print("\n" + "-"*3 + title + "-"*(maxRowLength-len(title)-3))

def printClosure():
    print("-"*maxRowLength + "\n")