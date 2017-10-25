from classes.game import Person, bcolours
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")


# Create Some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


# Instantiate People
player_magic = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "qty": 15}, {"item": hipotion, "qty": 5},
                {"item": superpotion, "qty": 5}, {"item": elixer, "qty": 5},
                {"item": hielixer, "qty": 2}, {"item": grenade, "qty": 5}]
player1 = Person("Valos:", 3260, 132, 300, 34, player_magic, player_items)
player2 = Person("Nick :", 4160, 188, 311, 34, player_magic, player_items)
player3 = Person("Robot:", 3089, 174, 288, 34, player_magic, player_items)

enemy1 = Person("Imp   ",1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus ",18200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp   ",1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolours.FAIL + bcolours.BOLD + "A HORDE OF ENEMIES APPROACH YOU" + bcolours.ENDC)

while running:
    print("===================")
    print("\n\n")
    print(bcolours.BOLD + "NAME:                 HP                                      MP" + bcolours.ENDC)
    for player in players:
        player.get_stats()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.gen_dmg()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_dmg(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ","") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(bcolours.BOLD + bcolours.OKGREEN +enemies[enemy].name.replace(" ","") + " has been defeated!" + bcolours.ENDC)
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.gen_dmg()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolours.FAIL + "\n Not Enough MP\n" + bcolours.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolours.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg) + "HP." + bcolours.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                print(bcolours.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to", enemies[enemy].name.replace(" ","") + bcolours.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolours.BOLD + bcolours.OKGREEN + enemies[enemy].name.replace(" ","") + " has been defeated!" + bcolours.ENDC)
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["qty"] == 0:
                print(bcolours.FAIL + "\n" + "None Left..." + bcolours.ENDC)
                continue
            player.items[item_choice]["qty"] -= 1


            if item.type == "potion":
                player.heal(item.prop)
                print(bcolours.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolours.ENDC)

            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                        print(bcolours.OKGREEN + "\n" + item.name + " fully restores HP/ MP" + bcolours.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolours.OKGREEN + "\n" + item.name + " fully restores HP/ MP" + bcolours.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_dmg(item.prop)
                print(bcolours.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to", enemies[enemy].name.replace(" ","") + bcolours.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolours.BOLD + bcolours.OKGREEN + enemies[enemy].name.replace(" ","") + " has been defeated!" + bcolours.ENDC)
                    del enemies[enemy]

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Player won
    if defeated_enemies == 2:
        print(bcolours.OKGREEN + "You defeated the enemies!" + bcolours.ENDC)
        running = False

    # Check if Enemy won
    elif defeated_players == 2:
        print(bcolours.FAIL + "The enemies have defeated you!" + bcolours.ENDC)
        running = False

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0,2)
        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0,3)
            enemy_dmg = enemy.gen_dmg()
            players[target].take_dmg(enemy_dmg)
            print(bcolours.FAIL + enemy.name.replace(" ", "") + " attacks " +
                  players[target].name.replace(" ", "") + " for", str(enemy_dmg) + bcolours.ENDC)
        elif enemy_choice == 1:
            # Chose magic
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            print(bcolours.FAIL + enemy.name.replace(" ", "") + " chose", spell.name, "for",
                  magic_dmg, "damage" + bcolours.ENDC)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolours.FAIL + "\n" + spell.name + " heals", enemy.name + "for",
                      str(magic_dmg) + "HP." + bcolours.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, len(players))
                players[target].take_dmg(magic_dmg)
                print(bcolours.FAIL + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals",
                      str(magic_dmg), "points of damage to", players[target].name.replace(" ","") + bcolours.ENDC)

                if players[target].get_hp() == 0:
                    print(bcolours.BOLD + bcolours.FAIL + players[target].name.replace(" ","") + " has been defeated!" + bcolours.ENDC)
                    del players[target]
