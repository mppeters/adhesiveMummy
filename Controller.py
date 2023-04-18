"""Game Controller"""
# pylint: disable=line-too-long
import sys
import pygame
import game
from button import Button


pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/BG800x800.jpg")


def get_font(size):  # Returns Press-Start-2P in the desired size
    """Gets the font for the menu"""
    return pygame.font.Font("assets/silkscreenFont.ttf", size)


def play():
    """Plays the game"""
    pygame.display.set_caption("Adhesive Mummy")

    player = game.Player(100, 640)
    player.create_world(game.world_levels[0])

    camera_group = game.CameraGroup()
    clock = pygame.time.Clock()

    while True:
        clock.tick(120)

        camera_group.update()
        camera_group.custom_draw(player)
        camera_group.update()
        camera_group.custom_draw(player)

        player.update()

        play_mouse_pos = pygame.mouse.get_pos()

        play_back = Button(image=None, pos=(100, 50),
                           text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")

        play_back.change_color(play_mouse_pos)
        play_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_back.check_for_input(play_mouse_pos):
                    main_menu()

        pygame.display.update()


def level_select():
    """Selects Level"""
    while True:
        levelselect_mouse_pos = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        levelselect_back = Button(image=None, pos=(100, 50),
                                  text_input="BACK", font=get_font(40), base_color="Black", hovering_color="Green")

        levelselect_back.change_color(levelselect_mouse_pos)
        levelselect_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if levelselect_back.check_for_input(levelselect_mouse_pos):
                    main_menu()

        pygame.display.update()


def main_menu():
    """Main Menu for the game"""
    pygame.display.set_caption("Menu")

    while True:
        screen.blit(BG, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(105).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(400, 100))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250),
                             text_input="PLAY", font=get_font(95), base_color="#d7fcd4", hovering_color="White")
        levelselect_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 400),
                                    text_input="LEVEL", font=get_font(95), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 550),
                             text_input="QUIT", font=get_font(95), base_color="#d7fcd4", hovering_color="White")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, levelselect_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                if levelselect_button.check_for_input(menu_mouse_pos):
                    level_select()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
