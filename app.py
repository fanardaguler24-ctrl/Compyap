import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from moviepy import VideoFileClip, concatenate_videoclips

st.set_page_config(page_title="EAGLE22 AI Comp Maker", layout="centered")

# Arayüz Tasarımı
st.markdown("<h3 style='text-align: center; color: #f1c40f;'>ZMK STUDIO</h3>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #2ecc71;'>AI COMP MAKER</h1>", unsafe_allow_html=True)

# Girdi Alanları
video_file = st.file_uploader("🎬 1. İşlenecek Videoyu Seç", type=['mp4', 'mov'])
player_img = st.file_uploader("📸 2. Hedef Oyuncu Fotoğrafı Seç", type=['jpg', 'png', 'jpeg'])
turbo = st.slider("⚡ Turbo Hızı (Atlama):", 1, 50, 10)

if st.button("✂️ COMP OLUŞTUR", use_container_width=True):
    if video_file and player_img:
        # Geçici dosya oluşturma
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
            tfile.write(video_file.read())
            video_path = tfile.name
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        st.info(f"Analiz başlıyor... Toplam {total_frames} kare taranıyor.")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        found_segments = []
        start_frame = None
        
        # Yüz tespiti için OpenCV sınıflandırıcısı
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Analiz Döngüsü
        for i in range(0, total_frames, turbo):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret: break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR_GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                if start_frame is None: start_frame = i
            else:
                if start_frame is not None:
                    # Sahneyi kaydet (En az 1 saniyelik sahneler)
                    if (i - start_frame) / fps > 0.5:
                        found_segments.append((start_frame / fps, i / fps))
                    start_frame = None
            
            # İlerleme güncelleme
            prog = min(i / total_frames, 1.0)
            progress_bar.progress(prog)
            status_text.text(f"Analiz ediliyor: %{int(prog*100)}")

        cap.release()
        
        if found_segments:
            st.success(f"✅ {len(found_segments)} sahne bulundu! Video birleştiriliyor...")
            try:
                full_video = VideoFileClip(video_path)
                clips = [full_video.subclipped(s, e) for s, e in found_segments[:15]] # İlk 15 sahne
                final_clip = concatenate_videoclips(clips)
                output_path = "result_comp.mp4"
                final_clip.write_videofile(output_path, codec="libx264", audio=True)
                
                with open(output_path, "rb") as f:
                    st.download_button("📥 HAZIR COMP'U İNDİR", f, "ai_comp_eagle22.mp4", "video/mp4", use_container_width=True)
                
                full_video.close()
            except Exception as e:
                st.error(f"Video birleştirme hatası: {e}")
        else:
            st.error("Oyuncunun yüzü videoda tespit edilemedi. Lütfen daha net bir video veya düşük Turbo hızı deneyin.")
        
        # Temizlik
        if os.path.exists(video_path): os.remove(video_path)
    else:
        st.error("Lütfen video ve fotoğrafı yükleyin!")
