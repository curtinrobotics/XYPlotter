"""
setup.py
Changes variables/flags used later in the program.
Interfaces with gui.py and lcd.py.
"""

import os
import re
import inputOutput as io

CONSTANTS_FILE_PATH = os.getcwd() + '/constants.py'

"""Retrieves variables as ConstantVariable objects from constants.py"""
def getVariables(ignoreUnchangeable = True, filePath = CONSTANTS_FILE_PATH):
    #ignoreUnchangeable - boolean - specifies whether or not unchangeable variables should be omitted

    fileData = io.readFileData(filePath)
    lines = fileData.split('\n')
    
    #Specifies format that variables should follow
    variableFormat = re.compile(r'''

        ([A-Z_]+)
        \s?=\s?
        (["A-Za-z0-9'/\\\.,_\-\s:]+ | [\(\[] [ 0-9,]+ [\)\]])
        (\s*\#.+)*

    ''', re.VERBOSE | re.DOTALL)


    allowedVariables = [] # Which variables are allowed to be retrieved
    
    for l in lines:
        if l == '# RESTRICTED' and ignoreUnchangeable == True:
            break
        allowedVariables.append(re.search(variableFormat, l))

    #Creates ConstantVariable objects from all variables given by regex
    variableObjects = [ConstantVariable(regObj.groups()[0], regObj.groups()[1], regObj.groups()[2]) for regObj in allowedVariables if type(regObj) == re.Match]

    return variableObjects

"""Sets a variable from constants.py"""
def setVariable(variable):
    # variable - ConstantVariable - the variable to set in constants.py

    variableObjects = getVariables()
    variableDict = dict()
    for obj in variableObjects:
        name = obj.getName()
        variableDict[name] = obj

    if type(variable) != ConstantVariable:
        io.printe("ERROR: Invalid variable type.\n Please recompile with valid type")
    elif variable.getName() not in variableDict.keys():
        io.printe("ERROR: Invalid variable name.\n Please recomplie with valid name")

    variableDict[variable.getName()] = variable

    return saveConstants(variableDict.values())


"""Saves the variables given to constants.py"""
def saveConstants(variableList):
    # variableList - list - list of ConstantVariable objects to set in constants.py

    success = True

    fileData = io.readFileData(CONSTANTS_FILE_PATH)
    lines = fileData.split('\n')

    for i in range(len(lines)):
        line = lines[i]
        if line in [str(var) for var in variableList]: # if line contains changeable variable
            lines[i] = line
            continue

        for var in variableList:
            if(line.startswith(var.getName())): # Set line as new data if variable name is the same as given
                lines[i] = str(var)
                break
        
    if not io.writeFileData(CONSTANTS_FILE_PATH, '\n'.join(lines)):
        success = False
        
    return success

"""Class to serve as custom constant variables"""
class ConstantVariable():
    
    def __init__(self, name, value, comment = '', type = str):
        self.name = name
        self.value = value
        self.comment = comment
        self.type = type
        self.debug = False

        self.min = 0
        self.max = 1

        self.formatTags()

    def __str__(self):
        """ Creates string representation of ConstantVariable object """
        if self.comment == None: self.comment = ''
        return self.name + ' = ' + str(self.value) + self.comment

    def getName(self):
        return self.name

    def getValue(self):
        return self.value
    
    def getComment(self):
        return self.comment
    
    def getType(self):
        return self.type

    def getMin(self):
        return self.min
    
    def getMax(self):
        return self.max

    def setValue(self, value):
        self.value = value

    def formatTags(self):
        """ Define tags set within constants.py """
        tagRegex = re.compile(r'''

            \|\s*
            (?:type\s*\=\s*)*
            ([0-9A-Za-z]+)*
            \s*
            (?:min\s*\=\s*)*
            ([0-9]+)*
            \s*
            (?:max\s*\=\s*)*
            ([0-9]+)*
            \s*
            (log\s*)*
                              
        ''', re.VERBOSE)

        match = re.search(tagRegex, self.getComment())
        if match != None: 
            # Assign found groups to variables
 
            foundType = match.groups()[0]
            self.min = match.groups()[1]
            self.max = match.groups()[2]
            self.debug = match.groups()[3]
        
        else: foundType = 'str' # if not found, define type as string

        # Define self.type objects based on found type
        if foundType == 'int': self.type = int
        elif foundType == 'float': self.type = float
        elif foundType == 'bool': self.type = bool
        elif foundType == 'str': self.type = str
        else: self.type = foundType