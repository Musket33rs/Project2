% pman.pl

%init
pmanAt(1,1,s0).

connectedRight(X,Y1,X,Y2):- \+isWall(X,Y2),
    (Y2 is Y1+1).
connectedLeft(X,Y1,X,Y2):- \+isWall(X,Y2),
      (Y2 is Y1-1).
connectedUp(X1,Y,X2,Y):- \+isWall(X2,Y),
      (X2 is X1+1).
connectedDown(X1,Y,X2,Y):- \+isWall(X2,Y),
      (X2 is X1-1).

%connected(1,2,1,1,s0).
hasFood(1,0,s0).
isFree(1,3,s0).
ghostAt(4,4,s0).
isWall(0,0).


%preconditions
poss(moveRight,S):- pmanAt(X,Y,S), connectedRight(X,Y,X,Y1),
                  (Y1 is Y+1),
                  (isFree(X,Y1,S);hasFood(X,Y1,S)),
                  \+ghostAt(X,Y1,S).
poss(moveLeft,S):- pmanAt(X,Y,S),isFree(X,Y1,S), connectedLeft(X,Y,X,Y1),
                  (Y1 is Y-1),
                  \+ghostAt(X,Y1,S).
poss(moveUp,S):- pmanAt(X,Y,S),isFree(X1,Y,S), connectedUp(X,Y,X1,Y),
                  (X1 is X+1),
                  \+ghostAt(X1,Y,S).
poss(moveDown,S):- pmanAt(X,Y,S),isFree(X1,Y,S), connectedDown(X,Y,X1,Y),
                  (X1 is X-1),
                  \+ghostAt(X1,Y,S).

%success state axioms move
pmanAt(X,Y,do(A,S)):-pmanAt(X1,Y1,S),
      (
        (A=moveRight,(Y is Y1+1),(X1=X));
        (A=moveLeft,(Y is Y1-1),(X1=X));
        (A=moveUp,(X is X1+1),(Y1=Y));
        (A=moveDown,(X is X1-1),(Y1=Y))
      );
      (
        pmanAt(X,Y,S),
        \+ A=moveRight;
        \+ A=moveLeft;
        \+ A=moveUp;
        \+ A=moveDown
      ).



/*legal axioms*/
  legal(s0).
  legal(do(A,S)):-legal(S),poss(A,S).

  cambia_s2n(s0,ACC,ACC).
  cambia_s2n(do(A,S1),ACC,X):-cambia_s2n(S1,[A|ACC],X).

  /* translates  */
  convierte(X,C) :- X=moveRight->C=1;
                    X=moveLeft->C=2;
                    X=moveUp ->C=3;
                    X=moveDown->C=4.
