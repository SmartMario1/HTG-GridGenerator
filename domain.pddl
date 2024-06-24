; This domain consists of a grid with a movable and objectives. The movable can move to adjacent nodes.
; Any node can be made adjacent to any other node that has just one node between them.
; which results in cubic action scaling with respect to the amount of nodes.
(define (domain htg-grid)

(:requirements :strips :typing)

(:types
    movable objective node
)

(:predicates
    (connected ?node1 - node ?node2 - node)
    (at-movable ?movable - movable ?node - node)
    (at-objective ?objective - objective ?node - node)
    (collected ?objective - objective)
)

;define actions
(:action move
    :parameters (?movable - movable ?nodefrom - node ?nodeto - node)
    :precondition (and  (at-movable ?movable ?nodefrom)
                        (connected ?nodefrom ?nodeto))
    :effect (and (not (at-movable ?movable ?nodefrom))
                 (at-movable ?movable ?nodeto))
)

(:action collect
    :parameters (?movable - movable ?objective - objective ?node - node)
    :precondition (and  (at-movable ?movable ?node)
                        (at-objective ?objective ?node))
    :effect (and (not (at-objective ?objective ?node))
                 (collected ?objective))
)

; This is the action that makes this domain HTG. Scales cubically with amount of nodes.
(:action connect
    :parameters (?nodefrom - node ?nodebetween - node ?nodeto - node)
    :precondition (and  (connected ?nodefrom ?nodebetween)
                        (connected ?nodebetween ?nodeto))
    :effect (and    (connected ?nodefrom ?nodeto)
                    (connected ?nodeto ?nodefrom))
)



)
