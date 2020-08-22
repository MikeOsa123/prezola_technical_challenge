from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegisterForm, WeddingForm
from app.models import User, List, Product, Wedding, Listitem
from app.helper import MergeDicts

'''
All User related routes
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        return redirect(url_for('dashboard'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, firstname=form.firstname.data, surname=form.surname.data)
        user.set_password(form.password.data)
        session["user_name"] = user.firstname
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('wedding_registry'))
    return render_template('register.html', title='Register', form=form)

@app.route('/wedding_registry', methods=['GET', 'POST'])
def wedding_registry():
    user_name = session.get("user_name", None)
    user = User.query.filter_by(firstname = user_name).first()
    user_id = user.id
    print(user_name, user_id)
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = WeddingForm()
    print(form.errors)
    print(form.data)
    if form.validate_on_submit():
        wedding = Wedding(user_id=user_id, partner=form.partner.data, wedding_date=form.wedding_date.data)
        print(wedding)
        db.session.add(wedding)
        db.session.commit()
        user_list = List(user_id=user_id)
        db.session.add(user_list)
        db.session.commit()
        flash('Congratulations, you can start creating your list!')
        return redirect(url_for('dashboard'))
    return render_template('wedding_register.html', title='Wedding Register', form=form, user_name=user_name)

@app.route('/dashboard')
@login_required
def dashboard():
    wedding = Wedding.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard.html', title='Dashboard', wedding=wedding)

@app.route('/logout')
def logout():
    session['Giftlist'] = {}
    session['Shoppingbaske'] = {}
    logout_user()
    return redirect(url_for('index'))