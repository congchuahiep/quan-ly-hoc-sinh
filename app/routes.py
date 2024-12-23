from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app import app
from app.auth import auth_user, role_required, get_nav_item_by_role


@app.route('/base')
def base():
    
    nav_items = [
        {'href': 'base', 'icon': '<i class="bi bi-grid me-2"></i>', 'title': 'Tổng quan'},
        {'href': 'base2', 'status': 'link-body-emphasis', 'icon': '', 'title': 'Contact'},
        {'href': 'login', 'status': 'link-body-emphasis', 'icon': '', 'title': 'Setting'},
    ]
    
    return render_template('layout.html', title='Testing...', nav_items=nav_items)


@app.route('/base2')
def base2():
    
    nav_items = [
        {'href': 'base', 'icon': '<i class="bi bi-house me-1"></i>', 'title': 'Home'},
        {'href': 'base2', 'icon': '', 'title': 'Contact'},
        {'href': 'login', 'icon': '', 'title': 'Setting'},
    ]
    
    return render_template('layout.html', title='Testing...', nav_items=nav_items)


@app.route('/')
def index():
    return render_template('login.html', title='Login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Login')
    
    username = request.form['username']
    password = request.form['password']
    remember = request.form.get('remember', False)
    
    user = auth_user(username, password)
    print(user)
    if user:
        login_user(user, remember=remember)
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', title='Login', error='Invalid username or password')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    nav_items = get_nav_item_by_role()
    return render_template('dashboard.html', title='Tổng quan', nav_items=nav_items)