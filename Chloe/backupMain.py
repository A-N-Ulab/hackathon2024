from flask import Flask, render_template, request, redirect, url_for, jsonify
from BackendPython.mainMenu import readTypesOfLines, readLine, readStringAfterUnderscore, extractTextAfterColon
from werkzeug.datastructures import ImmutableMultiDict

class HackathonApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.counter = 0
        self.lastLesson = 0
        self.msgPrev = "Poprzedni"
        self.msgNext = "Następny"
        self.dictOfTasks = {"Task": 0, "Info": 0}
        self.classList = ["lBt", "locked", "locked", "locked"]
        self.numAll = 0
        self.repeat = True
        self.sol = "Nie rozwiązano" 
        self.nameOfLesson = "lesson"
        self.accept = False
        self.sign = ""

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
        if password != repPassword or password != None and repPassword != None:
            return False
        return True



    #=== Main menu ===
    def main(self):
        if request.method == 'POST':
            if request.form['button'] == 'lesson1' or request.form['button'] == 'lesson2' or request.form['button'] == 'lesson3' or request.form['button'] == 'lesson4':
                self.nameOfLesson = request.form['button']
                self.dictOfTasks = readTypesOfLines("static/lessons/" + self.nameOfLesson + ".txt")
                self.numAll = self.dictOfTasks["Task"] + self.dictOfTasks["Info"]
                self.counter = 0
                self.repeat = True
                self.msgNext = "Rozpocznij"
                self.msgPrev = "-"

            if request.form['button'] == 'check':
                if request.form['input'] == readStringAfterUnderscore("static/lessons/" + self.nameOfLesson + ".txt", self.counter):
                    self.sol = "Zajebiście"
                    self.accept = True
                elif request.form['input'] != readStringAfterUnderscore("static/lessons/" + self.nameOfLesson + ".txt", self.counter):
                    self.sol = "To nie jest takie trudne..."
                    self.accept = False
                return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                    classLesson1=self.classList[0], classLesson2=self.classList[1], 
                    classLesson3=self.classList[2], classLesson4=self.classList[3],
                    updateForward=True, updateBackward=False)
            
            elif request.form['button'] == 'sqrt':
                self.sign = "√"
                return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                               classLesson1=self.classList[0], classLesson2=self.classList[1], 
                               classLesson3=self.classList[2], classLesson4=self.classList[3],
                               updateForward=True, updateBackward=False)
            
            elif request.form['button'] == 'prev':
                if self.counter > 0:
                    self.counter += -1
                return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                               classLesson1=self.classList[0], classLesson2=self.classList[1], 
                               classLesson3=self.classList[2], classLesson4=self.classList[3],
                               updateForward=False, updateBackward=True)
            
            elif request.form['button'] == 'next':
                print(self.dictOfTasks["Task"]-1)
                if self.counter <= self.dictOfTasks["Info"]:
                    self.counter += 1
                    self.msgPrev = "Poprzedni"
                    self.msgNext = "Następny"
                elif self.counter > self.dictOfTasks["Info"] and self.accept:
                    self.counter += 1
                    self.sol = "Nie rozwiązano"
                    self.accept = False
                    self.msgPrev = "Poprzedni"
                    self.msgNext = "Następny"
                    self.sign = ""
                if self.counter == self.numAll:
                    self.msgNext = "Koniec"
                
                elif self.counter == self.numAll + 1 and self.repeat == True:
                    try:
                        self.classList[self.lastLesson+1] = "lBt"
                    except:
                        self.classList[self.lastLesson] = "lBt"
                    self.lastLesson = self.lastLesson + 1
                    self.repeat = False
                elif self.counter > self.numAll + 1:
                    self.counter = self.numAll

                return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                               classLesson1=self.classList[0], classLesson2=self.classList[1], 
                               classLesson3=self.classList[2], classLesson4=self.classList[3],
                               updateForward=True, updateBackward=False)
            

        return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                               classLesson1=self.classList[0], classLesson2=self.classList[1], 
                               classLesson3=self.classList[2], classLesson4=self.classList[3],
                               updateForward=False, updateBackward=False)

    #=== Backward button ===
    def update_main_b(self):
        if self.counter <= self.dictOfTasks["Info"] and extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)) != None:
            return jsonify(new_content="""
                    <div class="task">
                        <h2>Wyjaśnienie</h2>
                        <p class="taskContent">{info}</p>
                        <img class="equ" src="{path}" alt="equation">
                    </div>""".format(info=readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)[:-4], path="static/lessons/"+extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter))+".png"))
        elif self.counter <= self.dictOfTasks["Info"] and extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)) == None:
            return jsonify(new_content="""
                    <div class="task">
                        <h2>Wyjaśnienie</h2>
                        <p class="taskContent">{info}</p>
                    </div>""".format(info=readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)))
        else:
            return jsonify(new_content="""
                    <div class="task">
                        <h2>Ćwiczenie - <em>{solution}</em></h2>
                        <p class="taskContent">{task}</p>   
                        <form method="post">
                            <input type="text" name="input" class="inputTask" value="{sign}" placeholder="Rozwiązanie zadania" onfocus="this.placeholder=''" onblur="this.placeholder = 'Rozwiązanie zadania'">
                            <button type="submit" name="button" value="check">Sprawdź</button>
                            <button type="submit" name="button" value="sqrt">√</button>
                        </form>
                    </div>""".format(task=readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter), solution=self.sol, sign=self.sign))

    #=== Forward button ===
    def update_main_f(self):
        if self.counter <= self.dictOfTasks["Info"] and extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)) != None:
            print("static/lessons/"+extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter))+".png")
            return jsonify(new_content="""
                    <div class="task">
                        <h2>Wyjaśnienie</h2>
                        <p class="taskContent">{info}</p>
                        <img class="equ" src="{path}" alt="equation">
                    </div>""".format(info=readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)[:-5], path="static/lessons/"+extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter))+".png"))
        elif self.counter <= self.dictOfTasks["Info"] and extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)) == None:
            return jsonify(new_content="""
                    <div class="task">
                        <h2>Wyjaśnienie</h2>
                        <p class="taskContent">{info}</p>
                    </div>""".format(info=readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)))
        else:
            return jsonify(new_content="""
                    <div class="task">
                        <h2>Ćwiczenie - <em>{solution}</em></h2>
                        <p class="taskContent">{task}</p>   
                        <form method="post">
                            <input type="text" name="input" class="inputTask" value="{sign}" placeholder="Rozwiązanie zadania" onfocus="this.placeholder=''" onblur="this.placeholder = 'Rozwiązanie zadania'">
                            <button type="submit" name="button" value="check">Sprawdź</button>
                            <button type="submit" name="button" value="sqrt">√</button>
                        </form>
                    </div>""".format(task=readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter), solution=self.sol, sign=self.sign))



    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app = HackathonApp()
    app.run()