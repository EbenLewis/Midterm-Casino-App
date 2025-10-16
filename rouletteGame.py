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

    def get_bet_types(self):
        return self.bet_types

    def validate_bet_amount(self, bet_amount, player_balance):
        if bet_amount == 0:
            return False, "quit"
        elif bet_amount < 0:
            return False, "Positive bets only."
        elif bet_amount > player_balance:
            return False, "Too much!"
        elif bet_amount < 1:
            return False, "Min $1."
        else:
            return True, ""

    def validate_bet_choice(self, choice):
        if choice == '0':
            return False, "quit"
        if choice in self.bet_types:
            return True, ""
        return False, "Invalid choice."

    def validate_straight_bet(self, number_input):
        try:
            number = int(number_input)
            if 0 <= number <= 36:
                return True, number, ""
            return False, None, "Enter 0-36."
        except ValueError:
            return False, None, "Enter a number."

    def spin_wheel(self):
        winning_number = random.choice(self.wheel_numbers)
        color = "Red" if winning_number in self.red_numbers else "Black" if winning_number != 0 else "Green"
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

def play_roulette(username, user_data):
    game = RouletteGame()
    current_balance = user_data['balance']
    
    game_data = {
        'balance': current_balance,
        'game_over': False,
        'message': "Welcome to Roulette!"
    }
    
    return game_data

