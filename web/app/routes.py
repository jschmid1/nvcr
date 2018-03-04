from app import app, db, bcrypt
from app.models import User, Bill, Market, Flat
from flask import Flask, Response, redirect, url_for, request, session, abort, jsonify, make_response, g, render_template, Response
from functools import wraps
import logging

log = logging.getLogger(__name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                g.current_user = user
                # Valid auth token
                return f(*args, **kwargs)
            # You did not provide a propoer token..
            return redirect(url_for('login', next=request.url))
        else:
            # No auth token sent with the request
            return redirect(url_for('login', next=request.url))
    return decorated_function


@app.route('/api/secret')
@login_required
def secret():
    message = "Hello {}".format(g.current_user.name)
    responseObject = {
        'message': message
    }
    return make_response(jsonify(responseObject)), 201


@app.route('/api/register', methods=['POST'])
def register():
    if request.method == 'POST':
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                return construct_response('success', 'succesfully registered', 201)
            except Exception as e:
                return construct_response('fail', 'Error - Please try again later', 401)
        else:
            return construct_response('fail', 'User already exists. Please log in', 202)


# somewhere to login
@app.route("/api/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                   email=post_data.get('email')
                   ).first()
            if user and bcrypt.check_password_hash(user.password, post_data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    return construct_response('success',
                                              'Successfully logged in',
                                              200,
                                              payload={'auth_token': auth_token.decode(),
                                                       'id_token': user.id})
            else:
                return construct_response('fail', 'User does not exist', 404)
        except Exception as e:
            print(e)
            return construct_response('fail', 'try again', 500)


def construct_response(status, message, ret_code=200, payload={}):
    responseObject = {
        'status': status,
        'message': message
    }
    responseObject.update(payload)
    return make_response(jsonify(responseObject)), ret_code


@app.route("/api/logout")
@login_required
def logout():
    try:
        logout_user()
        return construct_response('success', 'logged out', 200)
    except Exception as e:
        return construct_response('fail', 'failed to logout', 500)


@app.route('/api/bills')
# @login_required
def bills():
    # displays only the Bills that the user was part of.
    # are there also the bills included that he 'owns?'
    # shall I include the Bills that belong to the Flat? No, I don't think so..
    # Noone should bother about other people if he's not involved, right..

    # bills = g.current_user.bills_i_payed_for
    bills = User.query.first().bills_i_payed_for
    pl = []
    if bills:
        for bill in bills:
            payload = {'id': bill.id,
                       'amount': bill.amount,
                       'participants': ', '.join([u.name for u in bill.participants]),
                       'owner': bill.owner.name,
                       'market': bill.market.name}
            pl.append(payload)
        return construct_response('success', 'bills', 200, payload={'bills': pl})


@app.route('/api/markets')
# @login_required
def markets():
    markets = Market.query.all()
    ma = []
    if markets:
        for market in markets:
            payload = {'id': market.id,
                       'name': market.name}
            ma.append(payload)
        return construct_response('success', 'markets', 200, payload={'markets': ma})

@app.route('/api/users')
# @login_required
def users():
    users = User.query.all()
    us = []
    if users:
        for user in users:
            payload = {'id': user.id,
                       'name': user.name,
                       'avatar': 'https://placeimg.com/75/75/arch'
                       }
            us.append(payload)
        return construct_response('success', 'users', 200, payload={'users': us})

class ModelNotFound(Exception):
    """
    Can't find User
    """
    # TODO change message to reference _model_
    pass


def query_for_name(model, value):
    model_ret = model.query.filter_by(name=value).first()
    if not isinstance(model_ret, model):
        raise ModelNotFound()
    return model_ret


def query_for_id(model, value):
    model_ret = model.query.get(int(value))
    if not isinstance(model_ret, model):
        raise ModelNotFound()
    return model_ret


def calc_share(current_user, bill_owner, market, amount, participants):
    amount = float(amount)
    bill_owner.balance += amount
    try:
        stake = (amount / len(participants))
    except ZeroDivisionError as e:
        log.error("Division by Zero.. more information in logging")
        return construct_response('fail', 'Division by Zero detected', 400,
                                  payload={'err': 'test'})

    parts = []
    for user in participants:
        parts.append(user)
        user.balance -= stake
    new_bill = Bill(market=market,
                    amount=amount,
                    owner=bill_owner,
                    participants=parts)
    return new_bill

class EmptyReturn(Exception):
    """
    Validation Error. Insufficient or malformed return data
    """
    pass

def validate_input(*arg):
    for data in arg:
        # TODO: also check for negative input
        if data is None:
            raise EmptyReturn
        if isinstance(data, list) and not data:
            raise EmptyReturn
        if isinstance(data, str) and not data:
            raise EmptyReturn

@app.route("/api/bills/new", methods=["POST"])
def new_bill():
    # TODO fix todo retrieval
    current_user = User.query.first()

    post_data = request.get_json()

    bill_owner = post_data.get('owner_id')
    market = post_data.get('selected_market')
    participants = post_data.get('selected_members')
    date = post_data.get('date')
    amount = post_data.get('price')

    try:
        validate_input(bill_owner,
                       market,
                       participants,
                       date,
                       amount)
    except EmptyReturn:
        return construct_response('fail', 'missing or malformed data passed', 400)

    bill_owner = query_for_id(User, bill_owner)
    market = query_for_name(Market, market)
    participants = [query_for_name(User, user['name'].strip())
                    for user in participants
                    if user]

    new_bill = calc_share(current_user,
                          bill_owner,
                          market,
                          amount,
                          participants)

    if isinstance(new_bill, tuple):
        if isinstance(new_bill[0], Response):
            return new_bill

    db.session.add(new_bill)
    db.session.commit()
    return construct_response('success', 'bill', 200,
                              payload={'bill': 'Accepted new bill',
                                       'id': new_bill.id})


@app.route('/api/bills/<int:bill_id>', methods=["GET"])
def show_bill(bill_id):
    bill = Bill.query.get(bill_id)
    return construct_response('success', 'bill-{}'.format(bill.id), 200,
                              payload={'amount': bill.amount,
                                       'participants': bill.participant_names(),
                                       'owner': bill.owner.name,
                                       'market': bill.market.name})


@app.route('/api/markets/<int:market_id>', methods=["GET"])
def show_market(market_id):
    market = Market.query.get(market_id)
    return construct_response('success', 'market-{}'.format(market.id), 200,
                              payload={'market': market.name})


@app.route('/api/users/<int:user_id>', methods=["GET"])
def show_user(user_id):
    # temp
    user = User.query.get(user_id)
    # Serialize with json -> see bzr
    bills = Bill.query.all()
    #return render_template('index.html', title='Home', user=user, bills=bills)
    return construct_response('success', 'user-{}'.format(user.id), 200,
                              payload={'user': user.name,
                                       'balance': user.balance})


@app.route('/api/flat/<int:flat_id>', methods=["GET"])
def show_flat(flat_id):
    flat = Flat.query.get(flat_id)
    # Serialize with json -> see bzr
    return construct_response('success', 'user-{}'.format(flat.id), 200,
                              payload={'name': flat.name,
                                       'members': flat.member_names()})


@app.route('/')
def hw():
    return 'hello_world'
