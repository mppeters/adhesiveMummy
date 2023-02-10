import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set the size of the window
size = (800, 800)

# Create a window with the specified size and title
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Adhesive Mummy")

#  load in images
bg_img = pygame.image.load('background.png')

# set the tile sizes for each game tile
tile_size = 40

# camera class

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2() # adjust for offset
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # ground
        self.ground_surf = pygame.image.load('background.png').convert_alpha() # CURRENT IMG IS PLACEHOLDER FOR WORLD
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player):

        self.center_target_camera(player)

        # ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)


# player class


class player():
    def __init__(self, x, y):
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img, (300, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False

    # updates the player data for movement and

    def update(self):
        # change in x and change in y variables
        dx = 0
        dy = 0

        # checking to see if a key is pressed and moving in that direction if so
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -5
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 2
        if key[pygame.K_RIGHT]:
            dx += 2

        # add gravity to the player jumps
        self.vel_y += 0.05
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # player movement
        self.rect.x += dx
        self.rect.y += dy

        # test code to make sure the movement works while there is no collision effects
        if self.rect.bottom > 800:
            self.rect.bottom = 800
            dy = 0
        screen.blit(self.image, self.rect)


"""
class hyena():
    def __init__(self, x, y):
        img = pygame.image.load('hyena.png')
        self.image = pygame.transform.scale(img, (300, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.moving_left = True
        self.posX = 0
        self.posY = 0

    # updates hyena data for movement
    def update(self):

        # add gravity to hyena
        self.vel_y += 0.05
        if self.vel_y > 10:
            self.vel_y = 10
        self.posY += self.vel_y

        # hyena movement (paces back and forth)
        if self.posX <= -25:  # hits left boundary
            self.image = pygame.transform.flip(pygame.image.load('hyena.png'), True, False)
            self.posX += self.posX
        elif self.posX >= 25:  # hits right boundary
            self.image = pygame.transform.flip(pygame.image.load('hyena.png'), True, False)
            self.posX -= self.posX
        elif 25 > self.posX > -25 and self.moving_left == True: # moving left
            self.posX -= self.posX
        else: # moving right
            self.posX =+ self.posY

        # jump mechanic (if player is above)
        if self.rect.x + 10 <= player.rect.x <= self.rect.x - 10 and self.rect.y <= player.rect.y and not self.jumped:
            # if within 10 units of player and relatively below
            self.vel_y = -5
            self.jumped = True
        else :
            self.jumped = False

        self.rect.x += self.posX
        self.rect.y += self.posY

        # test code to make sure the movement works while there are no collision effects
        if self.rect.bottom > 800:
            self.rect.bottom = 800
            self.posY = 0
        screen.blit(self.image, self.rect)
"""


# class to create the world
class world():
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load('dirt.png')
        # creating each tile for the game space and assigning it the correct data based on the input data
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(
                        dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    # drawing the world tiles into the world

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


# world data board to hold world data 1 means dirt 0 means air
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# player instance
player = player(100, 640)
# creating a world instance with the world data table
world = world(world_data)
running = True

# setup camera
camera_group = CameraGroup()


# game loop
while running:
    screen.blit(bg_img, (0, 0))

    world.draw()
    player.update()
    """hyena.update()"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    camera_group.update()
    camera_group.custom_draw(player)

    pygame.display.update()
pygame.quit()
