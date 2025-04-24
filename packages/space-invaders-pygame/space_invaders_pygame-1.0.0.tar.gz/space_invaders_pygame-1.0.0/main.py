import pygame
import sys
import random
from player import Player
from enemy import Enemy
from bullet import Bullet, Explosion, PowerUp

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Game objects
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
enemies = [Enemy(x, 50) for x in range(50, SCREEN_WIDTH - 50, 100)]
bullets = []
explosions = []
powerups = []
powerup_timer = 0
rapid_fire = False
rapid_timer = 0
shield = False
shield_timer = 0
lives = 3

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Starfield background
def draw_starfield(screen, stars):
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), star, 1)

def update_starfield(stars, screen_height):
    for i, star in enumerate(stars):
        stars[i] = (star[0], star[1] + 2)
        if stars[i][1] > screen_height:
            stars[i] = (random.randint(0, SCREEN_WIDTH), 0)

# Starfield setup
stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(100)]

# Game loop
running = True
while running:
    screen.fill(BLACK)
    update_starfield(stars, SCREEN_HEIGHT)
    draw_starfield(screen, stars)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Power-up timers
    if rapid_fire:
        rapid_timer -= 1
        if rapid_timer <= 0:
            rapid_fire = False
    if shield:
        shield_timer -= 1
        if shield_timer <= 0:
            shield = False

    # Player controls
    keys = pygame.key.get_pressed()
    can_shoot = rapid_fire or pygame.time.get_ticks() % 10 == 0
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_UP]:
        player.move_up()
    if keys[pygame.K_DOWN]:
        player.move_down()
    if keys[pygame.K_SPACE] and can_shoot:
        if len(bullets) < (10 if rapid_fire else 5):
            bullets.append(Bullet(player.x + player.width // 2, player.y))

    # Update bullets
    for bullet in bullets[:]:
        bullet.move()
        if bullet.y < 0:
            bullets.remove(bullet)

    # Update enemies
    for enemy in enemies:
        enemy.update()

    # Update explosions
    for explosion in explosions[:]:
        explosion.update()
        if not explosion.active:
            explosions.remove(explosion)

    # Update powerups
    for powerup in powerups[:]:
        powerup.move()
        if not powerup.active:
            powerups.remove(powerup)
        elif (player.x < powerup.x < player.x + player.width and
              player.y < powerup.y < player.y + player.height):
            if powerup.type == 'rapid':
                rapid_fire = True
                rapid_timer = 300
            elif powerup.type == 'shield':
                shield = True
                shield_timer = 300
            elif powerup.type == 'life':
                lives += 1
            powerups.remove(powerup)

    # Collision detection
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.collides_with(enemy):
                bullets.remove(bullet)
                explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                # 1 in 3 chance to spawn a powerup
                if random.randint(1,3) == 1:
                    powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                enemies.remove(enemy)
                score += 100
                break

    # Draw game objects
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for explosion in explosions:
        explosion.draw(screen)
    for powerup in powerups:
        powerup.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (10, 10))

    # Draw shield effect
    if shield:
        pygame.draw.ellipse(screen, (0,255,255), (player.x-10, player.y-10, player.width+20, player.height+20), 3)

    # Draw lives
    life_text = font.render(f"Lives: {lives}", True, (0,255,0))
    screen.blit(life_text, (10, 40))

    # Check for game over
    if not enemies:
        print("You Win!")
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()