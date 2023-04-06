"""
log.py
Class to log error/warning/error messages.
"""

# Variables
log = None

"""Class for holding error, warning and debug log"""
class DebugLog():

    """Constructor create blank list to add to"""
    def __init__(self):
        self.dLog = []

    """Adding entry to log"""
    def newLog(self, cat, msg):
        if cat not in ["error", "warning", "debug"]:
            self.newlog("error", "Category \"" + str(cat) + "\" does not exist for \"" + str(msg) + "\"")
        else:
            self.dLog.append(self.__DebugLogEntry(cat, msg))

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

    """Inner class for each entry"""
    class __DebugLogEntry():

        def __init__(self, cat, msg):
            self.cat = cat
            self.msg = msg

"""Log data variable"""
def createLog():
    global log
    log = DebugLog()
