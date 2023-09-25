from character import NPC, Enemy, QuestItem

forest = {
    'forest_entrance': {
        'name': 'Forest Entrance',
        'description': 'You are at the entrance of a dark forest. The village is to the north.',
        'exits': {'north': 'center', 'south': 'clearing'},
        'items': [],
        'enemies': [],
        'npcs': []
    },
    'clearing': {
        'name': 'Forest Clearing',
        'description': 'You are in a clearing in the forest. There is a path leading north back to the village.',
        'exits': {'north': 'forest_entrance', 'south': 'cave'},
        'items': [],
        'enemies': [],
        'npcs': []
    },
    'cave': {
        'name': 'Cave',
        'description': 'You are in a cave. There is a path leading north back to the forest clearing.',
        'exits': {'north': 'clearing', 'south': 'boss_room'},
        'items': [],
        'enemies': [],
        'npcs': []
    },
    'boss_room': {
        'name': 'Boss Room',
        'description': 'You are in a large room. There is a path leading north back to the cave.',
        'exits': {'north': 'cave'},
        'items': [],
        'enemies': [],
        'npcs': []
    }
}


def create_goblin():
    goblin = Enemy("Goblin", 50, 50,
                   "A small goblin stands here. He looks angry.")
    return goblin


def create_goblin_leader():
    goblin_leader = Enemy("Goblin Leader", 100, 100,
                          "A large goblin stands here. He looks very angry.")
    return goblin_leader


def initialize_forest(forest):
    forest['forest_entrance']['enemies'] = [create_goblin()]
    forest['clearing']['enemies'] = [create_goblin()]
    forest['cave']['enemies'] = [create_goblin()]
    leader = create_goblin_leader()
    quest_item = QuestItem(
        "Goblin Leader's Head", "The head of the goblin leader. It's still warm.")
    leader.inventory.add_item(quest_item)
    forest['boss_room']['enemies'] = [leader]


initialize_forest(forest)
