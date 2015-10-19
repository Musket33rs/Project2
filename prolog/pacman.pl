%Pacman at X Y in situation S
%at(Pacman, X, Y, S).
%Ghost at X Y is scared/normal in situation S
%at(Ghost, X, Y, Ghost_scared, S).




wall(2,2).
wall(3,2).
wall(2,4).

wall(0,0).
wall(0,1).
wall(0,2).
wall(0,3).
wall(0,4).
wall(0,5).

wall(1,0).
wall(1,5).
wall(2,0).
wall(2,5).
wall(3,0).
wall(3,5).
wall(4,0).
wall(4,5).
wall(5,5).


food(1,2).
food(1,3).
food(2,1).
food(3,1).
food(3,4).
fodd(4,1).
fodd(4,2).
fodd(4,3).
fodd(4,4).

super_food(2,3).
super_food(3,3).


%precondition for primitive actions
%move for pacman
poss(moveUp,S):- at(pacman, X, Y0, S),
				 Y is Y0 + 1,
				 \+at(ghost,X,Y,S),
				 \+wall(X,Y),
				 at(pacman, X, Y, S).

poss(moveDown(Y),S):- at(pacman, X, Y0, S),
					  Y is Y0 - 1,
					  \+at(ghost,X,Y,S),
					  \+wall(X,Y),
					  at(pacman, X, Y, S).

poss(moveLeft(X),S):- at(pacman, X0, Y, S),
					  X is X0 - 1,
					  \+at(ghost,X,Y,S),
					  \+wall(X,Y),
					  at(pacman, X, Y, S).

poss(moveRight(X),S):- at(pacman, X0, Y, S),
					  X is X0 - 1,
					  \+at(ghost,X,Y,S),
					  \+wall(X,Y),
					  at(pacman, X, Y, S).





/*
poss(eat_food(X,Y),S):-  at(pacman, X1, Y1, S),
	% pacman is either a +-1 of X
	( X is X1+1 ; X is X1-1 ),
	% pacman is either a +-1 of Y
	( Y is Y1+1 ; Y is Y1-1 ),
	% there is food at X Y
	food(X,Y),
	% there is no ghost or ghost is scared
	\+ at(_, X, Y, normal, S);*\
	at(_, X, Y, scared, S).

poss(eat_super_food(X,Y),S):-  at(pacman, X1, Y1, S),
	% pacman is either a +-1 of X
	( X is X1+1 ; X is X1-1 ),
	% pacman is either a +-1 of Y
	( Y is Y1+1 ; Y is Y1-1 ),
	% there is food at X Y
	super_food(X,Y),
	% there is no ghost at X Y position
	\+ at(_, X, Y, normal,S);
	at(_, X , Y, scared, S).

poss(eat_ghost(X,Y),S):- at(pacman, X1, Y1, S),
	% pacman is either a +-1 of X
	( X is X1+1 ; X is X1-1 ),
	% pacman is either a +-1 of Y
	( Y is Y1+1 ; Y is Y1-1 ),
	% ghost at X Y is scared, (at(G, X, Y, S)),(ghost_scared).
	(at(_, X, Y, scared, S)).
*/

% Success state axioms
% win if my score is bigger than 0 at the end
% win(score, end, )
at(Pacman, X, Y, do(A,S)):-
	at(Pacman, X0, Y0, S),
	( 
		(A =  moveUp, Y is Y0+1);
		(A =  moveDown, Y is Y0-1);
		(A =  moveRight, X is X0+1);
		(A =  moveLeft, X is X0-1)
	)

	;

	(
		at(Pacman, X, Y, S),
		\+A=moveUp,
		\+A=moveDown,
		\+A=moveRight,
		\+A=moveLeft
	).

%Legal axioms
legal(s0).
legal(do(A,S)) :- legal(S), poss(A,S).




%initial conditions
at(pacman, 1, 1, s0).
%at(ghost, 1, 4, s0).


% what agents is at position X Y
% ghost_status().





