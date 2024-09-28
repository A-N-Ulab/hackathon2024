from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#website run
@app.route('/', methods=['GET', 'POST'])
def home():
    button_clicked = request.args.get('button')
    #if button_clicked == 'Zaloguj się':
    if request.method == 'POST':
        if request.form['button'] == 'logIn':    
            login = request.form['login']
            password = request.form['password']
        elif request.form['button'] == 'regIn':
            return redirect(url_for('register'))
        
    return render_template('login.html')
    
#main user interface
@app.route('/user')
def check(login, password):
    print(login, password)
    statusOfLogin = False
    return statusOfLogin
    
#register
@app.route('/register')
def register():
    return render_template('rejstr.html')

#password check

if __name__ == '__main__':
    app.run(debug=True)