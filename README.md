# A chatbot that you can ask questions about 18th-century English law
This repository contains all the source code for an expert system from 18th-century English Law, created for my CS152: Harnessing Artificial Intelligence Algorithms final.

To ensure your project can be evaluated effectively, include the following instructions in your submission (e.g., in a `README.md` file or at the top of your documentation).

---

## Instructions for Running Legal-ES

### 1. Prerequisites
Before running the application, ensure the following are installed on your system:

* **Python 3.10+**: The core language.
* **SWI-Prolog**: The logic engine. **Pyswip** requires the actual SWI-Prolog binary to be installed on your operating system (Download at [swi-prolog.org](https://www.swi-prolog.org/)).
* **Tkinter**: This is typically bundled with Python. If you are on Linux, you may need to install it manually (e.g., `sudo apt-get install python3-tk`).
* **Pyswip**: The bridge between Python and Prolog. Install via pip:
    ```bash
    pip install pyswip
    ```

### 2. How to Run the Application
1.  Navigate to the project root directory.
2.  Ensure `kb.pl` and `legal_gui.py` are in the same folder.
3.  Execute the following command:
    ```bash
    python legal_gui.py
    ```

### 3. Running the Test Cases
To verify the **Symbolic AI** logic, enter the following narratives into the chat interface. Each case is designed to test a specific layer of the inference engine:

| Test Case | Narrative to Input | Expected Result / AI Logic Tested |
| :--- | :--- | :--- |
| **TC1: Seamless Seeding** | *"A man stole 50 shillings from a dwelling house in 1678. He can read and this was his first time."* | **Verdict: Branding & Release.** Verifies successful symbol grounding (DCG) and NLP seeding. |
| **TC2: Conflict Resolution** | *"A woman stole 50 shillings from a dwelling house."* | **Verdict: Partial Verdict.** Verifies **Rule Prioritization** (Jury Mercy for women overrides the Death Statute). |
| **TC3: Short-Circuiting** | *"A man committed highway robbery."* | **Verdict: Death by Hanging.** Verifies search efficiency; engine skips irrelevant questions (e.g., value) for non-clergyable crimes. |
| **TC4: Backward Chaining** | *"A man stole some silk."* | **Action: Follow-up Questions.** Verifies the interactive loop; the agent should ask for missing variables (value and location). |

### 4. Troubleshooting
* **"SWI-Prolog not found"**: Ensure SWI-Prolog is added to your system's PATH. On macOS, you may need to manually point to the library in the code using `os.environ['LD_LIBRARY_PATH']`.
* **NestedQueryError**: This occurs if the Prolog query is interrupted. Restart the application to clear the internal state of the inference engine.