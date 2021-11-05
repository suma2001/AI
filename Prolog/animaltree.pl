
species-name('African wild dog', 'Lycaon pictus').
species-name('Common fox', 'Vulpes vulpes').
species-name('Arctic fox', 'Vulpes lagopus').
species-name('Fennec fox', 'Vulpes zerda').
species-name('Red wolf', 'Canis rufus').
species-name('Coyote', 'Canis latrans').
species-name('Gray wolf','Canis lupus').
species-name('Dog','Canis lupus').

species-genus('Lycaon pictus', 'Lycaon').
species-genus('Vulpes vulpes', 'Vulpes').
species-genus('Vulpes lagopus', 'Vulpes').
species-genus('Vulpes zerda', 'Vulpes').
species-genus('Canis rufus', 'Canis').
species-genus('Canis latrans', 'Canis').
species-genus('Canis lupus', 'Canis').

sub-species('Gray wolf', 'Canis lupus').
sub-species('Dog','Canis lupus familiaris').

genus-family('Lycaon', 'Canidae').
genus-family('Vulpes', 'Canidae').
genus-family('Canis', 'Canidae').

common-genus(X,Y) :-
	species-name(X,A),
	(sub-species(A,P) -> species-genus(P,C);
	species-genus(A,C)),
	species-name(Y,B),
	(sub-species(B,Q) -> species-genus(Q,D);
	species-genus(B,D)),
	not(X=Y),
	C==D.

common-species(X,Y) :-
	species-name(X,P),
	species-name(Y,P),
	not(X=Y).

path(A,B,X) :- 
	species-name(A,C),
	species-genus(C,D),
	species-name(B,E),
	species-genus(E,F),
	D=F,
	X=[A,C,D,E,B], !,
	format(' Path is :- ~n ~a <--> ~a <--> ~a <--> ~a <--> ~a ~n ~n', X).

path(A,B,X) :-
	species-name(A,C),
	species-genus(C,D),
	species-name(B,E),
	species-genus(E,F),
	genus-family(F,G),
	X=[A,C,D,G,F,E,B], !,
	format(' Path is :- ~n ~a <--> ~a <--> ~a <--> ~a <--> ~a <--> ~a <--> ~a ~n ~n', X).



