import random

def get_nam_hoc(hoc_ky):
    return hoc_ky // 10

def get_hoc_ky(nam_hoc):
    return (nam_hoc * 10 + 1, nam_hoc * 10 + 2)

def get_nam_sinh(nam_hoc, khoi_lop):
    
    mapping = {
        21: {10: 2006, 11: 2005, 12: 2004},
        22: {10: 2007, 11: 2006, 12: 2005},
        23: {10: 2008, 11: 2007, 12: 2006},
        24: {10: 2009, 11: 2008, 12: 2007}
    }
    return mapping.get(nam_hoc, {}).get(khoi_lop)

def chia_cac_phan_ngau_nhien(tong, so_phan, min_val, max_val):
    """
    Chia một tổng thành các phần ngẫu nhiên với ràng buộc. Phục vụ chính
    cho việc chia số lượng các học sinh trong một năm học mới, chia đều
    học sinh ra vào các lớp một cách ngẫu nhiên

    Args:
        tong: Tổng cần chia.
        so_phan: Số phần cần chia.
        min_val: Giá trị tối thiểu của mỗi phần.
        max_val: Giá trị tối đa của mỗi phần.

    Returns:
        Một list chứa các phần đã chia, hoặc None nếu không thể chia.
    """

    if tong < so_phan * min_val or tong > so_phan * max_val:
        return None  # Không thể chia với ràng buộc này

    phan_ban_dau = tong // so_phan  # Giá trị ban đầu cho mỗi phần
    phan_con_lai = tong % so_phan   # Phần dư

    ket_qua = [phan_ban_dau] * so_phan

    # Phân bổ phần dư vào các phần đầu tiên
    for i in range(phan_con_lai):
        ket_qua[i] += 1
    
    do_lech_tong = 0

    for i in range(so_phan):
        do_lech = random.randint(-min(phan_ban_dau - min_val, max_val - phan_ban_dau, 5), min(phan_ban_dau - min_val, max_val - phan_ban_dau, 5))
        ket_qua[i] += do_lech
        do_lech_tong += do_lech

    # Điều chỉnh để đảm bảo tổng bằng với giá trị ban đầu
    do_lech_can_dieu_chinh = 0 - do_lech_tong
    
    for i in range(abs(do_lech_can_dieu_chinh)):
        if do_lech_can_dieu_chinh > 0:
            index = random.randint(0, so_phan -1)
            if ket_qua[index] + 1 <= max_val:
                ket_qua[index] += 1
            else:
                continue
        elif do_lech_can_dieu_chinh < 0:
            index = random.randint(0, so_phan -1)
            if ket_qua[index] - 1 >= min_val:
                ket_qua[index] -= 1
            else:
                continue
    
    return ket_qua