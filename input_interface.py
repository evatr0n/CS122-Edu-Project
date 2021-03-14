# main function: run this to run our software!

import tkinter as tk
from tkinter import ttk
import pandas as pd
import os

import nctq
import output1
import output2
import default_stat_analysis as dsa
import basic_regression as b
from ui_util import VerticalScrolledFrame
from ui_util import NewWindow

# Import the nces data
nces_final = pd.read_csv("csv/nces_final.csv", index_col = 0)
nces_trends = nces_final[[col for col in nces_final.columns if col.startswith("Trend")]]
nces_original = pd.read_csv("csv/nces_raw.csv", index_col = 0)

# Import the nctq data
nctqdic_original = {}
for filename in os.listdir("csv/"):
    if filename.startswith("nctq"):
        nctqdic_original[filename.strip(".csv")] = pd.read_csv("csv/{}".format(filename), index_col = 0)
nctqdic_filled = nctq.fill_na(nctqdic_original)
avg_nctq = nctq.average_df(nctqdic_filled).sort_index()  
centered_avg_nctq = nctq.center_df(avg_nctq)

# Run function to get scores for Option 1 (so this never needs to be run again)
R2 = 0.1 
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
        """
        Constructor for the window class that takes in a tkinter root object
        """
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
        self.r2_cutoff_frame()
        self.bottom_frame()
    

    def welcome_frame(self):
        """
        Function that creates the topmost frame in the UI, which includes a short description of our tool
        """
        welcome_frame = tk.Frame(self.frame, bg = "pink")
        welcome_frame.pack(expand=True, fill='x')
        welcome_text_box = tk.Text(welcome_frame, height = 12, bg = "pink", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        welcome_text_box.grid(column = 0, row = 0)
        intro = "Hello and welcome to our program! This tool will allow you to evaluate the effectivness and correlations of American educational policies on its outcomes, on a per state, per outcome, or per policy basis"
        sources = "We ulilize data from the National Council on Teacher Quality (NCTQ) and the National Center for Education Statistics (NCES)"
        note = "*For a small number of missing datapoints, we filled them in with the US national average"
        welcome_text_box.insert(tk.END, intro + "\n"*2 + sources + "\n"*2 + note)
        welcome_text_box.configure(state='disabled')
    

    def default_opt_frame(self):
        """
        Function that creates the frame that holds the first user input option, which allows for state seletion
        """
        default_opt_frame = tk.Frame(self.frame, bg = "dark blue")
        default_opt_frame.pack(expand=True, fill='x')

        option1_label = ttk.Label(default_opt_frame, text = "Option 1 Retrieve information on how effective a state's relevant policies are in relation to all available educational outcomes: ").grid(column = 0,  
        row = 0, padx = 35, pady = 25, columnspan = 3)
        state_label = ttk.Label(default_opt_frame, text = "Select one state, or select multiple to compare").grid(column = 0,  
                row = 1, padx = 35, pady = 25, columnspan=2) 

        # State Selection listbox widget
        self.state_listbox = tk.Listbox(default_opt_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
        self.state_listbox.grid(column = 0, row = 2, sticky="E", pady = 25)

        # Adding scrollbar to listbox
        state_scrollbar = tk.Scrollbar(default_opt_frame)
        state_scrollbar.config(command=self.state_listbox.yview)
        self.state_listbox.config(yscrollcommand=state_scrollbar.set)
        state_scrollbar.grid(column=1, row=2, sticky='NSW', pady = 25)

        # Populating scrollbar
        for i, state in enumerate(states): 
    
            self.state_listbox.insert(tk.END, state) 
            self.state_listbox.itemconfig(i, bg = "deep sky blue")

        # Calculate Button
        button = tk.Button(default_opt_frame, text="Calculate!", bd = "5", command = lambda: self.retrieve1(states_score_dict, state_to_pols_score_dict))
        button.grid(column = 2, row = 2)
    
    def fws_nondefault_frame(self):
        """
        Function that creates the frame that holds the second user input option, which allows for state and outcome variable seletion
        """
        fws_nondefault_frame = tk.Frame(self.frame, bg = "purple")
        fws_nondefault_frame.pack(expand=True, fill='x')

        option2_label = ttk.Label(fws_nondefault_frame, text = "Option 2: Recalculate state scores by specifying particular outcome variables").grid(column = 0,  
        row = 0, padx = 35, pady = 25, columnspan = 2, sticky="W")
        state_label = ttk.Label(fws_nondefault_frame, text = "Select one state, or select multiple to compare").grid(column = 0,  
                row = 1, padx = 35, pady = 25, columnspan=2)

        # List box widget
        self.state2_listbox = tk.Listbox(fws_nondefault_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
        self.state2_listbox.grid(column = 0, row = 2, sticky="E")

        # Adding scrollbar to states listbox
        state_scrollbar = tk.Scrollbar(fws_nondefault_frame)
        state_scrollbar.config(command=self.state2_listbox.yview)
        self.state2_listbox.config(yscrollcommand=state_scrollbar.set)
        state_scrollbar.grid(column=1, row=2, sticky='NSW')

        # Populating states listbox
        for i, state in enumerate(states): 
    
            self.state2_listbox.insert(tk.END, state) 
            self.state2_listbox.itemconfig(i, bg = "deep sky blue")

        ## Outcomes selection listbox widget
        outcomes2_label = ttk.Label(fws_nondefault_frame, text = "Select the outcomes you want to investigate:").grid(column = 2,  
        row = 1, padx = 35, pady = 25, columnspan=2) 
        self.outcomes2_listbox = tk.Listbox(fws_nondefault_frame, selectmode = "multiple", exportselection = False, width=35, height=10)
        self.outcomes2_listbox.grid(column = 2, row = 2, sticky="E")

        # Adding vertical scrollbar to outcomes listbox
        outcomes2_scrollbar = tk.Scrollbar(fws_nondefault_frame)
        outcomes2_scrollbar.config(command=self.outcomes2_listbox.yview)
        self.outcomes2_listbox.config(yscrollcommand=outcomes2_scrollbar.set)
        outcomes2_scrollbar.grid(column=3, row=2, sticky='NSW')

        # Adding horizontal scrollbar to outcomes listbox
        outcomes2_scrollbarh = tk.Scrollbar(fws_nondefault_frame, orient="horizontal")
        outcomes2_scrollbarh.config(command=self.outcomes2_listbox.xview)
        self.outcomes2_listbox.config(xscrollcommand=outcomes2_scrollbarh.set)
        outcomes2_scrollbarh.grid(column=2, row=3, sticky='NWE')

        # Adding calculate button widget 
        button = tk.Button(fws_nondefault_frame, text="Calculate!", bd = "5", command=self.retrieve2)
        button.grid(column = 4, row = 2, padx = 35, pady = 25)

        # Populate the outcomes listbox
        for i, outcome in enumerate(trend_outcomes): 
    
            self.outcomes2_listbox.insert(tk.END, outcome) 
            self.outcomes2_listbox.itemconfig(i, bg = "deep sky blue")
    

    def special_opt_frame(self):
        """
        Function that creates frame and holds user input option 3, which allows for an outcome variable
        choice and chosing multiple policies
        """
        special_opt_frame = tk.Frame(self.frame, bg = "green")
        special_opt_frame.pack(expand=True, fill='x')

        option3_label = ttk.Label(special_opt_frame, text = "Option 3: Retrieve information on how particular policies interact with a given outcome: ").grid(column = 0,  
        row = 0, padx = 35, pady = 25)
        ttk.Label(special_opt_frame, text = "Select one outcome to investigate:").grid(column = 0,  
                row = 1, padx = 35, pady = 25)

        # Combobox widget for outcome choices        
        outcome_combo = tk.StringVar() 
        self.outcomes_combobox = ttk.Combobox(special_opt_frame, width = 27,  
                                    textvariable = outcome_combo, exportselection=0)
        self.outcomes_combobox['values'] = outcomes 
        self.outcomes_combobox.grid(column = 0, row = 2) 

        # Policies selection listbox widget
        policies_label = ttk.Label(special_opt_frame, text = "Select which policies to consider:").grid(column = 1,  
                row = 1, padx = 35, pady = 25, columnspan = 2) 
        self.policies3_listbox = tk.Listbox(special_opt_frame, selectmode = "multiple", exportselection = False, width=35, height=10)
        self.policies3_listbox.grid(column = 1, row = 2, sticky="E")

        # Adding veritcal scrollbar to policies listbox
        policies3_scrollbar = tk.Scrollbar(special_opt_frame)
        policies3_scrollbar.config(command=self.policies3_listbox.yview)
        self.policies3_listbox.config(yscrollcommand=policies3_scrollbar.set)
        policies3_scrollbar.grid(column=2, row=2, sticky='NSW')

        # Adding horizontal scrollbar to policies listbox
        policies3_scrollbarh = tk.Scrollbar(special_opt_frame, orient="horizontal")
        policies3_scrollbarh.config(command=self.policies3_listbox.xview)
        self.policies3_listbox.config(xscrollcommand=policies3_scrollbarh.set)
        policies3_scrollbarh.grid(column=1, row=3, sticky='NWE')

         # Adding calculate button widget 
        button = tk.Button(special_opt_frame, text="Calculate!", bd = "5", command=self.retrieve3)
        button.grid(column = 4, row = 2, padx = 35, pady = 25)

        # Populate the policies listbox
        for i, policy in enumerate(avg_nctq.columns): 
      
            self.policies3_listbox.insert(tk.END, policy) 
            self.policies3_listbox.itemconfig(i, bg = "deep sky blue") 
        

    def r2_cutoff_frame(self):
        """
        Function that creates and holds the frame for the helper tool, which allows a user to pick an outcome and R2 value
        and prints in a textbox the policies that have a correlation higher than R2 with that chosen outcome variable
        """
        r2_frame = tk.Frame(self.frame, bg = "orange")
        r2_frame.pack(expand=True, fill='x')

        r2_label = ttk.Label(r2_frame, text = "Helper tool: Given a particular outcome, find all policies with a correlation greater than a given R2").grid(column = 0,  
        row = 0, padx = 35, pady = 25, columnspan = 2, sticky = "w")
        ttk.Label(r2_frame, text = "Select one outcome to investigate:").grid(column = 0,  
                row = 1, padx = 35, pady = 25)

        # Outcomes combobox widget
        outcome_combo = tk.StringVar() 
        self.r2outcomes_combobox = ttk.Combobox(r2_frame, width = 27,  
                                    textvariable = outcome_combo, exportselection=0)
        self.r2outcomes_combobox['values'] = outcomes 
        self.r2outcomes_combobox.grid(column = 0, row = 2, padx = 35, pady = 25, rowspan =2) 

        # r2 value entry box
        r2_label = ttk.Label(r2_frame, text = "Enter an R2 value (number):").grid(column = 1,  
                row = 1, padx = 35, pady = 25, columnspan = 2) 
        self.entry = tk.StringVar()
        r2_entry = tk.Entry(r2_frame, exportselection = False, width=5, relief=tk.SUNKEN, textvariable = self.entry)
        r2_entry.grid(column = 1, row = 2)

        # Adding textbox that returns policies
        self.r2_textbox = tk.Text(r2_frame, height = 5, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        self.r2_textbox.grid(column = 1, row = 3, padx = 0, pady = 25)

        # Adding vertical scrollbar to textbox
        textbox_scrollbar = tk.Scrollbar(r2_frame)
        textbox_scrollbar.config(command=self.r2_textbox.yview)
        self.r2_textbox.config(yscrollcommand=textbox_scrollbar.set)
        textbox_scrollbar.grid(column=2, row=3, pady = 25, sticky='NSW')

        # Adding calculate button widget 
        button = tk.Button(r2_frame, text="Submit", bd = "5", command=self.retrieve4)
        button.grid(column = 4, row = 2, padx= 35, pady = 25)


    def bottom_frame(self):
        """
        This function creates the final frame with holds buttons that give the user options to view our data
        we are using for calculations, as well as get definitions for the policy names
        """
        bottom_frame = tk.Frame(self.frame, bg = "gold2")
        bottom_frame.pack(expand=True, fill='x', pady = (0, 70))
        # NCES button
        button1 = tk.Button(bottom_frame, text="Click here to see the NCES education outcome data we utilized in our calculations", pady=20, wraplength=250, width = 40)
        button1.grid(column = 0, row = 0, padx = 30, pady = 20)
        button1.bind("<Button>", lambda e: NewWindow("csv/nces_final.csv", self.frame))
        # NCTQ button
        button2 = tk.Button(bottom_frame, text="Click here to see the NCTQ policy grades we utilized in our calculations", pady=20, wraplength=250, width = 40)
        button2.grid(column = 1, row = 0, padx = 30, pady = 20)
        button2.bind("<Button>", lambda e: NewWindow("csv/avg_nctq.csv", self.frame))
        # Policy descriptions button
        button3 = tk.Button(bottom_frame, text="Click here to see the policy descriptions according to the NCTQ", pady=20, wraplength=250, width = 40)
        button3.grid(column = 2, row = 0, padx = 30, pady = 20)
        button3.bind("<Button>", lambda e: NewWindow("csv/policydesc_dic.json", self.frame))


    def scrollbar(self):
        """
        Implements a scrollbar
        """
        scrollbar = tk.Scrollbar(self.frame)
        return scrollbar

    
    def retrieve1(self, states_score_dict, state_to_pols_score_dict):
        """
        Function called when user hits the button for the 1st input option.
        It creates a dictionary with each state = key, and value = get_score() return values
        From default_stat_analysis.py. These return values have the state's score, best and worst
        policies for that particular state. These are passed into a new output window.
        Inputs: states_score_dict: dict that maps states to their effectiveness scores,
                    is the return from default_calc as a global variable
                state_to_pols_score_dict: dict that maps each state to a another dictionary of
                    policies, where each key = policy name, and effectiveness score for that policy
                    on that state's outcome
        """
        states = [self.state_listbox.get(idx) for idx in self.state_listbox.curselection()]
        outcomes = list(nces_trends.columns)
        return_dict = {}
        for state in states:
            score, best_pol, worst_pol = dsa.get_scores(states_score_dict, state_to_pols_score_dict, state)
            return_dict[state] = [score, best_pol, worst_pol]
        self.new_window1(return_dict, outcomes)


    def retrieve2(self):
        """
        Function called when user hits the button for the 2st input option. It runs the default_calc()
        once again given a different set of outcomes than the default of all outcomes.
        It creates a dictionary with each state = key, and value = get_score() return values
        From default_stat_analysis.py. These return values have the state's score, best and worst
        policies for that particular state. These are passed into a new output window.
        """
        states = [self.state2_listbox.get(idx) for idx in self.state2_listbox.curselection()]
        outcomes = [self.outcomes2_listbox.get(idx) for idx in self.outcomes2_listbox.curselection()]
        states_score_dict, state_to_pols_score_dict = dsa.default_calc(
                avg_nctq, centered_avg_nctq, nces_trends, R2, block_negative=True, outcomes=False
            )   
        return_dict = {}    
        for state in states:
            score, best_pol, worst_pol = dsa.get_scores(states_score_dict, state_to_pols_score_dict, state)
            return_dict[state] = [score, best_pol, worst_pol]
        self.new_window1(return_dict, outcomes)


    def retrieve3(self):
        """
        Function called when user hits 3rd input option button, and passes those selected inputs
        into a new output window.
        """
        outcome = self.outcomes_combobox.get()
        policies = [self.policies3_listbox.get(idx) for idx in self.policies3_listbox.curselection()]
        self.new_window2(outcome, policies)


    def retrieve4(self):
        """
        Function called when user hits submit button in the 4th helper tool frame
        Returns the appropriate policies to the text widget.
        """
        outcome = self.r2outcomes_combobox.get()
        self.r2_textbox.delete(1.0, tk.END)
        try:
            r2 = float(self.entry.get())
            policies = b.cutoff_R2(avg_nctq, nces_final[outcome], r2)
            print(policies)
            if policies:
                self.r2_textbox.insert(tk.END, "\n".join(policies))
            else: 
                self.r2_textbox.insert(tk.END, "No such policies found")

        except Exception:
            self.r2_textbox.insert(tk.END, "Please insert a number for the R2")
        

    def new_window1(self, return_dict, outcomes):
        """
        Creates a new output window for user input option 1 and 2
        """
        self.newWindow1 = tk.Toplevel(self.frame)
        self.output1 = output1.Output1(self.newWindow1, return_dict, outcomes)


    def new_window2(self, outcome, policies):
        """
        Creates a new output window for user input option 3
        """
        self.newWindow2 = tk.Toplevel(self.frame)
        self.output2 = output2.Output2(self.newWindow2, nces_final, avg_nctq, outcome, policies)


def main(): 
    """
    This function runs everything in this file, and makes calls to all other necessary files.
    """
    root = tk.Tk()
    root["bg"] = "white"
    # Getting screen width and height of display 
    screen_width = root.winfo_screenwidth()  #in pixels
    screen_height= root.winfo_screenheight() #in pixels
    # Setting tkinter window size 
    root.geometry("%dx%d" % (screen_width, screen_height))
    root.title("CS122 TJJE Project: Examining State Policies and Educational Outcomes")
    # Applying class
    app = Window1(root)
    root.mainloop()

if __name__ == '__main__':
    main()