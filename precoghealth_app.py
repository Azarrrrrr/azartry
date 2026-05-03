import streamlit as st
import numpy as np

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="PrecogHealth",
    page_icon="🧬",
    layout="centered"
)

# ── Simple rule-based model (sebelum pakai ML beneran) ───────
def calculate_risk(data):
    """
    Hitung skor risiko sederhana berdasarkan faktor input.
    Nanti bisa diganti dengan model scikit-learn sungguhan.
    """
    scores = {"Stroke": 0, "Diabetes": 0, "Hipertensi": 0}

    age = data["age"]
    bmi = data["bmi"]

    # --- Stroke ---
    if age > 50: scores["Stroke"] += 25
    elif age > 35: scores["Stroke"] += 10
    if data["smoking"]: scores["Stroke"] += 20
    if data["hypertension_history"]: scores["Stroke"] += 25
    if data["heart_disease_history"]: scores["Stroke"] += 20
    if data["family_stroke"]: scores["Stroke"] += 15
    if data["exercise"] == "Tidak pernah": scores["Stroke"] += 10
    if bmi > 30: scores["Stroke"] += 10

    # --- Diabetes ---
    if bmi > 30: scores["Diabetes"] += 25
    elif bmi > 25: scores["Diabetes"] += 10
    if data["family_diabetes"]: scores["Diabetes"] += 30
    if data["sweet_drink"] >= 3: scores["Diabetes"] += 20
    elif data["sweet_drink"] >= 1: scores["Diabetes"] += 10
    if data["exercise"] == "Tidak pernah": scores["Diabetes"] += 15
    if age > 40: scores["Diabetes"] += 10
    if data["diabetes_history"]: scores["Diabetes"] += 20

    # --- Hipertensi ---
    if data["smoking"]: scores["Hipertensi"] += 20
    if data["coffee"] >= 4: scores["Hipertensi"] += 20
    elif data["coffee"] >= 2: scores["Hipertensi"] += 10
    if data["stress"] in ["Tinggi", "Sangat tinggi"]: scores["Hipertensi"] += 20
    if data["family_hypertension"]: scores["Hipertensi"] += 25
    if bmi > 30: scores["Hipertensi"] += 15
    if data["exercise"] == "Tidak pernah": scores["Hipertensi"] += 10
    if age > 45: scores["Hipertensi"] += 10

    # Clamp 0–100
    for k in scores:
        scores[k] = min(scores[k], 100)

    return scores

def risk_label(pct):
    if pct >= 70: return "🔴 Tinggi", "#ef4444"
    elif pct >= 40: return "🟡 Sedang", "#f59e0b"
    else: return "🟢 Rendah", "#22c55e"

# ── UI ───────────────────────────────────────────────────────
st.title("🧬 PrecogHealth")
st.caption("Prediksi risiko penyakit tidak menular berdasarkan kebiasaan & riwayat kesehatan kamu.")
st.divider()

# ── FORM INPUT ───────────────────────────────────────────────
with st.form("health_form"):

    st.subheader("👤 Data Pribadi")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Umur", min_value=10, max_value=100, value=22)
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    with col2:
        weight = st.number_input("Berat Badan (kg)", min_value=30, max_value=200, value=65)
        height = st.number_input("Tinggi Badan (cm)", min_value=100, max_value=250, value=170)

    bmi = weight / ((height / 100) ** 2)
    st.caption(f"BMI kamu: **{bmi:.1f}**")

    st.divider()
    st.subheader("🚬 Kebiasaan Sehari-hari")

    col3, col4 = st.columns(2)
    with col3:
        smoking = st.checkbox("Merokok")
        coffee = st.slider("Kopi per hari (gelas)", 0, 10, 1)
        sweet_drink = st.slider("Minuman manis per hari (gelas)", 0, 10, 1)
    with col4:
        exercise = st.selectbox("Olahraga", ["Tidak pernah", "1–2x seminggu", "3–4x seminggu", "Setiap hari"])
        stress = st.selectbox("Tingkat stres", ["Rendah", "Sedang", "Tinggi", "Sangat tinggi"])
        sleep = st.slider("Jam tidur per malam", 3, 12, 7)

    st.divider()
    st.subheader("🏥 Riwayat Penyakit Pribadi")
    col5, col6 = st.columns(2)
    with col5:
        hypertension_history = st.checkbox("Pernah didiagnosa Hipertensi")
        diabetes_history = st.checkbox("Pernah didiagnosa Diabetes")
    with col6:
        heart_disease_history = st.checkbox("Pernah didiagnosa Penyakit Jantung")

    st.divider()
    st.subheader("👨‍👩‍👧 Riwayat Penyakit Keluarga")
    col7, col8, col9 = st.columns(3)
    with col7:
        family_stroke = st.checkbox("Stroke")
    with col8:
        family_diabetes = st.checkbox("Diabetes")
    with col9:
        family_hypertension = st.checkbox("Hipertensi")

    st.divider()
    submitted = st.form_submit_button("🔍 Analisis Risiko Saya", use_container_width=True)

# ── HASIL ────────────────────────────────────────────────────
if submitted:
    data = {
        "age": age, "bmi": bmi, "smoking": smoking,
        "coffee": coffee, "sweet_drink": sweet_drink,
        "exercise": exercise, "stress": stress, "sleep": sleep,
        "hypertension_history": hypertension_history,
        "diabetes_history": diabetes_history,
        "heart_disease_history": heart_disease_history,
        "family_stroke": family_stroke,
        "family_diabetes": family_diabetes,
        "family_hypertension": family_hypertension,
    }

    scores = calculate_risk(data)

    st.divider()
    st.subheader("📊 Hasil Prediksi Risiko")
    st.caption("Hasil ini bukan diagnosis medis. Selalu konsultasikan ke dokter untuk pemeriksaan lebih lanjut.")

    for disease, pct in scores.items():
        label, color = risk_label(pct)
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown(f"**{disease}**")
            st.progress(pct / 100)
        with col_b:
            st.markdown(f"<span style='color:{color}; font-size:14px'>{label}<br><b>{pct}%</b></span>", unsafe_allow_html=True)
        st.write("")

    # Rekomendasi
    st.divider()
    st.subheader("💡 Rekomendasi")

    tips = []
    if smoking:
        tips.append("🚭 Berhenti merokok bisa menurunkan risiko stroke dan hipertensi secara signifikan.")
    if coffee >= 4:
        tips.append("☕ Kurangi konsumsi kopi — lebih dari 3 gelas/hari meningkatkan tekanan darah.")
    if sweet_drink >= 2:
        tips.append("🧃 Kurangi minuman manis untuk menurunkan risiko diabetes.")
    if exercise == "Tidak pernah":
        tips.append("🏃 Mulai olahraga ringan 30 menit, 3x seminggu — efeknya besar untuk semua risiko.")
    if bmi > 25:
        tips.append(f"⚖️ BMI kamu {bmi:.1f} — menurunkan berat badan bisa mengurangi semua risiko sekaligus.")
    if stress in ["Tinggi", "Sangat tinggi"]:
        tips.append("🧘 Kelola stres dengan meditasi, olahraga, atau istirahat cukup.")
    if sleep < 6:
        tips.append("😴 Tidur kurang dari 6 jam meningkatkan risiko hipertensi dan diabetes.")
    if not tips:
        tips.append("✅ Kebiasaanmu sudah cukup baik! Pertahankan dan lakukan cek kesehatan rutin.")

    for tip in tips:
        st.info(tip)

    st.divider()
    st.caption("⚠️ PrecogHealth adalah prototipe eksperimental. Hasil prediksi menggunakan model berbasis aturan sederhana, bukan model machine learning terlatih. Jangan jadikan ini sebagai acuan medis.")
