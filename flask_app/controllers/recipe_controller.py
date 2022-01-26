from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.controllers import user_controller

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    return render_template('single_recipe.html', logged_in_user = User.get_one_by_id({"id": session['uuid']}), recipe = Recipe.get_one({'id': recipe_id}))

@app.route('/recipe/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    return render_template('edit_recipe.html', recipe = Recipe.get_one({'id': recipe_id}))

@app.route('/recipe/update/<int:recipe_id>', methods = ["POST"])
def update_recipe(recipe_id):
    if not Recipe.validator(request.form):
        return redirect(f'/recipe/edit/{recipe_id}')
    update_data = {
        **request.form,
        "id": recipe_id
    }
    Recipe.edit(update_data)
    return redirect('/dashboard')

@app.route('/recipe/new')
def new_recipe():
    return render_template('new_recipe.html')

@app.route('/recipe/create', methods = ['POST'])
def create_recipe():
    if not Recipe.validator(request.form):
        return redirect('/recipe/new')
    data = {
        **request.form,
        "user_id": session["uuid"]
    }
    Recipe.create(data)
    return redirect('/dashboard')

@app.route('/recipe/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    data = {"id": recipe_id}
    Recipe.delete(data)
    return redirect('/dashboard')
