from flask import Flask, request, redirect, url_for
from user_Utils import UserManager
from blackjackGame import play_blackjack
from rouletteGame import play_roulette, RouletteGame

app = Flask(__name__)
#landing page 
#TODO: add buttons for navigation
@app.route("/", methods=["GET","POST"])
def home():
    html = '''
    <h1> Welcome to the casino <h1>
    <p> let's go gambling! <p>
    <button type="button" onclick="window.location.href='/login'">Login</button>
    <button type="button" onclick="window.location.href='/createaccount'">Create Account</button>
    <button type="button" onclick="window.location.href='/userdata'">View user data</button>
    <button type="button" onclick="window.location.href='/blackjack'">Play Blackjack</button>
    <button type="button" onclick="window.location.href='/roulette'">Play Roulette</button>
    <button type="button" onclick="window.location.href='/sportsbetting'">Sports betting</button>
    '''
    return html

#display user data upon request
#TODO: display info for a user from userdata.json
@app.route("/userdata")
def view_account():
    html = '''
    <h1> This is your user data <h1>
    '''
    return html

#create account page
#TODO: save to  backend
@app.route("/createaccount", methods=["GET", "POST"])
def create_account():
    html = '''
    <h1>Create your account</h1>
    <form action="/createaccount" method="POST">
        <label for="username">Add username:</label>
        <input type="text" id="username" name="username"><br><br>

        <label for="password">Add password:</label>
        <input type="text" id="password" name="password"><br><br>

        <label for="initial_balance">Add initial funds:</label>
        <input type="number" id="initial_balance" name="initial_balance"><br><br>

        <input type="submit" value="Submit">
    </form>
    '''

    #account creation functionality
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        initial_balance = float(request.form["initial_balance"])
        UserManager.new_user(username, password, initial_balance)
        return redirect(url_for("home"))

    return html


#login route
#TODO: check for users from backend
@app.route("/login", methods=["GET","POST"])
def login():

    html = '''
    <form> 
        <label for = "username">Enter your username</label>
        <input type="text" id="username" name="username"><br><br>

        <label for = "password">Enter your password:</label>
        <input type="text" id="password" name="password"><br><br>

        <input type="submit" onclick="window.location.href='/' value="Submit">
    </form>
    '''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        UserManager.login(username, password)
        if UserManager.login(username, password):
            return f"<p>Welcome back {username}!<p>", redirect(url_for("home"))
        else: 
            return redirect(url_for("home"))

    return html

#Blackjack route
@app.route("/blackjack")
def blackjack():
    html = '''
    <button type="button" onclick="window.location.href='/blackjack/active'">Play blackjack?</button>
    <button type="button" onclick="window.location.href='/'">Return to home</button>
    '''
    return html

@app.route("/blackjack/active")
def game_running():
    html = '''
    <button type="button" >bet</button>
    <button type="button" >hit</button>
    <button type="button" >stand</button>
    '''
    if request.method == "POST":
        bet = request.form["bet"]
        hit = request.form["hit"]
        stand = request.form["stand"]
    play_blackjack()
    return html 
        
#Roulette route
@app.route("/roulette")
def roulette():
    html = '''
    <p> Welcome to roulette<p>
    <button type="button" onclick="window.location.href='/blackjack/active'">Play roulette?</button>
    <button type="button" onclick="window.location.href='/'">Return to home</button>
    '''

    return html

@app.route("/roulette/active")
def game_running():
    html = '''
    <form> 
        <label for = "color">Pick a color</label>
        <input type="text" id="color" name="color"><br><br>

        <label for = "number">Pick a number</label>
        <input type="number" id="number" name="number"><br><br>
    </form>
    <button type="button" >bet</button>
    '''
    if request.method == "POST":
        number = request.form["number"]
        color = request.form["color"]

    play_roulette()
    return html 

#Sports betting route
@app.route("/sportsbetting")
def sportsbetting():
    html = '''
    <p>There will be sports betting here eventually!<p>
    '''
    return html

if __name__ == "__main__":
    app.run()