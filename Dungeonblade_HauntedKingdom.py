"""
Dungeonblade - Haunted Kingdom

Fight through a large dungeon against many beasts that will test your
strength.

Your stamina depletes as you attack enemies and run through the dungeon.
You must find water and medical kits throughout the dungeon. Don't have enough
stamina? You'll be less effective in a fight. Don't have enough health and stamina?
You'll not survive the dungeon.

You must aquire gold coins that grant you strength, while
also allowing you to defeat the necromancer and escape the dungeon.

Dungeonblade - Haunted Kingdom is free software: you can redistribute it and/or modify 
it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version.

Dungeonblade - Haunted Kingdom is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this program.
If not, see https://www.gnu.org/licenses/.
"""

## add random.
import random

## increase recursion limit to avoid recusion errors (https://stackoverflow.com/questions/8177073/python-maximum-recursion-depth-exceeded)
import sys
sys.setrecursionlimit(10000000)

## game info

"""
On easy, you don't encounter 2 enemies at once that much.
With this var, you can encounter them more. Only used for play testing.
"""
test = False

# the game title
gametitle = "Dungeonblade - Haunted Kingdom"
# the game version
gameversion = "v1.0" + (" (Playtest Mode)" if test == True else "")
# the game codename
gamecodename = "StarDancer"

"""
set our game state.

-4: start the game
-3: difficulty select
-2: name change
-1: story
0: exploring
1: enemy encounter
2: combat
"""

gamestate = -4

# blank objects.
item_nullweapon = {
    'name': "null weapon",
    'desc': '',
    'healthtouse': 0,
    'staminatouse': 0,
    "rarity": 0,
    'isgold': False,
    'istrap': False}
npc_null =  {
    'name': 'null npc',
    'weapon': item_nullweapon,
    "health": 0,
    "maxhealth": 0,
    "rarity": 0}
room_null = {
    'name': 'null room',
    'desc': "",
    'rarity': 0}

# since everything is unintialized, initialize any required items as null.
itempool = []
npc_boss = npc_null
room_finalboss = room_null
item_sword = item_nullweapon
item_shield = item_nullweapon
enemypool = []
locationpool = []

#current enemy
currEnemy = npc_null
# are we attacking?
attacking = False
# are we dodging?
dodging = False
# are we blocking?
blocking = False

## player values

# the player name
playerName = "Player"
# maximum health
maxPlayerHealth = 100
# Maximum health after we get coins.
maxPlayerHealthAfterCoins  = 200
# maximum stamina
maxPlayerStamina = 100
# the health
playerHealth = maxPlayerHealth
# the stamina
playerStamina = maxPlayerStamina
# number of gold coins we have
playerGold = 0
# do we have the gold coins?
doesPlayerHaveGoldCoinPowers = False
# minimum name length
minNameLength = 2
# the location of the player in the dungeon.
playerLocation = [0,0]

## gold coins

# how many golden coins a coin should give to the player.
minGoldCoinsToGive = 1
# how many coins we need to win the game.
maxGoldCoinsToWin = 3
# how many coins we need.
goldCoinsNeeded = maxGoldCoinsToWin
# how much the coins will increase our damage when we get all of them.
goldCoinStrengthMultiplier = 2

## movement vars

# if we have <= 50 stamina, multiply the damage by this. 
lowStaminaDamageReductionMultiplier = 0.7
# if we have 0 stamina, multiply the damage by this.
emptyStaminaDamageReductionMultiplier = 0.4
# move direction
direction = 'forward'
#the game difficulty
difficulty = 'normal'
# how many steps we take when running forwards.
runYSteps = 14
# how many steps we take when running sideways (random).
runXStepsMin = 1
runXStepsMax = 5
runXmin = -5
runXmax = 5
maxXsteps = 5
# the amount of steps to discover our first discovery.
minStepsToDiscover = 5
# the amount of stamina to reduce when walking
staminaToReduceWhileWalking = 1.7
# the amount of stamina to reduce when running
staminaToReduceWhileRunning = 2
# the minimum stamina to get the damage penalty
minStaminaToGetLowDamage = 50
# the minimum stamina to get the stamina warning.
minStaminaToGetExaustionWarning = 69
# stammina addition after running
staminaToAddAfterRunning = 5
runStaminamin = 1
runStaminamax = 2

# when we get all the coins, they lead us to the boss's lair.
stepsToLair = 0
maxStepsToLair = 15
maxStepsCounter = maxStepsToLair

# rarity variables
enemyMinRarity = 1
enemyMaxRarity = 5
itemMinRarity = 1
itemMaxRarity = 5
locationMinRarity = 1
locationMaxRarity = 5

## combat vars

# dodge probability
mindodge = 1
maxdodge = 10
# attack probability
minattack = 1
maxattack = 6
# block probability
minblock = 1
maxblock = 5
# probablility for 2 enemies in one encounter.
minduel = 1
maxduel = 10
# greater probability for the player to atttack enemies after dodging.
minattack_afterdodge = 3
maxattack_afterdodge = 15
# lower probability for the player to atttack tougher enemies after dodging.
minattack_afterdodge_toughenemy = 3
maxattack_afterdodge_toughenemy = 10
# higher probability for the player to atttack tougher enemies after blocking.
minattack_afterblock_toughenemy = 3
maxattack_afterblock_toughenemy = 15
# probability for the enemy to attack the player before they start running.
minEnemyAttacksPlayer = 1
maxEnemyAttacksPlayer = 5
# probability for the tougher enemies to attack the player before they start running.
minToughEnemyAttacksPlayer = 1
maxToughEnemyAttacksPlayer = 2
# dodge probability when fighting tougher enemies.
mindodge_toughenemy = 1
maxdodge_toughenemy = 5
# block probability when fighting tougher enemies.
minblock_toughenemy = 1
maxblock_toughenemy = 10
# probability if we are going to be revived at 0 health.
minRevive = 1
maxRevive = 5
# probability if we are going to be revived at 0 health for tougher enemies
minRevive_toughenemy = 1
maxRevive_toughenemy = 3
# the minimum amount of hp to consider us a tough enemy. the enemy's health must be over this. 
minToughEnemyHP = 100
# minimum health to consider us being at low health.
minHealthForLowHealth = 50
# the amount of stamina to reduce when attacking
staminaToReduceWhenAttacking = 2.2
# the amount of stamina to reduce when missing the attack
staminaToReduceWhenMissingAttack = 2.5
# the amount of stamina to reduce when dodging attacks
staminaToReduceWhenDodging = 1.5
# the amount of stamina to give back after fighting
staminaToRegenAfterCombat = 15
# the additional amount of stamina to give back if we are low on stamina
additionalStaminaToRegenAfterCombat = 35
# the amount of health to give back at low health.
healthToRegenAfterCombat = 50

# used for bonus stamina.
bonusstamina = additionalStaminaToRegenAfterCombat + staminaToRegenAfterCombat

##commands

# command lists
dirCommands = ["forward", "f", "left", "l", "right", "r", "backward", "b"]
encounterCommands = ["fight", "f", "run", "r"]
combatCommands = ["attack", "a", "dodge", "d", "block", "b"]
bootupCommands = ["yes", "y", "no", "n"]
difficultySelectCommands = ["easy", "e", "normal", "n", "knightmare", "k"]
# commands. they include aliases too :D (https://www.pythoncentral.io/how-to-slice-listsarrays-and-tuples-in-python/)
command_dir_forward = dirCommands[0:2]
command_dir_left = dirCommands[2:4]
command_dir_right = dirCommands[4:6]
command_dir_backward = dirCommands[6:8]

command_encounter_fight = encounterCommands[0:2]
command_encounter_run = encounterCommands[2:4]

command_combat_attack = combatCommands[0:2]
command_combat_dodge = combatCommands[2:4]
command_combat_block = combatCommands[4:6]

command_bootup_yes = bootupCommands[0:2]
command_bootup_no = bootupCommands[2:4]

command_difficulty_easy = difficultySelectCommands[0:2]
command_difficulty_normal = difficultySelectCommands[2:4]
command_difficulty_hard = difficultySelectCommands[4:6]

## TEXT
wintextbase = ""
wintext = wintextbase
wintext_boss = wintextbase
breathtext = ""
breathtextalt = ""
refillhealthtext = ""
baserevivetext = ""
combatrevivetext = baserevivetext
revivetext = baserevivetext
basedeadtext = ""
deadtext = basedeadtext
deadtextdungeon = basedeadtext
easytext = ""
normaltext = ""
hardtext = ""
starttext = ""
proceedtext = ""
gohometext = ""
breathtextrunning = ""

# update the text.
def updateText():
    global wintextbase, wintext, wintext_boss
    global breathtext, breathtextalt, breathtextrunning
    global refillhealthtext
    global baserevivetext, combatrevivetext, revivetext
    global basedeadtext, deadtext, deadtextdungeon
    global easytext, normaltext, hardtext
    global starttext, proceedtext, gohometext
    global currEnemy
    global staminaToRegenAfterCombat, bonusstamina, maxPlayerStamina, staminaToAddAfterRunning
    global healthToRegenAfterCombat, maxPlayerHealth
    global playerName
    global goldCoinsNeeded
    global command_difficulty_easy, command_difficulty_normal, command_difficulty_hard
    global enemyattacktext
    global test, gametitle
    
    wintextbase = "The " + currEnemy['name'] + " has been slayed!"
    
    wintext = """
""" + wintextbase + " "

    wintext_boss = "" + wintextbase + """

You have saved the kingdom from a threat like no other.
The hordes of supernatural invaders suddenly vanish throughout the dungeon and the kingdom.

Although, as a result of your success, you feel the quakes of the now unstable dungeon.
Your gold coins make a chatter in your pocket, and suddenly, a portal opens behind you.

You go through the portal and end up where you started. You hop onto your horse and race back to the kingdom.
You see the dungeon fall apart. The spirits inhabiting the abandoned rooms can finally rest.

When you arrive to the kingdom, the King welcomes you with open arms as a large crowd cheers upon your arrival.

A day later, the King officially announces your success to the kingdom to an equally loud roar from an even larger crowd.
The King declares you as the next person in line to become King.

After the celebration, the King asks you to come with him to his quarters.
He pulls out a legendary sword known as the DUNGEONBLADE. Only the King's trusted men can use this sword, and you are its next owner.

The King gives you the sword. When examining the blade, you notice """ + str(maxGoldCoinsToWin) + """ coin-sized holes embedded in the blade.
You insert the coins into the blade, and they fill the empty space to become one with the metal.

A blue fire surrounds the sword blade as you hold it firmly in your grasp. No supernatural being ever will attack the kingdom again.

Meanwhile, a pair of small, glowing red eyes peer out from the ruins of the dungeon. Red eyes that peer out for revenge...

T H E  E N D ."""

    breathtext = """
You take a deep breath after the battle.
After calming down, you continue your journey.

+""" + str(staminaToRegenAfterCombat) + """ Stamina
"""

    breathtextalt = """
You take a deep breath after the battle for an extended amount of time.
After calming down, you continue your journey.

+""" + str(bonusstamina) + """ Stamina
"""

    refillhealthtext = """Suddenly, you see a faerie floating around.
The faerie notices that you are hurt, and as such it heals most of your wounds.

+""" + str(healthToRegenAfterCombat) + """ Health
"""

    baserevivetext = """As your vision starts to blur, you notice the image of a faerie.
Miraculously, the faerie fully revitalizes you and brings you back to life.

+""" + str(maxPlayerHealth) + """ Health
+""" + str(maxPlayerStamina) + """ Stamina"""

    combatrevivetext = """
After the strike from the """ + currEnemy['name'] + """, you collapse and you slowly begin to see the light.

""" + baserevivetext

    revivetext = """After you have been attacked by one of the dungeon's traps, you collapse and you slowly begin to see the light.

""" + baserevivetext + "\n"

    basedeadtext = """The kingdom is now in grave danger as hordes of paranormal beings overwhelm
the King's forces. Everyone tries to evacuate, but it is too late.

G A M E  O V E R."""

    deadtext = "You have been defeated by the " + currEnemy['name'] + """.

""" + basedeadtext

    deadtextdungeon = """You have been taken down by one of the dungeon's traps.

""" + basedeadtext

    easytext = "\n" + command_difficulty_easy[0].title() + """:
You begin with more power than you have ever imagined.
Enemies tremble in fear by your immense strength and luck.
Your lungs are made of iron, and will take a very long time to run out of breath.
Faeries will most likely come to you.
You are nearly invulnerable.
""" + ("""
NOTE: Test mode is enabled.
This gives you even more power for the convienence of testing harder elements of """ + gametitle + """.

You will also see debugging text for every element of the game for testing.""" if test == True else "")

    normaltext = "\n" + command_difficulty_normal[0].title() + """:
You begin with relatively high confidence.
Enemies are a fair challenge, but will eliminate you if you are not mindful of your strategies.
You will run out of breath often, but you will fully regain it with time.
Faeries come to you in times of need, sometimes before death.
Everything is balanced, as it should be.
"""

    hardtext = "\n" + command_difficulty_hard[0].title() + """:
You begin without any hope for survival. You are very weak.
Enemies will rip you apart, and some lower-ranking enemies are tougher.
You will be out of breath multiple times during your journey.
It is rare for a faerie to come to you.
You will die.
"""

    starttext = """
May 5th, 1394:

You are """ + playerName + """, the Royal Guard for the King.

You're rushing down a long, dark path on your horse.
There's been a dramatic turn of events.
    
You recently got a letter from the King, stating that the kingdom is in need of your services.
It's been under attack by paranormal beings beyond this material world.
After many weeks, the King was informed of the location of these beings.

A large dungeon was identified as being the main home for all these ghastly beasts roaming the kingdom.
This specific dungeon is a magical dungeon, which has a life of its own.
It builds itself around any living inhabitants and summons beasts, items, traps, and locations.
The dungeon also inhabits faeries that have magical healing properties.

As sworn Royal Guard for the King, you must protect the kingdom from these beasts by slaying them in this living dungeon.

You have also heard of a mythic legend where """ + str(goldCoinsNeeded) + """ golden coin""" + ("s" if maxGoldCoinsToWin > 1 else "") + """ """ + ("were placed in special locations all over the dungeon." if maxGoldCoinsToWin > 1 else "was placed in a special location inside the dungeon.") + """
""" + ("These coins give" if maxGoldCoinsToWin > 1 else "This coin gives") + """ the possessor immense boosts of strength. They also will lead you to a 'mystic figure' that rules the dungeon.
Defeat the figure, and you will be able to escape from the dungeon.
The legends also hinted at an 'apocalyptic event' that would happen afterward, but they weren't specific.

After hearing that, you took your """ + item_sword['name'].replace("their ", "") + """, your """ + item_shield['name'].replace("their ", "") + """, and your horse down this dark passage.

You stand before a mighty doorway. You go towards it, but you are unsure if you are ready.
"""

    proceedtext = """
You walk towards the large doorway.
The dungeon seems like a large maze at first.
You slice your sword into the ground to mark where you are, then you proceed through the hallway.
"""

    gohometext = """
You go back on your horse towards the kingdom.
You tell the king you were too cowardly to attack the beasts.
The King fires you, and the kingdom continues to be invaded by the paranormal.

G A M E  O V E R ."""

    breathtextrunning = """You stop for a moment to take a deep breath after running from the """ + currEnemy['name'] + """.
After calming down, you continue your journey.

+""" + str(staminaToAddAfterRunning) + """ Stamina
"""
    if test == True:
        print("DEBUG: Text updated")

## COMMANDS

# creates a string list for a command and aliases
def outputCommandListForCommand(lst, uppercase):
    if test == True:
        print("DEBUG: Grabbing command list...")

    cmdList = ""

    first = lst[0]
    last = lst[-1]

    for entry in lst:
        if entry != first:
            if entry != last:
                cmdList += str(entry) + "/"
            elif entry == last:
                cmdList += str(entry)
        elif entry == first:
            if uppercase == True:
                cmdList += str(entry).title() + "/"
            elif uppercase == False:
                cmdList += str(entry) + "/"

    if test == True:
        print("DEBUG: Command list is " + cmdList)

    return cmdList

# grabs input depending on gamestate.
def getParserForGameState():
    global gamestate
    global command_difficulty_easy, command_difficulty_normal, command_difficulty_hard
    global command_bootup_yes, command_bootup_no
    global command_dir_right, command_dir_left, command_dir_forward, command_dir_backward
    global command_encounter_fight, command_encounter_run
    global command_combat_attack, command_combat_dodge, command_combat_block
    global test

    if test == True:
        print("DEBUG: Grabbing parser for game state " + str(gamestate))

    parser = ""
    
    #-3: difficulty select
    if gamestate == -3:
        if test == False:
            parser = input("Type " +
                           outputCommandListForCommand(command_difficulty_easy, False) + " for the " + command_difficulty_easy[0].title() + " difficulty,\n" +
                           outputCommandListForCommand(command_difficulty_normal, False) + " for the " + command_difficulty_normal[0].title() + " difficulty, or\n" +
                           outputCommandListForCommand(command_difficulty_hard, False) + " for the " + command_difficulty_hard[0].title() + " difficulty: ")
        elif test == True:
            parser = input("Type " +
                           outputCommandListForCommand(command_difficulty_easy, False) + " for the " + command_difficulty_easy[0].title() + " difficulty. Test mode is enabled: ")
    #-2: name change
    elif gamestate == -2:
        parser = input("Please enter your name to proceed: ")
    #-1: story
    elif gamestate == -1:
        parser = input("Type " + outputCommandListForCommand(command_bootup_yes, False) + " if you are ready to proceed, or " +
                    outputCommandListForCommand(command_bootup_no, False) + " if you just want to go home: ")
    #0: exploring
    elif gamestate == 0:
        parser = input("Choose where you want to go: " + outputCommandListForCommand(command_dir_left, False) + ", " +
                      outputCommandListForCommand(command_dir_right, False) + ", " + outputCommandListForCommand(command_dir_forward, False) +
                      " or " + outputCommandListForCommand(command_dir_backward, False) + ": ")
    #1: enemy encounter
    elif gamestate == 1:
        parser = input("What do you want to do? " + outputCommandListForCommand(command_encounter_fight, True) + " or " + outputCommandListForCommand(command_encounter_run, False) + "?: ")
    #2: combat
    elif gamestate == 2:
        parser = input("What do you want to do? " +
                   outputCommandListForCommand(command_combat_attack, True) + ", " +
                   outputCommandListForCommand(command_combat_dodge, False) + " or " +
                   outputCommandListForCommand(command_combat_block, False) + "?: ")

    return parser

# get the command list array.
def getCommandsForGameState():
    global gamestate
    global combatCommands
    global encounterCommands
    global dirCommands
    global difficultySelectCommands
    global bootupCommands

    commands = []

    #-3: difficulty select
    if gamestate == -3:
        commands = difficultySelectCommands
    #-1: story
    elif gamestate == -1:
        commands = bootupCommands
    #0: exploring
    elif gamestate == 0:
        commands = dirCommands
    #1: enemy encounter
    elif gamestate == 1:
        commands = encounterCommands
    #2: combat
    elif gamestate == 2:
        commands = combatCommands

    if test == True:
        print("DEBUG: Commands for game state: " + str(commands))

    return commands

## difficulty stuff

# adjust difficulty setting
def adjustDifficulty():
    # WHYYYYYY ;_;
    # better now but STILL.
    global command_difficulty_easy, command_difficulty_normal, command_difficulty_hard
    global difficulty
    global playerHealth, maxPlayerHealth, maxPlayerHealthAfterCoins
    global playerStamina, maxPlayerStamina
    global mindodge, maxdodge
    global minattack, maxattack
    global minblock, maxblock
    global minattack_afterdodge, maxattack_afterdodge
    global minattack_afterdodge_toughenemy, maxattack_afterdodge_toughenemy
    global minEnemyAttacksPlayer, maxEnemyAttacksPlayer
    global minToughEnemyAttacksPlayer, maxToughEnemyAttacksPlayer
    global mindodge_toughenemy, maxdodge_toughenemy
    global minblock_toughenemy, maxblock_toughenemy
    global minRevive, maxRevive
    global minduel, maxduel
    global minRevive_toughenemy, maxRevive_toughenemy
    global minToughEnemyHP
    global minHealthForLowHealth
    global staminaToReduceWhenAttacking, staminaToReduceWhenMissingAttack, staminaToReduceWhenDodging, staminaToRegenAfterCombat, additionalStaminaToRegenAfterCombat, staminaToReduceWhileWalking, staminaToReduceWhileRunning, minStaminaToGetLowDamage, minStaminaToGetExaustionWarning, staminaToAddAfterRunning
    global healthToRegenAfterCombat
    global minStepsToDiscover
    global maxGoldCoinsToWin, goldCoinsNeeded
    global lowStaminaDamageReductionMultiplier, emptyStaminaDamageReductionMultiplier
    global runStaminamax
    global minattack_afterblock_toughenemy, maxattack_afterblock_toughenemy
    global easytext, normaltext, hardtext
    global test
    
    if difficulty in command_difficulty_easy:
        #easy

        # TEST MODE TOGGLED VALUES:
        #Increase health more on test mode and increase probability of harder stuff.
        if test == True:
            minduel = 1
            maxduel = 3
            # probability for the enemy to attack the player before they start running.
            minEnemyAttacksPlayer = 1
            maxEnemyAttacksPlayer = 3
            # probability for the tougher enemies to attack the player before they start running.
            minToughEnemyAttacksPlayer = 1
            maxToughEnemyAttacksPlayer = 3
            maxGoldCoinsToWin = 1
            # the amount of steps to discover our first discovery.
            minStepsToDiscover = 3
        elif test == False:
            minduel = 1
            maxduel = 15
            # probability for the enemy to attack the player before they start running.
            minEnemyAttacksPlayer = 1
            maxEnemyAttacksPlayer = 10
            # probability for the tougher enemies to attack the player before they start running.
            minToughEnemyAttacksPlayer = 1
            maxToughEnemyAttacksPlayer = 5
            # maximum health
            maxPlayerHealth = 150
            # Maximum health after we get coins.
            maxPlayerHealthAfterCoins  = 250
            # maximum stamina
            maxPlayerStamina = 150
            # the amount of stamina to reduce when walking
            staminaToReduceWhileWalking = 0.7
            # the amount of stamina to reduce when running
            staminaToReduceWhileRunning = 1.2
            maxGoldCoinsToWin = 2
            # the minimum amount of hp to consider us a tough enemy. the enemy's health must be over this. 
            minToughEnemyHP = 200

        # the health
        playerHealth = maxPlayerHealth
        # the stamina
        playerStamina = maxPlayerStamina
        # how many coins we need to win the game.
        goldCoinsNeeded = maxGoldCoinsToWin
        
        # if we have <= 50 stamina, multiply the damage by this. 
        lowStaminaDamageReductionMultiplier = 0.8
        # if we have 0 stamina, multiply the damage by this.
        emptyStaminaDamageReductionMultiplier = 0.6
        
        ## combat vars
            
        # dodge probability
        mindodge = 1
        maxdodge = 15
        # attack probability
        minattack = 1
        maxattack = 15
        # block probability
        minblock = 1
        maxblock = 10
        # greater probability for the player to atttack enemies after dodging.
        minattack_afterdodge = 3
        maxattack_afterdodge = 20
        # lower probability for the player to atttack tougher enemies after dodging.
        minattack_afterdodge_toughenemy = 1
        maxattack_afterdodge_toughenemy = 10
        # higher probability for the player to atttack tougher enemies after blocking.
        minattack_afterblock_toughenemy = 3
        maxattack_afterblock_toughenemy = 20
        # dodge probability when fighting tougher enemies.
        mindodge_toughenemy = 1
        maxdodge_toughenemy = 10
        # block probability when fighting tougher enemies.
        minblock_toughenemy = 1
        maxblock_toughenemy = 15
        # probability if we are going to be revived at 0 health.
        minRevive = 1
        maxRevive = 3
        # probability if we are going to be revived at 0 health for tougher enemies
        minRevive_toughenemy = 1
        maxRevive_toughenemy = 2
        # minimum health to consider us being at low health.
        minHealthForLowHealth = 75
        # the amount of stamina to reduce when attacking
        staminaToReduceWhenAttacking = 1
        # the amount of stamina to reduce when missing the attack
        staminaToReduceWhenMissingAttack = 1.5
        # the amount of stamina to reduce when dodging attacks
        staminaToReduceWhenDodging = 0.7
        # the amount of stamina to give back after fighting
        staminaToRegenAfterCombat = 50
        # the additional amount of stamina to give back if we are low on stamina
        additionalStaminaToRegenAfterCombat = 50
        # the amount of health to give back at low health.
        healthToRegenAfterCombat = 50
        # stammina addition after running
        staminaToAddAfterRunning = 10

        print(easytext)
    elif difficulty in command_difficulty_normal:
        #normal is default settings
        print(normaltext)
    elif difficulty in command_difficulty_hard:
        #hard
        # maximum health
        maxPlayerHealth = 50
        # Maximum health after we get coins.
        maxPlayerHealthAfterCoins  = 100
        # the health
        playerHealth = maxPlayerHealth
        
        # the amount of stamina to reduce when walking
        staminaToReduceWhileWalking = 2
        # the amount of stamina to reduce when running
        staminaToReduceWhileRunning = 3.5
        # the minimum stamina to get the damage penalty
        minStaminaToGetLowDamage = 55
        # the minimum stamina to get the stamina warning.
        minStaminaToGetExaustionWarning = 65

        # how many coins we need to win the game.
        maxGoldCoinsToWin = 5
        goldCoinsNeeded = maxGoldCoinsToWin
        # if we have <= 50 stamina, multiply the damage by this. 
        lowStaminaDamageReductionMultiplier = 0.5
        
        ## combat vars

        minduel = 1
        maxduel = 5
        # probability for the enemy to attack the player before they start running.
        minEnemyAttacksPlayer = 1
        maxEnemyAttacksPlayer = 3
        # dodge probability when fighting tougher enemies.
        mindodge_toughenemy = 1
        maxdodge_toughenemy = 4
        # probability if we are going to be revived at 0 health.
        minRevive = 1
        maxRevive = 7
        # probability if we are going to be revived at 0 health for tougher enemies
        minRevive_toughenemy = 1
        maxRevive_toughenemy = 5
        # the minimum amount of hp to consider us a tough enemy. the enemy's health must be over this. 
        minToughEnemyHP = 60
        # minimum health to consider us being at low health.
        minHealthForLowHealth = 20
        # the amount of stamina to reduce when attacking
        staminaToReduceWhenAttacking = 2.5
        # the amount of stamina to reduce when missing the attack
        staminaToReduceWhenMissingAttack = 3
        # the amount of stamina to reduce when dodging attacks
        staminaToReduceWhenDodging = 2
        # the amount of health to give back at low health.
        healthToRegenAfterCombat = 30
        # stammina addition after running
        staminaToAddAfterRunning = 2.5
        runStaminamax = 4

        print(hardtext)
        
    # used for bonus stamina.
    bonusstamina = additionalStaminaToRegenAfterCombat + staminaToRegenAfterCombat

    if test == True:
        print("DEBUG: Difficulty " + difficulty + "... initalized.")

#get the main difficulty command name.
def getDifficulty():
    global difficulty
    global command_difficulty_easy, command_difficulty_normal, command_difficulty_hard

    if test == True:
        print("DEBUG: Difficulty is " + difficulty + "... Interpreting...")

    # i don't like this...
    if difficulty in command_difficulty_easy:
        return command_difficulty_easy[0]
    elif difficulty in command_difficulty_normal:
        return command_difficulty_normal[0]
    elif difficulty in command_difficulty_hard:
        return command_difficulty_hard[0]

## ITEMS, ENEMIES, AND EVIRONMENT.

# update objects.
def updateObjects():
    global itempool, enemypool, locationpool
    global npc_boss, room_finalboss
    global item_sword, item_shield
    global maxPlayerHealth, maxPlayerStamina

    """
Items

aka Pickups, Weapons, and Traps

init items. simpler definition.

format: item name, the description upon pickup, the amount of health the item will give/take away from the player or enemy,
the amount of stamina it will give/take away from the player from using it, the rarity (from 1 to 4 for any item that's not the sword), and
a boolean if this item adds to the gold count upon pickup.

note, 'staminatouse' can also be used as the maximum damage an an enemy will deal to a player.
there's also a description for each enemy weapon to describe the enemy's actions.
    """

    ## weapons

    # player weapons

    # Sword
    item_sword = {
        'name': 'their sword',
        # used for enemies.
        'desc': 'The enemy swings their weapon at you!',
        'healthtouse': 15,
        #this is used for the max enemy damage only for enemy/player weapons.
        'staminatouse': 20,
        "rarity": 0,
        'isgold': False,
        'istrap': False}

    # Shield
    item_shield = {
        'name': 'their shield',
        'desc': 'The enemy blocks your attack!',
        'healthtouse': 0,
        'staminatouse': 0,
        "rarity": 0,
        'isgold': False,
        'istrap': False}

    # enemy weapons

    # bow and arrow. also used in a trap.
    item_arrow = {
        'name': 'their bow and arrow',
        'desc': 'The enemy shoots an arrow at you!',
        'healthtouse': 10,
        'staminatouse': 15,
        "rarity": 0,
        'isgold': False,
        'istrap': True}

    # rat claw
    item_claw = {
        'name': 'their claws',
        'desc': 'The enemy scratches you!',
        'healthtouse': 5,
        'staminatouse': 8,
        "rarity": 0,
        'isgold': False,
        'istrap': True}

    # claw for "low ranking" common enemies
    item_lowrankclaw = {
        'name': item_claw['name'],
        'desc': item_claw['desc'],
        'healthtouse': 15,
        'staminatouse': 20,
        "rarity": item_claw['rarity'],
        'isgold': item_claw['isgold'],
        'istrap': item_claw['istrap']}

    # claw for "high ranking" rare enemies
    item_highrankclaw = {
        'name': item_claw['name'],
        'desc': item_claw['desc'],
        'healthtouse': 25,
        'staminatouse': 30,
        "rarity": item_claw['rarity'],
        'isgold': item_claw['isgold'],
        'istrap': item_claw['istrap']}

    # katana for the demigod
    item_katana = {
        'name': 'their katana',
        'desc': item_sword['desc'],
        'healthtouse': 25,
        'staminatouse': 30,
        "rarity": item_sword['rarity'],
        'isgold': item_sword['isgold'],
        'istrap': item_sword['istrap']}

    # staff for the boss
    item_bossstaff = {
        'name': 'their staff',
        'desc': 'The enemy shoots a large lightning bolt at you!',
        'healthtouse': 35,
        'staminatouse': 40,
        "rarity": 0,
        'isgold': False,
        'istrap': True}

    # staff for the demigod
    item_highrankstaff = {
        'name': item_bossstaff['name'],
        'desc': 'The enemy shoots a small lightning bolt at you!',
        'healthtouse': 25,
        'staminatouse': 30,
        "rarity": item_bossstaff['rarity'],
        'isgold': item_bossstaff['isgold'],
        'istrap': item_bossstaff['istrap']}

    # telekinesis
    item_telekinesis = {
        'name': 'their telekinesis',
        'desc': 'The enemy flings heavy rocks and debis at you!',
        'healthtouse': 15,
        'staminatouse': 20,
        "rarity": 0,
        'isgold': False,
        'istrap': True}

    item_bite = {
        'name': "their bite",
        'desc': "The enemy bites you!",
        'healthtouse': 8,
        'staminatouse': 10,
        "rarity": 0,
        'isgold': False,
        'istrap': True}

    item_lowrankbite = {
        'name': item_bite['name'],
        'desc': item_bite['desc'],
        'healthtouse': 15,
        'staminatouse': 20,
        "rarity": item_bite['rarity'],
        'isgold': item_bite['isgold'],
        'istrap': item_bite['istrap']}

    item_highrankbite = {
        'name': item_bite['name'],
        'desc': item_bite['desc'] + " It was poisonous!",
        'healthtouse': 25,
        'staminatouse': 30,
        "rarity": item_bite['rarity'],
        'isgold': item_bite['isgold'],
        'istrap': item_bite['istrap']}

    ## Pickups

    # small Medical kit - gives the player 15 HP upon pickup.
    item_smallfirstaid = {
        'name': 'a small medical kit',
        # for pickups and traps, the health and stamina usage affects the player.
        'desc': """You open the medical kit. You kneel down and patch your wounds with the included bandages.
Afterwards, you stand up and you keep moving.
""",
        'healthtouse': 15,
        'staminatouse': 0,
        "rarity": 1,
        'isgold': False,
    'istrap': False}

    # Medical kit - gives the player 30 HP upon pickup.
    item_firstaid = {
        'name': 'a large medical kit',
        'desc': """You open the medical kit. You kneel down and patch your wounds with the included bandages.
Afterwards, you stand up and you keep moving.
""",
        'healthtouse': 30,
        'staminatouse': 0,
        "rarity": 1,
        'isgold': False,
        'istrap': False}

    # Water cup - gives the player 15 stamina points upon pickup.
    item_smallwater = {
        'name': 'a cup of water',
        'desc': """You drink the water. You feel refreshed.
""",
        'healthtouse': 0,
        'staminatouse': 15,
        "rarity": 1,
        'isgold': False,
        'istrap': False}

    # Water - gives the player 30 stamina points upon pickup.
    item_water = {
        'name': 'a bottle of water',
        'desc': """You drink the water. You feel refreshed.
""",
        'healthtouse': 0,
        'staminatouse': 30,
        "rarity": 1,
        'isgold': False,
        'istrap': False}

    # potion - gives the player 50 stamina points and 50 HP upon pickup.
    item_potion = {
        'name': 'a magical potion',
        'desc': """You drink the potion. You feel rejuvinated.
""",
        'healthtouse': maxPlayerHealth,
        'staminatouse': maxPlayerStamina,
        "rarity": 3,
        'isgold': False,
        'istrap': False}

    ## Traps

    # poison - harms the player, but is rare to find.
    item_poison = {
        'name': 'a magical potion',
        'desc': """You drink the potion. You instantly feel sick.
You recover shortly afterwards, but at a price.
""",
        'healthtouse': 15,
        'staminatouse': 3,
        "rarity": 3,
        'isgold': False,
        'istrap': True}

    # bear trap - harms the player, but is rare to find.
    item_beartrap = {
        'name': 'a bear trap (after stepping on it)',
        'desc': """You have accidentally stepped on a bear trap.
You scream in pain as you try to remove your foot from the metal jaws.
You manage to pry it free, but at a price.
""",
        'healthtouse': 25,
        'staminatouse': 5,
        "rarity": 3,
        'isgold': False,
        'istrap': True}

    # tripwire - harms the player. but is rare to find.
    item_tripwire = {
        'name': 'a line of silk (after tripping on it)',
        'desc': """You trip over a silk string, causing multiple arrows to fire at you.
Fortunately, you avoid most of them. However, only one of the arrows pierces your abdomen.
You manage to remove the arrow, but at a price.
""",
        'healthtouse': item_arrow['healthtouse'],
        'staminatouse': 0,
        "rarity": 3,
        'isgold': False,
        'istrap': True}

    # a pit, not the one from BIONICLE.
    item_pit = {
        'name': 'a pit (after falling into it)',
        'desc': """You accidentally fall into a small pit while not looking.
You manage to escape the pit, but at a price.
""",
        'healthtouse': 10,
        'staminatouse': 0,
        "rarity": 4,
        'isgold': False,
        'istrap': True}

    # spikes x5
    item_spikes = {
        'name': 'a tile of spikes (after stepping on it)',
        'desc': """You have accidentally stepped on a tile of spikes.
You scream in pain as you try to remove the small, but sharp pointy pieces of metal from your foot.
You manage to remove the spikes from your foot, but at a price.
""",
        'healthtouse': 20,
        'staminatouse': 3,
        "rarity": 4,
        'isgold': False,
        'istrap': True}

    # tripwire 2 arrows - harms the player. but is rare to find.
    item_tripwireX2 = {
        'name': 'a line of silk (after tripping on it)',
        'desc': """You trip over a silk string, causing multiple arrows to fire at you.
Fortunately, you avoid most of them. However, two of the arrows pierce your abdomen.
You manage to remove the arrows, but at a price.
""",
        'healthtouse': int(item_tripwire['healthtouse'] * 2),
        'staminatouse': item_tripwire['staminatouse'],
        "rarity": 5,
        'isgold': item_tripwire['isgold'],
        'istrap': item_tripwire['istrap']}

    # spikes and pit
    item_spikesandpit = {
        'name': 'a pit with serveral tiles of spikes (after falling into the pit and landing on the spikes)',
        'desc': """You accidentally fall into a small pit while not looking.
When you reach the bottom, you land on several tiles of spikes.
You manage to escape the deadly pit, but at a price.
""",
        'healthtouse': int((item_spikes['healthtouse'] * 1.1) + item_pit['healthtouse']),
        'staminatouse': 6,
        "rarity": 5,
        'isgold': False,
        'istrap': True}

    # Gold Coin
    item_goldcoin = {
        'name': 'a gold coin',
        'desc': """You pick up the gold coin. A glow illuminates from it.
You put it in your pocket and continue your journey.
""",
        'healthtouse': 50,
        'staminatouse': 0,
        "rarity": 5,
        'isgold': True,
        'istrap': False}

    # items must be added in here to be a part of the game. The sword/shield is given to the player by default so we don't include it.
    itempool = [item_smallfirstaid, item_firstaid, item_smallwater, item_water, item_goldcoin, item_potion, item_poison, item_beartrap, item_tripwire, item_pit, item_spikes, item_tripwireX2, item_spikesandpit]

    if test == True:
        print("DEBUG: Items initalized.")

    """
Enemies

init enemy stats with a dictionary (https://docs.python.org/3/library/stdtypes.html#dict)

format: enemy name, enemy weapon, minimum health, maximum health, and rarity (an integer from 1 to 5)
    """

    # skeleton knight
    npc_skeletonknight = {
        'name': 'skeleton knight',
        'weapon': item_sword,
        "health": 50,
        "maxhealth": 50,
        "rarity": 1}

    # skeleton archer
    npc_skeletonarcher = {
        'name': 'skeleton archer',
        'weapon': item_arrow,
        "health": 50,
        "maxhealth": 50,
        "rarity": 1}

    # zombies
    npc_zombie = {
        'name': 'zombie',
        'weapon': item_lowrankbite,
        "health": 75,
        "maxhealth": 75,
        "rarity": 1}

    # ghosts
    npc_ghost = {
        'name': 'ghost',
        'weapon': item_telekinesis,
        "health": 45,
        "maxhealth": 45,
        "rarity": 2}

    # the rat - Rarer than actual enemies for less encounters.
    npc_rat = {
        'name': 'rat',
        'weapon': item_claw,
        "health": 30,
        "maxhealth": 30,
        "rarity": 3}

    # the sp-ider
    npc_spider = {
        'name': 'spider',
        'weapon': item_bite,
        "health": 20,
        "maxhealth": 20,
        "rarity": 3}

    # silverfish
    npc_silverfish = {
        'name': 'silverfish',
        'weapon': item_bite,
        "health": 15,
        "maxhealth": 15,
        "rarity": 3}

    # goblins
    npc_goblin = {
        'name': 'goblin',
        'weapon': item_lowrankclaw,
        "health": 60,
        "maxhealth": 60,
        "rarity": 3}

    # gargoyles
    npc_gargoyle = {
        'name': 'gargoyle',
        'weapon': item_lowrankclaw,
        "health": 85,
        "maxhealth": 85,
        "rarity": 3}

    # the large sp-ider
    npc_largespider = {
        'name': 'large spider',
        'weapon': item_highrankbite,
        "health": 65,
        "maxhealth": 65,
        "rarity": 4}

    # Manticore
    npc_manticore = {
        'name': 'manticore',
        'weapon': item_highrankclaw,
        "health": 125,
        "maxhealth": 125,
        "rarity": 4}

    # ghost samurai
    npc_ghostsamurai = {
        'name': 'ghost samurai',
        'weapon': item_katana,
        "health": 100,
        "maxhealth": 100,
        "rarity": 4}

    # demigod
    npc_demigod = {
        'name': 'demigod',
        'weapon': item_highrankstaff,
        "health": 150,
        "maxhealth": 150,
        "rarity": 5}

    # minotaur
    npc_minotaur = {
        'name': 'minotaur',
        'weapon': item_highrankclaw,
        "health": 175,
        "maxhealth": 175,
        "rarity": 5}

    # Necromancer - this guy runs the place. Only in final boss battle.
    npc_boss = {
        'name': 'necromancer',
        'weapon': item_bossstaff,
        "health": 250,
        "maxhealth": 250,
        "rarity": 0}

    # enemies must be added in here to be a part of the game.
    enemypool = [npc_rat, npc_skeletonknight, npc_skeletonarcher, npc_zombie, npc_ghost, npc_goblin, npc_gargoyle, npc_demigod, npc_manticore, npc_spider, npc_largespider, npc_minotaur, npc_silverfish, npc_ghostsamurai]

    if test == True:
        print("DEBUG: Enemies initalized.")

    """
Locations/Rooms

init locations. even simpler definition.

format: location name, location description, and location rarity (1-5).
    """

    # Throne Room
    room_throneroom = {
        'name': 'a degraded throne room',
        'desc': """You see a large expance.
In front of you, you see a large throne with 2 portraits.
On the floor you see shattered vaces, rotten flowers, and articles of clothing. Some poor soul had to live in this place...
""",
        'rarity': 5}

    # Dining Room
    room_diningroom = {
        'name': 'a degraded dining room',
        'desc': """You see a large wooden table, with dishes left on it.
On the floor, you see more plates, most of them shattered.
You can see lavish decorations all over the room. Flies buzz all around the room. Who would eat here anymore?
""",
        'rarity': 4}

    # Armory
    room_armory = {
        'name': 'a large armory',
        'desc': """In front of you, you see several suits of armor.
Some of these suits of armor have broken apart over time.
You also see large shields between each suit, depicting a yellow lion over a red background. 
""",
        'rarity': 4}

    #A room with a lot of plants.
    room_overgrowth = {
        'name': 'a room covered in a massive overgrowth',
        'desc': """All over you, you see large plants growing from the cracks in the walls.
You see vines hanging from the ceiling.
This room has not been maintained for years...
""",
        'rarity': 2}

    #blank space
    room_empty = {
        'name': 'an empty room',
        'desc': """The entire room is empty, with apparently nothing to be found in all directions...
""",
        'rarity': 2}

    #ruins
    room_ruins = {
        'name': 'a pile of ruins',
        'desc': """You see remmnants of a massive building from centuries' past.
Large pieces of stone litter the ground.
These ruins seem to come from a temple of a religious purpose...
""",
        'rarity': 3}

    #room filled with bones
    room_bones = {
        'name': 'a room filled with bones',
        'desc': """Around you, you see thousands upon thousands of bones.
Many of them seem to be from fallen explorers who have dared to explore this place.
You hear the haunting voices of many of these unfortunate explorers, which sends a shiver down your spine...
""",
        'rarity': 4}

    # The final boss room. Not in the location pool as it's forced onto the player after we get the gold coins.
    room_finalboss = {
        'name': 'a large empty room',
        'desc': room_empty['desc'] + """
However, as you begin to investigate, a portal opens at the front of the room.
A large ghastly figure emerges from the portal. This must be the 'mystic figure'
the legends hinted at.

You ready your """ + item_sword['name'].replace("their ", "") + ".",
        'rarity': 0}

    # locations must be added in here to be a part of the game.
    locationpool = [room_throneroom, room_diningroom, room_armory, room_overgrowth, room_empty, room_ruins, room_bones]

    if test == True:
        print("DEBUG: Locations initalized.")
        print("DEBUG: Objects updated.")

## stat level manipuation

# stamina funcs

# set the stamina
def setStamina(amount):
    global playerStamina, maxPlayerStamina

    if playerStamina < maxPlayerStamina:
        playerStamina = amount
        # so we don't mess up the UI we round the number to the second decimal. (https://www.w3schools.com/python/ref_func_round.asp)
        playerStamina = round(playerStamina, 2)

        if playerStamina <= 0:
            playerStamina = 0

        if playerStamina >= maxPlayerStamina:
            playerStamina = maxPlayerStamina

    if test == True:
        print("DEBUG: Stamina is " + str(playerStamina))

# increase the stamina
def increaseStamina(amount):
    global playerStamina, maxPlayerStamina

    if playerStamina < maxPlayerStamina:
        playerStamina += amount
        # so we don't mess up the UI we round the number to the second decimal. (https://www.w3schools.com/python/ref_func_round.asp)
        playerStamina = round(playerStamina, 2)

        if playerStamina >= maxPlayerStamina:
            playerStamina = maxPlayerStamina

    if test == True:
        print("DEBUG: Stamina is " + str(playerStamina))

# reduce the stamina
def reduceStamina(amount):
    global playerStamina

    if playerStamina > 0:
        playerStamina -= amount
        # so we don't mess up the UI we round the number to the second decimal. (https://www.w3schools.com/python/ref_func_round.asp)
        playerStamina = round(playerStamina, 2)

        if playerStamina <= 0:
            playerStamina = 0

    if test == True:
        print("DEBUG: Stamina is " + str(playerStamina))

# health funcs

# set the health
def setHealth(amount):
    global playerHealth, maxPlayerHealth

    if playerHealth < maxPlayerHealth:
        playerHealth = int(amount)

        if playerHealth <= 0:
            playerHealth = 0

        if playerHealth >= maxPlayerHealth:
            playerHealth = maxPlayerHealth

    if test == True:
        print("DEBUG: Health is " + str(playerHealth))

# increase the health
def increaseHealth(amount):
    global playerHealth, maxPlayerHealth

    if playerHealth < maxPlayerHealth:
        playerHealth += int(amount)

        if playerHealth >= maxPlayerHealth:
            playerHealth = maxPlayerHealth

    if test == True:
        print("DEBUG: Health is " + str(playerHealth))

# sdecrease the health
def decreaseHealth(amount):
    global playerHealth

    if playerHealth > 0:
        # decrease only half the health amount in test mode.
        if test == True:
            playerHealth -= int(amount * 0.5)
        elif test == False:
            playerHealth -= int(amount)

        if playerHealth <= 0:
            playerHealth = 0

    if test == True:
        print("DEBUG: Health is " + str(playerHealth))

## direction/location stuff

def getDirection():
    global direction

    if test == True:
        print("DEBUG: Direction is " + direction + "... Interpreting...")

    # i don't like this...
    if direction in command_dir_left:
        return command_dir_left[0]
    elif direction in command_dir_right:
        return command_dir_right[0]
    elif direction in command_dir_forward:
        return command_dir_forward[0]
    elif direction in command_dir_backward:
        return command_dir_backward[0]

## "user interface"
        
def playerStats():
    global playerName
    global playerHealth, maxPlayerHealth
    global playerStamina, maxPlayerStamina
    global playerGold
    global doesPlayerHaveGoldCoinPowers
    global minStaminaToGetLowDamage, minStaminaToGetExaustionWarning
    global playerLocation

    addtext = ""

    # Add a status indicator if we are exhausted or enchanted.
    if doesPlayerHaveGoldCoinPowers == True:
        if playerStamina <= minStaminaToGetLowDamage:
            addtext = " the Empowered (Exhausted)"
        elif playerStamina > minStaminaToGetLowDamage:
            addtext = " the Empowered"
    elif doesPlayerHaveGoldCoinPowers == False:
        if playerStamina <= minStaminaToGetLowDamage:
            addtext = " (Exhausted)"
        elif playerStamina > minStaminaToGetLowDamage:
            addtext = ""

    # display player stats with style
    playerStats = "--------------------\n|Name: " + playerName + addtext + "|\n|Health: " + str(playerHealth) + "/" + str(
        maxPlayerHealth) + "|\n|Stamina: " + str(playerStamina) + "/" + str(maxPlayerStamina) + "|\n|Gold Coins: " + str(playerGold) + "|\n|Location:|\n|X: " + str(
        playerLocation[0]) + " Y: " + str(playerLocation[1]) + "|"
    print(playerStats)

    # tell us the steps if we have coins.
    if (doesPlayerHaveGoldCoinPowers == True) and (maxStepsCounter > 0):
        if maxStepsCounter > 1:
            print("|The coins lead you to the " + npc_boss['name'].title() + "'s lair.|\n|" +
                  str(maxStepsCounter) + " more steps to go...|")
        elif maxStepsCounter == 1:
            print("|The coins lead you to the " + npc_boss['name'].title() + "'s lair.|\n|" +
                  str(maxStepsCounter) + " more step to go...|")

    # tell us the status of our stamina.
    if playerHealth > 0:
        if playerStamina <= minStaminaToGetLowDamage:
            print("|You feel exhausted.|")
        elif playerStamina > minStaminaToGetLowDamage and playerStamina < minStaminaToGetExaustionWarning:
            print("|You begin to feel exhausted.|")

    # add line for asthetics
    print("--------------------\n")


def enemyStats(enemy):
    # display enemy stats
    # capitalize all words in enemy name. (https://www.tutorialspoint.com/python/string_title.htm)
    enemyStats = "\n--------------------\n|Name: " + enemy['name'].title() + "|\n|Health: " + str(
        enemy['health']) + "/" + str(enemy['maxhealth']) + "|\n--------------------\n"
    print(enemyStats)

## GAMEPLAY

## combat

# the enemy deals damage
def enemyDamage(enemy):
    damage = random.randint(enemy['weapon'].get('healthtouse'), enemy['weapon'].get('staminatouse'))
    
    if test == True:
        print("DEBUG: Enemy Damage is " + str(damage))
    
    print("You take " + str(damage) + " damage!")
    decreaseHealth(damage)

# calculate the player's damage amount.
def calcPlayerDamage(additionalmultiplier):
    global doesPlayerHaveGoldCoinPowers
    global lowStaminaDamageReductionMultiplier, emptyStaminaDamageReductionMultiplier
    global minStaminaToGetLowDamage

    if test == True:
        print("DEBUG: Calculating player damage...")

    damage = item_sword['healthtouse']

    # Change damage depending on how much stamina we have or how many coins we have.
    if playerStamina > 0:
        if playerStamina <= minStaminaToGetLowDamage:
            damage = damage * additionalmultiplier * lowStaminaDamageReductionMultiplier
        elif playerStamina > minStaminaToGetLowDamage:
            damage = damage * additionalmultiplier
    elif playerStamina <= 0:
        damage = damage * additionalmultiplier * emptyStaminaDamageReductionMultiplier

    if test == True:
        print("DEBUG: Player Damage is " + str(damage))

    return damage

# the player deals damage
def playerDamage(enemy):
    global playerStamina
    global goldCoinStrengthMultiplier

    if test == True:
        print("DEBUG: Player gives damage.")

    # ONE LINE IF STATEMENTS AAAAA (https://www.pythoncentral.io/one-line-if-statement-in-python-ternary-conditional-operator/)
    # if we are able to give damage, do so.
    damage = calcPlayerDamage(
        goldCoinStrengthMultiplier if doesPlayerHaveGoldCoinPowers == True else 1)

    if playerStamina > 0:
        print("You attack with " + str(damage) +
              " damage from your " + item_sword['name'].replace("their ", "") + "!")
    elif playerStamina <= 0:
        print("You struggle to attack the " + enemy['name'] + ", but you are completely out of breath.\nYou attack the " +
              enemy['name'] + " with only " + str(damage) + " damage from your " + item_sword['name'].replace("their ", "") + ".")

    enemy['health'] -= damage

# the player's attack
def attackEnemy(clonecombatenemy, minimum, maximum, definiteAttack):
    global staminaToReduceWhenAttacking, staminaToReduceWhenMissingAttack

    # if we are able to attack, do so.
    attackval = random.randint(minimum, maximum)

    attacksuccesstext = "You attack the " + clonecombatenemy['name'] + "!"

    attackenemydodgetext = "You try to attack the " + clonecombatenemy['name'] + \
    ", but the " + clonecombatenemy['name'] + " dodges your attack!"

    attackenemyattackstext = "You try to attack the " + clonecombatenemy['name'] + \
    ", but the " + clonecombatenemy['name'] + " attacks you first with " + clonecombatenemy['weapon'].get('name') + "!" + \
    ("\n" + clonecombatenemy['weapon'].get('desc') if clonecombatenemy['weapon'].get('desc') != "none" else "")

    """
    definite attacks are attacks where the enemy has a lower chance of attacking you back.
    mainly: dodge + attack for lower ranking enemies, and block + attack for higher ranking enemies.
    """
    
    if definiteAttack == False:
        if test == True:
            print("DEBUG: Attack is indefinite...")
        if (attackval > minimum) and (attackval < maximum):
            if test == True:
                print("DEBUG: Player attacks")
            print(attacksuccesstext)
            reduceStamina(staminaToReduceWhenAttacking)
            playerDamage(clonecombatenemy)
        elif attackval == maximum:
            if test == True:
                print("DEBUG: Enemy attacks")
            print(attackenemyattackstext)
            enemyDamage(clonecombatenemy)
        elif attackval == minimum:
            if test == True:
                print("DEBUG: Enemy dodges")
            print(attackenemydodgetext)
            reduceStamina(staminaToReduceWhenMissingAttack)
    elif definiteAttack == True:
        if test == True:
            print("DEBUG: Attack is definite...")
        if attackval > minimum:
            if test == True:
                print("DEBUG: Player attacks")
            print(attacksuccesstext)
            reduceStamina(staminaToReduceWhenAttacking)
            playerDamage(clonecombatenemy)
        elif attackval == minimum:
            if test == True:
                print("DEBUG: Enemy dodges")
            print(attackenemydodgetext)
            reduceStamina(staminaToReduceWhenMissingAttack)

# the player's shield block
def blockEnemy(clonecombatenemy, minimum, maximum):
    # if we are able to block, do so.

    blocksuccesstext = "You block the " + clonecombatenemy['name'] + "'s attack!"
    
    blockenemyattacktext = "You try to block the " + clonecombatenemy['name'] + \
    "'s attack, but the " + clonecombatenemy['name'] + " attacks you first with " + clonecombatenemy['weapon'].get('name') + "!" + \
    ("\n" + clonecombatenemy['weapon'].get('desc') if clonecombatenemy['weapon'].get('desc') != "none" else "")

    blockval = random.randint(minimum, maximum)
    
    if blockval > minimum:
        if test == True:
            print("DEBUG: Blocking enemy...")
        print(blocksuccesstext)
        return True
    elif blockval == minimum:
        if test == True:
            print("DEBUG: Enemy attacks while blocking...")
        print(blockenemyattacktext)
        enemyDamage(clonecombatenemy)
        return False

# the player's dodge
def dodgeEnemy(clonecombatenemy, minimum, maximum):
    global staminaToReduceWhenDodging

    successtext = "You dodge away from the " + \
        clonecombatenemy['name'] + "!"
    enemyattackstext = "You try to dodge from the " + \
        clonecombatenemy['name'] + ", but the " + \
        clonecombatenemy['name'] + " attacks you with " + clonecombatenemy['weapon'].get('name') + "! " + \
        ("\n" + clonecombatenemy['weapon'].get('desc') if clonecombatenemy['weapon'].get('desc') != "none" else "")

    dodgeval = random.randint(minimum, maximum)

    # if we are able to dodge, do so.
    if dodgeval > minimum:
        if test == True:
            print("DEBUG: Dodging enemy...")
        print(successtext)
        reduceStamina(staminaToReduceWhenDodging)
        return True
    elif dodgeval == minimum:
        if test == True:
            print("DEBUG: Enemy attacks while dodging...")
        print(enemyattackstext)
        enemyDamage(clonecombatenemy)
        return False

# check if we are able to get a definite attack.
def checkDefiniteAttack(enemy, hasDodged, hasBlocked):
    global minToughEnemyHP

    if enemy['maxhealth'] > minToughEnemyHP:
        if hasBlocked == True:
            if test == True:
                print("DEBUG: Tough Enemy: Definite attack...")
            return True
        elif hasBlocked == False:
            if test == True:
                print("DEBUG: Tough Enemy: Indefinite attack...")
            return False
    elif enemy['maxhealth'] <= minToughEnemyHP:
        if hasDodged == True:
            if test == True:
                print("DEBUG: Enemy: Definite attack...")
            return True
        elif hasDodged == False:
            if test == True:
                print("DEBUG: Enemy: Indefinite attack...")
            return False

# Combat
def combat(enemy, hasDodged, hasBlocked):
    global playerName
    global playerStamina
    global mindodge, maxdodge
    global minattack, maxattack
    global minattack_afterdodge, maxattack_afterdodge
    global command_combat_attack, command_combat_dodge, command_combat_block
    global minToughEnemyHP
    global mindodge_toughenemy, maxdodge_toughenemy
    global minattack_afterdodge_toughenemy, maxattack_afterdodge_toughenemy
    global minattack_afterblock_toughenemy, maxattack_afterblock_toughenemy
    global minblock, maxblock
    global minblock_toughenemy, maxblock_toughenemy
    global gamestate, currEnemy, attacking, dodging, blocking

    # This is so we know we dodged from an enemy.
    dodged = False

    # same thing here but it's for blocking.
    blocked = hasBlocked

    if test == True:
        print("DEBUG: Has Dodged: " + str(hasDodged))
        print("DEBUG: Has Blocked: " + str(hasBlocked))

    # set up a fake clone enemy with enemy combat stats
    clonecombatenemy = {
        'name': enemy['name'],
        'weapon': enemy['weapon'],
        'health': enemy['health'],
        "maxhealth": enemy['maxhealth'],
        'rarity': enemy['rarity']}

    # get user input
    choice = getParserForGameState()

    mina = minattack
    maxa = maxattack
    mind = mindodge
    maxd = maxdodge
    minb = minblock
    maxb = maxblock
    
    if hasDodged == True:
        if clonecombatenemy['health'] <= minToughEnemyHP:
            # increase attack chances for the player when dodging low ranking enemies
            minatt = minattack_afterdodge
            maxatt = maxattack_afterdodge
        elif clonecombatenemy['health'] > minToughEnemyHP:
            # decrease attack chances when dodging high ranking enemies.
            minatt = minattack_afterdodge_toughenemy
            maxatt = maxattack_afterdodge_toughenemy
    elif hasDodged == False:
        # override attack values for blocked tough enemies
        if hasBlocked == True:
            minatt = minattack_afterblock_toughenemy
            maxatt = maxattack_afterblock_toughenemy

    if clonecombatenemy['health'] > minToughEnemyHP:
        # increase attack chances for high ranking enemies when the player is dodging
        mind = mindodge_toughenemy
        maxd = maxdodge_toughenemy
        minb = minblock_toughenemy
        maxb = maxblock_toughenemy

    # get commands
    commands = getCommandsForGameState()

    # check if we are putting in a valid command.
    if choice in commands:
        if choice in command_combat_attack:
            print("\n" + playerName + " begins to attack!")
            attackEnemy(clonecombatenemy, mina, maxa, checkDefiniteAttack(clonecombatenemy, hasDodged, hasBlocked))
            if hasBlocked == True:
                blocked = False
        elif choice in command_combat_dodge:
            print("\n" + playerName + " begins to dodge!")
            dodged = dodgeEnemy(clonecombatenemy, mindodge, maxdodge)
        elif choice in command_combat_block:
            if hasBlocked == False: 
                print("\n" + playerName + " raises " + item_shield['name'] + "!")
                blocked = blockEnemy(clonecombatenemy, minb, maxb)
            elif hasBlocked == True:
                print("\nYou must attack again, and then block!")
                blocked = True
    elif choice not in commands:
        if test == True:
            print("DEBUG: Inavlid command...")
        print("\nYou cannot do that.")

    # attack is only initial
    currEnemy = clonecombatenemy
    attacking = False
    dodging = dodged
    blocking = blocked
    gamestate = 2

    if test == True:
        print("DEBUG: Enemy: " + str(clonecombatenemy))

## navigation/exploration
    
# when we first encounter an enemy
def firstEnemyEncounter(enemy):
    global staminaToReduceWhileRunning
    global command_encounter_fight, command_encounter_run
    global minEnemyAttacksPlayer, maxEnemyAttacksPlayer
    global minToughEnemyAttacksPlayer, maxToughEnemyAttacksPlayer, minToughEnemyHP
    global playerLocation
    global playerHealth
    global runYSteps
    global runXStepsMin, runXStepsMax
    global runXmin, runXmax
    global maxXsteps
    global runStaminamin, runStaminamax
    global command_difficulty_easy
    global gamestate, currEnemy, attacking, dodging, blocking
    global staminaToAddAfterRunning
    global breathtextrunning

    # get user input
    choice = getParserForGameState()
    commands = getCommandsForGameState()

    # check if we are putting in a valid command.
    if choice in commands:
        if choice in command_encounter_fight:
            # hop into combat
            currEnemy = enemy
            attacking = False
            dodging = False
            blocking = False
            gamestate = 2
        elif choice in command_encounter_run:
            # "ai" for enemy agressiveness.
            minimum = minEnemyAttacksPlayer
            maximum = maxEnemyAttacksPlayer

            if enemy['health'] > minToughEnemyHP:
                minimum = minToughEnemyAttacksPlayer
                maximum = maxToughEnemyAttacksPlayer

            attackval = random.randint(minimum, maximum)
            if attackval == maximum:
                if test == True:
                    print("DEBUG: Enemy is angry...")
                # enemy attacks!
                print("\nYou try to run away from the " +
                      enemy['name'] + ", but they begin to attack!")
                currEnemy = enemy
                attacking = True
                dodging = False
                blocking = False
                gamestate = 2
            elif attackval < maximum:
                # reduce stamina when we run
                if test == True:
                    print("DEBUG: We run away from the enemy.")
                    
                print("\nYou run away from the " +
                      enemy['name'] + ".\n")
                reduceStamina(staminaToReduceWhileRunning)

                if (getDifficulty() == command_difficulty_easy[0]):
                    increaseStamina(staminaToAddAfterRunning)
                    print(breathtextrunning)
                else:
                    regenStamina = random.randint(runStaminamin, runStaminamax)

                    if (regenStamina == runStaminamax):
                        increaseStamina(staminaToAddAfterRunning)
                        print(breathtextrunning)

                # randomly run on both the y and x axis
                playerLocation[1] += runYSteps
                runXsteps = 0
                while runXsteps < maxXsteps:
                    runXval = random.randint(runXmin, runXmax)
                    runXStepsval = random.randint(runXStepsMin, runXStepsMax)
                    
                    if runXval < 0:
                        playerLocation[0] -= runXStepsval
                    elif runXval > 0:
                        playerLocation[0] -= runXStepsval
                        
                    runXsteps += 1

                # reset state.
                currEnemy = npc_null
                attacking = False
                dodging = False
                blocking = False
                gamestate = 0
                                
    elif choice not in commands:
        if test == True:
            print("DEBUG: Invalid command...")
        print("\nYou cannot do that.\n")

# move the player around
def move():
    global doesPlayerHaveGoldCoinPowers
    global direction
    global stepsToLair, maxStepsCounter
    global staminaToReduceWhileWalking
    global command_dir_forward, command_dir_left, command_dir_right, command_dir_backward
    global initalspawn, playerLocation

    # Get direction then move in that direction.
    direction = getParserForGameState()
    commands = getCommandsForGameState()
    command_dir_backward
    additionaltext = ""

    # check if we are putting in a valid command.

    # this calls getDirection, which sets our location.
    direct = getDirection()
    
    if direction in commands: 
        isGettingOutofDungeon = False
        if direction in command_dir_forward:
            playerLocation[1] += 1
            additionaltext = "in front of you"
        elif direction in command_dir_backward:
            if playerLocation[1] != 0:
                playerLocation[1] -= 1
                additionaltext = "behind you"
            elif playerLocation[1] == 0:
                additionaltext = ""
                isGettingOutofDungeon = True
        elif direction in command_dir_left:
            playerLocation[0] +=1
            additionaltext = "on the " + direct
        elif direction in command_dir_right:
            playerLocation[0] -= 1
            additionaltext = "on the " + direct

        if isGettingOutofDungeon == False:
            if test == True:
                print("DEBUG: Moving player...")
            print("\nYou go though the nearest hallway " + additionaltext + ".\n")

            reduceStamina(staminaToReduceWhileWalking)

            if doesPlayerHaveGoldCoinPowers == True:
                stepsToLair += 1
                maxStepsCounter -= 1

            # random encounters! this is where we can spawn an enemy or item! We can also find random locations and rooms.
            encounter()
        elif isGettingOutofDungeon == True:
            if test == True:
                print("DEBUG: Player is trying to escape!")
            print("\nYou cannot get out of the dungeon...\n")
    elif direction not in commands:
        if test == True:
            print("DEBUG: Invalid command...")
        print("\nYou cannot go that way.\n")

    if test == True:
        print("DEBUG: Player Position: " + str(playerLocation))

# random encounters
def encounter():
    global doesPlayerHaveGoldCoinPowers
    global stepsToLair, maxStepsToLair
    global gamestate, currEnemy, attacking, dodging, blocking
    global test

    if doesPlayerHaveGoldCoinPowers == False:
        # play the game as normal.
        encounterLogic()
    elif doesPlayerHaveGoldCoinPowers == True:
        """
        if we have the golden coins, the game will lead us to the boss's lair. arrive there when we have all the steps.
        else, just continue the game as normal.
        """
        if stepsToLair == maxStepsToLair:
            if test == True:
                print("DEBUG: Boss battle generated...")
            # begin boss battle.
            location = room_finalboss
            print("You arrive at " + location['name'] +
                  ".\n" + location['desc'])
            enemy = npc_boss
            # capitalize all words in enemy name. (https://www.tutorialspoint.com/python/string_title.htm)
            print("You encounter the " + enemy['name'].title() + "!")
            currEnemy = enemy
            attacking = False
            dodging = False
            blocking = False
            gamestate = 2
            if test == True:
                print("DEBUG: Location: " + str(location))
                print("DEBUG: Location: " + str(enemy))
        elif stepsToLair != maxStepsToLair:
            # play the game as normal.
            encounterLogic()

# check if the encounter is valid.
def checkValidEncounter():
    global minStepsToDiscover
    global playerLocation
    
    if (playerLocation[0] >= minStepsToDiscover) or (playerLocation[0] <= -minStepsToDiscover) or (playerLocation[1] >= minStepsToDiscover) or (playerLocation[1] <= -minStepsToDiscover):
        if test == True:
            print("DEBUG: Planned encounter is valid.\nDEBUG: We can spawn an enemy, item or location now.")
        return True
    else:
        if test == True:
            print("DEBUG: Planned encounter is invalid.\nDEBUG: We cannot spawn an enemy, item or location at this moment.")
        return False

# logic for spawning 2 enemies at once.
def dualEnemies(enemy):
    global enemyMinRarity, enemyMaxRarity
    global minduel, maxduel
    global test

    if test == True:
        print("DEBUG: 2 enemies were generated...")
        
    enemyrarity2 = random.randint(enemyMinRarity, enemyMaxRarity)
    enemy2 = random.choice(enemypool)

    # bypass the rarity if we are in test mode
    if test == True:
        print("DEBUG: Using test mode bypass for 2 enemies...")
        testvar = random.randint(minduel, maxduel)
        if testvar == maxduel:
            print("DEBUG: Bypass successful...")
            enemy2['rarity'] = enemyrarity2
        elif testvar != maxduel:
            print("DEBUG: Bypass unsuccessful...")

    if enemy2['rarity'] == enemyrarity2:
        enemyweapon2 = {
            # https://www.tutorialspoint.com/python/string_replace.htm
            'name': "the " + enemy['name'] + "'s " + enemy['weapon'].get('name').replace("their ", "") + " + " + enemy2['name'] + "'s " + enemy2['weapon'].get('name').replace("their ", ""),
            'desc': enemy['weapon'].get('desc').replace("The enemy", "The first enemy") + " " + enemy2['weapon'].get('desc').replace("The enemy", "The second enemy"),
            'healthtouse': int(enemy['weapon'].get('healthtouse') if enemy['weapon'].get('healthtouse') < enemy2['weapon'].get('healthtouse') else enemy2['weapon'].get('healthtouse')),
            'staminatouse': int(enemy2['weapon'].get('staminatouse') if enemy2['weapon'].get('staminatouse') > enemy['weapon'].get('staminatouse') else enemy['weapon'].get('staminatouse')),
            "rarity": enemy['weapon'].get('rarity'),
            'isgold': enemy['weapon'].get('isgold'),
            'istrap': enemy['weapon'].get('istrap')}

        enemy22 = {
            'name': enemy['name'] + " + " + enemy2['name'],
            'weapon': enemyweapon2,
            'health': int(enemy['health'] + enemy2['health']),
            "maxhealth": int(enemy['maxhealth'] + enemy2['maxhealth']),
            'rarity': enemy['rarity']}
        
        if test == True:
            print("DEBUG: Successful generation...")

        return enemy22
    elif enemy2['rarity'] != enemyrarity2:
        if test == True:
            print("DEBUG: Unsuccessful generation...")

        return enemy

def encounterLogic():
    global playerStamina, maxPlayerStamina
    global playerHealth, maxPlayerHealth
    global playerGold, doesPlayerHaveGoldCoinPowers, goldCoinsNeeded, maxPlayerHealthAfterCoins, goldCoinStrengthMultiplier
    global direction
    global stepsToLair, maxStepsToLair
    global locationMinRarity, locationMaxRarity
    global enemyMinRarity, enemyMaxRarity
    global itemMinRarity, itemMaxRarity
    global minduel, maxduel
    global gamestate, currEnemy, attacking, dodging, blocking
    global test

    if test == True:
        print("DEBUG: Generating new encounter...")

    # don't discover anything if we are at initial spawn or if the encounter isn't valid.
    if playerLocation != [0,0] and checkValidEncounter():
        # grab a random location?
        locationrarity = random.randint(locationMinRarity, locationMaxRarity)
        location = random.choice(locationpool)

        if location['rarity'] == locationrarity:
            if test == True:
                print("DEBUG: New location generated...")
                print("DEBUG: Location: " + str(location))
            print("You arrive at " + location['name'] +
                  ".\n" + location['desc'])

        # spawn an enemy?
        enemyrarity = random.randint(enemyMinRarity, enemyMaxRarity)
        enemy = random.choice(enemypool)

        if enemy['rarity'] == enemyrarity:
            if test == True:
                print("DEBUG: New enemy generated...")
            duel = random.randint(minduel, maxduel)

            if duel == maxduel:
               enemy2 = dualEnemies(enemy)
               if test == True:
                    print("DEBUG: Enemy is a " + enemy2['name'].title())
                    print("DEBUG: Enemy: " + str(enemy2))
               print("You encounter a " + enemy2['name'] + "!\n")
               currEnemy = enemy2
            elif duel != maxduel:
               if test == True:
                    print("DEBUG: Enemy is a " + enemy['name'].title())
                    print("DEBUG: Enemy: " + str(enemy))
               print("You encounter a " + enemy['name'] + "!\n")
               currEnemy = enemy

            attacking = False
            dodging = False
            blocking = False
            gamestate = 1
        elif enemy['rarity'] != enemyrarity:
            # spawn an item if there are no enemies?
            itemrarity = random.randint(itemMinRarity, itemMaxRarity)
            item = random.choice(itempool)
            itemstring = "You found " + \
                item['name'] + "!\n" + item['desc']
            itemleavestring = "You found " + \
                item['name'] + \
                "!\nYou don't need it right now, so you leave it aside.\n"

            if item['rarity'] == itemrarity:
                if test == True:
                    print("DEBUG: New item generated...")
                    print("DEBUG: Item: " + str(item))
                
                itemprefix = "" + "-" if item['istrap'] == True else "+" + ""

                itemhealthstring = itemprefix + str(item['healthtouse']) + " Health"
                itemstaminastring = itemprefix + str(item['staminatouse']) + " Stamina"
                
                # give ourselves the gold coin.
                if item['isgold'] == True:
                    if test == True:
                        print("DEBUG: Item is gold")
                    if (playerGold < maxGoldCoinsToWin) and (doesPlayerHaveGoldCoinPowers == False):
                        print(itemstring + "\n+" + str(minGoldCoinsToGive) + " Gold Coins\n")
                        playerGold += minGoldCoinsToGive

                        if playerGold >= maxGoldCoinsToWin:
                            playerGold = maxGoldCoinsToWin
                            doesPlayerHaveGoldCoinPowers = True
                            maxPlayerHealth = maxPlayerHealthAfterCoins
                            increaseHealth(item['healthtouse'])
                            cointext = """You found all the golden coins!
You suddenly feel stronger than ever before...
The coins lead you towards a room deep in the dungeon!

""" + itemhealthstring + """
Your """ + item_sword['name'].replace("their ", "") + """ damage increases to """ + str(item_sword['healthtouse'] * goldCoinStrengthMultiplier) + """!
Your maximum health is now """ + str(maxPlayerHealth) + """! 
"""
                            print(cointext)
                        elif playerGold < maxGoldCoinsToWin:
                            goldCoinsNeeded -= 1
                            if goldCoinsNeeded == 1:
                                print("You still need " +
                                      str(goldCoinsNeeded) + " gold coin.\n")
                            elif goldCoinsNeeded > 1:
                                print("You still need " +
                                      str(goldCoinsNeeded) + " gold coins.\n")
                elif item['isgold'] == False:
                    # if this item isn't a trap, use it.
                    if item['istrap'] == False:
                        if test == True:
                            print("DEBUG: Item is not a trap")
                        # for items with both health and stamina, check those first
                        if item['healthtouse'] > 0 and item['staminatouse'] > 0:
                            if (playerHealth < maxPlayerHealth and playerStamina < maxPlayerStamina) or playerHealth < maxPlayerHealth or playerStamina < maxPlayerStamina:
                                print(itemstring + "\n" + itemhealthstring + "\n" + itemstaminastring + "\n")
                                increaseHealth(item['healthtouse'])
                                increaseStamina(item['staminatouse'])
                            elif (playerHealth >= maxPlayerHealth and playerStamina >= maxPlayerStamina):
                                print(itemleavestring)
                        else:
                            # heal ourselves if we use a medkit.
                            if item['healthtouse'] > 0:
                                if playerHealth < maxPlayerHealth:
                                    print(itemstring + "\n" + itemhealthstring + "\n")
                                    increaseHealth(item['healthtouse'])
                                elif playerHealth >= maxPlayerHealth:
                                    print(itemleavestring)

                            # refresh ourselves with water.
                            if item['staminatouse'] > 0:
                                if playerStamina < maxPlayerStamina:
                                    print(itemstring + "\n" + itemstaminastring + "\n")
                                    increaseStamina(item['staminatouse'])
                                elif playerStamina >= maxPlayerStamina:
                                    print(itemleavestring)
                    # if the item is a trap, damage us
                    elif item['istrap'] == True:
                        if test == True:
                            print("DEBUG: Item is trap")
                        # for items with both health and stamina, check those first
                        if item['healthtouse'] > 0 and item['staminatouse'] > 0:
                            print(itemstring + "\n" + itemhealthstring + "\n" + itemstaminastring + "\n")
                            decreaseHealth(item['healthtouse'])
                            reduceStamina(item['staminatouse'])
                        else:
                            # damage us.
                            if item['healthtouse'] > 0:
                                print(itemstring + "\n" + itemhealthstring + "\n")
                                decreaseHealth(item['healthtouse'])

                            # make us more tired.
                            if item['staminatouse'] > 0:
                                print(itemstring + "\n" + itemstaminastring + "\n")
                                reduceStamina(item['staminatouse'])

## game logic

def gameStart():
    global gametitle, gameversion, gamecodename
    global gamestate

    if test == True:
        print("DEBUG: Generating intro screen...")

    # fancy title (https://www.tutorialspoint.com/python/python_strings.htm)
    fancytitle = ' '.join(gametitle).upper()

    print(fancytitle + "\n" + gameversion +
          "\nCodename: " + gamecodename, end='\n\n')

    # tell the player to set difficulty.
    gamestate = -3

def difficultySelect():
    global command_difficulty_easy, command_difficulty_normal, command_difficulty_hard
    global difficulty
    global command_bootup_yes, command_bootup_no
    global gamestate

    # ask if the player wants to begin
    difficulty = getParserForGameState()
    commands = getCommandsForGameState()

    if difficulty in commands:
        if test == False:
            print("\nThe difficulty has been set to " + getDifficulty().title() + ".")
            adjustDifficulty()
            gamestate = -2
        elif test == True:
            if difficulty in command_difficulty_easy:
                print("\nThe difficulty has been set to " + getDifficulty().title() + ".")
                adjustDifficulty()
                gamestate = -2
            else:
                print("\nThat isn't an option. Test mode is enabled, so some difficulty levels are disabled.\n")
                gamestate = -3 
    elif difficulty not in commands:
        if test == True:
            print("DEBUG: Invalid command...")
        print("\nThat isn't an option.\n")
        gamestate = -3

def namePlayer():
    global playerName
    global minNameLength
    global gamestate

    # we need the player name for the intro sequence.
    playerName = getParserForGameState()

    if test == True:
        print("DEBUG: Player name is " + playerName)

    # check player name length.
    if len(playerName) >= minNameLength:
        if test == True:
            print("DEBUG: Valid name...")
        gamestate = -1
    elif len(playerName) < minNameLength and len(playerName) > 0:
        if test == True:
            print("DEBUG: Short name...")
        print("\nYour name is too short. Try again.\n")
        gamestate = -2
    elif len(playerName) <= 0:
        if test == True:
            print("DEBUG: No name...")
        print("\nYou must provide a name to continue. Try again.\n")
        gamestate = -2


def storyPrologue(isFixingMistake):
    global playerName
    global goldCoinsNeeded
    global command_bootup_yes, command_bootup_no
    global gamestate
    global starttext, proceedtext, gohometext

    if test == True:
        print("DEBUG: Showing story...")

    if isFixingMistake == False:
        # print the start text
        print(starttext)
    elif isFixingMistake == True:
        if test == True:
            print("DEBUG: We are fixing a mistake...")

    # ask if the player wants to begin
    proceed = getParserForGameState()
    commands = getCommandsForGameState()
    if proceed in commands:
        if proceed in command_bootup_yes:
            if test == True:
                print("DEBUG: Begin game...")
            print(proceedtext)
            gamestate = 0
        elif proceed in command_bootup_no:
            if test == True:
                print("DEBUG: Leave game...")
            print(gohometext)
            stop()
    elif proceed not in commands:
        if test == True:
            print("DEBUG: Invalid command...")
        print("\nThat isn't an option.\n")
        storyPrologue(True)

def triggerCombat():
    global playerHealth
    global currEnemy, attacking, dodging, blocking

    enemyattacktext = "\nThe " + currEnemy['name'] + " strikes you down with " + \
        currEnemy['weapon'].get('name') + " while you were trying to escape!" + \
        ("\n" + currEnemy['weapon'].get('desc') if currEnemy['weapon'].get('desc') != "none" else "")

    if attacking == True:
        print(enemyattacktext)
        enemyDamage(currEnemy)

    if playerHealth > 0:
        enemyStats(currEnemy)
        playerStats()
        combat(currEnemy, dodging, blocking)

## simple function that pauses the dialog then exits.
def stop():
    input("\nPress any key to exit...")
    exit()

## GAME LOOP

while playerHealth > 0:
    if test == True:
        print("DEBUG: Player is alive")
        print("DEBUG: Gamestate is " + str(gamestate))

    # update text and objects
    updateText()
    updateObjects()

    # -4: start the game
    if gamestate == -4:
        gameStart()
    #-3: difficulty select
    elif gamestate == -3:
        difficultySelect()
    #-2: name change
    elif gamestate == -2:
        namePlayer()
    #-1: story
    elif gamestate == -1:
        storyPrologue(False)
    #0: exploring
    elif gamestate == 0:
        playerStats()
        move()
    #1: enemy encounter
    elif gamestate == 1:
        playerStats()
        firstEnemyEncounter(currEnemy)
    #2: combat
    elif gamestate == 2:
        """
if we have over 0 health, continue combat loop if the enemy is alive. also sisplay stats
if we win the battle, regenerate some of the stamina and display win text.
if we have 0 or lower health, lock the health at 0, display stats, then display the death text.
        """
        if currEnemy['health'] <= 0:
            if test == True:
                print("DEBUG: Player is no longer in combat. Enemy is dead.")
            currEnemy['health'] = 0
            # give us more stamina if we are under minimum stamina!
            # also, heal us if we are under the minimum health
            if currEnemy['name'] != npc_boss['name']:
                if test == True:
                    print("DEBUG: Enemy is not boss...\nDEBUG: Display normal text...\nDEBUG: Updating player stats...")
                if playerStamina < minStaminaToGetLowDamage:
                    increaseStamina(bonusstamina)
                    print(wintext + breathtextalt)
                elif (playerStamina == minStaminaToGetLowDamage) or (playerStamina > minStaminaToGetLowDamage):
                    increaseStamina(staminaToRegenAfterCombat)
                    print(wintext + breathtext)
                    
                if playerHealth <= minHealthForLowHealth:
                    increaseHealth(healthToRegenAfterCombat)
                    print(refillhealthtext)

                # reset state
                currEnemy = npc_null
                attacking = False
                dodging = False
                blocking = False
                gamestate = 0
            elif currEnemy['name'] == npc_boss['name']:
                if test == True:
                    print("DEBUG: Enemy is boss...\nDEBUG: Display win text...")
                # reset state and display ending
                currEnemy = npc_null
                attacking = False
                dodging = False
                blocking = False
                gamestate = 0
                playerStats()
                print(wintext_boss)
                stop()
        elif currEnemy['health'] > 0:
                if test == True:
                    print("DEBUG: Player is in combat")
                # continue combat loop
                triggerCombat()

# player death event        
if playerHealth <= 0:
    if test == True:
        print("DEBUG: Player death event")
    
    if gamestate == 2:
        minr = minRevive
        maxr = maxRevive

        #higher chance to revive if we are fighting a tough enemy.
        if currEnemy['health'] > minToughEnemyHP:
            minr = minRevive_toughenemy
            maxr = maxRevive_toughenemy

        #revive the player?
        reviveval = random.randint(minr, maxr)
        if reviveval == maxRevive:
            if test == True:
                print("DEBUG: Combat: Player revived")
            print(combatrevivetext)
            setHealth(maxPlayerHealth)
            setStamina(maxPlayerStamina)
            triggerCombat()
        elif reviveval != maxRevive:
            if test == True:
                print("DEBUG: Combat: Player dead")
            enemyStats(currEnemy)
            playerStats()
            print(deadtext)
            stop()
    elif gamestate == 0:
        #revive the player?
        reviveval = random.randint(minRevive, maxRevive)
        if reviveval == maxRevive:
            if test == True:
                print("DEBUG: Idle: Player revived")
            print(revivetext)
            setHealth(maxPlayerHealth)
            setStamina(maxPlayerStamina)
            playerStats()
            move()
        elif reviveval != maxRevive:
            if test == True:
                print("DEBUG: Idle: Player dead")
            playerStats()
            print(deadtextdungeon)
            stop()
