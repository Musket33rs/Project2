%﻿ Tou Lee 656128
% Jaime Martinez 642231
﻿(define (domain ghost)

    (:requirements
        :typing
    )

    (:types
        position - object
    )

    (:predicates
        (ghostAt ?x - position)
        (pacmanAt ?x - position)
        (connected ?x ?y - position)
        (ghost-normal)
        (pacman-alive)
        (eat-pacman)

    )

    (:action move
        :parameters (?x ?y)
        :precondition (and (ghostAt ?x) (connected ?x ?y) )
        :effect (and
                    (ghostAt ?y)
                    (not (ghostAt ?x))
                )
    )

    (:action moveToEatPacman
        :parameters (?x ?y)
        :precondition (and (ghostAt ?x) (connected ?x ?y) (ghost-normal) (pacman-alive) (pacmanAt ?y))
        :effect (and
                    (ghostAt ?y)
                    (pacmanAt p_11)
                    (eat-pacman)
                    (not (ghostAt ?x))
                    (not (pacmanAt ?y))
                    (not (pacman-alive))
                )
    )





)
