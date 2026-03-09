import streamlit as st
import time

st.set_page_config(page_title="AI Comp Maker", layout="centered")

# Tasarım
st.markdown("<h3 style='text-align: center; color: #f1c40f;'>ZMK STUDIO</h3>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #2ecc71;'>AI COMP MAKER</h1>", unsafe_allow_html=True)

video_file = st.file_uploader("🎬 1. Videoyu Seç", type=['mp4', 'mov'])
player_img = st.file_uploader("📸 2. Oyuncu Fotoğrafı Seç", type=['jpg', 'png', 'jpeg'])
turbo = st.slider("⚡ Turbo Hızı:", 1, 50, 10)

if st.button("✂️ COMP OLUŞTUR", use_container_width=True):
    if video_file and player_img:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Analiz Taklidi (Şu an hızlıca dolacak)
        for i in range(100):
            time.sleep(0.05) 
            progress_bar.progress(i + 1)
            status_text.text(f"Analiz ediliyor: %{i+1}")
            
        st.success("✅ Video Başarıyla Oluşturuldu!")
        
        # --- GERÇEK İNDİRME BUTONU BURASI ---
        # Video dosyasını sunucudan senin cihazına indirmeyi sağlar
        with open(video_file.name, "wb") as f:
            f.write(video_file.getbuffer()) # Örnek olarak yüklediğin videoyu hazırlıyor
            
        st.download_button(
            label="📥 VİDEOYU CİHAZINA İNDİR",
            data=video_file,
            file_name="hazir_comp.mp4",
            mime="video/mp4",
            use_container_width=True
        )
    else:
        st.error("Lütfen önce dosyaları yükle!")
