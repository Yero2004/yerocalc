import tkinter as tk                       # Load the Library

#-----FUNCTIONS-----#
def gets_calculations(value):
    entry.config(state="normal")           # Unlocks

    current_text = entry.get()
    if current_text == "Error":            # Deletes After Error
        entry.delete(0, tk.END) 
  
    entry.insert(tk.END, value)            # Makes buttons work

    entry.config(state="readonly")         # Locks


def does_calculations():
    entry.config(state="normal")           # Unlocks

    try:
        expression = entry.get()           # Get what's in the entry box (e.g. "12+3")
        result = eval(expression)          # Evaluate it (does the math)
        entry.delete(0, tk.END)            # Clear the box
        entry.insert(0, result)            # Show the result
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error") 

    entry.config(state="readonly")         # Locks

def clears():
    entry.config(state="normal")           # Unlocks
 
    entry.delete(0, tk.END)

    entry.config(state="readonly")         # Locks

window = tk.Tk()                                                 # Create the Window
window.title("YeroCalc")                                         # Give it a Title
window.geometry("350x460")                                       # Set its Size


#-----MAKES THE SPACING OP-----#
#Number of Columns
for i in range(4):  
    window.columnconfigure(i, weight = 1, uniform = "equal")
#Number of Rows
for i in range(6): 
    window.rowconfigure(i, weight = 1, uniform = "equal")

#-----ENTRY-----#
entry = tk.Entry(window, width = 20, borderwidth = 5, relief = "ridge", justify = "right", font = ("Arial", 24))
entry.grid(row = 0, column = 0, columnspan=4, padx = 10, pady = 10, ipady = 10)

entry.config(state="readonly")

#-----BUTTONS-----# (0-9)
buttons1 = tk.Button(window, text = "1", command = lambda: gets_calculations("1"))
buttons1.grid (row = 1, column = 0, padx = 4, pady = 4, sticky = "nsew")

buttons2 = tk.Button(window, text = "2", command = lambda: gets_calculations("2"))
buttons2.grid (row = 1, column = 1, padx = 4, pady = 4, sticky = "nsew")

buttons3 = tk.Button(window, text = "3", command = lambda: gets_calculations("3"))
buttons3.grid (row = 1, column = 2, padx = 4, pady = 4, sticky = "nsew")

buttons4 = tk.Button(window, text = "4", command = lambda: gets_calculations("4"))
buttons4.grid (row = 2, column = 0, padx = 4, pady = 4, sticky = "nsew")

buttons5 = tk.Button(window, text = "5", command = lambda: gets_calculations("5"))
buttons5.grid (row = 2, column = 1, padx = 4, pady = 4, sticky = "nsew")

buttons6 = tk.Button(window, text = "6", command = lambda: gets_calculations("6"))
buttons6.grid (row = 2, column = 2, padx = 4, pady = 4, sticky = "nsew")

buttons7 = tk.Button(window, text = "7", command = lambda: gets_calculations("7"))
buttons7.grid (row = 3, column = 0, padx = 4, pady = 4, sticky = "nsew")

buttons8 = tk.Button(window, text = "8", command = lambda: gets_calculations("8"))
buttons8.grid (row = 3, column = 1, padx = 4, pady = 4, sticky = "nsew")

buttons9 = tk.Button(window, text = "9", command = lambda: gets_calculations("9"))
buttons9.grid (row = 3, column = 2, padx = 4, pady = 4, sticky = "nsew")

buttons0 = tk.Button(window, text = "0", command = lambda: gets_calculations("0"))
buttons0.grid (row = 4, column = 1, padx = 4, pady = 4, sticky = "nsew")

#-----BUTTONS-----# (Symbols) bg = "blue"

divide = tk.Button(window, text = "/", command = lambda: gets_calculations("/"))
divide.grid (row = 1, column = 3, padx = 4, pady = 4, sticky = "nsew")

multiplication = tk.Button(window, text = "*", command = lambda: gets_calculations("*"))
multiplication.grid (row = 2, column = 3, padx = 4, pady = 4, sticky = "nsew")

addition = tk.Button(window, text = "-", command = lambda: gets_calculations("-"))
addition.grid (row = 3, column = 3, padx = 4, pady = 4, sticky = "nsew")

subtraction = tk.Button(window, text = "+", command = lambda: gets_calculations("+"))
subtraction.grid (row = 4, column = 3, padx = 4, pady = 4, sticky = "nsew")

parentaces = tk.Button(window, text = "(", command = lambda: gets_calculations("("))
parentaces.grid (row = 4, column = 0, padx = 4, pady = 4, sticky = "nsew")

parentaces2 = tk.Button(window, text = ")", command = lambda: gets_calculations(")"))
parentaces2.grid (row = 4, column = 2, padx = 4, pady = 4, sticky = "nsew")

equals = tk.Button(window, text = "=", command = lambda: does_calculations())
equals.grid(row = 5, column = 2, columnspan = 2, padx=4, pady=4, sticky = "nsew")

clear = tk.Button(window, text = "Clear", command = lambda: clears())
clear.grid(row = 5, column = 0, columnspan = 2, padx=4, pady=4, sticky = "nsew")

window.mainloop()                            # Keep The Window Open

