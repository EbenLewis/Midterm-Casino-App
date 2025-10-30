import json
import random
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

SAVE_FILE = "slot_save.json"

SYMBOLS = ["🍒", "🍋", "🍊", "⭐", "🔔", "7️⃣"]
WEIGHTS = {"🍒": 6, "🍋": 6, "🍊": 6, "⭐": 4, "🔔": 3, "7️⃣": 1}

TRIPLE_PAYOUT = {"🍒": 10, "🍋": 12, "🍊": 14, "⭐": 18, "🔔": 25, "7️⃣": 50}
PAIR_PAYOUT = 3  # any 2-of-a-kind

def weighted_spin(n: int = 3) -> List[str]:
    symbols, weights = zip(*[(s, WEIGHTS[s]) for s in SYMBOLS])
    return random.choices(symbols, weights=weights, k=n)

def evaluate(slots: List[str], bet: int) -> Tuple[int, str]:
    a, b, c = slots
    if a == b == c:
        win = bet * TRIPLE_PAYOUT[a]
        return win, f"JACKPOT! {a}{b}{c} pays {TRIPLE_PAYOUT[a]}x ⇒ +${win}"
    if a == b or b == c or a == c:
        win = bet * PAIR_PAYOUT
        return win, f"Match! Two of a kind pays {PAIR_PAYOUT}x ⇒ +${win}"
    return 0, "No win this time."

def save_state(money: int, bet: int) -> None:
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump({"money": money, "bet": bet}, f)
    except Exception:
        pass

def load_state(default_money: int = 100, default_bet: int = 5) -> Tuple[int, int]:
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return int(data.get("money", default_money)), int(data.get("bet", default_bet))
    except Exception:
        return default_money, default_bet

@dataclass
class TextSlotMachine:
    money: int = field(default=100)
    bet: int = field(default=5)
    seed: Optional[int] = field(default=None)  # set for deterministic tests

    def __post_init__(self):
        if self.seed is not None:
            random.seed(self.seed)

    def can_bet(self) -> bool:
        return 1 <= self.bet <= self.money

    def spin_once(self) -> Tuple[List[str], int, str]:
        if not self.can_bet():
            return [], 0, "Not enough money for that bet."
        self.money -= self.bet
        slots = weighted_spin(3)
        win, msg = evaluate(slots, self.bet)
        self.money += win
        return slots, win, msg

    def show_animation(self, frames: int = 6, delay: float = 0.15) -> None:
        for _ in range(frames):
            temp = weighted_spin(3)
            print(f"[ {temp[0]} | {temp[1]} | {temp[2]} ]", end="\r", flush=True)
            time.sleep(delay)
        print(" " * 30, end="\r")  # clear line

    def play(self):
        print("🎰 Welcome to the Slot Machine! (type 'h' for help)")
        while self.money > 0:
            print(f"\n💰 Money: ${self.money} | Bet: ${self.bet}")
            print("1) Spin  2) Change bet  3) Auto-spin  4) Save & Quit  (h for help)")
            choice = input("Choose: ").strip().lower()

            if choice == "1":
                if not self.can_bet():
                    print("Not enough money for that bet.")
                    continue
                print(f"\nSpinning... (Bet ${self.bet})")
                self.show_animation()
                slots, _, msg = self.spin_once()
                print(f"[ {slots[0]} | {slots[1]} | {slots[2]} ]")
                print(msg)

            elif choice == "2":
                try:
                    new_bet = int(input("New bet amount: $").strip())
                    if 1 <= new_bet <= self.money:
                        self.bet = new_bet
                    else:
                        print("Bet must be between $1 and your current money.")
                except ValueError:
                    print("Please enter a valid integer.")

            elif choice == "3":
                try:
                    n = int(input("How many auto-spins? ").strip())
                    if n <= 0:
                        print("Enter a positive number.")
                        continue
                    for i in range(1, n + 1):
                        if not self.can_bet():
                            print("Stopped: not enough money.")
                            break
                        print(f"\nAuto-spin {i}/{n} (Bet ${self.bet})")
                        # faster animation for auto
                        self.show_animation(delay=0.08)
                        slots, _, msg = self.spin_once()
                        print(f"[ {slots[0]} | {slots[1]} | {slots[2]} ]  ->  {msg}")
                        time.sleep(0.05)
                except ValueError:
                    print("Please enter a valid integer.")

            elif choice in ("4", "save", "quit", "q", "exit"):
                save_state(self.money, self.bet)
                print(f"Saved. Thanks for playing! You leave with ${self.money}")
                break

            elif choice in ("h", "help"):
                print("\nHelp:")
                print("- Spin: play one round.")
                print("- Change bet: 1 to your current money.")
                print("- Auto-spin: run multiple spins quickly.")
                print("- Save & Quit: persist your balance to resume later.")

            else:
                print("Invalid choice.")
        else:
            print("You're out of money! Game over.")
            save_state(self.money, self.bet)

if __name__ == "__main__":
    money, bet = load_state()
    game = TextSlotMachine(money=money, bet=bet)
    game.play()
