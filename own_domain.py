#Create problem




    (:action moveEatFood 
        :parameters (?x ?y - position)
        :precondition (and (pacmanAt ?x) ( foodAt ?y))
        :effect (and (pacmanAt ?y) (isFree ?x)
                    (not (pacmanAt ?x))                
                    (not (foodAt ?y))
                )
    )
    
    (:action moveEatPower
        :parameters (?x ?y - position)
        :precondition (and (pacmanAt ?x) ( powerAt ?y))
        :effect (and (pacmanAt ?y) (isFree ?x)
                    (not (pacmanAt ?x))                
                    (not (powerAt ?y))
                )
    )
    (:action moveEatGhost
        :parameters (?x ?y - position)
        :precondition (and (pacmanAt ?x) (ghostAt ?y) (isGhostScared))
        :effect (and (pacmanAt ?y) (isFree ?x)
                    (not (pacmanAt ?x))                
                    (not (ghostAt ?y))
                    (not (isGhostScared))
                )
    )

