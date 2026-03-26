import pygame
import sys
import random

# --- CONFIGURAÇÕES GLOBAIS ---
LARGURA, ALTURA = 1200, 700
FPS = 60

# CORES PIXEL ART
PRETO       = (10, 10, 10)
BRANCO      = (240, 240, 240)
CINZA_ESTRADA = (40, 40, 45)
AMARELO_TOL = (255, 200, 0)
VERDE_GO    = (0, 255, 100)
VERMELHO_REV = (255, 50, 50)
AZUL_JDM    = (50, 100, 255)

# --- BANCO DE DADOS EXTENSO (BASEADO NA SUA LISTA) ---
# Aqui você pode expandir até os 100 carros
CARROS_DB = [
    {"id": 1, "nome": "Ford Pinto (1974)", "preco": 2000, "peso": 1000, "hp": 75, "tipo": "Americano"},
    {"id": 2, "nome": "Dodge Neon SRT-4", "preco": 3310, "peso": 1300, "hp": 230, "tipo": "Americano"},
    {"id": 3, "nome": "Eagle Talon TSI", "preco": 8000, "peso": 1450, "hp": 210, "tipo": "Americano"},
    {"id": 4, "nome": "Chevrolet Camaro IROC-Z", "preco": 11500, "peso": 1550, "hp": 245, "tipo": "Americano"},
    {"id": 5, "nome": "Ford Focus RS", "preco": 36900, "peso": 1500, "hp": 350, "tipo": "Europeu"},
    {"id": 6, "nome": "Nissan Skyline GT-R R34", "preco": 85000, "peso": 1560, "hp": 280, "tipo": "JDM"},
    # Adicione os outros 94 aqui seguindo o padrão...
]

PECAS_DB = {
    "motores": [
        {"nome": "Stock", "hp": 0, "preco": 0},
        {"nome": "V8 Big Block", "hp": 500, "preco": 25000},
        {"nome": "2JZ-GTE Swap", "hp": 320, "preco": 35000},
        {"nome": "RB26DETT", "hp": 300, "preco": 32000},
        {"nome": "LSX Twin Turbo", "hp": 1200, "preco": 95000}
    ],
    "turbos": [
        {"nome": "Nenhum", "boost": 0, "preco": 0},
        {"nome": "Street Turbo S1", "boost": 150, "preco": 5000},
        {"nome": "Garrett GT45 High", "boost": 600, "preco": 18000}
    ],
    "pneus": [
        {"nome": "Street", "grip": 0.5, "preco": 500},
        {"nome": "Semi-Slick", "grip": 0.8, "preco": 2500},
        {"nome": "Drag Slicks", "grip": 1.2, "preco": 6000}
    ]
}

# --- CLASSES PRINCIPAIS ---

class CarroJogador:
    def __init__(self, dados_carro):
        self.dados = dados_carro
        self.nome = dados_carro["nome"]
        self.peso = dados_carro["peso"]
        
        # Peças Instaladas
        self.motor = PECAS_DB["motores"][0]
        self.turbo = PECAS_DB["turbos"][0]
        self.pneu = PECAS_DB["pneus"][0]
        
        # Atributos de Performance Reais
        self.hp_total = dados_carro["hp"] + self.motor["hp"] + self.turbo["boost"]
        self.torque = self.hp_total * 1.2
        self.grip = self.pneu["grip"]
        
        # Dinâmica de Corrida
        self.x = 100
        self.velocidade = 0
        self.rpm = 800
        self.marcha = 0 # 0 = Neutro, 1-6 Marchas
        self.embreagem_pressionada = False
        self.temperatura_pneus = 0 # Para o Burnout
        
    def atualizar_status(self):
        """Recalcula o HP após modificações na loja"""
        self.hp_total = self.dados["hp"] + self.motor["hp"] + self.turbo["boost"]
        self.torque = self.hp_total * 1.1

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("PIXEL DRAG RACER - EXTREME CUSTOM")
        self.relogio = pygame.time.Clock()
        self.fonte_p = pygame.font.SysFont("Courier New", 18, bold=True)
        self.fonte_g = pygame.font.SysFont("Courier New", 45, bold=True)
        
        self.dinheiro = 50000
        self.carro = CarroJogador(CARROS_DB[5]) # Começa com o R34 para teste
        self.estado = "GARAGEM" # GARAGEM, LOJA, CORRIDA, DYNO

    def desenhar_hud_corrida(self):
        # Velocímetro e RPM
        pygame.draw.rect(self.tela, PRETO, (LARGURA-300, ALTURA-150, 250, 100))
        cor_rpm = VERDE_GO if self.carro.rpm < 7000 else VERMELHO_REV
        
        txt_rpm = self.fonte_p.render(f"RPM: {int(self.carro.rpm)}", True, cor_rpm)
        txt_vel = self.fonte_p.render(f"SPD: {int(self.carro.velocidade)} KM/H", True, BRANCO)
        txt_gear = self.fonte_g.render(f"G: {self.carro.marcha if self.carro.marcha > 0 else 'N'}", True, AMARELO_TOL)
        
        self.tela.blit(txt_rpm, (LARGURA-280, ALTURA-130))
        self.tela.blit(txt_vel, (LARGURA-280, ALTURA-100))
        self.tela.blit(txt_gear, (LARGURA-120, ALTURA-135))
        
        # Barra de Embreagem
        cor_emb = (0, 200, 255) if self.carro.embreagem_pressionada else (100, 100, 100)
        pygame.draw.rect(self.tela, cor_emb, (LARGURA-300, ALTURA-40, 250, 20))
        self.tela.blit(self.fonte_p.render("CLUTCH", True, PRETO), (LARGURA-210, ALTURA-42))

    def mecanica_corrida(self):
        teclas = pygame.key.get_pressed()
        
        # Lógica de Embreagem (Shift Esquerdo)
        self.carro.embreagem_pressionada = teclas[pygame.K_LSHIFT]
        
        # Aceleração e RPM
        if teclas[pygame.K_UP]:
            if self.carro.embreagem_pressionada or self.carro.marcha == 0:
                self.carro.rpm += 200 # Sobe rápido no neutro
            else:
                # Na marcha, a aceleração depende do torque e peso
                acel = (self.carro.torque / self.carro.peso) * (1 / (self.carro.marcha * 0.5))
                self.carro.velocidade += acel
                self.carro.rpm = 1000 + (self.carro.velocidade * 30 / self.carro.marcha)
        else:
            if self.carro.rpm > 800: self.carro.rpm -= 50
            if self.carro.velocidade > 0: self.carro.velocidade -= 0.5

        # Limite de RPM (Corte de giro)
        if self.carro.rpm > 9000: self.carro.rpm = 8800
        
        # Troca de Marchas (Espaço) - Requer Embreagem
        # (Lógica simplificada para o exemplo)
        
        # Desenho da Pista
        self.tela.fill(CINZA_ESTRADA)
        pygame.draw.rect(self.tela, VERDE_GO, (0, 0, LARGURA, 100)) # Grama
        pygame.draw.rect(self.tela, VERDE_GO, (0, 500, LARGURA, ALTURA)) # Grama
        
        # Carro (Pixel Bloc)
        x_render = 50 + (self.carro.x % LARGURA)
        pygame.draw.rect(self.tela, AZUL_JDM, (self.carro.x, 350, 120, 40)) # Corpo
        pygame.draw.rect(self.tela, PRETO, (self.carro.x+10, 380, 25, 25)) # Roda E
        pygame.draw.rect(self.tela, PRETO, (self.carro.x+85, 380, 25, 25)) # Roda D
        
        self.carro.x += self.carro.velocidade * 0.1
        
        self.desenhar_hud_corrida()

    def tela_garagem(self):
        self.tela.fill(PRETO)
        txt = self.fonte_g.render(f"GARAGEM: {self.carro.nome}", True, BRANCO)
        self.tela.blit(txt, (50, 50))
        
        info = [
            f"HP: {self.carro.hp_total}",
            f"MOTOR: {self.carro.motor['nome']}",
            f"TURBO: {self.carro.turbo['nome']}",
            f"DINHEIRO: ${self.dinheiro}",
            "",
            "[C] CORRER (DRAG)",
            "[L] LOJA DE PEÇAS",
            "[D] DYNO TUNING"
        ]
        
        for i, linha in enumerate(info):
            t = self.fonte_p.render(linha, True, VERDE_GO if "$" in linha else BRANCO)
            self.tela.blit(t, (50, 150 + (i*30)))

    def loop_principal(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if evento.type == pygame.KEYDOWN:
                    if self.estado == "GARAGEM":
                        if evento.key == pygame.K_c: self.estado = "CORRIDA"
                        if evento.key == pygame.K_l: self.estado = "LOJA"
                    
                    # Troca de marcha na corrida
                    if self.estado == "CORRIDA":
                        if evento.key == pygame.K_x and self.carro.embreagem_pressionada:
                            if self.carro.marcha < 6:
                                self.carro.marcha += 1
                                self.carro.rpm -= 3000 # Queda de RPM na troca
                        if evento.key == pygame.K_z and self.carro.embreagem_pressionada:
                            if self.carro.marcha > 0: self.carro.marcha -= 1

            if self.estado == "GARAGEM":
                self.tela_garagem()
            elif self.estado == "CORRIDA":
                self.mecanica_corrida()
            
            pygame.display.flip()
            self.relogio.tick(FPS)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    jogo = Jogo()
    jogo.loop_principal()