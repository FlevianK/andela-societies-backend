"""
Authorisation Module.

This module contains the authorisation required by the client to
communicate with the API.
"""

import random
from functools import wraps

from flask import g, jsonify, request
from jose import ExpiredSignatureError, JWTError, jwt

from .models import Society, User


# authorization decorator
def token_required(f):
    """Authenticate that a valid Token is present."""
    @wraps(f)
    def decorated(*args, **kwargs):
        # check that the Authorization header is set
        authorization_token = request.headers.get('Authorization')
        if not authorization_token:
            response = jsonify({
                "message": "Bad request. Header does not contain authorization"
                           " token"
            })
            response.status_code = 400
            return response

        unauthorized_response = jsonify({
            "message": "Unauthorized. The authorization token supplied is"
                       " invalid"
        })
        unauthorized_response.status_code = 401

        invalid_response = jsonify({
            "message": "Bad request. The information supplied is invalid."
        })
        invalid_response.status_code = 400

        expired_response = jsonify({
            "message": "The authorization token supplied is expired"
        })
        expired_response.status_code = 401

        try:
            # decode token
            payload = jwt.decode(authorization_token, 'secret',
                                 options={"verify_signature": False})
        except ExpiredSignatureError:
            return expired_response
        except JWTError:
            return unauthorized_response

        expected_user_info_format = {
            "id": "user_id",
            "email": "gmail",
            "first_name": "test",
            "last_name": "user",
            "name": "test user",
            "picture": "link",
            "roles": {
                "Andelan": "unique_id",
                "Fellow": "unique_id"
            }
        }

        # confirm that payload and UserInfo has required keys
        if ("UserInfo" and "exp") not in payload.keys():
            return invalid_response
        elif payload["UserInfo"].keys() != expected_user_info_format.keys():
            return invalid_response
        else:
            uuid = payload["UserInfo"]["id"]
            name = payload["UserInfo"]["name"]
            email = payload["UserInfo"]["email"]
            photo = payload["UserInfo"]["picture"]
            roles = payload["UserInfo"]["roles"]

            user = User.query.get(uuid)

            # save user to db if they haven't been saved yet
            if not user:
                user = User(
                    uuid=uuid, name=name, email=email, photo=photo
                )

                user.society = random.choice(Society.query.all())
                user.save()

            # set current user in flask global variable, g
            user.roles = roles
            g.current_user = user

            # now return wrapped function
            return f(*args, **kwargs)
    return decorated


def roles_required(roles):  # roles should be a list
    """Ensure only authorised roles may access sensitive data."""
    def check_user_role(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.current_user.society_position not in roles:
                return {
                    "message": "You're unauthorized to perform this operation"
                }, 401
            return f(*args, **kwargs)
        return decorated
    return check_user_role
