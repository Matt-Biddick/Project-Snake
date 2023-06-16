import pygame, sys

# Initialize the pygame module and set tickrate
pygame.init()
screen = pygame.display.set_mode((400, 500))
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(60)
    