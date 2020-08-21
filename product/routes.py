from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegisterForm, WeddingForm
from app.models import User, List, Product, Wedding, Listitem
from app.helper import MergeDicts

'''
All routes relating to product
'''

@app.route('/products')
@login_required
def products():
    wedding = Wedding.query.filter_by(user_id=current_user.id).first()
    products = Product.query.all()
    return render_template('products.html', title='Products', products=products, wedding=wedding)