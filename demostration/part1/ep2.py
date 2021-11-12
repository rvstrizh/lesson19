import calendar
import datetime

import jwt

secret = 's3cR$eT'
algo = 'HS256'


def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    return jwt.encode(data, secret, algorithm=[algo])


def check_token(token):
    try:
        jwt.decode(token, secret, algorithms=[algo])
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    data = {
        'username': 'myname',
        'role': 'user'
    }
    token = generate_token(data)
    is_ok = check_token(token)
