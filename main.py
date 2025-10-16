from flask import Flask, request, redirect, url_for, session
from user_Utils import UserManager, User
from blackjackGame import play_blackjack
from rouletteGame import play_roulette, RouletteGame

app = Flask(__name__)
app.secret_key = "not_very_secret_key" #hash this later
#landing page 
#WORKS
@app.route("/", methods=["GET","POST"])
def home():
    html = '''
    <h1> Welcome to the casino </h1>
    <p> let's go gambling! <p>
    <button type="button" onclick="window.location.href='/login'">Login</button>
    <button type="button" onclick="window.location.href='/createaccount'">Create Account</button>
    <button type="button" onclick="window.location.href='/userdata'">View user data</button>
    '''
    return html

#home page after login for user
#WORKS
@app.route("/userhome")
def user_home():
    html = '''
    <h1> Welcome back, '''+ session.get("username") + '''</h1>
    <p> let's go gambling! <p>
    <button type="button" onclick="window.location.href='/userdata'">View user data</button>
    <button type="button" onclick="window.location.href='/blackjack'">Play Blackjack</button>
    <button type="button" onclick="window.location.href='/roulette'">Play Roulette</button>
    <button type="button" onclick="window.location.href='/sportsbetting'">Sports betting</button>
    '''
    return html

#display user data upon request
#WORKS
@app.route("/userdata")
def view_account():
    if session.get('logged_in') != True:
        return redirect(url_for("home"))
    else: 
        userdata = UserManager.view_data(session.get('username'))
        html = '''
        <h1> This is your user data: </h1>
        <p> Username: ''' + userdata['username'] + '''</p>
        <p> UserID: ''' + str(userdata['userid']) + '''</p>
        <p> Total Money: $''' + str(userdata['money_total']) + '''</p>
        <p> Total Deposited: $''' + str(userdata['total_deposited']) + '''</p>
        <p> Total Withdrawn: $''' + str(userdata['total_withdrawn']) + '''</p>
        <p> Money Won: $''' + str(userdata['money_won']) + '''</p>
        <p> Money Lost: $''' + str(userdata['money_lost']) + '''</p>
        <button type="button" onclick="window.location.href='/changefunds'">Change Funds</button>
        <button type="button" onclick="window.location.href='/userhome'">Return to home</button>
        '''
        return html

#create account page
#WORKS
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
#WORKS
@app.route("/login", methods=["GET","POST"])
def login():

    html = '''
    <form action="/login" method="POST"> 
        <label for = "username">Enter your username</label>
        <input type="text" id="username" name="username"><br><br>

        <label for = "password">Enter your password:</label>
        <input type="text" id="password" name="password"><br><br>

        <input type="submit" value="Submit">
    </form>
    '''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success = UserManager.login(username, password)
        #uses session variables for each user to keep them seperate
        if success:
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for("user_home"))
        else: 
            return redirect(url_for("home"))

    return html

#change funds route
#WORKS
@app.route("/changefunds", methods=["GET","POST"])
def change_funds():
    if session.get('logged_in') != True:
        return redirect(url_for("home"))
    
    html = '''
    <form action="/changefunds" method="POST">
        <label for="amount">Enter amount to deposit/remove (use negative numbers to remove):</label>
        <input type="number" id="amount" name="amount"><br><br>
        <input type="submit" value="Submit">
        </form>'''
    if request.method == "POST":
        amount = float(request.form["amount"])
        user = User(session.get("username"))
        if amount > 0:
            user.add_funds(amount)
        else:
            user.withdraw_funds(-amount)
        return redirect(url_for("view_account"))
    return html

#Blackjack routes
#Doesn't work, when user presses play blackjack, game runs in terminal not webpage
@app.route("/blackjack", methods=["GET","POST"])
def blackjack():
    html = '''
    <button type="button" onclick="window.location.href='/blackjack/active'">Play blackjack?</button>
    <button type="button" onclick="window.location.href='/userhome'">Return to home</button>
    '''
    return html

#route to play the actual game in
@app.route("/blackjack/active", methods=["GET","POST"])
def blackjack_running():
    html = '''
    <form action="/blackjack/active" method="POST">
        <label for="bet">Place your bet:</label>
        <input type="number" id="bet" name="bet">
        <button type="submit">Submit Bet</button>
    </form>
    '''
    if request.method == "POST":
        bet = request.form["bet"]
        hit = request.form["hit"]
        stand = request.form["stand"]
    play_blackjack()
    return html 
        
#Roulette routes
#Doesn't currently work
@app.route("/roulette", methods=["GET","POST"])
def roulette():
    html = '''
    <p> Welcome to roulette<p>
    <button type="button" onclick="window.location.href='/roulette/active'">Play roulette?</button>
    <button type="button" onclick="window.location.href='/userhome'">Return to home</button>
    '''

    return html

@app.route("/roulette/active", methods=["GET","POST"])
def roulette_running():
    html = '''
    <form> 
        <label for = "color">Pick a color</label>
        <input type="text" id="color" name="color"><br><br>

        <label for = "number">Pick a number, </label>
        <input type="number" id="number" name="number"><br><br>
    
    </form>
    <button type="button" >bet</button>
    '''
    number = int(request.form["number"])
    color = request.form["color"]

    play_roulette(session.get("username"), UserManager.view_data(session.get("username")))
    
    return html 

#Sports betting route
#Slated for a different sprint, placeholder endpoint
@app.route("/sportsbetting")
def sportsbetting():
    html = '''
    <p>There will be sports betting here eventually!<p>
    '''
    return html

if __name__ == "__main__":
    app.run()