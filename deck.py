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

    
# Test the shuffled deck
print("Shuffled deck:")
for card in deck:
    rank, suit = get_card(card)
    print(f"{rank} of {suit}")
player_hand = []
dealer_hand = []
player_hand.append(deck.pop())
dealer_hand.append(deck.pop())
player_hand.append(deck.pop())
dealer_hand.append(deck.pop())