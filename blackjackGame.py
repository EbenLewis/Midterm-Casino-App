import random

# Card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11  # Ace initially 11, can be 1
}

"""Gameplay overview
-----------------
1) A shuffled deck is created; you and the dealer each have two cards at start.
2) Player turn: choose to Hit or Stand until you reach 21 or bust (>21).
3) Dealer turn: once the player stands (and hasn't busted), the dealer draws until
   the dealer's hand value is at least 17 (standard house rule).
4) Outcomes: blackjack (21 on initial deal), player win/lose, dealer bust, or push (tie).
"""

def create_deck():
    """Creates a standard 52-card deck.
     Returns
    -------
    list[Card]
        A shuffled list of card dicts like {'rank': 'K', 'suit': 'Hearts'}."""
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = list(CARD_VALUES.keys())
    deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def deal_card(deck):
    """Deals a single card from the deck.
     Parameters
    ----------
    deck : list[Card]
        The deck from which to deal.

    Returns
    -------
    Card
        The dealt card.

    Raises
    ------
    IndexError
        If the deck is empty."""
    return deck.pop()

def calculate_hand_value(hand):
    """Calculates the value of a hand, handling Aces.
     Aces count as 11 by default and are reduced to 1 as needed to keep the hand
    at 21 or below.

    Parameters
    ----------
    hand : list[Card]
        The player's or dealer's hand.

    Returns
    -------
    int
        The integer hand value according to Blackjack rules."""
    value = 0
    num_aces = 0
    for card in hand:
        value += CARD_VALUES[card['rank']]
        if card['rank'] == 'A':
            num_aces += 1
    
    # Adjust for Aces if hand busts
    while value > 21 and num_aces > 0:
        value -= 10  # Change Ace value from 11 to 1
        num_aces -= 1
    return value

def display_hand(player_name, hand, hide_one=False):
    """Displays a player's hand.
    
    Parameters
    ----------
    player_name : str
        Display name, e.g., "Your" or "Dealer's".
    hand : list[Card]
        The hand to display.
    hide_one : bool, optional
        If True, shows only the first card and hides the second (dealer's initial state)."""
    print(f"\n{player_name}'s hand:")
    if hide_one:
        print(f"  {hand[0]['rank']} of {hand[0]['suit']}")
        print("  [Hidden Card]")
    else:
        for card in hand:
            print(f"  {card['rank']} of {card['suit']}")
    print(f"Total value: {calculate_hand_value(hand)}")

def play_blackjack():
    """Main function to play a game of Blackjack.
    Flow:
    -----
    1) Create and shuffle a deck; deal two cards to player and dealer.
    2) Player turn: prompt Hit/Stand until blackjack (21), stand, or bust.
    3) Dealer turn: draw until total >= 17 (if player hasn't busted).
    4) Compare totals to determine the outcome, then prompt to play again.
    """
    print("Welcome to Blackjack!")
    deck = create_deck()

    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    # Player's turn
    while True:
        display_hand("Your", player_hand)
        display_hand("Dealer's", dealer_hand, hide_one=True)

        player_value = calculate_hand_value(player_hand)
        if player_value == 21:
            print("Blackjack! You win!")
            break
        elif player_value > 21:
            print("You busted! Dealer wins.")
            break

        choice = input("Do you want to [H]it or [S]tand? ").lower()
        if choice == 'h':
            player_hand.append(deal_card(deck))
        elif choice == 's':
            break
        else:
            print("Invalid input. Please enter 'h' or 's'.")

    # Dealer's turn (if player hasn't busted)
    if calculate_hand_value(player_hand) <= 21:
        print("\nDealer's turn:")
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card(deck))
            display_hand("Dealer's", dealer_hand)
        
        dealer_value = calculate_hand_value(dealer_hand)
        player_value = calculate_hand_value(player_hand)

        if dealer_value > 21:
            print("Dealer busted! You win!")
        elif dealer_value > player_value:
            print("Dealer wins!")
        elif dealer_value < player_value:
            print("You win!")
        else:
            print("It's a push (tie)!")

    play_again = input("\nPlay again? (yes/no): ").lower()
    if play_again == 'yes':
        play_blackjack()
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    play_blackjack()