from character_creation import character_creation
from world import World


def main():
    player = character_creation()
    input("\nPress Enter to continue to Elden village...")
    game = World(player)
    game.game_loop()


if __name__ == "__main__":
    main()
