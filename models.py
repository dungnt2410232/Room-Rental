from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

#table for favorites
favorites = db.Table(
    'favorites',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'room_id',
        db.Integer,
        db.ForeignKey('rooms.id'),
        primary_key=True
    )
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='sinhvien')
    favorite_rooms = db.relationship(
        'Room',                         
        secondary=favorites,
        backref='favorited_by'
    )

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    chutro_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



#function để nhìn database. chạy trên terminal python python -m flask --app app shell. from models import display_database. display_database(). Exit() để thoát
def display_database():
    print("\n--- USERS ---")
    for user in User.query.all():
        print(
            f"id={user.id}, "
            f"username={user.username}, "
            f"role={user.role}"
        )

    print("\n--- ROOMS ---")
    for room in Room.query.all():
        print(
            f"id={room.id}, "
            f"title={room.title}, "
            f"owner={room.chutro_id}"
        )

    print("\n--- FAVORITES TABLE ---")
    rows = db.session.execute(
        favorites.select()
    ).mappings().all()

    for row in rows:
        print(
            f"user_id={row['user_id']}, "
            f"room_id={row['room_id']}"
        )

    print("\n--- FAVORITES BY USER ---")
    for user in User.query.all():
        print(f"{user.username}:")
        for room in user.favorite_rooms:
            print(f"  - {room.title}")

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
