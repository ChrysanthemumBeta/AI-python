import json, pygame, os, Helper

pygame.init()

Display = pygame.display.set_mode((800, 800))
MAX_SIZE = -3000

#Colour Data
Colour = {
    "Stone" : (125, 125, 125),
    "Cloud" : (255, 255, 255),
    "Note Block" : (255, 192, 203),
    "? Block" : (255, 184, 28),
    "Coin" : (253, 218, 22),
    "Red Coin" : (220, 20, 60),
    "Block" : (150, 75, 0),
    "Ground" : (181, 101, 29),
    "Koopa" : (50, 205, 50),
    "Goomba" : (92, 64, 51),
    "Lakitu" : (152, 251, 152),
    "Hidden Block" : (192, 192, 192),
    "Muncher" : (0, 0, 0),
    "Piranha Flower" : (220, 0, 0),
    "Spiny" : (200, 10, 10)
    }

print(len(Colour.keys()))

IsCircle = ["Coin", "Red Coin"]

#Import json file
LevelData = json.load(open("AI Generated\\AI Generated Level.json", "r"))

LevelDataMinified = LevelData

#LevelDataMinified = Helper.Simplify(LevelData)

Xshift = 0
ScrollSpeed = 1

pygame.display.set_caption("Level - " + LevelData["name"])
Names = []

running = True

def DrawTile(tile, Tile):
        if tile["name"] in list(Colour.keys()):
            if tile["name"] not in IsCircle:
                pygame.draw.rect(Display, Colour[tile["name"]], Tile)
            else:
                pygame.draw.circle(Display, Colour[tile["name"]], ((tile["x"] + Xshift) + 7, (800 - tile["y"]) + 7), 7)
        if tile["name"] == "Dotted-Line Block":
            if tile["flag"] == 100663364:
                pygame.draw.rect(Display, (200, 0, 0), Tile)
            else:
                pygame.draw.rect(Display, (0, 0, 200), Tile)

def DrawLevel(data):
    for tile in data:
        Tile = pygame.Rect(tile["x"] + Xshift, 800 - tile["y"], 14, 14)
        DrawTile(tile, Tile)
    pygame.display.update()

while running:
    #Draw
    Display.fill((135, 206, 250))
    DrawLevel(LevelDataMinified["data"])
    #Scroll
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_LEFT]:
        if Xshift < 0:
            Xshift += ScrollSpeed
    if keyPressed[pygame.K_RIGHT]:
        if Xshift > MAX_SIZE:
            Xshift -= ScrollSpeed
    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


