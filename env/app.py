from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from pymongo import MongoClient
import thing

from thing import get_master_list, get_student

client = MongoClient()

class User:
    def __init__(self, id, username, password, type):
        self.id = id
        self.username = username
        self.password = password
        self.type = type

    def __repr__(self):
        return str(self.username)

users = []
users.append(User(id=1, username='Rahul@gmail.com', password='password', type='student'))
users.append(User(id=2, username='Wayhar@gmail.com', password='password', type='admin'))
users.append(User(id=3, username='Billy@gmail.com', password='password', type='student'))


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':            
        session.pop('user_id', None)
        #print(request.form['email'])
        #print(request.form['password'])
        username = request.form['email']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            if(user.type=='student'):
                return redirect(url_for('student'))
            if(user.type=='admin'):
                return redirect(url_for('admin'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/student', methods=['GET', 'POST'])
def student():
    if not g.user:
        return redirect(url_for('login'))
    print(request.method)
    if request.method == 'POST':
        session.pop('user_id', None)
        return redirect(url_for('logout'))
    student_1 = get_student(str(g.user))
    master_list = get_master_list()
    print(g.user)
    print("list")
    print(student_1)
    return render_template('index.html', student=student_1, schedule=master_list)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form["button"] == "edit":
            return redirect(url_for("editpage"))
        elif request.form["button"] == "logout":
            session.pop('user_id', None)
            return redirect(url_for('logout'))
    master_list = get_master_list()
    print("master list is")
    print(master_list)
    return render_template('admin.html', schedule=master_list)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/editpage', methods=['GET', 'POST'])
def editpage():
    print("method is")
    print(request.method)
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        print(request.form)
        print(request.form["button2"])
        if request.form["button2"] == "home":
            print("return here")
            return redirect(url_for("admin"))
        elif request.form["button2"] == "logout":
            print("return there")
            session.pop('user_id', None)
            return redirect(url_for('logout'))

    return render_template("lab.html")

if __name__ == '__main__':
    app.run(debug=True)
