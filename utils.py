from constants import maxRowLength, ansiColors

def getColoredText(text, colors):
    if isinstance(colors, str):
        colors = [colors] 

    wrappedText = text
    for color in colors:
        if color in ansiColors:
            color_code = ansiColors[color]
            wrappedText = color_code + wrappedText + ansiColors["reset"]

    return wrappedText

def printBoxAndAskUser(title, label):
    printTitle(title)
    choice = input("| "+label+": ")
    printClosure()
    return choice

def printBoxAndAskUserWithOptions(title, label, options, text=None):
    printTitle(title)
    if text is not None:
        print("| " + text)
    choice = None
    while True:
        choice = input("| "+label+": ")
        if choice in options:
            break
        else:
            print("| Invalid option, please try again!")
    printClosure()
    return choice

def printTitle(title):
    print("\n" + "-"*3 + getColoredText(title, "bold") + "-"*(maxRowLength-len(title)-3))

def printClosure():
    print("-"*maxRowLength + "\n")
