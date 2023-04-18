import pygame

tile_size = 25
screen = pygame.display.set_mode((800, 800))

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2() # adjust for offset
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # ground
        self.ground_surf = pygame.image.load('assets/pixelBG.jpg').convert_alpha() # CURRENT IMG IS PLACEHOLDER FOR WORLD
        self.ground_rect = self.ground_surf.get_rect(topleft=(-350, 50))

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
        self.img = pygame.image.load('player-sprites/player.png')
        self.image = pygame.transform.scale(self.img, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.vel_x = 0
        self.jumped = False
        self.in_air = False
        self.frames_rendered = 0
        self.walkingLeft = False
        self.last_update_time = 0
        self.current_frame = 0
        self.tile_list=[]
        # animation sprites for player
        self.player_walk_left = [pygame.transform.scale(pygame.image.load('player-sprites/PlayerL1.png'), (50, 100)),
                            pygame.transform.scale(pygame.image.load('player-sprites/PlayerL2.png'), (50, 100)),
                            pygame.transform.scale(pygame.image.load('player-sprites/PlayerL3.png'), (50, 100)),
                            pygame.transform.scale(pygame.image.load('player-sprites/PlayerL4.png'), (50, 100)),
                            pygame.transform.scale(pygame.image.load('player-sprites/PlayerL5.png'), (50, 100)),
                            pygame.transform.scale(pygame.image.load('player-sprites/PlayerL6.png'), (50, 100))]

        self.player_walk_right = [
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL1.png'), (50, 100)), True,
                                False),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL2.png'), (50, 100)), True,
                                False),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL3.png'), (50, 100)), True,
                                False),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL4.png'), (50, 100)), True,
                                False),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL5.png'), (50, 100)), True,
                                False),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('player-sprites/PlayerL6.png'), (50, 100)), True,
                                False)]

    def createWorld(self,data):
        dirt_img = pygame.image.load('assets/dirt.png')
        grass_img = pygame.image.load('assets/grass.png')
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
        
    def update(self):
        # change in x and change in y variables
        dx = 0
        dy = 0

        # checking to see if a key is pressed and moving in that direction if so
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
            self.vel_y = -3
            self.jumped = True
            self.in_air = True
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
        for tile in self.tile_list:
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
                self.in_air = False
        # player animation

        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update_time

        # update the animation frame based on the elapsed time
        if dx < 0:  # walking left
            self.current_frame = (self.current_frame + elapsed_time // 10) % len(self.player_walk_left)
            self.image = self.player_walk_left[self.current_frame]
        elif dx > 0:  # walking right
            self.current_frame = (self.current_frame + elapsed_time // 10) % len(self.player_walk_right)
            self.image = self.player_walk_right[self.current_frame]

        # player movement
        self.rect.x += dx
        self.rect.y += dy

        # reset the animation frame if the character stops moving
        if dx == 0:
            if self.current_frame != 0:
                self.current_frame = 0
                self.image = self.image
                

        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        self.last_update_time = now
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class hyena():
    def __init__(self, x, y):
        img = pygame.image.load('assets/hyena.png')
        self.image = pygame.transform.scale(img, (100, 50))
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
            self.image = pygame.transform.flip(pygame.image.load('assets/hyena.png'), True, False)
            self.posX += self.posX
        elif self.posX >= 25:  # hits right boundary
            self.image = pygame.transform.flip(pygame.image.load('assets/hyena.png'), True, False)
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

# class to create the world



        

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