from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegisterForm, WeddingForm
from app.models import User, List, Product, Wedding, Listitem
from app.helper import MergeDicts

# Landing page route
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    user = {'username': 'Michael'}
    return render_template('index.html', title='Home', user=user)
