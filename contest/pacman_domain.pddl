
(define (domain pacman)

    (:requirements
     :typing
    )

    (:types position - object)

    (:predicates
        ( pacman_at ?x - position )
        ( ghost_at ?x - position)
        ( connected ?x ?y - position )
        ( is_free ?x - position)
        ( enemy_ghost_at ?x - position )
        ( enemy_pacman_at ?x - position )
        ( food_at ?x - position )
        ( power_at ?x - position)
        ( ghost_scared )
        ( pacman_dead )
        

    )

    (:action move 
        :parameters (?x ?y - position)
        :precondition (and (pacman_at ?x) (connected ?x ?y) (not (enemy_ghost_at ?y)) )
        :effect (and  (pacman_at ?y) 
                      ( not (pacman_at ?x))       
                      ( not (pacman_dead))
                        
                )
    )
    (:action move_eat_food 
        :parameters (?x ?y - position)
        :precondition (and (pacman_at ?x) (connected ?x ?y) ( food_at ?y))
        :effect (and (pacman_at ?y) (is_free ?x)
                    (not (pacman_at ?x))                
                    (not (food_at ?y))
                )
    )
    (:action move_eat_power
        :parameters (?x ?y - position)
        :precondition (and (pacman_at ?x) (connected ?x ?y) ( power_at ?y) (not (enemy_ghost_at ?y)))
        :effect (and (pacman_at ?y) (ghost_scared) (is_free ?x)
                    (not (pacman_at ?x))                
                    (not (power_at ?y))
                )
    )
    (:action move_eat_ghost
        :parameters (?x ?y - position)
        :precondition (and (pacman_at ?x) (connected ?x ?y) ( enemy_ghost_at ?y) (ghost_scared))
        :effect (and (pacman_at ?y) (is_free ?x)
                    (not (pacman_at ?x))                
                    (not (ghost_at ?y))
                    (not (ghost_scared))
                )
    )
)