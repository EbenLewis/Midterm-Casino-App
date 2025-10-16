import random

CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11 
}
#this is good logic! doesn't need change
def create_deck():
    #Creates a standard 52-card deck.
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = list(CARD_VALUES.keys())
    deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def deal_card(deck):
    #Deals a single card from the deck.
    return deck.pop()

def calculate_hand_value(hand):
    #Calculates the value of a hand, handling Aces
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
    #Displays the player's or dealer's hand.
    print(f"\n{player_name}'s hand:")
    if hide_one:
        print(f"  {hand[0]['rank']} of {hand[0]['suit']}")
        print("  [Hidden Card]")
    else:
        for card in hand:
            print(f"  {card['rank']} of {card['suit']}")
    print(f"Total value: {calculate_hand_value(hand)}")

#logic is good, just needs to be integratable with main (just logic, takes input inside the function parameters and returns output)
def play_blackjack():
    """Main function to play a game of Blackjack."""
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
            for c in self.cards:
                print(f"  {c['rank']} of {c['suit']}")
            print(f"Total value: {self.value()}")

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player = Hand("Your")
        self.dealer = Hand("Dealer's")

    def initial_deal(self):
        for _ in range(2):
            self.player.add(self.deck.deal())
            self.dealer.add(self.deck.deal())

    def player_turn(self) -> bool:
        while True:
            self.player.show(hide_one=False)
            self.dealer.show(hide_one=True)

            pv = self.player.value()
            if pv == 21:
                print("Blackjack! You win!")
                return False
            if pv > 21:
                print("You busted! Dealer wins.")
                return False

            choice = input("Do you want to [H]it or [S]tand? ").strip().lower()
            if choice == 'h':
                self.player.add(self.deck.deal())
            elif choice == 's':
                return True
            else:
                print("Invalid input. Please enter 'h' or 's'.")

    def dealer_turn(self):
        print("\nDealer's turn:")
        self.dealer.show(hide_one=False)
        while self.dealer.value() < 17:
            self.dealer.add(self.deck.deal())
            self.dealer.show(hide_one=False)

    def settle(self):
        dv = self.dealer.value()
        pv = self.player.value()
        if dv > 21:
            print("Dealer busted! You win!")
        elif dv > pv:
            print("Dealer wins!")
        elif dv < pv:
            print("You win!")
        else:
            print("It's a push (tie)!")

    def play_round(self):
        self.__init__()
        print("Welcome to Blackjack!")
        self.initial_deal()
        proceed = self.player_turn()
        if proceed and self.player.value() <= 21:
            self.dealer_turn()
            self.settle()

    def run(self):
        while True:
            self.play_round()
            again = input("\nPlay again? (yes/no): ").strip().lower()
            if again != 'yes':
                print("Thanks for playing!")
                break

if __name__ == "__main__":
    BlackjackGame().run()