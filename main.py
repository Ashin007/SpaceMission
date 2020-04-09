import pygame
import random
import math
from pygame import mixer

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

number_of_enemy = 6
enemy_image = []
enemy_x_axis = []
enemy_y_axis = []
enemy_x_axis_change = []
enemy_y_axis_change = []
for i in range(number_of_enemy):
    enemy_image.append(pygame.image.load("enemy_1.png"))
    enemy_x_axis.append(random.randint(0, 800 - 64))
    enemy_y_axis.append(random.randint(0, 150))
    enemy_x_axis_change.append(1)
    enemy_y_axis_change.append(40)

# enemy attributes


# bullet attributes
bullet_image = pygame.image.load("bullet.png")
bullet_x_axis = player_x_axis
bullet_y_axis = 500
bullet_x_axis_change = 0
bullet_y_axis_change = 10
# bullet status -- ready-- not visible to screen
# bullet status -- fire-- visible to screen
bullet_status = "ready"
stop_bullet = "play"

# score attributes
score_value = 0
score_x_axis = 0
score_y_axis = 20
font_score = pygame.font.Font("breakout.otf", 32)
font_game_over = pygame.font.Font("breakout.otf", 65)

# back ground music

bg_sound = mixer.music.load("background_music.mp3")
mixer.music.play(-1)


def display_score(score_axis_x, score_axis_y):
    score = font_score.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (score_axis_x, score_axis_y))


def player(x, y):
    if stop_bullet is not "stop":
        screen.blit(player_image, (x, y))


def enemy(x, y, item):
    screen.blit(enemy_image[item], (x, y))


def fire_bullet(x, y):
    global bullet_status, stop_bullet
    bullet_status = "fire"
    if stop_bullet is not "stop":
        screen.blit(bullet_image, (x + 25, y - 50))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    # Distance between two points
    #         _________________________
    #    D = V p(x2 − x1)2 + (y2 − y1)2

    if stop_bullet is not "stop":
        distance = math.sqrt(math.pow((enemy_x - bullet_x), 2) + math.pow((enemy_y - bullet_y), 2))

        if distance < 30:  # enemy image in pixel
            return True
        else:
            return False


def show_game_over():
    score = font_game_over.render("Game Over", True, (255, 0, 0))
    screen.blit(score, (200, 230))


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
            if event.key == pygame.K_SPACE and stop_bullet is not "stop":
                shoot_sound = mixer.Sound("shoot.wav")
                shoot_sound.play()
            # else:
            #     game_over_sound = mixer.Sound("game_over_sound.mp3")
            #     game_over_sound.play()
                if bullet_status == "ready":
                    bullet_x_axis = player_x_axis
                    fire_bullet(bullet_x_axis, bullet_y_axis)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_axis_change = 0

    player_x_axis += player_x_axis_change

    if player_x_axis >= screen_width - 64:
        player_x_axis = screen_width - 64
    elif player_x_axis <= 0:
        player_x_axis = 0

    for i in range(number_of_enemy):
        if enemy_y_axis[i] >= screen_height - 130:
            for j in range(number_of_enemy):
                enemy_y_axis[j] = 2000
                show_game_over()
                stop_bullet = "stop"
            break
        enemy_x_axis[i] += enemy_x_axis_change[i]

        if enemy_x_axis[i] >= screen_width - 64:
            enemy_x_axis_change[i] = -1
            enemy_y_axis[i] += enemy_y_axis_change[i]
        elif enemy_x_axis[i] <= 0:
            enemy_x_axis_change[i] = 1
            enemy_y_axis[i] += enemy_y_axis_change[i]
        is_collision_happen = is_collision(enemy_x_axis[i], enemy_y_axis[i], bullet_x_axis, bullet_y_axis)
        # print(is_collision(enemy_x_axis, enemy_y_axis, bullet_x_axis, bullet_y_axis))
        if is_collision_happen:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bullet_y_axis = 500
            bullet_status = "ready"
            score_value += 1
            enemy_x_axis[i] = random.randint(0, 800 - 64)
            enemy_y_axis[i] = random.randint(0, 150)

        enemy(enemy_x_axis[i], enemy_y_axis[i], i)

    player(player_x_axis, player_y_axis)

    if bullet_y_axis <= 0:
        bullet_status = "ready"
        bullet_y_axis = 500
    if bullet_status == "fire":
        bullet_y_axis -= bullet_y_axis_change
        fire_bullet(bullet_x_axis, bullet_y_axis)
    display_score(score_x_axis, score_y_axis)

    pygame.display.update()
