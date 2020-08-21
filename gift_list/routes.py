from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegisterForm, WeddingForm
from app.models import User, List, Product, Wedding, Listitem
from app.helper import MergeDicts

'''
All routes relating to gift list
'''

@app.route('/add_list', methods=["POST"])
@login_required
def AddList():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == "POST":
            DictItems = {product_id: {'name': product.name, 'price': product.price, 'brand':product.brand, 'quantity': quantity}}
            if 'Giftlist' in session:
                print(session['Giftlist'])
                if product_id in session['Giftlist']:
                    print("This product is already in your list!")
                else:
                    session["Giftlist"] = MergeDicts(session['Giftlist'], DictItems)
                    return redirect(url_for('products'))
            else:
                session["Giftlist"] = DictItems
                return redirect(url_for('products'))
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('products'))

@app.route('/my-gift-list')
@login_required
def getGiftList():
    if len(session["Giftlist"]) == 0:
        try:
            my_gift_list = db.session.query(Product.name, Product.id, Product.brand, Product.price, Listitem.quantity).join(Listitem, Listitem.product_id == Product.id).filter(Listitem.user_id==current_user.id).all()
            for product in my_gift_list:
                print(product)
                DictItems = {product.id: {'name': product.name, 'price': product.price, 'brand':product.brand, 'quantity': product.quantity}}
                session["Giftlist"] = MergeDicts(session['Giftlist'], DictItems)
            return redirect(url_for('getGiftList'))
        except Exception as e:
            print(e)
        finally:
            flash('No Gifts in Database please add gifts to List')        
            return redirect(url_for('dashboard'))

    wedding = Wedding.query.filter_by(user_id=current_user.id).first()
    return render_template('my_gift_list.html', title='My Gift List', wedding=wedding)

@app.route('/my-gift-list/save', methods=["GET"])
@login_required
def saveList():
    wedding_list = List.query.filter_by(user_id=current_user.id).first()
    print(wedding_list)
    try:
        for key, item in session['Giftlist'].items():
            listitem= Listitem(list_id=wedding_list.id, product_id=key, quantity=item["quantity"], user_id=current_user.id, status="NOT PURCHASED")
            db.session.add(listitem)
            db.session.commit()
        flash('Gift List Saved on Database')
        return redirect(url_for('dashboard'))
    except Exception as e:
        print(e)
    finally:
        flash('Gift not Saved on Database')        
        return redirect(url_for('dashboard'))

@app.route('/my-gift-list/report', methods=["GET"])
@login_required
def giftListReport():
    wedding = Wedding.query.filter_by(user_id=current_user.id).first()
    # purchased = Listitem.query.join(Product, Product.id == Listitem.product_id).filter(Listitem.status=="PURCHASED").all()
    # not_purchased = Listitem.query.join(Product, Product.id == Listitem.product_id).filter(Listitem.status=="NOT PURCHASED").all()
    purchased = db.session.query(Product.name, Product.brand, Product.price, Listitem.quantity, Listitem.status).join(Listitem, Listitem.product_id == Product.id).filter(Listitem.status=="PURCHASED").filter(Listitem.user_id==current_user.id).all()
    not_purchased = db.session.query(Product.name, Product.brand, Product.price, Listitem.quantity, Listitem.status).join(Listitem, Listitem.product_id == Product.id).filter(Listitem.status=="NOT PURCHASED").filter(Listitem.user_id==current_user.id).all()
    for x in not_purchased:
        print(x)
    
    return render_template('list_report.html', title='Gift List Report', wedding=wedding, purchased=purchased, not_purchased=not_purchased)

@app.route('/my-gift-list/<int:id>', methods=["POST"])
@login_required
def updateList(id):
    if 'Giftlist' not in session and len(session["Giftlist"]) <= 0:
        return redirect(url_for('dashboard'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Giftlist'].items():
                if int(key) == id:
                    item["quantity"] = quantity
                    flash('Item is updated')
                    return redirect(url_for('getGiftList'))
        except Exception as e:
            print(e)
            return redirect(url_for('getGiftList'))

@app.route('/my-gift-list/deleteitem/<int:id>', methods=["GET"])
def removeListtItem(id):
    if 'Giftlist' not in session and len(session['Giftlist']) <= 0:
        return redirect(url_for('index'))
    try:
        session.modified = True
        for key, item in session['Giftlist'].items():
            if int(key) == id:
                session['Giftlist'].pop(key, None)
                return redirect(url_for('getGiftList'))
    except Exception as e:
        print(e)
        return redirect(url_for('getGiftList'))