# Text-based RPG Game

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Code Examples](#code-examples)
- [Challenges](#challenges)
- [What I Learned](#what-i-learned)
- [Credits](#credits)
- [Contact](#contact)

## Introduction

This project is a text-based Role Playing Game (RPG) built with Python. The game features a variety of classes, items, and abilities, offering an immersive experience in a fantasy setting.

## Features

- Multiple Character Classes: Warrior, Mage, Hunter
- Inventory System: Weapons, Armor, Potions, and more
- Battle System: Turn-based combat with different abilities
- NPCs: Interact with NPCs like Shopkeepers and Village Elders
- Quest System: Complete quests for rewards

## Tech Stack

- Python 3.x

## Installation

Clone this repository and navigate into the project directory. Run the game using Python 3.

```bash
git clone https://github.com/yourusername/text-based-rpg.git
cd text-based-rpg
python main.py
```

## Usage

To start the game, run `python main.py`.

Game Commands:

- `attack`: To attack an enemy
- `defend`: To defend against an enemy attack
- `ability`: To use a special ability
- `use`: To use an item from the inventory
- `flee`: To run away from a battle

## Screenshots

![Game Start](./screenshots/start.png)
![Battle](./screenshots/battle.png)

## Code Examples

An example of starting a battle_loop within the game world:

```python
def start_battle(action, target, current_room, player, rooms):
    """
    Starts a battle between the player and an enemy in the current room.

    Parameters:
    action (str): The action to perform.
    target (str): The target of the action.
    current_room (dict): The current room the player is in.
    player (Player): The player object.
    rooms (list): The list of all rooms in the game.

    Returns:
    tuple: A tuple containing the updated current room and a boolean indicating if the player has won the battle.
    """
    enemy = None
    for e in current_room['enemies']:
        if e.name.lower() == target.lower():
            enemy = e
            break

    if enemy is None:
        print("No such enemy here.")
        return current_room, False

    print("Starting battle...")
    player.battle_state = True
    enemy.battle_state = True

    print_pause(f"You are now in battle with {enemy.name}!")
    while player.health > 0 and enemy.health > 0 and player.battle_state and enemy.battle_state:
        valid_action_taken = False
        print("-----------")
        print("Battle Menu")
        print("-----------")
        print("Attack | Ability | Defend | Use | Flee")
        print("-----------")
        battle_action = input("What would you like to do? ")
        if battle_action.lower() == "attack":
            handle_attack_in_battle(player, enemy)
            valid_action_taken = True
        elif battle_action.lower() == "ability":
            valid_action_taken = handle_ability_in_battle(player, enemy)
        elif battle_action.lower() == "defend":
            handle_defend_in_battle(player, enemy)
            valid_action_taken = True
        elif battle_action.lower() == "use":
            valid_action_taken = handle_use_in_battle(player, enemy)
        elif battle_action.lower() == "flee":
            handle_flee_in_battle(player, enemy)
            valid_action_taken = True
        else:
            print("Invalid command.")
            valid_action_taken = False

        if valid_action_taken:
            player.decrement_cooldowns()

    player.battle_state = False
    enemy.battle_state = False
    if enemy.is_dead():
        end_battle(player, enemy, current_room)
    return current_room, False


```

## Challenges

Some of the major challenges I faced during the development of this game included:

- Properly organizing and setting up attributes for classes
- Linking up Items and Weapons: Getting the items to interact correctly with the player's inventory and being able to equip or use them
- Entity Management: Creating individual enemy entities and populating different areas of the game with them
- Implementing a Cooldown System: Designing and implementing a round-based cooldown system for abilities
- Questing: Implementing a quest system that allows for player interaction and reward mechanics

## What I Learned

In the course of this project, I acquired a wealth of insights and skills:

- **Object-Oriented Programming**: Mastered the fundamentals of class instantiation in Python, providing a solid foundation for more complex projects.

- **Game Loops**: Developed proficiency in creating game loops to manage player actions, and further extended this concept to nested loops for specific scenarios like battles.

- **Command Mapping**: Implemented a command mapping system where each player command triggers a corresponding function, streamlining the game's internal logic.

- **Alias Mapping**: Enhanced user experience by incorporating an alias map for commands, allowing for more intuitive gameplay.

- **Modular Design**: Embraced the principles of modular design by breaking the game down into smaller, reusable components like functions and classes, which significantly improved the maintainability and reusability of the code.

- **State Management**: Gained a strong understanding of how to manage and update the state of various game elements, including players, enemies, and items.

- **Data Structures**: Applied practical use of data structures like lists, dictionaries, and classes to effectively store and manage game data.

- **Error Handling**: Built a robust system capable of gracefully handling and recovering from user input errors and unexpected game states.

- **Game Logic and Flow**: Acquired a deep understanding of game mechanics and rules, which was crucial for creating a compelling and balanced game experience.

- **User Experience**: Learned the importance of user-centered design principles, such as providing easy-to-understand instructions, meaningful feedback, and an intuitive command interface.

## Credits

Special thanks to GPT-4 for assisting in debugging and providing valuable code snippets throughout the development process.

## Contact

For any questions or inquiries, please contact me at [z8phyr@hotmail.com].
