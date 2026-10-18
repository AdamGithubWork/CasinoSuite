import pygame
import random
from deck import get_card, get_hand_value, hit, dealer_turn, determine_winner

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Casino Suite")
running = True
font = pygame.font.SysFont("arial", 64)
title = font.render("Casino Suite", True, (255, 255, 255))
blackjack_button = pygame.Rect(400, 450, 200, 60)
hit_button = pygame.Rect(350, 600, 120, 50)
stand_button = pygame.Rect(530, 600, 120, 50)
play_again_button = pygame.Rect(400, 400, 200, 50)
bjfont = pygame.font.SysFont("arial", 16)
card_font = pygame.font.SysFont("arial", 28)
blackjack_text = bjfont.render("Blackjack", True, (255, 255, 255))
gamestate = "menu"
blackjack_deck = []
player_hand = []
dealer_hand = []
round_over = False
def start_blackjack_round():
    deck = list(range(52))
    random.shuffle(deck)

    player = []
    dealer = []

    for _ in range(2):
        hit(player, deck)
        hit(dealer, deck)

    return deck, player, dealer
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and blackjack_button.collidepoint(event.pos) and gamestate == "menu":
            gamestate = "blackjack"
            blackjack_deck, player_hand, dealer_hand = start_blackjack_round()
            round_over = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and gamestate == "blackjack":
            gamestate = "menu"
        if event.type == pygame.MOUSEBUTTONDOWN and gamestate == "blackjack":
            if not round_over:
                if hit_button.collidepoint(event.pos):
                    hit(player_hand, blackjack_deck)

                    if get_hand_value(player_hand) >= 21:
                        round_over = True

                elif stand_button.collidepoint(event.pos):
                    dealer_turn(dealer_hand, blackjack_deck)
                    round_over = True
            elif round_over:
                if play_again_button.collidepoint(event.pos):
                    blackjack_deck, player_hand, dealer_hand = start_blackjack_round()
                    round_over = False
    screen.fill((30, 30, 30))
    if gamestate == "menu":
        screen.blit(title, title.get_rect(center=(500, 350)))
        pygame.draw.rect(screen, (40, 120, 80), blackjack_button)
        screen.blit(blackjack_text, blackjack_text.get_rect(center=blackjack_button.center))
    elif gamestate == "blackjack":
        dealer_title = card_font.render(
            "Dealer's Hand", True, (255, 255, 255)
        )
        screen.blit(dealer_title, (100, 100))

        for i, card in enumerate(dealer_hand):
            if i > 0 and not round_over:
                card_label = "Hidden Card"
            else:
                rank, suit = get_card(card)
                card_label = f"{rank} of {suit}"

            card_text = card_font.render(
                card_label,
                True,
                (255, 255, 255)
            )

            screen.blit(card_text, (100, 150 + i * 35))

        player_title = card_font.render(
            "Your Hand", True, (255, 255, 255)
        )
        screen.blit(player_title, (100, 400))

        for i, card in enumerate(player_hand):
            rank, suit = get_card(card)

            card_text = card_font.render(
                f"{rank} of {suit}",
                True,
                (255, 255, 255)
            )

            screen.blit(card_text, (100, 450 + i * 35))

        hand_value = get_hand_value(player_hand)

        value_text = card_font.render(
            f"Hand Value: {hand_value}",
            True,
            (255, 255, 255)
        )

        screen.blit(value_text, (100, 550))
        pygame.draw.rect(screen, (40, 120, 80), hit_button)
        pygame.draw.rect(screen, (150, 50, 50), stand_button)

        hit_text = card_font.render("Hit", True, (255, 255, 255))
        stand_text = card_font.render("Stand", True, (255, 255, 255))
        if round_over:
            winner = determine_winner(player_hand, dealer_hand)

            if winner == "player":
                result = "You Win!"
            elif winner == "dealer":
                result = "Dealer Wins!"
            else:
                result = "Push! It's a Tie!"

            result_text = card_font.render(
                result,
                True,
                (255, 215, 0)
            )
            
            screen.blit(
                result_text,
                result_text.get_rect(center=(500, 350))
            )

            dealer_value = get_hand_value(dealer_hand)

            dealer_value_text = card_font.render(
                f"Dealer Value: {dealer_value}",
                True,
                (255, 255, 255)
            )

            screen.blit(dealer_value_text, (100, 300))
            pygame.draw.rect(screen, (40, 120, 80), play_again_button)

            play_again_text = card_font.render(
                "Play Again",
                True,
                (255, 255, 255)
            )

            screen.blit(
                play_again_text,
                play_again_text.get_rect(center=play_again_button.center)
            )
        screen.blit(
            hit_text,
            hit_text.get_rect(center=hit_button.center)
        )

        screen.blit(
            stand_text,
            stand_text.get_rect(center=stand_button.center)
        )
        
        
    pygame.display.flip()
pygame.quit()