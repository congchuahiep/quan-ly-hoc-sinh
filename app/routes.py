from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app import app
from app.auth import auth_user, role_required


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', title='Login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
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
    user = current_user._get_current_object()
    
    basic_info = user.get_basic_info()
    nav_items = user.get_nav_item_by_role()
    data = user.get_dashboard_data()
    
    return render_template(
        'dashboard.html',
        title='Tổng quan',
        nav_items=nav_items,
        basic_info=basic_info,
        data=data,
    )
    
@app.route('/score')
@login_required
@role_required('GiaoVien')
def score():
    user = current_user._get_current_object()
    
    basic_info = user.get_basic_info()
    nav_items = user.get_nav_item_by_role()
    
    return render_template(
        'score.html',
        title='Quản lý bảng điểm',
        basic_info=basic_info,
        nav_items=nav_items
    )