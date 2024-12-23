import hashlib
from functools import wraps
from flask_login import current_user

from app import login_manager

# Nhập thông tin đăng nhập NguoiDung vào hệ thống
@login_manager.user_loader
def load_user(user_id):
    from models import NguoiDung
    
    return NguoiDung.query.get(user_id)


# Decorator yêu cầu quyền
def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapped_view(*args, **kwargs):
            if current_user.loai_nguoi_dung != required_role:
                return "Bạn không có quyền truy cập vào trang này!", 403
            return func(*args, **kwargs)
        return wrapped_view
    return decorator


# Xác thực thông tin đăng nhập
def auth_user(username, password):
    # Kiểm tra xem người dùng có tồn tại không
    from models import NguoiDung
    
    user = NguoiDung.query.filter_by(username=username).first()
    if user is None:
        return False

    # Kiểm tra mật khẩu có đúng không
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user.password != password_hash:
        return False

    return user


def get_nav_item_by_role():
    print(current_user._get_current_object())
    if current_user._get_current_object().check_loai_nguoi_dung('QuanTri'):
        return [
            {'href': 'dashboard', 'icon': '<i class="bi bi-grid me-2"></i>', 'title': 'Tổng quan'},
            {'href': 'login', 'icon': '', 'title': 'Contact'},
            {'href': 'login', 'icon': '', 'title': 'Setting'},
        ]
    if current_user._get_current_object().check_loai_nguoi_dung('GiaoVien'):
        return [
            {'href': 'dashboard', 'icon': '<i class="bi bi-grid me-2"></i>', 'title': 'Home'},
            {'href': 'login', 'icon': '', 'title': 'Contact'},
            {'href': 'login', 'icon': '', 'title': 'Setting'},
        ]
    if current_user._get_current_object().check_loai_nguoi_dung('NhanVien'):
        return [
            {'href': 'dashboard', 'icon': '<i class="bi bi-grid me-2"></i>', 'title': 'Home'},
            {'href': 'login', 'icon': '', 'title': 'Contact'},
            {'href': 'login', 'icon': '', 'title': 'Setting'},
        ]
    return []