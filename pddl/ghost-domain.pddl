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
        (ghost_at ?x - position)
        (pacman_at ?x - position)
        (connected ?x ?y - position)

        (ghost_scared)
        (pacman_dead)


    )

    (:action move
        :parameters (?x ?y)
        :precondition (and (ghost_at ?x) (connected ?x ?y) )
        :effect (and
                    (ghost_at ?y)
                    (not (ghost_at ?x))
                )
    )

    (:action moveToEatPacman
        :parameters (?x ?y)
        :precondition (and (ghost_at ?x) (connected ?x ?y) (not(ghost_scared)) (pacman_at ?y))
        :effect (and
                    (ghost_at ?y)
                    (pacman_at p_11)
                    (eat-pacman)
                    (not (ghost_at ?x))
                    (not (pacman_at ?y))
                    (not (pacman_dead))
                )
    )





)
