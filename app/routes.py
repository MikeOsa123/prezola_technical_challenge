from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    user = {'username': 'Michael'}
    return render_template('index.html', title='Home', user=user)

@app.route('/find-list')
def find_list():
    return render_template('wedding_list_search.html', title='Search Wedding List')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember={}'.format(
            form.email.data, form.remember.data))
        return redirect('/dashboard')
    return render_template('login.html', title='Log In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', title='Register', form=form)

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
def dashboard():
    user = {
        "username":"Michael",
        "firstname":"Michael",
        "partner":"Mariam",
        "wedding_date": "22nd October 2021",
        "list_id": 12034
    }
    return render_template('dashboard.html', title='Dashboard', user=user)




