%Pacman at X Y in situation S
%at(Pacman, X, Y, S).
%Ghost at X Y is scared/normal in situation S
%at(Ghost, X, Y, Ghost_scared, S).



%precondition for primitive actions
%move for pacman
poss(moveUp,S):- pacmanAt(X, Y0, S),
				 Y is Y0 + 1,
				 \+ghostAt(X,Y,S),
				 \+wall(X,Y).
				 

poss(moveDown,S):- pacmanAt(X, Y0, S),
					  Y is Y0 - 1,
					  \+ghostAt(X,Y,S),
					  \+wall(X,Y).
					  

poss(moveLeft,S):- pacmanAt(X0, Y, S),
					  X is X0 - 1,
					  \+ghostAt(X,Y,S),
					  \+wall(X,Y).
					  

poss(moveRight,S):- pacmanAt(X0, Y, S),
					  X is X0 + 1,
					  \+ghostAt(X,Y,S),
					  \+wall(X,Y).	


% Success state axioms
% win if my score is bigger than 0 at the end
% win(score, end, )

pacmanAt(X, Y, do(A,S)):-
	pacmanAt(X0, Y0, S),
	( 
		(A =  moveUp, Y is Y0+1);
		(A =  moveDown, Y is Y0-1);
		(A =  moveRight, X is X0+1);
		(A =  moveLeft, X is X0-1)
	)

	;

	(
		pacmanAt(X, Y, S),
		\+A=moveUp,
		\+A=moveDown,
		\+A=moveRight,
		\+A=moveLeft
	).

%Legal axioms
legal(s0).
legal(do(A,S)) :- legal(S), poss(A,S).




%initial conditions
pacmanAt(1, 4, s0).
ghostAt(4, 4, s0).

% what agents is at position X Y
% ghost_status().

%Borders
wall(0,0).
wall(1,0).
wall(2,0).
wall(3,0).
wall(4,0).
wall(5,0).

wall(0,1).
wall(0,2).
wall(0,3).
wall(0,4).
wall(0,5).

wall(1,5).
wall(2,5).
wall(3,5).
wall(4,5).
wall(5,5).

wall(5,1).
wall(5,2).
wall(5,3).
wall(5,4).

%Internal walls
wall(2,2).
wall(2,3).
wall(2,3).
wall(4,3).


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




