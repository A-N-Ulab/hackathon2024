from flask import Flask, render_template, request, redirect, url_for, jsonify
from BackendPython.mainMenu import readTypesOfLines, readLine

class HackathonApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.counter = 0
        self.msgPrev = "Poprzedni"
        self.msgNext = "Następny"
        self.dictOfTasks = {}
        self.ls1 = "lBt"
        self.ls2 = "locked"
        self.ls3 = "locked"
        self.ls4 = "locked"

    def setup_routes(self):
        self.app.add_url_rule('/', 'logging', self.logging, methods=['GET', 'POST'])
        self.app.add_url_rule('/register', 'register', self.register, methods=['GET', 'POST'])
        self.app.add_url_rule('/user', 'main', self.main, methods=['GET', 'POST'])
        self.app.add_url_rule('/userUpdateB', 'updateMainB', self.update_main_b)
        self.app.add_url_rule('/userUpdateF', 'updateMainF', self.update_main_f)

    def logging(self):
        if request.method == 'POST':
            if request.form['button'] == 'logIn':
                email = request.form['email']
                password = request.form['password']
                if self.check_login(email, password):
                    return redirect(url_for('main'))
                else:
                    return render_template('login.html', email_placeholder="zły email lub hasło", 
                                           password_placeholder="zły email lub hasło")
            elif request.form['button'] == 'regIn':
                return redirect(url_for('register'))
        return render_template('login.html', email_placeholder="email", password_placeholder="hasło")

    def check_login(self, email, password):
        if email == 'admin' and password == 'admin':
            return True
        return False

    def register(self):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            repPassword = request.form['repassword']
            name = request.form['name']
            if request.form['button'] == 'regIn':
                if self.check_register(email, password, repPassword, name):
                    return redirect(url_for('main'))
                else:
                    return render_template('rejstr.html', email_placeholder="email", 
                                           password_placeholder="hasło się nie zgadza", 
                                           repPassword_placeholder="hasło się nie zgadza", 
                                           name_placeholder="imię")
        return render_template('rejstr.html', email_placeholder="email",
                               password_placeholder="hasło", repPassword_placeholder="powtórz hasło", 
                               name_placeholder="imię")

    def check_register(self, email, password, repPassword, name):
        if password != repPassword:
            return False
        return True




    def main(self):
        if request.method == 'POST':
            if request.form['button'] == 'less1':
                self.dictOfTasks = readTypesOfLines('static/lessons/lesson1.txt')
                self.counter = 0
            elif request.form['button'] == 'less2':
                self.dictOfTasks = readTypesOfLines('static/lessons/lesson2.txt')
                self.counter = 0
            elif request.form['button'] == 'less3':
                self.dictOfTasks = readTypesOfLines('static/lessons/lesson3.txt')
                self.counter = 0
            elif request.form['button'] == 'less4':
                self.dictOfTasks = readTypesOfLines('static/lessons/lesson4.txt')
                self.counter = 0

            self.numAll = self.dictOfTasks['Info'] + self.dictOfTasks['Task'] 
        return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                               classLesson1=self.ls1, classLesson2=self.ls2, 
                               classLesson3=self.ls3, classLesson4=self.ls4)


    #=== Backward button ===
    def update_main_b(self):
        #=== Counter control ===
        if self.counter > 0:
            self.counter -= 1
        
          
        return jsonify(new_content="""
        <div class="slide">
            <h2 class="slideTitle">{title}</h2>
            <p class="slideContent">{content}</p>
        </div>
        """.format(title=self.title, content=self.content))

    #=== Forward button ===
    def update_main_f(self):
        #=== Counter control ===
        self.counter += 1
        if self.counter == self.numAll:
            self.msgNext = "Zakończ"
        elif self.counter > self.numAll:
            self.ls2 = "lBt"

        #return 
        return jsonify()


    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app = HackathonApp()
    app.run()
