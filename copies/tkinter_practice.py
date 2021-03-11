# tkinter_practice.py

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import tkinter as tk

from tkinter import ttk
import pandas as pd
nces_final = pd.read_csv("csv/nces_final.csv")


from ui_util import VerticalScrolledFrame


states = ["US", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

outcomes = list(nces_final.columns)

class Window1:
    def __init__(self, root):
        self.screen_width = root.winfo_screenwidth()
        self.screen_height= root.winfo_screenheight()
        self.frame = VerticalScrolledFrame(
            root, 
            bg="white",
            cursor="arrow",
            height= self.screen_height,
            width= self.screen_width
        )
        self.frame.pack(side="top", fill="both", expand=True)
        self.welcome_frame()
        self.default_opt_frame()
        self.fws_nondefault_frame()
        self.special_opt_frame()
        self.scrollbar()
    
    def welcome_frame(self):
        welcome_frame = tk.Frame(self.frame, bg = "pink")
        welcome_frame.grid(column = 0, row = 0)
        welcome_text_box = tk.Text(welcome_frame, height = 12, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        welcome_text_box.grid(column = 0, row = 0)
        intro = "Hello and welcome to our program! This tool will allow you to evaluate the effectivness and correlations of American educational policies on its outcomes, on a per state, per outcome, or per policy basis"
        sources = "We ulilize data from the National Council on Teacher Quality (NCTQ) and the National Center for Education Statistics (NCES)"
        note = "*For a small number of missing datapoints, we filled them in with the US national average"
        welcome_text_box.insert(tk.END, intro + "\n"*2 + sources + "\n"*2 + note)
        welcome_text_box.configure(state='disabled')
    
    def default_opt_frame(self):
        default_opt_frame = tk.Frame(self.frame, bg = "dark blue")
        default_opt_frame.grid(column = 0, row = 1)
        option1_label = ttk.Label(default_opt_frame, text = "Option 1 Retrieve information on how effective a state's relevant policies are for all or particular educational outcomes: ").grid(column = 0,  
        row = 0, padx = 35, pady = 25)
        # State Selection Label
        state_label = ttk.Label(default_opt_frame, text = "Select one state, or select multiple to compare").grid(column = 0,  
                row = 1, padx = 35, pady = 25) 

        # State Selection listbox widget
        self.state_listbox = tk.Listbox(default_opt_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
        self.state_listbox.grid(column = 0, row = 2)
        # Adding scrollbar to listbox
        state_scrollbar = tk.Scrollbar(default_opt_frame)
        state_scrollbar.config(command=self.state_listbox.yview)
        self.state_listbox.config(yscrollcommand=state_scrollbar.set)
        state_scrollbar.grid(column=1, row=2, sticky='NSW')

        # Populating scrollbar
        for i, state in enumerate(states): 
    
            self.state_listbox.insert(tk.END, state) 
            self.state_listbox.itemconfig(i, bg = "deep sky blue")
        
        # Calculate Button
        button = tk.Button(default_opt_frame, text="Calculate!", bd = "5", command=self.retrieve1)
        button.grid(column = 3, row = 2)
    
    def fws_nondefault_frame(self):
        fws_nondefault_frame = tk.Frame(self.frame, bg = "purple")
        fws_nondefault_frame.grid(column = 0, row = 2)
        # Label 
        option2_label = ttk.Label(fws_nondefault_frame, text = "Option 2 Retrieve information on how effective a state's relevant policies are for all or particulr educational outcomes: ").grid(column = 0,  
        row = 0, padx = 35, pady = 25)

        # List box widget
        self.state2_listbox = tk.Listbox(fws_nondefault_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
        self.state2_listbox.grid(column = 0, row = 2)
        # Adding scrollbar to listbox
        state_scrollbar = tk.Scrollbar(fws_nondefault_frame)
        state_scrollbar.config(command=self.state2_listbox.yview)
        self.state2_listbox.config(yscrollcommand=state_scrollbar.set)
        state_scrollbar.grid(column=1, row=2, sticky='NSW')

        # Populating scrollbar
        for i, state in enumerate(states): 
    
            self.state2_listbox.insert(tk.END, state) 
            self.state2_listbox.itemconfig(i, bg = "deep sky blue")

        ## Outcomes selection listbox widget
        outcomes2_label = ttk.Label(fws_nondefault_frame, text = "Select the outcomes you want to investigate:").grid(column = 1,  
        row = 1, padx = 35, pady = 25) 
        # outcomes Selection listbox widget
        self.outcomes2_listbox = tk.Listbox(fws_nondefault_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
        self.outcomes2_listbox.grid(column = 1, row = 2)
        # Adding scrollbar to listbox
        outcomes2_scrollbar = tk.Scrollbar(fws_nondefault_frame)
        outcomes2_scrollbar.config(command=self.outcomes2_listbox.yview)
        self.outcomes2_listbox.config(yscrollcommand=outcomes2_scrollbar.set)
        outcomes2_scrollbar.grid(column=2, row=2, sticky='NSW')

        # Adding calculate button widget 
        button = tk.Button(fws_nondefault_frame, text="Calculate!", bd = "5", command=self.retrieve2)
        button.grid(column = 2, row = 2)

        for i, outcome in enumerate(outcomes): 
      
            self.outcomes2_listbox.insert(tk.END, outcome) 
            self.outcomes2_listbox.itemconfig(i, bg = "deep sky blue")
"""
    def special_opt_frame(self):
        special_opt_frame = tk.Frame(self.frame, bg = "green")
        special_opt_frame.grid(column = 0, row = 3)
        # Label 
        option3_label = ttk.Label(special_opt_frame, text = "Option 3 Retrieve information on how effective a state's relevant policies are for all or particulr educational outcomes: ").grid(column = 0,  
        row = 0, padx = 35, pady = 25)

        # List box widget
        self.state3_listbox = tk.Listbox(special_opt_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
        self.state3_listbox.grid(column = 0, row = 3)
        # Adding scrollbar to listbox
        state_scrollbar = tk.Scrollbar(special_opt_frame)
        state_scrollbar.config(command=self.state3_listbox.yview)
        self.state3_listbox.config(yscrollcommand=state_scrollbar.set)
        state_scrollbar.grid(column=1, row=2, sticky='NSW')

        # Populating scrollbar
        for i, state in enumerate(states): 
    
            self.state3_listbox.insert(tk.END, state) 
            self.state3_listbox.itemconfig(i, bg = "deep sky blue")

        ## Outcomes selection listbox widget
        outcomes3_label = ttk.Label(special_opt_frame, text = "Select the outcomes you want to investigate:").grid(column = 1,  
        row = 1, padx = 35, pady = 25) 
        # outcomes Selection listbox widget
        self.outcomes3_listbox = tk.Listbox(special_opt_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
        self.outcomes3_listbox.grid(column = 1, row = 2)
        # Adding scrollbar to listbox
        outcomes3_scrollbar = tk.Scrollbar(special_opt_frame)
        outcomes3_scrollbar.config(command=self.outcomes3_listbox.yview)
        self.outcomes3_listbox.config(yscrollcommand=special_opt_frame.set)
        outcomes3_scrollbar.grid(column=2, row=2, sticky='NSW')

        # Adding calculate button widget 
        button = tk.Button(special_opt_frame, text="Calculate!", bd = "5", command=self.retrieve3)
        button.grid(column = 2, row = 2)

        for i, outcome in enumerate(outcomes): 
      
            self.outcomes3_listbox.insert(tk.END, outcome) 
            self.outcomes3_listbox.itemconfig(i, bg = "deep sky blue")
"""
    def scrollbar(self):
        scrollbar = tk.Scrollbar(self.frame)
        return scrollbar
        #scrollbar.pack(side="right", fill="y")
    
    def retrieve1(self):
        states = [self.state_listbox.get(idx) for idx in self.state_listbox.curselection()]
        #outcomes = [outcomes_listbox.get(idx) for idx in outcomes_listbox.curselection()]
        print("states" + str(states))
        #print("outcomes" + str(outcomes))
        self.new_window1(states)

    def retrieve2(self):
        states = [self.state2_listbox.get(idx) for idx in self.state2_listbox.curselection()]
        outcomes = [self.outcomes2_listbox.get(idx) for idx in self.outcomes2_listbox.curselection()]
        print("states" + str(states))
        print("outcomes" + str(outcomes))
        self.new_window2(states, outcomes)

    def retrieve3(self, outcomes_combobox, policies_listbox):
        outcome = outcomes_combobox.get()
        policies = [policies_listbox.get(idx) for idx in policies_listbox.curselection()]
        print("outcome: " + str(outcome))
        print("policies" + str(policies))
    
    def new_window1(self, states):
        self.newWindow1 = tk.Toplevel(self.frame)
        self.output1 = Output1(self.newWindow1, states)

    def new_window2(self, states, outcomes):
        self.newWindow2 = tk.Toplevel(self.frame)
        self.output2 = Output2(self.newWindow2, states, outcomes)



class Output1:
    def __init__(self, master, states):
        self.master = master
        self.states = states
        self.frame = VerticalScrolledFrame(
            master, 
            bg="white",
            cursor="arrow",
            height= 1000,
            width= 1000
        )
        self.show_states()
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.grid(column = 1, row = 3)
        self.frame.pack()
    
    def show_states(self):
        state_text = tk.Text(self.frame, height = 12, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        state_text.grid(column = 1, row = 0)
        state_text.insert(tk.END, " ".join(self.states))
        state_text.configure(state='disabled')

    def close_windows(self):
        self.master.destroy()

class Output2:
    def __init__(self, master, states, outcomes):
        self.master = master
        self.states = states
        self.outcomes = outcomes
        self.frame = VerticalScrolledFrame(
            master, 
            bg="white",
            cursor="arrow",
            height= 1000,
            width= 1000
        )
        self.show_states()
        self.show_outcomes()
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.grid(column = 1, row = 3)
        self.frame.pack()
    
    def show_states(self):
        state_text = tk.Text(self.frame, height = 12, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        state_text.grid(column = 1, row = 0)
        state_text.insert(tk.END, " ".join(self.states))
        state_text.configure(state='disabled')

    def show_outcomes(self):
        outcome_text = tk.Text(self.frame, height = 12, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        outcome_text.grid(column = 1, row = 1)
        outcome_text.insert(tk.END, " ".join(self.outcomes))
        outcome_text.configure(state='disabled')

    def close_windows(self):
        self.master.destroy()

def main(): #run mianloop 
    root = tk.Tk()
    root["bg"] = "white"
    #getting screen width and height of display 
    screen_width = root.winfo_screenwidth()  #in pixels
    screen_height= root.winfo_screenheight() #in pixels
    #setting tkinter window size 
    root.geometry("%dx%d" % (screen_width, screen_height))
    root.title("CS122 TJJE Project: Examining State Policies and Educational Outcomes")
    app = Window1(root)
    root.mainloop()

if __name__ == '__main__':
    main()