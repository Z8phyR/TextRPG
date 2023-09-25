from utils import print_pause
from village import village
from forest import forest
import actions


class World:
    """
    A class representing the game world.

    Attributes:
    -----------
    player : Player
        The player object.
    rooms : dict
        A dictionary containing all the rooms in the game.
    command_map : dict
        A dictionary mapping commands to their corresponding handler functions.
    command_aliases : dict
        A dictionary mapping command aliases to their corresponding commands.

    Methods:
    --------
    get_command_handler(command: str) -> Tuple[Optional[Callable], str]:
        Returns the handler function for a given command.
    game_loop() -> None:
        The main game loop.
    """

    def __init__(self, player):
        """
        Initializes a new instance of the World class.

        Parameters:
        -----------
        player : Player
            The player object.
        """
        self.player = player
        self.rooms = {**village, **forest}
        self.command_map = {
            'north': actions.handle_move,
            'south': actions.handle_move,
            'east': actions.handle_move,
            'west': actions.handle_move,
            'attack': actions.handle_attack,
            'talk': actions. handle_talk,
            'exit': actions.handle_exit,
            'look': actions.handle_look,
            'take': actions.handle_take,
            'inventory': actions.handle_inventory,
            'stats': actions.handle_stats,
            'equip': actions.handle_equip,
            'unequip': actions.handle_unequip,
            'drop': actions.handle_drop,
            'use': actions.handle_use,
            'buy': actions.handle_buy,
            'sell': actions.handle_sell,
            'eq': actions.show_equipped,
            'attack': actions.start_battle
        }
        self.command_aliases = {
            'n': 'north',
            's': 'south',
            'e': 'east',
            'w': 'west',
            'get': 'take',
            'retrieve': 'take',
            'l': 'look',
            'i': 'inventory',
            'inv': 'inventory',
            'kill': 'attack',
            'atk': 'attack',
            'slay': 'attack',
            'quit': 'exit',

        }

    def get_command_handler(self, command):
        """
        Returns the handler function for a given command.

        Parameters:
        -----------
        command : str
            The command to get the handler function for.

        Returns:
        --------
        Tuple[Optional[Callable], str]
            A tuple containing the handler function and the actual command.
        """
        # Map alias to actual command
        actual_command = self.command_aliases.get(command, command)
        # Get the handler function
        return self.command_map.get(actual_command), actual_command

    def game_loop(self):
        """
        The main game loop.
        """
        print_pause(f"\nWelcome to the village of Elden, {self.player.name}!")
        current_room = self.rooms['start']
        display_description = True

        while True:
            if display_description:
                actions.display_room(current_room)

            player_bar = f"{actions.YELLOW}{self.player.name} {actions.END} | HP: {self.player.health} / {self.player.max_health} | Mana: {self.player.mana} | Exp: {self.player.experience} | Lvl: {self.player.level} |"
            print(f"\n< {player_bar} >")
            command = input(
                "What would you like to do? ").strip().lower().split(' ', 1)

            if not command[0]:
                continue

            action, target = command[0], command[1] if len(command) > 1 else ''
            handler, actual_command = self.get_command_handler(action)

            if handler:
                current_room, display_description = handler(
                    actual_command, target, current_room, self.player, self.rooms)
            else:
                print("Invalid command.")
