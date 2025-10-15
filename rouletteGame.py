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

    def spin_wheel(self):
        winning_number = random.choice(self.wheel_numbers)
        color = "Red" if winning_number in self.red_numbers else "Black" if winning_number != 0 else "Green"
        print(f"Ball: {winning_number} {color}")
        return winning_number, color

    def check_win(self, bet_type, bet_details, winning_number, winning_color):
        if bet_type == '1':
            return bet_details.get('number') == winning_number
        elif bet_type == '2':
            return winning_number in self.red_numbers
        elif bet_type == '3':
            return winning_number not in self.red_numbers and winning_number != 0
        elif bet_type == '4':
            return winning_number % 2 == 0 and winning_number != 0
        elif bet_type == '5':
            return winning_number % 2 == 1
        elif bet_type == '6':
            return 1 <= winning_number <= 18
        elif bet_type == '7':
            return 19 <= winning_number <= 36
        return False

    def calculate_payout(self, bet_type, bet_amount, did_win):
        if not did_win:
            return -bet_amount
        payout_ratio = self.bet_types[bet_type]['payout']
        return bet_amount * payout_ratio

    def validate_bet(self, player_balance):
        while True:
            try:
                bet_input = input(f"Bet (1-{player_balance}) or 0 to quit: $").strip()
                bet_amount = float(bet_input)
                
                if bet_amount == 0:
                    return None
                elif bet_amount < 0:
                    print("Positive bets only.")
                elif bet_amount > player_balance:
                    print("Too much!")
                elif bet_amount < 1:
                    print("Min $1.")
                else:
                    return bet_amount
                    
            except ValueError:
                print("Enter a number.")

    def play_round(self, player_balance):
        print(f"\nBalance: ${player_balance}")
        
        bet_amount = self.validate_bet(player_balance)
        if bet_amount is None:
            return player_balance
        
        self.display_bets()
        bet_type = self.get_bet_choice()
        if bet_type is None:
            return player_balance
        
        bet_details = self.get_bet_details(bet_type)
        winning_number, winning_color = self.spin_wheel()
        
        did_win = self.check_win(bet_type, bet_details, winning_number, winning_color)
        payout = self.calculate_payout(bet_type, bet_amount, did_win)
        new_balance = player_balance + payout
        
        if did_win:
            print(f"Win: ${payout}!")
        else:
            print(f"Lose: ${bet_amount}!")
        
        print(f"New Balance: ${new_balance}")
        return new_balance

def play_roulette(username, user_data):
    game = RouletteGame()
    
    print("\n ROULETTE!!")
    
    current_balance = user_data['balance']
    
    while current_balance > 0:
        current_balance = game.play_round(current_balance)
        
        play_again = input("\nAgain? (y/n): ").lower().strip()
        if play_again != 'y':
            break
    
    user_data['balance'] = current_balance
    return user_data

if __name__ == "__main__":
    test_user = {'balance': 100, 'money_won': 0, 'money_lost': 0}
    play_roulette("test_player", test_user)
