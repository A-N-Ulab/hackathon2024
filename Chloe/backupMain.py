#=== Import libraries ===
from flask import Flask, render_template, request, redirect, url_for, jsonify

#=== Create Flask app ===
app = Flask(__name__)


#=== Logging  screen ===
@app.route('/', methods=['GET', 'POST'])                        #define route and methods
def logging():
    #---- Check if the form was submitted ----
    if request.method == 'POST':
        #---- Check which button was pressed ----
        #---- if logIn button was pressed then check login data ----
        if request.form['button'] == 'logIn':    
            #---- Get data from form ----
            email = request.form['email']
            password = request.form['password']
            #
            valid = checkLogin(email, password)                  #check login data
            if valid == True:
                return redirect(url_for('main'))                #redirect to main page
            else:
                return render_template('login.html', email_placeholder="zły email lub hasło", 
                                       password_placeholder="zły email lub hasło")
        #
        #---- if regIn button was pressed then redirect to register page ----
        elif request.form['button'] == 'regIn':
            return redirect(url_for('register'))                #redirect to register page
        
    return render_template('login.html', email_placeholder="email", password_placeholder="hasło")  
#
#=== Check login data ===
def checkLogin(email, password):
    if email == None or password == None:
        return render_template('login.html')
    elif email == 'admin' and password == 'admin':
        statusOfLogin = True
    else:
        statusOfLogin = False
    return statusOfLogin


#=== Register ===
@app.route('/register', methods=['GET', 'POST'])
def register():
    #=== Check if inputs are filled and button is pressed ===
    if request.method == 'POST':
        #---- Read data from form ----
        email = request.form['email']
        password = request.form['password']
        repPassword = request.form['repassword']
        name = request.form['name']
        #
        #---- Check which button was pressed ----
        if request.form['button'] == 'regIn':
            valid = checkRegister(email, password, repPassword, name)               #check register data
            #
            #---- If data is valid then redirect to main page ----
            if valid == True:
                return redirect(url_for('main'))
            else:
                return render_template('rejstr.html', email_placeholder="email", 
                                       password_placeholder="hasło się nie zgadza", 
                                       repPassword_placeholder="hasło się nie zgadza", 
                                       name_placeholder="imię")

    return render_template('rejstr.html', email_placeholder="email",
                            password_placeholder="hasło", repPassword_placeholder="powtórz hasło", 
                            name_placeholder="imię")
#
#=== Check register data ===
def checkRegister(email, password, repPassword, name):
    if email == None or password == None or repPassword == None or name == None:
        return render_template('rejstr.html')
    elif password != repPassword:
        statusOfRegister = False
    else:
        statusOfRegister = True
    return statusOfRegister

#=== Main user interface ===
@app.route('/user', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

@app.route('/userUpdateB')
def updateMainB():
    return jsonify(new_content="{data}".format(data="Chuj Ci w dupe delikatnie"))

@app.route('/userUpdateF')
def updateMainF():
    return jsonify(new_content="{data}".format(data="Chuj Ci w dupE"))

#=== Run app ===
if __name__ == '__main__':
    app.run(debug=True)