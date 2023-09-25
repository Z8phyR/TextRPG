import random
import math
from utils import print_pause

# ANSI escape codes for colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
END = '\033[0m'


def handle_inventory(action, target, current_room, player, rooms):
    print(f"{YELLOW}Inventory{END}")
    print("-" * len("Inventory"))
    for item in player.inventory.items:
        print(item.name)
    print("-" * len("Inventory"))
    return current_room, False


def handle_stats(action, target, current_room, player, rooms):
    print(f"{YELLOW}Stats{END}")
    print("-" * len("Stats"))
    print(f"HP: {player.health}")
    print(f"Mana: {player.mana}")
    print(f"Exp: {player.experience}")
    print(f"Lvl: {player.level}")
    print(f"Gold: {player.gold}")
    print("-" * len("Stats"))
    print(f"Class: {player.__class__.__name__}")
    print(f"Strength: {player.stats.strength}")
    print(f"Intelligence: {player.stats.intelligence}")
    print(f"Dexterity: {player.stats.dexterity}")
    print(f"Defense: {player.stats.defense}")
    print(f"Speed: {player.stats.speed}")
    print("-" * len("Stats"))
    return current_room, False


def handle_equip(action, target, current_room, player, rooms):
    if target:
        item_to_equip = next(
            (item for item in player.inventory.items if item.name.lower() == target.lower()), None)
        if item_to_equip:
            player.equip(item_to_equip)
            print(f"You equipped {item_to_equip.name}.")
        else:
            print("You don't have that item in your inventory.")
    else:
        show_equipped(action, target, current_room, player, rooms)

    return current_room, False


def handle_unequip(action, target, current_room, player, rooms):
    item_to_unequip = next((item for slot, item in player.equipped_items.items(
    ) if item and item.name.lower() == target.lower()), None)
    if item_to_unequip:
        player.unequip(item_to_unequip)
        print(f"You unequipped {item_to_unequip.name}.")
    else:
        print("You don't have that item equipped.")
    return current_room, False


def show_equipped(action, target, current_room, player, rooms):
    print(f"{YELLOW}Equipped{END}")
    print("-" * len("Equipped"))
    for slot, item in player.equipped_items.items():
        if item:
            print(f"{slot.capitalize()}: {item.name}")
        else:
            print(f"{slot.capitalize()}: None")
    print("-" * len("Equipped"))
    return current_room, False


def handle_move(action, target, current_room, player, rooms):
    return move_rooms(current_room, action, rooms), True


def handle_attack(action, target, current_room, player, rooms):
    # Your attack code here
    return current_room, True


def handle_take(action, target, current_room, player, rooms):
    target = target.lower()  # Make the target case-insensitive
    item_names = [item.name.lower() for item in current_room['items']]
    if target in item_names:
        item_to_take = [item for item in current_room['items']
                        if item.name.lower() == target][0]
        player.inventory.add_item(item_to_take)
        current_room['items'].remove(item_to_take)
        print(f"You picked up the {item_to_take.name}.")
    else:
        print("That item is not here.")
    return current_room, False


def handle_drop(action, target, current_room, player, rooms):
    target = target.lower()
    # print(f"Target: {target}")  # Debug print
    item_names = [item.name.lower() for item in player.inventory.items]
    # print(f"Item names: {item_names}")  # Debug print
    if target in item_names:
        item_to_drop = [
            item for item in player.inventory.items if item.name.lower() == target][0]
        # print(f"Item to drop: {item_to_drop}")  # Debug print
        player.inventory.remove_item(item_to_drop)
        current_room['items'].append(item_to_drop)
        print(f"You dropped the {item_to_drop.name}.")
    else:
        print("You don't have that item in your inventory.")
    return current_room, False


def handle_use(action, target, current_room, player, rooms):
    # Your use code here
    return current_room, False


def handle_look(action, target, current_room, player, rooms):
    display_room(current_room)
    return current_room, False


def handle_talk(action, target, current_room, player, rooms):
    if current_room['npcs']:
        npc_to_talk_to = None
        for npc in current_room['npcs']:
            if npc.name.lower() == target.lower():  # Case-insensitive comparison
                npc_to_talk_to = npc
                break
        if npc_to_talk_to:
            print(f"\n{npc_to_talk_to.name}: {npc_to_talk_to.dialogue}\n")
            if npc_to_talk_to.name == "Shopkeeper":
                print(f"{YELLOW}Items for sale:{END}")
                print("-" * len("Items for sale:"))
                for item in npc_to_talk_to.inventory.items:
                    print(f"{item.name} | Price: {item.cost}")
            elif npc_to_talk_to.name == "Elder":
                quest_item_name = "Goblin Leader's Head"
                if player.has_item(quest_item_name):
                    print(
                        f"{npc_to_talk_to.name}: Thank you for defeating the goblin leader! Here is your reward.")
                    quest_item = next(
                        item for item in player.inventory.items if item.name == quest_item_name)
                    player.inventory.remove_item(quest_item)
                    player.gold += 100
                    player.gain_experience(100)
                    print(f"You received 100 gold & 100 experience.")
        else:
            print("That person is not here.")
    else:
        print("There is no one to talk to here.")
    return current_room, False


def handle_buy(action, target, current_room, player, rooms):
    shopkeeper_list = [npc for npc in current_room['npcs']
                       if npc.name == "Shopkeeper"]
    if not shopkeeper_list:
        print("No shopkeeper here.")
        return current_room, False

    shopkeeper = shopkeeper_list[0]

    item_list = [
        item for item in shopkeeper.inventory.items if item.name.lower() == target.lower()]

    if not item_list:
        print(f"No item named {target} is available.")
        return current_room, False

    item_to_buy = item_list[0]

    if player.gold >= item_to_buy.cost:
        player.gold -= item_to_buy.cost
        player.inventory.add_item(item_to_buy)
        shopkeeper.inventory.remove_item(item_to_buy)
        print(f"You bought {item_to_buy.name} for {item_to_buy.cost} gold.")
    else:
        print("You don't have enough gold.")

    return current_room, False


def handle_sell(action, target, current_room, player, rooms):
    shopkeeper = [npc for npc in current_room['npcs']
                  if npc.name == "Shopkeeper"][0]
    item_to_sell = [
        item for item in player.inventory.items if item.name.lower() == target.lower()][0]
    if item_to_sell:
        # 80% of the item cost, rounded down
        sell_price = math.floor(item_to_sell.cost * 0.80)
        player.gold += sell_price  # Add the sell price to player's gold
        # Remove the item from player's inventory
        player.inventory.remove_item(item_to_sell)
        # Add the item to shopkeeper's inventory
        shopkeeper.inventory.add_item(item_to_sell)
        # Display the actual sell price
        print(f"You sold {item_to_sell.name} for {sell_price} gold.")
    else:
        print("You don't have that item.")
    return current_room, False


def move_rooms(current_room, command, rooms):
    if command in current_room['exits']:
        new_room_name = current_room['exits'][command]
        new_room = rooms[new_room_name]
        return new_room
    else:
        print("You can't go that way.")
        return current_room


def handle_exit(action, target, current_room, player, rooms):
    print_pause("Goodbye!")
    exit(0)


def display_room(room):
    print("-" * len(room['name']))
    print(f"{GREEN}{room['name']} {END}")
    print("-" * len(room['name']))
    exit_str = "| ".join(
        [f"{RED} {direction} {END}" for direction in room['exits']])
    print(f"Exits | {exit_str} |")
    print("-" * len(exit_str))
    print(room['description'] + "\n")
    for item in room['items']:
        print(f"{item.description}")
    for enemy in room['enemies']:
        print(f"{enemy.description}")
    for npc in room['npcs']:
        print(f"{npc.description}")


# Battle Actions
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


def handle_ability_in_battle(player, enemy):
    print("Available Abilities:")
    for idx, (ability_name, ability) in enumerate(player.abilities.items()):
        cooldown_remaining = player.ability_cooldowns.get(ability_name, 0)
        print(
            f"{idx + 1}. {ability_name} (Mana cost: {ability.cost}, Cooldown: {cooldown_remaining})")
        print(f"Ability Cooldown: {ability.cooldown}")
    choice = input("Which ability would you like to use? ")

    if choice.isdigit() and int(choice) <= len(player.abilities):
        ability_to_use = list(player.abilities.values())[int(choice) - 1]
        ability_name_to_use = list(player.abilities.keys())[
            int(choice) - 1]  # get the ability name

        if player.mana < ability_to_use.cost:
            print("Not enough mana.")
            return False

        cooldown_remaining = player.ability_cooldowns.get(
            ability_name_to_use, 0)
        if cooldown_remaining > 0:
            print("Ability is on cooldown.")
            return False

        # Use the Ability
        player.use_ability(ability_name_to_use, enemy)

        # Set the cooldown
        player.ability_cooldowns[ability_name_to_use] = ability_to_use.cooldown

        # Enemy Attacks
        enemy.attack(player)
        return True
    else:
        print("Invalid choice.")
        return False


def end_battle(player, enemy, current_room):
    print(f"{enemy.name} has been defeated!")
    player.gold += enemy.gold
    player.gain_experience(enemy.experience_reward)
    print(
        f"You have received {enemy.gold} gold and {enemy.experience_reward} experience.")
    for item in enemy.inventory.items:
        print(f"You received {item.name}.")
        player.inventory.add_item(item)
        enemy.inventory.remove_item(item)
    current_room['enemies'].remove(enemy)


def handle_attack_in_battle(player, enemy):
    player.attack(enemy)
    if not enemy.is_dead():
        enemy.attack(player)
        if player.is_dead():
            print_pause("You have died. Better luck next time!")


def handle_flee_in_battle(player, enemy):
    # 80% chance to flee successfully placing the player in the previous room
    if random.random() < 0.8:
        print_pause("You fled successfully.")
        player.battle_state = False
        enemy.battle_state = False
        return
    else:
        print_pause("You failed to flee.")
        enemy.attack(player)


def handle_defend_in_battle(player, enemy):
    player.is_defending = True
    print_pause("You are defending.")
    enemy.attack(player)

    player.is_defending = False  # reset defending flag


def handle_use_in_battle(player, enemy):
    print("Usable Items:")
    for idx, item in enumerate(player.inventory.items):
        if item.is_usable:
            print(f"{idx + 1}. {item.name}")

    choice = input("Which item would you like to use? ")

    if choice.isdigit() and int(choice) <= len(player.inventory.items):
        item_to_use = player.inventory.items[int(choice) - 1]
        if item_to_use.is_usable:
            player.use_item(item_to_use, enemy)
            enemy.attack(player)
            return True
        else:
            print("That item is not usable in battle.")
            return False
    else:
        print("Invalid choice.")
        return False
