import pygame
import random
import math
import time
import os

# Initialize Pygame
pygame.init()

# Screen Dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Background
background = pygame.image.load("theam.png")

# Background Music
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)  # Play in a loop

# Title and Icon
pygame.display.set_caption("Spaceship")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("battleship (1).png")
player_x = screen_width // 2 - 32
player_y = screen_height - 120
player_speed = 2
player_x_change = 0

# Enemies
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
initial_num_of_enemies = 6
respawn_time = 5  # 5 seconds respawn time
enemy_respawn_timers = [0] * initial_num_of_enemies

# Bullets
bullet_img = pygame.image.load('bullet_9.png')
bullet_speed = 8
bullets = []

# Enemy Bullets
enemy_bullet_img = pygame.image.load('bullet_9.png')
enemy_bullet_speed = 5
enemy_bullets = []

# Explosion
explosion_img = pygame.image.load('blast.png')
explosions = []

# Score
score_value = 0
high_score = 0
if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
font = pygame.font.Font('freesansbold.ttf', 32)
text_x, text_y = 10, 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
retry_font = pygame.font.Font('freesansbold.ttf', 32)

# Sounds
bullet_sound = pygame.mixer.Sound("laser.wav")
collision_sound = pygame.mixer.Sound("explosion.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
enemy_bullet_sound = pygame.mixer.Sound("enemy_laser.wav")

# Functions
def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    high_score_text = font.render("HIGH SCORE: " + str(high_score), True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(high_score_text, (x, y + 40))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    retry_text = retry_font.render("Press Space to Retry", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    screen.blit(retry_text, (250, 320))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    bullets.append([x, y])
    bullet_sound.play()

def fire_enemy_bullet(x, y):
    enemy_bullets.append([x, y])
    enemy_bullet_sound.play()

def collision_occurance(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

def display_explosion(x, y):
    explosions.append([x, y, time.time()])
    collision_sound.play()

def reset_game():
    global player_x, player_y, player_x_change
    global bullets, enemy_bullets, score_value, initial_num_of_enemies
    global enemy_img, enemy_x, enemy_y, enemy_x_change, enemy_y_change, enemy_respawn_timers
    global explosions, high_score

    player_x = screen_width // 2 - 32
    player_y = screen_height - 120
    player_x_change = 0
    bullets = []
    enemy_bullets = []
    if score_value > high_score:
        with open("high_score.txt", "w") as file:
            file.write(str(score_value))
        high_score = score_value
    score_value = 0
    initial_num_of_enemies = 6
    explosions = []

    enemy_img = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []
    enemy_respawn_timers = [0] * initial_num_of_enemies

    for i in range(initial_num_of_enemies):
        enemy_img.append(pygame.image.load("ufo (2).png"))
        enemy_x.append(random.randint(0, screen_width - 64))
        enemy_y.append(random.randint(50, 100))
        enemy_x_change.append(3)
        enemy_y_change.append(0.09)

reset_game()

# Game Loop
running = True
game_over = False

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE:
                if game_over:
                    game_over = False
                    reset_game()
                else:
                    fire_bullet(player_x + 16, player_y + 10)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    if not game_over:
        player_x += player_x_change
        if player_x >= screen_width - 64:
            player_x = screen_width - 64
        if player_x <= 0:
            player_x = 0

        for i in range(initial_num_of_enemies):
            if enemy_respawn_timers[i] == 0:
                enemy_x[i] += enemy_x_change[i]
                if enemy_x[i] >= screen_width - 64:
                    enemy_x_change[i] = -3
                if enemy_x[i] <= 0:
                    enemy_x_change[i] = 3
                if enemy_y[i] <= player_y - 40:
                    enemy_y[i] += enemy_y_change[i]

                if enemy_y[i] > player_y - 40:
                    game_over_sound.play()
                    game_over = True

                if random.randint(0, 1000) < 1:
                    fire_enemy_bullet(enemy_x[i] + 16, enemy_y[i] + 10)

                for bullet in bullets[:]:
                    bullet[1] -= bullet_speed
                    if collision_occurance(enemy_x[i], enemy_y[i], bullet[0], bullet[1]):
                        bullets.remove(bullet)
                        display_explosion(enemy_x[i], enemy_y[i])
                        score_value += 1
                        enemy_respawn_timers[i] = time.time()
                    else:
                        screen.blit(bullet_img, (bullet[0], bullet[1]))
                    if bullet[1] <= 0:
                        bullets.remove(bullet)

                enemy(enemy_x[i], enemy_y[i], i)
            else:
                if time.time() - enemy_respawn_timers[i] >= respawn_time:
                    enemy_respawn_timers[i] = 0
                    enemy_x[i] = random.randint(0, screen_width - 64)
                    enemy_y[i] = random.randint(50, 100)

        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet[1] += enemy_bullet_speed
            if collision_occurance(player_x, player_y, enemy_bullet[0], enemy_bullet[1]):
                enemy_bullets.remove(enemy_bullet)
                game_over_sound.play()
                game_over = True
            else:
                screen.blit(enemy_bullet_img, (enemy_bullet[0], enemy_bullet[1]))
            if enemy_bullet[1] >= screen_height:
                enemy_bullets.remove(enemy_bullet)

        if score_value % 5 == 0 and score_value != 0 and (len(enemy_img) < score_value // 5 + initial_num_of_enemies):
            num_new_enemies = score_value // 5 - len(enemy_img) + initial_num_of_enemies
            for _ in range(num_new_enemies):
                enemy_img.append(pygame.image.load("ufo (2).png"))
                enemy_x.append(random.randint(0, screen_width - 64))
                enemy_y.append(random.randint(50, 100))
                enemy_x_change.append(3 + score_value // 5)
                enemy_y_change.append(0.09 + score_value / 1000)
                enemy_respawn_timers.append(0)
                for j in range(len(enemy_y_change)):
                    enemy_y_change[j] += 0.1  # Increase downward speed for all enemies

        player(player_x, player_y)
        show_score(text_x, text_y)

        current_time = time.time()
        for explosion in explosions[:]:
            if current_time - explosion[2] <= 2:
                screen.blit(explosion_img, (explosion[0], explosion[1]))
            else:
                explosions.remove(explosion)

    else:
        game_over_text()

    pygame.display.update()

pygame.quit()
