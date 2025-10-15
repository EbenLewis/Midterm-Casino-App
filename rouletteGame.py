import random

class RouletteGame:
    def __init__(self):
        self.wheel_numbers = list(range(0, 37))
        self.red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
        self.bet_types = {
            '1': {'name': 'Straight', 'payout': 35},
            '2': {'name': 'Red', 'payout': 1},
            '3': {'name': 'Black', 'payout': 1},
            '4': {'name': 'Even', 'payout': 1},
            '5': {'name': 'Odd', 'payout': 1},
            '6': {'name': '1-18', 'payout': 1},
            '7': {'name': '19-36', 'payout': 1}
        }

    def display_bets(self):
        print("\nRoulette Bets:")
        for key, value in self.bet_types.items():
            print(f"{key}. {value['name']} (Pays {value['payout']}:1)")

    def get_bet_choice(self):
        while True:
            choice = input("\nChoose bet (1-7) or 0 to quit: ").strip()
            if choice == '0':
                return None
            if choice in self.bet_types:
                return choice
            print("Invalid choice.")

    def get_bet_details(self, bet_type):
        if bet_type == '1':
            while True:
                try:
                    number = int(input("Enter number (0-36): "))
                    if 0 <= number <= 36:
                        return {'number': number}
                    print("Enter 0-36.")
                except ValueError:
                    print("Enter a number.")
        return {}
