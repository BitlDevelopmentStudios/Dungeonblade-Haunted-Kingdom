gameState = 0

def explore():
    global gameState
    
    gameState = 1
    print("EXPLORE")

def combat():
    global gameState
    
    gameState = 2
    print("COMBAT")

def encounter():
    global gameState
    
    gameState = 0
    print("ENCOUNTER")

while True:
    test = input("GAMESTATE: 0, 1, 2: ")

    if gameState == 0:
        explore()
    elif gameState == 1:
        combat()
    elif gameState == 2:
        encounter()
