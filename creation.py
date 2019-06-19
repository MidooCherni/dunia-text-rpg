print("Importing creation module...")
import world
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def create_character(pc):
    cls()
    pc.name = input("What is your name? \n\n")
    cls()
    print("First of all, you will choose a Race.\nThis will define your allegiance and your starting zone, along with some bonuses.\n")
    print("\n   The Draconic Legion:")
    print("tynnin - The Dragon Empire")
    print("dwarf - Iklisztefon, the Hollow Mountain")
    print("ogre - Redrock, the Pit of Flame")
    print("kam'kalei - The Tree of Life")
    print("\n   The Divine Pact:")
    print("human - The Crusader Kingdom of Hylonia")
    print("shan'kalei - Goldstar, the Sun's Abode")
#    print("skyborn - Au, The Golden Citadel")
#    print("centaur - Nomads of the Wastelands")
#    print("\n   The Underworld:")
#    print("khanfus - The Temple-City of Khanfusaj")
#    print("undead - The Dreaded Underworld")
#    print("demon - The All-Consuming Void")
#    print("\n   Other:")
#    print("mer'kalei - The City Beneath The Waves")
#    print("minotaur - Reavers of the Wastelands")
#    print("halfling - Unawood, the Free Ones")
#    print("nymir - Sajrokka, Heart of the Jungle")
#    print("girdani - The Monkey Isles")
    chosen_race = ""
    playable_races = ["tynnin", "dragon", "reptilian", "ogre", "dwarf", "human", "sun elf", "moon elf", "sea elf", "halfling", "shan'kalei", "shankalei", "kam'kalei",
                      "kamkalei", "markalei", "mer'kalei", "skyborn", "angel", "khanfus", "centaur", "minotaur", "undead", "skeleton", "zombie", "demon"]
    while chosen_race not in playable_races:
        chosen_race = input("\n>")
        chosen_race = chosen_race.lower()
        if chosen_race == "tynnin" or chosen_race == "dragon" or chosen_race == "reptilian":
            pc.race = "Dragon"
            cls()
            print("You have chosen the TYNNIN.\nFearsome and wrathful warriors of the Dragon Empire,"
                  "they obey the Dragon God with fanatical devotion and live every moment with dedication to spread the reach of their empire further.\n"
                  "Boost to Attack value.\nImmune to Burn and Poison.\nCan regenerate health slowly.")
            allowed_strength_classes = ["knight", "barbarian", "shaman", "ranger"]
            allowed_intellect_classes = ["priest", "wizard", "necromancer", "shaman"]
            allowed_agility_classes = ["ranger", "monk", "assassin"]
            pc.atk += 10
            pc.status.append("regeneration")
            pc.location = world.draenin
        elif chosen_race == "human":
            pc.race = "Human"
            cls()
            print("You have chosen the HUMAN.\nZealous warriors of light, on a dedicated crusade to rid the world of the chaotic Dragons and the vile Undead. "
                  "Slight boosts to every stat.\nMay use any weapon or armor regardless of class restrictions.")
            allowed_strength_classes = ["knight", "paladin", "barbarian", "ranger"]
            allowed_intellect_classes = ["priest", "wizard"]
            allowed_agility_classes = ["ranger", "monk", "assassin", "bard"]
            pc.location = world.hylonian_kingdom
        elif chosen_race == "dwarf":
            pc.race = "Dwarf"
            cls()
            print("You have chosen the DWARF.\nStout and kind-hearted creatures born of stone, they live in cave complexes and hollow mountains and are particularly "
                  "fond of metallurgy.\nBoost to Stamina.\nMay cleanse out all negative status effects with their stone form.")
            allowed_strength_classes = ["knight", "barbarian", "shaman", "ranger"]
            allowed_intellect_classes = ["priest", "wizard", "shaman",]
            allowed_agility_classes = ["ranger", "monk", "assassin", "bard"]
            pc.sta += 50
            pc.hp += 50
            pc.spells.append(world.DCleanse)
            pc.location = world.iklistzefon
        elif chosen_race == "ogre":
            pc.race = "Ogre"
            cls()
            print("You have chosen the OGRE.\nDeeply misunderstood creatures, ridiculed for their somewhat low intellect. They are rotund and blissfully jovial, and bear "
                  "undying loyalty to those who care for them.\nLarge boost to stamina. Unlocks the power of spite at higher levels.")
            allowed_strength_classes = ["knight", "barbarian", "shaman", "ranger"]
            allowed_intellect_classes = ["shaman"]
            allowed_agility_classes = ["ranger"]
            pc.sta += 100
            pc.hp += 100
            pc.location = world.redrock
        elif chosen_race == "sun elf" or chosen_race == "shankalei" or chosen_race == "sham'kalei":
            pc.race = "Sun Elf"
            cls()
            print("You have chosen the SUN ELF.\nMystical, svelt beings obsessed with the magical nature of life, they live in their mage city of Goldstar, built upon "
                  "the drifting isles off the northern coast of Karra.\nBoost to Wisdom.\nMay life tap for mana.")
            allowed_strength_classes = ["knight", "paladin", "ranger"]
            allowed_intellect_classes = ["priest", "wizard", "necromancer",]
            allowed_agility_classes = ["ranger", "monk", "assassin", "bard"]
            pc.spells.append(world.SelfRacial)
            pc.wis += 50
            pc.mana += 50
            pc.location = world.goldstar
        elif chosen_race == "moon elf" or chosen_race == "kam'kalei" or chosen_race == "kamkalei":
            pc.race = "Moon Elf"
            cls()
            print("You have chosen the MOON ELF.\nMystical beings of mesmerizing beauty that rarely interact with other cultures, they live to protect and nourish "
                  "the tree of life, and to pursue the arts of druidic magic.\nAlways attack first.\nAttempts to escape any non-boss fight will always succeed.")
            allowed_strength_classes = ["knight", "ranger"]
            allowed_intellect_classes = ["priest", "druid"]
            allowed_agility_classes = ["ranger", "monk", "assassin", "bard", "druid"]
            pc.speed = 3
            pc.location = world.the_blackwood
        elif chosen_race == "halfling":
            pc.race = "Halfling"
            cls()
            print("You have chosen the HALFLING.\nShort creatures with large, hairy feet who are void of facial hair, they share the Dwarves' fondness of life and sense "
                  "and are in tune with nature out of friendship with the Moon Elves.\nMay instinctively camouflage.")
            allowed_strength_classes = ["knight", "shaman", "ranger"]
            allowed_intellect_classes = ["priest", "shaman", "druid"]
            allowed_agility_classes = ["ranger", "monk", "assassin", "bard", "druid"]
            pc.spells.append(world.Stealth)
        elif chosen_race == "mer'kalei" or chosen_race == "merkalei" or chosen_race == "sea elf":
            pc.race = "Mer'kalei"
            cls()
            print("You have chosen the MER'KALEI.\nElves with translucent skin and a feint azure coloration. They live independent of land-dwellers in a city under the sea. "
                  "\nMay shapeshift into their aquatic form.")
            allowed_strength_classes = ["knight", "shaman"]
            allowed_intellect_classes = ["priest", "wizard", "necromancer", "shaman"]
            allowed_agility_classes = ["assassin", "bard"]
            pc.spells.append(world.SirenForm)
        elif chosen_race == "skyborn" or chosen_race == "angel":
            pc.race = "Skyborn"
            cls()
            print("You have chosen the SKYBORN.\nGiants of pure lights, with skin of true gold, dedicated to an endless service to the light and to the eradication of evil. "
                  "\nThe death of their physical form only returns them to Au at the cost of their memory.")
            allowed_strength_classes = ["knight", "paladin"]
            allowed_intellect_classes = ["priest"]
            allowed_agility_classes = ["bard"]
        elif chosen_race == "khanfus":
            pc.race = "Khanfus"
            cls()
            print("You have chosen the KHANFUS.\nSkittering beasts who dwell in the forgotten underground catacombs of southern Karra, dedicating themselves to deep research "
                  "of shadow and death.\nMay burrow and travel underground. Immune to poison.")
            allowed_strength_classes = ["knight", "shaman"]
            allowed_intellect_classes = ["wizard", "necromancer", "shaman"]
            allowed_agility_classes = ["assassin"]
        elif chosen_race == "centaur":
            pc.race = "Centaur"
            cls()
            print("You have chosen the CENTAUR.\nThe native nomadic race of guardians that roam southern Karra, they are incredibly fast, deceptively agile, and in tune "
                  "with the elements.\nMay trample their enemies, and gain bonus Attack value from items.")
            allowed_strength_classes = ["knight", "barbarian", "shaman", "ranger"]
            allowed_intellect_classes = ["shaman"]
            allowed_agility_classes = ["ranger", "bard"]
            pc.spells.append(world.WarriorCharge)
        elif chosen_race == "minotaur":
            pc.race = "Minotaur"
            cls()
            print("You have chosen the MINOTAUR.\nMassive, short-tempered bestial folk of the wastelands, they are burly and fond of weapon-making.\nMay charge at their enemies, "
                  "and gain bonus Stamina value from items.")
            allowed_strength_classes = ["knight", "barbarian", "shaman", "ranger"]
            allowed_intellect_classes = ["shaman"]
            allowed_agility_classes = ["ranger"]
        elif chosen_race == "undead" or chosen_race == "skeleton" or chosen_race == "zombie":
            pc.race = "Undead"
            cls()
            print("You have chosen the UNDEAD.\nRotting carcasses re-infused with memories and consciousness, they hold a deep grudge for life that stems from jealousy.\nMay "
                  "learn spells from any school but Nature, regardless of class.")
            allowed_strength_classes = ["knight"]
            allowed_intellect_classes = ["priest", "wizard", "necromancer"]
            allowed_agility_classes = ["monk", "assassin"]
        elif chosen_race == "demon":
            pc.race = "Demon"
            cls()
            print("You have chosen the DEMON.\nMalicious beasts from the deepest, coldest corners of the universe, they are sent into existence with the sole purpose of \n"
                  "destruction and chaos.\nThe death of their physical form only returns them to the void at the cost of their memory.")
            allowed_strength_classes = ["knight", "barbarian"]
            allowed_intellect_classes = ["priest", "wizard", "necromancer"]
            allowed_agility_classes = ["assassin"]
        else:
            print("Try again.")
    print("\nNow you must choose a Path.\nThis will decide your armor proficiency.")
    print("FIGHTER")
    print("CASTER")
    print("ROGUE")
    chosen_path = ""
    chosen_class = ""
    while chosen_path not in ["fighter", "caster", "rogue"]:
        chosen_path = input("\n>")
        chosen_path = chosen_path.lower()
        if chosen_path == "fighter":
            cls()
            while chosen_class not in allowed_strength_classes:
                print("Choose a class.\nThis will determine your starting abilities.\n")
                if "knight" in allowed_strength_classes:
                    print("The KNIGHT")
                if "paladin" in allowed_strength_classes:
                    print("The PALADIN")
                if "barbarian" in allowed_strength_classes:
                    print("The BARBARIAN")
                if "shaman" in allowed_strength_classes:
                    print("The SHAMAN")
                if "ranger" in allowed_strength_classes:
                    print("The RANGER")
                chosen_class = input("\n>")
                chosen_class = chosen_class.lower()
        elif chosen_path == "caster":
            cls()
            while chosen_class not in allowed_intellect_classes:
                print("Choose a class.\nThis will determine your starting spells.\n")
                if "priest" in allowed_intellect_classes:
                    print("The PRIEST")
                if "wizard" in allowed_intellect_classes:
                    print("The WIZARD")
                if "necromancer" in allowed_intellect_classes:
                    print("The NECROMANCER")
                if "shaman" in allowed_intellect_classes:
                    print("The SHAMAN")
                if "druid" in allowed_intellect_classes:
                    print("The DRUID")
                chosen_class = input("\n>")
                chosen_class = chosen_class.lower()
        elif chosen_path == "rogue":
            cls()
            while chosen_class not in allowed_agility_classes:
                print("Choose a class.\nThis will determine your starting moves.\n")
                if "bard" in allowed_agility_classes:
                    print("The BARD")
                if "monk" in allowed_agility_classes:
                    print("The MONK")
                if "assassin" in allowed_agility_classes:
                    print("The ASSASSIN")
                if "ranger" in allowed_agility_classes:
                    print("The RANGER")
                if "druid" in allowed_agility_classes:
                    print("The DRUID")
                chosen_class = input("\n>")
                chosen_class = chosen_class.lower()
        else:
            print("Try again.")
    if chosen_class == "knight":
        cls()
        pc.job = "Knight"
        pc.spells = world.starterKnight
        print("You have chosen the Knight.\n"
              "The knight is a burly, plate-wearing champion of a certain nation who uses their stamina and defensive power to protect his party. ")
    elif chosen_class == "paladin":
        cls()
        pc.job = "Paladin"
        pc.spells = world.starterPaladin
        print("You have chosen the Paladin.\n"
              "The paladin is a devout disciple of Light who sacrifices their life to cleanse all evil and chaos in the world.")
    elif chosen_class == "barbarian":
        cls()
        pc.job = "Barbarian"
        print("You have chosen the Barbarian.\n"
              "The barbarian is a master of savage combat, channeling their inner beast for a frenzied playstyle of darting from enemy to enemy.")
    elif chosen_class == "wizard":
        cls()
        pc.job = "Wizard"
        pc.spells = world.starterWizard
        print("You have chosen the Wizard.\n"
              "The wizard is an obsessive student of the primary forces that bind the world of Dunia together, harnessing it primarily harm or conjure.")
    elif chosen_class == "priest":
        cls()
        pc.job = "Priest"
        pc.spells = world.starterPriest
        print("You have chosen the Priest.\n"
              "The priest dedicates their life to a certain deity of the world of Dunia, gaining magical powers in exchange for their faith and service.")
    elif chosen_class == "necromancer":
        cls()
        pc.job = "Necromancer"
        pc.spells = world.starterNecro
        print("You have chosen the Necromancer.\n"
              "The necromancer is a servant of the evil Black Titan, studying dark arts and mysterious tomes to gain control over the world of the undead.")
    elif chosen_class == "bard":
        cls()
        pc.job = "Bard"
        print("You have chosen the Bard.\n"
              "Bards use their custom-made instruments to weave different spell effects into songs that can do everything from buffing to debuffing.")
    elif chosen_class == "assassin":
        cls()
        pc.job = "Assassin"
        pc.spells = world.starterAssassin
        print("You have chosen the Assassin.\n"
              "The assassin is a fearsome yet subtle fighter who can reach crazy amounts of damage, while sacrificing other things like defenses or mobility")
    elif chosen_class == "monk":
        cls()
        pc.job = "Monk"
        print("You have chosen the Monk.\n"
              "The monk is a master of coordination and balance, using their body as a living weapon to execute complex techniques and defeat fearsome foes.")
    elif chosen_class == "ranger":
        cls()
        pc.job = "Ranger"
        pc.spells = world.starterRanger
        print("You have chosen the Ranger.\n"
              "In tune with natural life and all ways of the wild, rangers dedicate their lives to understanding as much of nature as a mortal is allowed to.")
    elif chosen_class == "druid":
        cls()
        pc.job = "Druid"
        pc.spells = world.starterDruid
        print("You have chosen the Druid.\n"
              "Druids harness their understanding of nature to control the forces of weather, fauna, and the forms of its living beings.")
    elif chosen_class == "shaman":
        cls()
        pc.job = "Shaman"
        pc.spells = world.starterShaman
        cls()
        print("You have chosen the Shaman.\n"
              "Shamanism is the essential magic through which the tribal priests of the primitive races of Dunia control the elements and spirits.")
    print("Your character has been forged. The wheel of fate is turning...\n")
    print(pc.name + " the " + pc.race + " " + pc.job + ", welcome to the World of Dunia.")