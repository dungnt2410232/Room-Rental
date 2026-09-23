from app import app
from models import db, User, Room, Favorite
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

    Favorite.query.delete()
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
        ),
        Room(
            title="Studio with Natural Light",
            price=3800000,
            area=25.0,
            district="Cau Giay",
            address="12/106 Hoang Quoc Viet Street",
            description="Small room with full of services, air conditional, and kitchen.",
            image_url="https://rencity-bucket.s3-han02.fptcloud.com/images/03da10f0-4270-4be5-a599-385d6cedf56c.jpg",
            chutro_id=host.id
        ),
        Room(
            title="New apartment with Balcony and Kitchen",
            price=4500000,
            area=35.0,
            district="Bac Tu Liem",
            address="12/55 Co Nhue 2 Street",
            description="Căn hộ 1 phòng ngủ riêng biệt, view thoáng mát, an ninh đảm bảo 24/7.",
            image_url="https://rencity-bucket.s3-han02.fptcloud.com/images/0bdc1e62-2d8c-4f51-8744-b868e78b97c3.jpg",
            chutro_id=host.id
        ),
        Room(
            title="Affordable Single Room for Students",
            price=2300000,
            area=20.0,
            district="Cau Giay",
            address="5/88 Tran Duy Hung Street",
            description="Private room with full services, but no kitchen.",
            image_url="https://rencity-bucket.s3-han02.fptcloud.com/images/5583cccf-df19-42c4-977b-580d4b621728.jpg",
            chutro_id=host.id
        ),
        Room(
            title="Luxury Studio near West Lake",
            price=6000000,
            area=32.0,
            district="Tay Ho",
            address="31/12/115 Lac Long Quan Street",
            description="A studio with luxury detail, full services with 2 bedrooms and 1 living room.",
            image_url="https://rencity-bucket.s3-han02.fptcloud.com/images/40954585-4fef-4f7b-a10d-1e75ae0110a8.jpg",
            chutro_id=host.id
        ),
        Room(
            title="Quiet Mezzanine Room in Alley",
            price=3500000,
            area=22.0,
            district="Dong Da",
            address="2/82 Chua Lang Street",
            description="Small room with full service, suit for 2-3 students.",
            image_url="https://rencity-bucket.s3-han02.fptcloud.com/images/0a366ecf-1e76-44e4-9492-dca5aa883536.webp",
            chutro_id=host.id
        ),
        Room(
            title="Modern Serviced Apartment with Balcony",
            price=8200000,
            area=55.0,
            district="Ba Dinh",
            address="2/285 Doi Can Street",
            description="Balcony, 2 private bedroom, and fingerprint lock.",
            image_url="https://rencity-bucket.s3-han02.fptcloud.com/images/54e5a672-1ede-4a99-9577-bea1ae900cc7.webp",
            chutro_id=host.id
        ),
                Room(
            title="Tiny room for 1-2 students",
            price=1500000,
            area=20.0,
            district="Cau Giay",
            address="2/122 Cau Giay Street",
            description="Small room with full service, No cooking.",
            image_url="https://rencity-bucket.s3-han02.fptcloud.com/images/d81dc3c9-e2ba-453a-a461-6b298c945fb7.webp",
            chutro_id=host.id
        ),
        Room(
            title="Modern Serviced Apartment with Luxury Style",
            price=4200000,
            area=35.0,
            district="Thanh Xuan",
            address="2/123 Nguyen Trai Street",
            description="New room, balcony, private kitchen, and fingerprint lock.",
            image_url="https://rencity-bucket.s3-han02.fptcloud.com/images/61dac535-3fee-4731-8149-485720dbc4d5.webp",
            chutro_id=host.id
        ),
        Room(
            title="Convenient Studio near Metro Station",
            price=4000000,
            area=26.0,
            district="Thanh Xuan",
            address="1/17/288 Nguyen Trai Street",
            description="Near the bus stop metro station, near supermarket, restaurant,...",
            image_url="https://rencity-bucket.s3-han02.fptcloud.com/images/6351f9bb-e9da-44d6-8042-f6f191c94c61.jpg",
            chutro_id=host.id
        )
    ]

    db.session.bulk_save_objects(sample_rooms)
    db.session.commit()

    print("Database seeded successfully!")