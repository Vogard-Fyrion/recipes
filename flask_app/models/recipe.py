from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models import user

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.quick = data["quick"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = user.User.get_one_by_id({"id": data["user_id"]})

    @classmethod
    def create(cls, data):
        query = (
            "INSERT INTO recipes (name, description, instructions, date_made, quick, user_id) "
            "VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(quick)s, %(user_id)s);"
        )
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = (
            "SELECT * FROM recipes;"
        )
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_one(cls, data):
        query = (
            "SELECT * FROM recipes "
            "WHERE id = %(id)s;"
        )
        results = connectToMySQL('recipes').query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def edit(cls, data):
        query = (
            "UPDATE recipes SET name = %(name)s, description = %(description)s, "
            "instructions = %(instructions)s, date_made = %(date_made)s, quick = %(quick)s "
            "WHERE id = %(id)s;"
        )
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = (
            "DELETE FROM recipes "
            "WHERE id = %(id)s;"
        )
        connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            flash("Name must be a minimum of 3 characters")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be a minimum of 3 characters")
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash("Instructions must be a minimum of 3 characters")
            is_valid = False
        if len(form_data['date_made']) < 8:
            flash("Must be a valid date")
            is_valid = False
        print(form_data)
        if not 'quick' in form_data:
            flash("Under 30 minutes must be 'Yes' or 'No'")
            is_valid = False
        return is_valid