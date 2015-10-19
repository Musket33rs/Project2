%initial conditions
%Pacman at X Y in situation S
%at(Pacman, X, Y, S).
%Ghost at X Y is scared/normal in situation S
%at(Ghost, X, Y, Ghost_scared, S).

at(pacman, 1, 1, s0).
at(ghost, 1, 4, normal, s0).


% what agents is at position X Y
% ghost_status().



wall(2,2).
wall(3,2).
wall(2,4).

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
poss(move(X,Y),S):- at(pacman, X1, Y1, S),
	% pacman is either a +-1 of X
	( X is X1+1 ; X1 is X1-1 ),
	% pacman is either a +-1 of Y
	( Y is Y1+1 ; Y is Y1-1 ),
	% there is no ghost at X Y position
	\+ at(ghost, X, Y, S),
	% not a wall
	\+ wall(X,Y).

poss(eat_food(X,Y),S):-  at(pacman, X1, Y1, S),
	% pacman is either a +-1 of X
	( X is X1+1 ; X is X1-1 ),
	% pacman is either a +-1 of Y
	( Y is Y1+1 ; Y is Y1-1 ),
	% there is food at X Y
	food(X,Y),
	% there is no ghost or ghost is scared
	\+ at(_, X, Y, normal, S);
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






