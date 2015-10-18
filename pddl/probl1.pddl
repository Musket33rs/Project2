; Tou Lee 656128
; Jaime Martinez 642231
( define ( problem pacman_1)
    (:domain pacman )
    (:objects
        p_11 p_12 p_13 p_14
        p_21 p_22 p_23 p_24
        p_31 p_32 p_33 p_34
        p_41 p_42 p_43 p_44 - position
    )
    
    (:init
        (connected p_11 p_12 ) ( connected p_12 p_11 )
        (connected p_12 p_13 ) ( connected p_13 p_12 )
        (connected p_13 p_14 ) ( connected p_14 p_13 )
        (connected p_11 p_21 ) ( connected p_21 p_11 )
        (connected p_21 p_31 ) ( connected p_31 p_21 )
        (connected p_31 p_41 ) ( connected p_41 p_31 )
        (connected p_41 p_42 ) ( connected p_42 p_41 )
        (connected p_42 p_43 ) ( connected p_43 p_42 )
        (connected p_43 p_44 ) ( connected p_44 p_43 )
        (connected p_34 p_44 ) ( connected p_44 p_34 )
        (connected p_13 p_23 ) ( connected p_23 p_13 )
        
        
        ( pacmanAt p_11 )
        ( ghostAt p_14 )
        ( powerAt p_44)
        
        ( foodAt p_12 )
        ( foodAt p_13 )
        ( foodAt p_21 )
        ( foodAt p_31 )
        ( foodAt p_41 )
        ( foodAt p_42 )
        ( foodAt p_43 )
        ( isFree p_23 )
        ( foodAt p_34 )
        
    )
    (:goal
        (and    (pacmanAt p_14)
        )
    )
    
)
    