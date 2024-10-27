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
GROUND_BROWN = (139, 69, 19)
GREY = (128, 128, 128)
CAR_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (34, 139, 34)
CLOUD_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
BATTERY_COLOR = (255, 215, 0)

game_font = pygame.font.SysFont("Arial", 50)

# Game Variables
image = pygame.image.load("Carimage2.png")
game_speed = 5
gravity = 0.5
fall_speed = 5
ground_x = 0
ground_y = 680
car_x, car_y = 100, ground_y - 30
max_jump_height = 200
obstacle_x = 1200
obstacle_y = 1200
obstacle_height = random.choice([30, 60, 90])
obstacle_height_y_height = random.choice([550, 500, 600])
clouds = [(random.randint(200, 1200), random.randint(50, 150)) for _ in range(5)]
battery_x, battery_y = random.randint(1300, 1600), random.randint(ground_y - 80, ground_y - 40)
score = 1885
high_score = 0


# Menu screen
def show_menu():
    screen.fill(SKY_BLUE)
    title_text = game_font.render("Delorean Game", True, BLACK)
    start_text = game_font.render("Press Enter to Start", True, BLACK)
    screen.blit(title_text, (400, 250))
    screen.blit(start_text, (400, 350))
    pygame.display.update()


def rect_circle_collision(rect, circle):
    rect_center_x = rect.x + rect.width / 2
    rect_center_y = rect.y + rect.height / 2
    circle_distance_x = abs(circle.x - rect_center_x)
    circle_distance_y = abs(circle.y - rect_center_y)

    if circle_distance_x > (rect.width / 2 + circle.radius):
        return False
    if circle_distance_y > (rect.height / 2 + circle.radius):
        return False

    if circle_distance_x <= (rect.width / 2):
        return True
    if circle_distance_y <= (rect.height / 2):
        return True

    corner_distance_sq = (circle_distance_x - rect.width / 2) ** 2 + (circle_distance_y - rect.height / 2) ** 2

    return corner_distance_sq <= (circle.radius ** 2)


class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


# Main Game Loop with Menu
game_active = False

# main menu start up
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
    if keys[pygame.K_SPACE] and car_y > max_jump_height:
        car_y -= 2
    else:
        if car_y < ground_y - 30:
            car_y += fall_speed
        else:
            car_y = ground_y - 30

    screen.fill(SKY_BLUE)

    # Draws the ground
    ground_x -= game_speed
    pygame.draw.rect(screen, GROUND_BROWN, (ground_x, ground_y, 1200, 40))
    pygame.draw.rect(screen, GROUND_BROWN, (ground_x + 1200, ground_y, 1200, 40))

    if ground_x <= -1200:
        ground_x = 0

    # Draw clouds
    for i in range(len(clouds)):
        clouds[i] = (clouds[i][0] - 1, clouds[i][1])

        if clouds[i][0] < -100:
            clouds[i] = (random.randint(1200, 1600), random.randint(50, 150))

        pygame.draw.rect(screen, CLOUD_COLOR, (*clouds[i], 100, 40))

    # Draws the car (implement the car image)
    car_rect = pygame.Rect(car_x, car_y, 60, 30)
    screen.blit(image, car_rect)
    #pygame.draw.rect(screen, CAR_COLOR, car_rect)

    # Draw a random cactus
    obstacle_x -= game_speed
    obstacle_y -= 1.5 * game_speed
    obstacle_y -= random.choice([5, 10, 20])

    if obstacle_y < - 175:
        obstacle_y = 1200
        obstacle_height_y_height = random.choice([400, 450, 550, 500, 600])
        obstacle_y -= random.choice([5, 10, 20])
    if obstacle_x < -50:
        obstacle_x = 1200
        obstacle_height = random.choice([30, 60, 90])

    # Draw and move power battery
    battery_x -= game_speed

    if battery_x < -50:
        battery_x = random.randint(1300, 1600)
        battery_y = random.randint(ground_y - 80, ground_y - 40)

    battery_rect = pygame.Rect(battery_x, battery_y, 20, 20)
    pygame.draw.rect(screen, BATTERY_COLOR, battery_rect)

    obstacle_circle = Circle(obstacle_y, obstacle_height_y_height, 10, OBSTACLE_COLOR)
    obstacle_rect = pygame.Rect(obstacle_x, ground_y - obstacle_height, 30, obstacle_height)
    pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle_rect)

    # Check for collisions with the cactus
    if car_rect.colliderect(obstacle_rect):
        game_over_text = game_font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (500, 360))
        pygame.display.update()
        pygame.time.delay(2000)
        game_active = False
        if score > high_score:
            high_score = score
        score = 1885
        car_x, car_y = 100, ground_y - 30
        obstacle_x = 1200
        battery_x = random.randint(1300, 1600)
        GROUND_BROWN = (139, 69, 19)
        continue

    # Check for collisions with the power battery
    if car_rect.colliderect(battery_rect):
        score += 10
        game_speed += .25
        battery_x = random.randint(1300, 1600)
        battery_y = random.randint(ground_y - 80, ground_y - 40)
    if score > 1:
        pygame.draw.circle(screen, GROUND_BROWN, (obstacle_circle.x, obstacle_circle.y),
                           obstacle_circle.radius)
        GROUND_BROWN = GREY
        if rect_circle_collision(car_rect, obstacle_circle):
            game_over_text = game_font.render("Game Over", True, BLACK)
            screen.blit(game_over_text, (500, 360))
            pygame.display.update()
            pygame.time.delay(2000)
            game_active = False
            if score > high_score:
                high_score = score
            score = 1885
            car_x, car_y = 100, ground_y - 30
            obstacle_x = 1200
            battery_x = random.randint(1300, 1600)
            GROUND_BROWN = (139, 69, 19)
            continue


    # Displays the score on the screen
    score_text = game_font.render(f"Year: {score}", True, BLACK)
    screen.blit(score_text, (50, 50))

    high_score_text = game_font.render(f"Farthest Year: {high_score}", True, BLACK)
    screen.blit(high_score_text, (50, 100))

    clock.tick(60)
    pygame.display.update()