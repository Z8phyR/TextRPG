class Character:
    """
    A class representing a character for our text-based RPG game.

    Attributes:
    - name (str): the name of the character
    - gold (int): the amount of gold the character has
    - experience (int): the amount of experience the character has
    - level (int): the level of the character
    - health (int): the current health of the character
    - mana (int): the current mana of the character
    - max_health (int): the maximum health of the character
    - stats (Stats): the stats of the character
    - inventory (Inventory): the inventory of the character
    - abilities (dict): the abilities of the character
    - equipped_items (dict): the equipped items of the character
    - battle_state (bool): the battle state of the character
    - is_defending (bool): whether the character is defending or not
    - ability_cooldowns (dict): the cooldowns of the character's abilities
    """

    def __init__(self, name, health, mana, max_health=100, level=1, gold=100, experience=0):
        self.name = name
        self.gold = gold
        self.experience = experience
        self.level = level
        self.health = health
        self.mana = mana
        self.max_health = max_health
        self.stats = Stats(strength=5, intelligence=5,
                           dexterity=5, defense=5, speed=5)
        self.inventory = Inventory(capacity=10)
        self.abilities = {}
        self.equipped_items = {'weapon': None, 'armor': None}
        self.battle_state = False
        self.is_defending = False
        self.ability_cooldowns = {}

    def decrement_cooldowns(self):
        """
        Decrements the cooldowns of the character's abilities.
        """
        for ability_name, cooldown in list(self.ability_cooldowns.items()):
            ability = self.abilities.get(ability_name)
            if ability and ability.is_used:
                self.ability_cooldowns[ability_name] = max(0, cooldown - 1)
                if self.ability_cooldowns[ability_name] == 0:
                    ability.is_used = False  # Reset the flag

    def restore_health(self, amount):
        """
        Restores the character's health by the given amount.

        Args:
        - amount (int): the amount of health to restore
        """
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def attack(self, target):
        """
        Attacks the given target.

        Args:
        - target (Character): the target to attack
        """
        if self.is_dead():
            return
        if target.is_dead():
            return

        print(f"{self.name} attacks {target.name}!")
        weapon = self.equipped_items.get('weapon', None)
        damage = self.stats.strength + (weapon.damage if weapon else 0)
        if target.is_defending:
            damage = max(0, damage - target.stats.defense)

        target.health -= damage
        print(f"{self.name} dealt {damage} damage to {target.name}!")

        if target.is_dead():
            return
        print(f"{target.name} Health: {target.health}")

    def equip(self, item):
        """
        Equips the given item.

        Args:
        - item (Item): the item to equip
        """
        if isinstance(item, Weapon):
            if self.equipped_items['weapon'] is not None:
                print("You already have a weapon equipped!")
                return

            self.equipped_items['weapon'] = item
            self.stats.strength += item.damage  # Or however you wish to modify stats
            self.inventory.remove_item(item)
        elif isinstance(item, Armor):
            if self.equipped_items['armor'] is not None:
                print("You already have armor equipped!")
                return

            self.equipped_items['armor'] = item
            self.stats.defense += item.defense  # Or however you wish to modify stats
            self.inventory.remove_item(item)

    def unequip(self, item):
        """
        Unequips the given item.

        Args:
        - item (Item): the item to unequip
        """
        if item == self.equipped_items.get('weapon', None):
            self.inventory.add_item(item)
            self.stats.strength -= item.damage  # Reverse the stat modification
            self.equipped_items['weapon'] = None
        elif item == self.equipped_items.get('armor', None):
            self.inventory.add_item(item)
            self.stats.defense -= item.defense  # Reverse the stat modification
            self.equipped_items['armor'] = None
        else:
            print("You don't have that item equipped!")

    def use_item(self, item, target):
        """
        Uses the given item on the given target.

        Args:
        - item (Item): the item to use
        - target (Character): the target to use the item on
        """
        if isinstance(item, Potion):
            self.restore_health(item.health)
            self.inventory.remove_item(item)
            print(f"You used {item.name} and restored {item.health} health.")

        elif isinstance(item, Scroll):
            self.inventory.remove_item(item)
            target.health -= item.damage
            print(
                f"You used {item.name} and dealt {item.damage} damage to {target.name}.")
        elif isinstance(item, Gem):
            self.inventory.remove_item(item)
            self.stats.strength += item.buff
            print(f"You used {item.name} and gained {item.buff} strength.")

        else:
            print(f"{self.name} can't use {item.name}!")

    def use_ability(self, ability_name):
        """
        Uses the given ability.

        Args:
        - ability_name (str): the name of the ability to use
        """
        if ability_name in self.abilities:
            a = self.abilities[ability_name]
            print(f"{self.name} tries to use {a.name} but it doesn't work.")
        else:
            print(f"{self.name} doesn't know how to use {ability_name}.")

    def update_abilities(self):
        """
        Updates the character's abilities.
        """
        pass

    def level_up(self):
        """
        Levels up the character.
        """
        self.level += 1
        self.experience = 0
        self.health += 5
        self.stats.strength += 1
        self.stats.intelligence += 1
        self.stats.dexterity += 1
        self.stats.defense += 1
        self.stats.speed += 1
        self.update_abilities()

        print(f"{self.name} is now level {self.level}!")
        return f"{self.name} is now level {self.level}!"

    def is_dead(self):
        """
        Returns True if the character is dead, False otherwise.
        """
        return self.health <= 0

    def has_item(self, item_name):
        """
        Returns True if the character has the given item, False otherwise.

        Args:
        - item_name (str): the name of the item to check for
        """
        return any(item.name == item_name for item in self.inventory.items)

    def gain_experience(self, amount):
        """
        Adds the given amount of experience to the character.

        Args:
        - amount (int): the amount of experience to add
        """
        self.experience += amount
        if self.experience >= 100:
            self.level_up()
        else:
            print(f"{self.name} gained {amount} experience!")
            return f"{self.name} gained {amount} experience!"

    def rest(self):
        """
        Rests the character and restores 10 health.
        """
        self.restore_health(10)
        return 10

    def display_inventory(self):
        """
        Displays the character's inventory.
        """
        print("Inventory:")
        return "\n".join([item.name for item in self.inventory.items])

    def display_stats(self):
        """
        Displays the character's stats.
        """
        return f"""
    Stats for {self.name}:
--------------------            
Name:           {self.name}
Level:          {self.level}
Health:         {self.health}
Strength:       {self.stats.strength}
Intelligence:   {self.stats.intelligence}
Dexterity:      {self.stats.dexterity}
Defense:        {self.stats.defense}
Speed:          {self.stats.speed}
    
Experience:     {self.experience}
Gold:           {self.gold}

Class:          {self.__class__.__name__}
--------------------
    """

# Ability subclasses


class Ability:
    def __init__(self, name, damage, cost, cooldown=0):
        self.name = name
        self.damage = damage
        self.cost = cost
        self.cooldown = cooldown
        self.is_used = False


class Stats:
    def __init__(self, strength, intelligence, dexterity, defense, speed):
        self.strength = strength
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.defense = defense
        self.speed = speed


# Character subclasses
class Warrior(Character):
    def __init__(self, name, health, mana):
        super().__init__(name, health, mana)
        self.update_abilities()

    def use_ability(self, ability, target):
        if ability in self.abilities:
            a = self.abilities[ability]
            print(f"{self.name} uses {a.name} and deals {a.damage} damage!")
            target.health -= a.damage
            self.mana -= a.cost
            self.ability_cooldowns[ability] = a.cooldown
            a.is_used = True

        else:
            super().use_ability(ability)

    def update_abilities(self):
        if self.level >= 1:
            self.abilities["Kick"] = Ability(
                "Kick", damage=15, cost=5, cooldown=5)
        if self.level >= 3:
            self.abilities["Charge"] = Ability("Charge", 20, 10)
        if self.level >= 5:
            self.abilities["Slam"] = Ability("Slam", 35, 15)
        if self.level >= 7:
            self.abilities["Execute"] = Ability("Execute", 50, 20)
        if self.level >= 9:
            self.abilities["Whirlwind"] = Ability("Whirlwind", 25, 25)
        if self.level >= 10:
            self.abilities["Rampage"] = Ability("Rampage", 60, 30)


class Mage(Character):
    def __init__(self, name, health, mana):
        super().__init__(name, health, mana)
        self.update_abilities()

    def use_ability(self, ability):
        if ability in self.abilities:
            a = self.abilities[ability]
            print(f"{self.name} uses {a.name} and deals {a.damage} damage!")
        else:
            super().use_ability(ability)

    def update_abilities(self):
        if self.level >= 1:
            self.abilities["Fireball"] = Ability("Fireball", 5, 5, 2)
        if self.level >= 3:
            self.abilities["Frostbolt"] = Ability("Frostbolt", 10, 10)
        if self.level >= 5:
            self.abilities["Arcane Blast"] = Ability("Arcane Blast", 15, 15)
        if self.level >= 7:
            self.abilities["Pyroblast"] = Ability("Pyroblast", 20, 20)
        if self.level >= 9:
            self.abilities["Blizzard"] = Ability("Blizzard", 25, 25)
        if self.level >= 10:
            self.abilities["Arcane Explosion"] = Ability(
                "Arcane Explosion", 30, 30)


class Hunter(Character):
    def __init__(self, name, health, mana):
        super().__init__(name, health, mana)
        self.update_abilities()

    def use_ability(self, ability):
        if ability in self.abilities:
            a = self.abilities[ability]

            print(f"{self.name} uses {a.name} and deals {a.damage} damage!")
        else:
            super().use_ability(ability)

    def update_abilities(self):
        if self.level >= 1:
            self.abilities["Shoot"] = Ability("Shoot", 5, 5, 2)
        if self.level >= 3:
            self.abilities["Aimed Shot"] = Ability("Aimed Shot", 10, 10)
        if self.level >= 5:
            self.abilities["Steady Shot"] = Ability("Steady Shot", 15, 15)
        if self.level >= 7:
            self.abilities["Multi-Shot"] = Ability("Multi-Shot", 20, 20)
        if self.level >= 9:
            self.abilities["Kill Shot"] = Ability("Kill Shot", 25, 25)
        if self.level >= 10:
            self.abilities["Explosive Shot"] = Ability(
                "Explosive Shot", 30, 30)


# Enemy subclasses
class Enemy(Character):
    def __init__(self, name, health, mana, description, level=1, gold=20, experience_reward=10):
        # You can set default values for strength, intelligence, etc., here if you want them to be different than the Character defaults
        super().__init__(name, health, mana, level, gold)
        self.stats.strength = 5
        self.stats.intelligence = 5
        self.stats.dexterity = 5
        self.stats.defense = 5
        self.stats.speed = 5
        self.experience_reward = experience_reward
        self.description = description
        self.equipped_items = {'weapon': None, 'armor': None}


class NPC(Character):
    def __init__(self, name, health, mana, description, dialogue):
        super().__init__(name, health, mana)
        self.description = description
        self.dialogue = dialogue


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        else:
            return False

    def remove_item(self, item):
        if item not in self.items:
            return False
        self.items.remove(item)
        return True

    def display_inventory(self):
        print("Inventory:")
        return "\n".join([item.name for item in self.items])


# Item classes
class Item:
    def __init__(self, name, cost, description=None, is_usable=False):
        self.name = name
        self.cost = cost
        self.description = description
        self.is_usable = is_usable

    def __str__(self):
        return f"{self.name} (Cost: {self.cost})"

    def __repr__(self):
        return f"{self.name} (Cost: {self.cost})"


class Weapon(Item):
    def __init__(self, name, cost, damage, description=None):
        super().__init__(name, cost, description, is_usable=False)
        self.damage = damage


class Armor(Item):
    def __init__(self, name, cost, defense, description=None):
        super().__init__(name, cost, description, is_usable=False)
        self.defense = defense


class Potion(Item):
    def __init__(self, name, cost, effect, description=None):
        super().__init__(name, cost, description, is_usable=True)
        self.health = effect


class Scroll(Item):
    def __init__(self, name, cost, effect, description=None):
        super().__init__(name, cost, description, is_usable=True)
        self.damage = effect


class Gem(Item):
    def __init__(self, name, cost, effect, description=None):
        super().__init__(name, cost, description, is_usable=True)
        self.buff = effect


class QuestItem(Item):
    def __init__(self, name, description):
        super().__init__(name, 0)
        self.description = description
