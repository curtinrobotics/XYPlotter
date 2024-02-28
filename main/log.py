"""
log.py
Class to log error/warning/error messages.
"""

import datetime
import constants as const
import inputOutput as io

# Variables
log = None

"""Class for holding error, warning and debug log"""
class DebugLog():

    """Constructor create blank list to add to"""
    def __init__(self):
        self.dLog = []
        self.dLog.append(self.__DebugLogEntry('timestamp', str(datetime.datetime.now())))
        io.writeFileData(const.TEMP_LOG_PATH, str(self) + '\n')

    def __str__(self):
        
        entries = []
        
        for i in range(len(self.dLog)):
            #entry = self.dLog[i]
            entries.append(self.dLog[i])#[entry.cat, entry.msg])

        return '\n'.join([str(e) for e in entries])

    """Adding entry to log"""
    def newLog(self, cat, msg):
        if cat not in ["error", "warning", "debug"]:
            self.newlog("error", "Category \"" + str(cat) + "\" does not exist for \"" + str(msg) + "\"")
        else:
            self.dLog.append(self.__DebugLogEntry(cat, msg))
            self.updateLogFile(str(self.dLog[-1]) + '\n')

    """Print log to terminal and return string"""
    def outputLog(self, error=False, warning=False, debug=False, terminal=True):
        outputString = ""
        for item in self.dLog:
            if item.cat == "error" and error:
                outputString += str(item.msg) + "\n"
            elif item.cat == "warning" and warning:
                outputString += str(item.msg) + "\n"
            elif item.cat == "debug" and debug:
                outputString += str(item.msg) + "\n"
        if terminal:
            print(outputString)
        return outputString
    
    def updateLogFile(self, data):
        return io.appendFileData(const.TEMP_LOG_PATH, data)

    """Inner class for each entry"""
    class __DebugLogEntry():

        def __init__(self, cat, msg):
            self.cat = cat
            self.msg = msg

        def __str__(self):
            return f'{self.cat.upper()}:\t{self.msg}'

"""Log data variable"""
def createLog():
    global log
    log = DebugLog()
