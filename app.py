import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Room, Review

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

@app.route('/room/<int:room_id>', methods=['GET', 'POST'])
def room_detail(room_id):
    room = Room.query.get_or_404(room_id)
    reviews = Review.query.filter_by(room_id=room_id).all()

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để bình luận.', 'danger')
            return redirect(url_for('login'))
        
        content = request.form.get('content')
        if content:
            new_review = Review(content=content, user_id=current_user.id, room_id=room.id)
            db.session.add(new_review)
            db.session.commit()
            return redirect(url_for('room_detail', room_id=room.id))

    return render_template('room_detail.html', room=room, reviews=reviews)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post_room():
    # Chi cho phep role'chutro' dang bai
    if current_user.role != 'chutro':
        flash('Only owners can post rooms.', 'danger')
        return redirect(url_for('index'))

    # Xu ly submit form
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        price = request.form.get('price', type=float)
        area = request.form.get('area', type=float)
        district = request.form.get('district', '').strip()
        address = request.form.get('address', '').strip()
        image_url = request.form.get('image_url', '').strip()
        description = request.form.get('description', '').strip()

        # Validate cac truong bat buoc
        if not all([title, price, area, district, address]):
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('post_room'))

        # Link anh mac dinh neu bo trong
        if not image_url:
            image_url = 'https://keystoneacademic-res.cloudinary.com/image/upload/f_auto/q_auto/g_auto/w_200/dpr_2.0/element/16/164506_logoUSTHmoi-01.png'

        # Tao va luu Room moi gan voi current_user.id
        new_room = Room(
            title=title,
            price=price,
            area=area,
            district=district,
            address=address,
            image_url=image_url,
            description=description,
            chutro_id=current_user.id
        )

        db.session.add(new_room)
        db.session.commit()

        flash('Room posted successfully!', 'success')
        return redirect(url_for('room_detail', room_id=new_room.id))

    return render_template('post_room.html')

@app.route('/my-rooms')
@login_required
def my_rooms():
    # Only role chutro moi co trang quan ly
    if current_user.role != 'chutro':
        flash('Access denied. Only owners can view their listings.', 'danger')
        return redirect(url_for('index'))

    # Check cac phong dang thuoc so huu cua user
    rooms = Room.query.filter_by(chutro_id=current_user.id).order_by(Room.id.desc()).all()
    return render_template('my_rooms.html', rooms=rooms)


@app.route('/room/<int:room_id>/delete', methods=['POST'])
@login_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)

    # Khong cho phep xoa cua nguoi khac
    if room.chutro_id != current_user.id:
        flash('You are not authorized to delete this room.', 'danger')
        return redirect(url_for('my_rooms'))

    db.session.delete(room)
    db.session.commit()

    flash(f'Room "{room.title}" has been deleted.', 'success')
    return redirect(url_for('my_rooms'))

@app.route('/room/<int:room_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)

    # Chi co role chu tro moi dc chinh sua
    if room.chutro_id != current_user.id:
        flash('You are not authorized to edit this room.', 'danger')
        return redirect(url_for('my_rooms'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        price = request.form.get('price', type=float)
        area = request.form.get('area', type=float)
        district = request.form.get('district', '').strip()
        address = request.form.get('address', '').strip()
        image_url = request.form.get('image_url', '').strip()
        description = request.form.get('description', '').strip()

        if not all([title, price, area, district, address]):
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('edit_room', room_id=room.id))

        # Update room detail
        room.title = title
        room.price = price
        room.area = area
        room.district = district
        room.address = address
        room.image_url = image_url if image_url else room.image_url
        room.description = description

        db.session.commit()
        flash('Room updated successfully!', 'success')
        return redirect(url_for('my_rooms'))

    return render_template('edit_room.html', room=room)


#favorite system
@app.route('/room/<int:room_id>/favorite', methods=['POST'])
@login_required
def favorite_room(room_id):
    room = Room.query.get_or_404(room_id)

    if room not in current_user.favorite_rooms:
        current_user.favorite_rooms.append(room)
        db.session.commit()
        flash('Room added to favorites.', 'success')
    else:
        flash('Room is already in your favorites.', 'info')

    return redirect(url_for('room_detail', room_id=room.id))


@app.route('/room/<int:room_id>/unfavorite', methods=['POST'])
@login_required
def unfavorite_room(room_id):
    room = Room.query.get_or_404(room_id)

    if room in current_user.favorite_rooms:
        current_user.favorite_rooms.remove(room)
        db.session.commit()
        flash('Room removed from favorites.', 'success')

    return redirect(url_for('room_detail', room_id=room.id))

@app.route('/favorites')
@login_required
def favorites():
    rooms = current_user.favorite_rooms
    return render_template('favorites.html', rooms=rooms)


if __name__ == '__main__':
    app.run(debug=True)