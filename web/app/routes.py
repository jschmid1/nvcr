from app import app, db, bcrypt
from app.models import User
from flask import Flask, Response, redirect, url_for, request, session, abort, jsonify, make_response, g
from functools import wraps

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
            if user and bcrypt.check_password_hash(
                user.password, post_data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    return construct_response('success', 
                                              'Successfully logged in', 
                                              200, 
                                              payload={'auth_token': auth_token.decode()})
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

#               /v1/
@app.route('/api/bills')
#@login_required
def bills():
    # displays only the Bills that the user was part of.
    # are there also the bills included that he 'owns?'
    # shall I include the Bills that belong to the Flat? No, I don't think so..
    # Noone should bother about other people if he's not involved, right..

    #bills = g.current_user.bills_i_payed_for
    bills = User.query.first().bills_i_payed_for
    pl = []
    if bills:
        for bill in bills:
            payload = { 'id': bill.id,
                        'amount': bill.amount,
                        'participants': ', '.join([u.name for u in bill.participants]),
                        'owner': bill.owner.name,
                        'market': bill.market.name
                      }
            pl.append(payload)
        return construct_response('success', 'bills', 200, payload={'bills': pl})

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    # temp
    user = User.query.first()
    # Serialize with json -> see bzr
    return construct_response('success', 'user-{}'.format(user.id), 200, payload={'user': user.name})

@app.route('/')
def hw():
    return 'hello_world'
