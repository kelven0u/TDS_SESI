import pygame
import random
import sys

pygame.init()

# Tela
LARGURA, ALTURA = 400, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
VERDE = (0, 200, 0)
AZUL = (135, 206, 250)
PRETO = (0, 0, 0)

# Fonte
fonte = pygame.font.Font(None, 36)

# Jogador
bird_x = 80
bird_y = 300
bird_radius = 15
vel_y = 0
gravity = 0.5

# Cano
pipe_width = 70
pipe_gap = 150
pipe_x = LARGURA
pipe_height = random.randint(150, 400)

score = 0

def reset():
    global bird_y, vel_y, pipe_x, pipe_height, score
    bird_y = 300
    vel_y = 0
    pipe_x = LARGURA
    pipe_height = random.randint(150, 400)
    score = 0

running = True
while running:
    clock.tick(60)
    TELA.fill(AZUL)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                vel_y = -8

    # Física
    vel_y += gravity
    bird_y += vel_y

    # Cano movimento
    pipe_x -= 4
    if pipe_x < -pipe_width:
        pipe_x = LARGURA
        pipe_height = random.randint(150, 400)
        score += 1

    # Desenho
    pygame.draw.circle(TELA, BRANCO, (bird_x, int(bird_y)), bird_radius)
    pygame.draw.rect(TELA, VERDE, (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(TELA, VERDE, (pipe_x, pipe_height + pipe_gap, pipe_width, ALTURA))

    # Colisão
    if bird_y <= 0 or bird_y >= ALTURA:
        reset()

    if (bird_x + bird_radius > pipe_x and bird_x - bird_radius < pipe_x + pipe_width):
        if bird_y - bird_radius < pipe_height or bird_y + bird_radius > pipe_height + pipe_gap:
            reset()

    # Pontuação
    text = fonte.render(f"Pontos: {score}", True, PRETO)
    TELA.blit(text, (10, 10))

    pygame.display.update()