from utils import print_pause
from character import Character, Warrior, Mage, Hunter


def allocate_points(player, stat, points):
    try:
        amount = int(
            input(f"How many points would you like to allocate to {stat}? "))
        if amount > points:
            print_pause(
                f"You don't have that many points left. You have {points} remaining.")
            return points
        if amount + getattr(player.stats, stat) > 10:
            print_pause(
                "You can't allocate more than 10 points to a single stat.")
            return points
        setattr(player.stats, stat, getattr(player.stats, stat) + amount)
        return points - amount
    except ValueError:
        print_pause("Invalid input. Please enter an integer.")
        return points


def character_creation():
    print_pause("Welcome to TextRPG!")
    name = input("What's your name, adventurer? ")
    print_pause(f"Welcome, {name}!\n")
    print_pause("You are a young adventurer, eager to make a name for yourself.")
    player = Character(name, 100, 100)
    # print(player.display_stats())

    # Class selection
    print_pause("Choose your class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Hunter")
    class_choice = input(
        "Enter the number corresponding to your class choice: ")

    if class_choice == '1':
        player = Warrior(name, 100, 50)
    elif class_choice == '2':
        player = Mage(name, 100, 100)
    elif class_choice == '3':
        player = Hunter(name, 100, 50)
    else:
        print_pause("Invalid choice. Defaulting to Warrior.")
        player = Warrior(name, 100, 50)

    # Let's allocate some stat points
    print_pause("You have 5 stat points to allocate.")
    print_pause(
        "You can allocate them to strength, intelligence, dexterity, defense, or speed.")

    points = 5
    stats = ["strength", "intelligence", "dexterity", "defense", "speed"]

    for stat in stats:
        points = allocate_points(player, stat, points)
        print(f"You have {points} points remaining.")

    print_pause("Stat allocation complete!")
    print(player.display_stats())
    return player
