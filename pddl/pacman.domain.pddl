; Tou Lee 656128
; Jaime Martinez 642231
(define (domain pacman)

    (:requirements
     :typing
    )

    (:types position - object)

    (:predicates
        ( pacmanAt ?x - position )
        ( connected ?x ?y - position )
        ( isFree ?x - position)
        ( ghostAt ?x - position )
        ( foodAt ?x - position )
        ( powerAt ?x - position)
        ( isGhostScared )

    )

    (:action move 
        :parameters (?x ?y - position)
        :precondition (and (pacmanAt ?x) (connected ?x ?y) (isFree ?y))
        :effect (and  (pacmanAt ?y) (isFree ?x)
                        ( not (pacmanAt ?x))       
                        (not (isFree ?y))
                )
    )
    (:action moveEatFood 
        :parameters (?x ?y - position)
        :precondition (and (pacmanAt ?x) (connected ?x ?y) ( foodAt ?y))
        :effect (and (pacmanAt ?y) (isFree ?x)
                    (not (pacmanAt ?x))                
                    (not (foodAt ?y))
                )
    )
    (:action moveEatPower
        :parameters (?x ?y - position)
        :precondition (and (pacmanAt ?x) (connected ?x ?y) ( powerAt ?y))
        :effect (and (pacmanAt ?y) (isGhostScared) (isFree ?x)
                    (not (pacmanAt ?x))                
                    (not (powerAt ?y))
                )
    )
    (:action moveEatGhost
        :parameters (?x ?y - position)
        :precondition (and (pacmanAt ?x) (connected ?x ?y) ( ghostAt ?y) (isGhostScared))
        :effect (and (pacmanAt ?y) (isFree ?x)
                    (not (pacmanAt ?x))                
                    (not (ghostAt ?y))
                    (not (isGhostScared))
                )
    )
)