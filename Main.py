import pygame
from pygame.locals import *

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
bg_img = pygame.image.load('background.png')

# set the tile sizes for each game tile
tile_size = 25

# animation sprites for player
player_walk_left = [pygame.transform.scale(pygame.image.load('player-sprites/PlayerL1.png'), (25, 50)),
                    pygame.transform.scale(pygame.image.load('player-sprites/PlayerL2.png'), (25, 50)),
                    pygame.transform.scale(pygame.image.load('player-sprites/PlayerL3.png'), (25, 50)),
                    pygame.transform.scale(pygame.image.load('player-sprites/PlayerL4.png'), (25, 50)),
                    pygame.transform.scale(pygame.image.load('player-sprites/PlayerL5.png'), (25, 50)),
                    pygame.transform.scale(pygame.image.load('player-sprites/PlayerL6.png'), (25, 50))]

player_walk_right = [
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL1.png'), (25, 50)), True,
                          False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL2.png'), (25, 50)), True,
                          False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL3.png'), (25, 50)), True,
                          False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL4.png'), (25, 50)), True,
                          False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL5.png'), (25, 50)), True,
                          False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL6.png'), (25, 50)), True,
                          False)]


# player class


class player():
    def __init__(self, x, y):
        self.img = pygame.image.load('player-sprites/player.png')
        self.image = pygame.transform.scale(self.img, (25, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.frames_rendered = 0
        self.walkingLeft = False

    # updates the player data for movement and

    def update(self):
        # change in x and change in y variables
        dx = 0
        dy = 0

        # checking to see if a key is pressed and moving in that direction if so
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -3
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 1
        if key[pygame.K_RIGHT]:
            dx += 1

        # add gravity to the player jumps
        self.vel_y += 0.05
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for player collision
        for tile in world.tile_list:
            # check for collision in X-direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                dx = 0
            # check collision in y-direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                # check if below block
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        # player animation ( 1 step per second ) ( if running in 60fps... )
        if dx < 0:  # walking left
            self.walkingLeft = True
            if 0 <= self.frames_rendered <= 60:
                self.image = player_walk_left[0]
            elif 61 <= self.frames_rendered <= 120:
                self.image = player_walk_left[1]
            elif 121 <= self.frames_rendered <= 180:
                self.image = player_walk_left[2]
            elif 181 <= self.frames_rendered <= 240:
                self.image = player_walk_left[3]
            elif 241 <= self.frames_rendered <= 320:
                self.image = player_walk_left[4]
            elif 321 <= self.frames_rendered <= 380:
                self.image = player_walk_left[5]
                self.frames_rendered = 0  # reset after last step
        elif dx > 0:  # walking right
            self.walkingLeft = False
            if 0 <= self.frames_rendered <= 60:
                self.image = player_walk_right[0]
            elif 61 <= self.frames_rendered <= 120:
                self.image = player_walk_right[1]
            elif 121 <= self.frames_rendered <= 180:
                self.image = player_walk_right[2]
            elif 181 <= self.frames_rendered <= 240:
                self.image = player_walk_right[3]
            elif 241 <= self.frames_rendered <= 320:
                self.image = player_walk_right[4]
            elif 321 <= self.frames_rendered <= 380:
                self.image = player_walk_right[5]
                self.frames_rendered = 0  # reset after last step
        else:  # stationary
            if self.walkingLeft:
                self.image = pygame.transform.scale(self.img, (25, 50))
            else:
                self.image = pygame.transform.flip(pygame.transform.scale(self.img, (25, 50)), True, False)
                self.frames_rendered = 0

        # player movement
        self.rect.x += dx
        self.rect.y += dy

        # test code to make sure the movement works while there is no collision effects
        if self.rect.bottom > 800:
            self.rect.bottom = 800
            dy = 0

        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


# class to create the world


class world():
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load('dirt.png')
        grass_img = pygame.image.load('grass.png')
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
                if tile == 2:
                    img = pygame.transform.scale(
                        grass_img, (tile_size, tile_size))
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
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


# world data board to hold world data 1 means dirt 0 means air
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# player instance
player = player(100, 640)
# creating a world instance with the world data table
world = world(world_data)
running = True

# game loop
while running:
    clock.tick(120)
    screen.blit(bg_img, (0, 0))

    world.draw()
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()
