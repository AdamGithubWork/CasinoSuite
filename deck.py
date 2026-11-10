import random

# Each card is represented by an integer from 0 to 51.
# Suits: 0 = Hearts, 1 = Diamonds, 2 = Clubs, 3 = Spades
# Ranks: 0 = Ace, 1 = 2, ..., 12 = King

suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
ranks = ["Ace", "2", "3", "4", "5", "6", "7",
         "8", "9", "10", "Jack", "Queen", "King"]

# Create a standard 52-card deck
deck = list(range(52))

random.shuffle(deck)

# Convert a card ID into its rank and suit
def get_card(card):
    suit = suits[card // 13]
    rank = ranks[card % 13]
    return rank, suit

def get_card_value(card):
    val = card% 13
    if(val == 0):
        return 11
    elif(val > 9):
        return 10
    else:
        return val +1
def get_hand_value(hand):
    total = 0
    aces = 0
    for card in hand:
        total += get_card_value(card)

        if card % 13 == 0:
            aces += 1

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total
def hit(hand, deck):
    hand.append(deck.pop())
def player_turn(player_hand, deck):
    while get_hand_value(player_hand) < 21:
        choice = input("Hit or Stand? (h/s): ").lower()

        if choice == "h":
            hit(player_hand, deck)
            print("Your hand:", [get_card(card) for card in player_hand])
            print("Hand value:", get_hand_value(player_hand))

        elif choice == "s":
            break

        else:
            print("Invalid choice. Enter h or s.")
def dealer_turn(dealer_hand, deck):
    while get_hand_value(dealer_hand)<17:
        dealer_hand.append(deck.pop())
def determine_winner(player_hand, dealer_hand):
    player_blackjack = is_blackjack(player_hand)
    dealer_blackjack = is_blackjack(dealer_hand)

    if player_blackjack and not dealer_blackjack:
        return "player"
    elif dealer_blackjack and not player_blackjack:
        return "dealer"

    player_value = get_hand_value(player_hand)
    dealer_value = get_hand_value(dealer_hand)

    if player_value > 21:
        return "dealer"
    elif dealer_value > 21:
        return "player"
    elif player_value > dealer_value:
        return "player"
    elif player_value < dealer_value:
        return "dealer"
    else:
        return "push"
def is_blackjack(hand):
    return len(hand) == 2 and get_hand_value(hand) == 21    
# Test the shuffled deck
if __name__ == "__main__":
    player_hand = []
    dealer_hand = []
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    print("Player:", [get_card(card) for card in player_hand])
    print("Player value:", get_hand_value(player_hand))

    print("Dealer:", [get_card(card) for card in dealer_hand])
    print("Dealer value:", get_hand_value(dealer_hand))

    player_turn(player_hand, deck)

    if get_hand_value(player_hand) <= 21:
        dealer_turn(dealer_hand, deck)

    print("\nFinal dealer hand:", [get_card(card) for card in dealer_hand])
    print("Dealer value:", get_hand_value(dealer_hand))

    print("Winner:", determine_winner(player_hand, dealer_hand))