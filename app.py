
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from datetime import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blackops'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

online_users = []

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    rank = db.Column(db.String(50), default='USER')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    text = db.Column(db.String(1000))
    time = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return 'Utente esistente'

        admin = username.lower() == 'admin'

        user = User(
            username=username,
            password=password,
            is_admin=admin,
            rank='ADMIN' if admin else 'USER'
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:

            login_user(user)

            if username not in online_users:
                online_users.append(username)

            return redirect('/dashboard')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():

    stats = {
        "cpu": random.randint(1,99),
        "ram": random.randint(1,99),
        "net": random.randint(100,999),
        "time": datetime.now().strftime('%H:%M:%S')
    }

    messages = Message.query.order_by(Message.id.desc()).limit(30)

    return render_template(
        'dashboard.html',
        stats=stats,
        users=online_users,
        messages=messages,
        username=current_user.username,
        is_admin=current_user.is_admin
    )

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():

    text = request.form['text']

    if text.strip():

        msg = Message(
            username=current_user.username,
            text=text,
            time=datetime.now().strftime('%H:%M:%S')
        )

        db.session.add(msg)
        db.session.commit()

    return redirect('/dashboard')

@app.route('/admin')
@login_required
def admin():

    if not current_user.is_admin:
        return redirect('/dashboard')

    users = User.query.all()

    return render_template('admin.html', users=users)

@app.route('/delete/<int:id>')
@login_required
def delete(id):

    if not current_user.is_admin:
        return redirect('/dashboard')

    user = User.query.get(id)

    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect('/admin')

@app.route('/chatbot')
@login_required
def chatbot():

    q = request.args.get('q','')

    responses = [
        'ACCESS GRANTED',
        'SERVER ONLINE',
        'DECRYPTION COMPLETE',
        'TARGET FOUND',
        'NETWORK SECURED'
    ]

    return jsonify({
        'response': random.choice(responses) + ' -> ' + q
    })

@app.route('/logout')
@login_required
def logout():

    if current_user.username in online_users:
        online_users.remove(current_user.username)

    logout_user()

    return redirect('/login')

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
