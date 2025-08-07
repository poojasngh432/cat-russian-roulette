import pygame
import sys
import random
import os
import time

# Better BASE_DIR setup for py2app
if getattr(sys, 'frozen', False):
    # Running in a bundle
    BASE_DIR = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    # For py2app specifically
    if 'Contents/MacOS' in BASE_DIR:
        BASE_DIR = os.path.join(BASE_DIR, '..', 'Resources')
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Set BASE_DIR for asset loading
# if getattr(sys, 'frozen', False):
#     BASE_DIR = os.path.dirname(sys.executable)
# else:
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat Russian Roulette - 2 Player")

# Colors and fonts
WHITE = (255, 255, 255)
PINK = (255, 182, 193)
BLUE = (173, 216, 230)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("Chalkboard SE", 30)

click_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "click.wav"))
bang_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "bang.wav"))

cat1_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "cat1.png"))
cat2_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "cat2.png"))
cat1_img = pygame.transform.scale(cat1_img, (140, 140))
cat2_img = pygame.transform.scale(cat2_img, (140, 140))

# Ensure explosion_img is loaded and scaled right after BASE_DIR setup
explosion_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "explosion.png"))
explosion_img = pygame.transform.scale(explosion_img, (40, 40))

gun_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "gun.png"))
gun_img = pygame.transform.scale(gun_img, (60, 60))

# Load visuals (placeholder colored rectangles for players)
player1 = pygame.Rect(200, 220, 100, 100)
player2 = pygame.Rect(500, 220, 100, 100)

# Game variables

bullet_position = random.randint(1, 6)
shots_taken = 0
current_chamber = 1
current_player = 1
game_over = False
winner_text = ""

# Reset game state
def reset_game():
    global bullet_position, shots_taken, current_chamber, current_player, game_over, winner_text
    bullet_position = random.randint(1, 6)
    shots_taken = 0
    current_chamber = 1
    current_player = 1
    game_over = False
    winner_text = ""

def draw_scene(flash=False):
    screen.fill(WHITE if not flash else (255, 0, 0))

    # Draw player images
    screen.blit(cat1_img, player1.topleft)
    screen.blit(cat2_img, player2.topleft)


    # Draw red X on shot player
    if game_over and current_chamber == bullet_position:
        target = player1 if current_player == 1 else player2
        x, y = target.center
        pygame.draw.line(screen, (255, 0, 0), (x - 30, y - 30), (x + 30, y + 30), 5)
        pygame.draw.line(screen, (255, 0, 0), (x + 30, y - 30), (x - 30, y + 30), 5)

    # Draw gun
    if current_player == 1:
        gun_x = player1.right - 5
        gun_y = player1.centery - gun_img.get_height() // 2
    else:
        gun_x = player2.right - 2
        gun_y = player2.centery - gun_img.get_height() // 2
    screen.blit(gun_img, (gun_x, gun_y))

    # Turn info
    # turn_text = font.render(f"Turn {shots_taken}/20", True, BLACK)
    # screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, 50))
    name = "smol cat" if current_player == 1 else "evil cat"
    player_text = font.render(f"{name}'s turn", True, BLACK)
    screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, 90))

    if game_over and winner_text.strip():
        result = font.render(winner_text, True, BLACK)
        text_x = WIDTH // 2 - result.get_width() // 2
        text_y = HEIGHT // 2 + 150
        screen.blit(result, (text_x, text_y))

        # Draw explosion image to the right of the winner text
        screen.blit(explosion_img, (text_x + result.get_width() + 10, text_y))

        restart_msg = font.render("Press 'R' to play again!", True, (100, 149, 237))  # Cornflower Blue
        screen.blit(restart_msg, (WIDTH // 2 - restart_msg.get_width() // 2, text_y + 40))

    pygame.display.flip()

def bullet_animation(start_x, end_x, y):
    step = 5 if start_x < end_x else -5
    for x in range(start_x, end_x, step):
        draw_scene()
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 5)
        pygame.display.flip()
        pygame.time.delay(10)

def take_turn():
    global shots_taken, current_chamber, current_player, game_over, winner_text

    if game_over or shots_taken >= 20:
        return

    shots_taken += 1

    if current_player == 1:
        start_x = player1.centerx
        end_x = player1.centerx
        y = player1.top - 40
    else:
        start_x = player2.centerx
        end_x = player2.centerx
        y = player2.top - 40

    if current_chamber == bullet_position:
        bang_sound.play()
        bullet_animation(start_x, end_x, y)
        draw_scene(flash=True)
        pygame.display.flip()
        pygame.time.delay(500)
        game_over = True
        winner_name = "smol cat" if current_player == 2 else "evil cat"
        winner_text = f"{winner_name} wins!"
    else:
        click_sound.play()
        current_chamber = current_chamber % 6 + 1
        current_player = 2 if current_player == 1 else 1

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    draw_scene()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                take_turn()
            elif event.key == pygame.K_r:
                reset_game()

    clock.tick(30)

pygame.quit()
sys.exit()