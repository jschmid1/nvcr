from app import db, bcrypt, app, Base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
import datetime
import jwt


class User_Bill(db.Model):
  __tablename__ = 'user_bill'
  #id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
  bill_id = Column(Integer, ForeignKey('bill.id'), primary_key=True)

  user = relationship("User", backref=backref("user_bill", cascade="all, delete-orphan" ))
  bill = relationship("Bill", backref=backref("user_bill", cascade="all, delete-orphan" ))

  def __repr__(self):
    return '<User_Bill {} - {}>'.format(self.user.name, self.bill.amount)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    flat_id = db.Column(db.Integer, db.ForeignKey('flat.id'))
    flat = db.relationship("Flat", back_populates="users")
    bills = db.relationship("Bill", back_populates="owner")
    _password = db.Column(db.Binary(60), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    bills_i_payed_for = relationship("Bill", secondary="user_bill")


    def __init__(self, plaintext_password=None, name=None, email=None, flat=None):
        self.name = name
        self.email = email
        self.hash_pw = plaintext_password
        self.authenticated = False
        self.registered_on = datetime.datetime.now()

    @property
    def password(self):
        return self._password

    @password.setter
    def hash_pw(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def __repr__(self):
        return '<User: {}>'.format(self.email)    

class Bill(db.Model):
    __tablename__ = 'bill'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'))
    market = db.relationship("Market", back_populates="bills")
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship("User", back_populates="bills")

    participants = relationship("User", secondary="user_bill")

    def __repr__(self):
        return '<Bill: {}>'.format(self.amount)    

class Flat(db.Model):
    __tablename__ = 'flat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    users = db.relationship("User", back_populates="flat")

    def __repr__(self):
        return '<Flat: {}>'.format(self.name)    

class Market(db.Model):
    __tablename__ = 'market'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    bills = db.relationship("Bill", back_populates="market")

    def __repr__(self):
        return '<Market: {}>'.format(self.name)    

