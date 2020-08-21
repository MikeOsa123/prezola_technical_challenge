from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegisterForm, WeddingForm
from app.models import User, List, Product, Wedding, Listitem
from app.helper import MergeDicts

'''
All routes relating to guest experience
'''

@app.route('/wedding-list-result')
def wedding_list_result():
    try:
        results = List.query.filter(List.id==session["wedding_list_id"]).first()
        wedding = Wedding.query.filter(Wedding.user_id==results.user_id).first()
        user = User.query.filter(User.id==results.user_id).first()
        return render_template('wedding_list_results.html', title='Wedding-List', wedding_list_id=session["wedding_list_id"], user=user, wedding=wedding)        
    except Exception as e:
        print(e)

@app.route('/wedding-list/', methods=["GET", "POST"])
def purchase_list():
    
    results = List.query.filter(List.id==session["wedding_list_id"]).first()
    wedding = Wedding.query.filter(Wedding.user_id==results.user_id).first()
    user = User.query.filter(User.id==results.user_id).first()
    #find list item id from list id to retrieve product and listitem data
    listitem_id = Listitem.query.filter(Listitem.list_id==session["wedding_list_id"]).first()
    products = db.session.query(Product.name, Product.id, Product.brand, Product.price, Listitem.quantity).join(Listitem, Listitem.product_id == Product.id).filter(Listitem.user_id==listitem_id.user_id).all()
    return render_template('purchase_list.html', products=products, wedding=wedding, user=user)

@app.route('/find-list', methods=["GET", "POST"])
def find_list():
    if request.method == "POST":
        # search for list
        wedding_list_id = request.form['wedding_list_id']
        try:
            results = List.query.filter(List.id==wedding_list_id).first()
            session["wedding_list_id"] = wedding_list_id
            flash("Found wedding list")
            return redirect(url_for('wedding_list_result'))
        except Exception as e:
            print(e)

        
    return render_template('wedding_list_search.html', title='Search Wedding List')