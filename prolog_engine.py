import sys
import os
from pyswip.prolog import Prolog
from pyswip.easy import *

prolog = Prolog()
# Global to hold the message coming from the web UI
current_web_input = ""

# Functors for state management
retractall = Functor("retractall")
known = Functor("known", 3)

def write_py(X):
    # For web, we usually log to console or skip
    print(f"Prolog: {str(X)}")
    return True

def read_py(A, V, Y):
    """
    Web-ready handler: Instead of input(), it uses the current_web_input
    provided by the Flask route.
    """
    global current_web_input
    if isinstance(Y, Variable):
        # We pass the message from the Flask app directly to Prolog
        # If the input is empty, we return False to let Prolog know nothing was found
        if not current_web_input:
            return False
            
        Y.unify(Atom(current_web_input))
        return True
    return False

# Registering arity and foreign functions
write_py.arity = 1
read_py.arity = 3
registerForeign(read_py)
registerForeign(write_py)

# Consult the KB once at startup
kb_path = os.path.join(os.path.dirname(__file__), "kb.pl")
if os.path.exists(kb_path):
    prolog.consult(kb_path)

def handle_chat_message(user_message):
    """
    The main bridge function for your Flask app.py.
    It handles the narrative first, then the inference.
    """
    global current_web_input
    
    # 1. Clean the message for Prolog
    clean_text = user_message.lower().replace('.', '').replace(',', '').replace(';', '')
    tokens = clean_text.split()
    
    # Check if this is the start of a new case (narrative) 
    # or a follow-up answer
    existing_facts = list(prolog.query("known(yes, _, _)"))
    
    if not existing_facts:
        # First interaction: Run parse_narrative
        word_list = "[" + ",".join([w if w.isdigit() else f"'{w}'" for w in tokens]) + "]"
        list(prolog.query(f"parse_narrative({word_list})"))
    else:
        # Follow-up interaction: Set the global for read_py/3 to pick up
        current_web_input = user_message.lower().strip()

    # 2. Run the Expert System
    # We query for the verdict. If it hits an 'ask', read_py is triggered.
    try:
        results = list(prolog.query("verdict(X)", maxresult=1))
        
        if results:
            # We found a verdict! Clear the state for the next case.
            outcome = str(results[0]['X']).replace('_', ' ').upper()
            prolog.query("retractall(known(_,_,_))")
            return f"The Court has reached a verdict: {outcome}"
        else:
            # If no verdict yet, we need to check what the last 'ask' was.
            # In a basic CS152 engine, the agent just asks for more info.
            return "The Court requires more detail. Can you tell me more about the location, value, or the defendant?"
            
    except Exception as e:
        return f"The legal proceedings encountered an error: {str(e)}"

def reset_court():
    """Resets the knowledge base state."""
    list(prolog.query("retractall(known(_,_,_))"))
    return "The court records have been cleared."