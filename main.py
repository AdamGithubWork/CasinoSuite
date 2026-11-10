import pygame
import random
from deck import get_card, get_hand_value, hit, dealer_turn, determine_winner, is_blackjack

pygame.init()

screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Casino Suite")
running = True

font = pygame.font.SysFont("arial", 64)
bjfont = pygame.font.SysFont("arial", 16)
card_font = pygame.font.SysFont("arial", 28)

title = font.render("Casino Suite", True, (255, 255, 255))
blackjack_text = bjfont.render("Blackjack", True, (255, 255, 255))

blackjack_button = pygame.Rect(400, 450, 200, 60)
hit_button = pygame.Rect(350, 600, 120, 50)
stand_button = pygame.Rect(530, 600, 120, 50)
play_again_button = pygame.Rect(400, 400, 200, 50)
reset_button = pygame.Rect(400, 470, 200, 60)

bet_buttons = [
    (10, pygame.Rect(250, 350, 140, 60)),
    (50, pygame.Rect(430, 350, 140, 60)),
    (100, pygame.Rect(610, 350, 140, 60))
]

gamestate = "menu"
blackjack_deck = []
player_hand = []
dealer_hand = []
round_over = False

balance = 1000
current_bet = 0
payout_message = ""


def start_blackjack_round():
    deck = list(range(52))
    random.shuffle(deck)

    player = []
    dealer = []

    for _ in range(2):
        hit(player, deck)
        hit(dealer, deck)

    return deck, player, dealer


def finish_blackjack_round():
    global round_over, balance, payout_message

    if round_over:
        return

    round_over = True
    winner = determine_winner(player_hand, dealer_hand)

    if winner == "player":
        if is_blackjack(player_hand):
            winnings = current_bet * 3 // 2
        else:
            winnings = current_bet

        balance += current_bet + winnings
        payout_message = f"You won {winnings} chips!"

    elif winner == "push":
        balance += current_bet
        payout_message = "Push! Bet returned."

    else:
        payout_message = f"You lost {current_bet} chips."


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and gamestate != "menu":
                gamestate = "menu"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if gamestate == "menu":
                if blackjack_button.collidepoint(event.pos):
                    gamestate = "betting"

            elif gamestate == "betting":
                if balance < 10 and reset_button.collidepoint(event.pos):
                    balance = 1000

                for amount, button in bet_buttons:
                    if button.collidepoint(event.pos) and balance >= amount:
                        current_bet = amount
                        balance -= current_bet
                        payout_message = ""

                        blackjack_deck, player_hand, dealer_hand = start_blackjack_round()
                        round_over = False
                        gamestate = "blackjack"

                        if is_blackjack(player_hand) or is_blackjack(dealer_hand):
                            finish_blackjack_round()

                        break

            elif gamestate == "blackjack":
                if round_over:
                    if play_again_button.collidepoint(event.pos):
                        gamestate = "betting"

                else:
                    end_turn = False

                    if hit_button.collidepoint(event.pos):
                        hit(player_hand, blackjack_deck)

                        if get_hand_value(player_hand) >= 21:
                            end_turn = True

                    elif stand_button.collidepoint(event.pos):
                        end_turn = True

                    if end_turn:
                        if get_hand_value(player_hand) <= 21:
                            dealer_turn(dealer_hand, blackjack_deck)

                        finish_blackjack_round()

    screen.fill((30, 30, 30))

    if gamestate == "menu":
        screen.blit(title, title.get_rect(center=(500, 350)))

        pygame.draw.rect(screen, (40, 120, 80), blackjack_button)
        screen.blit(
            blackjack_text,
            blackjack_text.get_rect(center=blackjack_button.center)
        )

    elif gamestate == "betting":
        betting_title = font.render(
            "Place Your Bet",
            True,
            (255, 255, 255)
        )
        screen.blit(
            betting_title,
            betting_title.get_rect(center=(500, 220))
        )

        chips_text = card_font.render(
            f"Available Chips: {balance}",
            True,
            (255, 215, 0)
        )
        screen.blit(
            chips_text,
            chips_text.get_rect(center=(500, 290))
        )

        for amount, button in bet_buttons:
            if balance >= amount:
                button_color = (40, 120, 80)
            else:
                button_color = (80, 80, 80)

            pygame.draw.rect(screen, button_color, button)

            bet_text = card_font.render(
                f"{amount} Chips",
                True,
                (255, 255, 255)
            )
            screen.blit(
                bet_text,
                bet_text.get_rect(center=button.center)
            )

        if balance < 10:
            out_of_chips = card_font.render(
                "You're out of chips!",
                True,
                (255, 100, 100)
            )
            screen.blit(
                out_of_chips,
                out_of_chips.get_rect(center=(500, 450))
            )

            pygame.draw.rect(screen, (40, 120, 80), reset_button)

            reset_text = card_font.render(
                "Reset Chips",
                True,
                (255, 255, 255)
            )
            screen.blit(
                reset_text,
                reset_text.get_rect(center=reset_button.center)
            )

    elif gamestate == "blackjack":
        balance_text = card_font.render(
            f"Chips: {balance}",
            True,
            (255, 215, 0)
        )
        screen.blit(balance_text, (750, 30))

        bet_text = card_font.render(
            f"Bet: {current_bet}",
            True,
            (255, 215, 0)
        )
        screen.blit(bet_text, (750, 70))

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

        if not round_over:
            pygame.draw.rect(screen, (40, 120, 80), hit_button)
            pygame.draw.rect(screen, (150, 50, 50), stand_button)

            hit_text = card_font.render(
                "Hit", True, (255, 255, 255)
            )
            stand_text = card_font.render(
                "Stand", True, (255, 255, 255)
            )

            screen.blit(
                hit_text,
                hit_text.get_rect(center=hit_button.center)
            )
            screen.blit(
                stand_text,
                stand_text.get_rect(center=stand_button.center)
            )

        else:
            winner = determine_winner(player_hand, dealer_hand)

            if winner == "player":
                if is_blackjack(player_hand):
                    result = "Blackjack!"
                else:
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

            pygame.draw.rect(
                screen,
                (40, 120, 80),
                play_again_button
            )

            play_again_text = card_font.render(
                "Play Again",
                True,
                (255, 255, 255)
            )
            screen.blit(
                play_again_text,
                play_again_text.get_rect(center=play_again_button.center)
            )

            payout_text = card_font.render(
                payout_message,
                True,
                (255, 215, 0)
            )
            screen.blit(
                payout_text,
                payout_text.get_rect(center=(500, 490))
            )

    pygame.display.flip()

pygame.quit()
