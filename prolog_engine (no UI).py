import sys
import os
from pyswip.prolog import Prolog
from pyswip.easy import *

# Initialize Prolog
prolog = Prolog()

# Functors for state management
retractall = Functor("retractall")
known = Functor("known", 3)

# --- Foreign Functions ---

def write_py(X):
    """Prints messages from Prolog to the Python console."""
    print(str(X))
    sys.stdout.flush()
    return True

def read_py(A, V, Y):
    """
    Simplified handler: Returns the raw user string to Prolog.
    Prolog will then handle the DCG parsing internally.
    """
    if isinstance(Y, Variable):
        attr_name = str(A).replace('_', ' ')
        
        # Determine the prompt
        if str(A) == 'item_value_shillings':
            prompt = f"\nThe Court requires the value. What was the worth of the goods? "
        elif str(A) == 'circumstance':
            prompt = f"\nThe Court needs more context on the circumstance. Please elaborate if this was their first crime or if there were any malice aforethought: "
        else:
            prompt = f"\nThe Court is unclear on the {attr_name}. Please provide more detail: "
        
        try:
            response = input(prompt).lower().strip()
            # Unify the variable Y with the raw string atom
            # We wrap it in quotes to ensure it is a valid Prolog atom
            Y.unify(Atom(response))
            return True
        except EOFError:
            return False
    return False

# Registering arity and foreign functions
write_py.arity = 1
read_py.arity = 3
registerForeign(read_py)
registerForeign(write_py)

# --- Knowledge Base Integration ---

def load_kb():
    """Locates and consults the kb.pl file."""
    kb_path = "kb.pl" # Assumes file is in the same directory
    if os.path.exists(kb_path):
        prolog.consult(kb_path)
    else:
        print(f"Error: {kb_path} not found.")
        sys.exit(1)

def run_chatbot():
    print("--- 18th Century Old Bailey Legal Agent ---")
    narrative = input("\nDescribe the case (e.g., 'A woman stole silk in a shop'): ").lower()
    
    # Tokenize and ensure every word is treated as a Prolog atom. 
    clean_text = narrative.replace('.', '').replace(',', '').replace(';', '')
    tokens = clean_text.split()
    # Wrapping words in single quotes prevents Prolog from seeing them as variables. [cite: 13, 82]
    word_list = "[" + ",".join([f"'{w}'" for w in tokens]) + "]"
    
    # Reset and Parse
    call(retractall(known))
    # Forces the query to run and assert facts before deduction begins. 
    list(prolog.query(f"parse_narrative({word_list})"))
    
    print("\n[The Court is deliberating based on the statutes...]")
    results = list(prolog.query("verdict(X)", maxresult=1))
    
    if results:
        outcome = str(results[0]['X']).replace('_', ' ').upper()
        print(f"\nPREDICTED VERDICT: {outcome}")
    else:
        print("\nRESULT: Insufficient evidence for a specific historical verdict.")

if __name__ == "__main__":
    load_kb()
    run_chatbot()
