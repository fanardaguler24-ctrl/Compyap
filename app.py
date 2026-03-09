import streamlit as st
import cv2
import numpy as np
import os

# Sayfa Ayarı
st.set_page_config(page_title="AI Comp Maker", page_icon="✂️")

# CSS ile Arayüzü Fotoğraftakine Benzettim
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h3 { color: #f1c40f; text-align: center; margin-bottom: 0px; }
    h1 { color: #2ecc71; text-align: center; margin-top: 0px; }
    .stButton>button {
        background-color: #ff0050;
        color: white;
        border-radius: 5px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("### ZMK STUDIO")
st.markdown("<h1>AI COMP MAKER</h1>", unsafe_allow_html=True)

# 1. Bölüm: Video Seçimi
st.markdown("#### 🎬 1. İşlenecek Videoyu Seç")
video_file = st.file_uploader("", type=['mp4', 'mov'], key="video")

# 2. Bölüm: Oyuncu Seçimi
st.markdown("#### 📸 2. Hedef Oyuncu/Kişi Fotoğrafı Seç")
player_img = st.file_uploader("", type=['jpg', 'png', 'jpeg'], key="player")

# 3. Bölüm: Turbo Hızı
turbo = st.number_input("⚡ Turbo Hızı (Kat):", min_value=1, max_value=10, value=3)

# Oluştur Butonu
if st.button("✂️ COMP OLUŞTUR"):
    if video_file and player_img:
        st.info("Analiz başlatılıyor... Oyuncu videoda taranıyor.")
        # Buraya video işleme fonksiyonu gelecek
    else:
        st.error("Lütfen önce video ve oyuncu fotoğrafını yükle!")
