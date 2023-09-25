from character import NPC, Enemy, Weapon, Item, Potion, Scroll


def initialize_village(village):
    elder = NPC("Elder", 100, 100, "The village elder stands here. He looks very wise",
                "Welcome to our village! We have a quest for you! Defeat the goblin leader in the forest to the south and you will be rewarded handsomely.")
    shopkeeper = NPC("Shopkeeper", 100, 100, "The shopkeeper stands here. He looks bored.",
                     "Welcome to my shop! I have many items for sale.")
    potion = Potion(
        "Potion", 20, 10, "A potion that restores 10 health glimmers from the dirt.")
    scroll = Scroll(
        "Scroll", 20, 10, "A scroll with strange writing on it collects dust on the ground.")
    sword = Weapon(
        "Sword", 50, 5, "A sword that does 5 damage sticks out from the earth.")
    shopkeeper.inventory.add_item(potion)
    shopkeeper.inventory.add_item(sword)
    village['center']['npcs'] = [elder]
    village['shop']['npcs'] = [shopkeeper]
    village['west_square']['items'] = [scroll]


village = {
    'start': {
        'name': 'Village Entrance',
        'description': 'You are at the entrance of a small village. There is a path leading south to the village center.',
        'exits': {'south': 'center'},
        'items': [],
        'enemies': [],
        'npcs': []
    },
    'center': {
        'name': 'Village Center',
        'description': 'You are in the center of the village. Paths lead in all directions.',
        'exits': {'south': 'forest_entrance', 'north': 'start', 'east': 'shop', 'west': 'west_square'},
        'items': [],
        'enemies': [],
        'npcs': []
    },
    'shop': {
        'name': 'Shop',
        'description': 'You are in the village shop. You can buy items here. The path back to the center is to the west.',
        'exits': {'west': 'center'},
        'items': [],
        'enemies': [],
        'npcs': []
    },
    'west_square': {
        'name': 'West Square',
        'description': 'You are in the west square of the village. The center is to the east.',
        'exits': {'east': 'center'},
        'items': [],
        'enemies': [],
        'npcs': []
    },
}

initialize_village(village)
