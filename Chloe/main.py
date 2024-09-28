#=== Import libraries ===
from flask import Flask, render_template, request, redirect, url_for

#=== Create Flask app ===
app = Flask(__name__)


#=== Logging  screen ===
@app.route('/', methods=['GET', 'POST'])                        #define route and methods
def logging():
    #---- Check if the form was submitted ----
    if request.method == 'POST':
        #
        #---- Check which button was pressed ----
        #---- if logIn button was pressed then check login data ----
        if request.form['button'] == 'logIn':    
            #---- Get data from form ----
            email = request.form['email']
            password = request.form['password']
            #
            valid = check(email, password)                      #check login data
            if valid == True:
                return redirect(url_for('main'))                #redirect to main page
        #
        #---- if regIn button was pressed then redirect to register page ----
        elif request.form['button'] == 'regIn':
            return redirect(url_for('register'))                #redirect to register page
        
    return render_template('login.html')                        #render login page
#
#=== Check login data ===
def check(email, password):
    if email == None or password == None:
        return render_template('login.html')
    elif email == 'admin' and password == 'admin':
        statusOfLogin = True
    else:
        statusOfLogin = False
    return statusOfLogin


#=== Register ===
@app.route('/register')
def register():
    return render_template('rejstr.html')


#=== Main user interface ===
@app.route('/user')
def main():
    return render_template('main.html')

#=== Run app ===
if __name__ == '__main__':
    app.run(debug=True)