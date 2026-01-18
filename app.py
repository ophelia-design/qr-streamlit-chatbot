import streamlit as st
import pandas as pd
import os
import qrcode
from io import BytesIO

DATA_FILE = "data.csv"

# =========================
# Utility Functions
# =========================
def generate_user_id():
    if not os.path.exists(DATA_FILE):
        return "USR0001"
    df = pd.read_csv(DATA_FILE)
    return f"USR{len(df)+1:04d}"

def save_data(data):
    df_new = pd.DataFrame([data])
    header = not os.path.exists(DATA_FILE)
    df_new.to_csv(DATA_FILE, mode="a", header=header, index=False)

def get_user(uid):
    if not os.path.exists(DATA_FILE):
        return None
    df = pd.read_csv(DATA_FILE)
    row = df[df["User_ID"] == uid]
    return row.iloc[0] if not row.empty else None

def generate_qr_image(url):
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return buf

# =========================
# MODE 1: QR SCAN (DETAIL)
# =========================
query = st.query_params
if "uid" in query:
    uid = query["uid"]
    data = get_user(uid)

    st.title("📄 Detail Data Pengguna")

    if data is not None:
        st.table(data.to_frame(name="Nilai"))
    else:
        st.error("❌ Data tidak ditemukan")

    st.stop()

# =========================
# MODE 2: INPUT DATA
# =========================
st.title("🤖 Rule-Based Chatbot Input Data")

user_id = generate_user_id()
st.info(f"User_ID otomatis: {user_id}")

with st.form("form_input"):
    nama = st.text_input("Nama")
    usia = st.number_input("Usia", 0, 120)
    pekerjaan = st.text_input("Pekerjaan")
    submit = st.form_submit_button("Simpan Data")

if submit:
    data = {
        "User_ID": user_id,
        "Nama": nama,
        "Usia": usia,
        "Pekerjaan": pekerjaan
    }

    save_data(data)

    base_url = st.get_option("server.baseUrlPath") or ""
    app_url = st.runtime.get_instance()._session_mgr._runtime._server._address

    full_url = f"https://{app_url}/?uid={user_id}"

    st.success("✅ Data berhasil disimpan")

    qr_img = generate_qr_image(full_url)
    st.image(qr_img, caption="Scan QR untuk melihat detail data")

    if st.button("➕ Tambah Data Lagi"):
        st.experimental_rerun()
