from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models import recipe

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, data):
        query = (
            "INSERT INTO users (first_name, last_name, email, password) "
            "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        )
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = (
            "SELECT * FROM users;"
        )
        results = connectToMySQL('recipes').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one_by_id(cls, data):
        query = (
            "SELECT * FROM users "
            "WHERE id = %(id)s;"
        )
        results = connectToMySQL('recipes').query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_one_by_email(cls, data):
        query = (
            "SELECT * FROM users "
            "WHERE email = %(email)s"
        )
        results = connectToMySQL('recipes').query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash("First Name minimum of 2 characters")
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("Last Name minimum of 2 characters")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be a minimum of 8 characters")
            is_valid = False
        if not form_data['password'] == form_data['confirm_password']:
            flash("Passwords must match")
            is_valid = False
        return is_valid