import pygame
import random
import sys

# ==========================================
# CONFIGURAÇÕES INICIAIS E CORES
# ==========================================
pygame.init()

LARGURA = 800
ALTURA = 600
FPS = 60

# Cores (Paleta estilo Pixel Art)
VERDE_GRAMA = (34, 139, 34)
CINZA_ASFALTO = (50, 50, 50)
BRANCO = (255, 255, 255)
AMARELO_FAIXA = (255, 215, 0)
VERMELHO = (220, 20, 60)
AZUL_CARRO = (30, 144, 255)
PRETO = (10, 10, 10)
CINZA_CLARO = (180, 180, 180)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Retro Pixel Racer - By Gemini")
relogio = pygame.time.Clock()

# Fontes
fonte_painel = pygame.font.SysFont("consolas", 24, bold=True)
fonte_titulo = pygame.font.SysFont("consolas", 48, bold=True)

# ==========================================
# FUNÇÕES DE DESENHO ESTILO PIXEL ART
# ==========================================
def desenhar_carro(superficie, x, y, cor_principal):
    """Desenha um carro estilo pixel art usando retângulos"""
    # Pneus
    pygame.draw.rect(superficie, PRETO, (x - 18, y - 20, 8, 16)) # Pneu esq topo
    pygame.draw.rect(superficie, PRETO, (x + 10, y - 20, 8, 16)) # Pneu dir topo
    pygame.draw.rect(superficie, PRETO, (x - 18, y + 15, 8, 16)) # Pneu esq base
    pygame.draw.rect(superficie, PRETO, (x + 10, y + 15, 8, 16)) # Pneu dir base
    
    # Chassi principal
    pygame.draw.rect(superficie, cor_principal, (x - 15, y - 25, 30, 50))
    # Teto / Vidro
    pygame.draw.rect(superficie, BRANCO, (x - 10, y - 10, 20, 15))
    # Faróis
    pygame.draw.rect(superficie, AMARELO_FAIXA, (x - 12, y - 25, 6, 4))
    pygame.draw.rect(superficie, AMARELO_FAIXA, (x + 6, y - 25, 6, 4))
    # Aerofólio (detalhe traseiro)
    pygame.draw.rect(superficie, PRETO, (x - 15, y + 20, 30, 4))

def desenhar_obstaculo(superficie, x, y, tipo):
    """Desenha obstáculos que vêm na direção do jogador"""
    if tipo == 'carro':
        desenhar_carro(superficie, x, y, VERMELHO)
    elif tipo == 'buraco':
        pygame.draw.ellipse(superficie, PRETO, (x - 15, y - 10, 30, 20))
        pygame.draw.ellipse(superficie, CINZA_ASFALTO, (x - 12, y - 8, 24, 16))

# ==========================================
# CLASSES DO JOGO
# ==========================================
class Jogador:
    def __init__(self):
        self.x = LARGURA // 2
        self.y = ALTURA - 80
        self.velocidade_movimento = 7
        self.largura_hitbox = 30
        self.altura_hitbox = 50

    def mover(self, teclas):
        # Limites da estrada (grama começa em x=150 e termina em x=650)
        limite_esq = 170
        limite_dir = 630
        
        if teclas[pygame.K_LEFT] and self.x > limite_esq:
            self.x -= self.velocidade_movimento
        if teclas[pygame.K_RIGHT] and self.x < limite_dir:
            self.x += self.velocidade_movimento

    def desenhar(self, tela):
        desenhar_carro(tela, self.x, self.y, AZUL_CARRO)
        
    def obter_rect(self):
        return pygame.Rect(self.x - 15, self.y - 25, self.largura_hitbox, self.altura_hitbox)


class Inimigo:
    def __init__(self, velocidade_jogo):
        self.x = random.choice([250, 400, 550]) # Faixas da pista
        self.y = -50
        self.tipo = random.choice(['carro', 'carro', 'buraco']) # Mais chance de ser carro
        self.velocidade = velocidade_jogo + random.randint(1, 4) if self.tipo == 'carro' else velocidade_jogo
        self.largura_hitbox = 30
        self.altura_hitbox = 50 if self.tipo == 'carro' else 20

    def atualizar(self, velocidade_jogo):
        # Buracos se movem com a pista, carros se movem um pouco mais rápido
        if self.tipo == 'buraco':
            self.y += velocidade_jogo
        else:
            self.y += self.velocidade

    def desenhar(self, tela):
        desenhar_obstaculo(tela, self.x, self.y, self.tipo)

    def obter_rect(self):
        if self.tipo == 'carro':
            return pygame.Rect(self.x - 15, self.y - 25, self.largura_hitbox, self.altura_hitbox)
        else:
            return pygame.Rect(self.x - 15, self.y - 10, 30, 20)

# ==========================================
# CICLO PRINCIPAL DO JOGO
# ==========================================
def jogar():
    jogador = Jogador()
    inimigos = []
    
    # Variáveis de Estado
    velocidade_jogo = 8
    pontuacao = 0
    distancia = 0
    deslocamento_faixa = 0
    
    # Timers e Controle de Dificuldade
    tempo_geracao = 0
    intervalo_geracao = 90 # Em frames (a 60 fps = 1.5s)
    
    jogando = True
    game_over = False

    while jogando:
        relogio.tick(FPS)
        tela.fill(VERDE_GRAMA)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and game_over:
                if evento.key == pygame.K_r:
                    # Reinicia o loop do jogo
                    return jogar()
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # --- Atualizações Lógicas ---
            teclas = pygame.key.get_pressed()
            jogador.mover(teclas)

            # Animação da pista
            deslocamento_faixa = (deslocamento_faixa + velocidade_jogo) % 60
            
            # Controle de dificuldade e pontuação
            distancia += velocidade_jogo / 60
            pontuacao = int(distancia * 10)
            
            # Aumentar dificuldade gradualmente
            if pontuacao > 0 and pontuacao % 100 == 0:
                velocidade_jogo += 0.05
                if intervalo_geracao > 30:
                    intervalo_geracao -= 0.5
                    
            # Gerador de Inimigos
            tempo_geracao += 1
            if tempo_geracao >= intervalo_geracao:
                inimigos.append(Inimigo(int(velocidade_jogo)))
                tempo_geracao = 0

            # --- Desenhando o Cenário ---
            # Asfalto Principal (x: 150 a 650, largura: 500)
            pygame.draw.rect(tela, CINZA_ASFALTO, (150, 0, 500, ALTURA))
            
            # Bordas da Pista (Acostamento)
            pygame.draw.rect(tela, BRANCO, (140, 0, 10, ALTURA))
            pygame.draw.rect(tela, BRANCO, (650, 0, 10, ALTURA))

            # Linhas Tracejadas Centrais
            for y in range(0, ALTURA, 60):
                pygame.draw.rect(tela, AMARELO_FAIXA, (310, y + deslocamento_faixa - 60, 10, 30))
                pygame.draw.rect(tela, AMARELO_FAIXA, (480, y + deslocamento_faixa - 60, 10, 30))

            # --- Atualizando e Desenhando Objetos ---
            for inimigo in inimigos[:]:
                inimigo.atualizar(velocidade_jogo)
                inimigo.desenhar(tela)
                
                # Checagem de Colisão
                if jogador.obter_rect().colliderect(inimigo.obter_rect()):
                    game_over = True
                
                # Remoção de inimigos que saíram da tela
                if inimigo.y > ALTURA + 50:
                    inimigos.remove(inimigo)

            jogador.desenhar(tela)

            # --- Interface (Velocímetro e Pontos) ---
            velocidade_kmh = int((velocidade_jogo * 15)) # Cálculo fictício para km/h
            
            # Fundo do Painel (HUD)
            pygame.draw.rect(tela, PRETO, (10, 10, 200, 90), border_radius=10)
            pygame.draw.rect(tela, CINZA_CLARO, (12, 12, 196, 86), 2, border_radius=10)
            
            # Textos
            texto_vel = fonte_painel.render(f"VEL: {velocidade_kmh} KM/H", True, BRANCO)
            texto_pts = fonte_painel.render(f"PTS: {pontuacao:05d}", True, BRANCO)
            
            tela.blit(texto_vel, (20, 25))
            tela.blit(texto_pts, (20, 60))

        else:
            # --- Tela de Game Over ---
            # Fundo escuro semi-transparente
            s = pygame.Surface((LARGURA, ALTURA))
            s.set_alpha(150)
            s.fill((0, 0, 0))
            tela.blit(s, (0, 0))
            
            texto_go = fonte_titulo.render("BATIDA!", True, VERMELHO)
            texto_reinicio = fonte_painel.render("Pressione [R] para Reiniciar", True, BRANCO)
            texto_sair = fonte_painel.render("Pressione [Q] para Sair", True, BRANCO)
            
            tela.blit(texto_go, (LARGURA//2 - texto_go.get_width()//2, 200))
            tela.blit(texto_reinicio, (LARGURA//2 - texto_reinicio.get_width()//2, 300))
            tela.blit(texto_sair, (LARGURA//2 - texto_sair.get_width()//2, 350))

        pygame.display.flip()

# Inicia o Jogo
if __name__ == "__main__":
    jogar()