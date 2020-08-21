from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegisterForm, WeddingForm
from app.models import User, List, Product, Wedding
from app.helper import MergeDicts
# Landing page route
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    user = {'username': 'Michael'}
    return render_template('index.html', title='Home', user=user)

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
        session["user_id"] = user.id
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('wedding_registry'))
    return render_template('register.html', title='Register', form=form)

@app.route('/wedding_registry', methods=['GET', 'POST'])
def wedding_registry():
    user_name = session.get("user_name", None)
    user_id = session.get("user_id", None)
    print(user_name)
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
        flash('Congratulations, you can start creating your list!')
        return redirect(url_for('dashboard'))
    return render_template('wedding_register.html', title='Wedding Register', form=form, user_name=user_name)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/wedding-list-result')
def wedding_list_result():
    user = {
        "username":"Michael",
        "firstname":"Michael",
        "wedding_date": "22nd October 2021",
        "partner":"Mariam"
    }
    return render_template('wedding_list_results.html', title='Register', user=user, list_id=12034)

@app.route('/wedding-list/list_id')
def purchase_list():
    user = {
        "username":"Michael",
        "firstname":"Michael",
        "partner":"Mariam",
        "wedding_date": "22nd October 2021",
        "list_id": 12034
    }
    return render_template('purchase_list.html', title='{} x {} - #{}'.format('Michael', 'Mariam', 12034), user=user)

@app.route('/dashboard')
@login_required
def dashboard():
    wedding = Wedding.query.first()
    return render_template('dashboard.html', title='Dashboard', wedding=wedding)

@app.route('/products')
@login_required
def products():
    wedding = Wedding.query.first()
    products = Product.query.all()
    return render_template('products.html', title='Products', products=products, wedding=wedding)

@app.route('/find-list')
def find_list():
    return render_template('wedding_list_search.html', title='Search Wedding List')

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
    wedding = Wedding.query.first()
    return render_template('my_gift_list.html', title='My Gift List', wedding=wedding)

@app.route('/my-gift-list/save', methods=["POST"])
@login_required
def saveList():
    return redirect(url_for('dashboard'))

@app.route('/my-gift-list/report', methods=["POST"])
@login_required
def giftListReport():
    return render_template('list_report.html', title='Gift List Report', wedding=wedding)

@app.route('/wedding-list/basket')
def getBasket():
    if 'Shoppingbasket' not in session:
        return redirect(url_for(request.referrer))
    subtotal = 0   
    grandtotal = 0
    for key, product in session['Shoppingbasket'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        grandtotal = float("%.2f" % (subtotal))

    return render_template('shopping_basket.html', grandtotal=grandtotal)

@app.route('/updatebasket/<int:id>', methods=["POST"])
def updateCart(id):
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

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
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