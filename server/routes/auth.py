from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from db_csv import get_user_by_email, create_user

auth_bp = Blueprint("auth", __name__)

JWT_SECRET = os.getenv("JWT_SECRET", "mysecretkey")

@auth_bp.route("/api/auth/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"message": "Please fill all fields"}), 400

        user_exists = get_user_by_email(email)
        if user_exists:
            return jsonify({"message": "Email already exists"}), 400

        hashed_password = generate_password_hash(password)
        new_user = create_user(username, email, hashed_password)

        token = jwt.encode(
            {
                "id": new_user["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
            },
            JWT_SECRET,
            algorithm="HS256"
        )
        
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return jsonify({
            "message": "User Registered Successfully",
            "token": token,
            "user": {
                "id": new_user["id"],
                "username": new_user["username"],
                "email": new_user["email"]
            }
        }), 201

    except Exception as e:
        print(e)
        return jsonify({"message": "Server Error"}), 500

@auth_bp.route("/api/auth/signin", methods=["POST"])
def signin():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Please fill all fields"}), 400

        user = get_user_by_email(email)
        if not user:
            return jsonify({"message": "User not found"}), 400

        if not check_password_hash(user["password"], password):
            return jsonify({"message": "Invalid Password"}), 400

        token = jwt.encode(
            {
                "id": user["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
            },
            JWT_SECRET,
            algorithm="HS256"
        )
        
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return jsonify({
            "message": "Login Successful",
            "token": token
        }), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Server Error"}), 500
