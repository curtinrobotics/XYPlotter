"""
fileIO - read and write from file

"""

def fileRunner(file):
    with open(file, "r") as fileObj:
        try:
            fileText = fileObj.read()
        except FileNotFoundError:
            print("ERROR: Invalid file.\n Please recomplie with valid file")
    
    return fileText

