/*initial conditions */ 
robot(3,s0). 
obstaculo(5,s0).

/*preconditions for primitive actions */ 
poss(avanzar,S):-robot(X,S),
                 Y is X+1,
                 \+obstaculo(Y,S). 

poss(retroceder,S):-robot(X,S),
                    Y is X-1, 
                    \+obstaculo(Y,S).

poss(agregar_obstaculo(X),S):-robot(Y,S),
							               (X is Y-1; X is Y+1),
							               \+obstaculo(X,S). 

poss(eliminar_obstaculo(X),S):-robot(Y,S),
							                 (X is Y-1; X is Y+1),
							                 obstaculo(X,S). 


 /*successor state axioms for primitive fluents */
 robot(X,do(A,S)):- robot(Y,S),
 					( 
 						(A=avanzar, X is Y+1);
 						(A=retroceder, X is Y-1)
 					);

 					(
 						robot(X,S),
 						\+A=avanzar,
 						\+A=retroceder

 					).

obstaculo(X,do(A,S)):- A=agregar_obstaculo(X);
					   obstaculo(X,S),
					   \+ A=eliminar_obstaculo(X).


/*legal axioms*/ 
legal(s0). 
legal(do(A,S)):-legal(S),poss(A,S).  

cambia_s2n(s0,ACC,ACC). 
cambia_s2n(do(A,S1),ACC,X):-cambia_s2n(S1,[A|ACC],X).  

/* translates  */ 
convierte(X,C) :- X=avanzar->C=1;
                  X=eliminar_obstaculo(_)->C=2;
                  X=retroceder ->C=3;
                  X=agregar_obstaculo(_)->C=4. 