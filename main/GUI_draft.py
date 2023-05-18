import tkinter as tk
import os

'''Still editing inputting file list of svg's '''
#FInds all svg files in directory
dirname = os.getcwd()

filedir = dirname + '\sgvFiles' #yes svg is spelt wrong ;)
file_list = os.listdir(filedir)


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

# create a listbox with items in file_list for svg files
listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=100, height=1)
for filename in file_list:
    listbox.insert(tk.END, filename)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

# function to save the selected file in the list
def save_selection():
    selection = listbox.curselection()
    if selection:
        global selected_file
        selected_file = listbox.get(selection)

# create a button to save the selection of the file
button = tk.Button(root, text='Save selection', command=save_selection)
button.pack()

root.mainloop()

print(selected_file)
