"Evil elf's castle" by Tomislav Peharda
Release along with an interpreter.
Release along with a website.
Release along with the introductory booklet.

When play begins:
	say "You just entered evil elf's castle who don't want to let you go! Hurry and escape the castle before you get trapped in there forever. Be careful, elfs have their tricks."
	
The player carries a torch, an apple and a bottle.

The entrance is a room. The description is "This is the entrance of a castle that you shouldn't have ever entered.".
A black box is in the entrance. It is an openable container. It is closed. It is fixed in place. A gold coin is inside the black box. A silver coin is inside the black box.
A red box is in the entrance. It is an openable container. It is open. It is fixed in place. A wooden coin is inside the red box.
Aquatic elf is a woman. Aquatic elf is in the entrance.

The kitchen is a room. It is west of the entrance. The description is "Kitchen is a place where evil elfs like to gather to indulge themselves in food.".
A purple crate is in the kitchen. It is an openable container. It is open. It is fixed in place. A spoon is in the purple crate. A knife is in the purple crate.
A blue create is in the kitchen. It is an openable container. It is open. It is fixed in place. A fork is inside the blue crate.
Dark elf is a man. Dark elf is in the kitchen.
Deep elf is a man. Deep elf is in the kitchen.
Grey elf is a woman. Grey elf is in the kitchen.

The bathroom is a room. It is east of the the kitchen. The description is "Bathroom...".
A yellow locker is in the bathroom. It is an openable container. It is closed. It is fixed in place. A towel is in the yellow chest. A brush is in the yellow chest.

The hallway is a room.  It is south of the bathroom. The description is "Hope not too many elfs pass by.".
A green case is in the hallway. It is an openable container. It is open. It is fixed in place. A pen is in the green case. A pencil is in the green case.
A cyan case is in the hallway. It is an openable container. It is closed. It is fixed in place.
A white case is in the hallway. It is an openable container. It is open. It is fixed in place. A hat is in the white case.
High elf is a man. High elf is in the hallway.
Moon elf is a woman. Moon elf is in the hallway.

The garage is a room. It is north of the hallway. The description is "Garage sounds like a place plenty with tools.".
A pink box is in the garage. It is an openable container. It is open. It is fixed in place. A hammer is in the pink box.
A brown box is in the garage. It is an openable container. It is open. It is fixed in place. A screwdriver is in the brown box.
Snow elf is a woman. Snow elf is in the garage.
Sun elf is a woman. Sun elf is in the garage.

The bedroom is a room. It is west of the garage. The description is "Silently here, shhh...".
An orange create is in the bedroom. It is an openable container. It is closed. It is fixed in place. A pillow is in the orange crate.
Wild elf is a woman. Wild elf is in the bedroom.
Wood elf is a woman. Wood elf is in the bedroom.
Winged elf is a man. Winged elf is in the bedroom.

Disarming is an action applying to nothing. Understand "disarm" as disarming.
Instead of disarming:
	if the player carries anything:
		say "Elf disarmed you";
		now everything carried by the player is in the location;
	otherwise:
		say "Elf tried to disarm you, but you carry nothing"
	
Teleporting is an action applying to nothing. Understand "teleport" as teleporting.
Instead of teleporting:
	say "Elf teleported you to a different room...";
	move the player to a random room