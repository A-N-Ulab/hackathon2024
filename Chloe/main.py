from flask import Flask, render_template, request, redirect, url_for, jsonify
from BackendPython.mainMenu import readTypesOfLines, readLine, readStringAfterUnderscore, extractTextAfterColon
from werkzeug.datastructures import ImmutableMultiDict

class HackathonApp:
    '''
    Class to handle the Flask app for the hackathon project
    '''

    #=== Initialize the flask app ===
    def __init__(self):
        self.app = Flask(__name__)                                                                      # Initialize Flask app
        self.setup_routes()                                                                             # Setup routes for the app
        self.counter = 0                                                                                # Initialize counter
        self.lastLesson = 0                                                                             # Initialize last lesson index
        self.msgPrev = "Poprzedni"                                                                      # Message for previous button
        self.msgNext = "Następny"                                                                       # Message for next button
        self.dictOfTasks = {"Task": 0, "Info": 0}                                                       # Dictionary to store tasks and info count
        self.classList = ["lBt", "locked", "locked", "locked"]                                          # List to store class states
        self.numAll = 0                                                                                 # Total number of tasks and info
        self.repeat = True                                                                              # Flag to allow repetition
        self.sol = "Nie rozwiązano"                                                                     # Solution status
        self.nameOfLesson = "lesson"                                                                    # Default lesson name
        self.accept = False                                                                             # Flag to check if solution is accepted
        self.sign = ""                                                                                  # Sign for input field


    #=== Setup routes for the app ===
    def setup_routes(self):
        self.app.add_url_rule('/', 'logging', self.logging, methods=['GET', 'POST'])
        self.app.add_url_rule('/register', 'register', self.register, methods=['GET', 'POST'])
        self.app.add_url_rule('/user', 'main', self.main, methods=['GET', 'POST'])
        self.app.add_url_rule('/userUpdateB', 'updateMainB', self.update_main_b)
        self.app.add_url_rule('/userUpdateF', 'updateMainF', self.update_main_f)


    #=== Login and registration ===
    def logging(self):
        #=== Handle login and regitration redirectory ===
        if request.method == 'POST':
            #---- Check if login or register button is clicked ----
            if request.form['button'] == 'logIn':
                email = request.form['email']                                                            # Get email from form                                          
                password = request.form['password']                                                      # Get password from form
                #
                #---- Check if email and password are correct ----
                if self.check_login(email, password):
                    return redirect(url_for('main'))
                else:
                    return render_template('login.html', email_placeholder="zły email lub hasło", 
                                           password_placeholder="zły email lub hasło")
            #
            #---- Check if register button is clicked ----
            elif request.form['button'] == 'regIn':
                return redirect(url_for('register'))
        #
        #---- Render login page ----
        return render_template('login.html', email_placeholder="email", password_placeholder="hasło")

    #=== Check login credentials ===
    def check_login(self, email, password):
        if email == 'admin' and password == 'admin':
            return True
        return False

    #=== Registration ===
    def register(self):
        if request.method == 'POST':
            email = request.form['email']                                                         # Get email from form
            password = request.form['password']                                                   # Get password from form
            repPassword = request.form['repassword']                                              # Get repeated password from form
            name = request.form['name']                                                           # Get name from form
            #
            #---- Check if register button is clicked ----
            if request.form['button'] == 'regIn':
                #
                #---- Check if email, password, repeated password and name are correct ----
                if self.check_register(email, password, repPassword, name):
                    return redirect(url_for('main'))
                else:
                    return render_template('rejstr.html', email_placeholder="email", 
                                           password_placeholder="hasło się nie zgadza", 
                                           repPassword_placeholder="hasło się nie zgadza", 
                                           name_placeholder="imię")
        #
        #---- Render registration page ----
        return render_template('rejstr.html', email_placeholder="email",
                               password_placeholder="hasło", repPassword_placeholder="powtórz hasło", 
                               name_placeholder="imię")

    #=== Check registration credentials ===
    def check_register(self, email, password, repPassword, name):
        if password != repPassword or password != None and repPassword != None:
            return False
        return True


    #=== Main menu ===
    def main(self):
        if request.method == 'POST':
            #---- Check if lesson's button is clicked ----
            if request.form['button'] == 'lesson1' or request.form['button'] == 'lesson2' or request.form['button'] == 'lesson3' or request.form['button'] == 'lesson4':
                self.nameOfLesson = request.form['button']
                self.dictOfTasks = readTypesOfLines("static/lessons/" + self.nameOfLesson + ".txt")
                self.numAll = self.dictOfTasks["Task"] + self.dictOfTasks["Info"]
                self.counter = 0
                self.repeat = True
                self.msgNext = "Rozpocznij"
                self.msgPrev = "-"
            
            #---- Check if check button is clicked ----
            if request.form['button'] == 'check':
                #---- Check if solution is correct ----
                if request.form['input'] == readStringAfterUnderscore("static/lessons/" + self.nameOfLesson + ".txt", self.counter):
                    self.sol = "Zajebiście"
                    self.accept = True
                #
                #---- Check if solution is incorrect ----
                elif request.form['input'] != readStringAfterUnderscore("static/lessons/" + self.nameOfLesson + ".txt", self.counter):
                    self.sol = "To nie jest takie trudne..."
                    self.accept = False
                #
                #---- Render main page ----
                return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                    classLesson1=self.classList[0], classLesson2=self.classList[1], 
                    classLesson3=self.classList[2], classLesson4=self.classList[3],
                    updateForward=True, updateBackward=False)
            
            #---- Check if sqrt button is clicked ----
            elif request.form['button'] == 'sqrt':
                self.sign = "√"
                #
                #---- Render main page ----
                return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                               classLesson1=self.classList[0], classLesson2=self.classList[1], 
                               classLesson3=self.classList[2], classLesson4=self.classList[3],
                               updateForward=True, updateBackward=False)
            
            #---- Check if previous button is clicked ----
            elif request.form['button'] == 'prev':
                #---- Idiot proofing ----
                if self.counter > 0:
                    self.counter += -1
                #
                #---- Render main page ----
                return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                               classLesson1=self.classList[0], classLesson2=self.classList[1], 
                               classLesson3=self.classList[2], classLesson4=self.classList[3],
                               updateForward=False, updateBackward=True)
            
            #---- Check if next button is clicked ----
            elif request.form['button'] == 'next':
                #---- Checking if you should be able to move to next page ----
                #---- If it's info ----
                if self.counter <= self.dictOfTasks["Info"]:
                    self.counter += 1
                    self.msgPrev = "Poprzedni"
                    self.msgNext = "Następny"
                #
                #---- If it's task ----
                elif self.counter > self.dictOfTasks["Info"] and self.accept:
                    self.counter += 1
                    self.sol = "Nie rozwiązano"
                    self.accept = False
                    self.msgPrev = "Poprzedni"
                    self.msgNext = "Następny"
                    self.sign = ""
                #
                #---- At the end of the lesson ulock the new one ----
                #---- Change button -----
                if self.counter == self.numAll:
                    self.msgNext = "Koniec"
                #
                #---- Unlock the new leson ----
                elif self.counter == self.numAll + 1 and self.repeat == True:
                    try:
                        self.classList[self.lastLesson+1] = "lBt"
                    except:
                        self.classList[self.lastLesson] = "lBt"
                    self.lastLesson = self.lastLesson + 1
                    self.repeat = False
                elif self.counter > self.numAll + 1:
                    self.counter = self.numAll
                #
                #---- Render main page ----
                return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                               classLesson1=self.classList[0], classLesson2=self.classList[1], 
                               classLesson3=self.classList[2], classLesson4=self.classList[3],
                               updateForward=True, updateBackward=False)
            
        #---- Render main page ----
        return render_template('main.html', textPrevious=self.msgPrev, textNext=self.msgNext, 
                               classLesson1=self.classList[0], classLesson2=self.classList[1], 
                               classLesson3=self.classList[2], classLesson4=self.classList[3],
                               updateForward=False, updateBackward=False)

    #=== Backward button ===
    def update_main_b(self):
        #---- Handle back button updates ----
        #---- Dispaying info with image----
        if self.counter <= self.dictOfTasks["Info"] and extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)) != None:
            return jsonify(new_content="""
                    <div class="task">
                        <h2>Wyjaśnienie</h2>
                        <p class="taskContent">{info}</p>
                        <img class="equ" src="{path}" alt="equation">
                    </div>""".format(info=readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)[:-4], path="static/lessons/"+extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter))+".png"))
        #
        #---- Displaying info without image ----
        elif self.counter <= self.dictOfTasks["Info"] and extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)) == None:
            return jsonify(new_content="""
                    <div class="task">
                        <h2>Wyjaśnienie</h2>
                        <p class="taskContent">{info}</p>
                    </div>""".format(info=readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)))
        #
        #---- Displaying task ----
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
        #---- Handle forward button updates ----
        #---- Displaying info with image ----
        if self.counter <= self.dictOfTasks["Info"] and extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)) != None:
            print("static/lessons/"+extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter))+".png")
            return jsonify(new_content="""
                    <div class="task">
                        <h2>Wyjaśnienie</h2>
                        <p class="taskContent">{info}</p>
                        <img class="equ" src="{path}" alt="equation">
                    </div>""".format(info=readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)[:-5], path="static/lessons/"+extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter))+".png"))
        #
        #---- Displaying info without image ----
        elif self.counter <= self.dictOfTasks["Info"] and extractTextAfterColon(readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)) == None:
            return jsonify(new_content="""
                    <div class="task">
                        <h2>Wyjaśnienie</h2>
                        <p class="taskContent">{info}</p>
                    </div>""".format(info=readLine("static/lessons/" + self.nameOfLesson + ".txt", self.counter)))
        #
        #---- Displaying task ----
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


    #=== Run the Flask app ===
    def run(self):
        self.app.run(debug=True)


#=== Program execution ===
if __name__ == '__main__':
    app = HackathonApp()
    app.run()