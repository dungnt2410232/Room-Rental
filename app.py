from flask import Flask, render_template
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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)