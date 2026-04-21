# A chatbot that you can ask questions about 18th-century English law
This repository contains all the source code for an expert system from 18th-century English Law, created for my CS152: Harnessing Artificial Intelligence Algorithms final.

This project addresses the challenge of modeling historical legal outcomes from the Old Bailey Online archives by framing 18th-century English law as a formal Expert System. Historically, judicial decisions are often perceived as purely narrative; however, by applying Predicate Logic, I encoded the court’s “working knowledge” of factors such as crime severity, defendant status, and evidence into a deductive framework that yields the case’s outcome (an overly simplified version, of course). By simplifying a large dataset into a deductive logic framework, I created a digital product that makes the general working system of 18th-century English law a fun learning experience for non-experts and kids.

## Enhanced with Semantic Mapping via Definite Clause Grammars (DCGs)

The system now includes **Definite Clause Grammars (DCGs)** for sophisticated natural language parsing and semantic mapping.

### DCG Semantic Parsing Overview

DCGs enable the system to parse user input in natural language and automatically extract semantic information that populates the knowledge base. This eliminates the need for rigid question-answer formats.

#### How DCG Semantic Mapping Works

1. **User Input** → Natural language (e.g., "theft from a shop")
2. **Tokenization** → Convert to token list: `[theft, from, a, shop]`
3. **DCG Parsing** → Match against grammar rules to extract semantics
4. **Semantic Extraction** → Identify: `offense(theft)`, `location(shop)`
5. **Knowledge Base Update** → Assert facts for inference

#### Supported Semantic Categories

| Category | DCG Rule | Example Inputs |
|----------|----------|-----------------|
| **Offenses** | `parse_offense/2` | theft, murder, robbery, burglary, coining |
| **Locations** | `parse_location/2` | shop, dwelling house, street, marketplace |
| **Gender** | `parse_gender/2` | male, female, man, woman |
| **Circumstances** | `parse_circumstance/2` | first offense, malice aforethought, premeditation |
| **Abilities** | `parse_ability/2` | can read, illiterate, educated |
| **Values** | `parse_value/2` | "5 shillings", "40 pence", "10 s." |

#### Example Usage

```prolog
?- parse_user_input("theft from a dwelling house", Attr, Val).
Attr = offense,
Val = theft ;
Attr = location,
Val = dwelling_house.

?- process_natural_input("first time offender").
Parsed: circumstance(first_offense)
true.
```

#### DCG Grammar Rules (Simplified Example)

```prolog
% Parse offense keywords
parse_offense(offense, theft) --> [theft] | [steal] | [stole] | [stolen].

% Parse location keywords
parse_location(location, shop) --> [shop] | [merchant] | [store].

% Parse numerical values
parse_value(item_value_shillings, Value) --> 
    number(N), 
    shilling_unit,
    { Value is N }.
```

### Integration with Prolog Inference Engine

The DCG parser is tightly integrated with the expert system's inference engine:

1. **Dynamic Knowledge Base** → Parsed facts are asserted dynamically
2. **Inference** → Legal rules query the populated knowledge base
3. **Verdict Generation** → Case verdict is derived from accumulated facts

### Running the System

```bash
python3 prolog_engine.py
```

The enhanced chatbot now accepts:
- **Natural language input** (parsed by DCGs)
- **Traditional yes/no responses** (fallback support)
- **Numerical values** (e.g., "5 shillings")
- **Complex case descriptions** (e.g., "murder with malice aforethought")

### DCG Testing & Demonstration

To test the DCG semantic parser directly in Prolog:

```prolog
?- demonstrate_dcg.
```

This runs through example inputs and displays parsed semantic representations.

### Architecture

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
    ┌────▼────┐
    │Tokenizer│
    └────┬────┘
         │
    ┌────▼──────────┐
    │  DCG Parser   │  (Definite Clause Grammars)
    └────┬──────────┘
         │
    ┌────▼──────────────┐
    │Semantic Extractor │
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │Knowledge Base     │  (dynamic facts)
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │Inference Engine   │  (Prolog rules)
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │  Verdict Output   │
    └───────────────────┘
```

### Key Features

✅ **Natural Language Processing** — DCGs parse flexible user input
✅ **Semantic Mapping** — Extracts case facts from text
✅ **Dynamic Knowledge Base** — Facts asserted during runtime
✅ **Backward Chaining** — Inference driven by verdict rules
✅ **Historical Accuracy** — Rules based on Old Bailey legal precedents
✅ **Extensible** — Easy to add new grammar rules and semantic categories
