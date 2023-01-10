import json, pygame

LevelName = input("Enter name: ")
MAX_SIZE = -200


pygame.init()

Display = pygame.display.set_mode((800, 800))

running = True

pygame.display.set_caption("Level - " + LevelName)

Xshift = 0
ScrollSpeed = 0.1

GridSize = 10

while running:
    mousePos = pygame.mouse.get_pos()
    GridPos = ((round((mousePos[0])/GridSize) * GridSize), round(mousePos[1]/GridSize) * GridSize)
    
    
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_LEFT]:
        if Xshift < 0:
            Xshift += ScrollSpeed
    if keyPressed[pygame.K_RIGHT]:
        if Xshift > MAX_SIZE:
            Xshift -= ScrollSpeed
    #Draw
    Display.fill((0, 0, 0))
    pygame.draw.rect(Display, (255, 255, 255), pygame.Rect(GridPos[0], GridPos[1], GridSize, GridSize))
    
    pygame.draw.rect(Display, (255, 255, 255), pygame.Rect(200 + Xshift, 0, GridSize, GridSize))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
