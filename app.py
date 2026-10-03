import streamlit as st
st.image("IMG_0834.jpeg")
st.set_page_config(page_title="Tính Lãi Gửi Tiết Kiệm", page_icon="💰", layout="centered")

st.title("💰 Công Cụ Tính Lãi Gửi Tiết Kiệm")
st.caption("Ứng dụng hỗ trợ tính toán tiền lãi tiết kiệm theo lãi đơn và lãi kép")

st.markdown("---")

# --- NHẬP THÔNG TIN ---
st.subheader("📝 Nhập thông tin khoản gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "Số tiền gửi (VNĐ):",
        min_value=1_000_000,
        value=100_000_000,
        step=1_000_000,
        format="%d"
    )
    
    ky_han_thang = st.number_input(
        "Kỳ hạn gửi (tháng):",
        min_value=1,
        max_value=360,
        value=12,
        step=1
    )

with col2:
    lai_suat_nam = st.number_input(
        "Lãi suất (%/năm):",
        min_value=0.1,
        max_value=20.0,
        value=6.0,
        step=0.1,
        format="%.1f"
    )
    
    loai_lai = st.selectbox(
        "Loại lãi suất:",
        options=["Lãi đơn", "Lãi kép"]
    )

hinh_thuc_nhan = st.selectbox(
    "Hình thức nhận lãi:",
    options=["Cuối kỳ", "Hàng tháng", "Hàng quý"]
)

# --- XỬ LÝ TÍNH TOÁN ---
# Quy đổi tần số lĩnh lãi theo tháng (n)
if hinh_thuc_nhan == "Hàng tháng":
    so_thang_nhan = 1
elif hinh_thuc_nhan == "Hàng quý":
    so_thang_nhan = 3
else:  # Cuối kỳ
    so_thang_nhan = ky_han_thang

so_lan_nhan_lai = ky_han_thang / so_thang_nhan

# Lãi suất theo kỳ lĩnh lãi
r_ky = (lai_suat_nam / 100) * (so_thang_nhan / 12)

if loai_lai == "Lãi đơn":
    # Lãi đơn: Lãi hàng kỳ tính trên gốc ban đầu
    lai_dinh_ky = so_tien_gui * r_ky
    tong_lai = lai_dinh_ky * so_lan_nhan_lai
    tong_tien = so_tien_gui + tong_lai

else:  # Lãi kép
    if hinh_thuc_nhan == "Cuối kỳ":
        # Nhận lãi cuối kỳ thì không nhập gốc định kỳ, lãi kép tính tròn theo số tháng
        tong_tien = so_tien_gui * ((1 + (lai_suat_nam / 100) / 12) ** ky_han_thang)
        tong_lai = tong_tien - so_tien_gui
        lai_dinh_ky = tong_lai  # Nhận một lần ở cuối kỳ
    else:
        # Lãi kép định kỳ (Lãi nhập gốc)
        tong_tien = so_tien_gui * ((1 + r_ky) ** so_lan_nhan_lai)
        tong_lai = tong_tien - so_tien_gui
        # Lãi kỳ đầu tiên làm mốc tham khảo
        lai_dinh_ky = so_tien_gui * r_ky

# --- HIỂN THỊ KẾT QUẢ ---
st.markdown("---")
st.subheader("📊 Kết quả tính toán")

# 3 Ô chỉ số chính
col_res1, col_res2, col_res3 = st.columns(3)

with col_res1:
    if loai_lai == "Lãi kép" and hinh_thuc_nhan != "Cuối kỳ":
        st.metric(
            label="Lãi kỳ đầu tiên",
            value=f"{lai_dinh_ky:,.0f} VNĐ",
            help="Do có lãi kép nhập gốc nên tiền lãi các kỳ sau sẽ tăng dần."
        )
    else:
        st.metric(
            label=f"Tiền lãi ({hinh_thuc_nhan.lower()})",
            value=f"{lai_dinh_ky:,.0f} VNĐ"
        )

with col_res2:
    st.metric(
        label="Tổng tiền lãi nhận được",
        value=f"{tong_lai:,.0f} VNĐ"
    )

with col_res3:
    st.metric(
        label="Tổng gốc + lãi cuối kỳ",
        value=f"{tong_tien:,.0f} VNĐ"
    )

# Ghi chú tổng hợp
st.info(
    f"💡 Với số tiền **{so_tien_gui:,.0f} VNĐ**, gửi trong **{ky_han_thang} tháng** với lãi suất **{lai_suat_nam}%/năm** "
    f"({loai_lai.lower()}, nhận lãi {hinh_thuc_nhan.lower()}), tổng số tiền nhận được khi đáo hạn là **{tong_tien:,.0f} VNĐ**."
)
