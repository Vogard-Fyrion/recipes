from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.controllers import recipe_controller
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if "uuid" in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('recipes.html', logged_in_user = User.get_one_by_id({"id": session['uuid']}), all_recipes = Recipe.get_all())

@app.route('/user/create', methods = ['POST'])
def register():
    if not User.validator(request.form):
        return redirect('/')
    hashbrowns = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashbrowns
    }
    session['uuid'] = User.create(data)
    return redirect('/dashboard')

@app.route('/user/login', methods = ['POST'])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_one_by_email(data)
    if not user_in_db:
        flash("Invalid Email or Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email or Password")
        return redirect('/')
    session['uuid'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')