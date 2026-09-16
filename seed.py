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
            title="Cozy Studio Apartment near Metro Station",
            price=3500000,
            area=25.0,
            district="Cau Giay",
            address="No. 15, Tran Quoc Hoan Street",
            description="Fully furnished with air conditioning, private balcony, high-speed WiFi, and 24/7 access.",
            image_url="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=600",
            chutro_id=host.id
        ),
        Room(
            title="Modern Mini Apartment with Elevator",
            price=4800000,
            area=32.0,
            district="Hai Ba Trung",
            address="No. 88, Ta Quang Buu Street",
            description="Spacious studio, fingerprint lock, security camera, close to major universities and supermarkets.",
            image_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600",
            chutro_id=host.id
        ),
        Room(
            title="Shared Living Space for Students",
            price=1800000,
            area=18.0,
            district="Nam Tu Liem",
            address="No. 199, Ho Tung Mau Street",
            description="Clean room, shared kitchen, affordable utility fees, convenient public bus stops nearby.",
            image_url="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600",
            chutro_id=host.id
        )
    ]

    db.session.bulk_save_objects(sample_rooms)
    db.session.commit()
    print("Database seeded successfully!")