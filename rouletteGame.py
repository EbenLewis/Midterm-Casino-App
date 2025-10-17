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

    def get_bet_info(self):
        bet_info = []
        for key, value in self.bet_types.items():
            bet_info.append(f"{key}. {value['name']} (Pays {value['payout']}:1)")
        return bet_info

    def process_bet_choice(self, choice_input):
        choice = choice_input.strip()
        if choice == '0':
            return None, "quit"
        if choice in self.bet_types:
            return choice, ""
        return None, "Invalid choice."

    def process_straight_bet(self, number_input):
        try:
            number = int(number_input)
            if 0 <= number <= 36:
                return {'number': number}, ""
            return {}, "Enter 0-36."
        except ValueError:
            return {}, "Enter a number."

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

    def process_bet_amount(self, bet_input, player_balance):
        try:
            bet_amount = float(bet_input)
            is_valid, message = self.validate_bet_amount(bet_amount, player_balance)
            if is_valid:
                return bet_amount, ""
            elif message == "quit":
                return None, "quit"
            else:
                return None, message
        except ValueError:
            return None, "Enter a number."

    def play_round(self, player_balance, bet_amount_input, bet_choice_input, straight_bet_input=None):
        self.current_balance = player_balance
        
        bet_amount, error = self.process_bet_amount(bet_amount_input, player_balance)
        if error:
            return {'error': error, 'game_over': error == "quit"}
        
        bet_type, error = self.process_bet_choice(bet_choice_input)
        if error:
            return {'error': error, 'game_over': error == "quit"}
        
        bet_details = {}
        if bet_type == '1':
            if straight_bet_input is None:
                return {'error': "Straight bet requires a number", 'game_over': False}
            bet_details, error = self.process_straight_bet(straight_bet_input)
            if error:
                return {'error': error, 'game_over': False}
        
        winning_number, winning_color = self.spin_wheel()
        did_win = self.check_win(bet_type, bet_details, winning_number, winning_color)
        payout = self.calculate_payout(bet_type, bet_amount, did_win)
        new_balance = player_balance + payout
        
        return {
            'winning_number': winning_number,
            'winning_color': winning_color,
            'bet_type': self.bet_types[bet_type]['name'],
            'bet_amount': bet_amount,
            'did_win': did_win,
            'payout': payout,
            'new_balance': new_balance,
            'game_over': False
        }

def play_roulette(username, user_data):
    game = RouletteGame()
    current_balance = user_data['balance']
    
    game_data = {
        'balance': current_balance,
        'game_over': False,
        'message': "Welcome to Roulette!"
    }
    
    return game_data
