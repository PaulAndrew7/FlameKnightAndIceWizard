# Description
This is a clone of the game Fireboy and Watergirl made using Raylib in Python. It features easy level editing and creation using Tiled and also enemy AI which is original to this game.

# Features
## Two Player Adventure
The game is meant to be played by two players. One controls Flame Knight and the other controls Ice Wizard. Players must co-operate together to solve the puzzles, avoid enemies and escape the dungeon.

![image](https://github.com/user-attachments/assets/e300f5d1-a007-4728-9b3a-ad3596ac8e54)

Flame Knight and Ice Wizard as seen in the game. Made using Stable Diffusion AnimaPencil,  Pixelator, PixelOver and Photoshop.

## Level Design using Tiled
Tiled is a free and open source software that makes creating 2D levels easy. It also exports the tile placements as JSON. The game reads this JSON file and places the platforms and obstacles in the game according to the JSON. This allows for custom level generation.

![image](https://github.com/user-attachments/assets/0a455b6e-b413-4957-9d3f-7919f70357d9)

## Buttons, Levers and Elevators
They are the most essential part of this game. They must be carefully interacted with to ensure that the players reach their goal successfully. As long as a player is touching a button, it remains activated. Each button activates a corresponding elevator. Multiple buttons can activate the same elevator aswell.

![image](https://github.com/user-attachments/assets/3c0b2eb9-4d27-4ead-a2a6-a40c042e8950)

Button Turned Off &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;  Button Turned On


Levers are turned on when a player touches them and presses ‘S’ (for Flame Knight)
or Down Arrow (for Ice Wizard). They toggle on and off each time they are
interacted with and activate a corresponding elevator.

![image](https://github.com/user-attachments/assets/625437af-cac2-45b5-8989-8d153ee1b2f2)

Lever Turned On &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;  Lever Turned Off

Elevators are of two types: The first type keeps moving up and down (or left and
right) between a specified range. The second type moves to a specified position
when active and returns back to its original position when inactive.

![image](https://github.com/user-attachments/assets/fb128550-315f-46b6-8719-bd756d17ba4c)

 &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Elevator

 ## Hazards
 There are certain types of hazards present in the level: Lava kills Ice Wizard, Water
kills Flame Knight and Goo kills both players. These can also function as pathways to
one player while being a threat to the other.

![image](https://github.com/user-attachments/assets/3a7e2118-6f6e-4b54-9f56-0fa148b79954)

 &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Goo

 ![image](https://github.com/user-attachments/assets/5392aed0-9852-43d6-b0b2-15ff4015323d)

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Water&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;  Lava

## Goals
The game ends when both Flame Knight and Ice Wizard reach their respective goals.

![image](https://github.com/user-attachments/assets/67a543ad-dcb5-4d3f-960e-6bd5174961d8)

 &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Goals

 ## Menus
 The game features a main menu and a level selector. The level selector only displays
the levels that have been unlocked and locked levels with chains.

![image](https://github.com/user-attachments/assets/2db38472-7e41-41fe-80b9-2cd68c0a8e81)

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Main Menu&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Level Selector with Locked Level

## Enemies
These are the AI agents that hunt for the player. The game ends when the enemy touches either of the players. These enemies remain inactive at first till a player enters their range. Once they do, the enemy becomes active and moves towards the player. However, if the player is on the same elevation as the enemy and looking directly at the enemy, then it does not move and closes its eyes. It always finds the nearest player and follows them.

![image](https://github.com/user-attachments/assets/a41d9976-f75d-4690-96fb-af4ab7429876)


&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Enemy Inactive&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Enemy Active

# Gameplay Screenshots

![image](https://github.com/user-attachments/assets/aa648cba-076f-4cb2-b19f-e9c7b8ba104e)

![image](https://github.com/user-attachments/assets/73ad9fdd-56ea-4b37-9ff9-272c354b1cdf)


