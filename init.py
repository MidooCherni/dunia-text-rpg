# TO-DO:
#   X   Health bars and refreshing screen
#   X   Shorthand symbols for commands
#   X   Special keyword based dialogue
#   X   Weapon types in attacks
#   X   Rarity colors (white > green > blue > purple)
#   X   Teleport NPCs between the contents
#   X   Add some new races
#   X   Some classes are race specific
#   X   Talent point system
#   X   Priests can full heal you in every major city
#   X   Time system with day and night cycle
#   X       Every turn is 5 minutes
#   X       Traveling from zone to zone is 1 hour
#   X       Using flight takes 1 day
#   X       Sleeping takes 8 hours
#   X   Pressing UP repeats the last commmand
#   X   Talents actually functional
#       Many more quests
#       More companions
#       Faction dislikes (Dragons attack Humans, etc.)
#       Add the commented out races
#       Add some new cities
#       Ranged attacks
#       Bard songs and talents + unfinished talents


print("Loading...\n")
import random
import creation
import world
import pickle
import os


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


class Player:
    def __init__(self, name, race, job, sta, hp, atk, wis, mana, speed, xp, xpmax, level, talents,
                 spells, status, inventory, set, in_combat, location, questlog, companion):
        self.name = name
        self.race = race
        self.job = job
        self.sta = sta
        self.hp = hp
        self.atk = atk
        self.wis = wis
        self.mana = mana
        self.speed = speed
        self.xp = xp
        self.xpmax = xpmax
        self.level = level
        self.talents = talents
        self.spells = spells
        self.status = status
        self.inventory = inventory
        self.set = set
        self.in_combat = in_combat
        self.location = location
        self.questlog = questlog
        self.companion = companion


def genTip():
    l = random.randint(0, 15)
    if l == 0: print("\nPROTIP: Talents aren't functional yet.")
    elif l == 1: print("\nPROTIP: The Dragon Empire and Redrock are linked by a flight route.\nFind the elder in either cities.")
    elif l == 2: print("\nPROTIP: This game isn't a finished product yet.\nQuest, kill, buy and sell, say hi to people you meet..")
    elif l == 3: print("\nPLANNED IN THE FUTURE: Crafting professions.")
    elif l == 4: print("\nPLANNED IN THE FUTURE: Ship route. Northern continent.")
    elif l == 5: print("\nPROTIP: An enchanter in the great college in Hylonia\noffers a task for the worthy.")
    elif l == 6: print("\nPROTIP: This game was mostly influenced by World of Warcraft, \nEverquest Classic, and past-century MUDs.")
    elif l == 7: print("\nPLANNED IN THE FUTURE: If you enter a Human city as a Dragon,\nprepare for a challenge.")
    elif l == 8: print("\nPLANNED IN THE FUTURE: Fishing. Hunting. Herbalism. Mining.\nI don't know, something relaxing. Maybe tea brewing or cooking.")
    elif l == 9: print("\nPROTIP: There's a total of ten of these. Keep track of them.\nA round also passes per command, so use it to pass time while grinding.")
    elif l == 10: print("\nPROTIP: Special thanks to my programming classes for being so \nboring that I'd rather do this in secret than actual school work.")
    elif l == 11: print("\nPROTIP: I have a cat named coochie.")
    elif l == 12: print("\nPROTIP: You're hot then you're cold, you're yes then you're no.")
    elif l == 13: print("\nI KISSED A GIRL: And I liked it.")
    elif l == 14: print("\nHungUp On Thread 4\nRCP is HUNG UP!!\nOh, MY GOD!!")
    elif l == 15: print("\nPROTIP: Avoid crying or pissing your pants. Don't shit or cum, either.")
    else: print("\nCouldn't load tips for some reason.")


def save(char):
    try:
        with open(char.name + '.sav', 'wb') as save_file:
            pickle.dump(char, save_file)
        print("File saved as " + char.name + ".sav")
    except:
        print("Couldn't save.")
        return


def load(char):
    try:
        with open(char + '.sav', 'rb') as save_file:
            return pickle.load(save_file)
    except FileNotFoundError:
        print("Couldn't find a save file with that name.")
        return


pc = Player("debug", "Human", "Shaman", 100, 100, 10, 100, 100, 1, 0, 1000, 1, [], [], [], world.inventory, world.set, 0, world.hylonian_outskirts, [], None)


# Main Code
print('Welcome to the "World of DUNIA", coded, designed and written by Midoo.')
print("This world is one full of strife and epic combat.\n")
genTip()
print('Type "tips" in-game for more.')
print('\nMOTD:')
print('\nPlaceholder for 0.4: Talk about talents..\n')
game_ongoing = 0


# New Game or Load Save
while game_ongoing == 0:
    choice = input("Create or continue? ")
    if choice.lower() in ["yes", "y", "create", "new"]:
        creation.create_character(pc)
        game_ongoing = 1
    elif choice.lower() in ["no", "n", "load", "continue"]:
        pc = load(input("Name of the character to load: "))
        if pc.name != "debug":
            print("Welcome back, " + pc.name + " the " + pc.race + " " + pc.job + ".")
            game_ongoing = 1
    elif choice == "88224646ab":
        game_ongoing = 1
    else:
        print("Please make a choice.")


pc.in_combat = 0


# Tick starts here
while game_ongoing == 1:
    world.check_starting_statuses(pc)
    if pc.companion != None:
        world.check_starting_statuses(pc.companion)
    print("\nYou are in " + pc.location.name + ".")
    if pc.companion != None:
        fr = random.randint(0, 3)
        if fr == 0:
            print(pc.companion.name + pc.companion.afkquotes)
    decision = input("\n>")
    decision = decision.lower()
    cls()
    world.show_gui(pc)
    print("(s)tatus    (b)ackpack    s(p)ellbook    (c)ast    (l)og    w(h)o")
    print("(eat)    (wear)    (remove)    (g)o    (t)alk    tale(n)ts    (z)zz")
    print("")
    if "spellbook" in decision or "spells" in decision or decision == "p":
        world.spellbook(pc.spells)
    elif decision == "debug level up":
        world.LevelUp(pc)
    elif "dance" in decision or "boogie" in decision:
        if random.randint(0,1) == 1:
            print("You boogie your fucking soul out.")
        else:
            print("You dance very aggressively.")
    elif "wander" in decision:
        print("You wander around aimlessly.")
    elif "drink" in decision or "eat" in decision or "consume" in decision or "quaff" in decision:
        world.check_food(decision, pc.inventory, pc)
    elif "inventory" in decision or "bag" in decision or decision == "b":
        world.list_inventory(pc.inventory)
    elif "read" in decision:
        world.check_item(decision, pc.inventory, pc, pc)
    elif "wear" in decision or "equip " in decision or "wield" in decision:
        world.check_weapon(decision, pc.inventory, pc)
    elif "inspect" in decision or "equipment" in decision or "set" in decision or "status" in decision or decision == "s":
        world.inspect_equipment(pc)
    elif "remove" in decision or "clear" in decision or "unequip" in decision:
        world.remove(pc, decision)
    elif "save" in decision:
        save(pc)
    elif "cast" in decision or (len(decision)>1 and decision[0]=="c" and decision[1]==" "):
        world.check_spellOUT(decision, pc.spells, pc)
    elif decision in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        world.cast_hotkeyOUT(decision, pc)
    elif "load" in decision:
        assurance = input("Do you really want to abandon this character? Y/N " )
        if assurance in ["yes", "y"]:
            pc = load(input("Name of the character to load: "))
    elif "talk" in decision or "speak" in decision or (len(decision)>1 and decision[0]=="t" and decision[1]==" "):
        world.check_npcs(decision, pc)
    elif "go" in decision or "travel" in decision or "where" in decision or decision == "g" or (len(decision)>1 and decision[0]=="g" and decision[1]==" "):
        world.check_zones(decision, pc)
    elif "who" in decision:
        world.who(pc.location)
        if pc.companion != None:
            print(pc.companion.name + " is following you.")
    elif "aabb123123z" in decision:
        world.LevelUp(pc)
    elif "bbaa321321y" in decision:
        pc.inventory[0].quantity += 10000
    elif "pet" in decision or "companion" in decision or "follower" in decision:
        if pc.companion == None:
            print("You have no companions.")
        else:
            if pc.companion.name != pc.companion.species:
                print(pc.companion.name + ", " + pc.companion.species + ", " + pc.name + "'s companion.")
            else:
                print(pc.companion.name + ", " + pc.name + "'s companion.")
            print(str(pc.companion.hp) + "/" + str(pc.companion.sta) + " HP _ " + str(pc.companion.mana) + "/" + str(pc.companion.wis) + " Mana")
    elif "rest" in decision or "sleep" in decision or "lay down" in decision or decision == "z":
        if (world.date[1] < 7 or world.date[1] > 19):
            pc.hp = pc.sta
            pc.mana = pc.wis
            world.date[1] += 8
            if (world.date[1] >= 24):
                world.date[0] += 1
                world.date[1] -= 24
            print("\nYou wake up feeling well rested.")
        else:
            print("\nYou can't sleep in broad daylight!")
    elif decision in ["tip", "tips", "protip", "protips"]:
        genTip()
    elif "quest" in decision or decision == "l":
        world.list_quests(pc)
    elif "find" in decision or "fight" in decision or "search" in decision or decision == "f":
        world.find_enemy(pc, pc.location)
    elif decision in ["talent", "perk", "build", "n"]:
        world.ListTalents(pc)
    else:
        print("What?")
    # Combat Loop
    world.date[2] += 10
    if (world.date[2] >= 60):
        world.date[1] += 1
        world.date[2] -= 60
    if (world.date[1] >= 24):
        world.date[0] += 1
        world.date[1] -= 24
    combatant = world.check_encounter(pc, pc.location)
    while pc.in_combat == 1:
        world.start(pc, combatant)
    world.check_ending_statuses(pc)
    if pc.companion != None:
        world.check_ending_statuses(pc.companion)
        if pc.companion.hp <= 0:
            if "redeemed" in pc.companion.status:
                print("Your companion is spared from death... They are brought back to life.")
                pc.companion.hp = pc.companion.sta
                pc.companion.status.remove("redeemed")
            print(pc.companion.name + " has died...")
            pc.companion = None
    if pc.hp <= 0:
        if world.Rebirth in pc.talents:
            print("The souls of your ancestors gather their strength to return you to the mortal realm...")
            pc.location = world.creek_of_life
            print("You are brought back to life.")
            pc.hp = 1
            pc.mana = 1
        elif "redeemed" in pc.talents:
            print("The ultimate blessing comes to action... You glow with holy light...")
            pc.location = world.creek_of_life
            print("You are brought back to life.")
            pc.hp = 1
            pc.mana = 1
            pc.status.remove("redeemed")
        else:
            game_ongoing = 0


print("Game over. Press any key to exit.")
input()