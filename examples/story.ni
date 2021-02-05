"The Dungeon" by "Markus Schatten".


Release along with an interpreter.
Release along with a website.
Release along with the introductory booklet.

When play begins:
	say "You find yourself in a dungeon surrounded by darkness. The stench is awful." ;


The pit is a room. The description is "This is the place you woke up. What a scary place!"

A torch is here. The description is "You can see a dim light flickering a few steps away from you."

The tunnel is a room. It is south of the pit. The description is "[if we have not taken the torch]A dark and small tunnel seemingly going nowhere[otherwise]The tunnel seems to be leading somewhere[end if]".

Instead of going to the torture chamber:
	if we have not taken the torch:
		say "It is to dark in there!" ;
	otherwise:
		Move the player to the torture chamber.

The torture chamber is a room. It is south of the tunnel. The description is "A medieval torture chamber".

The lair is west from the torture chamber.

The hatchery is east from the torture chamber.

A Chest is in the pit. It is an openable container. It is closed. The description is "An old wodden chest lies on the floor."

An old smelly cheese is inside the Chest. It is edible.

The description of the lair is "Creatures seem to be resting here. There is a stone bed full of dirty looking hair."

A bed is in the lair. It is scenery.

An Orc lady is a woman. Orc lady is in the torture chamber. The description is "A green skinned but blond haired orcish lady. Well that's a lot of make-up!"

Instead of asking Orc lady about "this place", say "Orc lady: [italic type]Oh, you mean my home? It's cozy, isn't it?[roman type]"

Instead of asking Orc lady about "torture chamber", say "Orc lady looks at you and winks."

Feeding cheese is an action applying to one visible thing. Understand "feed [someone] with cheese" as feeding cheese.

Check feeding cheese:
	if the noun is not a person, say "You can only feed creatures." instead.

Instead of feeding cheese:
	if the noun is the orc lady:
		say "You feed [the noun] with cheese. She is munching it down, grunting happily. You see something falling down. It seems to be a key. You grab it while she isn't looking.";
		Move the iron key to the player;
	otherwise:
		say "You try feeding [the noun] with cheese, but there is no reaction."

The treasure chamber is a room. "A treasure chamber full of gold, jewels and precious gems."

The iron door is a door. It is locked. The iron key unlocks it. The iron door is south of the torture chamber and north of the treasure chamber.

The sceptre of foul cheese is in the treasure chamber. "Ahh... The sceptre of foul cheese. It is magical. It can turn anything to cheese."

Instead of taking the sceptre of foul cheese:
	end the story finally saying "You have found it, the most precious treasure. You can now turn the whole dungeon with all its walls into ridicioulus amounts of cheese. And eat your self out. "



