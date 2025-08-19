fof(human_mortality, axiom,
    (! [X] : (human(X) => mortal(X)))).

fof(socrates_human, axiom,
    human(socrates)).

fof(mortality_question, conjecture,
    mortal(socrates)).
% Simple propositional satisfiability problem
cnf(clause1, axiom, (p | q)).
cnf(clause2, axiom, (~p | r)).
cnf(clause3, axiom, (~q | r)).
cnf(clause4, negated_conjecture, (~r)).
