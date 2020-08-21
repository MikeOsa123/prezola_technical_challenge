from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegisterForm, WeddingForm
from app.models import User, List, Product, Wedding, Listitem
from app.helper import MergeDicts

'''
All routes related to dealing with the shopping basket and checkout
'''

@app.route('/add_basket', methods=["POST"])
def addBasket():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == "POST":
            DictItems = {product_id: {'name': product.name, 'price': product.price, 'brand':product.brand, 'quantity': quantity}}
            if 'Shoppingbasket' in session:
                print(session['Shoppingbasket'])
                if product_id in session['Shoppingbasket']:
                    print("This product is already in your list!")
                else:
                    session["Shoppingbasket"] = MergeDicts(session['Shoppingbasket'], DictItems)
                    return redirect(url_for('purchase_list'))
            else:
                session["Shoppingbasket"] = DictItems
                return redirect(url_for('purchase_list'))
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('purchase_list'))

@app.route('/wedding-list/basket')
def getBasket():
    if 'Shoppingbasket' not in session:
        return redirect(url_for(request.referrer))
    subtotal = 0   
    grandtotal = 0
    for key, product in session['Shoppingbasket'].items():
        price = product['price'].replace("GBP","")
        subtotal += float(price) * int(product['quantity'])
        grandtotal = float("%.2f" % (subtotal))

    return render_template('shopping_basket.html', grandtotal=grandtotal)

@app.route('/updatebasket/<int:id>', methods=["POST"])
def updateBasket(id):
    if 'Shoppingbasket' not in session and len(session["Shoppingbasket"]) <= 0:
        return redirect(url_for('index'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Shoppingbasket'].items():
                if int(key) == id:
                    item["quantity"] = quantity
                    flash('Item is updated')
                    redirect(url_for('getBasket'))
        except Exception as e:
            print(e)
            return redirect(url_for('getBasket'))

@app.route('/wedding-list/basket/deleteitem/<int:id>')
def removeBasketItem(id):
    if 'Shoppingbasket' not in session and len(session['Shoppingbasket']) <= 0:
        return redirect(url_for('index'))
    try:
        session.modified = True
        for key, item in session['Shoppingbasket'].items():
            if int(key) == id:
                session['Shoppingbasket'].pop(key, None)
                return redirect(url_for('getBaset'))
    except Exception as e:
        print(e)
        return redirect(url_for('getBasket'))

@app.route('/empty')
def empty_basket():
    try:
        session.clear()
        return redirect(url_for('index'))
    except Exception as e:
        print(e)

@app.route('/checkout')
def checkout():
    session['Shoppingbasket'] = {}
    flash("CHECKOUT COMPLETE")
    return render_template('checkout.html')