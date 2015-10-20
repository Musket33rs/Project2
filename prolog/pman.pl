% pman.pl

%init
pmanAt(1,1,s0).
hasFood(2,2).
ghostAt(4,4).
powerAt(3,3).
isConnected(X,Y1,X,Y2):-(Y2 is Y1+1);(Y2 is Y1-1).
%isConnected(X,Y1,X,Y2):-(Y2 is Y1-1).
isConnected(X1,Y,X2,Y):-(X2 is X1+1);(X2 is X1-1).
%isConnected(X1,Y,X2,Y):-(X2 is X1-1).


%preconditions
poss(move(X1,Y1),S):- pmanAt(X,Y,S),isConnected(X,Y,X1,Y1),
                  \+ghostAt(X1,Y1).
poss(eatFood,S):-hasFood(X,Y,S),pmanAt(X,Y,S).
poss(eatPower,S):-powerAt(X,Y,S),pmanAt(X,Y,S).
poss(eatGhost,S):-hasFood(X,Y,S),pmanAt(X,Y,S).
%success state axioms move
pmanAt(X,Y,do(A,S)):-pmanAt(X1,Y1,S),
      (
        (A=move(X,Y),isConnected(X1,Y1,X,Y))
      );
      (
        pmanAt(X,Y,S),
        \+ A=move(X,Y)
      ).



/*legal axioms*/
  legal(s0).
  legal(do(A,S)):-legal(S),poss(A,S).
