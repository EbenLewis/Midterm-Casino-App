from flask import Flask, request
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
#TODO: save to henry's backend
@app.route("/createaccount", methods=["GET","POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    #html for the page
    html = '''
    <h1> Create your account <h1>
    <form action="/createaccount" method="POST">
    <form> 
        <label for = "username">Add username:</label>
        <input type="text" id="username" username="username"><br><br>

        <label for = "password">Add password:</label>
        <input type="text" id="password" password="password"><br><br>
    '''
    
    return html

#login route
#TODO: check for users from backend
@app.route("/login", methods=["GET","POST"])
def login():
    html = '''
    <form> 
        <label for = "username">Enter your username</label>
        <input type="text" id="username" username="username"><br><br>

        <label for = "password">Enter your password:</label>
        <input type="text" id="password" password="password"><br><br>
    '''
    return html

#Blackjack route
@app.route("/blackjack")
def blackjack():
    html = '''
    <p>There will be blackjack here eventually!<p>
    '''
    return html

#Roulette route
@app.route("/roulette")
def roulette():
    html = '''
    <p>There will be roulette here eventually!<p>
    '''
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