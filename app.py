import os

from flask import Flask, jsonify
from flask_restful import Api, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required, JWTManager, set_access_cookies, unset_access_cookies
from resources.book import Book, BookList, Author, BookId
from resources.user import User, UserRegister, UserLogin, UserLogout
app = Flask(__name__)

from datetime import datetime
from datetime import timedelta
from datetime import timezone

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'SUPER-SECRET'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.secret_key = 'jose'
api = Api(app)

jwt = JWTManager(app)

api.add_resource(Author, '/book/author/<string:author>')
api.add_resource(Book, '/book')
api.add_resource(BookId, '/book/<int:_id>')
api.add_resource(BookList, '/books')



@app.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity='example_user')
    refresh_token = create_refresh_token(identity="example_user")
    return jsonify(access_token=access_token, refresh_token=refresh_token)

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@app.route('/protected')
@jwt_required()
def protected():
    return jsonify(foo="bar")

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)