from app import app
from models import db, User, Room
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    
    host = User.query.filter_by(username='chutro1').first()
    if not host:
        host = User(
            username='chutro1',
            password=generate_password_hash('123456', method='pbkdf2:sha256'),
            role='chutro'
        )
        db.session.add(host)
        db.session.commit()

    Room.query.delete()
    
    sample_rooms = [
        Room(
            title="Cozy Studio Apartment with Living room and Bedroom",
            price=6500000,
            area=45.0,
            district="Cau Giay",
            address="No. 15, Tran Quoc Hoan Street",
            description="Fully furnished with air conditioning, private bedroom, high-speed WiFi, and 24/7 access.",
            image_url="https://cdn.thuviennhadat.vn/upload/tin-dang/hinh-anh/20250312083555/20250312083555638773653556653142.jpg",
            chutro_id=host.id
        ),
        Room(
            title="Modern Mini Apartment with Elevator",
            price=4200000,
            area=28.0,
            district="Hai Ba Trung",
            address="No. 88, Ta Quang Buu Street",
            description="Loft studio, fingerprint lock, security camera, close to supermarkets.",
            image_url="https://bandon.vn/uploads/thiet-ke-nha-tro-dep-2020-bandon-28.jpg",
            chutro_id=host.id
        ),
        Room(
            title="Shared Living Space for Students",
            price=4800000,
            area=18.0,
            district="Nam Tu Liem",
            address="No. 10, Ho Tung Mau Street",
            description="Clean room, private kitchen, affordable utility fees, convenient public bus stops nearby.",
            image_url="https://pt123.cdn.static123.com/images/thumbs/900x600/fit/2023/06/08/6280b7391048c1169859_1686212509.jpg",
            chutro_id=host.id
        )
    ]

    db.session.bulk_save_objects(sample_rooms)
    db.session.commit()
    print("Database seeded successfully!")