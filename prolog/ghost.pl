% pman.pl
%﻿ Tou Lee 656128
% Jaime Martinez 642231

% assumptions
% Connected points ar adjacent up,down,left or right, unless there is a wall.
% Only need to check if a move is legal checking if two coordinates are
% connected. To check if they are connected, the point cannot be a wall, and
% be adjacent.
% To move to a certain possition is possible as long as is not a wall.
% To eat pacman, move condition has to be true and the ghost should not be
% scared.


%initial condition
pmanAt(4,5).

ghostAt(4,4,scared,s0).
wall(0,0).
/*
% sample grid
wall(1,2).
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
*/

% Helpers
isConnected(X,Y1,X,Y2):-(\+wall(X,Y2)),(Y2 is Y1+1);(Y2 is Y1-1).
isConnected(X1,Y,X2,Y):-(\+wall(X2,Y)),(X2 is X1+1);(X2 is X1-1).

% preconditions

poss(move(X1,Y1),S):- ghostAt(X,Y,notScared,S),isConnected(X,Y,X1,Y1).
poss(move(X1,Y1),S):- ghostAt(X,Y,scared,S),isConnected(X,Y,X1,Y1),
                      ( \+pmanAt(X1,Y1)).

% success state axioms  for action move
ghostAt(X,Y,Z,do(A,S)):-ghostAt(X1,Y1,Z,S),isConnected(X1,Y1,X,Y),
      (
        A=move(X,Y)
      );
      (
        ghostAt(X,Y,Z,S),
        \+ A=move(X,Y)
      ).

% This predicates allow to trace legal actions, checking the Preconditions.
/*legal axioms*/
  legal(s0).
  legal(do(A,S)):-legal(S),poss(A,S).

% to test do:  legal(S),ghostAt(X,Y,_,S). where X,Y are coordinates in a plane.
% The third argument should be left as _ otherwise it will fail. Unless the
% argument matches to what is defined on line 8, in this case 'scared'.
