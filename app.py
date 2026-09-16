import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nhom-web-dev-secret-key'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phongtro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    keyword = request.args.get('keyword', '').strip()
    district = request.args.get('district', '').strip()
    max_price = request.args.get('max_price', type=float)

    query = Room.query
    if keyword:
        query = query.filter(Room.title.ilike(f"%{keyword}%") | Room.description.ilike(f"%{keyword}%"))

    if district:
        query = query.filter(Room.district == district)

    if max_price:
        query = query.filter(Room.price <= max_price)

    rooms = query.all()
    return render_template(
        'index.html',
        rooms=rooms,
        keyword=keyword,
        district=district,
        max_price=max_price
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        role = request.form.get('role', 'sinhvien')
        password = request.form.get('password', '')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/room/<int:room_id>')
def room_detail(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template('room_detail.html', room=room)

@app.route('/post')
@login_required
def post_room():
    return render_template('post_room.html')

if __name__ == '__main__':
    app.run(debug=True)