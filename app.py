import datetime
import pandas as pd
import streamlit as st

st.title("Lập Bảng Kế Hoạch Trả Nợ Vay")

# Nhập thông tin đầu vào
so_tien_vay = st.number_input("Số tiền vay (VNĐ):", value=700_000_000, step=10_000_000)
thoi_han_nam = st.number_input("Thời hạn vay (năm):", value=5, step=1)
ls_dau = st.number_input("Lãi suất 3 tháng đầu (%/năm):", value=9.0, step=0.1) / 100
ls_huy_dong = st.number_input("Lãi suất huy động từ tháng 4 (%/năm):", value=10.0, step=0.1) / 100
bien_do = st.number_input("Biên độ (%/năm):", value=4.0, step=0.1) / 100
ngay_giai_ngan = st.date_input("Ngày giải ngân:", value=datetime.date(2023, 10, 22))
so_ky = st.number_input("Số kỳ cần lập (tháng):", value=5, step=1)

if st.button("Lập bảng kế hoạch trả nợ"):
    thang_tong = thoi_han_nam * 12
    goc_hang_thang = so_tien_vay / thang_tong
    du_no = so_tien_vay
    ngay_truoc = ngay_giai_ngan
    ls_sau = ls_huy_dong + bien_do

    data = []
    for ky in range(1, int(so_ky) + 1):
        # Ngày thu tiền cố định ngày 15 hàng tháng
        if ky == 1:
            thang = ngay_giai_ngan.month + 1
            nam = ngay_giai_ngan.year
            if thang > 12:
                thang = 1
                nam += 1
            ngay_thu = datetime.date(nam, thang, 15)
        else:
            thang = ngay_truoc.month + 1
            nam = ngay_truoc.year
            if thang > 12:
                thang = 1
                nam += 1
            ngay_thu = datetime.date(nam, thang, 15)

        so_ngay = (ngay_thu - ngay_truoc).days
        ls = ls_dau if ky <= 3 else ls_sau

        # Tính số ngày trong năm (365 hoặc 366 năm nhuận)
        nam_nhuan = (ngay_truoc.year % 4 == 0 and ngay_truoc.year % 100 != 0) or (ngay_truoc.year % 400 == 0)
        so_ngay_trong_nam = 366 if nam_nhuan else 365

        tien_lai = du_no * ls * (so_ngay / so_ngay_trong_nam)
        tong_tra = goc_hang_thang + tien_lai
        du_no_cuoi = du_no - goc_hang_thang

        data.append({
            "Kỳ": ky,
            "Ngày thu": ngay_thu.strftime("%d/%m/%Y"),
            "Dư nợ đầu kỳ": f"{round(du_no):,}",
            "Số ngày": so_ngay,
            "Lãi suất (%/năm)": f"{ls * 100:.1f}%",
            "Tiền gốc": f"{round(goc_hang_thang):,}",
            "Tiền lãi": f"{round(tien_lai):,}",
            "Tổng phải trả": f"{round(tong_tra):,}",
            "Dư nợ cuối kỳ": f"{round(max(0, du_no_cuoi)):,}"
        })

        ngay_truoc = ngay_thu
        du_no = du_no_cuoi

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
