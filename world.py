import random
print("Importing world module...")
from colorama import init
init()
import os


date = [0, 10, 0]


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def show_combat_gui(pc, e_or_hp, e_curr_hp):
    segments = ""
    how_many_bars = (pc.hp*10)/pc.sta
    continuation = 10 - how_many_bars
    for i in range(1, int(how_many_bars)):
        segments += "\033[1;32;40m==\033[0m"
    for i in range(1, int(continuation)):
        segments += "__"
    e_segments = ""
    how_many_enemy_bars = (e_curr_hp*10)/e_or_hp
    e_continuation = 10 - how_many_enemy_bars
    for i in range(1, int(how_many_enemy_bars)):
        e_segments += "\033[1;31;40m==\033[0m"
    for i in range(1, int(e_continuation)):
        e_segments += "__"
    if (date[1] > 5 and date[1] < 19):
        dn = "Day"
    else:
        dn = "Night"
    dispHR = str(date[1])
    if date[1] < 10:
        dispHR = "0" + str(date[1])
    dispMN = str(date[2])
    if date[2] < 10:
        dispMN = "0" + str(date[2])
    print(dn + " " + str(date[0]) + ", " + dispHR + ":" + dispMN)
    print("[" + segments + "] " + str(pc.hp) + "/" + str(pc.sta) + " HP             "
          "[" + e_segments + "] " + str(e_curr_hp) + "/" + str(e_or_hp) + " HP")
    segments = ""
    how_many_bars = (pc.mana * 10) / pc.wis
    continuation = 10 - how_many_bars
    for i in range(1, int(how_many_bars)):
        segments += "\033[1;36;40m==\033[0m"
    for i in range(1, int(continuation)):
        segments += "__"
    print("[" + segments + "] " + str(pc.mana) + "/" + str(pc.wis) + " MP")
    print("")


def show_gui(pc):
    segments = ""
    how_many_bars = (pc.hp*10)/pc.sta
    continuation = 10 - how_many_bars
    for i in range(1, int(how_many_bars)):
        segments += "=="
    for i in range(1, int(continuation)):
        segments += "  "
    if (date[1] > 5 and date[1] < 19):
        dn = "Day"
    else:
        dn = "Night"
    dispHR = str(date[1])
    if date[1] < 10:
        dispHR = "0" + str(date[1])
    dispMN = str(date[2])
    if date[2] < 10:
        dispMN = "0" + str(date[2])
    print(pc.name + " - Level " + str(pc.level) + " " + pc.race + " " + pc.job + "      " + str(pc.xp) + "/" + str(pc.xpmax) + "      "
          + dn + " " + str(date[0]) + ", " + dispHR + ":" + dispMN)
    print("[\033[1;32;40m" + segments + "\033[0m] " + str(pc.hp) + "/" + str(pc.sta) + " HP")
    segments = ""
    how_many_bars = (pc.mana * 10) / pc.wis
    continuation = 10 - how_many_bars
    for i in range(1, int(how_many_bars)):
        segments += "=="
    for i in range(1, int(continuation)):
        segments += "  "
    print("[\033[1;36;40m" + segments + "\033[0m] " + str(pc.mana) + "/" + str(pc.wis) + " MP")
    print("")


def LevelUp(whom):
    whom.xp = 0
    whom.xpmax += 1000
    whom.sta += 100
    whom.hp += 100
    whom.wis += 100
    whom.mana += 100
    whom.atk += 10
    whom.level += 1
    print("Congratulations! Welcome to level " + str(whom.level) + ".")
    if whom.level in [2, 4, 6]:
        LearnTalent(whom)


class Spell:
    def __init__(self, name, flavor, damage, effect, cost, announcement, description):
        self.name = name
        self.flavor = flavor
        self.damage = damage
        self.effect = effect
        self.cost = cost
        self.announcement = announcement
        self.description = description


def check_if_castable(spell, caster, victim, wording):
    if "freespell" in caster.status:
        caster.status.remove("freespell")
        print("\033[1;43;40mIt cost no mana.\033[0m")
        cast(spell, caster, victim, wording)
    else:
        if caster.mana >= spell.cost:
            cast(spell, caster, victim, wording)
            caster.mana -= spell.cost
        else:
            print("\033[1;31;40mYou don't have enough mana to cast that spell.\033[0m")


def cast_hotkeyOUT(number, caster):
    if number == "0":
        print("Not in combat.")
    elif len(caster.spells) == int(number):
        if caster.spells[int(number)-1].effect in ["reflect", "tp", "immunity", "item", "freespell", "manabuff", "healthbuff", "atkbuff", "heal"]:
            check_if_castable(caster.spells[int(number)-1], caster, caster, number)
            return
        else:
            print("Invalid target.")


def cast_hotkey(number, target, caster):
    if number == "0":
        combat_loop(caster, target)
        if caster.companion != None:
            Eattack(caster.companion, target)
    elif len(caster.spells) == int(number):
        if "stunned" not in caster.status and "badly stunned" not in caster.status and "mesmerized" not in caster.status:
            check_if_castable(caster.spells[int(number)-1], caster, target, number)
            if caster.in_combat == 1:
                Eattack(target, caster)
                if caster.companion != None:
                    Eattack(caster.companion, target)
        else:
            print("You're incapcaitated!")
            Eattack(target, caster)
            if caster.companion != None:
                Eattack(caster.companion, target)


def cast(spell, caster, victim, wording):
    spelldamage = spell.damage
    if hasattr(caster, 'talents'):
        if RealityUnwoven in caster.talents:
            spelldamage += spelldamage/3
        if spell.flavor == "Frost":
            if IceFloes in caster.talents:
                spelldamage += spelldamage / 2
            if FireFrost in caster.talents:
                caster.status.append("Steam Explosion")
            if WeatherMastery in caster.talents:
                spelldamage += spelldamage / 5
        if spell.flavor == "Fire":
            if WeatherMastery in caster.talents:
                spelldamage += spelldamage / 2
            if "Steam Explosion" in caster.status:
                print("\033[1;31;40mFire magic reacted violently to ice, thawing it with a blast!\033[0m")
                caster.status.remove("Steam Explosion")
                spelldamage *= 2
    if spell.effect not in ["minion", "item", "tp"] and type(caster).__name__ == "Player":
        spelldamage = spell.damage*caster.level
    if spell.effect == "heal":
        if hasattr(caster, 'talents'):
            if Holiness in caster.talents or LifeSpring in caster.talents or Mercy in caster.talents:
                spelldamage += spelldamage/5
        if caster.companion != None and caster.companion.name in wording:
            caster.companion.hp -= spelldamage
            print(caster.name + spell.announcement + caster.companion.name + " for \033[1;31;40m" + str(-spelldamage) + " \033[0mHealth Points.")
            if caster.companion.hp > caster.companion.sta:
                caster.companion.hp = caster.companion.sta
            if hasattr(caster, 'talents'):
                if AncestralHealing in caster.talents:
                    caster.companion.status.append("afterheal")
        else:
            caster.hp -= spelldamage
            print(caster.name + spell.announcement + caster.name + " for \033[1;31;40m" + str(-spelldamage) + " \033[0mHealth Points.")
            if caster.hp > caster.sta:
                caster.hp = caster.sta
            if hasattr(caster, 'talents'):
                if Renewal in caster.talents:
                    caster.status.append("afterheal")
    elif spell.effect == "resurrect":
        if caster.companion != None and caster.companion.name in wording:
            caster.companion.status.append("redeemed")
            print(caster.name + spell.announcement + caster.companion.name + " for \033[1;31;40m" + str(-spelldamage) + " \033[0mHealth Points.")
        else:
            caster.status.append("redeemed")
            print(caster.name + spell.announcement + caster.name + " for \033[1;31;40m" + str(-spelldamage) + " \033[0mHealth Points.")
    elif spell.effect == "direct":
        if spell.flavor == "Nature" and WrathOfKamarr in caster.talents:
            spelldamage += spelldamage/2
        victim.hp -= spelldamage
        print(caster.name + spell.announcement + victim.name + " for \033[1;31;40m" + str(spelldamage) + " \033[0mdamage!")
        print(victim.name + " has \033[1;32;40m" + str(victim.hp) + "\033[0m health points remaining.\n")
        if hasattr(caster, 'talents'):
            if Atonement in caster.talents or BloodTap in caster.talents:
                caster.hp += spelldamage/2
                print("Dark magics restored " + caster.name + "'s health by \033[1;32;40m" + str(spelldamage/2) + " \033[0mhealth points...")
                if caster.hp > caster.sta:
                    caster.hp = caster.sta
    elif spell.effect == "burn":
        if victim.race == "Tynnin":
            print("Dragons are immune to fire!")
        else:
            if hasattr(caster, 'talents'):
                if DirePlague in caster.talents:
                    spelldamage*=2
            victim.hp -= spelldamage
            print(caster.name + spell.announcement + victim.name + " for \033[1;31;40m" + str(spelldamage) + " \033[0mdamage! It's \033[1;31;40mon fire!\033[0m")
            print(victim.name + " has \033[1;32;40m" + str(victim.hp) + "\033[0m health points remaining.\n")
            victim.status.append("burning")
    elif spell.effect == "poison":
        if victim.race == "Tynnin":
            print("Dragons are immune to poison!")
        else:
            if hasattr(caster, 'talents'):
                if DirePlague in caster.talents:
                    spelldamage*=2
            victim.hp -= spelldamage
            print(caster.name + spell.announcement + victim.name + " for \033[1;31;40m" + str(spelldamage) + " \033[0mdamage! It's \033[1;32;40m poisoned!\033[0m")
            print(victim.name + " has \033[1;32;40m" + str(victim.hp) + "\033[0m health points remaining.\n")
            victim.status.append("poisoned")
    elif spell.effect == "stun":
        victim.status.append("stunned")
        print(caster.name + spell.announcement + victim.name + " for \033[1;31;40m" + str(spelldamage) + " \033[0mdamage! It's stunned for one round...")
        print(victim.name + " has \033[1;32;40m" + str(victim.hp) + "\033[0m health points remaining.\n")
    elif spell.effect == "bigstun":
        if hasattr(victim, 'talents'):
            if AdamantineWill in victim.talents:
                print(victim.name + "'s unbreakble will powered through the stun, snapping them awake instantly!")
            else:
                victim.status.append("badly stunned")
                print(caster.name + spell.announcement + victim.name + " for \033[1;31;40m" + str(spelldamage) + " \033[0mdamage! They're stunned for two rounds...")
                print(victim.name + " has \033[1;32;40m" + str(victim.hp) + "\033[0m health points remaining.\n")
        else:
            victim.status.append("badly stunned")
            print(caster.name + spell.announcement + victim.name + " for \033[1;31;40m" + str(spelldamage) + " \033[0mdamage! It's stunned for two rounds...")
            print(victim.name + " has \033[1;32;40m" + str(victim.hp) + "\033[0m health points remaining.\n")
    elif spell.effect == "atkbuff":
        if caster.companion != None and caster.companion.name in wording:
            caster.companion.atk += caster.companion.atk
            caster.status.append("atkbuffed")
            print(caster.name + spell.announcement + caster.companion.name + ".")
            print(caster.companion.name + "'s attack increases.")
        else:
            caster.atk += caster.atk
            caster.status.append("atkbuffed")
            print(caster.name + spell.announcement + caster.name + ".")
            print(caster.name + "'s attack increases.")
    elif spell.effect == "healthbuff":
        if caster.companion != None and caster.companion.name in wording:
            caster.companion.sta += caster.companion.sta
            caster.companion.hp += caster.companion.sta
            caster.companion.status.append("healthbuffed")
            print(caster.name + spell.announcement + caster.companion.name + ".")
            print(caster.companion.name + "'s health increases.")
        else:
            caster.sta += caster.sta
            caster.hp += caster.sta
            caster.status.append("healthbuffed")
            print(caster.name + spell.announcement + caster.name + ".")
            print(caster.name + "'s health increases.")
    elif spell.effect == "manabuff":
        if caster.companion != None and caster.companion.name in wording:
            caster.companion.wis += caster.companion.wis
            caster.companion.mana += caster.companion.wis
            caster.companion.status.append("manabuffed")
            print(caster.name + spell.announcement + caster.companion.name + ".")
            print(caster.companion.name + "'s mana increases.")
        else:
            caster.wis += caster.wis
            caster.mana += caster.wis
            caster.status.append("manabuffed")
            print(caster.name + spell.announcement + caster.name + ".")
            print(caster.name + "'s mana increases.")
    elif spell.effect == "freespell":
        caster.status.append("freespell")
        print(caster.name + spell.announcement + caster.name + ".")
        print(caster.name + "'s next spell is free.")
    elif spell.effect == "minion":
        if caster.companion != None:
            print("You already have a companion.")
        else:
            print(caster.name + spell.announcement)
            summon_servant(caster, spelldamage)
    elif spell.effect == "item":
        print(caster.name + spell.announcement + caster.name + ".")
        caster.inventory[caster.inventory.index(spelldamage)].quantity += 1
    elif spell.effect == "totem":
        print("\nWhich totem to carve?")
        print("     a) Totem of Fire: Damages the enemy every turn.")
        print("     b) Totem of Water: Heals you every turn.")
        print("     c) Totem of Air: Cleanses you every turn.")
        print("     d) Totem of Earth: Increases your defenses when carried.")
        decision = input("\n>")
        if decision.lower() == "a":
            print(caster.name + " has created a Totem of Fire.")
            caster.inventory[caster.inventory.index(totem_of_fire)].quantity += 1
        elif decision.lower() == "b":
            print(caster.name + " has created a Totem of Water.")
            caster.inventory[caster.inventory.index(totem_of_water)].quantity += 1
        elif decision.lower() == "c":
            print(caster.name + " has created a Totem of Air.")
            caster.inventory[caster.inventory.index(totem_of_air)].quantity += 1
        elif decision.lower() == "d":
            print(caster.name + " has created a Totem of Earth.")
            caster.inventory[caster.inventory.index(totem_of_earth)].quantity += 1
    elif spell.effect == "impale":
        print(caster.name + spell.announcement + caster.name + ".")
        victim.status.append("impaled")
        print(victim.name + " is impaled!")
    elif spell.effect == "unimpale":
        if "impaled" in victim.status:
            victim.hp -= spelldamage
            print(caster.name + spell.announcement + caster.name + ".")
            victim.status.remove("impale")
        else:
            print("Nothing impaled!")
    elif spell.effect == "reflect":
        caster.status.append("reflect")
        print(caster.name + "\033[1;33;40m" + spell.announcement + "..\033[0m")
    elif spell.effect == "immunity":
        caster.status.append("immune")
        print("\033[1;33;40mA protective barrier shimmers around " + caster.name + "!\033[0m")
    elif spell.effect == "frostbite":
        print(caster.name + spell.announcement + victim.name + ".")
        print(victim.name + "'s movement was slowed down!")
        victim.speed = 1
    elif spell.effect == "absorblife":
        print(caster.name + spell.announcement + victim.name + " for \033[1;31;40m" + str(spelldamage) + " \033[0mdamage!")
        print(victim.name + " has \033[1;32;40m" + str(victim.hp) + "\033[0m health points remaining.\n")
        victim.hp -= spelldamage
        caster.hp += spelldamage
        if caster.hp > caster.sta:
            caster.hp = caster.sta
    elif spell.effect == "tp":
        print(caster.name + " ripped a gate to " + spelldamage.name + "!")
        c = random.randint(0, 5)
        if c == 0:
            print("The unstable gate collapses prematurely!")
        else:
            caster.in_combat = 0
            go(spelldamage, caster)
    elif spell.effect == "tamebeast":
        print(caster.name + spell.announcement + victim.name + "...")
        if caster.companion != None:
            print("You already have a companion.")
        else:
            if victim.race == "Beast":
                tame_beast(caster, victim)
            else:
                print("You can't tame that type of enemy.")
    elif spell.effect == "charmdead":
        print(caster.name + spell.announcement + victim.name + "...")
        if caster.companion != None:
            print("You already have a companion.")
        else:
            if victim.race == "Undead" or victim.race == "Demon":
                charm(caster, victim)
            else:
                print("You can only command undead or demons.")
    elif spell.effect == "polymorph":
        pass
    elif spell.effect == "tracking":
        print("Your scouting acumen reveals what creatures dwell here.")
        for i in range(len(caster.location)):
            print("     - " + caster.location.npc_table[i])
    elif spell.effect == "charm":
        print(caster.name + spell.announcement + victim.name + "...")
        if caster.companion != None:
            print("You already have a companion.")
        else:
            chance = random.randint(0, 2)
            if chance == 0:
                charm(caster, victim)
            else:
                print(victim.name + " resisted the spell!")
    elif spell.effect == "mesmerize":
        print(caster.name + spell.announcement + victim.name + "!")
        victim.status.append("mesmerized")
    elif spell.effect == "stealth":
        print(caster.name + spell.announcement)
        caster.in_combat = 0
    elif spell.effect == "backstab":
        if caster.speed > victim.speed:
            victim.hp -= spelldamage*2
            print(caster.name + spell.announcement + victim.name + " in the back for \033[1;31;40m" + str(spelldamage*2) + " \033[0mdamage!")
            print(victim.name + " has \033[1;32;40m" + str(victim.hp) + "\033[0m health points remaining.\n")
        else:
            victim.hp -= spelldamage
            print(caster.name + spell.announcement + victim.name + " for \033[1;31;40m" + str(spelldamage) + " \033[0mdamage!")
            print(victim.name + " has \033[1;32;40m" + str(victim.hp) + "\033[0m health points remaining.\n")


def check_spell(string, caster_spells, caster, victim):
    for i in range(len(caster_spells)):
        if caster_spells[i].name.lower() in string:
            check_if_castable(caster_spells[i], caster, victim, string)
            return
    print("Cast what?")


def check_spellOUT(string, caster_spells, caster):
    for i in range(len(caster_spells)):
        if caster_spells[i].name.lower() in string:
            if caster_spells[i].effect in ["reflect","tp","immunity","item","freespell","manabuff","healthbuff","atkbuff","heal","resurrect","totem"]:
                check_if_castable(caster_spells[i], caster, caster, string)
                return
            else:
                print("Invalid target.")
    print("Cast what?")


def spellbook(caster_spells):
    print("Your spells:")
    for i in range(len(caster_spells)):
        if caster_spells[i].flavor == "Nature": color = "\033[0;32;40m"
        elif caster_spells[i].flavor == "Arcane": color = "\033[1;37;40m"
        elif caster_spells[i].flavor == "Frost": color = "\033[1;36;40m"
        elif caster_spells[i].flavor == "Fire": color = "\033[1;31;40m"
        elif caster_spells[i].flavor == "Holy": color = "\033[1;33;40m"
        elif caster_spells[i].flavor == "Shadow": color = "\033[0;35;40m"
        else: color = "\033[1;37;40m"
        cost_diaplay = ""
        if caster_spells[i].effect in ["heal", "direct", "burn", "poison"]:
            cost_display = " " + str(caster_spells[i].damage) + "*LVL DMG. " + str(caster_spells[i].cost) + " MP."
        print("    " + color + "(" + caster_spells[i].flavor + ")\033[0m " + caster_spells[i].name + ": " + caster_spells[i].description + cost_display)














class Set:
    def __init__(self, weapon, offhand, head, chest, legs, feet, hands, neck, back, finger):
        self.weapon = weapon
        self.offhand = offhand
        self.head = head
        self.chest = chest
        self.legs = legs
        self.feet = feet
        self.hands = hands
        self.neck = neck
        self.back = back
        self.finger = finger


class Inventory:
    def __init__(self, name, plural, category, magnitude, description, quantity, price):
        self.name = name
        self.plural = plural
        self.category = category
        self.magnitude = magnitude
        self.description = description
        self.quantity = quantity
        self.price = price


Fists = Inventory("Fists", "Fists", "Weapon", [0, 0, 0, 0], "Shake them angrily.", 0, 0)
Nothing = Inventory("Nothing", "Nothing", "Armor", [0, 0, 0, 0], "As naked as the day you were born.", 0, 0)


def use_item(item, user, target):
    if item.quantity > 0:
        if item.category == "Explosive":
            print(user.name + " threw a " + item.name + " at " + target.name + " for " + item.magnitude + " damage!")
            target.hp -= item.magnitude
            print(target.name + " has " + target.hp + " HP remaining.")
        elif item.category == "Readable":
            print("You read " + item.name + "...")
            print('    ' + item.magnitude)
        elif item.category == "Book" or item.category == "Scroll":
            if item.magnitude.flavor == "Nature" and user.job in ["Shaman", "Druid", "Ranger"]:
                print(user.name + " read " + item.name + ", learning the Nature spell " + item.magnitude.name + ".")
                user.spells.append(item.magnitude)
                item.quantity -= 1
                return
            elif item.magnitude.flavor == "Arcane" and (user.job in ["Wizard"] or MagicalProficiency in user.talents):
                print(user.name + " read " + item.name + ", learning the Arcane spell " + item.magnitude.name + ".")
                user.spells.append(item.magnitude)
                item.quantity -= 1
                return
            elif item.magnitude.flavor == "Frost" and (user.job in ["Wizard", "Shaman", "Druid", "Necromancer"] or Druidism in user.talents):
                print(user.name + " read " + item.name + ", learning the Frost spell " + item.magnitude.name + ".")
                user.spells.append(item.magnitude)
                item.quantity -= 1
                return
            elif item.magnitude.flavor == "Fire" and (user.job in ["Wizard", "Shaman", "Druid"] or Druidism in user.talents):
                print(user.name + " read " + item.name + ", learning the Fire spell " + item.magnitude.name + ".")
                user.spells.append(item.magnitude)
                item.quantity -= 1
                return
            elif item.magnitude.flavor == "Holy" and user.job in ["Priest", "Paladin"]:
                print(user.name + " read " + item.name + ", learning the Holy spell " + item.magnitude.name + ".")
                user.spells.append(item.magnitude)
                item.quantity -= 1
                return
            elif item.magnitude.flavor == "Shadow" and (user.job in ["Necromancer"] or CalamitousIntent in user.talents or ShadowKnight in user.talents):
                print(user.name + " read " + item.name + ", learning the Shadow spell " + item.magnitude.name + ".")
                user.spells.append(item.magnitude)
                item.quantity -= 1
                return
            else:
                print("Your class can't comprehend that ability.")
        else:
            print("That's not usable.")
    else:
        print("You don't have that.")


def consume(user, item):
    if item.quantity > 0:
        if item.category == "Health Potion" or item.category == "Food":
            user.hp += item.magnitude
            if user.hp > user.sta:
                user.hp = user.sta
            print("It restores " + str(item.magnitude) + " HP.")
            item.quantity -= 1
        elif item.category == "Mana Potion" or item.category == "Drink":
            user.mana += item.magnitude
            if user.mana > user.wis:
                user.mana = user.wis
            print("It restores " + str(item.magnitude) + " Mana.")
            item.quantity -= 1
        elif item.category == "Meal":
            user.hp += item.magnitude
            if user.hp > user.sta:
                user.hp = user.sta
            print("It restores " + str(item.magnitude) + " HP.")
            user.mana += item.magnitude
            if user.mana > user.wis:
                user.mana = user.wis
            print("It restores " + str(item.magnitude) + " Mana.")
            item.quantity -= 1
    else:
        print("You don't have that.")


def item_buff(user, item):
    # Stamina increase
    user.sta += item.magnitude[0]
    user.hp += item.magnitude[0]
    if user.race == "Centaur":
        user.sta += item.magnitude[0]/2
        user.hp += item.magnitude[0]/2
    if ArmorProficiency in user.talents:
        user.sta += item.magnitude[0]/2
        user.hp += item.magnitude[0]/2
    if MightofOx in user.talents:
        user.sta += item.magnitude[0]/2
        user.hp += item.magnitude[0]/2
    if BattleEndurance in user.talents:
        user.sta += item.magnitude[0]/2
        user.hp += item.magnitude[0]/2
    if ShieldOfVengeance in user.talents:
        user.atk += item.magnitude[0]
    # Attack increase
    user.atk += item.magnitude[1]
    if user.race == "Minotaur":
        user.atk += item.magnitude[1]/2
    if WeaponProficiency in user.talents:
        user.atk += item.magnitude[1]/2
    if BladeProficiency in user.talents:
        user.atk += item.magnitude[1]/2
    if MasteryOfArms in user.talents:
        user.atk += item.magnitude[1]
    if BoundlessWisdom in user.talents:
        user.wis += item.magnitude[1]
    # Wisdom increase
    user.wis += item.magnitude[2]
    user.mana += item.magnitude[2]
    if SpiritualVigor in user.talents:
        user.atk += item.magnitude[2]
    if item.magnitude[3] != 0:
        user.spells.append(item.magnitude[3])


def item_debuff(user, item):
    # Stamina decrease
    user.sta -= item.magnitude[0]
    user.hp -= item.magnitude[0]
    if user.race == "Centaur":
        user.sta -= item.magnitude[0]/2
        user.hp -= item.magnitude[0]/2
    if ArmorProficiency in user.talents:
        user.sta -= item.magnitude[0]/2
        user.hp -= item.magnitude[0]/2
    if MightofOx in user.talents:
        user.sta -= item.magnitude[0]/2
        user.hp -= item.magnitude[0]/2
    if BattleEndurance in user.talents:
        user.sta -= item.magnitude[0]/2
        user.hp -= item.magnitude[0]/2
    if ShieldOfVengeance in user.talents:
        user.atk -= item.magnitude[0]
    # Attack decrease
    user.atk -= item.magnitude[1]
    if user.race == "Minotaur":
        user.atk -= item.magnitude[1]/2
    if WeaponProficiency in user.talents:
        user.atk -= item.magnitude[1]/2
    if BladeProficiency in user.talents:
        user.atk -= item.magnitude[1]/2
    if MasteryOfArms in user.talents:
        user.atk -= item.magnitude[1]
    if BoundlessWisdom in user.talents:
        user.wis -= item.magnitude[1]
    # Wisdom decrease
    user.wis -= item.magnitude[2]
    user.mana -= item.magnitude[2]
    if SpiritualVigor in user.talents:
        user.atk -= item.magnitude[2]
    if item.magnitude[3] != 0:
        user.spells.append(item.magnitude[3])


def wear(user, item):
    if item.quantity > 0:
        if item.category in ["Sword", "Axe", "Spear", "Mace", "Staff", "Dagger", "Scythe", "Gun", "Weapon"]:
            if user.set.weapon.name == "Fists":
                user.set.weapon = item
                print("You equipped " + user.set.weapon.name + ".")
                item_buff(user, item)
                item.quantity -= 1
            else:
                print("You already have a " + user.set.weapon.name + ". Remove it first.")
        if item.category == "Head":
            if user.set.head.name == "Nothing":
                user.set.head = item
                print("You equipped " + user.set.head.name + ".")
                item_buff(user, item)
                item.quantity -= 1
            else:
                print("You already have a " + user.set.head.name + ". Remove it first.")
        if item.category == "Offhand":
            if user.set.offhand.name == "Nothing":
                user.set.offhand = item
                print("You equipped " + user.set.offhand.name + ".")
                item_buff(user, item)
                item.quantity -= 1
            else:
                print("You already have a " + user.set.head.name + ". Remove it first.")
        if item.category == "Chest":
            if user.set.chest.name == "Nothing":
                user.set.chest = item
                print("You equipped " + user.set.chest.name + ".")
                item_buff(user, item)
                item.quantity -= 1
            else:
                print("You already have a " + user.set.chest.name + ". Remove it first.")
        if item.category == "Legs":
            if user.set.legs.name == "Nothing":
                user.set.legs = item
                print("You equipped " + user.set.legs.name + ".")
                item_buff(user, item)
                item.quantity -= 1
            else:
                print("You already have a " + user.set.legs.name + ". Remove it first.")
        if item.category == "Feet":
            if user.set.feet.name == "Nothing":
                user.set.feet = item
                print("You equipped " + user.set.feet.name + ".")
                item_buff(user, item)
                item.quantity -= 1
            else:
                print("You already have a " + user.set.feet.name + ". Remove it first.")
        if item.category == "Hands":
            if user.set.hands.name == "Nothing":
                user.set.hands = item
                print("You equipped " + user.set.hands.name + ".")
                item_buff(user, item)
                item.quantity -= 1
            else:
                print("You already have a " + user.set.hands.name + ". Remove it first.")
        if item.category == "Necklace":
            if user.set.neck.name == "Nothing":
                user.set.neck = item
                print("You equipped " + user.set.neck.name + ".")
                item_buff(user, item)
                item.quantity -= 1
            else:
                print("You already have a " + user.set.neck.name + ". Remove it first.")
        if item.category == "Back":
            if user.set.back.name == "Nothing":
                user.set.back = item
                print("You equipped " + user.set.back.name + ".")
                item_buff(user, item)
                item.quantity -= 1
            else:
                print("You already have a " + user.set.back.name + ". Remove it first.")
        if item.category == "Ring":
            user.set.finger.append(item)
            print("You slipped a " + item.name + " on one of your fingers.")
            item_buff(user, item)
            item.quantity -= 1
    else:
        print("You don't have that.")


def remove(user, string):
    string = string.lower()
    if "weapon" in string:
        if user.set.weapon == Fists:
            print("Nothing to remove in that slot.")
        else:
            print("You remove a " + user.set.weapon.name + ".")
            item_debuff(user, user.set.weapon)
            user.inventory[user.inventory.index(user.set.weapon)].quantity += 1
            user.set.weapon = Fists
    if "offhand" in string:
        if user.set.offhand.name == "Nothing":
            print("Nothing to remove in that slot.")
        else:
            print("You remove a " + user.set.offhand.name + ".")
            item_debuff(user, user.set.offhand)
            user.inventory[user.inventory.index(user.set.offhand)].quantity += 1
            user.set.offhand = Nothing
    if "head" in string:
        if user.set.head.name == "Nothing":
            print("Nothing to remove in that slot.")
        else:
            print("You remove a " + user.set.head.name + ".")
            item_debuff(user, user.set.head)
            user.inventory[user.inventory.index(user.set.head)].quantity += 1
            user.set.head = Nothing
    if "chest" in string:
        if user.set.chest.name == "Nothing":
            print("Nothing to remove in that slot.")
        else:
            print("You remove a " + user.set.chest.name + ".")
            item_debuff(user, user.set.chest)
            user.inventory[user.inventory.index(user.set.chest)].quantity += 1
            user.set.chest = Nothing
    if "legs" in string:
        if user.set.legs.name == "Nothing":
            print("Nothing to remove in that slot.")
        else:
            print("You remove a " + user.set.legs.name + ".")
            item_debuff(user, user.set.legs)
            user.inventory[user.inventory.index(user.set.legs)].quantity += 1
            user.set.legs = Nothing
    if "hands" in string:
        if user.set.hands.name == "Nothing":
            print("Nothing to remove in that slot.")
        else:
            print("You remove a " + user.set.hands.name + ".")
            item_debuff(user, user.set.hands)
            user.inventory[user.inventory.index(user.set.hands)].quantity += 1
            user.set.hands = Nothing
    if "feet" in string:
        if user.set.feet.name == "Nothing":
            print("Nothing to remove in that slot.")
        else:
            print("You remove a " + user.set.feet.name + ".")
            item_debuff(user, user.set.feet)
            user.inventory[user.inventory.index(user.set.feet)].quantity += 1
            user.set.feet = Nothing
    if "neck" in string:
        if user.set.neck.name == "Nothing":
            print("Nothing to remove in that slot.")
        else:
            print("You remove a " + user.set.neck.name + ".")
            item_debuff(user, user.set.neck)
            user.inventory[user.inventory.index(user.set.neck)].quantity += 1
            user.set.neck = Nothing
    if "back" in string:
        if user.set.back.name == "Nothing":
            print("Nothing to remove in that slot.")
        else:
            print("You remove a " + user.set.back.name + ".")
            item_debuff(user, user.set.back)
            user.inventory[user.inventory.index(user.set.back)].quantity += 1
            user.set.back = Nothing


def inspect_equipment(user):
    print(user.name + " the " + user.race + " " + user.job)
    print("Level " + str(user.level) + " - " + str(user.xp) + "/" + str(user.xpmax) + " XP.")
    print(str(user.hp) + "/" + str(user.sta) + " HP - " + str(user.mana) + "/" + str(user.wis) + " Mana")
    if "redeemed" in user.status:
        print("+ You are granted the ultimate blessing... Fear nothing.")
    if "immunity" in user.status:
        print("+ Your skin glows with holy light of immunity.")
    if "freespell" in user.status:
        print("+ You can see clearly. Your next spell will cost no mana.")
    if "reflect" in user.status:
        print("+ You're poised to counter-attack...")
    if "healthbuffed" in user.status:
        print("+ Your body is swollen with stamina!")
    if "atkbuffed" in user.status:
        print("+ Your limbs are swollen with strength!")
    if "manabuffed" in user.status:
        print("+ Your mind flows with unprecedented clarity!")
    if "meditation" in user.status:
        print("+ You are slowly regenerating mana.")
    if "Steam Explosion" in user.status:
        print("+ Your next Fire spell will violently thaw your target.")
    if "remorseless" in user.status:
        print("+ You scheme upon your next kill...")
    if "afteheal" in user.status:
        print("+ A past healing spell still lingers in your body.")
    if "burning" in user.status:
        print("- You're on fire!!")
    if "bleeding" in user.status:
        print("- You're bleeding...")
    if "poisoned" in user.status:
        print("- You don't feel so good...")
    if "stunned" in user.status:
        print("- You're stunned...")
    if "badlystunned" in user.status:
        print("- You're knocked out!")
    if "impaled" in user.status:
        print("- There's something in your chest!!")
    print("Head:", user.set.head.name)
    print("Neck:", user.set.neck.name)
    print("Chest:", user.set.chest.name)
    print("Back:", user.set.back.name)
    print("Hands:", user.set.hands.name)
    print("Legs:", user.set.legs.name)
    print("Feet:", user.set.feet.name)
    print("Weapon:", user.set.weapon.name)
    print("Offhand:", user.set.offhand.name)


def check_item(string, user_inventory, user, victim):
    for i in range(len(user_inventory)):
        if user_inventory[i].name.lower() in string:
            if user_inventory[i].category in ["Health Potion", "Mana Potion", "Food", "Drink", "Meal"]:
                consume(user, user.inventory[i])
            else:
                use_item(user.inventory[i], user, victim)
            return
    print("Use what?")


def check_food(string, user_inventory, user):
    for i in range(len(user_inventory)):
        if user_inventory[i].name.lower() in string:
            if user_inventory[i].category in ["Health Potion", "Mana Potion", "Food", "Drink", "Meal"]:
                consume(user, user.inventory[i])
            else:
                print("You can't consume that!")
            return
    print("Consume what?")


def check_weapon(string, user_inventory, user):
    for i in range(len(user_inventory)):
        if user_inventory[i].name.lower() in string:
            if user_inventory[i].category in ["Sword", "Axe", "Spear", "Mace", "Staff", "Dagger", "Offhand", "Head", "Scythe",
                                              "Gun", "Chest", "Legs", "Hands", "Feet", "Back", "Necklace", "Ring", "Weapon"]:
                wear(user, user.inventory[i])
            else:
                print("You can't wear that!")
            return
    print("Equip what?")


def list_inventory(bag):
    print("Your items:")
    for i in range(len(bag)):
        if bag[i].quantity > 0:
            if bag[i].quantity == 1:
                print("(" + str(bag[i].quantity) + ") " + bag[i].name + " - " + bag[i].category + ": " + bag[i].description)
            else:
                print("(" + str(bag[i].quantity) + ") " + bag[i].plural + " - " + bag[i].category + ": " + bag[i].description)
    print("")












class Quest:
    def __init__(self, title, action, object, counter, countertracker, reward, reward2, rewardItem, desc, desc_ongoing, completed, followup):
        self.title = title
        self.action = action
        self.counter = counter
        self.countertacker = countertracker
        self.object = object
        self.reward = reward
        self.reward2 = reward2
        self.rewardItem = rewardItem
        self.desc = desc
        self.desc_ongoing = desc_ongoing
        self.completed = completed
        self.followup = followup


def discuss_quest(pc, giver):
    #   Does the player have that quest already? If yes, read out the quest_ongoing
    if giver.quest in pc.questlog:
        print(giver.quest.desc_ongoing)
        if giver.quest.action == "Collect":
            if pc.inventory[pc.inventory.index(giver.quest.object)].quantity >= giver.quest.counter:
                if giver.quest.counter == 1:
                    print("You relinquish " + giver.quest.object.name + ".")
                else:
                    print("You relinquish " + str(giver.quest.counter) + " " + giver.quest.object.plural + ".")
                pc.inventory[pc.inventory.index(giver.quest.object)].quantity -= giver.quest.counter
                print("Quest Complete. You received " + str(giver.quest.reward) + "g and " + str(giver.quest.reward2) + " XP.")
                print("\n" + giver.name + " says: \"" + giver.quest.completed + "\"")
                pc.inventory[0].quantity += giver.quest.reward
                pc.xp += giver.quest.reward2
                if pc.xp >= pc.xpmax:
                    LevelUp(pc)
                pc.questlog.remove(giver.quest)
                if giver.quest.rewardItem is not None:
                    pc.inventory[pc.inventory.index(giver.quest.rewardItem)].quantity += 1
                    print("You got " + giver.quest.rewardItem)
                giver.quest = giver.quest.followup
                return
            else:
                print("You only have " + str(pc.inventory[pc.inventory.index(giver.quest.object)].quantity) + " of " + str(giver.quest.counter) + " "
                      + giver.quest.object.plural + ".")
                return
        else:
            pass # Add new quest types here.
    #   If not, read out the dialogue behind a quest
    else:
        print(giver.name + ' says: "' + giver.quest.desc + '"')
    #   Allow a player to pick yes or no:
        d = input("\nDo you accept this quest? Y/N: ")
        if d.lower() in ["yes", "y", "accept", "of course", "absolutely"]:
            print("You accepted the quest: " + giver.quest.title)
            pc.questlog.append(giver.quest)
            return
        elif d.lower() in ["n", "no", "decline"]:
            print("You declined the quest.")
            return
        else:
            print("I'll take that as a no.")
            return


def list_quests(pc):
    if len(pc.questlog) == 0:
        print("You aren't on any quests.")
    else:
        for i in range(len(pc.questlog)):
            print(pc.questlog[i].title + " - " + str(pc.inventory[pc.inventory.index(pc.questlog[i].object)].quantity) + " of " + str(pc.questlog[i].counter) + " "
                          + pc.questlog[i].object.name + ".")












class NPC:
    def __init__(self, name, type, description, dialogue, faction, items_sold, quest):
        self.name = name
        self.type = type
        self.description = description
        self.dialogue = dialogue
        self.faction = faction
        self.items_sold = items_sold
        self.quest = quest


def trade(pc, NPC, bag):
    # Display the trader's inventory
    print(NPC.name + "'s items:")
    for i in range(len(bag)):
        print(bag[i].name + " " + "(" + bag[i].category + " item)" + ": " + bag[i].description + ". (" + str(bag[i].price) + "g)")
    trade_ongoing = 1
    while trade_ongoing == 1:
        decide = input("\n>")
        decide = decide.lower()
        if "inventory" in decide:
            list_inventory(pc.inventory)
        # Command for selling: check if it exists in your inventory, then gold qty+item price and item qty -1
        elif "sell" in decide:
            for i in range(len(pc.inventory)):
                if pc.inventory[i].name.lower() in decide:
                    if pc.inventory[i].quantity > 0:
                        pc.inventory[0].quantity += pc.inventory[i].price
                        print("Sold " + pc.inventory[i].name + " for " + str(pc.inventory[i].price) + "g.")
                        pc.inventory[i].quantity -= 1
                    else:
                        print("You don't have one of those.")
        # Command for buying: check if it exists in the npc inventory, then gold qty-item price and item qty +1
        elif "buy" in decide:
            for i in range(len(bag)):
                if bag[i].name.lower() in decide:
                    if pc.inventory[0].quantity >= bag[i].price:
                        pc.inventory[0].quantity -= bag[i].price
                        pc.inventory[pc.inventory.index(bag[i])].quantity += 1
                        print("Bought " + bag[i].name + " for " + str(bag[i].price) + "g.")
                    else:
                        print("You can't afford that.")
        else:
            trade_ongoing = 0
            print("Come again.")


def teach(pc, NPC):
    if pc.job.lower() not in ["knight", "barbarian", "rogue", "monk"]:
        if pc.level >= 3 and "meditation" not in pc.status:
            print(NPC.name + " offers to teach you Meditation (passive mana regen). Y/N? ")
            if input(">").lower() == "y":
                pc.status.append("meditation")
    if pc.job.lower() in ["knight", "warrior"]:
        if pc.level >= 3 and WarriorShout not in pc.spells:
            print(NPC.name + " offers to teach you Guttural Shout (damage buff). Y/N? ")
            if input(">").lower() == "y":
                pc.spells.append(WarriorShout)
        if pc.level >= 5 and WarriorCharge not in pc.spells:
            print(NPC.name + " offers to teach you Charge (single-target stun). Y/N? ")
            if input(">").lower() == "y":
                pc.spells.append(WarriorCharge)
    if pc.job.lower() == "assassin":
        if pc.level >= 3 and Stealth not in pc.spells:
            print(NPC.name + " offers to teach you Stealth. Y/N? ")
            if input(">").lower() == "y":
                pc.spells.append(Stealth)


def attempt_learning(pc, NPC):
    if pc.job.lower() == NPC.type:
        teach(pc, NPC)
    elif pc.job.lower() == "paladin" and NPC.type in ["priest", "paladin"]:
        teach(pc, NPC)
    elif pc.job.lower() in ["knight", "barbarian"] and NPC.type == "warrior":
        teach(pc, NPC)
    else:
        print(NPC.name + " doesn't train your class.")


def teleport(pc, NPC):
    if NPC.name == "Elder Firestorm":
        if pc.location.name == "the Storm Perch":
            print("You ride the Dragon across the sea to Redrock...")
            go(redrock, pc)
            date[0] += 1
        elif pc.location == redrock:
            print("You ride the Dragon across the sea to Tynnin...")
            go(stormperch, pc)
            date[0] += 1


def start_dialogue(player, NPC, keyword):
    keyword = keyword.lower()
    if NPC.name == "High Priest Sakhr":
        if "mits" in keyword:
            print("High Priest Sakhr says: \"Aye, what about 'er?\"")
            print("     a) \"Who was she?\"")
            print("     b) \"Where is she now?\"")
            if player.job == "Wizard":
                print("     c) \"How good was she at the arcane?\"")
            answer = input(">")
            if answer.lower() == "a":
                print("High Priest Sakhr says: \"She was a good lass...  The wife of an old friend. I treated her like a daughter!\"")
            elif answer.lower() == "b":
                print("High Priest Sakhr says: \"I dinnae. She's pro'lly back living with her husband.\"")
            elif answer.lower() == "c" and player.job == "Wizard":
                print("High Priest Sakhr says: \"Aye, she was a wee Wizard just like ye, and a very good one at that!\"")
            else:
                print("High Priest Sakhr says: \"Mhm.\"")
            return
    if "heal" in keyword or "restore" in keyword or "help" in keyword:
        if NPC.type == "priest":
            print(NPC.name + " lays their hand on your head, uttering a few words and restoring your health.")
            player.hp = player.sta
            player.mana = player.wis
        else:
            print(NPC.name + " cannot help you, but advises you to find a priest.")
        return
    if "light" in keyword:
        if NPC.faction == "Dwarf":
            print(NPC.name + " says: \"Aye... Thae light is thae source of our powers. It's thae sentient energy of all livin' bein's. Some o' us learn ta harness "
                             "it, either ta combat ill-willed creatures, or ta heal thae injured.\"")
        elif NPC.faction == "Human":
            print(NPC.name + " says: \"The LIGHT is the power that allies us to smite unruly foes! A creature can only be measured by its righteousness, and such "
                             "righteousness comes from how devoted they are to TRUTH and JUSTICE!\"")
        elif NPC.faction == "Moon Elf":
            print(NPC.name + " says: \"The silvery beams of the moon are our Light... In it, we find truth where it is most hidden, we enlighten the dankest corners "
                             "of the woods, and we safeguard our sacred lands from desecration...\"")
        elif NPC.faction == "Sun Elf":
            print(NPC.name + " says: \"Yes, the elder eye of the White Titan. For millenia, it has served as the veritable fountain of our arcane magicks. Where would "
                             "we be without the light? Likely rotting in the mainland under the guise of righteousness.\"")
        elif NPC.faction == "Ogre":
            print(NPC.name + " says: \"Da light be scary! It make da grass grow faster. Me prefer mossy caverns.\"")
        elif NPC.faction == "Dragon":
            print(NPC.name + " says: \"THE LIGHT IS A PRETENTIOUS BEACON OF SELF RIGHTEOUSNESS FOR THE VILE AND THE DEPRAVED!! THE SO-CALLED \"LIGHT WIELDERS\" SEE US "
                             "AS A THREAT TO THEIR DOMINION, AND CLAIM THE LIGHT SPOKE TO THEM AND ORDERED THEM TO PURGE US! LIES! HERESY! GREED AND GUILE MASQUERADING "
                             "AS SOME SORT OF HOLY COMMAND!!\"")
        else:
            print(NPC.name + " looks at you perplexedly.")
    if ("god" in keyword and "dragon" in keyword) or ("dragon" in keyword and "lord" in keyword) or "odym" in keyword:
        if NPC.faction == "Dwarf":
            print(NPC.name + " says: \"Under all thae't hatred an' savagery, thae Dragon God is merely a misunderstood visionaery.\"")
        elif NPC.faction == "Human":
            print(NPC.name + " says: \"WICKED spawn of hell! The kingpin of the demonic Dragon kind! We must slay him at all costs.\"")
        elif NPC.faction == "Moon Elf":
            print(NPC.name + " says: \"His legions keep the humans at bay from the Blackwood... The enemy of our enemy is our friend.\"")
        elif NPC.faction == "Sun Elf":
            print(NPC.name + " says: \"Argh! Skies help whoever crosses that madman!\"")
        elif NPC.faction == "Ogre":
            print(NPC.name + " says: \"He VERY scary!! DO NOT look at dragon king in da eyes!!\"")
        elif NPC.faction == "Dragon":
            print(NPC.name + " says: \"ALL PRAISE THE MIGHTY GOD-EMPEROR OF SCALES! ASHAKH-MALRAK!!\"")
        else:
            print(NPC.name + " shudders in fear.")


def talk(pc, NPC):
    d = random.randint(0,2)
    print(NPC.name + ' says : "' + NPC.dialogue[d] + '"')
    speech = input("\n>")
    speech = speech.lower()
    if "hail" in speech or "hello" in speech or "hi" in speech or "greeings" in speech:
        print(NPC.name + ' greets you.')
    elif "trade" in speech or "barter" in speech or "buy" in speech or "sell" in speech:
        if NPC.type == "vendor":
            trade(pc, NPC, NPC.items_sold)
        else:
            print(NPC.name + " has nothing to sell.")
    elif "attack" in speech:
        print("Not implemented yet.")
    elif NPC.quest and (NPC.quest.object.name in speech or "job" in speech or "mission" in speech or "quest" in speech or "favor" in speech):
        discuss_quest(pc, NPC)
    elif NPC.quest == None and ("job" in speech or "mission" in speech or "quest" in speech or "favor" in speech):
        print(NPC.name + " has nothing to ask of you at them moment.")
    elif "learn" in speech and NPC.type not in ["guard", "vendor,", "tp", "idle"]:
        attempt_learning(pc, NPC)
    elif NPC.type == "tp" and ("teleport" in speech or "sail" in speech or "travel" in speech or "fly" in speech or "flight" in speech):
        teleport(pc, NPC)
    elif "bye" in speech or "farwell" in speech or "cya" in speech or "leave" in speech:
        print(NPC.name + ' says: "Farewell."')
        return
    else:
        start_dialogue(pc, NPC, speech)


def who(zone):
    for i in range(len(zone.npc_table)):
        if zone.npc_table[i].quest == []:
            print("You see " + zone.npc_table[i].name + ".")
        else:
            print("You see " + zone.npc_table[i].name + ". (!)")


def check_npcs(decision, pc):
    for i in range(len(pc.location.npc_table)):
        if pc.location.npc_table[i].name.lower() in decision.lower():
            talk(pc, pc.location.npc_table[i])
            return
    print("You can't find anyone by that name.")


oldmanmarcus_dialogue = ["There isn't much to do around here but strike the soil.", "There's a nip in the air.", "Check with one of the farmers out back."]
farmer_dialogue = ["Hylonia relies on our hard work.", "Wanna buy something?", "We don't have much to sell, but we hope you appreciate it."]
humanguard_dialogue = ["No loitering.", "Mind your manners.", "Obey."]
officerlanicus_dialogue = ["We serve Whitechapel without question.", "The world will be ours.", "Curse the Dragons."]
officererathos_dialogue = ["We will rise up.", "Just you wait...", "They won't see it coming."]
noble_dialogue = ["Light cleanses lesser beings.", "Praise king Whitechapel!", "We are the Skyborn's chosen people."]
priest_dialogue = ["The Light will grant us victory.", "Yes, child?", "Be cleansed of your sins."]
paladin_dialogue = ["Strike with great vengeance.", "I live to serve all believers.", "Gloria in Lucem."]
student_dialogue = ["Be quick about your business!", "I have somewhere to be!", "The Librarian is the wisest person I know."]
librarian_dialogue = ["Welcome to the heart of all knowledge.", "Every page of every tome is a strand of hair in a luscious lock.", "Metior, Disco, Scio."]
xyrus_dialogue = ["This had better be worth it.", "Prudentia semper.", "The Light is but unmeasured Arcane."]
gardun_dialogue = ["Patience.", "Strike with precision.", "Control your breathing."]
brassam_dialogue = ["Strike!", "Do not waste my time!", "Actions will be taken!"]
tailor_dialogue = ["Browse my wares!", "Sown with love!", "Don't go out naked!"]
smith_dialogue = ["As strong as the mountain.", "Keep it sharp!", "It's hammer time."]
innkeeper_dialogue = ["Stay a while.", "What are you drinking?", "One for the road?"]
aurilius_dialogue = ["Did you read my work?", "Are you new here?", "Appearances are deceiving."]


dwarfguard_dialogue = ["Aye.", "Watch yer back.", "No loiterin'."]
dwarfcommon_dialogue = ["Aye!", "What brings ye here?", "Ya got sumn to say?"]
dminer_dialogue = ["Work truly do be tirin'!", "I miss me wife an' kids!", "How be yer travels?"]
ulid_dialogue = ["OOOOHHH There was once a lad...", "CRYSTAL LAAAAKE, CRYSTAL LAAAAKE", "Two coins a song!"]
ureg_dialogue = ["Handle't.", "Move yer arse.", "No time fer games."]
warplanner_dialogue = ["Move on, young'n.", "Stae safe.", "Haul out 'ere."]
nolag_dialogue = ["Wanna trade?", "Artifacts fer sale.", "Keep yer manners 'round thae priest."]
utham_dialogue = ["Light bless ye.", "G'day, young'n.", "Dinnae disturb thae priest."]
sakhr_dialogue = ["Any news ov' thae surface?", "Steel yer heart with prayer.", "Watch thae skies, fear thae depths."]
urnn_dialogue = ["Dinnae disturb me!", "I'm workin!", "LAETAR!"]
orrin_dialogue = ["Skolde!", "Don't mind me elementals.", "Honor thae forge an' thae anvil."]
hajjar_dialogue = ["Ye need armer?", "Ye need weap'ns?", "What ye be doin' here?"]
steamgolem_dialogue = ["*pschhhh...*", "*pschhhh...*", "*pschhhh...*"]
strikk_dialogue = ["Watch where ye step!", "Welcome to me workshop!", "Yae need sum'n?"]
larr_dialogue = ["Yae buyin' sum'n?", "How goes it?", "Yae buyin', lad?"]
juris_dialogue = ["Get out", "Iklistzefon for thae dwarves.", "We will have victory."]
urist_dialogue = ["Welc'me tae Iklistzefon.", "What be yaer business 'ere?", "Skolde!"]
dbartend_dialogue = ["Welc'me tae Stonehearth!", "Take a seat!", "What yae drinkin'?"]


watcher_dialogue = ["We are the Watchers.", "Do not disturb the wild.", "Peace."]
stag_dialogue = ["Peace!", "Hello!" "Ahh, the great outdoors!"]
melf_dialogue = ["Peace.", "Il'tah, y'layl.", "Yes?"]
melfguard_dialogue = ["Peace.", "Go, now.", "Yes?"]
wisp_dialogue = ["<buzzes>", "<sparkles>", "<rings>"]
elftrader_dialogue = ["Goods for sale.", "Your gold is welcome here.", "Behold my wares."]
elflib_dialogue = ["Peace in knowledge.", "I have seen many millenia.", "Welcome, young one."]
soarer_dialogue = ["To the skies!", "I long for the skies!", "Skawk! Just kidding!"]
caretaker_dialogue = ["Mmhm?", "Yes?", "May I assist you?"]
hierophant_dialogue = ["Obey the wilds.", "Do not disturb our trance.", "Welcome to Tel'layl."]
nayla_dialogue = ["Preservation is our duty.", "Abide to nature.", "Do not loiter."]
embas_dialogue = ["Yeah, sweet cheeks?", "What'cha lookin' at?", "Look, I'm a busy girl."]
sleeper_dialogue = ["Snzz..", "Zzz..", "Mmmzmzz..."]


ogreg_dialogue = ["You beware!", "Me guard!", "Me stand ready!"]
seerred_dialogue = ["What you want?", "No disturb us!", "Me busy. Go away."]
seerblue_dialogue = ["Hello, friend!", "You need?", "Ogor-mog!"]
seerblack_dialogue = ["BEWAAARE", "No disturb us!", "Me dark shaman."]
assmorag_dialogue = ["Me likey work!", "Me carry tool for shamans!", "You want book?"]
takk_dialogue = ["Me fish!", "Me like fishies!", "Me pull fishie out, then me THWACK!!"]
smog_dialogue = ["You need?", "You drink?", "Little one drink?"]
ogre_dialogue = ["Red rock beautiful.", "Me fear dragons!", "Who you be?"]
thog_dialogue = ["thog dont caare", "thog dont caare", "thog dont caare"]
embasdrak_dialogue = ["RAAAHHHH!", "BE QUICK!", "FUCK OFF."]
earthbleed_dialogue = ["WE'RE BUSY.", "YOU SHOULDN'T BE HERE.", "GO AWAY!"]


maenistrin_dialogue = ["Hold your steps in these halls.", "Praise the sun.", "We would spill blood for the sun."]
sunguard_dialogue = ["Do not loiter.", "Praise the sun.", "Watch the dawn."]
elfmage_dialogue = ["Praise the sun!", "We handle the dawn.", "Rise like the sun."]
highmagus_dialogue = ["Yes?", "Do not distract us.", "Disturbance!"]
arcaneprotector_dialogue = ["Mmmh...", "Hmm...", "<warps inside out>"]
dawnwatcher_dialogue = ["Welcome to the sanctuary of Dawn.", "Praise the sun, young one.", "We will persevere."]
selfvendor_dialogue = ["My goods are of the highest quality", "You wish to trade?", "Your coin is welcome here."]
selfbar_dialogue = ["Your coin is welcome here.", "Feast on the arcane.", "We are not stringy about our mana. Feast with us."]
self_dialogue = ["Do not loiter.", "Praise the sun.", "Watch the dawn."]
firetamer_dialogue = ["I enjoy being around these birds!", "Praise the sun!", "Phoenixes are my favorite animal."]
phoenix_dialogue = ["Skawk!", "Tweet!", "Skrr!"]
bbphoenix_dialogue = ["Skwee!", "Eek!", "Skaww!"]
selflib_dialogue = ["Welcome to the heart of knowledge.", "You wish to learn?", "Obey the sun and the elders."]
elfappren_dialogue = ["These classes are killing me.", "What brings you here?", "Quick! I'm late!"]


draguard1_dialogue = ["WE ARE THE VIGIL!", "NO LOITERING!", "RHAAARGHH"]
draguard2_dialogue = ["OBEY!", "BOW DOWN!", "KRAK TANIN-RRAHH"]
draguard_dialogue = ["KNOW YOUR PLACE!", "RGHHHHH", "<grumbles>"]
grimeye_dialogue = ["I AM THE GOD'S FIST", "MOVE ALONG", "GO"]
ashslave_dialogue = ["Urghh...", "It's tiring here...", "Beats being at the ash mines."]
nomad_dialogue = ["Yes?", "The Dragons have a very short temper!", "Watch yourself around here!"]
provis_dialogue = ["I HAVE GOODS", "I SELL", "SHOW ME YOUR COIN"]
salbart_dialogue = ["You drink?", "What do you want?", "Mmmhm?"]
konikki_dialogue = ["I have seen eons...", "Strife fuels the Dragons...", "Watch your step in these halls..."]
mindlash_dialogue = ["I SPEAK FOR THE SPIRITS", "THE VOICES TELL ME TO KILL", "BLOOD FEEDS THE FLAME"]
elderwyrm_dialogue = ["Krazakh shanil ukhan..", "Khiran karakh..", "Uronn nokhaliz"]
whelp_dialogue = ["Rrr!!", "Arry!!", "Skhrr!"]
drakcom_dialogue = ["HAHA YES", "HELLO", "<sniffs>"]
draklegion_dialogue = ["RRARGHHH", "WE ARE WARRIORS", "WE ARE LEGION"]
draktrainee_dialogue = ["I WORK", "FOR THE DRAGON GOD!", "WE ARE A TIDE OF DEATH"]
tracker_dialogue = ["I LIE IN WAIT", "PATIENCE!", "THE DUSKRAIL COMES."]
slashtail_dialogue = ["GO AWAY", "FUCK OFF", "BEGONE, THE GOD DOES NOT TAKE VISITORS"]
gnasher_dialogue = ["BLEARUGHGHH!", "LAVISH BRUTALITY!", "MY JAWS LONGS FOR BLOOD"]
wrathguard_dialogue = ["BOW DOWN!", "YOU ARE IN THE PRESENCE OF A GOD!", "HOLD YOUR HIDE"]
odym_dialogue = ["<guttural growls>", "<rumbles>", "<frowns>"]
firestorm_dialogue = ["Do you wish to [travel], young one?", "Is [travel] on your mind?", "Where would you like to [fly]?"]


#       Humans
farmer = NPC("a hylonian farmer", "vendor", "Tired and lethargic from all the work.", farmer_dialogue, "Human",[], [])
OldManMarcus = NPC("Old Man Marcus", "farmer", "The owner of the local farmland, grizzled with age.", oldmanmarcus_dialogue, "Human", [] ,[])
HumanGuard = NPC("a Human guard", "guard", "A diligent guard for the Human kingdom.", humanguard_dialogue, "Human", [], [])
OfficerLanicus = NPC("Officer Lanicus", "idle", "Sharp, with a stiff posture. Embodies the pride of Hylonia.", officerlanicus_dialogue, "Human", [], [])
OfficerErathos = NPC("Officer Erathos", "idle", "Keep your eyes on this one.", officererathos_dialogue, "Human", [], [])
HylonianNoble = NPC("a Hylonian noble", "idle", "Useless.", noble_dialogue, "Human", [], [])
HighPriest = NPC("a High Priest", "idle", "Touched by the light.", noble_dialogue, "Human", [], [])
GrandKnight = NPC("a Grand Knight", "idle", "In shiny armor!", noble_dialogue, "Human", [], [])
ArchpriestRylai = NPC("Archpriest Rylai", "priest", "A halo of light circles behind his head.", priest_dialogue, "Human", [], [])
PaladinLordAltareus = NPC("Paladin Lord Altareus", "paladin", "His wisened old eyes leer through his golden helmet.", paladin_dialogue, "Human", [], [])
Arcanestudent = NPC("an arcane student", "idle", "Draped in stock purple robes and carrying several tomes.", student_dialogue, "Human", [], [])
Librarian = NPC("The Librarian", "vendor", "A grin stretches across his wrinkled face.", librarian_dialogue, "Human", [], [])
ArchmageXyrus = NPC("Archmage Xyrus", "wizard", "Draped in a colorful robe, with a glowing staff strapped across his back.", xyrus_dialogue, "Human", [], [])
Knight = NPC("a human Knight", "idle", "Clad in shining armor, riding atop a fierce steed.", noble_dialogue, "Human", [], [])
TacticianGardun = NPC("Tactician Gardun", "rogue", "Wields an enormous crossbow, about the size of his whole body.", gardun_dialogue, "Human", [], [])
GeneralBrassam = NPC("General Brassam", "warrior", "His grizzled, scarred war face has seen countless battles.", brassam_dialogue, "Human", [],[])
Tailor = NPC("Tailor Ann", "vendor", "Her face shines with ephemeral beauty as she smiles at you.", tailor_dialogue, "Human", [],[])
Blacksmith = NPC("Smith Jeffrey", "vendor", "His face is soiled from working in the mines.", smith_dialogue, "Human",[ ],[])
Innkeeper = NPC("Innkeeper Alistair", "vendor", "Alistair shines his mugs as he leans to you.", innkeeper_dialogue, "Human", [],[])
EnchanterAurilius = NPC("Enchanter Aurilius", "idle", "Sitting alone, cloaked in an ominous hood.", aurilius_dialogue, "Human", [], [])


#       Dwarves
DwarfGuard = NPC("a Dwarven guard", "guard", "Clad in the gold-trimmed steel armor of Iklistzefon.", dwarfguard_dialogue, "Dwarf", [], [])
DwarfCommoner = NPC("a Dwarven commoner", "idle", "Wrinkled, stout, hairy, an utter party animal.", dwarfcommon_dialogue, "Dwarf", [], [])
ExhaustedMiner = NPC("an exhausted miner", "idle", "Dirtied with grime from the work in the mines.", dminer_dialogue, "Dwarf", [], [])
UlidTheBard = NPC("Ulid the Bard", "rogue", "Won't shut up about the Crystal River or something.", ulid_dialogue, "Dwarf", [], [])
GeneralUreg = NPC("General Ureg", "warrior", "A very mean looking dwarf with lots of face tattoos.", ureg_dialogue, "Dwarf", [], [])
WarplannerRumin = NPC("Warplanner Rumin", "idle", "An old dwarf with many battle scars.", warplanner_dialogue, "Dwarf", [], [])
WeaverNolag = NPC("Weaver Nolag", "vendor", "Stands in front of a huge stock of magical items.", nolag_dialogue, "Dwarf", [], [])
SpeakerUtham = NPC("Speaker Utham", "shaman", "Many idols and fetishes hang from his traditional robe.", utham_dialogue, "Dwarf", [], [])
HighPriestSakhr = NPC("High Priest Sakhr", "priest", "An ivory white beard descends from his wrinkled, pensive old face.", sakhr_dialogue, "Dwarf", [], [])
SmithHajjar = NPC("Grandsmith Hajjar", "vendor", "The black-haired dwarf has a crazed look on his face.", hajjar_dialogue, "Dwarf", [], [])
EarthMoverOrrin = NPC("Earthmover Orrin", "idle", "Draped in red robes, with a circlet of rubies upon his head.", orrin_dialogue, "Dwarf", [], [])
AnvilMasterUrnn = NPC("Anvilmaster Urnn", "idle", "In extremely meditative trance as he hammers the anvil.", urnn_dialogue, "Dwarf", [], [])
SteamGolem = NPC("The Great Steam Golem", "idle", "The construct huffs steam and rattles rhythmically.", steamgolem_dialogue, "Dwarf", [], [])
TinkerStrikk = NPC("Tinker Strig", "idle", "Too busy working on his latest creation. Sparks fly away.", strikk_dialogue, "Dwarf", [], [])
AssistantLarr = NPC("Assistant Larr", "vendor", "Stockpiles his boss' inventions for any investors.", larr_dialogue, "Dwarf", [], [])
AdvisorJuris = NPC("Advisor Juris", "idle", "Eyes you carefully. His brows furrow.", juris_dialogue, "Dwarf", [], [])
KingUrist = NPC("King Urist", "idle", "He leans aside and scratches his enormous ginger beard.", urist_dialogue, "Dwarf", [], [])
StoneGolem = NPC("a Stone Golem", "idle", "Scary.", steamgolem_dialogue, "Dwarf", [], [])
DwarfBartender = NPC("a Dwarven bartender", "vendor", "Carefully shining his glass mugs and brass goblets.", dbartend_dialogue, "Dwarf", [], [])


#       Moon Elf
WatcherHaelev = NPC("Watcher Haelev", "guard", "Clad in shining silver and draped in twilight robes.", watcher_dialogue, "Moon Elf", [], [])
WatcherMyysa = NPC("Watcher Myssa", "guard", "Wields an enormous crescent-shaped glaive.", watcher_dialogue, "Moon Elf", [], [])
StagAurial = NPC("Stag Aurial", "idle", "Stubby little horn tips sit on her forehead.", stag_dialogue, "Stagkin", [], [])
ElvenCommoner = NPC("Elven Commoner", "idle", "Blue-ish gray skinned with long leaf-decorated hair.", melf_dialogue, "Moon Elf", [], [])
ElvenGuard = NPC("Elven Guard", "guard", "Mildly upset glare, yet still as calm and composed as his kin.", melfguard_dialogue, "Moon Elf", [], [])
Wisp = NPC("Wisp", "idle", "A shimmering ball of blue glow. It seems sentient and follows you around.", wisp_dialogue, "Moon Elf", [], [])
Wisp2 = NPC("Wisp", "idle", "A shimmering ball of blue glow. You catch the glimps of a face materializing in it.", wisp_dialogue, "Moon Elf", [], [])
ElvenHomekeeper = NPC("an Elven homekeeper", "vendor", "Draped in trimmed, traditional elven robes.", elftrader_dialogue, "Moon Elf", [], [])
ElvenLibrarian = NPC("an Elven librarian", "vendor", "A long beard descends from his face, as he's considerably elder.", elflib_dialogue, "Moon Elf", [], [])
SoarerSaaryel = NPC("Soarer Saaryel", "druid", "A feathery plumage covers the back of her arms.", soarer_dialogue, "Moon Elf", [], [])
CaretakerUyella = NPC("Caretaker Uyella", "ranger", "Carefully leaning over to tend to her druid sisters.", caretaker_dialogue, "Stagkin", [], [])
HierophantAyella = NPC("Hierophant Ayella", "druid", "Draped in jade green robes, focused in her meditation.", hierophant_dialogue, "Moon Elf", [], [])
PriestessNayla = NPC("Priestess Nayla", "priest", "Draped in ivory robes, tending to the hierophant.", nayla_dialogue, "Moon Elf", [], [])
LunarianEmbassador = NPC("a Lunarian Embassador", "idle", "In a business suit and a lavender skirt, her bunny ears twitch in tandem.", embas_dialogue, "Lunarian", [], [])
SleeperLayalin = NPC("Sleeper Layalin", "idle", "A grizzly bear, curled up on a warm bed.", sleeper_dialogue, "Stagkin", [], [])
CaretakerSynnia = NPC("Caretaker Synnia", "idle", "Often shifts the pillows around and patrols the barrow.", caretaker_dialogue, "Moon Elf", [], [])


#       Ogre
GuardSlipkik = NPC("Guard Slipkik", "guard", "Wraps what seems to be a huge frying pan around his belly.", ogreg_dialogue, "Ogre", [], [])
GuardRokok = NPC("Guard Rokok", "guard", "Wearing what seems to be a huge cooking pot on his head.", ogreg_dialogue, "Ogre", [], [])
SeerOrog = NPC("Seer Orog", "shaman", "His face and belly are painted red.", seerred_dialogue, "Ogre", [], [])
SeerFlimig = NPC("Seer Flimig", "shaman", "His face and belly are painted blue.", seerblue_dialogue, "Ogre", [], [])
SeerToktok = NPC("Seer Toktok", "shaman", "His face and belly are painted black", seerblack_dialogue, "Ogre", [], [])
AssistantMoragg = NPC("Assistant Moragg", "vendor", "Very enthusiastic about his job.", assmorag_dialogue, "Ogre", [], [])
FishermanTakk = NPC("Fisherman Takk", "vendor", "Leans from side to side and hums as he holds the stick.", takk_dialogue, "Ogre", [], [])
BartenderSmog = NPC("Bartender Smog", "vendor", "He's wiping a stone mug that's about the size of your head.", smog_dialogue, "Ogre", [], [])
OgreCommoner = NPC("an Ogre commoner", "idle", "Huge, round, light beige in skin with a jutting jaw.", ogre_dialogue, "Ogre", [], [])
thog = NPC("thog", "idle", "he don't caare", thog_dialogue, "Ogre", [], [])
TynninEmbassador = NPC("Tynnin Embassador", "idle", "Thrashes and looks around frantically.", embasdrak_dialogue, "Dragon", [], [])
EarthbleederRokhmaran = NPC("Earthbleeder Rokhmaran", "idle", "Whips his tail in frenzy as the runes on his scales glow.", earthbleed_dialogue, "Dragon", [], [])


#       Sun Elf
SunguardMaeniStrin = NPC("Sunguard Maeni Strin", "guard", "Her long, flowing white hair is contrasted by her red armor.", maenistrin_dialogue, "Sun Elf", [], [])
SunGuard = NPC("a Sunguard", "guard", "Their ivory skin contrasts their gold-trimmed, blood red armor.", sunguard_dialogue, "Sun Elf", [], [])
ElvenMagus = NPC("a Sun Magus", "idle", "Their long, flowing red robes and condescending stare intimidate you.", elfmage_dialogue, "Sun Elf", [], [])
HighMagusTelenSorian = NPC("High Magus Telen Sorian", "wizard", "He's extremely tall and lanky, his face somewhat vampiric.", highmagus_dialogue, "Sun Elf", [], [])
TowerGuardian = NPC("a Tower guardian", "guard", "Their spiked helmet is fierce. You can't tell their gender.", sunguard_dialogue, "Sun Elf", [], [])
ArcaneProtector = NPC("an Arcane protector", "guard", "A hunched, humanoid ball of arcane energies.", arcaneprotector_dialogue, "Sun Elf", [], [])
DawnwatcherNorianelAran = NPC("Dawnwatcher Norianel Aran", "priest", "His golden robes are breathtakingly beautiful.", dawnwatcher_dialogue, "Sun Elf", [], [])
ElvenSmith = NPC("an Elven smith", "vendor", "Composed as the pile of wares behind him wobbles.", selfvendor_dialogue, "Sun Elf", [], [])
ElvenBartender = NPC("an Elven bartender", "vendor", "His goods are of the highest quality.", selfbar_dialogue, "Sun Elf", [], [])
SElvenCommoner = NPC("an Elven commoner", "idle", "Holds a resting smug face.", self_dialogue, "Sun Elf", [], [])
FiretamerNinilAuronan = NPC("Firetamer Ninil Auronan", "ranger", "Busy watching the fire hawks and phoenixes.", firetamer_dialogue, "Sun Elf", [], [])
PhoenixBird = NPC("a Phoenix bird", "idle", "Sparkles in eternal flames as it circles the skies.", phoenix_dialogue, "Sun Elf", [], [])
PhoenixBaby = NPC("a Phoenix hatchling", "idle", "Tiny, but fearsome!", bbphoenix_dialogue, "Sun Elf", [], [])
SElvenLibrarian = NPC("an Elven Librarian", "vendor", "Wise beyond her years.", selflib_dialogue, "Sun Elf", [], [])
ElvenApprentice = NPC("an Elven apprentice", "idle", "Very young and reckless.", elfappren_dialogue, "Sun Elf", [], [])


#       Dragon
FirstGuard = NPC("the First Guard", "guard", "A fierce stare in his eyes loom over you as he stands unmoving", draguard1_dialogue, "Dragon", [], [])
SecondGuard = NPC("the Second Guard", "guard", "A fierce stare in his eyes loom over you as he stands unmoving", draguard2_dialogue, "Dragon", [], [])
ashslave = NPC("an ashlander slave", "idle", "An utter mess of grey skin and whiteless eyes. Curled in a fetus position", ashslave_dialogue, "Ashlander", [], [])
lessernomad = NPC("a lesser nomad", "idle", "Riding a caravan of tightly fastened goods.", nomad_dialogue, "Ashlander", [], [])
CenturionGrimeye = NPC("Centurion Grimeye", "warrior", "His eyes sparkle with flames as he stands guard.", grimeye_dialogue, "Dragon", [], [])
ReptileGuard = NPC("a Reptile guard", "guard", "Clenched teeth, angry glare, restless thousand meter stare.", draguard_dialogue, "Dragon", [], [])
DrakonidProvisioner = NPC("a Drakonid provisioner", "vendor", "Cares for the massive pile of hoarded goods behind him.", provis_dialogue, "Dragon", [], [])
Salbartender = NPC("a Salamander bartender", "vendor", "Salamanders are quick, agile, witty, and their memory is impressive.", salbart_dialogue, "Dragon", [], [])
SeerKonikki = NPC("Seer Konikki", "priest", "A heavy shell on his back, a humped neck and a calm, elder face.", konikki_dialogue, "Dragon", [], [])
EarthbleederMindlash = NPC("Earthbleeder Mindlash", "shaman", "Swipes his tail frantically as he applies more woad to his face.", mindlash_dialogue, "Dragon", [], [])
AncientWyrm = NPC("an Ancient Wyrm", "idle", "One of the noble, massive winged dragons, calmly attending some sort of ritual.", elderwyrm_dialogue, "Dragon", [], [])
DragonWhelp = NPC("a Dragon whelp", "idle", "Flies and roars around with tiny joy.", whelp_dialogue, "Dragon", [], [])
DrakonidCommoner = NPC("a Drakonid commoner", "idle", "Most Drakonid are furiously bloodthirsty and long for war. Some aren't.", drakcom_dialogue, "Dragon", [], [])
DragonLegionnaire = NPC("a Drakonid legionnaire", "idle", "Clad in light brown spiked armor where scales aren't enough.", draklegion_dialogue, "Dragon", [], [])
ReptileTrainee = NPC("a Reptile trainee", "idle", "Reptiles mature unsure of their role in the army, which is decided later.", draktrainee_dialogue, "Dragon", [], [])
TrackwatcherStoneclaw = NPC("Trackwatcher Stoneclaw", "transporter", "Gazes in the distance, awaiting the Duskrail.", tracker_dialogue, "Dragon", [], [])
WarmasterSlashtail = NPC("Warmaster Slashtail", "guard", "Massive spikes spring from his spine and back.", slashtail_dialogue, "Dragon", [], [])
OverlordGnasher = NPC("Overlord Gnasher", "guard", "Teeth furiously clenched, a glaive in hand, he thirsts for war.", gnasher_dialogue, "Dragon", [], [])
EliteWrathguard = NPC("an Elite Wrathguard", "guard", "Some of the biggest humanoid Drakonid. Extremely fierce.", wrathguard_dialogue, "Dragon", [], [])
Odym = NPC("Odym, the Dragon God", "idle", "His dreadful stare is like knives flying right into your chest.", odym_dialogue, "Dragon", [], [])
ElderFirestorm = NPC("Elder Firestorm", "tp", "A wise elder dragons with an impressive wingspan, could carry you on his back.", firestorm_dialogue, "Dragon", [], [])








class Enemy:
    def __init__(self, name, hp, atk, speed, bio, status, item_drops, race, ability, tamed):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.speed = speed
        self.bio = bio
        self.status = status
        self.item_drops = item_drops
        self.race = race
        self.ability = ability
        self.tamed = tamed


def attack(attacker, target):
    attackverb = ' hit '
    if hasattr(attacker, 'set'):
        if attacker.set.weapon.category in ["Sword", "Axe", "Scythe"]:
            attackverb = ' slashed '
        elif attacker.set.weapon.category in ["Mace", "Staff"]:
            attackverb = ' bashed '
        elif attacker.set.weapon.category in ["Spear", "Dagger"]:
            attackverb = ' stabbed '
        elif attacker.set.weapon.category == "Gun":
            attackverb = ' shot '
        else:
            attackverb = ' punched '
    if attacker.hp > 0:
        #   Calculating round damage
        round_damage = random.randint(attacker.atk - 5, attacker.atk + 5)
        if "remorseless" in attacker.status:
            print("First strike!!")
            round_damage *= 2
            user.status.remove("remorseless")
        if hasattr(attacker, 'talents'):
            if DeadlyCalm in attacker.talents or Precision in attacker.talents:
                critchance = random.randint(0,2)
                if critchance == 0:
                    round_damage *= 2
                    print("Critical strike! ")
            if Reckoning in attacker.talents and target.race in ["Demon", "Undead"]:
                round_damage *= 2
                print("The holy strike repelled the vile creature!")
            if Murder in attacker.talents and target.race == "Humanoid":
                round_damage += round_damage/5
                print(attacker.name + " went right for the throat!")
            if Butchering in attacker.talents and target.race in ["Beast", "Dragon"]:
                round_damage += round_damage/5
                print(attacker.name + " went for the neck of the beast!")
            if Retribution in attacker.talents:
                round_damage += round_damage/5
        hitdie = random.randint(0, 5)
        #   Calculating dodge chance
        if hasattr(target, 'talents'):
            if (hitdie == 0):
                if (SwiftFootwork in target.talents):
                    print("\033[1;33;40m" + target.name + " dodged the strike masterfully!\033[0m")
                if (HowlingWinds in target.talents):
                    print("\033[1;33;40mA gust of wind slammed into " + attacker.name + ", stopping the attack!\033[0m")
                if (ForcefulDeflection in target.talents):
                    print("\033[1;33;40m" + target.talents + " forcefully deflected the strike!\033[0m")
                if (Blur in target.talents):
                    print("\033[1;33;40m" + attacker.name + " missed, hitting a blur instead!" + "\033[0m")
                round_damage = 0
            if (hitdie in [1, 2]):
                if (Blur in target.talents):
                    print("\033[1;33;40m" + attacker.name + " missed, hitting a blur instead!" + "\033[0m")
                round_damage = 0
        if round_damage < 0:
            round_damage = 0
        #   Miscellaneous on-hit effects
        if "stunned" not in attacker.status and "badly stunned" not in attacker.status  and "mesmerized" not in attacker.status:
            print("\n" + attacker.name + attackverb + target.name + ' for \033[1;31;40m' + str(round_damage) + ' damage!\033[0m')
            if "immune" not in target.status:
                target.hp -= round_damage
                print(target.name + ' has \033[1;32;40m' + str(target.hp) + ' \033[0mhealth points remaining.')
                if "mesmerized" in target.status and round_damage > 0:
                    print(target.name + " snapped awake!!")
                    target.status.remove("mesmerized")
                if hasattr(attacker, 'talents'):
                    if DeepWounds in attacker.talents or DeepWoundsMONK in attacker.talents or JaggedWounds in attacker.talents:
                        target.status.append("bleeding")
                    if Atonement in attacker.talents or BloodTap in attacker.talents:
                        attacker.hp += round_damage
                        print("Dark magics restored " + attacker.name + "'s health by \033[1;32;40m" + str(round_damage) + " \033[0mhealth points...")
                        if attacker.hp > attacker.sta:
                            attacker.hp = attacker.sta
                    if ManyStrikes in attacker.talents:
                        chance = random.randint(0, 3)
                        if chance == 3:
                            target.hp -= round_damage
                            print("Multistrike!! \033[1;31;40m" + str(round_damage) + " damage!\033[0m")
                            target.hp -= round_damage
                            print(target.name + ' has \033[1;32;40m' + str(target.hp) + ' \033[0mhealth points remaining.')
            else:
                print("A spell has rendered " + target.name + "\033[1;33;40m immune!\033[0m")
                target.status.remove("immune")
        if "reflect" in target.status:
            print("A spell reflected damage onto " + attacker.name + "!")
            attacker.hp -= round_damage


def Eattack(attacker, target):
    if len(attacker.ability) > 0:
        ss = random.randint(0, 5)
        if ss == 0:
            cast(attacker.ability[ss], attacker, target, "")
            return
    attack(attacker, target)


def scan(target):
    print(target.bio)
    print(str(target.atk) + " Attack")
    print(str(target.hp) + " Health Points")
    if "immunity" in target.status:
        print("+ Their skin glows with holy light of immunity.")
    if "freespell" in target.status:
        print("+ They can see clearly; their next spell costs no mana.")
    if "reflect" in target.status:
        print("+ They're poised to counter-attack...")
    if "healthbuffed" in target.status:
        print("+ Their body is swollen with stamina!")
    if "atkbuffed" in target.status:
        print("+ Their limbs are swollen with strength!")
    if "manabuffed" in target.status:
        print("+ Their mind flows with unprecedented clarity!")
    if "mesmerized" in target.status:
        print("- They're mesmerized...")
    if "burning" in target.status:
        print("- They're on fire!!")
    if "bleeding" in target.status:
        print("- They're bleeding...")
    if "poisoned" in target.status:
        print("- They don't look very healthy...")
    if "stunned" in target.status:
        print("- They're stunned...")
    if "badlystunned" in target.status:
        print("- They're knocked out!")
    if "impaled" in target.status:
        print("- There's something lodged in their chest!!")


def combat_loop(a, b):
    if a.speed >= b.speed:
        attack(a, b)
        Eattack(b, a)
    else:
        Eattack(b, a)
        attack(a, b)


def dodge(a, b):
    if "badly stunned" not in b.status and "stunned" not in b.status  and "mesmerized" not in b.status:
        if a.speed >= b.speed:
            print(b.name + " strikes!")
            print(a.name + " dodged the attack!")
        else:
            print("They're too quick!")
            Eattack(b, a)


def check_starting_statuses(target):
    if "burning" in target.status:
        print("\n" + target.name + " is burning!")
        target.hp -= target.hp/10
        target.status.remove("burning")
    if "bleeding" in target.status:
        print("\n" + target.name + " is bleeding!")
        target.hp -= target.hp/10
        target.status.remove("bleeding")
    if "poisoned" in target.status:
        print("\n" + target.name + " is poisoned!")
        target.hp -= target.hp/10
        target.status.remove("poisoned")
    if "stunned" in target.status:
        print("\n" + target.name + " is starting to regain consciousness...")
    if "meditation" in target.status:
        if hasattr(target, 'level'):
            target.mana += target.wis/10
        if target.mana > target.wis:
            target.mana = target.wis
    if "regeneration" in target.status:
        hpregen = 5
        if hasattr(target, 'talents') and (Stoicism in target.talents or SecondWind in target.talents or Chloroplast in target.talents):
                hpregen = 10
                target.hp += target.level * (hpregen)
                if target.hp > target.sta:
                    target.hp = target.sta
        else:
            target.hp += hpregen
            if target.hp > target.sta:
                target.hp = target.sta
    if "afterheal" in target.status:
        if hasattr(target, 'sta'):
            print("The echo of a previous healing spell mends " + target.name + " for " + target.sta/10 + " health points.")
            target.hp += target.sta/10
        else:
            print("The echo of a previous healing spell mends " + target.name + " for " + target.hp/10 + " health points.")
        target.status.remove("afterheal")


def check_ending_statuses(target):
    if "stunned" in target.status:
        print("\n" + target.name + " woke up!")
        target.status.remove("stunned")
    if "badly stunned" in target.status:
        print("\n" + target.name + " twirls around aimlessly...")
        target.status.remove("badly stunned")
        target.status.append("stunned")
    if "mesmerized" in target.status:
        chance = random.randint(0, 2)
        if chance == 0:
            print("Mesmerization broke on " + target.name + "!")
            target.status.remove("mesmerized")

    if "atkbuffEND" in target.status:
        target.atk -= target.atk/2
        print("\n" + "Strength fades from " + target.name + "...")
        target.status.remove("atkbuffEND")
    if "atkbuffed" in target.status:
        target.status.remove("atkbuffed")
        target.status.append("atkbuffEND")

    if "healthbuffEND" in target.status:
        percentage = target.hp/target.sta
        target.hp = target.hp * percentage
        target.sta -= target.sta/2
        target.status.remove("healthbuffEND")
    if "healthbuffed" in target.status:
        target.status.remove("healthbuffed")
        target.status.append("healthbuffEND")

    if "manabuffEND" in target.status:
        percentage = target.mana/target.wis
        target.mana = target.mana * percentage
        target.wis -= target.wis/2
        target.status.remove("manabuffEND")
    if "manabuffed" in target.status:
        target.status.remove("manabuffed")
        target.status.append("manabuffEND")


def check_encounter(playa, zone):
    if len(zone.enemy_table) > 0:
        if zone.bossroom == True:
            playa.in_combat = 1
            attacker = generate_enemy(zone)
            #show_combat_gui(playa, attacker.hp, attacker.hp)
            print(attacker.name + " appears!")
            return attacker
        else:
            chance = random.randint(0, 5)
            if chance == 0:
                playa.in_combat = 1
                attacker = generate_enemy(zone)
                #show_combat_gui(playa, attacker.hp, attacker.hp)
                print(attacker.name + " appears!")
                return attacker
        return
    else:
        print("It seems quiet here.")


def find_enemy(playa, zone):
    if len(zone.enemy_table) > 0:
        playa.in_combat = 1
        attacker = generate_enemy(zone)
        #show_combat_gui(playa, attacker.hp, attacker.hp)
        print("You find " + attacker.name + "!")
        start(playa, attacker)
    else:
        print("This place is safe.")


def drop(pc, enemy):
    i = random.randint(0, 9)
    item_dropped = enemy.item_drops[i]
    if item_dropped.name is not "Nothing":
        print("You looted " + item_dropped.name + ".")
        pc.inventory[pc.inventory.index(item_dropped)].quantity += 1


def start(pc, enemy):
    combatant = Enemy(enemy.name, enemy.hp, enemy.atk, enemy.speed, enemy.bio, enemy.status, enemy.item_drops, enemy.race, enemy.ability, enemy.tamed)
    xp_gain = combatant.hp*4
    while (pc.hp > 0) or (combatant.hp > 0):
        decision = input("\n>")
        cls()
        #show_combat_gui(pc, xp_gain/4, combatant.hp)
        decision = decision.lower()
        check_starting_statuses(pc)
        if pc.companion != None:
            check_starting_statuses(pc.companion)
        check_starting_statuses(combatant)
        if decision == "attack" or decision == "strike" or decision == "0" or decision == "a":
            combat_loop(pc, combatant)
            if pc.companion != None:
                Eattack(pc.companion, combatant)
        elif decision == "dodge" or decision == "d":
            if "stunned" not in pc.status and "badly stunned" not in pc.status and "mesmerized" not in pc.status:
                dodge(pc, combatant)
            else:
                print("You're incapcaitated!")
                Eattack(combatant, pc)
            if pc.companion != None:
                Eattack(pc.companion, combatant)
        elif decision == "run" or decision == "flee" or decision == "escape" or decision == "f":
            if "stunned" not in pc.status and "badly stunned" not in pc.status and "mesmerized" not in pc.status:
                print("You make a run for it!")
                pc.in_combat = 0
                break
            else:
                print("You're incapcaitated!")
                Eattack(combatant, pc)
                if pc.companion != None:
                    Eattack(pc.companion, combatant)
        elif decision == "description" or decision == "who" or decision == "what" or decision == "bio" or decision == "i":
            scan(combatant)
        elif "cast" in decision or "c " in decision:
            if "stunned" not in pc.status and "badly stunned" not in pc.status and "mesmerized" not in pc.status:
                check_spell(decision, pc.spells, pc, combatant)
                if pc.in_combat == 1:
                    Eattack(combatant, pc)
                    if pc.companion != None:
                        Eattack(pc.companion, combatant)
            else:
                print("You're incapcaitated!")
                Eattack(combatant, pc)
                if pc.companion != None:
                    Eattack(pc.companion, combatant)
        elif "spellbook" in decision or "spells" in decision or decision == "p":
            spellbook(pc.spells)
        elif "use" in decision or "u " in decision:
            if "stunned" not in pc.status and "badly stunned" not in pc.status and "mesmerized" not in pc.status:
                check_item(decision, pc.inventory, pc, combatant)
                Eattack(combatant, pc)
                if pc.companion != None:
                    Eattack(pc.companion, combatant)
            else:
                print("You're incapacitated!")
                Eattack(combatant, pc)
                if pc.companion != None:
                    Eattack(pc.companion, combatant)
        elif "drink" in decision or "eat" in decision or "consume" in decision or "e " in decision:
            if "stunned" not in pc.status and "badly stunned" not in pc.status and "mesmerized" not in pc.status:
                check_food(decision, pc.inventory, pc)
                Eattack(combatant, pc)
                if pc.companion != None:
                    Eattack(pc.companion, combatant)
            else:
                print("You're incapacitated!")
                Eattack(combatant, pc)
            if pc.companion != None:
                    Eattack(pc.companion, combatant)
        elif "inventory" in decision or "bag" in decision or decision == "b":
            list_inventory(pc.inventory)
        elif "read" in decision:
            check_item(decision, pc.inventory, pc, combatant)
            Eattack(combatant, pc)
        elif "wear" in decision or "equip " in decision or "wield" in decision or "w " in decision:
            check_weapon(decision, pc.inventory, pc)
        elif "inspect" in decision or "equipment" in decision or "set" in decision or "status" in decision or decision == "s":
            inspect_equipment(pc)
        elif "remove" in decision or "clear" in decision or "unequip" in decision or "r " in decision:
            remove(pc, decision)
        elif decision in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            cast_hotkey(decision, combatant, pc)
        else:
            print("What?")
            Eattack(combatant, pc)
        if pc.hp <= 0:
            print(pc.name + ' has died!')
            pc.in_combat = 0
            break
        elif combatant.hp <= 0:
            print(combatant.name + ' has died!')
            print("")
            drop(pc, combatant)
            print("")
            print("You gained " + str(xp_gain) + " XP.")
            print("")
            pc.xp += xp_gain
            if CarcassShaper in pc.talents and pc.companion == None:
                conf = input("Raise a corpse out of your fallen enemy? Y/N ")
                if conf.lower() == 'y':
                    a = combatant
                    a.name = a.name + "'s revived corpse"
                    pc.companion = Companion(a.name, a.name, a.hp, xp_gain/4, a.wis, a.wis, a.atk, a.speed, a.bio, a.status, " slowly limps behind you.", "Undead", a.ability)
            if Remorseless in pc.talents:
                pc.status.append("remorseless")
            if pc.xp >= pc.xpmax:
                LevelUp(pc)
            if pc.location.bossroom == True:
                pc.location.enemy_table.remove(enemy)
                for i in range(len(pc.location.enemy_table)): print("DEBUG " + pc.location.enemy_table[i].name)
            pc.in_combat = 0
            break
        check_ending_statuses(pc)
        if pc.companion != None:
            check_ending_statuses(pc.companion)
            if pc.companion.hp <= 0:
                print(pc.companion.name + " has died...")
                pc.companion = None
        check_ending_statuses(combatant)
        date[2] += 5
        if (date[2] >= 60):
            date[1] += 1
            date[2] -= 60
        if (date[1] >= 24):
            date[0] += 1
            date[1] -= 24


def generate_enemy(zone):
    if len(zone.enemy_table) > 0:
        eID = random.randint(0, len(zone.enemy_table)-1)
        return zone.enemy_table[eID]









class Companion:
    def __init__(self, name, species, hp, sta, mana, wis, atk, speed, bio, status, afkquotes, race, ability):
        self.name = name
        self.species = species
        self.hp = hp
        self.sta = sta
        self.mana = mana
        self.wis = wis
        self.atk = atk
        self.speed = speed
        self.bio = bio
        self.status = status
        self.afkquotes = afkquotes
        self.race = race
        self.ability = ability


def tame_beast(caster, beast):
    print("You attempt to tame " + beast.name + "...")
    print(beast.tamed.species + " joins your party!")
    a = beast.tamed
    caster.companion = Companion(a.name, a.species, a.hp, a.sta, a.mana, a.wis, a.atk, a.speed, a.bio, a.status, a.afkquotes, a.race, a.ability)
    caster.in_combat = 0
    print("\nName " + caster.companion.species + "? Y/N ")
    yn = input("\n>")
    if yn.lower() == "y" or yn.lower() == "yes":
        caster.companion.name = input("\n>")
    else:
        caster.companion.name = caster.companion.species


def charm(caster, a):
    print("You attempt to charm " + a.name + "...")
    print(a.name + " joins your party!")
    caster.companion = Companion(a.name, a.name, a.hp, a.hp, a.mana, a.wis, a.atk, a.speed, a.bio, a.status, " follows compliantly.", a.race, a.ability)
    caster.in_combat = 0


def summon_servant(caster, servant):
    print("You attempt to summon " + servant.name + "...")
    print(servant.name + " joins your party!")
    caster.companion = Companion(servant.name, servant.species, servant.hp, servant.sta, servant.mana, servant.wis, servant.atk, servant.speed, servant.bio, servant.status,
                                 servant.afkquotes, servant.race, servant.ability)


tamed_boar = Companion("", 'the tamed boar', 50, 50, 0, 0, 10, 1, "It snorts at you affectionately.", [], " snorts.", "Beast", [])
tamed_bear = Companion("", 'the tamed bear', 80, 80, 0, 0, 15, 2, "You could probably ride it if you had a harness.", [], " sniffs you.", "Beast", [])
tamed_wolf = Companion("", 'the tamed wolf', 50, 50, 0, 0, 10, 2, "Its tail is wagging.", [], " tries to lick you.", "Beast", [])
arcane_ele = Companion("the arcane servant", "the arcane servant", 10, 10, 50, 50, 10, 1, "The living cloud of arcane shimmers blue.", [], " glows ominously.", "Elemental", [])
summoned_skeleton = Companion("the skeleton", "the skeleton", 30, 30, 0, 0, 10, 1, "A bit creaky, but will work just fine.", [], " rattles ominously.", "Undead", [])
phantasm = Companion("the phantasm", "the phantasm", 20, 20, 0, 0, 20, 1, "It's a mirror image of you!", [], " glimmers.", "Elemental", [])
pwraithguard = Companion("a wraithguard", "the wraithguard", 50, 50, 100, 100, 20, 2, "Its bones creak.", ["meditation"], " creaks and moans.", "Undead", [])
legion = Companion("your military squad", "your military squad", 1000, 1000, 0, 0, 100, 2, "Ranks of soldiers at your service.", [], " stands ready.", "Humanoid", [])
shamwlf = Companion("the spirit wolf", "the spirit wolf", 50, 50, 100, 100, 20, 1, "A guiding spirit in the body of a wolf.", ["meditation"], " howls.", "Elemental", [])
cat = Companion("your familiar", "the black cat", 30, 30, 200, 200, 10, 1, "A magical black cat, serving as your assistant.", ["meditation"], " purrs.", "Elemental", [])
monkclone = Companion("your shadow clone", "your shadow clone", 5, 5, 0, 0, 10, 1, "A fading afterimage of yourself.", [], " copies your movements.", "Elemental", [])
firetotem = Companion("the fire totem", "the fire totem", 10, 10, 100, 100, 20, 1, "A painted totem pole.", ["meditation"], " rumbles and glows red.", "Totem", [])
watertotem = Companion("the water totem", "the water totem", 10, 10, 100, 100, 0, 1, "A painted totem pole.", ["meditation"], " glows azure.", "Totem", [])
airtotem = Companion("the air totem", "the air totem", 10, 10, 100, 100, 0, 1, "A painted totem pole.", ["meditation"], " glows purple.", "Totem", [])













class Zone:
    def __init__(self, name, linked_zones, enemy_table, npc_table, description, lock, bossroom, item_table):
        self.name = name
        self.linked_zones = linked_zones
        self.enemy_table = enemy_table
        self.npc_table = npc_table
        self.description = description
        self.lock = lock
        self.bossroom = bossroom
        self.item_table = item_table


def go(destination, pc):
    if destination.lock == None:
        print("You travel to " + destination.name + "...")
        chance = random.randint(0, 5)
        if chance == 0:
            if len(pc.location.enemy_table) > 0:
                pc.in_combat = 1
                attacker = generate_enemy(pc.location)
                #show_combat_gui(pc, attacker.hp, attacker.hp)
                print(attacker.name + " blocks your path!")
                start(pc, attacker)
        pc.location = destination
        print(pc.location.description)
        date[2] += 50
        if (date[2] >= 60):
            date[1] += 1
            date[2] -= 60
        if (date[1] >= 24):
            date[0] += 1
            date[1] -= 24
        print("")
        if len(pc.location.npc_table) > 0:
            for i in range(len(pc.location.npc_table)):
                if pc.location.npc_table[i].quest == []:
                    print("You see " + pc.location.npc_table[i].name + ".")
                else:
                    print("You see " + pc.location.npc_table[i].name + ". (!)")
    else:
        if pc.inventory[pc.inventory.index(destination.lock)].quantity > 0:
            print("You unlocked " + destination.name + " with " + destination.lock.name + ".")
            destination.lock = None
            go(destination, pc)
        else:
            print("It's locked.")


def check_zones(string, pc):
    for i in range(len(pc.location.linked_zones)):
        if pc.location.linked_zones[i].name.lower() in string:
            go(pc.location.linked_zones[i], pc)
            return
        if str(i) in string:
            go(pc.location.linked_zones[i], pc)
            return
    print("Go where?\n")
    print("Nearby zones:")
    for i in range(len(pc.location.linked_zones)):
        print("g " + str(i) + " - " + pc.location.linked_zones[i].name)


#defining zones
#       NORTHERN KARRA


plains_of_strife = Zone("the Plains of Strife", [], [], [],
                        "The calm winds huff upon the quiet hinterlands of the human kingdom.", None, False, [])
reothian_glades = Zone("the Reothian Glades", [], [], [],
                       "Quiet breeze passes through the clearing. Plains extend to the west, bordered with woodlands to the east.", None, False, [])
hylonian_outskirts = Zone("Hylonian Outskirts", [], [], [OldManMarcus, farmer], "Lush farmlands extend as far as the eye can see. "
                                                                                "Ivory towers of the Crusader Kingdom cover the horizon.", None, False, [])
hylonian_kingdom = Zone("The Crusader Kingdom of Hylonia", [], [], [HumanGuard, OfficerLanicus, OfficerErathos],
                        "Massive ivory towers and rooves of homes and cathedrals dot the city. Puffs of smoke coil out of chimneys and into the clear blue sky."
                        " The atmosphere is supremely awe-inspiring, as people make roam way through the whitestone-paved, gold-tipped streets of the city,"
                        " some visibly more well-endowed than others. In this nation, priests and paladins rule supreme, and the word of the King is law.", None, False, [])
the_whitechapel = Zone("the Whitechapel", [], [], [],
                       "Ruins of a broken chapel lay atop a hill, its once beautiful banners now torn and its windows broken.", None, False, [])
estate_thornhaart = Zone("Estate Thornhaart", [], [], [],
                        "What was once a beautiful mansion embellished with flowers and herbs of all sorts is now a"
                        " decaying shell where spiteful ghouls roam endlessly.", None, False, [])
the_blackwood = Zone("the Blackwood", [], [], [],
                     "The dark woods surrounds you, with leaves bunched so tight that not even light can enter them."
                     " You hear noises of imps cackling and beasts growling. Eyes appear and disappear in the corner"
                     " of your eye as you struggle with your own sanity. Dead, rotting logs and elder roots litter "
                     "the ground in front of you and thick fog keeps you from seeing the other end of the woods.", None, False, [])
creek_of_life = Zone("the Creek of Life", [], [], [], "You find yourself in an odd, circular clearing of the Blackwood. The grass glows with potent"
                                                      " mystical energies as your eyes happen upon a shining crucible in the center. It's surrounded "
                                                      "with roots and many runic symbols.", None, False, [])
crystal_river = Zone("the Crystal River", [], [], [],
                     "Life springs forth from the earth and cascades down into a river. The water flowing by is "
                     "miraculously clear. You can see the gravels at the bottom as the river trails out of the woods.", None, False, [])
tellayl = Zone("Tel'layl", [], [], [], "You finally reach the fabled Tel'layl, home of the Elves of the Moon. The majestic, gigantic tree springing from the earth"
                                       " extends up into the sky as far as your eyes can see. For a moment, you guess if it could reach the stars. Countless homes "
                                       "and vines extend and hang down from the vines of the tree, and countless wisps light the leaves in a breathtaking "
                                       "carnival of colors. Elves appear and disappear, yet tracking their stealthy, agile movements seems impossible.", None, False, [])
iklistzefon = Zone("Iklistzefon", [], [], [], "You enter the humongous gate of Iklistzefon, the hollow mountain. The gigantic structure stands tall before you:"
                                              " cauldrons chained to the ceiling so high that you're unable to see where they's tethered, countless shops and "
                                              "homes build upon the inner rim of the mountain, lakes and waterfalls of lava cascading from the rooves "
                                              "and onto the bellows of the city. Dwarves all around you are walking and working tirelessly. The air is warm"
                                              " with the huffing of smithing tools, and the symphonic clanging of hammers and picks feels like music.", None, False, [])
wetlands = Zone("the Wetlands", [], [], [],
                "A vast bog extends in front of you all the way to the ocean. Rivers break through the shore and continue into the swamp."
                " The hulls of some broken ships litter the edge.", None, False, [])
goldstar = Zone("Goldstar", [], [], [], "The mystical city of the Sun Elves extends in front of you, with towers of gold erected from the marble ground that covers"
                                        " the whole city, statues of sun discs float above hommages to Elves warriors and mages. Slender and fair-skinned nobles "
                                        "carelessly walk around the magocratic metropolis, levitating into their chambers with all sorts of books and papers.", None, False, [])

#       SOUTHERN KARRA


crystal_lake = Zone("the Crystal Lake", [], [], [], "The crystal clear waters of the enchanted river empty into this vast lake. A little island is in the center."
                                                    " You can see the wildlife swimming and jumping around in the healing waters.", None, False, [])
canyon_of_woe = Zone("the Canyon of Woe", [], [], [],
                     "A tall canyon extends in front of you. The path through swirls around as the earth gets redder and redder.", None, False, [])
wilting_steppes = Zone("the Wilting Steppes", [], [], [],
                       "You enter a vast expanse of land. The dirt and grass beneath your feet are sparse and colored a "
                       "light brownish yellow. The emptiness extends for miles and miles, accentuated with hills of "
                       "the same pigeon-shit yellow. You can hear hooves from afar. This land is dying.", None, False, [])
swamp_of_sorrow = Zone("the Swamp of Sorrow", [], [], [],
                       "You enter the deadly bog that's darkened by dying trees as a powerful sense of dread and sadness overcomes "
                       "you. All you can hear is the hissing and whistilng of beasts of the night, dotted with the endless croaking "
                       "of countless frogs. The air smells rancid, and scum covers every inch of the water's surface."
                       " Wading through this mess is hard and going forward is scary. Don't stand still for too long, "
                       "or the thick waters of the swamp will swallow you.", None, False, [])
windy_desert = Zone("Northern Des'ra", [], [], [],
                    "You enter a harsh and unwelcoming desert. The sands seem to shift beneath your feet as endless blasts of sirocco "
                    "and blistering hurricans huff into your face. You struggle to cover your eyes as you wade forth through the dunes.", None, False, [])
desra = Zone("Southern Des'ra", [], [], [],
             "This part of the desert seems somewhat calmer. The harsh blistering wind has given way to the striking, endless sun of the"
             " desert to beam upon your head. You hear ominous clacking and cricketing in the distance. Sand extends in every direction.", None, False, [])
kronmar = Zone("Kronmar Camp", [], [], [], "You happen upon the camp site of a warrior tribe. The men here are burly and brown-skinned. They wield massive steel"
                                           " weapons and wear bandit masks. They don't seem to pay attention to you.", None, False, [])
khanfusaj = Zone("Khanfusaj", [], [], [], "You fall into the underground insect city of Khanfusaj. The vastness of this vile kingdom extends far beyond anything "
                                          "you would have ever expected while traveling above ground. There are countless massive pillars holding the city up "
                                          "hundreds of meters, inscribed with mystical runes and symbols, webs and nests of all sizes extend around the temples and "
                                          "dens of the city, which are built in intricate, hexagonal engraved black stones.", None, False, [])
redrock = Zone("Red Rock", [], [], [ElderFirestorm],
               "Trailing through the mountain walls, you find yourself in the stone coast of Redrock. Miles of red stone extend beneath "
               "your feet, dotted with cactii and some red stones. Hills appear in the far distance...", None, False, [])
crag = Zone("Crag Hills", [], [], [], "The hills turn out to be carved ogre dens, decorated with all sorts of morbid reminders: from the heads of daring desert "
                                      "adventurers impaled upon spikes to the carapaces and exoskeletons of defeated Khanfusaj swarmers, and the crudely drawn "
                                      "banners of the Ogre Kingdom. Outposts and towers are built upon wooden logs and blades are hung as trophies from them.", None, False, [])
emerald_jungle = Zone("the Emerald Jungle", [], [], [],
                      "A beautiful, lush jungle extends in front of you. Tall green shady trees stand proudly and numerously around,"
                      " covering the sky and blocking most of the sunlight. Odd, unique beasts with alien-like bodies walk around "
                      "and feast off the shining, crystal-textured fruit that hangs off the emerald trees.", None, False, [])
sajrokka = Zone("the Sajrokka", [], [], [],
                "You're lead into the sprawling temple city of the Skullgrin tribe. Circular carvings adorn all sorts of stone pillars and walls, an enormous "
                "arena stands poking out of the thick jungle horizon, and a sense of dread and unease clings to you as the malformed witchdoctors and "
                "spear-wielding hunters stare you down like an alien.", None, False, [])


#       THE GREAT TYNNIN

draenin = Zone("The Dragon Empire", [], [], [], "Carved inside the canyons of the northeastern quarter of the continent is the fearsome Dragon Empire. "
                                                "Its architecture inspires fear in enemies and awe in allies, with buildings clad in dark iron, brimstone "
                                                "and ivory spikes. Gigantic pillars of power loom over the nation, embellished with glowing runes of blood "
                                                "and magma, and the Citadel of Fire and Dread atop a mountain where the fallen God of this domain dwells.", None, False, [])
hatchery = Zone("the Dragon Hatchery", [], [], [], "This pseudo desert is barren and vast, spare for the enormous stone towers dotted with holes and nests "
                                                   "where the broodlings and whelps of the Dragons are raised.", None, False, [])
dread_wastes = Zone("the Dread Wastes", [], [], [], "Vast, untamed swaths of land extend around the black Dragon Empire. Its earth burning black with cinder "
                                                    "and its mountains erupting with rivers of lava and magma, every step might end up with your death.", None, False, [])
vulken = Zone("Mount Vulken", [], [], [], "Sticking from the Dread Wastes like a sore thumb is the humongous Mount Vulken. It's an active volcano, about as tall "
                                          "as your eyes can see. You can hear the moaning of slaves and the striking of tools from a distance, and the dreaded "
                                          "Duskrail links this industrial hellhole to the Dragon Empire.", None, False, [])
ashlands = Zone("the Ashlands", [], [], [], "The Ashlands are endless steppes of cinder and black earth that extend around Mount Vulken. Pockets of tribal "
                                            "races that are unique to this area live here in fear of the Dragons. They are somewhat offered protection "
                                            "by their lords in exchange for a sacrifice of workers and slaves every once in a while.", None, False, [])


#       INDOOR ZONES


#   Hylonia


noblestreet = Zone("the Silver Promenade", [hylonian_kingdom], [], [HylonianNoble, HighPriest, GrandKnight],
                   "You walk into breahtakingly beautiful and unnecessarily lavish street of the Human Kingdom. It's littered with nobles, socialites, and other"
                   " high class rulers and puppetmasters of society.", None, False, [])
church = Zone("the Temple of Light", [hylonian_kingdom], [], [ArchpriestRylai, PaladinLordAltareus, HighPriest],
              "The ceiling is enormous, and as you tilt your head up to observe it, your eyes are filled with reflections of the light beaming into the colorful "
              "crystals of the dome and the tryptich windows. A lavish chandelier hangs high and low humming fills the air.", None, False, [])
mageschool = Zone("Collegium Arcana", [hylonian_kingdom], [], [Arcanestudent, Librarian, ArchmageXyrus, EnchanterAurilius],
                  "Countless pillars extend in front of you, chiseled with swirling vines. An innumerable amount of bookshelves, covering several floors up fills"
                  " your view; everything from scrolls to books beyond comprehension exist in this very building. Countless chroniclers trail the space between "
                  "the shelves, shifting and opening the books. Some disappear into corridors and gates that lead into the inner halls and rooms of the college."
                  " The Librarian's altar is at the end of the building.", None, False, [])
barrack = Zone("the Academy of War", [hylonian_kingdom], [], [HumanGuard, Knight, TacticianGardun, GeneralBrassam],
               "A vast, concrete piece of land rolls in front of you, with warriors sparring left and right and commanders ordering their units into formations. "
               "The constant sound of humming and the loud sounds of phony battles fill the air.", None, False, [])
tradedistrict = Zone("the trade district", [hylonian_kingdom], [], [Tailor, Blacksmith, Innkeeper],
                     "The streets boil with the noise of people bartering and gossiping. Countless shops are open, and numerous vendors are barking in the streets "
                     "for their wares and prices.", None, False, [])


#   Iklisztefon


dwarf_commons = Zone("the Dwarven Commons", [], [], [DwarfGuard, DwarfCommoner],
                     "Upon entering the first ring, you sight several floors of homes and other Dwarven dwellings. Finely built and embellished with engravings of"
                     " limestone and obsidian, bridges gap the tall space between suspended homes carved into the inner rim of the mountain. The wild flail of"
                     " torch flames adds an air of warmth to the cozy homes. Round, stout men and women with beards that nigh touch the ground "
                     " walk casually across the halls.", None, False, [])
stonehearth_inn = Zone("the Stonehearth inn", [dwarf_commons], [], [DwarfBartender, ExhaustedMiner, UlidTheBard],
                       "The moment you step into the Stonehearth inn, a gust of warm air bursts into your face. The echoing sound of laughter and ringing plates "
                       "fills your ears as you make your way to the counter. Stout dwarves are rolling around and getting drunk left and right. This is truly the "
                       "beloved center of their kingdom.", None, False, [])
dwarf_commons.linked_zones = [iklistzefon, stonehearth_inn]
ring_of_war = Zone("the Ring of War", [iklistzefon], [], [DwarfGuard, GeneralUreg, WarplannerRumin],
                   "The Ring of War, an enormous curved hall cared into red stones and paved in obsidian extends around you. War banners of tribes and clans hang "
                   "high from the ceilings and the massive brazier at the center of the hall illuminates the room. Several grand generals and tacticians sit in a "
                   "circle around a map of the world, discussing strategies.", None, False, [])
ring_of_soul = Zone("the Ring of Soul", [iklistzefon], [], [WeaverNolag, SpeakerUtham, HighPriestSakhr],
                    "The Ring of Soul, significantly more spiritual than the others, is carved into white stone and paved with black and white marbles. Ivory "
                    "statues of Dwarven heroes and ancient spirits embellish the walls and hallways, and low hums fill the corridors. Stairs raise up into a "
                    "platform where the High Priest and his speaker sit in contemplation.", None, False, [])
heart_of_the_mountain = Zone("the Heart of the Mountain", [iklistzefon], [], [SmithHajjar, EarthMoverOrrin, AnvilMasterUrnn],
                             "The Humongous forge fills most of the core of the hollow mountain. Waterfalls of lava cascade from cauldrons hung "
                             "up by chains into the ceiling and pool into rivers beneath the raised earth. An enormous anvil, glowing with intimidating magical "
                             "powers is pinned in the center of the room, about as tall as two dwarves and with a surface flat and smooth. Dwarves work tirelessly "
                             "to craft their next masterpiece and to honor their tradition by toiling with metal.", None, False, [])
steamhalls = Zone("the Steam Halls", [iklistzefon], [], [TinkerStrikk, SteamGolem, AssistantLarr],
                  "This hall that extends between the commons and the heart of the mountain is embellished with countless inventions and steel machines that "
                  "are works of deep creativity. Everything from steaming golems to piles of wire and steel that seemingly have no purpose you know of bump and "
                  "whirr in some odd concert. Dwarves with goggles and gloves skitter between the separate rooms, all holding parts or tools.", None, False, [])
hall_of_the_mountain_king = Zone("the Hall of the Mountain King", [iklistzefon], [], [DwarfGuard, AdvisorJuris, KingUrist],
                                 "Trumpets fire in melodic choir as your eyes raise up to see the King of Dwarves. Urist, the Mountain King, sits atop a throne "
                                 "of steel and stone and eyes you carefully. He's surrounded by other guards that share his ginger beard, and an advisor that "
                                 "seemingly does not warm up to you.", None, False, [])


#   Tellayl


the_grove = Zone("the Lush Grove", [tellayl], [], [WatcherHaelev, WatcherMyysa],
                 "True to its name, the grove extends wide in a rim around the tree of life, blossoming with countless plants and flowers. Elves bask in the "
                 "beauty of their ethereal, heavenlike domain, slipping in and out of the shadows, nimbly making their ways between the branches of the tree.", None, False, [])
tree_base = Zone("the base of the Tree", [], [], [StagAurial, ElvenCommoner, ElvenGuard, Wisp],
                 "The base of the tree of life is sturdy, strong, its bark near unchippable and its root unbreakable. It's deeply planted in the ground, you suspect "
                 "as deep as the earth can go. Commoners and wisps lay in relaxation beneath the canopy and discuss matters in their odd tongue.", None, False, [])
tree_branch = Zone("a branch of the Tree", [], [], [ElvenHomekeeper, ElvenLibrarian, Wisp2],
                   "The branches of the Tree of life were numerous, nigh uncountable. They spread in fractal patterns up into the air, each of them thick and sturdy "
                   "enough to support several elven homes built upon it. Some elves peer out of the windows, staring at you.", None, False, [])
tree_top = Zone("the top of the Tree", [], [], [SoarerSaaryel, CaretakerUyella],
                "The top of the Tree of Life holds an enormous canopy of thick, green leaves that seem to radiate some sort of soothing energy. Small wisps cascade like "
                "motes of dust from its top and onto the glades. Elves fade in and out of bird forms, perch upon the thinner branches and stare at the horizon", None, False, [])
altar_of_the_moon = Zone("the Altar of the Moon", [the_grove], [], [HierophantAyella, PriestessNayla, LunarianEmbassador],
                         "Three enormous pillars extend into the sky, curved into the center of the circle like crescent moons. An eclipse is depicted upon the circular "
                         "marble tiled floor, with runic engravings all over the walls and around the rim. The sky is unobstructed as the canopy of the forest gives way "
                         "to an unfettered view of the sky.", None, False, [])
saotaer_barrows = Zone("the Saotaer barrows", [the_grove], [], [SleeperLayalin, CaretakerSynnia],
                       "You descend into the barrow caverns beneath the grove of the tree of life. [Placeholder]", None, False, [])
the_grove.linked_zones = [tellayl, tree_base, altar_of_the_moon, saotaer_barrows]
tree_base.linked_zones = [the_grove, tree_branch]
tree_branch.linked_zones = [tree_base, tree_top]
tree_top.linked_zones = [tree_branch]


#   Redrock


da_mudslide = Zone("Da Mudslide", [], [], [GuardSlipkik, GuardRokok],
                   "You slide down a broad crack in the walls of the barrow, opening into an open ceiling canyon. Mud and stone homes are built and litter the yards, and "
                   "shoddy bridges hang around the heights of the canyon. Many paths lead around to inner cul-de-sacs", None, False, [])
da_campfaya = Zone("Da Campfaya", [da_mudslide], [], [SeerOrog, SeerFlimig, SeerToktok, AssistantMoragg],
                   "A humongous pile of tree logs are ablaze in the center of the cul-de-sac. Many ogres stand in a circle around it, their faces painted in woad and runes "
                   "as they shake idols and pieces of odd voodoo jewelry, adorned with shrunken skulls, as they hum in low tones.", None, False, [])
da_riva = Zone("Da Riva", [da_mudslide], [], [FishermanTakk],
               "A river soiled with used water from the Ogre huts runs in this small cove. Your footsteps echo as you walk down the muddy path.", None, False, [])
da_huts = Zone("Da Huts", [da_mudslide], [], [BartenderSmog, OgreCommoner, thog],
               "Huts of stone are awkwardly built around this \"suburb\" of the ogre city. What seems to be a bar is erected at its center,"
               "with many oafs going in and out of it.", None, False, [])
da_bloodcave = Zone("Da Blood Cave", [da_mudslide], [], [TynninEmbassador, EarthbleederRokhmaran],
                    "After much effort, you manage to slip into the hidden caves at the back of the city. It's quite dark, but you can see two reptilian creatures hunched "
                    "over a ring of runes. You get a nagging sensation that you shouldn't be here...", None, False, [])
da_mudslide.linked_zones = [redrock, da_campfaya, da_riva, da_huts, da_bloodcave]


#   Goldstar


terrace_of_the_sun = Zone("Terrace of the Sun", [], [], [SunguardMaeniStrin, SunGuard, ElvenMagus],
                          "An absolute beauty of architecture, this marble circle paves the entrance into the city with an enormous swirling symbol of the sun "
                          "in its center. Proud elves, tall and ivory-skinned, walk along the paths of the city.", None, False, [])
ivory_tower = Zone("the Ivory Tower", [terrace_of_the_sun], [], [HighMagusTelenSorian, TowerGuardian, ArcaneProtector],
                   "This humongous tower of ivory sticks from the center of the terrace, decorated with arcane lights and flowing purple and gold banners. It houses "
                   "the greatest of the greatest of arcane researchers, and the tip contains jeweled focus that beams onto the city with light.", None, False, [])
sun_watch = Zone("Sunwatch", [ivory_tower], [], [DawnwatcherNorianelAran],
                 "The tip of the tower feels oddly lonely. The view from the balcony is mesmerizing.", None, False, [])
veiled_commons = Zone("the Veiled Commons", [], [], [ElvenSmith, ElvenBartender, SElvenCommoner],
                  "Behind a crystalline veils that separates the terrace from the cozy alleyways of the inner city, you find yourself in the midst of a busy "
                  "street where the lesser minded Elves set up shops.", None, False, [])
phoenixwatch = Zone("Phoenixwatch", [veiled_commons], [], [FiretamerNinilAuronan, PhoenixBird, PhoenixBaby],
                    "A penned little crop, behind the marbled streets of the city, where Firetamers raise Phoenix birds and care for them through their rebirths. "
                    "Magestic flame eagles soar in circles in the sky as their Elven caretakers cheer them on.", None, False, [])
collegia_helios = Zone("Collegia Helios", [terrace_of_the_sun], [], [SElvenLibrarian, ElvenMagus, ElvenApprentice],
                       "The ivory colored, checker marbled heart of Sun Elven culture, houses an innumerable amount of books that contain everything from spells to "
                       "enchantments and odes to the glory of the sun.", None, False, [])
veiled_commons.linked_zones = [phoenixwatch, terrace_of_the_sun]
terrace_of_the_sun.linked_zones = [goldstar, ivory_tower, veiled_commons, collegia_helios]


#   Draenin


mortal_yard = Zone("the Mortal Yard", [], [], [FirstGuard, SecondGuard, ashslave, lessernomad],
                   "The dusty path in front of the gate to the inside of the fortress extends in front of you as the winds huff quietly between the shrubs. Slaves "
                   "and lesser mortals lay on the ground and caravans loaded with goods wait for the opportunity to walk in.", None, False, [])
third_gate = Zone("Draenin Third Gate", [], [], [CenturionGrimeye, ReptileGuard, DrakonidProvisioner, Salbartender],
                  "Massive braziers sparkle atop high pillars of stone from which banners adorned with the royal Dragon insigna swing in the wind. The harsh warmth "
                  "of the canyon gusts calms down in the cul-de-sac where countless horned roofs pop at the horizon: shops, homes, settlements of all kinds.", None, False, [])
stormperch = Zone("the Storm Perch", [], [], [ElderFirestorm],
                  "You climb to the top of the stone tower, and after a few moments, you find yourself near an enormous elder dragon perched on top. His wings rest by his "
                  "side, but you have no doubt their span would be incredible. He gazes into the horizon.", None, False, [])
cove_of_flame = Zone("the Cove of Flame", [], [], [EarthbleederMindlash, SeerKonikki, AncientWyrm],
                     "The dank, dark pits of fog and purple smog sinks deeper into a catacomb built into a cave system. Stalagmites and stalactites act as pillars "
                     "keeping the cave hollow as flames of shamanistic campfires raise smoke high up.", None, False, [])
the_brood_pit = Zone("the Brood Pit", [], [], [DragonWhelp, DrakonidCommoner],
                     "The inner walls of the canyon are lined with holes drilled into it, decorated and stuffed with hay nests of dragonlings and whelps. Some lay "
                     "in hibernation and ritualistic rest as others fly around calmly.", None, False, [])
wargrounds = Zone("Draenin Wargrounds", [], [], [DragonLegionnaire, ReptileTrainee],
                  "The training grounds, paved in grey stone, extend in a circle in the middle of the city. Gladiatorial pits are dug as holes into the earth, as "
                  "barracks marked with large ivory horns spew forth Drakonid after Drakonid who rush into their stations.", None, False, [])
duskrail_station = Zone("Duskrail Station", [], [], [TrackwatcherStoneclaw],
                        "The Duskrail station is busy, boiling with workers who stands vigil for the arrival of the train. Cranes are poised ready to lift "
                        "the goods that arrive and to load the carts that are about to leave.", None, False, [])
the_gauntlet = Zone("the Gauntlet", [], [], [WarmasterSlashtail, OverlordGnasher],
                    "The towering figures guard the entrance to the fortress. Braziers all around you, torches hung in the walls and banners are a constant, aggressive "
                    "reminder of where you're about to step foot.", None, False, [])
draenin_fort = Zone("the Citadel of Dread", [the_gauntlet], [], [EliteWrathguard, Odym],
                    "The inside of the citadel is dark, save for a few flickering torches. Humongous pillars keep the high ceiling up, and the black walls have seen "
                    "shoddy maintenance after millenia. Trophies of heads are hung up from the ceiling and a large carpet shaped as the various continents of the land "
                    "paves the floor. Elite guardians, vizirs and seers stands in a row along the walls. A horrifying figure, a giant of extremely muscular proportions "
                    "sits and eyes you from the end of the hallway with burning red eyes. The shadow from his throne of bones and scales hides his face.", None, False, [])
the_gauntlet.linked_zones = [draenin_fort, wargrounds]
wargrounds.linked_zones = [the_gauntlet, the_brood_pit, third_gate]
third_gate.linked_zones = [wargrounds, the_brood_pit, cove_of_flame, duskrail_station, mortal_yard, stormperch]
stormperch.linked_zones = [third_gate]
the_brood_pit.linked_zones = [wargrounds, third_gate]
cove_of_flame.linked_zones = [third_gate]
duskrail_station.linked_zones = third_gate
mortal_yard.linked_zones = [draenin, third_gate]


#   Estate Thornhaart (dungeon, [])


thorn_key = Inventory("a key to the basement", "keys to the basement", "Key", 0, "Spiky, chiseled with beautiful engravings.", 0, 100)
thornhaart_floor1 = Zone("the first floor", [], [], [], "The first floor is damp and muddy. Moss and spider webs creep through the cracks.", None, False, [])
thornhaart_kitchen = Zone("the kitchen", [], [], [], "The kitchen of the estate is dirty beyond use, littered with expired garbage and rot.", None, True, [])
thornhaart_hallway = Zone("the hallway", [], [], [], "The hallway gives off a creepy, haunted chill that lingers in your neck.", None, False, [])
thornhaart_guestroom = Zone("the guest room", [], [], [], "The room is furnished with pillows that are worn and torn beyond repair.", None, True, [])
thornhaart_floor2 = Zone("the second floor", [], [], [], "The floor feels like it could give off at any moment.", None, False, [])
thornhaart_chamber = Zone("the upper chambers", [], [], [], "You hear ear-piercing wails and heartbreaking moans almost shatter your chest.", None, True, [])
thornhaart_basement = Zone("the basement", [], [], [], "The door unlocks and the stairway gives into a damp, disgusting basement that reeks of death.", thorn_key, True, [])
thornhaart_floor1.linked_zones = [estate_thornhaart, thornhaart_hallway, thornhaart_basement]
thornhaart_hallway.linked_zones = [thornhaart_floor1, thornhaart_kitchen, thornhaart_guestroom, thornhaart_floor2]
thornhaart_kitchen.linked_zones = [thornhaart_hallway]
thornhaart_guestroom.linked_zones = [thornhaart_hallway]
thornhaart_basement.linked_zones = [thornhaart_floor1]
thornhaart_floor2.linked_zones = [thornhaart_hallway, thornhaart_chamber]
thornhaart_chamber.linked_zones = [thornhaart_floor2]


#setting zone connections


plains_of_strife.linked_zones = [reothian_glades, hylonian_outskirts]
reothian_glades.linked_zones = [plains_of_strife, the_blackwood]
hylonian_outskirts.linked_zones = [plains_of_strife, hylonian_kingdom, the_whitechapel]
hylonian_kingdom.linked_zones = [hylonian_outskirts, noblestreet, church, mageschool, barrack, tradedistrict]
the_whitechapel.linked_zones = [hylonian_outskirts, estate_thornhaart]
estate_thornhaart.linked_zones = [the_whitechapel, thornhaart_floor1]
the_blackwood.linked_zones = [reothian_glades, creek_of_life, crystal_river]
creek_of_life.linked_zones = [the_blackwood, tellayl]
crystal_river.linked_zones = [tellayl, creek_of_life, iklistzefon]
tellayl.linked_zones = [crystal_river, creek_of_life, the_grove]
iklistzefon.linked_zones = [crystal_river, wetlands, crystal_lake, dwarf_commons, ring_of_war,
                            ring_of_soul, heart_of_the_mountain, steamhalls, hall_of_the_mountain_king]
wetlands.linked_zones = [crystal_river, iklistzefon, crystal_lake]
goldstar.linked_zones = [wetlands, terrace_of_the_sun]

crystal_lake.linked_zones = [iklistzefon, wetlands, canyon_of_woe]
canyon_of_woe.linked_zones = [crystal_lake, swamp_of_sorrow, wilting_steppes]
swamp_of_sorrow.linked_zones = [canyon_of_woe]
wilting_steppes.linked_zones = [canyon_of_woe, windy_desert]
windy_desert.linked_zones = [wilting_steppes, redrock, kronmar, desra]
redrock.linked_zones = [windy_desert, da_mudslide]
desra.linked_zones = [windy_desert, kronmar, khanfusaj]
kronmar.linked_zones = [windy_desert, desra]
emerald_jungle.linked_zones = [kronmar, desra, sajrokka]
sajrokka.linked_zones = [emerald_jungle]

draenin.linked_zones = [hatchery, vulken, dread_wastes, mortal_yard]
hatchery.linked_zones = [draenin, dread_wastes]
dread_wastes.linked_zones = [draenin, hatchery]
vulken.linked_zones = [draenin, ashlands]
ashlands.linked_zones = [vulken]










# NATURE SPELLS
Lightning = Spell("Lightning Bolt", "Nature", 20, "direct", 20, " thundered ", "Lightning bolt! Lightning bolt!")
HealingSpring = Spell("Healing Spring", "Nature", -30, "heal", 30, " sprung life into ", "When you don't have then nerve to tell them to take a shower.")
Tremor = Spell("Tremor", "Nature", 50, "stun", 65, " burst a pillar of Earth under ", "Someone really fat tripped and fell somewhere.")
Earthquake = Spell("Earthquake", "Nature", 100, "bigstun", 130, " caused an Earthquake under ", "Mother Earth is on her period.")
Torpor = Spell("Torpor", "Nature", 0, "bigstun", 30, " infused Torpor into ", "It's a more mystical-sounding version of \"hibernation\".")
StrengthOfEarth = Spell("Strength of the Earth", "Nature", 100, "healthbuff", 100, " infused the Strength of the Earth into ", "Who'd say no to 100 HP?.")
PropheticVisions = Spell("Prophetic Visions", "Nature", 0, "freespell", 50, " saw visions of ", "Your next spell is free, but this consultation isn't.")
HealingRain = Spell("Healing Rain", "Nature", -50, "heal", 0, " blessed the rains down on ", "Now you too can bless the rains.")
Root = Spell("Root", "Nature", 0, "bigstun", 30, " commanded the earth to wrap around ", "The return of the Avatar.")
AJcreek = Spell("Astral Journey of Wind", creek_of_life, "Nature", "tp", 100, "", "A shortcut through the spirt realm into the Creek of Life")
AJdraenin = Spell("Astral Journey of Fire", ashlands, "Nature", "tp", 100, "", "A shortcut through the spirit realm into the Ashlands")
AJthalj = Spell("Astral Journey of Ice", wetlands, "Nature", "tp", 100, "", "(INCOMPLETE) A shortcut through the spirit realm into Coldskar.")
AJdesrah = Spell("Astral Journey of Earth", redrock, "Nature", "tp", 100, "", "A shortcut through the spirit realm into Redrock.")
#_
Starfall = Spell("Starfall", "Nature", 20, "direct", 20, " shot a tiny star into ", "Twinkle, twinkle, little star.")
Moonfire = Spell("Moonfire", "Nature", 10, "burn", 15, " blasted rays of moon into ", "By the power of the moon...")
Rejuvenation = Spell("Rejuvenation", "Nature", -20, "heal", 20, " rejuvenated ", "Dermatologists HATE them!")
GraspingRoots = Spell("Grasping Roots", "Nature", 0, "bigstun", 30, " sprung roots under ", "As effective as awkwardly bumping into a talkative friend.")
TigerForm = Spell("Tiger Form", "Nature", 0, "atkbuff", 50, " granted the shape of a tiger to ", "\"Please don't call me a furry. I only did it for the buff.\"")
BearForm = Spell("Bear Form", "Nature", 0, "healthbuff", 50, " granted the shape of a bear to ", "Become totally un-bear-able to your enemies.")
OwlForm = Spell("Owl Form", "Nature", 0, "manabuff", 50, " granted the shape of an owl to ", "Who? Caster-spec hybrids, that's who.")
WindWall = Spell("Wind Wall", "Nature", 0, "immunity", 20, " blew a wall of wind before ", 'For maximum effect, scream "Hasagi!"')
Sirocco = Spell("Sirocco", "Nature", 50, "bigstun", 50, " hurled searing winds into ", "Cover your eyes.")
CharmBeast = Spell("Charm Beast", "Nature", 0, "tamebeast", 25, " tried to charm ", 'Now you can call yourself "Dolittle".')
Thorns = Spell("Thorns", "Nature", 0, "reflect", 50, "'s skin sprouted thorns!", "A classic hedgehog move.")
SirenForm = Spell("Siren Form", "Nature", 0, "heal", 0, "'s legs shifted into one large scaly tail, and gills grew on their neck!", "(UNFINISHED)")
TALENTWolf = Spell("Spirit Wolf", "Nature", 0, "minion", 0, " summoned an ancestral beast...", "He-who-yiffs-under-the-clouds.")
TALENTTotem = Spell("Carve Totem", "Nature", 0, "totem", 50, " begins carving a totem...", "Carry it in your hand and recieve an ancestral blessing.")
TALENTTracking = Spell("Tracking", "Nature", 0, "tracking", 0, " analyzes tracks...", "Put your ear to the ground and you can hear the bisons running.")

# ARCANE SPELLS
Minion = Spell("Elemental Minion", "Arcane", 0, "minion", 30, " summoned an Arcane minion!", "Will take out the trash if you ask nicely.")
Conjure = Spell("Conjure Food", "Arcane", 0, "item", 20, " conjured a Mana Bun for ", "\"Conjure grocery list\" would have been more convenient.")
SelfRacial = Spell("Evocation", "Arcane", 25, "evocation", 25, "", "Sun Elves have mastered the art of exploiting their own soul energies.")
Phylonia = Spell("Portal to Hylonia", "Arcane", hylonian_outskirts, "tp", 100, "", "Tear a rift through space and time, leading to Hylonia.")
Pgoldstar = Spell("Portal to Goldstar", "Arcane", goldstar, "tp", 100, "", "Tear a rift through space and time, leading to Goldstar.")
Pabandoned = Spell("Portal to Redrock", "Arcane", redrock, "tp", 100, "", "Tear a rift through space and time, leading somewhere near Redrock.")
Pdesert = Spell("Portal to Des'rah", "Arcane", desra, "tp", 100, "", "Tear a rift through space and time, leading to Des'rah.")
PrismaticAnimation = Spell("Prismatic Animation", "Arcane", phantasm, "minion", 50, " beamed an illusion forward!", "Light clone jutsu!")
TALENTFamiliar = Spell("Conjure Familiar", "Arcane", cat, "minion", 100, " summoned an Arcane familiar!", "A black cat. Perfectly sentient, intelligent and witty.")
TALENTMindControl = Spell("Mind Control", "Arcane", 0, "charm", 100, " tried to charm ", "Wololo, my child.")
TALENTMesmerize = Spell("Mesmerism", "Arcane", 0, "mesmerize", 100, " cast a prism of light that mesmerized ", "\"Ah, fuck, stop shining that thing in my eyes!\"")
TALENTPolymorph = Spell("Polymorph", "Arcane", 0, "polymorph", 100, " polymorphs ", "Turn the titanic elder dragon into a harmless baby bunny.")

# FROST SPELLS
FrostBolt = Spell("Frostbolt", "Frost", 20, "direct", 20, " frostbolted ", "Snowball fighting to the extreme.") 
IceLance = Spell("Ice Lance", "Frost", 10, "impale", 10, " hurled an ice lance at ", "Brutally self-explanatory.")
Release = Spell("Release", "Frost", 50, "unimpale", 0, " shoved the lance out of ", "Jesus christ.")
FlashFreeze = Spell("Flash Freeze", "Frost", 0, "bigstun", 30, " flash froze ", "Now read them their rights.")
Blizzard = Spell("Blizzard", "Frost", 20, "frostbite", 60, " formed a blizzard over ", "The most Entertaining(tm) spell to watch.")
Icewall = Spell("Icewall", "Frost", 0, "healthbuff", 50, " burst a wall of ice in front of ", "That one bullshit move a certain chinese character overuses.")

# FIRE SPELLS
Fireball = Spell("Fireball", "Fire", 20, "direct", 20, " fireballed ", "Likely the most cliche magical projectile in existence.")
Sunfire = Spell("Sunfire", "Fire", 10, "burn", 15, " blased the heat of the sun into ", "Alternate name: \"gamma ray\".")
FlameLick = Spell("Flame Lick", "Fire", 10, "burn", 20, " lashed flames into ", "Somewhat suggestive.")
CoronalBeam = Spell("Coronal Beam", "Fire", 40, "burn", 50, " unleashed a coronal beam on ", "Wear sunscreen.")
LavaBolt = Spell("Lava Bolt", "Fire", 10, "burn", 15, " lava bolted ", "Hurl a ball of molten lava on an enemy.")
MoltenSlag = Spell("Molten Slag", "Fire", 50, "bigstun", 80, " knocked a molten slag into ", "Don't call her that. It's insensitive.")

# HOLY SPELLS
Judgement = Spell("Judgement", "Holy", 20, "direct", 20, " judged ", "Please do not use this on book covers.")
HolyLight = Spell("Holy Light", "Holy", -30, "heal", 30, " healed ", "Direct and efficient. I like that.")
HolyShock = Spell("Holy Shock", "Holy", 10, "stun", 25, " shocked ", "Holy sh--")
EyeForEye = Spell("An Eye For An Eye", "Holy", 100, "reflect", 50, " prepared to counter-attack.", "...and the world goes blind.")
LayOnHands = Spell("Lay On Hands", "Holy", 100, "fullheal", 100, " laid hands on ", "A whole new meaning to \"throwing hands\".")
SoulOfCrusade = Spell("Soul of Crusade", "Holy", 0, "atkbuff", 50, " blessed the Soul of the Crusade into ", "The barbarian counterpart is \"Soul of the Jihad\".")
FinalStand = Spell("Final Stand", "Holy", 0, "immunity", 100, " stood defiantly against ", "Also known as \"Gold Experience Requiem\".")
LightOfDawn = Spell("Light of Dawn", "Holy", 50, "heal", 50, " sprung dawnlight into ", "Just five more minutes, please.")
Smite = Spell("Smite", "Holy", 20, "burn", 30, " smit ", "Also stuns the undead for a while.")
Silence = Spell("Silence!", "Holy", 0, "bigstun", 30, " silenced ", "For those particularly mouthy non-believers.")
Exorcism = Spell("Exorcism", "Holy", 50, "antiundead", 70, " attempted to exorcise ", "Would make a great B-list horror movie.")
Cleanse = Spell("Cleanse", "Holy", 25, "cleanse", 0, " \033[1;33;40mcleansed\033[0m themselves of harmful status effects.", "An alternative to taking a shower.")
DCleanse = Spell("Stone Form", "Holy", 0, "cleanse", 0, " swells up into their stone form, cleansing all harmful status effects!", "Rock solid.")
TALENTLayOnHands = Spell("Lay On Other Hand", "Holy", 100, "fullheal", 100, " laid another hand on ", "For when the audience asks for an encore.")
TALENTAvenging = Spell("Avenging Wrath", "Holy", 0, "atkbuff", 50, " sprouted wings of holy light on ", "Makes you even more paladin-y for a while.")
TALENTRedemption = Spell("Redemption", "Holy", 0, "resurrect", 100, " prayed for the ultimate blessing.", "In case you have unfinished business.")
TALENTGuardian = Spell("Guardian of Ancient Kings", "Holy", 0, "immunity", 150, " prayed for the Guardian of Ancient Kings.", "It must be the work of an enemy stand!")
TALENTShield = Spell("Power Word: Shield", "Holy", 0, "immunity", 50, " surrounded themselves in a bubble of holy light.", "A favorite of Disc priests everywhere.")

# SHADOW SPELLS
Lifetap = Spell("Life Tap", "Shadow", 10, "absorblife", 20, " tapped life from ", "Better than coffee.")
Fear = Spell("Fear", "Shadow", 0, "bigstun", 30, " feared ", "Useful for curing hiccups.")
SummonSkeleton = Spell("Summon Skeleton", "Shadow", 0, "minion", 30, " raised a Skeleton from the earth!", "Also serves as Halloween decorations.")
ShadowBolt = Spell("Shadow Bolt", "Shadow", 20, "direct", 20, " fired a Shadow Bolt at ", "A cackling skull engulfed in black flame. Edgy enough.")
Shadowstep = Spell("Shadowstep", "Shadow", 0, "immunity", 100, " shadowstepped through ", "Shadow walk. I don't even understand, how the fuck my necro talk.")
FeignDeath = Spell("Feign Death", "Shadow", 0, "immunity", 50, " dropped dead in front of ", "Wanna skip school? Your parents will totally fall for it.")
Transfusion = Spell("Trasfusion", "Shadow", 30, "absorblife", 60, " transfused the blood of ", "How do you tell vampires from hemomancers? The latter brand you as \"donor\".")
TALENTWraithGuard = Spell("Summon Wraithguard", "Shadow", 0, "minion", 0, " animated a Wraithguard!", "Undead servants, loyal to your cause.")
TALENTShriek = Spell("Psychic Dread", "Shadow", 0, "bigstun", 30, " screeched at ", "A loud, booming screech that assaults a target's hearing.")
TALENTPhylactery = Spell("Craft Phylactery", "Shadow", 0, "item", 200, " created a Phylactery.", "An item of darkness that stores your soul.")
TALENTOrb = Spell("Summon Orb", "Shadow", 0, "item", 100, " summoned an orb of blood.", "An orb of darkness that stores life energy for later use.")
TALENTCommand = Spell("Command Undead", "Shadow", 0, "charm", 100, " tried to control ", "\m/")

# WEAPON ABILITIES
FistOfKarra = Spell("Fist of Karra", "Item Ability", 100, "direct", 0, " commanded the Fist of Karra upon ", "Best served cold.")
PoisonStrike = Spell("Poison Strike", "Item Ability", 10, "poison", 0, " poisoned ", "You could extract an antidote out of that poison. Or you could do this.")
WhirlOfAekhal = Spell("Whirl of Aekhal", "Shadow", 50, "bigstun", 0, " ripped a black hole behind ", '"The stars swept chill currents that made men shiver in the dark."')
PrayerOfMending = Spell("Prayer of Mending", "Holy", 50, "heal", 0, " prayed for the mending of ", '"Wherever light touches, We shall be. Unfaltering, menders of the broken."'
                                                                                                   '-Skyborn Oath of Mending')
Charge = Spell("Charge", "Item Ability", 50, "bigstun", 0, " charged at ", "The last thing the enemies of the Ramhorn dwarves hear.")
FistBump = Spell("Fist Bump", "Item Ability", 50, "bigstun", 0, " fired the steam-powered fist into ", "Brother fist!")
SummonFireTotem = Spell("Place Fire Totem", "Item Ability", 0, "minion", 0, " planted a fire totem on the ground.", "Fire Nation Inc.")
SummonWaterTotem = Spell("Place Water Totem", "Item Ability", 0, "minion", 0, " planted a water totem on the ground.", "Water Benders Inc.")
SummonAirTotem = Spell("Place Air Totem", "Item Ability", 0, "minion", 0, " planted an air totem on the ground.", "Air Temple Inc... Or whatever remains of them.")

# PHYSICAL MOVES
WarriorShout = Spell("Guttural Shout", "Move", 0, "atkbuff", 0, " growled a strengthening battle cry at ", "YEEEET!")
WarriorCharge = Spell("Charge", "Move", 0, "bigstun", 50, " charged at ", "Your whole body weight, steel and iron included.")
Backstab = Spell("Backstab", "Move", 20, "backstab", 20, " stabbed ", "Deals double damage if you're faster than your victim.")
Stealth = Spell("Stealth", "Move", 0, "stealth", 50, " melded into the shadows...", "Some dumb relatable joke about introversion.")
TALENTCompanions = Spell("Summon Companions", "Move", legion, "minion", 0, " summoned an army by their side!", "Fearless defenders of their general.")
TALENTBloodfury = Spell("Bloodfury", "Move", 0, "atkbuff", 0, " inspired a bloodrage into ", "Never fight a barbarian without tranquilizing darts.")
TALENTBarblur = Spell("Afterimage", "Move", monkclone, "minion", 0, " vibrated an afterimage!", "Pray your enemy doesn't have 20/20.")

starterAssassin = [Shadowstep, FeignDeath]
starterKnight = [EyeForEye, FinalStand]
starterPaladin = [Judgement, HolyLight, HolyShock, LayOnHands]
starterNecro = [Lifetap, SummonSkeleton, IceLance, Release]
starterPriest = [Smite, HolyLight, LightOfDawn, Silence]
starterWizard = [Fireball, FlameLick, Minion, Conjure]
starterShaman = [Lightning, LavaBolt, HealingSpring, Torpor]
starterDruid = [Starfall, Sunfire, Rejuvenation, GraspingRoots, CharmBeast]
starterRanger = [Rejuvenation, CharmBeast]

debugColor = [Fireball, FrostBolt, Conjure, Earthquake, FinalStand, Lifetap]

summoned_skeleton.ability = [Lifetap]
shamwlf.ability = [Lightning]
cat.ability = [FlameLick]
firetotem.ability = [FlameLick]
watertotem.ability = [HealingRain]
airtotem.ability = [Cleanse]



















# Talents essentially operate this way: every two levels you get a choice between three talents.
# You can choose one of either which are basically specs.
class Talent:
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect


#       KNIGHT TALENTS (Guardian - Tactician - Black)
#   Tier 1
ArmorProficiency = Talent("Armor Proficiency", "Attune to worn armor and shields, gaining 150% Stamina value from items.", None)
WeaponProficiency = Talent("Weapon Proficiency", "Attune to carried blades and maces, gaining 150% Attack value from items.", None)
MagicalProficiency = Talent("Magical Proficiency", "Secretly study the ways of Magic, gaining access to the Arcane tree.", None)
#   Tier 2
Stoicism = Talent("Stoicism", "Accept life as it comes, no longer clinging to mortal woes, increasing your HP regeneration.", None)
DeadlyCalm = Talent("Deadly Calm", "Bottle all of your negative energy up, becoming a brooding titan. Increases Critical Strike chance.", None)
Wraithguard = Talent("Wraithguard", "Your sheer hatred and spite allows you to reach to the earth and summon an Undead servant.", TALENTWraithGuard)
#   Tier 3
AdamantineWill = Talent("Adamantine Will", "You are cold, but not uncaring. Patient, but not aloof. You become immune to long stuns.", None)
IronLegion = Talent("Iron Legion", "Your renown and fame attracts soldiers from across Dunia to join your cause and serve you.", TALENTCompanions)
ShadowKnight = Talent("Shadow Knight", "You renounce your mortality and spirit, becoming a half-necromancer and gaining access to the Shadow tree.", None)
knight_talents = [[ArmorProficiency, WeaponProficiency, MagicalProficiency], [Stoicism, DeadlyCalm, Wraithguard], [AdamantineWill, IronLegion, ShadowKnight]]
#       BARBARIAN TALENTS (Pugilist - Armsman - Bloodrage)
#   Tier 1
SwiftFootwork = Talent("Swift Footwork", "You work on improving your stance, increasing your chance to dodge attacks.", None)
BladeProficiency = Talent("Blade Proficiency", "Your proficiency with bladed weapons increases your Attack value from items by 50%.", None)
BloodFury = Talent("Blood Fury", "You channel your inner rage to double the damage of your next attack at the cost of some health.", TALENTBloodfury)
#   Tier 2
SecondWind = Talent("Second Wind", "You grow accustomed to the chaos of combat, increasing your regeneration.", None)
DeepWounds = Talent("Deep Wounds", "You strike with such force that every attack causes your enemy to bleed for another round.", None)
Precision = Talent("Combat Precision", "You hone your ability to think and percieve quickly, increasing your critical strike chance.", None)
#   Tier 3
BattleEndurance = Talent("Battle Endurance", "Your body is littered with scars, as countless battles have hardened you, increasing your Stamina by +50%.", None)
MasteryOfArms = Talent("Mastery of Arms", "Time has passed, and your hands have gripped countless hilts. Gain 200% Attack value from weapons.", None)
Afterimage = Talent("Mirror Image", "Your movements are so quick and erratic that you may spawn a volatile afterimage.", TALENTBarblur)
barbarian_talents = [[SwiftFootwork, BladeProficiency, BloodFury], [SecondWind, DeepWounds, Precision], [BattleEndurance, MasteryOfArms, Afterimage]]
#       PALADIN TALENTS (Crusade - Mercy - Discipline)
#   Tier 1
Retribution = Talent("Retribution", "Cross the path of Retribution, increasing your Attack value by 20%.", None)
Holiness = Talent("Holiness", "Cross the path of Mercy, increasing your Healing by 20%.", None)
Protection = Talent("Protection", "Cross the path of Discipline, increasing Stamina by 20%.", None)
#   Tier 2
Reckoning = Talent("Reckoning", "Take up the mantle of cleansing, doubling your Attack when you fight Demons or Undead.", None)
BidexterousHealing = Talent("Bidexterous Healing", "Realize you have two hands, allowing you to Lay on Hands twice in a row.", None)
ShieldOfVengeance = Talent("Shield of Vengeance", "All Stamina gained from your off-hand counts as Attack value as well.", None)
#   Tier 3
AvengingWrath = Talent("Avenging Wrath", "Gain the ability [Avenging Wrath].", TALENTAvenging)
Redemption = Talent("Redemption", "Allows you to resurrect a fallen companion, or return from death as you were two levels ago.", TALENTRedemption)
GuardianOfKings = Talent("Guardian of Kings", "Summon the Guardian of Ancient Kings, soaking up all damage next round.", TALENTGuardian)
paladin_talents = [[Retribution, Holiness, Protection], [Reckoning, BidexterousHealing, ShieldOfVengeance], [AvengingWrath, Redemption, GuardianOfKings]]
#       SHAMAN TALENTS (Avatar - Totemic - Oracle)
#   Tier 1
RollingThunder = Talent("Rolling Thunder", "[Lightning Bolt] now scales to your level.", None)
TotemWielder = Talent("Totem Wielder", "You take your time to carve totems that you can wield to increase your stats.", TALENTTotem)
LifeSpring = Talent("Life Spring", "You spring waters of life more efficiently, increasing all healing by 20%.", None)
#   Tier 2
SpiritWolf = Talent("Spirit Wolf", "Manifest a Spirit Wolf companion by your side.", TALENTWolf)
RuneCarving = Talent("Rune Carving", "Gain the ability to carve runes to increase your Attack value.", None)
AncestralHealing = Talent("Ancestral Healing", "All your heals leave another smaller heal-over-time effect.", None)
#   Tier 3
Rebirth = Talent("Rebirth", "Grants you the ability to return from death to level 5.", None)
SpiritualVigor = Talent("Spiritual Vigor", "20% of your Intellect gains from items also count to your Attack value.", None)
AncestralVision = Talent("Ancestral Vision", "Grants you the ability [Prophetic Visions].", PropheticVisions)
shaman_talents = [[RollingThunder, TotemWielder, LifeSpring], [SpiritWolf, RuneCarving, AncestralHealing], [Rebirth, SpiritualVigor, AncestralVision]]
#       PRIEST TALENTS (Cleric - Might - Void)
#   Tier 1
Mercy = Talent("Mercy", "Increases your healing by 20%.", None)
HolyShock = Talent("Holy Shock", "Grants you the ability to stun your target.", HolyShock)
CalamitousIntent = Talent("Calamitous Intent", "Grants you access to the Shadow tree.", None)
#   Tier 2
Renewal = Talent("Renewal", "All your heals leave another smaller heal-over-time effect.", None)
PowerWordShield = Talent("Power Word: Shield", "Gives you the ability to shield from damage.", TALENTShield)
DireShriek = Talent("Dire Shriek", "Grants you the ability [Psychic Dread].", TALENTShriek)
#   Tier 3
Compassion = Talent("Compassion", "Your healing is more effective based on your target's missing health.", None)
Atonement = Talent("Atonement", "50% of the magical damage you deal is returned to you as health.", None)
Contempt = Talent("Contempt", "You deal more Shadow damage based on your target's missing health.", None)
priest_talents = [[Mercy, HolyShock, CalamitousIntent], [Renewal, PowerWordShield, DireShriek], [Compassion, Atonement, Contempt]]
#       NECRO TALENTS (Blood - Plague - Lich)
#   Tier 1
BloodTap = Talent("Blood Tap", "All your magical damage heals you for 20% of what you deal.", None)
DirePlague = Talent("Dire Plague", "Your DoT effects are twice as strong.", None)
IceFloes = Talent("Ice Floes", "Your Frost damage is 50% stronger.", None)
#   Tier 2
CarcassShaper = Talent("Carcass Shaper", "You can raise a Revenant after killing an enemy.", None)
Phylactery = Talent("Phylactery", "You can turn any common item into your phylactery, consuming it on death to revive you.", TALENTPhylactery)
HowlingWinds = Talent("Howling Winds", "Your presence is accompanied by howling wind, reducing the enemy's hit chance.", None)
#   Tier 3
CrimsonOrb = Talent("Crimson Orb", "You wield an orb that's charged every time an enemy takes damage and can be consumed to heal you.", TALENTOrb)
CommandUndead = Talent("Command Undead", "You can tame Undead and Demon enemies to serve as your companions.", TALENTCommand)
RemorselessWinter = Talent("Remorseless Winter", "Your sheer presence halves the Attack of your enemies.", None)
necro_talents = [[BloodTap, DirePlague, IceFloes], [CarcassShaper, Phylactery, HowlingWinds], [CrimsonOrb, CommandUndead, RemorselessWinter]]
#       WIZARD TALENTS (Arcane - Elemental - Enchantment)
#   Tier 1
ArcaneFamiliar = Talent("Arcane Familiar", "You can summon an arcane familiar to assist you.", TALENTFamiliar)
FireFrost = Talent("Firefrost Bolt", "After casting a Fire spell, your next Frost spell deals double damage.", None)
Mesmerize = Talent("Mesmerize", "You gain the ability to mesmerize your target, rendering them harmless until attacked.", TALENTMesmerize)
#   Tier 2
BoundlessWisdom = Talent("Boundless Wisdom", "All Attack gains from items also count toward your Wisdom.", None)
WeatherMastery = Talent("Weather Mastery", "Increase both your Fire and Frost damage by 20%", None)
Polymorph = Talent("Polymorph", "Gain the ability to Polymorph your enemy into a harmless critter.", TALENTPolymorph)
#   Tier 3
RealityUnwoven = Talent("Reality, Unwoven", "Renounce your compliance to the rules of reality, increasing all magical damage by 30%.", None)
Adaptability = Talent("Adaptability", "If your enemy was immune to a spell you cast, change its school to another they aren't immune to.", None)
ShackleWill = Talent("Mind Control"," You gain the ability to usher anyone to your ranks.", TALENTMindControl)
wizard_talents = [[ArcaneFamiliar, FireFrost, Mesmerize], [BoundlessWisdom, WeatherMastery, Polymorph], [RealityUnwoven, Adaptability, ShackleWill]]
#       DRUID TALENTS (Astral - Feral - Mender)
#   Tier 1
Balance = Talent("Balance", "Your Nature spells do more damage at night while your Fire spells do more damage during the day.", None)
Camouflage = Talent("Camouflage", "Gain the ability to stealth around.", Stealth)
Swiftmend = Talent("Swiftmend", "Gain the ability to cancel a HoT and do its full healing direcly.", None) #UNFINISHED -------------------------------------------
#   Tier 2
Eclipse = Talent("Eclipse", "Gain the ability to control the cycle of Night and Day.", "druideclipse") #UNFINISHED -----------------------------------------------
JaggedWounds = Talent("Jagged Wounds", "All of your attacks leave a faint bleed effect.", None)
Chloroplast = Talent("Chloroplast", "Increase your and your companion's health regeneration by 50%.", None)
#   Tier 3
WrathOfKamarr = Talent("Wrath of Kamarr", "Become an embodiment of the wrath of the moon, doubling your Nature damage.", None)
ExaltedStag = Talent("Exalted Stag", "Shapeshift into the form of an Exalted Stag, becoming immune to all damage and pacifying all Beast creatures.", "druidstag") #UNFINISHED
SkinLikeNature = Talent("Skin Like Nature", "All of your health buffs are twice as effective.", None)
druid_talents = [[Balance, Camouflage, Swiftmend], [Eclipse, JaggedWounds, Chloroplast], [WrathOfKamarr, ExaltedStag, SkinLikeNature]]
#       BARD TALENTS (Drummer - Windpipe - String)
#   Tier 1
PercussiveAura = Talent("Percussive Aura", "Your song hit chance scales off your Attack stat.", None)
GraceOfAir = Talent("Grace of Air", "Your song hit chance scales off your Wisdom stat.", None)
Dissonance = Talent("Dissonance", "Your song hit chance scales off your Speed stat.", None)
#   Tier 2
ThrummingPulse = Talent("Thrumming Pulse", "Your health regen rate increases dramatically.", None)
CharmingMelody = Talent("Charming Melody", "Your Charming song is more likely to land.", None)
Alacrity = Talent("Alacrity", "Your Speed stat increases by 1 point.", "bardalacrity")
#   Tier 3
DrumsOfWar = Talent("Drums of War", "Your presence reduces the enemy's Attack stat by 50% of yours.", None)
ExtendedBreath = Talent("Extended Breath", "Your affinity with the windpipe increaese your Stamina dramatically.", None)
Concerto = Talent("Concerto", "Your buffs to your companions increase by 50%.", None)
bard_talents = [[PercussiveAura, GraceOfAir, Dissonance], [ThrummingPulse, CharmingMelody, Alacrity], [DrumsOfWar, ExtendedBreath, Concerto]]
#       ASSASSIN TALENTS (Combat - Subtlety - Assassin)
#   Tier 1
Mobility = Talent("Mobility", "Your Speed stat increases by 1 point.", None)
Malice = Talent("Malice", "Your first strike does double damage.", None)
Remorseless = Talent("Remorseless", "Killing a creature doubles the damage of your next attack.", None)
#   Tier 2
ForcefulDeflection = Talent("Forceful Deflection", "Gain the chance to parry attacks at random.", None)
ShadowDancing = Talent("Shadow Dancing", "The success rate of your Stealth becomes 100%.", None)
Murder = Talent("Murder", "You deal 20% more damage against Humanoids.", None)
#   Tier 3
SweepingStrikes = Talent("Sweeping Strikes", "Your attacks have a chance to strike another target.", None)
Nightfall = Talent("Nightfall", "You automatically stealth at night with no chance of failure.", None)
Butchering = Talent("Butchering", "You deal 20% more damage against non-humanoids.", None)
assassin_talents = [[Mobility, Malice, Remorseless], [ForcefulDeflection, ShadowDancing, Murder], [SweepingStrikes, Nightfall, Butchering]]
#       MONK TALENTS (Tiger - Crane - Ox)
#   Tier 1
CrouchingTiger = Talent("Crouching Tiger", "You may Stealth like an Assassin.", None)
SpinningCrane = Talent("Spinning Crane", "Your attacks have a chance to strike another target.", None)
MightofOx = Talent("Might of Ox", "Your Stamina stat scales by 120% of your gear.", None)
#   Tier 2
DeepWoundsMONK = Talent("Deep Wounds", "Your attacks leave a bleeding effect on the target", None)
Blur = Talent("Blur", "You move at such speed that 50% of attacks against you miss.", None)
Stomping = Talent("Stomping", "Your first strike in combat deals 50% more damage.", None)
#   Tier 3
ProwlingHunter = Talent("Prowling Hunter", "Your attack damage scales 20% more off your Strength.", None)
ManyStrikes = Talent("Many Strikes", "You have a chance of striking more than once per round.", None)
ShadowClone = Talent("Shadow Clone Jutsu", "You may summon a harmless clone of yourself.", TALENTBarblur)
monk_talents = [[CrouchingTiger, SpinningCrane, MightofOx], [DeepWoundsMONK, Blur, Stomping], [ProwlingHunter, ManyStrikes, ShadowClone]]
#       RANGER TALENTS (Archer - Beastlord - Scout)
#   Tier 1
Fletching = Talent("Fletching", "You gain the ability to fletch arrows and use bows.", None) # UNFINISHED ------------------------------------------
Company = Talent("Company", "You may charm any beast to accompany you.", CharmBeast)
Swiftness = Talent("Swiftness", "Your speed stat increases by 1 point.", None)
#   Tier 2
KeenEye = Talent("Keen Eye", "Your ranged strikes no longer miss.", None)
NaturalBond = Talent("Natural Bond", "Your companions recieve +50% of your own stats.", None)
Tracking = Talent("Tracking", "You may analyze the land to sense all creatures that dwell in it.", TALENTTracking)
#   Tier 3
HailOfArrows = Talent("Hail of Arrows", "Your ranged attacks may strike more than one target per turn.", None)
KingOfBeasts = Talent("King of Beasts", "You may also charm Dragons along with Beasts.", None)
Druidism = Talent("Druidism", "You may cast Nature, Frost and Fire spells.", None)
ranger_talents = [[Fletching, Company, Swiftness], [KeenEye, NaturalBond, Tracking], [HailOfArrows, KingOfBeasts, Druidism]]


def LearnTalent(pc):
    if pc.job == "Knight": talents = knight_talents
    if pc.job == "Barbarian": talents = barbarian_talents
    if pc.job == "Paladin": talents = paladin_talents
    if pc.job == "Shaman": talents = shaman_talents
    if pc.job == "Priest": talents = priest_talents
    if pc.job == "Necromancer": talents = necro_talents
    if pc.job == "Wizard": talents = wizard_talents
    if pc.job == "Druid": talents = druid_talents
    if pc.job == "Bard": talents = bard_talents
    if pc.job == "Assassin": talents = assassin_talents
    if pc.job == "Monk": talents = monk_talents
    if pc.job == "Ranger": talents = ranger_talents
    print("You reached Tier " + str(pc.level//2) + ".")
    print("Choose a talent:\n")
    for i in [0, 1, 2]:
        print("    ", str(i+1), ") ", talents[(pc.level//2)-1][i].name, ": ",  talents[(pc.level//2)-1][i].description)
    while(talents):
        chosen_talent = input("\n>")
        chosen_talent = chosen_talent.lower()
        if "1" in chosen_talent or "2" in chosen_talent or "3" in chosen_talent:
            choice = talents[(pc.level // 2) - 1][int(chosen_talent) - 1]
            print("You learned [" + choice.name + "].")
            pc.talents.append(choice)
            if choice.effect != None:
                pc.spells.append(choice.effect)
            if choice == Mobility or choice == Swiftness:
                pc.speed += 1
            break


def ListTalents(pc):
    if len(pc.talents) == 0:
        print("You have no special talents yet.")
    else:
        print("Your talents:")
        for i in range(len(pc.talents)):
            print("    +" + pc.talents[i].name + ": " + pc.talents[i].description)













# Useless mob junk
Gold = Inventory("a Gold Piece", "Gold Pieces", "Currency", 1, "Useless were it not for international convention.", 100, 1)
GoblinSkin = Inventory("a patch of goblin skin", "patches of goblin skin", "Junk", 0, "Soft and wrinkly, like raw chicken skin.", 0, 20)
TornImpWing = Inventory("a torn imp wing", "torn imp wings", "Junk", 0, "According to all known laws of aviations, an imp shouldn't be able to fly.", 0, 15)
GnollFang = Inventory("a gnoll fang", "gnoll fangs", "Junk", 0, "Not really that sharp.", 0, 20)
CritterFur = Inventory("a patch of critter fur", "patches of critter furs", "Junk", 0, "Soft and stained with blood.", 0, 10)
PatchOfCloth = Inventory("a patch of cloth", "patches of cloth", "Junk", 0, "Remove it, show bob.", 0, 20)
BoneChips = Inventory("a bone chip", "bone chips", "Junk", 0, "Shattered.", 0, 10)
ScarabCarapace = Inventory("a scarab carapace", "scarab carapaces", "Junk", 0, "Somewhat cracked and frail.", 0, 10)
SnakeFang = Inventory("a snake fang", "snake fangs", "Junk", 0, "Pretty sharp.", 0, 10)
Slimeball = Inventory("a ball of slime", "balls of slime", "Junk", 0, "Rubbery texture.", 0, 10)
Scale = Inventory("a reptilian scale", "reptilian scales", "Junk", 0, "They regenerate when pulled off.", 0, 20)
CrocodileFang = Inventory("a crocodile fang", "crocodile fangs", "Junk", 0, "Chipped beyond use.", 0, 10)
Horn = Inventory("a keratin horn", "keratin horns", "Junk", 0, "It's pretty heavy.", 0, 20)
Tusk = Inventory("a broken tusk", "broken tusks", "Junk", 0, "Not as expensive as you think.", 0, 50)
IntactTusk = Inventory("an intact tusk", "intact tusks", "Junk", 0, "Pristine ivory for filthy poachers like you.", 0, 125)
BrokenHoof = Inventory("a broken hoof", "broken hooves", "Junk", 0, "Bleeding bloodhoof.", 0, 20)
OgreEye = Inventory("an ogre eye", "ogre eyes", "Junk", 0, "Gross.", 0, 20)
Beak = Inventory("a torn beak", "torn beaks", "Junk", 0, "The tip is deceptively sharp.", 0, 10)
Feather = Inventory("a feather", "feathers", "Junk", 0, "Birds of it flock together.", 0, 10)
FuzzyLeg = Inventory("a fuzzy leg", "fuzzy legs", "Junk", 0, "Yucky.", 0, 10)
Spinneret = Inventory("a spinneret", "spinnerets", "Junk", 0, "Spits out silk.", 0, 20)
Fang = Inventory("a chipped fang", "chipped fangs", "Junk", 0, "Cracked.", 0, 10)
RippedTendon = Inventory("a tendon", "tendons", "Junk", 0, "Contracts and expands to allow movement.", 0, 20)
Skull = Inventory("a skull", "skulls", "Junk", 0, "Somebody's skull.", 0, 10)
GiantFang = Inventory("a giant fang", "giant fangs", "Junk", 0, "How does it fit in your bag?", 0, 30)
TwitchingLeg = Inventory("a huge twitching leg", "huge twitching legs", "Junk", 0, "Ew.", 0, 30)
TigerFur = Inventory("tiger fur", "tiger furs", "Junk", 0, "Typical bed covers for ethnic households.", 0, 200)
Thorn = Inventory("thorn", "thorns", "Junk", 0, "Ouch!", 0, 10)
CursedSeed = Inventory("a cursed seed", "cursed seeds", "Junk", 0, "Throw them into the dirt and sprout a giant stalk.", 0, 20)
DreadPetal = Inventory("a dread petal", "dread petals", "Junk", 0, "Probably useful for something.", 0, 30)
Rock = Inventory("a rock", "rocks", "Junk", 0, "Holds a lot of sentimental value.", 0, 5)
brimstone = Inventory("a piece of brimstone", "pieces of brimstone", "Junk", 0, "Still hot.", 0, 30)
obsidiancore = Inventory("an obsidian core", "obsidian cores", "Junk", 0, "The heart of a flame elemental.", 0, 50)
ruby = Inventory("a rough ruby", "rough rubies", "Junk", 0, "The sunken eyes of a flame elemental.", 0, 100)
fireessence = Inventory("a fire essence", "fire essences", "Junk", 0, "The soul of a flame elemental.", 0, 100)
enchanting_rune = Inventory("a phantasmal rune", "phantasmal runes", "Junk", 0, "The etched stone glimmers a rainbow spectrum of colors.", 0, 100)
phylactery = Inventory("a phylactery", "phylacteries", "Junk", 0, "A crystalline urn, etched with symbols of undeath.", 0, 0)


# Consumables
HPotion1 = Inventory("a Standard Health Potion", "Standard Health Potions", "Health Potion", 20, "Tastes like syrup. 20 HP.", 0, 20)
MPotion1 = Inventory("a Standard Mana Potion", "Standard Mana Potions", "Mana Potion", 20, "Tastes sour. 20 Mana.", 0, 20)
ManaBun = Inventory("a mana bun", "mana buns", "Meal", 30, "Warm and soft, filled with honey-like substance. 30 HP and Mana.", 0, 0)
Firebomb = Inventory("a firebomb", "firebombs", "Explosive", 20, "Labeled 'DANGER - SHORTFUSE Co. 20 Damage.'", 0, 20)
Bread = Inventory("a chunk of bread", "chunks of bread", "Food", 30, "Pretty stale. 30 HP.", 0, 5)
FrogLegs = Inventory("frog legs", "frog legs", "Food", 20, "Still twitching. 15 HP.", 0, 10)
CrackedFemur = Inventory("a cracked femur", "cracked femora", "Explosive", 30, "Break it on someone's skull.", 0, 30)
PaleAle = Inventory("a bottle of ale", "bottles of ale", "Drink", 25, "Fruity, crisp and copper in color. 25 Mana.", 0, 20)
Beer = Inventory("a bottle of beer", "bottles of beer", "Drink", 30, "Tastes like piss. 30 Mana.", 0, 10)
Wine = Inventory("a bottle of wine", "bottles of wine", "Drink", 10, "For the refined palate. 10 Mana.", 0, 50)
Cheeseroll = Inventory("a cheese roll", "cheese rolls", "Food", 20, "Goes great with wine. 20 HP.", 0, 10)
PickledRaptorLung = Inventory("a pickled raptor lung", "pickled raptor lungs", "Food", 30, "Somewhat sour and tangy. 30 HP.", 0, 30)
PickledElfEars = Inventory("a pickled elf's ear", "pickled elf's ears", "Food", 20, "It's just a plant, don't worry. 20 HP.", 0, 30)
BlackwaterFish = Inventory("a blackwater fish", "blackwater fishes", "Food", 30, "Greasy, tastes like shit. 30 HP.", 0, 30)
DreadAle = Inventory("a dread ale", "dread ales", "Drink", 30, "Don't read the ingredients. 30 Mana.", 0, 30)
Mudbeer = Inventory("a mud beer", "mud beers", "Drink", 20, "You can probably guess the secret ingredient. 20 Mana.", 0, 20)
DragonbreathGin = Inventory("a flask of Dragonbreath gin", "flasks of Dragonbreath gin", "Drink", 50, "Stings your throat horribly. 50 Mana.", 0, 60)
DwarvenStout = Inventory("a skin of Dwarven stout", "skins of Dwarven stout", "Drink", 50, "Get it? 30 Mana.", 0, 40)
StoneBourbon = Inventory("a jug of Stone bourbon", "jugs of Stone bourbon", "Drink", 60, "Has a very strong, lingering taste. 60 Mana.", 0, 50)
Rockbeer = Inventory("a Rock beer", "Rock beers", "Drink", 30, "The flavor of hops is distinguishable, but not overwhelming. 50 Mana.", 0, 20)
DesrahGin = Inventory("a flask of Desrah gin", "flasks of Desrah gin", "Drink", 80, "Ridiculously dry. 80 Mana.", 0, 70)
OnyxianBrew = Inventory("an Onyxian brew", "Onyxian brews", "Drink", 150, "The ultimate Dwarven brew. 150 Mana.", 0, 120)
FruitOfLife = Inventory("\033[1;32;40ma Fruit of Life\033[0m", "\033[1;32;40mFruits of Life\033[0m", "Meal", 99999,
                        "All costs go to tending to the Tree. Refills HP and Mana.", 0, 500)
ManaDrink = Inventory("a drink of pure mana", "drinks of pure mana", "Drink", 100, "Glimmers and sparkles with energy. 100 Mana.", 0, 50)
DrakonidRation = Inventory("a Drakonid ration", "Drakonid rations", "Meal", 50, "Completely bland and utilitarian. 50 HP and Mana.", 0, 50)
orbofdarkness = Inventory("an Orb of Darkness", "Orbs of Darkness", "Meal", 200, "Shimmers a tint of crimson red. 200 HP and Mana.", 0, 0)


# Scrolls and Books
Goosebumps = Inventory("\033[1;32;40mGoosebumps\033[0m", "\033[1;32;40mGoosebumps\033[0m", "Book", Fear, "A true best seller. Teaches: Fear", 0, 100)
RainCallersTome = Inventory("\033[1;32;40mRaincaller's Tome\033[0m", "\033[1;32;40mRaincaller's Tomes\033[0m", "Book", HealingRain,
                            "What? You think we just WAIT for it to rain?", 0, 150)
madmandesc = "The ink faded off the sun-bleached paper. You can only make out a few words about artifacts and otherwordly riches."
MadmanPaper = Inventory("a scribbled paper", "scribbled papers", "Readable", madmandesc, "A folded piece of paper with hastily scribbled writing.", 0, 1)
lostmissive = "Placeholder clue for a desert dungeon."
LostMissive = Inventory("a lost missive", "lost missives", "Readable", lostmissive, "Sealed and wrapped neatly.", 0, 10)
desertmap = "The canyon separates us from the filthy northerners. The ongoing war between the centaur and the minotaur should be enough to dissuade travelers.\n" \
            "The Swamp of Sorrow is littered with ships and undead crews from northerners who attempted to cut around the sea to attack us.\n" \
            "The windy desert makes the borders of the steppes nigh untraversable. Beware the skittering hellions east of here. Do not approach the ruins.\n" \
            "South of here is a jungle with those godless tribes. Avoid confrontation but do NOT allow them to get your corpse intact."
DesertMap = Inventory("a Kron desert map", "Kron desert maps", "Readable", desertmap, "Helpful notes for tourists.", 0, 100)
BFireball = Inventory("Tome: Fireball", "Tomes of Fireball", "Book", Fireball, "Teaches: Fireball", 0, 50)
BFrostBolt = Inventory("Tome: Frostbolt", "Tomes of Frostbolt", "Book", FrostBolt, "Teaches: Frostbolt", 0, 50)
BIceLance = Inventory("Tome: Ice Lance - Step I", "Tomes: Ice Lance - Step I", "Book", IceLance, "Teaches: Ice Lance", 0, 50)
BRelease = Inventory("Tome: Ice Lance - Step II", "Tomes: Ice Lance - Step II", "Book", Release, "Teaches: Release", 0, 50)
BConjure = Inventory("Tome: Basic Conjuration", "Tomes: Basic Conjuration", "Book", Conjure, "Teaches: Conjure Food", 0, 50)
BOwlForm = Inventory("Scripture: Owl Form", "Scriptures: Owl Form", "Book", OwlForm, "Teaches: Owl Form", 0, 100)
BStarfall = Inventory("Scripture: Starfall", "Scriptures: Starfall", "Book", Starfall, "Teaches: Starfall", 0, 50)
BRejuvenation = Inventory("Scripture: Rejuvenation", "Scriptures: Rejuvenation", "Book", Rejuvenation, "Teaches: Rejuvenation", 0, 50)
BGraspingRoots = Inventory("Scripture: Grasping Roots", "Scriptures: Grasping Roots", "Book", GraspingRoots, "Teaches: Grasping Roots", 0, 50)
BCharmBeast = Inventory("Scripture: Charm Beast", "Scriptures: Charm Beast", "Book", CharmBeast, "Teaches: Charm Beast", 0, 200)
ScrollOfSun = Inventory("Scroll: Sunfire", "Scrolls: Sunfire", "Scroll", Sunfire, "Teaches: Sunfire", 0, 80)
BCoronalBeam = Inventory("Scroll: Coronal Beam", "Scrolls: Coronal Beam", "Scroll", CoronalBeam, "Teaches: Coronal Beam", 0, 100)
BMinion = Inventory("Scroll: Summon Minion", "Scrolls: Summon Minion", "Scroll", Minion, "Teaches: Summon Minion", 0, 100)
BSmite = Inventory("Scroll: Smite", "Scrolls: Smite", "Scroll", Smite, "Teaches: Smite", 0, 80)
BSilence = Inventory("Scroll: Silence", "Scrolls: Silence", "Scroll", Silence, "Teaches: Silence", 0, 100)



# Weapons and Armor
# [+stamina, +attack, +wisdom, item effect]
IronDagger = Inventory("an iron dagger", "iron daggers", "Dagger", [0, 5, 0, 0], "Somewhat dull. +5 ATK.", 0, 20)
RustyScythe = Inventory("a rusty scythe", "rusty scythes", "Scythe", [0, 10, 0, 0], "Great range. Horrible everything else. +10 ATK.", 0, 40)
ScarabPlate = Inventory("a scarab plate", "scarab plates", "Head", [20, 0, 0, 0], "Exceptionally tough. Try wearing it. +20 STA", 0, 80)
SharpFang = Inventory("a sharp fang", "sharp fangs", "Dagger", [0, 10, 0, PoisonStrike], "The gland is still attached. +10 ATK.", 0, 60)
TreantStaff = Inventory("\033[1;32;40ma Treant staff\033[0m", "\033[1;32;40mTreant staves\033[0m", "Staff", [0, 5, 20, Root],
                        "The living branch of a treant commands the earth. +20 WIS.", 0, 80)
Stick = Inventory("a stick", "sticks", "Staff", [0, 10, 0, 0], "A cool stick I found. +10 ATK.", 0, 30)
CentaurAxe = Inventory("a Centaur Axe", "Centaur Axes", "Axe", [0, 25, 0, 0], "Standard issue. +25 ATK.", 0, 100)
LostShield = Inventory("a lost shield", "lost shields", "Offhand", [50, 0, 0, 0], "Second hand. +50 STA.", 0, 200)
DuneShield = Inventory("\033[1;32;40mShield of Dunes\033[0m", "\033[1;32;40mShields of Dunes\033[0m", "Offhand", [100, 0, 0, Sirocco],
                       "The carvings on it are amazing, yet corroded. +100 STA.", 0, 500)
KronSaber = Inventory("a Kron saber", "Kron sabers", "Sword", [0, 30, 0, 0], "These people really know how to carve their iron. +30 ATK.", 0, 180)
DesertAmulet = Inventory("a desert amulet", "desert amulets", "Neck", [0, 0, 20, WindWall], "Etched with runes that promise dominion over the wind. +20 WIS.", 0, 80)
PurpleRobe = Inventory("a purple robe", "purple robes", "Chest", [0, 0, 30, 0], "What a cute color. +30 WIS.", 0, 30)
GoldenRobe = Inventory("a golden robe", "golden robes", "Chest", [0, 0, 50, 0], "It's fake. +50 WIS.", 0, 50)
TrimmedRobe = Inventory("\033[1;32;40ma trimmed azure robe\033[0m", "\033[1;32;40mtrimmed azure robes\033[0m", "Chest", [0, 0, 100, 0], "It's glowing... +100 WIS.", 0, 100)
SilkPants = Inventory("a pair of silk pants", "pairs of silk pants", "Legs", [0, 0, 0, 0], "Comfy, but useless.", 0, 20)
SilkSlippers = Inventory("a pair of silk slippers", "pairs of silk slippers", "Feet", [0, 0, 0, 0], "Comfy, but useless.", 0, 20)
Bandana = Inventory("a red bandana", "red bandanas", "Head", [0, 0, 0, 0], "Makes you feel sneakier.", 0, 20)
Turban = Inventory("a silk turban", "silk turbans", "Head", [0, 0, 30, 0], "Big brain! +30 WIS.", 0, 30)
IronHelm = Inventory("an iron helmet", "iron helmets", "Head", [20, 0, 0, 0], "A casque for your cranium. +20 STA.", 0, 20)
IronPlate = Inventory("an iron chestplate", "iron chestplates", "Chest", [50, 0, 0, 0], "Now you can pretend to have abs. +50 STA.", 0, 50)
IronBoots = Inventory("a pair of iron boots", "pairs of iron boots", "Feet", [20, 0, 0, 0], "Cowboy boots? Bitch, disgusting. +20 STA.", 0, 20)
IronGreaves = Inventory("a pair of iron greaves", "pairs of iron greaves", "Legs", [30, 0, 0, 0], "Give him his cigar. +30 STA.", 0, 30)
Shortsword = Inventory("a shortsword", "shortswords", "Sword", [0, 10, 0, 0], "Also known as: the Manlet sword. +10 ATK.", 0, 40)
IronBuckler = Inventory("an iron buckler", "iron bucklers", "Offhand", [50, 0, 0, 0], "Smack it to scare people off. +50 STA.", 0, 50)
RobeOfTheDeeps = Inventory("\033[1;32;40mRobe of the Deeps\033[0m", "\033[1;32;40mRobes of the Deeps\033[0m", "Chest", [0, 0, 100, 0],
                           "Black, trimmed with silver. +100 WIS.", 0, 100)
IronsilkRobe = Inventory("\033[1;32;40mIronsilk Robe\033[0m", "\033[1;32;40mIronsilk Robes\033[0m", "Chest", [50, 0, 50, 0],
                         "Shiny. For casters who loathe being glass cannons. +50 STA, +50 WIS.", 0, 100)
AbyssalStaff = Inventory("\033[1;32;40mAbyssal Staff\033[0m", "\033[1;32;40mAbyssal Staves\033[0m", "Staff", [0, 10, 20, WhirlOfAekhal],
                         "The onyx-jeweled head is so black it absorbs light. +10 ATK, +20 WIS.", 0, 200)
Heartmender = Inventory("\033[1;32;40mHeartmender\033[0m", "\033[1;32;40mHeartmenders\033[0m", "Mace", [0, 20, 50, PrayerOfMending],
                        "Ivory, steel, engraved with golden runes. +20 ATK, +50 WIS.", 0, 200)
RubyCirclet = Inventory("a ruby circlet", "ruby circlets", "Head", [0, 0, 20, 0], "A beautiful crimson jewel is nested in the front. +20 WIS.", 0, 20)
SapphireCirclet = Inventory("a sapphire circlet", "sapphire circlets", "Head", [0, 0, 30, 0], "An ocean-blue jewel glimmers in the front. +30 WIS.", 0, 30)
SteelHammer = Inventory("a steel warhammer", "steel warhammers", "Mace", [0, 20, 0, 0], "A stout and blunt steel warhammer. +20 ATK.", 0, 80)
BarbedAxe = Inventory("a barbed axe", "barbed axes", "Axe", [0, 30, 0, 0], "Razor sharp to the touch. Don't touch. +30 ATK.", 0, 120)
ObsidiumScythe = Inventory("\033[1;32;40man Obsidium scythe\033[0m", "\033[1;32;40mObsidium scythes\033[0m", "Scythe", [0, 40, 0, 0],
                           "Blackish-purple metal, chipped from the bellows of the earth. +40 ATK.", 0, 160)
TheBlackCleaver = Inventory("\033[1;32;40mthe Black Cleaver\033[0m", "\033[1;32;40mBlack Cleavers\033[0m", "Axe", [50, 20, 0, 0],
                            "Somewhat boosts your vitality when held properly. +50 STA, +20 ATK.", 0, 130)
CasqueOfTheMountain = Inventory("a horned helm", "horned helms", "Head", [50, 0, 0, Charge], "Carved to resemble horns of rams the Dwarves so idolize. +50 STA.", 0, 100)
SteamPoweredFist = Inventory("a steam-powered fist", "steam-powered fists", "Hand", [20, 0, 0, FistBump], "Brother fist! +20 STA.", 0, 80)
GreenTintedGoggles = Inventory("\033[1;32;40mNightmare vision goggles\033[0m", "\033[1;32;40mNightmare vision goggles\033[0m", "Head", [20, 0, 0, 0],
                               "Everything looks exactly the same. +20 STA.", 0, 40)
TommyGun = Inventory("a Tommy gun", "Tommy guns", "Gun", [0, 30, 0, 0], "RAT-TAT-TAT-TAT! +30 ATK.", 0, 120)
SteelBellyplate = Inventory("a steel bellyplate", "steel bellyplates", "Chest", [50, 0, 0, 0], "Traditional Ogre craftsmanship. +50 STA.", 0, 50)
SteelHeadcover = Inventory("a steel headcover", "steel headcover", "Head", [30, 0, 0, 0], "It's just a cooking pot. +30 STA.", 0, 30)
OgreGlove = Inventory("Ogre gloves", "Ogre gloves", "Hands", [30, 0, 0, 0], "RIDICULOUSLY heavy. +30 STA.", 0, 30)
WildSpear = Inventory("\033[1;32;40ma Wild Spear\033[0m", "\033[1;32;40mWild Spears\033[0m", "Spear", [0, 20, 30, 0],
                      "Adorned with feathers and shrunken skulls at the neck. +20 ATK, +30 WIS", 0, 110)
ElvenGlaive = Inventory("an Elven glaive", "Elven glaives", "Scythe", [0, 20, 0, 0], "Curved in the shape of a crescent moon. +20 ATK.", 0, 80)
FallenHorn = Inventory("a shed horn", "shed horns", "Offhand", [0, 0, 50, 0], "When male Stagkin mature, they shed their small \"milk\" horns. +50 WIS.", 0, 80)
ElvenMail = Inventory("Elven chainmail", "Elven chainmail", "Chest", [0, 60, 20, 0], "Sturdy mail with some light magical properties. +60 STA, +20 WIS.", 0, 100)
ElvenHammer = Inventory("an Elven hammer", "Elven hammers", "Mace", [20, 0, 20, 0], "Zirconic, crystalline chipped tip. +20 ATK, +20 WIS.", 0, 100)
ElvenBlade = Inventory("an Elven blade", "Elven blades", "Sword", [30, 0, 20, 0], "Chipped crystalline edge out of a wing-shaped hilt. +30 ATK, +20 WIS.", 0, 150)
SunAmulet = Inventory("an Amulet of the Sun", "Amulets of the Sun", "Neck", [0, 0, 50, 0], "Offers magical constitution and faith of the Sunborn. +50 WIS.", 0, 80)
magmacrown = Inventory("a magma crown", "magma crowns", "Head", [20, 0, 50, 0], "Warm to the touch, harmless to its wearer. +20 STA, +50 WIS.", 0, 80)
ScalemailPlate = Inventory("a Scalemail plate", "Scalemail plates", "Chest", [0, 100, 0, 0], "The scales are retractable. +100 STA.", 0, 100)
DragonAxe = Inventory("a Dragon Ax", "Dragon Axes", "Axe", [50, 0, 0, 0], "Adorned with swirling golden wyrms and red scratches. +50 ATK.", 0, 200)
spectral_cleaver = Inventory("\033[0;36;40mSpectral Cleaver\033[0m", "\033[0;36;40mSpectral Cleavers\033[0m", "Axe", [50, 0, 0, 0],
                             "The tip is stained with ectoplasm. +50 ATK.", 0, 200)
skullfrost_shield = Inventory("\033[0;36;40mSkullfrost Kite Shield\033[0m", "\033[0;36;40mSkullfrost Kite Shields\033[0m", "Offhand", [0, 200, 0, Icewall],
                              "A large crystalline skull glows blue in the center. +200 STA. ", 0, 300)
the_thornheart = Inventory("\033[0;36;40mthe Thornheart\033[0m", "\033[0;36;40mThornhearts\033[0m", "Neck", [0, 20, 100, Thorns],
                           "A rose inside a ruby, adorned with jeweled thorns swirling around it. +20 STA, +100 WIS.", 0, 200)
shadowslippers = Inventory("\033[0;36;40ma pair of shadowslippers\033[0m", "\033[0;36;40mpairs of shadowslippers\033[0m", "Feet", [0, 20, 20, Shadowstep],
                           "They phase quickly into the ether when tapped. +20 STA, +20 WIS.", 0, 100)
PhantasmalStaff = Inventory("\033[0;36;40ma Phantasmal Staff\033[0m", "\033[0;36;40mPhantasmal Staves\033[0m", "Staff", [0, 0, 200, PrismaticAnimation],
                            "The staff's color changes when you tilt it. +200 WIS. ", 0, 1000)
KamarFistOfTynnin = Inventory("\033[0;35;40mKamar, Wrath of Dunia\033[0m", "\033[0;35;40mKamar, Wrath of Dunia\033[0m", "Sword", [0, 0, 200, 0],
                            "\"...With her dying breath, the shattered earth cursed men with looming vengeance.\" -Oggomas, Archivist of Eons", 0, 1000)
totem_of_fire = Inventory("a Totem of Fire", "Totems of Fire", "Offhand", [0, 0, 0, SummonFireTotem], "A log carved and painted with symbols of fire.", 0, 0)
totem_of_water = Inventory("a Totem of Water", "Totems of Water", "Offhand", [0, 0, 0, SummonWaterTotem], "A log carved and painted with symbols of water.", 0, 0)
totem_of_air = Inventory("a Totem of Air", "Totems of Air", "Offhand", [0, 0, 0, SummonAirTotem], "A log carved and painted with symbols of air.", 0, 0)
totem_of_earth = Inventory("a Totem of Earth", "Totems of Earth", "Offhand", [100, 0, 0, 0], "A log carved and painted with symbols of earth. +100 STA.", 0, 0)


set = Set(Fists, Nothing, Nothing, Nothing, Nothing, Nothing, Nothing, Nothing, Nothing, Nothing)

nothing_drops = [Nothing, Nothing, Nothing, Nothing, Nothing,
                 Nothing, Nothing, Nothing, Nothing, Nothing]
goblin_drops = [GoblinSkin, GoblinSkin, GoblinSkin, GoblinSkin, IronDagger,
                Bread, Nothing, Nothing, Nothing, Nothing]
woodimp_drops = [TornImpWing, TornImpWing, TornImpWing, TornImpWing, TornImpWing,
                 Nothing, Nothing, Nothing, Nothing, Nothing]
gnoll_drops = [GnollFang, GnollFang, GnollFang, GnollFang, IronDagger,
               IronDagger, Bread, Nothing, Nothing, Nothing]
bandit_drops = [IronDagger, IronDagger, IronDagger, IronDagger, Bread,
                PatchOfCloth, PatchOfCloth, PatchOfCloth, PatchOfCloth, PatchOfCloth]
critter_drops = [CritterFur, CritterFur, CritterFur, CritterFur, CritterFur,
                 CritterFur, CritterFur, CritterFur, Nothing, Nothing]
frog_drops = [FrogLegs, FrogLegs, FrogLegs, FrogLegs, FrogLegs,
              Nothing, Nothing, Nothing, Nothing, Nothing]
skeleton_drops = [BoneChips, BoneChips, BoneChips, BoneChips, Skull,
                  CrackedFemur, Nothing, Nothing, Nothing, Skull]
scarab_drops = [ScarabCarapace, ScarabCarapace, ScarabCarapace, ScarabCarapace, ScarabCarapace,
                ScarabPlate, Nothing, Nothing, Nothing, Nothing]
snake_drops = [SnakeFang, SnakeFang, SnakeFang, SnakeFang, SnakeFang,
               SharpFang, Nothing, Nothing, Nothing, Nothing]
treant_drops = [Stick, Stick, Stick, Stick, Nothing,
                TreantStaff, Nothing, Nothing, Nothing, Nothing]
crocodile_drops = [Scale, Scale, Scale, Scale, Nothing,
                   CrocodileFang, CrocodileFang, CrocodileFang, CrocodileFang, Nothing]
slime_drops = [Slimeball, Slimeball, Slimeball, Slimeball, Slimeball,
               Slimeball, IronDagger, BoneChips, Nothing, Nothing]
minotaur_drops = [CritterFur, CritterFur, CritterFur, CritterFur, Horn,
                  Horn, Horn, BrokenHoof, BrokenHoof, BrokenHoof, Nothing]
ogre_drops = [Horn, Horn, Horn, OgreEye, OgreEye,
              OgreEye, Nothing, Nothing, Nothing, Nothing]
bird_drops = [Beak, Beak, Beak, Beak, Beak, Nothing,
              Feather, Feather, Feather, Feather, Nothing]
centaur_drops = [BrokenHoof, BrokenHoof, BrokenHoof, BrokenHoof, BrokenHoof,
                 CentaurAxe, CentaurAxe, Nothing, Nothing, Nothing]
poisonreptile_drops = [Scale, Scale, Scale, SharpFang, SharpFang,
                       CrocodileFang, CrocodileFang, CrocodileFang, Nothing, Nothing]
spider_drops = [FuzzyLeg, FuzzyLeg, FuzzyLeg, SharpFang, Spinneret,
                Spinneret, Spinneret, SharpFang, SharpFang, Nothing]
canine_drops = [Fang, Fang, Fang, Fang, Fang,
                RippedTendon, RippedTendon, CritterFur, CritterFur, Nothing]
worm_drops = [Fang, Fang, Fang, Slimeball, Slimeball, LostShield,
              Skull, Skull, RippedTendon, Nothing]
madman_drop = [IronDagger, Nothing, Nothing, MadmanPaper, Bread,
               PatchOfCloth, PatchOfCloth, PatchOfCloth, PatchOfCloth, PatchOfCloth]
bigworm_drops = [GiantFang, GiantFang, GiantFang, Slimeball, Slimeball,
                 DuneShield, Skull, Skull, RippedTendon, Nothing]
kron_drops = [PatchOfCloth, PatchOfCloth, PatchOfCloth, DesertMap, DesertMap,
              LostMissive, DesertMap, DesertAmulet, PatchOfCloth, Nothing]
kronblade_drops = [PatchOfCloth, PatchOfCloth, PatchOfCloth, PatchOfCloth, Nothing,
                   KronSaber, KronSaber, DesertAmulet, PatchOfCloth, Nothing]
khanfus_drops = [TwitchingLeg, TwitchingLeg, TwitchingLeg, TwitchingLeg, ScarabPlate,
                 ScarabPlate, ScarabPlate, ScarabPlate, Nothing, Nothing]
pig_drops = [Tusk, Tusk, Tusk, Tusk, IntactTusk,
             BrokenHoof, BrokenHoof, BrokenHoof, BrokenHoof, Nothing]
tiger_drops = [Fang, Fang, Fang, Fang, Fang,
               RippedTendon, RippedTendon, TigerFur, TigerFur, Nothing]
flower_drops = [Thorn, Thorn, Thorn, CursedSeed, CursedSeed,
                DreadPetal, DreadPetal, DreadPetal, Nothing, Nothing]
gorilla_drops = [Fang, Fang, Fang, Fang, Fang,
                 RippedTendon, RippedTendon, TigerFur, TigerFur, Nothing]
fire_drops = [brimstone, brimstone, brimstone, obsidiancore, obsidiancore,
              obsidiancore, ruby, magmacrown, fireessence, fireessence]
pudgebulk_drops = [spectral_cleaver, spectral_cleaver, spectral_cleaver, spectral_cleaver,
                   Nothing, Nothing, Nothing, Nothing, Nothing]
oathrend_drops = [skullfrost_shield, skullfrost_shield, skullfrost_shield, Nothing, Nothing,
                  Nothing, Nothing, Nothing, Nothing, Nothing]
thornlady_drops = [thorn_key, thorn_key, thorn_key, thorn_key, thorn_key,
                   thorn_key, thorn_key, thorn_key, thorn_key, thorn_key]
ranissius_drops = [the_thornheart, the_thornheart, the_thornheart, Nothing, Nothing,
                   shadowslippers, shadowslippers, shadowslippers, Nothing, Nothing]
phantasm_drops = [enchanting_rune, enchanting_rune, enchanting_rune, enchanting_rune, enchanting_rune,
                  enchanting_rune, enchanting_rune, enchanting_rune, enchanting_rune, enchanting_rune]

inventory = [Gold, GoblinSkin, TornImpWing, GnollFang, CritterFur, PatchOfCloth, BoneChips, ScarabCarapace, Slimeball, Scale, CrocodileFang, Horn, BrokenHoof, OgreEye,
             Beak, Feather, FuzzyLeg, Spinneret, Fang, RippedTendon, Skull, GiantFang, TwitchingLeg, TigerFur, Thorn, CursedSeed, DreadPetal, Rock, brimstone, obsidiancore,
             ruby, fireessence, thorn_key, enchanting_rune, SnakeFang, phylactery,
             HPotion1, MPotion1, Firebomb, ManaBun, Bread, FrogLegs, CrackedFemur, PaleAle, Beer, Wine, Cheeseroll, DreadAle, Mudbeer, DragonbreathGin, PickledRaptorLung,
             PickledElfEars, BlackwaterFish, DwarvenStout, StoneBourbon, Rockbeer, DesrahGin, OnyxianBrew, FruitOfLife, ManaDrink, DrakonidRation, orbofdarkness,
             Goosebumps, RainCallersTome, ScrollOfSun, MadmanPaper, LostMissive, DesertMap, BFireball, BFrostBolt, BIceLance, BRelease, BConjure,BStarfall, BRejuvenation,
             BGraspingRoots, BCharmBeast, BCoronalBeam, BMinion, BConjure, BSmite, BSilence,
             IronDagger, RustyScythe, ScarabPlate, SharpFang, TreantStaff, Stick, CentaurAxe, LostShield, DuneShield, KronSaber, DesertAmulet, PurpleRobe, GoldenRobe,
             TrimmedRobe, SilkPants, SilkSlippers, Bandana, Turban, IronHelm, IronPlate, IronBoots, IronGreaves, Shortsword, IronBuckler, RobeOfTheDeeps, IronsilkRobe,
             AbyssalStaff, Heartmender, RubyCirclet, SapphireCirclet, SteelHammer, BarbedAxe, ObsidiumScythe, TheBlackCleaver, CasqueOfTheMountain, SteamPoweredFist,
             GreenTintedGoggles, TommyGun, SteelBellyplate, SteelHeadcover, OgreGlove, WildSpear, ElvenGlaive, FallenHorn, ElvenMail, ElvenHammer, ElvenBlade, SunAmulet,
             magmacrown, ScalemailPlate, DragonAxe, spectral_cleaver, skullfrost_shield, the_thornheart, shadowslippers, PhantasmalStaff, KamarFistOfTynnin, totem_of_fire,
             totem_of_earth, totem_of_water, totem_of_air]

farmer.items_sold = [Bread, RustyScythe, RainCallersTome]
Librarian.items_sold = [BFireball, BFrostBolt, BIceLance, BRelease, BConjure]
Tailor.items_sold = [PurpleRobe, GoldenRobe, TrimmedRobe, SilkPants, SilkSlippers, Bandana, Turban]
Blacksmith.items_sold = [IronHelm, IronPlate, IronBoots, IronGreaves, Shortsword, IronBuckler]
Innkeeper.items_sold = [PaleAle, Beer, Wine, Cheeseroll]
WeaverNolag.items_sold = [RobeOfTheDeeps, IronsilkRobe, AbyssalStaff, Heartmender, RubyCirclet, SapphireCirclet]
SmithHajjar.items_sold = [SteelHammer, BarbedAxe, ObsidiumScythe, TheBlackCleaver, CasqueOfTheMountain]
AssistantLarr.items_sold = [Firebomb, SteamPoweredFist, GreenTintedGoggles, TommyGun]
DwarfBartender.items_sold = [DwarvenStout, StoneBourbon, Rockbeer, DesrahGin, OnyxianBrew]
AssistantMoragg.items_sold = [SteelBellyplate, SteelHeadcover, OgreGlove, WildSpear, Rock]
FishermanTakk.items_sold = [PickledRaptorLung, PickledElfEars, BlackwaterFish, FrogLegs]
BartenderSmog.items_sold = [DreadAle, Mudbeer, DragonbreathGin]
ElvenHomekeeper.items_sold = [ElvenGlaive, FallenHorn, FruitOfLife]
ElvenLibrarian.items_sold = [BStarfall, BRejuvenation, BGraspingRoots, BCharmBeast]
ElvenSmith.items_sold = [ElvenMail, ElvenHammer, ElvenBlade, SunAmulet, GoldenRobe]
SElvenLibrarian.items_sold = [ScrollOfSun, BCoronalBeam, BMinion, BConjure, BSmite, BSilence]
ElvenBartender.items_sold = [ManaDrink]
DrakonidProvisioner.items_sold = [ScalemailPlate, DrakonidRation, DragonAxe]
Salbartender.items_sold = [DreadAle, DragonbreathGin]

Conjure.damage = ManaBun
Minion.damage = arcane_ele
SummonSkeleton.damage = summoned_skeleton
SummonFireTotem.damage = firetotem
SummonWaterTotem.damage = watertotem
SummonAirTotem.damage = airtotem
TALENTWolf.damage = shamwlf
TALENTWraithGuard.damage = pwraithguard
TALENTPhylactery.damage = phylactery
TALENTOrb.damage = orbofdarkness
TALENTCompanions.damage = legion
TALENTBarblur.damage = monkclone











goblin = Enemy('a goblin', 50, 5, 2, "A goblin from the uncharted caverns beneath Iklisztefon.", [], goblin_drops, "Humanoid", [], None)
woodimp = Enemy('a captured wood imp', 30, 5, 2,"A wriggling Fraba imp, as tall as three apples. Very slippery.", [], woodimp_drops, "Humanoid", [], None)
salamander = Enemy('a lost Salamander scout', 80, 20, 1, "Far away from its warm and dry homeland.", [], nothing_drops, "Tynnin", [FlameLick], None)
gnoll = Enemy('a scrawny gnoll', 60, 5, 1, "If it was stronger it could make a living as a highway bandit.", [], gnoll_drops, "Humanoid", [], None)
wildboar = Enemy('a wild boar', 50, 10, 1, "Fodder for level 1 players ever since RPGs were a thing.", [], critter_drops, "Beast", [], tamed_boar)
wildbear = Enemy('a bear', 80, 15, 1, "Quick! Play dead!", [], critter_drops, "Beast", [], tamed_bear)
highwayman = Enemy('a Human highwayman', 70, 10, 2, "He's staring at your belongings.", [], bandit_drops, "Humanoid", [], None)
swolefrog = Enemy('a swole frog', 20, 20, 2, "Chad-ilay... Chad-ilay...", [], frog_drops, "Beast", [], None)
hugeskunk = Enemy('an enormous skunk', 10, 10, 1, "Always face it from the front.", [], critter_drops, "Beast", [], None)
humanspy = Enemy('a human spy', 70, 10, 2, 'Obviously just visiting a relative.', [], bandit_drops, "Humanoid", [], None)
vengefulghoul = Enemy('a vengeful ghoul', 50, 10, 1, "Holding a grudge for that long is impressive.", [], nothing_drops, "Undead", [Fear], None)
skeletalservant = Enemy('a skeltal servant', 60, 10, 1, "When you tell a dedicated waiter to wait too long", [], skeleton_drops, "Undead", [Lifetap], None)
blackscarab = Enemy("a black scarab", 30, 5, 2, "It's shiny.", [], scarab_drops, "Beast", [], None)
viscioussnake = Enemy("a viscious snake", 20, 10, 2, "Deceptively painful bite.", [], snake_drops, "Beast", [PoisonStrike], None)
howlingwolf = Enemy("a howling wolf", 50, 10, 2, "Five, six, seven 'o nine.", [], canine_drops, "Beast", [], tamed_wolf)
angrytreant = Enemy("an angry treant", 100, 10, 1, "Watch out for splinters.", [], treant_drops, "Elemental", [Root], None)
wetlandcrocodile = Enemy("a wetland crocodile", 70, 15, 2, "Turns very slowly.", [], crocodile_drops, "Beast", [], None)
sludge = Enemy("a giant slime", 50, 10, 2, "Accidentally set the world to superflat.", [], slime_drops, "Demon", [], None)
undeadsailor = Enemy("an undead sailor",  60, 10, 2, "... moon.", [], skeleton_drops, "Undead", [], None)


lostreptile = Enemy("a lost Reptilian", 60, 5, 1, "Red canyon long way from Tynnin.", [], crocodile_drops, "Undead", [], None)
bloodhideraptor = Enemy("a woe raptor", 40, 10, 1, "Kept as tamed pets by the Minotaurs.", [], crocodile_drops, "Beast", [], None)
lesserminotaur = Enemy("a less minotaur", 80, 5, 2, "Very angry.", [], minotaur_drops, "Minotaur", [], None)
loneogre = Enemy("a lone ogre", 80, 5, 2, "D'oh!", [], ogre_drops, "Ogre", [], None)
starvingvulture = Enemy("a starving vulture", 50, 10, 1, "Sharp fang!", [], bird_drops, "Beast", [], None)
cacklinghyena = Enemy("a cackling hyena", 70, 15, 2, "What's so funny?", [], canine_drops, "Beast", [], None)
centaurscout = Enemy("a centaur scout", 50, 5, 2, "Can run massive distances while half asleep.", [], centaur_drops, "Centaur", [], None)
centaurwarrunner = Enemy("a centaur war runner", 70, 15, 2, "Don't stand behind it.", [], centaur_drops, "Centaur", [], None)
bogreptile = Enemy("a bog reptile", 60, 10, 2, "Creeping through the swamp.", [], poisonreptile_drops, "Beast", [], None)
massivespider = Enemy("a massive tarantula", 50, 10, 1, "All it does is molt and threat pose.", [], spider_drops, "Beast", [PoisonStrike], None)
sandwyrm = Enemy("a sand wyrm", 80, 15, 1, "Shifts through the sand.", [], worm_drops, "Beast", [], None)
lion = Enemy("a desert lion", 80, 20, 1, "The king of the ...desert?", [], canine_drops, "Beast", [], None)
madman = Enemy("a madman", 30, 10, 2, "Stood in the sun for too long.", [], madman_drop, "Humanoid", [], None)
cisternasp = Enemy("a cistern asp", 20, 10, 2, "Slinking out of underground water reserves.", [], snake_drops, "Beast", [], None)
skitteringhellion = Enemy("a skittering hellion", 90, 20, 1, "Hope you brought insecticide.", [], khanfus_drops, "Khanfus", [], None)
grandwyrm = Enemy("a grand wyrm", 150, 25, 2, "Massive.", [], bigworm_drops, "Beast", [], None)
kronscout = Enemy("a Kron scout", 70, 10, 2, "Almost entirely covered in indigo cloth.", [], kron_drops, "Kron", [Sirocco], None)
kronreaver = Enemy("a Kron reaver", 100, 20, 1, "Wields as blade taller than he is.", [], kronblade_drops, "Kron", [], None)
cragboar = Enemy("a crag boar", 30, 10, 1, "Its tusks are cracked and corroded.", [], pig_drops, "Beast", [], None)
dreadlurker = Enemy("a dreadlurker crocodile", 100, 20, 1, "Laying in a cut...", [], crocodile_drops, "Beast", [], None)
shadowtiger = Enemy("a shadow tiger", 110, 30, 2, "Push him out the tree, he falls right on his nuts.", [], tiger_drops, "Beast", [], None)
enormousboa = Enemy("a boa constrictor", 90, 20, 1, "Hit him with a coconut, stab him in his gut.", [], snake_drops, "Beast", [], None)
thornedstrangler = Enemy("a thorned strangler", 80, 20, 1, "Give him some elbow room!", [], flower_drops, "Elemental", [PoisonStrike], None)
skullgringorilla = Enemy("a skullgrin gorilla", 150, 20, 1, "Swingin on a vine! Sucking on a piece of swine!", [], gorilla_drops, "Beast", [], None)


spitecoil_cobra = Enemy("a Spitecoil cobra", 50, 20, 1, "Sleak, shiny black, wants you to die.", [], snake_drops, "Beast", [], None)
bull_revenant = Enemy("a desert revenant", 70, 20, 1, "Reanimated bones of dead desert beasts.", [], skeleton_drops, "Undead", [], None)
fleeing_slave = Enemy("a fleeing slave", 40, 10, 1, "Panicking coward.", [], bandit_drops, "Humanoid", [], None)
magma_spider = Enemy("a magma spider", 80, 30, 1, "Fuzzy in red, with glowing lava legs.", [], spider_drops, "Beast", [], None)
ashlander_scout = Enemy("an ashlander scout", 70, 20, 1, "Completely grey skinned, with blackened eyes and scarce hair.", [], bandit_drops, "Humanoid", [], None)
ashlander_warrior = Enemy("an ashlander warrior", 90, 30, 1, "Considerably meaner than the others.", [], kron_drops, "Humanoid", [], None)
lava_elemental = Enemy("a lava elemental", 100, 30, 1, "A humanoid blob of spewing lava, visibly angry.", [], fire_drops, "Elemental", [], None)


spectral_butler = Enemy("a spectral butler", 50, 10, 1, "The floating suit seems very angry.", [], nothing_drops, "Undead", [], None)
pudgebulk = Enemy("Pudgebulk", 200, 20, 1, "Fat beyond belief, with the head of a pig. Wields a nasty cleaver.", [], pudgebulk_drops, "Undead", [], None)
spectral_cook = Enemy("a spectral cook", 40, 20, 1, "The flying apron doesn't seem too pleased.", [], nothing_drops, "Undead", [], None)
knight_oathrend = Enemy("Knight Oathrend", 200, 20, 1, "A flying set of armor and a big shield.", [], oathrend_drops, "Undead", [], None)
lady_thornhaart = Enemy("Lady Thornhaart", 250, 15, 1, "New Smash character: Lonely Wife", [], thornlady_drops, "Undead", [], None)
ranissius_thornhaart = Enemy("Ranissius Thornhaart", 200, 20, 1, "\"The Crimson Weaver promised us we'd be safe!!\"", [], ranissius_drops, "Undead", [], None)
flesh_golem = Enemy("a shifting phantasm", 400, 20, 1, "The formless bubble of light that shifts in and out of existence.", [], phantasm_drops, "Undead", [], None)


plains_of_strife.enemy_table = [goblin, gnoll, humanspy, salamander]
reothian_glades.enemy_table = [woodimp, swolefrog, hugeskunk, gnoll, humanspy]
the_whitechapel.enemy_table = [vengefulghoul]
estate_thornhaart.enemy_table = [vengefulghoul, skeletalservant, blackscarab]
the_blackwood.enemy_table = [woodimp, viscioussnake, angrytreant, howlingwolf, angrytreant]
wetlands.enemy_table = [wetlandcrocodile, undeadsailor, sludge]

canyon_of_woe.enemy_table = [lostreptile, bloodhideraptor, lesserminotaur, loneogre]
swamp_of_sorrow.enemy_table = [sludge, bogreptile, swolefrog, viscioussnake, massivespider]
wilting_steppes.enemy_table = [starvingvulture, cacklinghyena, lesserminotaur, centaurscout, centaurwarrunner]
windy_desert.enemy_table = [sandwyrm, lion, madman, cisternasp]
desra.enemy_table = [skitteringhellion, grandwyrm, kronscout, madman, kronreaver, # wyrm is 1/3 as likely to spawn
                     skitteringhellion, kronscout, madman, kronreaver,
                     skitteringhellion, kronscout, madman, kronreaver]
redrock.enemy_table = [salamander, cragboar, lostreptile, bloodhideraptor, loneogre]
emerald_jungle.enemy_table = [dreadlurker, shadowtiger, enormousboa, thornedstrangler, skullgringorilla]

dread_wastes.enemy_table = [spitecoil_cobra, madman, bull_revenant, massivespider]
vulken.enemy_table = [fleeing_slave, magma_spider, ashlander_scout]
ashlands.enemy_table = [ashlander_warrior, magma_spider, lava_elemental]

thornhaart_floor1.enemy_table = [spectral_butler]
thornhaart_kitchen.enemy_table = [pudgebulk, spectral_cook]
thornhaart_hallway.enemy_table = [vengefulghoul]
thornhaart_guestroom.enemy_table = [knight_oathrend]
thornhaart_floor2.enemy_table = [vengefulghoul]
thornhaart_chamber.enemy_table = [lady_thornhaart]
thornhaart_basement.enemy_table = [ranissius_thornhaart, flesh_golem]










bring_linen = Quest("Fetch Some Furs", "Collect", CritterFur, 3, 0, 100, 500, None, "I've been getting into weaving lately, and I was curious how critter fur could fit into"
                                                                                    " the equation. Could you fetch me 3 pieces of critter fur from the nearby plains?",
                                                                                    "Have you gotten those furs yet?", "Thank you!", None)
bring_linen.followup = bring_linen
OldManMarcus.quest = bring_linen
boots = Quest('She Put "Cheater" On The Warboots!', "Collect", IronBoots, 1, 0, 100, 1000, None, "This HAS to stop. This is NEVER gonna end. \nLook what she did to my favorite "
                                                                                     "boots! She cut my favorite boots! Not that warboots! Not the WARBOOTS!! She "
                                                                                     'did "Curse You, Swine" on the warboots!!\n'
                                                                                     "She put poisoned worms in a napkin!? Harpies are devious!! I'm gonna need a "
                                                                                     "new pair...", 'She put "CHEATER" on the warboots...', "Thank you!", [])
OfficerErathos.quest = boots
enchanter3 = Quest("Phantasmal Staff: The Jewel", "Collect", enchanting_rune, 1, 0, 0, 5000, PhantasmalStaff, "I'll need a rune powerful enough "
                                                                                                  "to act as the jewel head and focus of the staff. This might be a bit too "
                                                                                                  "much to ask, but a decent one I know of has been stolen from the college's "
                                                                                                  "laboratorium. I hear whoever owns the Estate of Thornhaart is using it to "
                                                                                                  "create phantasmal servants for their dilapidated home. Go, and good luck.",
                                                                                                  "To reach the Estate of Thornhaart, you'll have to go out of the kingdom and "
                                                                                                  "into the Outskirts, and from there, cross through the Whitechapel.",
                                                                                                  "You've done an amazing job. You can keep the staff. You need it more."
                                                                                                  , [])
enchanter2 = Quest("Phantasmal Staff: The Neck", "Collect", PatchOfCloth, 2, 0, 0, 1000, None, "The cloth that the bandits out in the plains of strife wear has "
                                                                                              "some anti-magic properties that when amplified will keep the staff's wielder "
                                                                                              "safe from any magical recoil or feedback. Bring me two pieces of it to fasten.",
                                                                                              "Don't get yourself killed out there.",
                                                                                              "Amzing job. Now, for the final ingredient.", enchanter3)
enchanter1 = Quest("Phantasmal Staff: The Base", "Collect", TreantStaff, 1, 0, 0, 1000, None, "I've been eyeing this library for weeks, waiting for the right person to come "
                                                                                            "along and help me craft an amazing staff I wrote about. If you're wiling to help "
                                                                                            "me, you can start with the base. The branches of the Treants in the Blackwood "
                                                                                            "make great staves thanks to their potent magical energies.",
                                                                                            "Beware the Blackwood and its denizens.",
                                                                                            "Good. What I need, now, is some sturdy cloth to act as the damper between the neck "
                                                                                            "and the head.", enchanter2)
EnchanterAurilius.quest = enchanter1
