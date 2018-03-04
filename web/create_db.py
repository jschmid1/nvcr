# create_db.py
from app import db
from app.models import User, Flat, Bill, Market


qr = db.session.query
db.create_all()

if not qr(Flat).first():
    flat = Flat(name='test')
    db.session.add(flat)
if not qr(User).first():
    user1 = User(name='John', email='test@test.com', plaintext_password='test')
    user2 = User(name='Adl', email='adl@test.com', plaintext_password='test')
    user1.flat = flat
    user2.flat = flat
    db.session.add(user1)
    db.session.add(user2)
if not qr(Market).first():
    market2 = Market(name='Aldi')
    market1 = Market(name='Lidl')
    db.session.add(market1)
    db.session.add(market2)
if not qr(Bill).first():
    for i in range(1, 100):
        bill1 = Bill(amount=10.1, owner_id=user1.id, owner=user1, market=market2, participants=[user1, user2])
        db.session.add(bill1)

db.session.commit()

