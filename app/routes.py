from flask import jsonify, redirect, render_template, request, url_for
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
    
    # Basic data
    basic_info = user.get_basic_info()
    nav_items = user.get_nav_item_by_role()
    
    # Functional Data
    data = user.get_dashboard_data()
    
    return render_template(
        'dashboard.html',
        title='Tổng quan',
        nav_items=nav_items,
        basic_info=basic_info,
        data=data,
    )
    
@app.route('/score', methods=['POST', 'GET'])
@login_required
@role_required('GiaoVien')
def score():
    from models import HocKy
    
    user = current_user._get_current_object()
    
    if request.method == 'POST':
        mon_hoc_id = request.json.get('mon_hoc_id')
        hoc_ky_id = request.json.get('hoc_ky_id')
        lop_hoc_id = request.json.get('lop_hoc_id')
        
        print(mon_hoc_id)
        print(hoc_ky_id)
        print(lop_hoc_id)
        
        return user.get_bang_diem_mon_hoc(mon_hoc_id, hoc_ky_id, lop_hoc_id)
    
    # Basic data
    basic_info = user.get_basic_info()
    nav_items = user.get_nav_item_by_role()
    
    # Functional Data
    danh_sach_lop_day = user.lop_giao_vien_day
    danh_sach_hoc_ky = HocKy.query.order_by(HocKy.id.desc()).all()
    
    return render_template(
        'score.html',
        title='Quản lý bảng điểm',
        basic_info=basic_info,
        danh_sach_lop_day=danh_sach_lop_day,
        danh_sach_hoc_ky=danh_sach_hoc_ky,
        nav_items=nav_items
    )
    
@app.route('/get-teach-class', methods=['POST'])
@login_required
@role_required('GiaoVien')
def get_teach_class():
    user = current_user._get_current_object()
    hoc_ky_id = request.json.get('hoc_ky_id')
    
    danh_sach_lop_day = user.get_info_lop_giao_vien_day(hoc_ky_id=hoc_ky_id)
    
    return jsonify(danh_sach_lop_day)

@app.route('/update_bang_diem', methods=['POST'])
@login_required
@role_required('GiaoVien')
def update_bang_diem():
    from models import BangDiem
    from app import db
    
    try:
        up_date_bang_diem_data = request.json.get('bang_diem')
        print(up_date_bang_diem_data)
        
        bang_diem = BangDiem.query.get(up_date_bang_diem_data["bang_diem_id"])
        print(bang_diem)
        
        bang_diem.refresh_cot_diem_15_phut()
        for diem_15_phut in up_date_bang_diem_data["diem_15_phuts"]:
            bang_diem.add_cot_diem_15_phut(diem_15_phut)
            
        bang_diem.refresh_cot_diem_mot_tiet()
        for diem_mot_tiet in up_date_bang_diem_data["diem_mot_tiets"]:
            bang_diem.add_cot_diem_mot_tiet(diem_mot_tiet)
            
        db.session.commit()
            
        bang_diem.update_diem_cuoi_ky(up_date_bang_diem_data["diem_cuoi_ky"])
        
        return jsonify(bang_diem.get_bang_diem())
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400  # Trả về mã lỗi 400 và thông điệp lỗi

    except Exception as e:
        return jsonify({"error": "Đã xảy ra lỗi, vui lòng thử lại."}), 500  # Trả về mã lỗi 500 cho lỗi khác
    
@app.route('/homeroom')
@login_required
@role_required('GiaoVien')
def homeroom():
    from models import HocKy
    
    user = current_user._get_current_object()
    
    # Basic data
    basic_info = user.get_basic_info()
    nav_items = user.get_nav_item_by_role()
    
    # Functional Data
    lop_hoc = user.get_lop_chu_nhiem(HocKy.nam_hoc_hien_tai())
    danh_sach_lop = lop_hoc.get_danh_sach_hoc_sinh(doi_tuong=True)
    si_so = len(danh_sach_lop)
    
    return render_template(
        'homeroom.html',
        title='Thông tin lớp chủ nhiệm',
        basic_info=basic_info,
        nav_items=nav_items,
        lop_hoc=lop_hoc,
        danh_sach_lop=danh_sach_lop,
        si_so = si_so
    )