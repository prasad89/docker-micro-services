import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from http import HTTPStatus

app = Flask(__name__)
CORS(app)

load_dotenv()

db_config = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT')
}


def db_conn():
    return psycopg2.connect(**db_config)


@app.route('/')
def home():
    return "Hello!"


@app.route('/users', methods=['GET'])
def show_users():
    try:
        conn = db_conn()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users ORDER BY id")

        users = cur.fetchall()
        cur.close()
        conn.close()

        all_users = []
        for user in users:
            user_data = {
                'name': user[1],
                'email': user[2],
                'phone': user[3]
            }
            all_users.append(user_data)

        return jsonify(all_users), HTTPStatus.OK

    except Exception as e:
        return jsonify(msg='Error while retrieving users.', error=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        if not name or not email or not phone:
            return jsonify(msg="All fields are required."), HTTPStatus.BAD_REQUEST

        conn = db_conn()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify(msg="User added successfully."), HTTPStatus.OK

    except Exception as e:
        return jsonify(msg="Error while adding user.", error=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get("email")
        phone = data.get("phone")

        if not name or not email or not phone:
            return jsonify(msg="All fields are required."), HTTPStatus.BAD_REQUEST

        conn = db_conn()
        cur = conn.cursor()

        cur.execute("UPDATE users SET name = %s, email = %s, phone = %s WHERE id = %s",
                    (name, email, phone, user_id))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify(msg="User updated successfully."), HTTPStatus.OK

    except Exception as e:
        return jsonify(msg="Error while updating user.", error=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = db_conn()
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify(msg="User deleted successfully."), HTTPStatus.OK

    except Exception as e:
        return jsonify(msg='Error while deleting the user.', error=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
