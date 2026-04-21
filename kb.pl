% Tell Prolog that known/3 and multivalued/1 will be added later
:- dynamic known/3, multivalued/1.

% Directives to suppress warnings and allow spread-out rules
:- discontiguous find_gender/3.
:- discontiguous find_offense/3.
:- discontiguous find_location/3.
:- discontiguous find_value/3.
:- discontiguous find_circumstance/3.
:- discontiguous find_ability/3.
:- discontiguous find_year/3.

% --- 1. NLP PARSING LAYER ---

parse_narrative(Words) :-
    (phrase(find_gender(G), Words, _) -> assertz(known(yes, gender, G)) ; true),
    (phrase(find_offense(O), Words, _) -> assertz(known(yes, offense, O)) ; true),
    (phrase(find_location(L), Words, _) -> assertz(known(yes, location, L)) ; true),
    (phrase(find_value(V), Words, _) -> assertz(known(yes, item_value_shillings, V)) ; true),
    (phrase(find_circumstance(C), Words, _) -> assertz(known(yes, circumstance, C)) ; true),
    (phrase(find_ability(A), Words, _) -> assertz(known(yes, ability, A)) ; true),
    (phrase(find_year(Y), Words, _) -> assertz(known(yes, year_period, Y)) ; true).

% --- DCG Rules for Vocabulary Mapping ---

% Gender
find_gender(male) --> [man] ; [he] ; [him] ; [boy] ; [male] ; [gentleman].
find_gender(female) --> [woman] ; [she] ; [her] ; [girl] ; [female] ; [lady].
find_gender(G) --> [_], find_gender(G).

% Offenses (based on historical statutes)
find_offense(highway_robbery) --> [highway, robbery].
find_offense(coining) --> [coin] ; [counterfeit] ; [money] ; [treason].
find_offense(murder) --> [murder] ; [killed] ; [killing] ; [slaying].
find_offense(burglary) --> [burglary] ; [broke, into] ; [at, night].
find_offense(theft) --> [stole] ; [theft] ; [stolen] ; [larceny] ; [shoplifting] ; [pickpocket].
find_offense(O) --> [_], find_offense(O).

% Locations
find_location(dwelling_house) --> [dwelling, house] ; [home] ; [house] ; [residence].
find_location(shop) --> [shop] ; [store] ; [warehouse].
find_location(highway) --> [highway] ; [road] ; [street] ; [path].
find_location(L) --> [_], find_location(L).

% Numeric Value
find_value(V) --> [Token], {atom_number(Token, V), V < 1000}. 
find_value(V) --> [_], find_value(V).

% Circumstances and Legal Status
find_circumstance(malice_aforethought) --> [malice] ; [intent] ; [planned] ; [wilful].
find_circumstance(first_offense) --> [first, time] ; [never, before] ; [clean, record].
find_circumstance(C) --> [_], find_circumstance(C).

% Literacy/Ability
find_ability(can_read) --> [read] ; [reading] ; [clergy] ; [literate] ; [bible].
find_ability(A) --> [_], find_ability(A).

% Year Period
find_year(pre_1706) --> ['1600s'] ; [seventeenth, century] ; [early]; [Token], {atom_number(Token, Y), Y >= 1000, Y < 1706}.
find_year(post_1718) --> ['1700s'] ; [eighteenth, century] ; [late]; [Token], {atom_number(Token, Y), Y >= 1718}. 
find_year(Y_per) --> [_], find_year(Y_per).


% --- VERDICT RULES ---

% Rule: Pious Perjury (Jury Mercy for women/first-timers)
verdict(partial_verdict_transportation) :-
    offense(theft),
    location(dwelling_house),
    item_value_shillings(V), V >= 40,
    % The AI "predicts" the jury will intervene for females or first-timers
    (gender(female) ; circumstance(first_offense)).

% Rule: Benefit of Clergy (The literacy loophole)
verdict(branding_and_release) :-
    offense(theft),
    circumstance(first_offense),
    ability(can_read),
    year_period(pre_1706).

% Rule: The "Standard" Death Sentence (Only if Mercy/Clergy didn't trigger)
verdict(death_by_hanging) :-
    offense(theft),
    location(dwelling_house),
    item_value_shillings(V), V >= 40.

% Rule: Shoplifting Act of 1699. Theft from a shop of goods > 5 shillings was a capital crime.
verdict(death_by_hanging) :-
    offense(theft),
    location(shop),
    item_value_shillings(V), V > 5.

% Rule: High Treason (Coining). Historically, counterfeiting money was a non-clergyable capital offense.
verdict(death_by_hanging) :- 
    offense(coining).

% Rule: Murder with Malice. Direct killing with intent led to the gallows.
verdict(death_by_hanging) :- 
    offense(murder),
    circumstance(malice_aforethought).

% Rule: Highway Robbery. Under the Bloody Code, this was always a capital offense regardless of value.
verdict(death_by_hanging) :- 
    offense(highway_robbery).

% Rule: Burglary. Breaking and entering a dwelling at night was a non-clergyable felony.
verdict(death_by_hanging) :- 
    offense(burglary).


% Rule: Transportation Act of 1718. Allowed 7 years for "clergyable" felonies or 14 for pardoned capital ones.
verdict(transportation_7_years) :-
    offense(theft),
    \+ verdict(death_by_hanging),  % If it doesn't meet capital thresholds
    item_value_shillings(V), V >= 1. % Grand Larceny threshold (12 pence).


% Rule: Petty Larceny. Theft of items < 1 shilling (12 pence).
verdict(whipping_and_imprisonment) :-
    offense(theft),
    item_value_shillings(V), V < 1.


% --- ASKABLES ---
offense(X) :- ask(offense, X).
location(X) :- ask(location, X).
gender(X) :- ask(gender, X).
circumstance(X) :- ask(circumstance, X).
ability(X) :- ask(ability, X).
item_value_shillings(X) :- ask(item_value_shillings, X).
year_period(X) :- ask(year_period, X).

% --- ASKING CLAUSES (Provided Framework) ---
ask(A, V) :-
    known(yes, A, V), % Success if already known
    !.

ask(A, V) :-
    known(no, A, V), % Fail if known to be false
    !, fail.

% If not known, ask the user and parse the response
ask(A, V) :-
    \+ multivalued(A),
    known(yes, A, V2),
    V \== V2,
    !, fail.

ask(A, V) :-
    read_py(A, V, RawString),            % Get the raw string from Python
    atomic_list_concat(Words, ' ', RawString), % Tokenize the string into a list
    parse_narrative(Words),              % Run the DCG parser on the new words
    % After parsing, check if the specific fact we need (A, V) is now known
    (known(yes, A, V) -> true ; 
        % Fallback for simple 'yes' or 'y' responses
        (RawString == 'yes' ; RawString == 'y') -> assertz(known(yes, A, V)) ; 
        (assertz(known(no, A, V)), fail)
    ).