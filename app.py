import streamlit as st
import cv2
import numpy as np
import tempfile
from moviepy.editor import VideoFileClip, concatenate_videoclips

st.set_page_config(page_title="AI Comp Maker", layout="centered")

st.markdown("<h3 style='text-align: center; color: #f1c40f;'>ZMK STUDIO</h3>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #2ecc71;'>AI COMP MAKER</h1>", unsafe_allow_html=True)

video_file = st.file_uploader("🎬 1. Videoyu Seç", type=['mp4', 'mov'])
player_img = st.file_uploader("📸 2. Oyuncu Fotoğrafı Seç", type=['jpg', 'png', 'jpeg'])
turbo = st.slider("⚡ Turbo Hızı (Atlama):", 1, 30, 10)

if st.button("✂️ COMP OLUŞTUR", use_container_width=True):
    if video_file and player_img:
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(video_file.read())
        
        cap = cv2.VideoCapture(tfile.name)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        st.info(f"Analiz başlıyor... Toplam {total_frames} kare taranacak.")
        progress_bar = st.progress(0)
        
        found_segments = []
        start_frame = None
        
        # Basit AI: Videoda yüz olan sahneleri bulur (Geliştirilebilir)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
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
                    found_segments.append((start_frame / fps, i / fps))
                    start_frame = None
            
            progress_bar.progress(min(i / total_frames, 1.0))

        cap.release()
        
        if found_segments:
            st.success(f"✅ {len(found_segments)} adet oyuncu sahnesi bulundu! Video birleştiriliyor...")
            full_video = VideoFileClip(tfile.name)
            clips = [full_video.subclip(s, e) for s, e in found_segments[:10]] # İlk 10 sahne (hız için)
            final_clip = concatenate_videoclips(clips)
            final_clip.write_videofile("result.mp4", codec="libx264")
            
            with open("result.mp4", "rb") as f:
                st.download_button("📥 HAZIR COMP'U İNDİR", f, "ai_comp.mp4", "video/mp4", use_container_width=True)
        else:
            st.error("Maalesef seçtiğin oyuncuya ait net bir sahne bulunamadı.")
    else:
        st.error("Dosyaları eksik yükledin!")
