# tkinter_practice.py

import tkinter as tk
from tkinter import ttk
import pandas as pd
import os

#import nces
import nctq
import output1
import output2
import default_stat_analysis as dsa
from ui_util import VerticalScrolledFrame

# Import the nces data
nces_final = pd.read_csv("csv/nces_final.csv", index_col=0)
nces_trends = nces_final[[col for col in nces_final.columns if col.startswith("Trend")]]
nces_original = pd.read_csv("csv/nces_raw.csv", index_col=0)

# Import the nctq data
nctqdic_original = {}
for filename in os.listdir("csv/"):
    if filename.startswith("nctq"):
        nctqdic_original[filename.strip(".csv")] = pd.read_csv("csv/{}".format(filename), index_col = 0)
nctqdic_filled = nctq.fill_na(nctqdic_original)
avg_nctq = nctq.average_df(nctqdic_filled).sort_index()  
centered_avg_nctq = nctq.center_df(avg_nctq)

# Run function to get scores for Option 1 (so this never needs to be run again)
R2 = 0.1 # change this in function call as needed, this is just a placeholder
states_score_dict, state_to_pols_score_dict= dsa.default_calc(
        avg_nctq, centered_avg_nctq, nces_trends, R2, block_negative=True, outcomes=None
    )


states = ["US", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

outcomes = list(nces_final.columns)
trend_outcomes = list(nces_trends.columns)

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
        #welcome_frame.grid(column = 0, row = 0)
        welcome_frame.pack(expand=True, fill='x')
        welcome_text_box = tk.Text(welcome_frame, height = 12, bg = "pink", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        welcome_text_box.grid(column = 0, row = 0)
        intro = "Hello and welcome to our program! This tool will allow you to evaluate the effectivness and correlations of American educational policies on its outcomes, on a per state, per outcome, or per policy basis"
        sources = "We ulilize data from the National Council on Teacher Quality (NCTQ) and the National Center for Education Statistics (NCES)"
        note = "*For a small number of missing datapoints, we filled them in with the US national average"
        welcome_text_box.insert(tk.END, intro + "\n"*2 + sources + "\n"*2 + note)
        welcome_text_box.configure(state='disabled')
    
    def default_opt_frame(self):
        default_opt_frame = tk.Frame(self.frame, bg = "dark blue")
        default_opt_frame.pack(expand=True, fill='x')
        #grid(column = 0, row = 1)
        option1_label = ttk.Label(default_opt_frame, text = "Option 1 Retrieve information on how effective a state's relevant policies are for all or particular educational outcomes: ").grid(column = 0,  
        row = 0, padx = 35, pady = 25, columnspan = 3)
        # State Selection Label
        state_label = ttk.Label(default_opt_frame, text = "Select one state, or select multiple to compare").grid(column = 0,  
                row = 1, padx = 35, pady = 25, columnspan=2) 

        # State Selection listbox widget
        self.state_listbox = tk.Listbox(default_opt_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
        self.state_listbox.grid(column = 0, row = 2, sticky="E")
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
        button = tk.Button(default_opt_frame, text="Calculate!", bd = "5", command = lambda: self.retrieve1(states_score_dict, state_to_pols_score_dict))
        #command=self.retrieve1)
        button.grid(column = 2, row = 2)
    
    def fws_nondefault_frame(self):
        fws_nondefault_frame = tk.Frame(self.frame, bg = "purple")
        fws_nondefault_frame.pack(expand=True, fill='x')
        #grid(column = 0, row = 2)
        # Label 
        option2_label = ttk.Label(fws_nondefault_frame, text = "Option 2: Recalculate state scores by specifying particular outcome variables").grid(column = 0,  
        row = 0, padx = 35, pady = 25, columnspan = 2, sticky="W")
        state_label = ttk.Label(fws_nondefault_frame, text = "Select one state, or select multiple to compare").grid(column = 0,  
                row = 1, padx = 35, pady = 25, columnspan=2)

        # List box widget
        self.state2_listbox = tk.Listbox(fws_nondefault_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
        self.state2_listbox.grid(column = 0, row = 2, sticky="E")
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
        outcomes2_label = ttk.Label(fws_nondefault_frame, text = "Select the outcomes you want to investigate:").grid(column = 2,  
        row = 1, padx = 35, pady = 25, columnspan=2) 
        # outcomes Selection listbox widget
        self.outcomes2_listbox = tk.Listbox(fws_nondefault_frame, selectmode = "multiple", exportselection = False, width=35, height=10)
        self.outcomes2_listbox.grid(column = 2, row = 2, sticky="E")
        # Adding scrollbar to listbox
        outcomes2_scrollbar = tk.Scrollbar(fws_nondefault_frame)
        outcomes2_scrollbar.config(command=self.outcomes2_listbox.yview)
        self.outcomes2_listbox.config(yscrollcommand=outcomes2_scrollbar.set)
        outcomes2_scrollbar.grid(column=3, row=2, sticky='NSW')

        # Adding calculate button widget 
        button = tk.Button(fws_nondefault_frame, text="Calculate!", bd = "5", command=self.retrieve2)
        button.grid(column = 4, row = 2)

        for i, outcome in enumerate(trend_outcomes): 
    
            self.outcomes2_listbox.insert(tk.END, outcome) 
            self.outcomes2_listbox.itemconfig(i, bg = "deep sky blue")
    
    def special_opt_frame(self):
        special_opt_frame = tk.Frame(self.frame, bg = "green")
        special_opt_frame.pack(expand=True, fill='x')
        #grid(column = 0, row = 3)
        # Label 
        option3_label = ttk.Label(special_opt_frame, text = "Retrieve information on how particular policies interact with a given outcome: ").grid(column = 0,  
        row = 0, padx = 35, pady = 25)

        ttk.Label(special_opt_frame, text = "Select one outcome to investigate:").grid(column = 0,  
                row = 1, padx = 35, pady = 25)
        outcome_combo = tk.StringVar() 
        self.outcomes_combobox = ttk.Combobox(special_opt_frame, width = 27,  
                                    textvariable = outcome_combo, exportselection=0)
        self.outcomes_combobox['values'] = outcomes 
        self.outcomes_combobox.grid(column = 0, row = 2) 

        # policies selection label
        policies_label = ttk.Label(special_opt_frame, text = "Select which policies to consider:").grid(column = 1,  
                row = 1, padx = 35, pady = 25, columnspan = 2) 

        # policies Selection listbox widget
        self.policies3_listbox = tk.Listbox(special_opt_frame, selectmode = "multiple", exportselection = False, width=35, height=10)
        self.policies3_listbox.grid(column = 1, row = 2, sticky="E")

        # Adding scrollbar to listbox
        policies3_scrollbar = tk.Scrollbar(special_opt_frame)
        policies3_scrollbar.config(command=self.policies3_listbox.yview)
        self.policies3_listbox.config(yscrollcommand=policies3_scrollbar.set)
        policies3_scrollbar.grid(column=2, row=2, sticky='NSW')

        # Adding scrollbar to listbox
        policies3_scrollbarh = tk.Scrollbar(special_opt_frame)
        policies3_scrollbarh.config(command=self.policies3_listbox.xview)
        self.policies3_listbox.config(xscrollcommand=policies3_scrollbarh.set)
        policies3_scrollbarh.grid(column=1, row=3, sticky='NWE')

         # Adding calculate button widget 
        button = tk.Button(special_opt_frame, text="Calculate!", bd = "5", command=self.retrieve3)
        button.grid(column = 4, row = 2)

        for i, outcome in enumerate(outcomes): 
      
            self.policies3_listbox.insert(tk.END, outcome) 
            self.policies3_listbox.itemconfig(i, bg = "deep sky blue") 
        

    def scrollbar(self):
        scrollbar = tk.Scrollbar(self.frame)
        return scrollbar
        #scrollbar.pack(side="right", fill="y")
    
    def retrieve1(self, states_score_dict, state_to_pols_score_dict):
        states = [self.state_listbox.get(idx) for idx in self.state_listbox.curselection()]
        outcomes = list(nces_trends.columns)
        return_dict = {}
        for state in states:
            score, best_pol, worst_pol = dsa.get_scores(states_score_dict, state_to_pols_score_dict, state)
            return_dict[state] = [score, best_pol, worst_pol]
        print("states" + str(states))
        # for testing purposes
        return_dict = {"IL": [50, "Pay Scales (Retaining Effective Teachers Policy)", "	Academic Requirements (Early Childhood Preparation Policy)"], 
        "CA": [75, "Pension Flexibility (Retaining Effective Teachers Policy)", "Induction (Retaining Effective Teachers Policy)"]}
        self.new_window1(return_dict, outcomes)


    def retrieve2(self):
        states = [self.state2_listbox.get(idx) for idx in self.state2_listbox.curselection()]
        outcomes = [self.outcomes2_listbox.get(idx) for idx in self.outcomes2_listbox.curselection()]
        states_score_dict, state_to_pols_score_dict = dsa.default_calc(
                avg_nctq, centered_avg_nctq, nces_trends, R2, block_negative=True, outcomes=False
            )   
        return_dict = {}    
        for state in states:
            score, best_pol, worst_pol = dsa.get_scores(states_score_dict, state_to_pols_score_dict, state)
            return_dict[state] = [score, best_pol, worst_pol]
        print("states" + str(states))
        print("outcomes" + str(outcomes))
        # for testing purposes
        return_dict = {"IL": [50, "Pay Scales (Retaining Effective Teachers Policy)", "	Academic Requirements (Early Childhood Preparation Policy)"], 
        "CA": [75, "Pension Flexibility (Retaining Effective Teachers Policy)", "Induction (Retaining Effective Teachers Policy)"]}
        self.new_window1(return_dict, outcomes)


    def retrieve3(self):
        outcome = self.outcomes_combobox.get()
        policies = [self.policies3_listbox.get(idx) for idx in self.policies3_listbox.curselection()]
        print("outcome: " + str(outcome))
        print("policies" + str(policies))
        self.new_window2(outcome, policies)
    

    def new_window1(self, return_dict, outcomes):
        self.newWindow1 = tk.Toplevel(self.frame)
        self.output1 = output1.Output1(self.newWindow1, return_dict, outcomes)


    def new_window2(self, outcome, policies):
        self.newWindow2 = tk.Toplevel(self.frame)
        self.output2 = output2.Output2(self.newWindow2, outcome, policies)


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