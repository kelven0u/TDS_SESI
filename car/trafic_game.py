import pygame
import random
import sys

pygame.init()

# Tela
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Racer Melhorado")

clock = pygame.time.Clock()

# Cores
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)

# Jogador
player = pygame.Rect(175, 500, 50, 80)
player_speed = 5

# Inimigos
enemies = []
enemy_speed = 6

# Estrada
line_y = 0

score = 0
font = pygame.font.Font(None, 30)

def spawn_enemy():
    x = random.choice([120, 175, 230])
    return pygame.Rect(x, -100, 50, 80)

# 🔥 CARRO BONITO
def draw_car(rect, color):
    # Corpo
    pygame.draw.rect(screen, color, rect, border_radius=8)

    # Vidro
    pygame.draw.rect(screen, (180, 220, 255), (rect.x + 10, rect.y + 10, 30, 20), border_radius=5)

    # Rodas
    pygame.draw.rect(screen, (20, 20, 20), (rect.x - 5, rect.y + 10, 5, 20))
    pygame.draw.rect(screen, (20, 20, 20), (rect.x + rect.width, rect.y + 10, 5, 20))
    pygame.draw.rect(screen, (20, 20, 20), (rect.x - 5, rect.y + 50, 5, 20))
    pygame.draw.rect(screen, (20, 20, 20), (rect.x + rect.width, rect.y + 50, 5, 20))

    # Faróis
    pygame.draw.rect(screen, (255, 255, 100), (rect.x + 5, rect.y, 10, 5))
    pygame.draw.rect(screen, (255, 255, 100), (rect.x + rect.width - 15, rect.y, 10, 5))


running = True
spawn_timer = 0

while running:
    clock.tick(60)
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Movimento jogador
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # Limite pista
    if player.x < 100:
        player.x = 100
    if player.x > 250:
        player.x = 250

    # Spawn inimigos
    spawn_timer += 1
    if spawn_timer > 25:
        enemies.append(spawn_enemy())
        spawn_timer = 0

    # Mover inimigos
    for enemy in enemies[:]:
        enemy.y += enemy_speed

        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            score += 1

        # Colisão
        if player.colliderect(enemy):
            pygame.quit()
            sys.exit()

    # Movimento linhas
    line_y += enemy_speed
    if line_y > HEIGHT:
        line_y = 0

    # Estrada
    pygame.draw.rect(screen, (20, 20, 20), (100, 0, 200, HEIGHT))

    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, YELLOW, (195, (i + line_y) % HEIGHT, 10, 20))

    # 🚗 Jogador bonito
    draw_car(player, BLUE)

    # 🚗 Inimigos bonitos
    for enemy in enemies:
        cor = random.choice([
            (200, 0, 0),
            (0, 200, 0),
            (200, 200, 0),
            (255, 100, 0),
            (150, 0, 200)
        ])
        draw_car(enemy, cor)

    # Pontuação
    text = font.render(f"Pontos: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()