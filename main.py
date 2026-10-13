import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Casino Suite")
running = True
font = pygame.font.SysFont("arial", 64)
title = font.render("Casino Suite", True, (255, 255, 255))
blackjack_button = pygame.Rect(400, 450, 200, 60)
bjfont = pygame.font.SysFont("arial", 16)
blackjack_text = bjfont.render("Blackjack", True, (255, 255, 255))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and blackjack_button.collidepoint(event.pos):
            print("Mouse Clicked")
    screen.fill((30, 30, 30))
    screen.blit(title, title.get_rect(center=(500, 350)))
    pygame.draw.rect(screen, (40, 120, 80), blackjack_button)
    screen.blit(blackjack_text, blackjack_text.get_rect(center=blackjack_button.center))
    pygame.display.flip()
pygame.quit()