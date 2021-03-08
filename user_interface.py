# File for tkinter User Interface
import tkinter as tk
from tkinter import ttk

def retrieve():
    val = statechoosen.get()
    print(val)

root = tk.Tk()
root.title("CS122 TJJE Project: Examining State Policies and Educational Outcomes")
root.geometry("400x400")

ttk.Label(root, text = "Select a US state: ",  
        font = ("Times New Roman", 10)).grid(column = 1,  
        row = 15, padx = 10, pady = 25) 

n = tk.StringVar() 
statechoosen = ttk.Combobox(root, width = 27,  
                            textvariable = n)

statechoosen['values'] = ("AL", "AL", "AR" "fill rest in") 

button = tk.Button(root, text="retrieve", bd = "5", command=retrieve)
button.grid(column = 1, row = 25)
statechoosen.grid(column = 2, row = 15) 
root.mainloop()
