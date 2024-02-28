"""
gui.py
GUI to handle user inputs and setup using Tkinter.
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.colorchooser as colour
import tkinter.scrolledtext as scrollT
import tkinter.simpledialog as dia
import os
import subprocess
import setup
import inputOutput as io
import datetime
import log
import constants as const
import numpy as np
import re
import importlib
from turtle import ScrolledCanvas, RawTurtle, TurtleScreen
import turtlePlot
import importlib

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.variableCreation()
        self.notebookSetup()

    def variableCreation(self):
        #Finds all svg files in directory
        dirname = os.getcwd()

        self.filedir = dirname + '/sgvFiles' #yes svg is spelt wrong ;)
        self.file_list = os.listdir(self.filedir)
        self.DEFAULT_CONSTANTS_FILE_PATH = dirname + '/constants_defaults.py'

        # Create log for gui:
        log.createLog()

        # convert cm to pixels
        PIXELS_PER_CM = 267/2.54 #different resolution on 3D printer thingy
        height_in_cm = 2.5
        width_in_cm = 8.5

        self.height_in_pixels = int(height_in_cm * PIXELS_PER_CM)
        self.width_in_pixels = int(width_in_cm * PIXELS_PER_CM)

    def notebookSetup(self):
        # create the tkinter window
        self.geometry(f"{self.width_in_pixels}x{self.height_in_pixels}")

        label = tk.Label(self, text="XY-Plotter GUI")
        label.pack()

        # Create notebook
        self.notebook = ttk.Notebook(self, width=self.width_in_pixels, height=self.height_in_pixels)
        self.notebook.pack(fill = 'both', expand=True)

        self.frameCreation()
        self.frameSetup()

    def frameCreation(self):
        self.frameDict = {}

        mainFrame = MainFrame(self.notebook, self)
        self.frameDict[MainFrame] = mainFrame

        variablesFrame = VariablesFrame(self.notebook, self)
        self.frameDict[VariablesFrame] = variablesFrame

        logFrame = LogFrame(self.notebook, self)
        self.frameDict[LogFrame] = logFrame

        # Add main notebook tab
        self.notebook.add(self.frameDict[MainFrame], text='Menu')

    def frameSetup(self):
        for frame in self.frameDict.values():
            frame.createPage()



    # Common Functions:

    # verify user action on file save
    def fileSaveCheck(self, fileDir : str, fileExtension : str, fileData : str, executeFunction = None, name : str = None):
        if name == None:
            name = dia.askstring("File Name", "What would you like to call the file (leave blank for timestamp)")

            if name == None: return

            if name.strip() == '': name = datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')

        #fileData = io.readFileData(tempLogFilePath)
        if fileData != False and io.writeFileData(f'{fileDir}/{name}.{fileExtension}', fileData):
            mb.showinfo("SUCCESS", "File successfully saved!")
            
            if executeFunction != None: executeFunction(name)

            #io.deleteFile(tempLogFilePath)
            #combobox.set(f'{name}.log')
        else: 
            print('fileData: ', fileData)
            print('fileDir: ', fileDir)
            print('name: ', name)
            print('fileExtension: ', fileExtension)
            mb.showerror("ERROR", "File could not be saved!")

class MainFrame(tk.Frame):
    def __init__(self, master, parent):
        super().__init__(master, name='main')
        self.parent = parent

    def createPage(self):
        # Create main frame
        self.configure(width=self.parent.width_in_pixels, height=self.parent.height_in_pixels - 20)
        #self.pack(fill='both', expand=True)

        # Create frames for sections of the screen (work around for using pack instead of grid)
        topFrame = tk.Frame(self)
        topFrame.pack(fill='x', expand=False, anchor='n')

        bottomFrame = tk.Frame(self)
        bottomFrame.pack(fill='x', expand=True, anchor='n')

        # create a listbox with items in file_list for svg files
        self.listboxHeight = tk.IntVar(self)
        self.listboxHeight.set(len(self.parent.file_list)) # Create dynamic tk variable # Doesn't work

        self.listbox = tk.Listbox(topFrame, selectmode=tk.SINGLE, width=80, height=self.listboxHeight.get())
        for filename in self.parent.file_list:
            self.listbox.insert(tk.END, filename)
        self.listbox.pack(side=tk.LEFT, fill='x', expand=True, anchor='n')

        # Create a frame to contain all the buttons
        mainButtonFrame = tk.Frame(topFrame)
        mainButtonFrame.pack(side=tk.RIGHT, fill='x', expand=True, anchor='n')

        self.canvasWidth = tk.IntVar(self)
        self.canvasHeight = tk.IntVar(self)

        self.canvasWidth.set(const.PLOTTER_WIDTH)
        self.canvasHeight.set(const.PLOTTER_HEIGHT)

        self.previewCanvas = ScrolledCanvas(bottomFrame, width=self.canvasWidth.get(), height=self.canvasHeight.get())
        self.previewCanvas.pack(anchor='center')

        self.screen = TurtleScreen(self.previewCanvas)
        self.turtle = RawTurtle(self.screen)

        self.master.bind('<<NotebookTabChanged>>', self.notebookTabChangedFunc, add='+')
        self.listbox.bind('<<ListboxSelect>>', self.save_selection)
        self.previewCanvas.bind('<Configure>', lambda e: e.widget.configure(width=self.canvasWidth.get(), height=self.canvasHeight.get()))

        self.createButtons(mainButtonFrame)


    def createButtons(self, mainButtonFrame):
        # Button to execute run_selection()
        previewButton = tk.Button(mainButtonFrame, text='Show Preview', command=self.run_selection)
        previewButton.pack()

        # Create button to create new change variable tab
        changeButton = tk.Button(mainButtonFrame, text='Change Variables', command=self.setupVariablesPage)
        changeButton.pack()

        # Create button to create new log tab
        logButton = tk.Button(mainButtonFrame, text='View Log', command=self.setupLogPage)
        logButton.pack()

        # Create button to quit
        quitButton = tk.Button(mainButtonFrame, text='Quit', command=self.exitGui)
        quitButton.pack()

    def updateListbox(self, e):
        self.listbox.delete(0, tk.END)
        for filename in os.listdir(self.parent.filedir):
            self.listbox.insert(tk.END, filename)
        self.listboxHeight.set(len(os.listdir(self.parent.filedir)))
        self.listbox.configure(height=self.listboxHeight.get())

    def updatePreviewCanvas(self, e):
        importlib.reload(const)
        self.canvasWidth.set(const.PLOTTER_WIDTH)
        self.canvasHeight.set(const.PLOTTER_HEIGHT)
        self.previewCanvas.configure(width=self.canvasWidth.get(), height=self.canvasHeight.get())
        
        if e.widget.tab(e.widget.select())['text'] == 'Menu':
            try:
                self.selected_file
                io.printd("Updating Selected Preview")
                self.run_selection()
            except AttributeError:
                ...

    def notebookTabChangedFunc(self, e):
        self.updateListbox(e)
        self.updatePreviewCanvas(e)

    def exitGui(self):
        """ Function to ask user about intention to quit """

        if mb.askyesno(title='Quit?', message='Are you sure you want to quit?'):
            self.parent.quit()

    # function to save the selected file in the list
    def save_selection(self, e):
        #selection = listbox.curselection()
        selection = e.widget.curselection()
        if selection:
            self.selected_file = self.listbox.get(selection)
            
            self.filePath = '\"sgvFiles/' + self.selected_file + '\"'

            # Save filePath in constants.py
            if setup.setVariable(setup.ConstantVariable('FILE', self.filePath, '   # Source file for plotting')):
                print('File successfully saved!')
                #mb.showinfo(title="SUCCESS", message='File successfully saved!')
            else:
                mb.showerror(title="FAILURE", message='File could not be saved!')
        else:
            if self.master.tab(self.master.select())['text'] != 'Log':
                mb.showwarning(title="WARNING", message='Ensure that you have first selected a file!')

    # Run main.py with the given selection
    def run_selection(self):
        """ Function to run the main.py file with the given gui parameter """

        # Check if a file has been saved
        try:
            # Define file path format to save in constants.py 
            self.filePath = '\"sgvFiles/' + self.selected_file + '\"'
            print(self.filePath)
        except AttributeError as e:
            mb.showwarning(title="WARNING", message='Ensure that you have first saved a selection!')
            return
        

        #turtle.clear()
        self.screen.reset()
        self.turtle.reset()
        #turtle.speed(10)
        #screen.clear()

        # Run main.py
        try:
            #subprocess.run(['python3', 'main.py', 'gui']
            #import main
            try:
                importlib.reload(self.main)
                io.printd('Main reloaded!')
            except AttributeError:
                self.main = importlib.import_module('main')

            #main = importlib.import_module('main')
            self.main.tp.turtlePlot(self.main.pointList, gui=True, turt=self.turtle, s=self.screen)
            #global logContents
            #logContents = log.log.dLog
        except Exception as e:
            print(e)

    def setupVariablesPage(self):
        self.master.add(self.parent.frameDict[VariablesFrame], text='Variables')

    def setupLogPage(self):
        self.master.add(self.parent.frameDict[LogFrame], text='Log')
        
class VariablesFrame(tk.Frame):
    def __init__(self, master, parent):
        super().__init__(master, name='variable')
        self.parent = parent

    def createPage(self):
        """ Function to create scrolling tab within notebook to contain variable changing objects """
        
        # Frame created for new tab
        self.configure(width=self.parent.width_in_pixels, height=self.parent.height_in_pixels)
        #tabFrame = tk.Frame(self, width=self.parent.width_in_pixels, height=self.parent.height_in_pixels, name='variables')
        #tabFrame.pack(fill='both', expand=True)

        # Canvas created to allow for scrolling
        scrollableCanvas = tk.Canvas(self)
        scrollableCanvas.pack(fill='both', expand=True)

        # Create scrollbar
        scrollBar = tk.Scrollbar(scrollableCanvas, orient='vertical', command=scrollableCanvas.yview)
        scrollBar.pack(fill=tk.Y, side=tk.RIGHT)

        # Configure scrollbar to the canvas
        scrollableCanvas.configure(yscrollcommand=scrollBar.set)
        scrollableCanvas.bind('<Configure>', lambda e: scrollableCanvas.configure(scrollregion=scrollableCanvas.bbox("all")))

        # Create frame that will be scrolled
        # This will contain all variable changing objects
        self.variableFrame = tk.Frame(scrollableCanvas)
        scrollableCanvas.create_window(0, 0, window=self.variableFrame, anchor='nw', width=self.parent.width_in_pixels) # Add frame to canvas

        # Add variable changer objects to given frame
        self.implement_Variables(self.variableFrame)

        # Create button to reset values
        defaultsButton = tk.Button(self.variableFrame, text="Reset to Default?", command=self.verify)
        defaultsButton.pack(side=tk.RIGHT)

    # Create variable changer tab
    def implement_Variables(self, frame):
        """ Function to add required variables to create a variable change interface in the given frame """
        # frame - tk.Frame object - the frame to add objects to.
        
        self.variableDict = dict()
        variableObjects = dict()
        varlist = setup.getVariables()

        # For each changeable variable in constants.py
        for var in varlist:
            self.variableDict[var.getName()] = var
            if var.debug != None: continue

            if var.getType() in [int, float]:
                """ If variable is of type int or float, create a scale object """
                # Note: floats with increments not implemented yet

                # Create Scale object
                variableObjects[var.getName()] = tk.Scale(frame, label=var.getName(), from_= var.getMin(), to= var.getMax(), orient='horizontal')
                variableObjects[var.getName()].set(var.getValue()) # Set current value as saved value
                variableObjects[var.getName()].bind("<ButtonRelease-1>", self.scaleFunc) # Add function
                variableObjects[var.getName()].pack(fill='x') # Fill scale along x axis

            if var.getType() in [bool]:
                """ If variable is of type bool, create a checkbutton object """

                #Create Checkbutton object
                variableObjects[var.getName()] = ttk.Checkbutton(frame, text=var.getName())
                variableObjects[var.getName()].invoke() # Used to update state when variables are reset
                variableObjects[var.getName()].bind("<ButtonRelease-1>", self.checkFunc) # Add function
                variableObjects[var.getName()].pack(fill='x') # Fill scale along x axis

                if var.getValue() == 'True': variableObjects[var.getName()].state(['selected']) # If saved value is True, set as checked
                else: variableObjects[var.getName()].state(['!selected']) # else set as unchecked

            if var.getType() in ['colour', 'color']:
                """ If variable is of type colour/color, create a colour chooser object """
                
                # Create variable label
                header = tk.Label(frame, text=var.getName())
                header.pack(expand=True, fill='x')

                # Create button to execute colourFunc()
                variableObjects[var.getName()] = tk.Button(frame, text='Choose Colour', name=var.getName().lower())
                variableObjects[var.getName()].bind("<ButtonRelease-1>", self.colourFunc) # Add function to button
                variableObjects[var.getName()].pack(fill='x') # Fill scale along x axis


    def scaleFunc(self, event):
        """ Function to call when a scale object is adjusted """
        
        widget = event.widget
        value = widget.get()
        var = self.variableDict[widget.cget('label')]

        setup.setVariable(setup.ConstantVariable(var.getName(), value, var.getComment()))

    def checkFunc(self, event):
        """ Function to call when checkbutton object is pressed """

        widget = event.widget
        value = widget.instate(['!selected'])
        var = self.variableDict[widget.cget('text')]

        setup.setVariable(setup.ConstantVariable(var.getName(), value, var.getComment()))

    def colourFunc(self, event):
        """ Function to call when button to create colour chooser is pressed """
        
        widget = event.widget
        var = self.variableDict[widget.winfo_name().upper()]
        colour.Chooser(self.variableFrame, label=var.getName()) # Create colour picker
        selected_colour = colour.askcolor()

        if selected_colour[0] != None: setup.setVariable(setup.ConstantVariable(var.getName(), selected_colour[0], var.getComment()))

    def verify(self):
        """ Function to check whether the user truly wishes to reset variables or not """
        # Note: reset also changes comment
        # Note: can be generalised, but no requirement as of creation

        # Create message box to inquire about user's true intention
        if mb.askyesno(title='Continue?', message='Are you sure you want to reset values to defaults?'):
            # Get default variable values 
            defaultObjects = setup.getVariables(filePath=self.parent.DEFAULT_CONSTANTS_FILE_PATH)

            for var in defaultObjects:
                setup.setVariable(var) # Save each variable as default

            self.parent[MainFrame].previewCanvas.configure(width=self.parent[MainFrame].canvasWidth.get(), height=self.parent[MainFrame].canvasHeight.get())
            self.createPage() # Re-create variable changer tab

class LogFrame(tk.Frame):
    
    def __init__(self, master, parent):
        super().__init__(master, name='logframe')
        self.parent = parent

    def createPage(self):
        self.logFilesPath = './logFiles'
        self.tempLogFilePath = const.TEMP_LOG_PATH
        self.logContents = tk.StringVar(self.parent)

        #------------------------------------------------------------------------------------
        
        # Elements
        self.configure(width=self.parent.width_in_pixels, height=self.parent.height_in_pixels)
        #logFrame = tk.Frame(notebook, width=width_in_pixels, height=height_in_pixels, name='logframe')
        
        self.scrolledText = scrollT.ScrolledText(self)
        self.combobox = ttk.Combobox(self, postcommand=lambda: self.combobox.configure(values=os.listdir(self.logFilesPath)))
        buttonFrame = tk.Frame(self)
        saveButton = tk.Button(buttonFrame, command=self.saveLogFile, text='Save Log File')
        deleteButton = tk.Button(buttonFrame, command=self.deleteFile, text='Delete File')
        filtersButton = tk.Button(buttonFrame, command=self.openFilterButtons, text='Open Filters')
        
        #------------------------------------------------------------------------------------

        #------------------------------------------------------------------------------------

        # Configurations

        #logContents = io.readFileData(tempLogFilePath)
        self.logContents.set(io.readFileData(self.tempLogFilePath))

        if self.logContents.get() != None and self.logContents.get(): self.scrolledText.insert(tk.INSERT, self.logContents.get())
        self.scrolledText.configure(state='disabled')


        self.combobox.set(const.TEMP_LOG_PATH.replace(self.logFilesPath + '/', ''))
        self.combobox['state'] = 'readonly'
        self.combobox.bind('<<ComboboxSelected>>', self.selectedLogFile)

        self.master.bind('<<NotebookTabChanged>>', self.updateLogContents, add="+")

        #------------------------------------------------------------------------------------
        

        # Packing order and grid placements

        self.combobox.pack()
        buttonFrame.pack(fill='x')
        saveButton.grid(row=0, column=0)
        deleteButton.grid(row=0, column=1)
        filtersButton.grid(row=0, column=2)
        self.scrolledText.pack(fill='both', expand=True)

        #------------------------------------------------------------------------------------

    #import log
    #def openLog():

        # General Functions

    def updateScrolledText(self, scrolledText, logContents):
        scrolledText.configure(state='normal')
        scrolledText.delete(0.0, tk.END)
        scrolledText.insert(tk.INSERT, logContents)
        scrolledText.configure(state='disabled')
        
        #------------------------------------------------------------------------------------

        # Button Functions
    def saveLogFile(self):
        def f(name):
            io.deleteFile(self.tempLogFilePath)
            self.combobox.set(f'{name}.log')

        self.parent.fileSaveCheck(self.logFilesPath, 'log', io.readFileData(self.tempLogFilePath), f)

    def deleteFile(self):
        selection = self.combobox.get()
        result = mb.askyesno("WARNING", f"Are you sure you want to delete the file {selection}?")
        if result == True:
            if io.deleteFile(self.logFilesPath + '/' + selection):
                mb.showinfo('SUCCESS', 'File successfully deleted!')
                defaultFile = os.listdir(self.logFilesPath)[0]
                
                self.combobox.set(defaultFile)
                self.updateScrolledText(self.scrolledText, io.readFileData(self.logFilesPath + '/' + defaultFile))
            else:
                mb.showerror('ERROR', f'File {selection} could not be deleted!')
        
    def openFilterButtons(self):
        filterRoot = tk.Toplevel(self.parent)
        filterRoot.lift(aboveThis=self.parent)

        frame = tk.Frame(filterRoot, width=self.parent.width_in_pixels, height=self.parent.height_in_pixels)

        variableObjects = dict()

        def filterFunc(e):
            widget = e.widget
            varName = widget.cget('text')
            value = widget.instate(['!selected'])

            print(value)

            outputType = re.search('([A-Z]+)_\w+', varName).groups()[0]
            
            textValue = self.scrolledText.get(0.0, tk.END)
            
            if value == False:
                filteredText = []

                lines = textValue.split('\n')
                for i in range(len(lines)):
                    line = lines[i]
                    if not line.startswith(outputType):
                        filteredText.append(line)

                textValue = '\n'.join(filteredText)
                self.updateScrolledText(scrolledText=self.scrolledText, logContents=textValue)

            elif value == True: # Requires work.
                filteredText = []
                savedLines = [line for line in self.logContents.get().split('\n') if line != '']
                textBoxLines = [line for line in textValue.split('\n') if line != '']
                
                b = 0

                for i in range(len(savedLines)):

                    if savedLines[i].startswith(textBoxLines[b]): 
                        filteredText.append(textBoxLines[b])
                        if b < len(textBoxLines) - 1: b += 1
                    
                    else: 
                        
                        if savedLines[i].startswith(outputType):
                            filteredText.append(savedLines[i])

                
                textValue = '\n'.join(filteredText)
                self.updateScrolledText(scrolledText=self.scrolledText, logContents=textValue)


        logVariables = setup.getVariables()
        for var in logVariables:
            if var.debug == None: continue

            if var.getType() in [bool]:
                """ If variable is of type bool, create a checkbutton object """

                #Create Checkbutton object
                variableObjects[var.getName()] = ttk.Checkbutton(frame, text=var.getName())
                variableObjects[var.getName()].invoke() # Used to update state when variables are reset
                variableObjects[var.getName()].bind("<ButtonRelease-1>", filterFunc) # Add function
                variableObjects[var.getName()].pack(fill='x') # Fill scale along x axis

                if var.getValue() == 'True': variableObjects[var.getName()].state(['selected']) # If saved value is True, set as checked
                else: variableObjects[var.getName()].state(['!selected']) # else set as unchecked

        frame.pack()

        filterRoot.mainloop()



        

    # Event Bound Functions

    def updateLogContents(self, e):
        #logContents = io.readFileData(tempLogFilePath)
        self.logContents.set(io.readFileData(self.tempLogFilePath))
        #updateScrolledText(scrolledText, logContents)
        self.updateScrolledText(self.scrolledText, self.logContents.get())
        self.combobox.set(self.tempLogFilePath.replace(self.logFilesPath + '/', ''))

    def selectedLogFile(self, e):
        widget = e.widget
        value = widget.get()

        #logContents = io.readFileData(logFilesPath + '/' + value)
        self.logContents.set(io.readFileData(self.logFilesPath + '/' + value))

        if self.logContents.get() != None and self.logContents.get():
            self.updateScrolledText(self.scrolledText, self.logContents.get())

        
        #notebook.add(logFrame, text='Log')


if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()