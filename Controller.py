import pygame
from pygame.locals import *
import Game

# addition function to demonstrate Tests
def add(x,y):
    return x + y

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()

# Set the size of the window
size = (800, 800)

# Create a window with the specified size and title
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Adhesive Mummy")

# load in images
bg_img = pygame.image.load('pixelBG.jpg')

# set the tile sizes for each game tile
tile_size = 25

# player instance
player = Game.player(100, 640)
# creating a world instance with the world data table
world = Game.world(Game.world_data)
running = True

# setup camera
camera_group = Game.CameraGroup()

# game loop
while running:
    clock.tick(120)

    camera_group.update()
    camera_group.custom_draw(player)

    world.draw()
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()
             