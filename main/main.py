"""
main.py
Call to start the program.
Calls other functions to run program.
Has command line arguments for running in different modes (CLI(default), GUI, LCD)
"""

# Libraries
import gui
import pipeline
import turtlePlot
import sys

def main():
    argv = sys.argv
    argc = len(argv)

    isCli = False
    isGui = False
    isHelp = False
    isError = False
    errorReason = ""

    # What is in arguments
    validArgs = ["-c", "--cli", "-g", "--gui", "-h", "--help"]
    for arg in argv[1:]:
        if arg not in validArgs:
            isError = True
            errorReason = f"Invalid argument: {arg}"
    if "-c" in argv or "--cli" in argv or argc == 1:
        isCli = True
    if "-g" in argv or "--gui" in argv:
        isGui = True
    if "-h" in argv or "--help" in argv:
        isHelp = True
    if isCli + isGui + isHelp != 1 and not isError:
        isError = True
        errorReason = "Invalid combination of arguments"

    # Run depending on arguments
    if isError:
        print(errorReason)
        displayHelp()
    elif isCli:
        callCli()
    elif isGui:
        callGui()
    elif isHelp:
        displayHelp()


def displayHelp():
    print("Usage: python main.py [OPTIONS]")
    print()
    print("  -c, --cli          Run program in CLI mode. (default)")
    print("  -g, --gui          Run program in GUI mode.")
    print("  -h, --help         Show this message and exit.")


def callCli():
    print("\n--== SVG Processing Tool v.alpha ==--\n")
    pointList = pipeline.pipeline()
    turtlePlot.turtlePlot(pointList)


def callGui():
    print("\n--== SVG Processing Tool v.alpha ==--\n")
    newGui = gui.GUI()
    newGui.mainloop()


if __name__ == '__main__':
    main()