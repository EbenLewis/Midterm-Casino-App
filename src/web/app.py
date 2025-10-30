from flask import Flask, request, redirect, url_for, session
from ..user.user_manager import UserManager, User
from ..games.blackjack import BlackjackGame
from ..games.roulette import RouletteGame

app = Flask(__name__)
app.secret_key = "not_very_secret_key"  # hash this later


# landing page
# WORKS
@app.route("/", methods=["GET", "POST"])
def home():
    error_message = request.args.get("error", "")
    error_html = f'<p style="color: red;">{error_message}</p>' if error_message else ""
    html = f"""
    <h1> Welcome to the casino" </h1>
    <p> let's go gambling! <p>
    {error_html}
    <button type="button" onclick="window.location.href='/login'">Login</button>
    <button type="button" onclick="window.location.href='/createaccount'">Create Account</button>
    """
    return html


# home page after login for user
# WORKS
@app.route("/userhome")
def user_home():
    userdata = UserManager.view_data(session.get("username"))
    if "user_preferred_name" in userdata:
        name = userdata["user_preferred_name"]
    else:
        name = userdata["username"]
    html = (
        f"""
    <h1> Welcome back, """
        + name
        + """</h1>
    <p> let's go gambling! <p>
    <p> Total Money: $"""
        + f"{userdata['money_total']:.2f}"
        + """</p>
    <button type="button" onclick="window.location.href='/userdata'">View user data</button>
    <button type="button" onclick="window.location.href='/blackjack'">Play Blackjack</button>
    <button type="button" onclick="window.location.href='/roulette'">Play Roulette</button>
    <button type="button" onclick="window.location.href='/slots'">Play Slots</button>
    <button type="button" onclick="window.location.href='/logout'">Logout</button>
    """
    )
    return html


# display user data upon request
# WORKS
@app.route("/userdata")
def view_account():
    if not session.get("logged_in"):
        return redirect(url_for("home"))
    else:
        userdata = UserManager.view_data(session.get("username"))
        html = (
            """
        <h1> This is your user data: </h1>
        <p> Username: """
            + userdata["username"]
            + """</p>
        <p> UserID: """
            + str(userdata["userid"])
            + """</p>
        <p> Total Money: $"""
            + f"{userdata['money_total']:.2f}"
            + """</p>
        <p> Money Won: $"""
            + f"{userdata['money_won']:.2f}"
            + """</p>
        <p> Money Lost: $"""
            + f"{userdata['money_lost']:.2f}"
            + """</p>
        <button type="button" onclick="window.location.href='/changefunds'">Change Funds</button>
        <button type="button" onclick="window.location.href='/userhome'">Return to home</button>
        """
        )
        return html


# create account page
# WORKS
@app.route("/createaccount", methods=["GET", "POST"])
def create_account():
    html = """
    <h1>Create your account</h1>
    <form action="/createaccount" method="POST">
        <label for="username">Add username:</label>
        <input type="text" id="username" name="username"><br><br>

        <label for="password">Add password:</label>
        <input type="text" id="password" name="password"><br><br>

        <label for="initial_balance">Add initial funds:</label>
        <input type="number" id="initial_balance" name="initial_balance"><br><br>

        <label for="preferred_name">Add a preferred name (optional):</label>
        <input type="text" id="preferred_name" name="preferred_name"><br><br>
        
        <input type="submit" value="Submit">
    </form>
    """

    # account creation functionality
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        initial_balance = float(request.form["initial_balance"])
        user_preferred_name = request.form["preferred_name"]
        UserManager.new_user(username, password, initial_balance, user_preferred_name)
        session["username"] = username
        session["logged_in"] = True
        return redirect(url_for("user_home"))

    return html


# login route
# WORKS
@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = request.args.get("error", "")
    error_html = f'<p style="color: red;">{error_message}</p>' if error_message else ""

    html = f"""
    <form action="/login" method="POST"> 
        <label for = "username">Enter your username</label>
        <input type="text" id="username" name="username"><br><br>

        <label for = "password">Enter your password:</label>
        <input type="text" id="password" name="password"><br><br>

        <input type="submit" value="Submit">
    </form>
    {error_html}
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success = UserManager.login(username, password)
        # uses session variables for each user to keep them seperate
        if success:
            session["username"] = username
            session["logged_in"] = True
            return redirect(url_for("user_home"))
        else:
            return redirect(url_for("home", error="Invalid login credentials"))

    return html


# change funds route
# WORKS
@app.route("/changefunds", methods=["GET", "POST"])
def change_funds():
    if not session.get("logged_in"):
        return redirect(url_for("home"))

    error_message = request.args.get("error", "")
    error_html = f'<p style="color: red;">{error_message}</p>' if error_message else ""

    html = f"""
    <form action="/changefunds" method="POST">
        <label for="amount">Enter amount to deposit/remove (use negative numbers to remove):</label>
        <input type="number" id="amount" name="amount" step="0.01"><br><br>
        <input type="submit" value="Submit">
        </form>
    {error_html}"""

    if request.method == "POST":
        try:
            amount_str = request.form.get("amount", "")
            if not amount_str:
                return redirect(url_for("change_funds", error="Invalid deposit amount"))

            amount = float(amount_str)

            #check if deposit amounts are within limit
            if amount > 0:
                if amount < 0.01:
                    return redirect(
                        url_for("change_funds", error="Invalid deposit amount")
                    )
                if amount > 1000000000000.00:
                    return redirect(
                        url_for("change_funds", error="Invalid deposit amount")
                    )

            #check if withdrawal amounts are within limit
            elif amount < 0:
                if amount > -0.01:
                    return redirect(
                        url_for("change_funds", error="Invalid deposit amount")
                    )

            #zero handling
            else:
                return redirect(url_for("view_account"))

            user = User(session.get("username"))
            if amount > 0:
                user.add_funds(amount)
            elif amount < 0:
                user.remove_funds(-amount)

            return redirect(url_for("view_account"))

        except (ValueError, TypeError):
            return redirect(url_for("change_funds", error="Invalid deposit amount"))

    return html


# Blackjack routes
@app.route("/blackjack", methods=["GET", "POST"])
def blackjack():
    html = """
    <button type="button" onclick="window.location.href='/blackjack/active'">Play blackjack?</button>
    <button type="button" onclick="window.location.href='/userhome'">Return to home</button>
    """
    return html


# route to play the actual game in
@app.route("/blackjack/active", methods=["GET", "POST"])
def blackjack_running():
    if not session.get("logged_in"):
        return redirect(url_for("home"))

    userdata = UserManager.view_data(session.get("username"))
    balance = userdata.get("money_total", 0.0)

    error_message = request.args.get("error", "")
    error_html = f'<p style="color: red;">{error_message}</p>' if error_message else ""

    # Handle betting
    if request.method == "POST" and "bet" in request.form:
        try:
            bet_str = request.form.get("bet", "")
            if not bet_str:
                return redirect(
                    url_for("blackjack_running", error="Invalid bet amount")
                )

            bet = float(bet_str)

            # check if bet is positive
            if bet < 0.01:
                return redirect(
                    url_for("blackjack_running", error="Invalid bet amount")
                )

            # check bet against balance
            if bet > balance:
                return redirect(
                    url_for("blackjack_running", error="Insufficient funds for bet")
                )

            session["blackjack_bet"] = bet

            # Create new game and deal initial cards
            game = BlackjackGame()
            game.initial_deal()

            # Store game state in session
            session["blackjack_game"] = {
                "player_cards": game.player.cards,
                "dealer_cards": game.dealer.cards,
                "deck_cards": game.deck.cards,
            }

            return redirect(url_for("blackjack_game"))

        except (ValueError, TypeError):
            return redirect(url_for("blackjack_running", error="Invalid bet amount"))

    html = f"""
    <h1>Blackjack</h1>
    <p><strong>Balance: ${balance:.2f}</strong></p>
    {error_html}
    <form action="/blackjack/active" method="POST">
        <label for="bet">Place your bet:</label>
        <input type="number" id="bet" name="bet" step="0.01" required>
        <button type="submit">Deal Cards</button>
    </form>
    <button type="button" onclick="window.location.href='/userhome'">Back to home</button>
    """
    return html


@app.route("/blackjack/game", methods=["GET", "POST"])
def blackjack_game():
    if not session.get("logged_in") or "blackjack_bet" not in session:
        return redirect(url_for("blackjack_running"))

    # Recreate game from session
    game = BlackjackGame()
    game_data = session["blackjack_game"]
    game.player.cards = game_data["player_cards"]
    game.dealer.cards = game_data["dealer_cards"]
    game.deck.cards = game_data["deck_cards"]

    # Handle hit/stand actions
    if request.method == "POST":
        action = request.form.get("action")

        if action == "hit":
            new_card = game.deck.deal()
            game.player.add(new_card)
        elif action == "stand":
            # Dealer plays
            while game.dealer.value() < 17:
                new_card = game.deck.deal()
                game.dealer.add(new_card)

        # Update session
        session["blackjack_game"] = {
            "player_cards": game.player.cards,
            "dealer_cards": game.dealer.cards,
            "deck_cards": game.deck.cards,
        }

    player_total = game.player.value()
    dealer_total = game.dealer.value()
    bet = session["blackjack_bet"]

    # Check game end conditions
    game_over = False
    result = ""
    show_settle = False

    if player_total > 21:
        game_over = True
        result = "Bust! You lose!"
        show_settle = True
    elif request.method == "POST" and request.form.get("action") == "stand":
        game_over = True
        if dealer_total > 21:
            result = "Dealer busts! You win!"
        elif dealer_total > player_total:
            result = "Dealer wins!"
        elif dealer_total < player_total:
            result = "You win!"
        else:
            result = "Push!"
        show_settle = True

    # Format cards for display
    def format_cards(cards):
        return [f"{card['rank']} of {card['suit']}" for card in cards]

    player_cards_str = ", ".join(format_cards(game.player.cards))

    if game_over or (
        request.method == "POST" and request.form.get("action") == "stand"
    ):
        dealer_cards_str = ", ".join(format_cards(game.dealer.cards))
        dealer_display = f"Dealer cards: {dealer_cards_str} (Total: {dealer_total})"
    else:
        # Show only first dealer card
        first_card = (
            format_cards([game.dealer.cards[0]])[0] if game.dealer.cards else ""
        )
        dealer_display = f"Dealer cards: {first_card}, [Hidden Card]"

    html = f"""
    <h1>Blackjack Game</h1>
    <p><strong>Bet: ${bet:.2f}</strong></p>
    <p><strong>Your cards: {player_cards_str} (Total: {player_total})</strong></p>
    <p><strong>{dealer_display}</strong></p>
    """

    if show_settle:
        html += f"""
        <p><strong>{result}</strong></p>
        <form action="/blackjack/settle" method="POST">
            <button type="submit">Settle Game</button>
        </form>
        """
    else:
        html += """
        <form action="/blackjack/game" method="POST" style="display: inline;">
            <input type="hidden" name="action" value="hit">
            <button type="submit">Hit</button>
        </form>
        <form action="/blackjack/game" method="POST" style="display: inline;">
            <input type="hidden" name="action" value="stand">
            <button type="submit">Stand</button>
        </form>
        """

    return html


@app.route("/blackjack/settle", methods=["POST"])
def blackjack_settle():
    if not session.get("logged_in") or "blackjack_bet" not in session:
        return redirect(url_for("blackjack_running"))

    # Recreate game from session to get final results
    game = BlackjackGame()
    game_data = session["blackjack_game"]
    game.player.cards = game_data["player_cards"]
    game.dealer.cards = game_data["dealer_cards"]

    player_total = game.player.value()
    dealer_total = game.dealer.value()
    bet = session["blackjack_bet"]

    # Determine winner and update money
    user = User(session.get("username"))

    if player_total > 21:
        result = "You busted! You lose!"
        user.update_money_lost(bet)
    elif dealer_total > 21:
        result = "Dealer busts! You win!"
        user.update_money_won(bet)
    elif dealer_total > player_total:
        result = "Dealer wins!"
        user.update_money_lost(bet)
    elif dealer_total < player_total:
        result = "You win!"
        user.update_money_won(bet)
    else:
        result = "Push! No money changes hands."

    # Get updated balance
    userdata = UserManager.view_data(session.get("username"))
    new_balance = userdata.get("money_total", 0.0)

    # Clear session
    session.pop("blackjack_bet", None)
    session.pop("blackjack_game", None)

    html = f"""
    <h1>Game Settled</h1>
    <p><strong>{result}</strong></p>
    <p><strong>New Balance: ${new_balance:.2f}</strong></p>
    <button type="button" onclick="window.location.href='/blackjack/active'">Play Again</button>
    <button type="button" onclick="window.location.href='/userhome'">Home</button>
    """

    return html


# Roulette routes
@app.route("/roulette", methods=["GET", "POST"])
def roulette():
    html = """
    <p> Welcome to roulette<p>
    <button type="button" onclick="window.location.href='/roulette/active'">Play roulette?</button>
    <button type="button" onclick="window.location.href='/userhome'">Return to home</button>
    """

    return html


@app.route("/roulette/active", methods=["GET", "POST"])
def roulette_running():
    if not session.get("logged_in"):
        return redirect(url_for("home"))

    userdata = UserManager.view_data(session.get("username"))
    balance = userdata.get("money_total", 0.0)

    error_message = request.args.get("error", "")
    error_html = f'<p style="color: red;">{error_message}</p>' if error_message else ""

    if request.method == "POST":
        try:
            bet_str = request.form.get("bet", "")
            if not bet_str:
                return redirect(url_for("roulette_running", error="Invalid bet amount"))

            bet = float(bet_str)

            #check that bet is positive
            if bet < 0.01:
                return redirect(url_for("roulette_running", error="Invalid bet amount"))

            #check bet against balance
            if bet > balance:
                return redirect(
                    url_for("roulette_running", error="Insufficient funds for bet")
                )

            bet_type = request.form["bet_type"]

        except (ValueError, TypeError):
            return redirect(url_for("roulette_running", error="Invalid bet amount"))

        # Use RouletteGame class
        roulette_game = RouletteGame()

        # Map web form values to game values
        if bet_type == "red":
            game_bet_type = "2"
        elif bet_type == "black":
            game_bet_type = "3"
        elif bet_type == "even":
            game_bet_type = "4"
        elif bet_type == "odd":
            game_bet_type = "5"
        elif bet_type.startswith("number_"):
            game_bet_type = "1"
            straight_number = bet_type.split("_")[1]
        else:
            game_bet_type = "2"  # default
            straight_number = None

        # Play the round
        if game_bet_type == "1":
            result = roulette_game.play_round(
                balance, str(bet), game_bet_type, straight_number
            )
        else:
            result = roulette_game.play_round(balance, str(bet), game_bet_type)

        if "error" in result:
            return f"<p>Error: {result['error']} <a href='/roulette/active'>Try again</a></p>"

        winning_number = result["winning_number"]
        winning_color = result["winning_color"]
        did_win = result["did_win"]
        payout = result["payout"]

        user = User(session.get("username"))

        if did_win:
            user.update_money_won(abs(payout))
            result_text = f"You win ${abs(payout):.2f}! Number: {winning_number} ({winning_color})"
        else:
            user.update_money_lost(bet)
            result_text = f"You lose! Number: {winning_number} ({winning_color})"

        return f"""
        <h1>Roulette Result</h1>
        <p>{result_text}</p>
        <button type="button" onclick="window.location.href='/roulette/active'">Play Again</button>
        <button type="button" onclick="window.location.href='/userhome'">Home</button>
        """

    # Generate number options for dropdown
    number_options = ""
    for i in range(37):  # 0-36
        number_options += f'<option value="number_{i}">{i}</option>'

    html = f"""
    <h1>Roulette</h1>
    <p><strong>Balance: ${balance:.2f}</strong></p>
    {error_html}
    <form action="/roulette/active" method="POST">
        <label for="bet">Bet amount:</label>
        <input type="number" id="bet" name="bet" step="0.01" required><br><br>
        
        <label for="bet_type">Bet on:</label>
        <select id="bet_type" name="bet_type" required>
            <option value="red">Red (1:1)</option>
            <option value="black">Black (1:1)</option>
            <option value="green">Green (35:1)</option>
            <option value="even">Even (1:1)</option>
            <option value="odd">Odd (1:1)</option>
            {number_options}
        </select><br><br>
        
        <button type="submit">Spin</button>
    </form>
    <button type="button" onclick="window.location.href='/userhome'">Back to home</button>
    """
    return html


# Slots route
# Slated for a different sprint, placeholder endpoint
@app.route("/slots")
def sportsbetting():
    html = """
    <p>There will be slots here eventually!<p>
    """
    return html


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()
