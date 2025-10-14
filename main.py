from flask import Flask, request
app = Flask(__name__)
#landing page 
#TODO: add buttons for navigation
@app.route("/")
def home():
    html = '''
    <h1> Welcome to the casino <h1>
    <p> let's go gambling! <p>
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
        username = request.form("username")
        password = request.form("passowrd")

        
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

if __name__ == "__main__":
    app.run()
