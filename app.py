from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager
from models import db, User, Room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nhom-web-dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phongtro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
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
    # Keyword
    if keyword:
        query = query.filter(Room.title.ilike(f"%{keyword}%") | Room.description.ilike(f"%{keyword}%"))

    # District
    if district:
        query = query.filter(Room.district == district)

    # Price filter
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/room/<int:room_id>')
def room_detail(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template('room_detail.html', room=room)

@app.route('/post')
def post_room():
    return render_template('post_room.html')

if __name__ == '__main__':
    app.run(debug=True)