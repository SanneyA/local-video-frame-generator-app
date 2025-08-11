import streamlit as st
import cv2
import os
import tempfile
import zipfile

st.title("🎥 Local Video Frame Extractor & Downloader")

# Upload video file
video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

if video_file is not None:
    # Save uploaded video to a temporary file
    temp_dir = tempfile.mkdtemp()
    temp_video_path = os.path.join(temp_dir, video_file.name)
    with open(temp_video_path, "wb") as f:
        f.write(video_file.read())

    st.video(temp_video_path)
    
    # Button to start extraction
    if st.button("Extract Frames"):
        output_folder = os.path.join(temp_dir, "frames")
        os.makedirs(output_folder, exist_ok=True)
        
        cap = cv2.VideoCapture(temp_video_path)
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            frame_count += 1

        cap.release()
        st.success(f"✅ Extracted {frame_count} frames")
        
        # Create ZIP file of frames
        zip_path = os.path.join(temp_dir, "frames.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for img_name in sorted(os.listdir(output_folder)):
                zipf.write(os.path.join(output_folder, img_name), img_name)

        # Show preview of first few frames
        st.subheader("Preview of Extracted Frames")
        preview_images = sorted(os.listdir(output_folder))[:5]  # show first 5 frames
        for img_name in preview_images:
            st.image(os.path.join(output_folder, img_name), caption=img_name, use_column_width=True)

        # Download ZIP button
        with open(zip_path, "rb") as f:
            st.download_button(
                label="📥 Download All Frames as ZIP",
                data=f,
                file_name="extracted_frames.zip",
                mime="application/zip"
            )
