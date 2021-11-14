import calendar
import datetime

import jwt
from flask import request, Flask
from flask_restx import abort, Api, Resource, Namespace

secret = 's3cR$eT'
algo = 'HS256'


class Config(object):
    DEBUG = True
    SECRET_HERE = '249y823r9v8238r9u'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, secret, algorithms=[algo])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    api = Api(app)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)


auth_ns = Namespace('auth')


def generate_tokens():
    data = {
        "username": "yser",
        "role": "role"
    }

    # 30 min access_token живет
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, secret, algorithm=algo)
    return {"access_token": access_token}


@auth_ns.route('/')
class AuthsView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None in [username, password]:
            return "", 400

        tokens = generate_tokens()

        return tokens, 201


user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def delete(self):
        return "", 204


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
