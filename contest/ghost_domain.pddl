
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
        (enemy_pacman_at ?x - position)
        
        ;not really needed for the ghost domain
        (food_at ?x - position)
        (power_at ?x - position)
        
        (connected ?x ?y - position)

        (ghost_scared)
        (enemy_pacman_dead)

        (enemy_ghost_at ?x - position)

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
                    ;(pacman_at p_11)
                    (not (ghost_at ?x))
                    (not (enemy_pacman_at ?y))
                    (enemy_pacman_dead)
                )
    )






)
