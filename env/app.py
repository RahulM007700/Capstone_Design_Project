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

client = MongoClient()

class User:
    def __init__(self, id, username, password, type):
        self.id = id
        self.username = username
        self.password = password
        self.type = type

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Rahul', password='password', type='student'))
users.append(User(id=2, username='Wayhar', password='password', type='admin'))


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
    print("Here")
    print(request.method)
    if request.method == 'POST':
        print("here")
        session.pop('user_id', None)
        print(request.form['user'])
        print(request.form['pass'])
        username = request.form['user']
        password = request.form['pass']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            if(user.type=='student'):
                return redirect(url_for('student'))
            if(user.type=='admin'):
                return redirect(url_for('admin'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/student')
def student():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/admin')
def admin():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)
