def fileRunner(FILE):
    with open(FILE, "r") as fileObj:
        try:
            fileText = fileObj.read()
        except FileNotFoundError:
            print("ERROR: Invalid file.\n Please recomplie with valid file")
    
    return fileObj

