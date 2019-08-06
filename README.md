# doves_hawks_seagulls

Requires Matplotlib library


This script simulates the behaviour of the creatures: 
											
                      1. "doves"  - cowardly (don't fight)
											
                      2. "hawks" - aggressive (always fight to the end)
											
                      3. "seagulls" - semi-aggressive (fight cowards and each other)

with this setup there is a limited amount of food. Each food gives two points.

A creature needs 1 food point to survive to the next day. 

If a creature has less than 1 point it has a (1-points)% chance to die.

If it gets more than 1 point it has a (points-1)) % chance to reproduce.

If two creatures approach same piece of food they compete for it according to the relative weights of their behaviour models.

Every day previous food dissappears, new food spawns, creatures "search" for food, then the kill/reproduce actions are resolved.

To create proper data the amount of days should better be inbetween 1000 and 10000.


Current weights setup:

    doves : doves  			   1  :  1  		doves share 

    doves : hawks 		 	 0.5  :  1.5 		hawks take 50% of doves' share

    doves : seagulls 		 0.75 :  1.25 		seagulls take 25% of doves' share

    hawks : hawks 		 	   0  :  0 		hawks waste too much energy and die fighting

    hawks : seagulls	 	   1  :  0.75   	seagulls run but lose 25% of their share

    seagulls : seagulls       	 0.25  :  0.25 		seagulls fight and lose 75% of their share
    


Later might want to readjust the weights to energy cost.

Looks like with the current wights setup and amount of food most of the times the doves can't survive through set
number of days. 
