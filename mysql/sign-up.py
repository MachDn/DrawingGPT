# from flask      import Flask, jsonify, request
# from sqlalchemy import create_engine, text


# def create_app(test_config = None):
#     app = Flask(__name__)
#     app.config.from_pyfile('config.py')

#     database = create_engine(app.config['DB_URL'], encoding = 'utf-8')
#     app.database = database

#     @app.route('/sign-up', methods = ['POST'])
#     def sign_up():
#         user = request.json
#         user_id = app.database.execute(text("""
#                                             INSERT INTO users (
#                                             Name,
#                                             Age,
#                                             Text,
#                                             TIME
#                                           ) VALUES (
#                                             :Name,
#                                             :Age
#                                             :Text
#                                             :TIME
#                                           )
#                                             """), user).lastrowid

#         return "", 200

#     return app