import tkinter as tk
from tkinter import scrolledtext
from pyswip.prolog import Prolog
from pyswip.easy import *
import sys
import os 

 
class LegalChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Old Bailey Legal Agent")
        
        # --- 1. PROLOG SETUP  ---
        self.prolog = Prolog()
        self.retractall = Functor("retractall", 1)
        self.known = Functor("known", 3)
        
        # Registering foreign functions
        registerForeign(self.read_py, arity=3)
        registerForeign(self.write_py, arity=1)
        
        # Load KB
        if os.path.exists("kb.pl"):
            self.prolog.consult("kb.pl")
        else:
            self.log("Error: kb.pl not found.")

        # --- 2. GUI LAYOUT ---
        self.txt_log = scrolledtext.ScrolledText(root, state='disabled', width=70, height=20, font=("Garamond", 12))
        self.txt_log.pack(padx=10, pady=10)

        self.entry_input = tk.Entry(root, width=50, font=("Garamond", 12))
        self.entry_input.pack(side=tk.LEFT, padx=10, pady=10)
        self.entry_input.bind("<Return>", lambda e: self.handle_send())

        self.btn_send = tk.Button(root, text="Send", command=self.handle_send)
        self.btn_send.pack(side=tk.LEFT, padx=5, pady=10)

        # State management for waiting
        self.input_value = tk.StringVar()
        self.waiting_for_user = False
        
        self.log("--- 18th Century Old Bailey Legal Agent ---")
        self.log("Describe the case (e.g., 'A woman stole silk in a shop'):")

    # --- 3. REPLACING PRINT/INPUT WITH GUI METHODS ---

    def log(self, message):
        """Replaces print()"""
        self.txt_log.config(state='normal')
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.config(state='disabled')
        self.txt_log.see(tk.END)

    def write_py(self, X):
        self.log(str(X))
        return True

    def read_py(self, A, V, Y):
        """Replaces input() - Pauses Prolog until GUI button is clicked."""
        if isinstance(Y, Variable):
            attr_name = str(A).replace('_', ' ')
            
            # Set the prompt in the log
            if str(A) == 'item_value_shillings':
                self.log("\n[The Court requires the value. What was the worth of the goods?]")
            elif str(A) == 'circumstance':
                self.log("\n[The Court needs context. Was this a first crime or was there malice?]")
            else:
                self.log(f"\n[The Court is unclear on the {attr_name}. Please provide detail:]")
            
            # BLOCKING WAIT
            self.waiting_for_user = True
            self.root.wait_variable(self.input_value) 
            
            response = self.input_value.get()
            Y.unify(Atom(response))
            self.waiting_for_user = False
            return True
        return False

    def handle_send(self):
        """Captures input from the entry field."""
        user_text = self.entry_input.get().lower().strip()
        if not user_text: return
        
        self.entry_input.delete(0, tk.END)
        self.log(f"You: {user_text}")

        if self.waiting_for_user:
            # If Prolog is waiting, trigger the wait_variable
            self.input_value.set(user_text)
        else:
            # Otherwise, start a new case
            self.run_inference(user_text)

    def run_inference(self, narrative):
        """Your run_chatbot() logic, adjusted for the GUI."""
        clean_text = narrative.replace('.', '').replace(',', '').replace(';', '')
        tokens = clean_text.split()
        word_list = "[" + ",".join([f"'{w}'" for w in tokens]) + "]"
        
        # Reset and Parse
        call(self.retractall(self.known))
        list(self.prolog.query(f"parse_narrative({word_list})"))
        
        self.log("\n[The Court is deliberating based on the statutes...]")
        
        # Start the query - this will trigger read_py if info is missing
        results = list(self.prolog.query("verdict(X)", maxresult=1))
        
        if results:
            outcome = str(results[0]['X']).replace('_', ' ').upper()
            self.log(f"\nPREDICTED VERDICT: {outcome}")
            self.log("\n--- Case Closed. Enter a new case narrative to begin again. ---")
        else:
            self.log("\nRESULT: Insufficient evidence for a verdict.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LegalChatbotGUI(root)
    root.mainloop()