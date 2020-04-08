import pygame
import random

# initialization
pygame.init()

# initialize some variables

screen_width = 800
screen_height = 600

# create screen
screen = pygame.display.set_mode((screen_width, screen_height))

# background image
bg_image = pygame.image.load("back_ground_image.png")

# Title and Icon
pygame.display.set_caption("Space Mission")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player attributes
player_image = pygame.image.load("player.png")
player_x_axis = (screen_width // 2) - 64
player_y_axis = screen_height - 100
player_x_axis_change = 0

# enemy attributes
enemy_image = pygame.image.load("enemy_1.png")
enemy_x_axis = random.randint(0, 800 - 64)
enemy_y_axis = random.randint(0, 150)
enemy_x_axis_change = 1
enemy_y_axis_change = 40


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y):
    screen.blit(enemy_image, (x, y))


# main while loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg_image, (0, 0))
    # player_x_axis += 0.1
    # if player_x_axis > 800:
    #     player_x_axis = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_x_axis_change = 3
            if event.key == pygame.K_LEFT:
                player_x_axis_change = -3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_axis_change = 0

    player_x_axis += player_x_axis_change

    if player_x_axis >= screen_width - 64:
        player_x_axis = screen_width - 64
    elif player_x_axis <= 0:
        player_x_axis = 0

    enemy_x_axis += enemy_x_axis_change

    if enemy_x_axis >= screen_width - 64:
        enemy_x_axis_change = -1
        enemy_y_axis += enemy_y_axis_change
    elif enemy_x_axis <= 0:
        enemy_x_axis_change = 1
        enemy_y_axis += enemy_y_axis_change
    enemy(enemy_x_axis, enemy_y_axis)
    player(player_x_axis, player_y_axis)

    pygame.display.update()
