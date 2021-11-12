from flask import request, abort, Flask
from flask_restx import Api, Resource


def login_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        return func(*args, **kwargs)

    return wrapper


app = Flask(__name__)
api = Api(app)
book_ns = api.namespace('')


@book_ns.route('/books')
class BooksView(Resource):
    def get(self):
        return [], 200

    @login_required
    def post(self):
        return "", 201


if __name__ == '__main__':
    app.run(debug=False)
