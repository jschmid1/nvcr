from app import app, db
from app.models import User, Flat, Bill, Market, User_Bill

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 
            'qr': db.session.query,
            'User': User, 
            'Flat': Flat,
            'Bill': Bill,
            'User_Bill': User_Bill,
            'Market': Market}
