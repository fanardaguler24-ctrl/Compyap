import streamlit as st
import os

st.set_page_config(page_title="EAGLE22 AI", layout="centered")

st.markdown("<h3 style='text-align: center; color: #f1c40f;'>EAGLE22 STUDIO</h3>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #2ecc71;'>AI COMP MAKER</h1>", unsafe_allow_html=True)

# Girdi Alanları
video_file = st.file_uploader("🎬 Videoyu Seç", type=['mp4', 'mov'])
player_img = st.file_uploader("📸 Oyuncu Fotoğrafı Seç", type=['jpg', 'png', 'jpeg'])
turbo = st.number_input("⚡ Turbo Hızı:", 1, 20, 10)

if st.button("✂️ COMP OLUŞTUR"):
    if video_file and player_img:
        st.write("✅ Sistem Hazır! Analiz Başlıyor...")
        # Burada işlem yapılacak
    else:
        st.error("Lütfen video ve fotoğrafı eksiksiz yükle!")
