from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
        responseObject = {
            'status': 'success',
            'message': 'Request successful but please send an HTTP POST request to register the user. Test 1'
        }
        return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        post_data = request.get_json(); 

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
                print("User id is ", user.id)

                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.',
                    'error message': e
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

class viewUsers(MethodView):
    def get(self):
        users = User.query.all()
        usersArray = []

        for user in users:
            userObject = {
                "id": user.id,
                "email": user.email,
                "registered_on": user.registered_on,
                "admin": user.admin
            }
            usersArray.append(userObject)

        responseObject = {
            'status': 'Success',
            'message': 'All registered users are returned.',
            'users': usersArray
        }
        return make_response(jsonify(responseObject)), 200

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
listUsers_view = viewUsers.as_view('listUsers_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)

auth_blueprint.add_url_rule(
    '/users/index',
    view_func=listUsers_view,
    methods=['GET']
)