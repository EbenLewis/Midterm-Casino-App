import random
#create card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11 
}
#create deck and shuffle
class Deck:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = list(CARD_VALUES.keys())

    def __init__(self):
        self.cards = [{'rank': r, 'suit': s} for s in self.SUITS for r in self.RANKS]
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            raise IndexError("The deck is empty.")
        return self.cards.pop()

#create hand for player and dealer
class Hand:
    def __init__(self, owner: str):
        self.owner = owner
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def value(self) -> int:
        total, aces = 0, 0
        for c in self.cards:
            total += CARD_VALUES[c['rank']]
            if c['rank'] == 'A':
                aces += 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

# Display hand for the user and player
    def show(self, hide_one=False):
        print(f"\n{self.owner}'s hand:")
        if hide_one and len(self.cards) >= 2:
            c0 = self.cards[0]
            print(f"  {c0['rank']} of {c0['suit']}")
            print("  [Hidden Card]")
            shown_val = Hand(self.owner)
            shown_val.cards = [self.cards[0]]
            print(f"Total value (showing): {CARD_VALUES[c0['rank']] if c0['rank']!='A' else 11}")
        else:
            for c in self.cards:
                print(f"  {c['rank']} of {c['suit']}")
            print(f"Total value: {self.value()}")

#create main game class
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player = Hand("Your")
        self.dealer = Hand("Dealer's")

    def initial_deal(self):
        for _ in range(2):
            self.player.add(self.deck.deal())
            self.dealer.add(self.deck.deal())

    #option for player to hit or stand 
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

    #dealer's turn logic
    def dealer_turn(self):
        print("\nDealer's turn:")
        self.dealer.show(hide_one=False)
        while self.dealer.value() < 17:
            self.dealer.add(self.deck.deal())
            self.dealer.show(hide_one=False)

    #settle the game outcome
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
    #play a full round of blackjack
    def play_round(self):
        self.__init__()
        print("Welcome to Blackjack!")
        self.initial_deal()
        proceed = self.player_turn()
        if proceed and self.player.value() <= 21:
            self.dealer_turn()
            self.settle()
    #option to play again 
    def run(self):
        while True:
            self.play_round()
            again = input("\nPlay again? (yes/no): ").strip().lower()
            if again != 'yes':
                print("Thanks for playing!")
                break

if __name__ == "__main__":
    BlackjackGame().run()