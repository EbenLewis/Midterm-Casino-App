import random
import time

class TextSlotMachine:
    def __init__(self):
        self.money = 100
        self.bet = 5
        
    def show_slots(self):
        symbols = ["🍒", "🍋", "🍊", "⭐", "🔔", "7️⃣"]
        return [random.choice(symbols) for _ in range(3)]
    
    def spin(self):
        if self.money < self.bet:
            print("Not enough money!")
            return
            
        self.money -= self.bet
        print(f"\nSpinning... Bet: ${self.bet}")
        
        # Show spinning animation
        for i in range(5):
            slots = [random.choice(["🍒", "🍋", "🍊", "⭐", "🔔", "7️⃣"]) for _ in range(3)]
            print(f"[ {slots[0]} | {slots[1]} | {slots[2]} ]", end="\r")
            time.sleep(0.2)
        
        # Final result
        final_slots = self.show_slots()
        print(f"[ {final_slots[0]} | {final_slots[1]} | {final_slots[2]} ]")
        
        # Check win
        if final_slots[0] == final_slots[1] == final_slots[2]:
            win = self.bet * 10
            self.money += win
            print(f"JACKPOT! You won ${win}!")
        elif final_slots[0] == final_slots[1] or final_slots[1] == final_slots[2]:
            win = self.bet * 3
            self.money += win
            print(f"Match! You won ${win}!")
        else:
            print("No win this time.")
    
    def play(self):
        while self.money > 0:
            print(f"\n💰 Money: ${self.money} | Current Bet: ${self.bet}")
            print("1. Spin (costs bet amount)")
            print("2. Change bet")
            print("3. Quit")
            
            choice = input("Choose(between 1 to 3): ")
            
            if choice == "1":
                self.spin()
            elif choice == "2":
                try:
                    new_bet = int(input("New bet amount: $"))
                    if 1 <= new_bet <= self.money:
                        self.bet = new_bet
                    else:
                        print("Invalid bet amount")
                except:
                    print("Enter a number")
            elif choice == "3":
                print(f"Thanks for playing! You leave with ${self.money}")
                break
            else:
                print("Invalid choice")
        
        if self.money <= 0:
            print("You're out of money! Game over.")

# Run the game
if __name__ == "__main__":
    game = TextSlotMachine()
    game.play()