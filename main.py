import random
import sys
import pygame

# Inicialização do Pygame
pygame.init()

# Configurações de exibição
LARGURA = 800
ALTURA = 600
TAMANHO_BLOCO = 20
FPS = 12

# Paleta de Cores (RGB)
COR_FUNDO = (24, 28, 36)
COR_COBRA = (46, 204, 113)
COR_CABETA = (39, 174, 96)
COR_COMIDA = (231, 76, 60)
COR_TEXTO = (236, 240, 241)
COR_GAME_OVER = (230, 126, 34)

# Configuração da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Cobrinha")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Times New Roman", 22, bold=True)


def gerar_comida(cobrinha):
    """Gera uma posição aleatória alinhada com a grade e fora do corpo da cobra."""
    while True:
        x = (
            random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO)
            * TAMANHO_BLOCO
        )
        y = (
            random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO)
            * TAMANHO_BLOCO
        )
        if (x, y) not in cobrinha:
            return (x, y)


def executar_jogo():
    # Posições iniciais do corpo da cobra (cabeça na posição 0)
    cobrinha = [(300, 200), (280, 200), (260, 200)]
    direcao = (TAMANHO_BLOCO, 0)  # Movimento inicial: Direita
    comida = gerar_comida(cobrinha)
    pontuacao = 0
    game_over = False

    while True:
        # Processamento de eventos de teclado e janela
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if game_over:
                    if evento.key == pygame.K_e:
                        executar_jogo()  # Reinicia a partida
                    elif evento.key == pygame.K_r:
                        pygame.quit()
                        sys.exit()
                else:
                    # Impede a rotação imediata de 180 graus (inversão para o próprio corpo)
                    if (
                        evento.key == pygame.K_UP
                        and direcao != (0, TAMANHO_BLOCO)
                    ):
                        direcao = (0, -TAMANHO_BLOCO)
                    elif (
                        evento.key == pygame.K_DOWN
                        and direcao != (0, -TAMANHO_BLOCO)
                    ):
                        direcao = (0, TAMANHO_BLOCO)
                    elif (
                        evento.key == pygame.K_LEFT
                        and direcao != (TAMANHO_BLOCO, 0)
                    ):
                        direcao = (-TAMANHO_BLOCO, 0)
                    elif (
                        evento.key == pygame.K_RIGHT
                        and direcao != (-TAMANHO_BLOCO, 0)
                    ):
                        direcao = (TAMANHO_BLOCO, 0)

        if not game_over:
            # Calcula nova posição da cabeça
            nova_cabeca = (
                cobrinha[0][0] + direcao[0],
                cobrinha[0][1] + direcao[1],
            )

            # Teste de colisão com as bordas da tela
            if (
                nova_cabeca[0] < 0
                or nova_cabeca[0] >= LARGURA
                or nova_cabeca[1] < 0
                or nova_cabeca[1] >= ALTURA
            ):
                game_over = True

            # Teste de colisão com o próprio corpo
            if nova_cabeca in cobrinha:
                game_over = True

            if not game_over:
                cobrinha.insert(0, nova_cabeca)

                # Teste se a cobra atingiu a comida
                if nova_cabeca == comida:
                    pontuacao += 10
                    comida = gerar_comida(cobrinha)
                else:
                    cobrinha.pop()  # Remove a cauda se não comeu nada

        # --- Renderização na Tela ---
        tela.fill(COR_FUNDO)

        # Desenha a comida
        pygame.draw.rect(
            tela,
            COR_COMIDA,
            (comida[0], comida[1], TAMANHO_BLOCO - 1, TAMANHO_BLOCO - 1),
        )

        # Desenha a cobra (diferenciando a cabeça do corpo)
        for i, segmento in enumerate(cobrinha):
            cor = COR_CABETA if i == 0 else COR_COBRA
            pygame.draw.rect(
                tela,
                cor,
                (
                    segmento[0],
                    segmento[1],
                    TAMANHO_BLOCO - 1,
                    TAMANHO_BLOCO - 1,
                ),
            )

        # Desenha o placar
        texto_placar = fonte.render(f"Pontos: {pontuacao}", True, COR_TEXTO)
        tela.blit(texto_placar, (15, 12))

        # Desenha a tela de fim de jogo
        if game_over:
            texto_over = fonte.render(
                "GAME OVER! Pressione [E] para reiniciar ou [R] para sair",
                True,
                COR_GAME_OVER,
            )
            rect_over = texto_over.get_rect(
                center=(LARGURA // 2, ALTURA // 2)
            )
            tela.blit(texto_over, rect_over)

        pygame.display.flip()
        relogio.tick(FPS)


if __name__ == "__main__":
    executar_jogo()