"""
gui.py
GUI to handle user inputs and setup using Tkinter.
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.colorchooser as colour
import os
import subprocess
import setup

'''Still editing inputting file list of svg's '''
#Finds all svg files in directory
dirname = os.getcwd()

filedir = dirname + '/sgvFiles' #yes svg is spelt wrong ;)
file_list = os.listdir(filedir)
DEFAULT_CONSTANTS_FILE_PATH = dirname + '/constants_defaults.py'


# convert cm to pixels
PIXELS_PER_CM = 267/2.54 #different resolution on 3D printer thingy
height_in_cm = 2.5
width_in_cm = 8.5

height_in_pixels = int(height_in_cm * PIXELS_PER_CM)
width_in_pixels = int(width_in_cm * PIXELS_PER_CM)

# create the tkinter window
root = tk.Tk()
root.geometry(f"{width_in_pixels}x{height_in_pixels}")

label = tk.Label(root, text="XY-Plotter GUI")
label.pack()

# Create notebook
notebook = ttk.Notebook(root, width=width_in_pixels, height=height_in_pixels)
notebook.pack(fill = 'both', expand=True)

# Create main frame
mainFrame = tk.Frame(notebook, width=width_in_pixels, height=height_in_pixels - 20)
mainFrame.pack(fill='both', expand=True)

# create a listbox with items in file_list for svg files
listbox = tk.Listbox(mainFrame, selectmode=tk.SINGLE, width=100, height=1)
for filename in file_list:
    listbox.insert(tk.END, filename)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

# function to save the selected file in the list
def save_selection():
    selection = listbox.curselection()
    if selection:
        global selected_file
        selected_file = listbox.get(selection)
        mb.showinfo(title="SUCCESS", message='File successfully saved!')
    else:
        mb.showwarning(title="WARNING", message='Ensure that you have first selected a file!')

# create a button to save the selection of the file
savebutton = tk.Button(mainFrame, text='Save selection', command=save_selection)
savebutton.pack()


# Run main.py with the given selection
def run_selection():
    """ Function to run the main.py file with the given gui parameter """
    
    # Check if a file has been saved
    try:
        # Define file path format to save in constants.py 
        filePath = '\"sgvFiles/' + selected_file + '\"'
    except NameError as e:
        mb.showwarning(title="WARNING", message='Ensure that you have first saved a selection!')
        return

    # Save filePath in constants.py
    if setup.setVariable(setup.ConstantVariable('FILE', filePath, '   # Source file for plotting')):
        try:
            subprocess.run(['python3', 'main.py', 'gui'])
        except Exception as e:
            print(e)
    

# Button to execute run_selection()
previewButton = tk.Button(mainFrame, text='Show Preview', command=run_selection)
previewButton.pack()


# Create variable changer tab
def implement_Variables(frame):
    """ Function to add required variables to create a variable change interface in the given frame """
    # frame - tk.Frame object - the frame to add objects to.
    
    variableDict = dict()
    variableObjects = dict()
    varlist = setup.getVariables()


    def scaleFunc(event):
        """ Function to call when a scale object is adjusted """
        
        widget = event.widget
        value = widget.get()
        var = variableDict[widget.cget('label')]

        setup.setVariable(setup.ConstantVariable(var.getName(), value, var.getComment()))

    def checkFunc(event):
        """ Function to call when checkbutton object is pressed """

        widget = event.widget
        value = widget.instate(['!selected'])
        var = variableDict[widget.cget('text')]

        setup.setVariable(setup.ConstantVariable(var.getName(), value, var.getComment()))

    def colourFunc(event):
        """ Function to call when button to create colour chooser is pressed """
        
        widget = event.widget
        var = variableDict[widget.winfo_name().upper()]
        colour.Chooser(frame, label=var.getName()) # Create colour picker
        selected_colour = colour.askcolor()

        if selected_colour[0] != None: setup.setVariable(setup.ConstantVariable(var.getName(), selected_colour[0], var.getComment()))

    
    # For each changeable variable in constants.py
    for var in varlist:
        variableDict[var.getName()] = var

        if var.getType() in [int, float]:
            """ If variable is of type int or float, create a scale object """
            # Note: floats with increments not implemented yet

            # Create Scale object
            variableObjects[var.getName()] = tk.Scale(frame, label=var.getName(), from_= var.getMin(), to= var.getMax(), orient='horizontal')
            variableObjects[var.getName()].set(var.getValue()) # Set current value as saved value
            variableObjects[var.getName()].bind("<ButtonRelease-1>", scaleFunc) # Add function
            variableObjects[var.getName()].pack(fill='x') # Fill scale along x axis

        if var.getType() in [bool]:
            """ If variable is of type bool, create a checkbutton object """

            #Create Checkbutton object
            variableObjects[var.getName()] = ttk.Checkbutton(frame, text=var.getName())
            variableObjects[var.getName()].invoke() # Used to update state when variables are reset
            variableObjects[var.getName()].bind("<ButtonRelease-1>", checkFunc) # Add function
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
            variableObjects[var.getName()].bind("<ButtonRelease-1>", colourFunc) # Add function to button
            variableObjects[var.getName()].pack(fill='x') # Fill scale along x axis


    def verify():
        """ Function to check whether the user truly wishes to reset variables or not """
        # Note: reset also changes comment
        # Note: can be generalised, but no requirement as of creation

        # Create message box to inquire about user's true intention
        if mb.askyesno(title='Continue?', message='Are you sure you want to reset values to defaults?'):
            # Get default variable values 
            defaultObjects = setup.getVariables(filePath=DEFAULT_CONSTANTS_FILE_PATH)

            for var in defaultObjects:
                setup.setVariable(var) # Save each variable as default

            change_variables() # Re-create variable changer tab

    # Create button to reset values
    defaultsButton = tk.Button(frame, text="Reset to Default?", command=verify)
    defaultsButton.pack(side=tk.RIGHT)


def change_variables():
    """ Function to create scrolling tab within notebook to contain variable changing objects """
    
    # Frame created for new tab
    tabFrame = tk.Frame(notebook, width=width_in_pixels, height=height_in_pixels, name='variables')
    tabFrame.pack(fill='both', expand=True)

    # Canvas created to allow for scrolling
    scrollableCanvas = tk.Canvas(tabFrame)
    scrollableCanvas.pack(fill='both', expand=True)

    # Create scrollbar
    scrollBar = tk.Scrollbar(scrollableCanvas, orient='vertical', command=scrollableCanvas.yview)
    scrollBar.pack(fill=tk.Y, side=tk.RIGHT)

    # Configure scrollbar to the canvas
    scrollableCanvas.configure(yscrollcommand=scrollBar.set)
    scrollableCanvas.bind('<Configure>', lambda e: scrollableCanvas.configure(scrollregion=scrollableCanvas.bbox("all")))

    # Create frame that will be scrolled
    # This will contain all variable changing objects
    variableFrame = tk.Frame(scrollableCanvas)
    scrollableCanvas.create_window(0, 0, window=variableFrame, anchor='nw', width=width_in_pixels) # Add frame to canvas

    # Add variable changer objects to given frame
    implement_Variables(variableFrame)
    
    # Add notebook tab
    notebook.add(tabFrame, text='Variables')
    

# Create button to create new change variable tab
changeButton = tk.Button(mainFrame, text='Change Variables', command=change_variables)
changeButton.pack()


def exitGui():
    """ Function to ask user about intention to quit """

    if mb.askyesno(title='Quit?', message='Are you sure you want to quit?'):
        root.quit()

# Create button to quit
quitButton = tk.Button(mainFrame, text='Quit', command=exitGui)
quitButton.pack()

# Add main notebook tab
notebook.add(mainFrame, text='Menu')

# Keep the gui open
root.mainloop()