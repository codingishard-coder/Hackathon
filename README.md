import os
import pygame
import sys
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Delorean Game")

# Colors variables
SKY_BLUE = (173, 216, 230)
SKY_DUSK = (0,0,0)
SKY_MIDNIGHT = (55, 14, 151)
GROUND_BROWN = (139, 69, 19)
CAR_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (34, 139, 34)
CLOUD_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
BATTERY_COLOR = (255, 215, 0)
GRASS_COLOR = (24, 240, 60)

game_font = pygame.font.SysFont("Arial", 50)

# Game Variables
image = pygame.image.load(os.path.join('Carimage2.png'))
game_speed = 6
gravity = 0.5
fall_speed = 3.5
ground_x = 0
ground_y = 680
car_x, car_y = 100, ground_y - 30
max_jump_height = 500
second_max_jump_height = 150
jump_count = 1
obstacle_x = 1200
obstacle_height = random.choice([30, 60, 90])
clouds = [(random.randint(200, 1200), random.randint(50, 150)) for _ in range(5)]
battery_x, battery_y = random.randint(1300, 1600), random.randint(ground_y - 80, ground_y - 40)
score = 0
highscore = 0
Time = 1
# Menu screen
def show_menu():
    screen.fill(SKY_BLUE)
    title_text = game_font.render("Delorean Game", True, BLACK)
    start_text = game_font.render("Press Enter to Start", True, BLACK)
    screen.blit(title_text, (400, 250))
    screen.blit(start_text, (400, 350))
    pygame.display.update()

# Main Game Loop with Menu
game_active = False

#main menu start up
while True:
    if not game_active:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
        continue

    # Game logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Check if the space bar is being held down for jumping
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and car_y > max_jump_height and jump_count == 1:
        if keys[pygame.K_SPACE] and car_y > second_max_jump_height:
            car_y -= 10

    else:
        if car_y < ground_y - 30:
            car_y += fall_speed
            jump_count = 0
        elif car_y >= ground_y - 30:
            jump_count = 1


    screen.fill(SKY_BLUE)
    #if Time < 10:
    #    screen.fill(SKY_MIDNIGHT)
    #elif Time < 20:
    #    screen.fill(SKY_BLUE)
    #else:
    #    screen.fill(SKY_MIDNIGHT)
    #    Time = 0


    # Draws the ground
    ground_x -= game_speed
    pygame.draw.rect(screen, GROUND_BROWN, (ground_x, ground_y, 1200, 40))
    pygame.draw.rect(screen, GROUND_BROWN, (ground_x + 1200, ground_y, 1200, 40))
    pygame.draw.rect(screen, GRASS_COLOR, (ground_x, ground_y, 1200, 10))
    pygame.draw.rect(screen, GRASS_COLOR, (ground_x + 1200, ground_y, 1200, 10))
    if ground_x <= -1200:
        ground_x = 0

    # Draw clouds
    for i in range(len(clouds)):
        clouds[i] = (clouds[i][0] - 1, clouds[i][1])
        if clouds[i][0] < -100:
            clouds[i] = (random.randint(1000, 1800), random.randint(50, 425))
        pygame.draw.rect(screen, CLOUD_COLOR, (*clouds[i], 100, 40))

    # Draws the car (implement the car image)
    car_rect = pygame.Rect(car_x, car_y, 60, 30)
    screen.blit(image, car_rect)
    #pygame.draw.rect(screen, CAR_COLOR, car_rect)


    # Draw a random cactus
    obstacle_x -= game_speed
    if obstacle_x < -50:
        obstacle_x = 1200
        obstacle_height = random.choice([30, 60, 90])
    obstacle_rect = pygame.Rect(obstacle_x, ground_y - obstacle_height, 30, obstacle_height)
    pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle_rect)

    # Draw and move power battery
    battery_x -= game_speed
    if battery_x < -50:
        battery_x = random.randint(1300, 1600)
        battery_y = random.randint(ground_y - 80, ground_y - 40)
    battery_rect = pygame.Rect(battery_x, battery_y, 20, 20)
    pygame.draw.rect(screen, BATTERY_COLOR, battery_rect)

    # Check for collisions with the cactus
    if car_rect.colliderect(obstacle_rect):
        game_over_text = game_font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (500, 360))
        pygame.display.update()
        pygame.time.delay(2000)
        game_active = False
        if highscore < score:
            highscore = score
        score = 0
        game_speed = 6
        car_x, car_y = 100, ground_y - 30
        obstacle_x = 1200
        battery_x = random.randint(1300, 1600)
        continue

    # Check for collisions with the power battery
    if car_rect.colliderect(battery_rect):
        score += 1
        Time += 1
        game_speed += .5
        battery_x = random.randint(1300, 1600)
        battery_y = random.randint(ground_y - 80, ground_y - 40)

    # Displays the score on the screen
    score_text = game_font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (50, 50))

    High_score_text = game_font.render(f"High Score: {highscore}", True, BLACK)
    screen.blit(High_score_text, (50, 100))

    pygame.display.update()
    clock.tick(60)


