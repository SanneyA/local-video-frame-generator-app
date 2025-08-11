import os
import cv2
import streamlit as st
import tempfile

# ========= Extract frames =========
def extract_frames(video_path, output_folder="frames", frame_skip=1):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        st.error("❌ Error: Cannot open video file.")
        return []

    frame_count = 0
    saved_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    progress = st.progress(0)

    while True:
        success, frame = cap.read()
        if not success:
            break

        if frame_count % frame_skip == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1

        frame_count += 1
        progress.progress(min(1.0, frame_count / total_frames))

    cap.release()
    st.success(f"✅ Done! {saved_count} frames saved in '{output_folder}'.")
    return [os.path.join(output_folder, f) for f in sorted(os.listdir(output_folder)) if f.endswith(".jpg")]

# ========= Streamlit UI =========
st.set_page_config(page_title="🎥 Local Video Frame Extractor", layout="centered")
st.title("🎥 Local Video Frame Extractor & Downloader")

video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])
frame_skip = st.number_input("📸 Frame skip (1 = every frame, 2 = every other...)", min_value=1, value=1)

if video_file is not None:
    # Save uploaded video to a temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_video_path = os.path.join(tmpdir, video_file.name)
        with open(temp_video_path, "wb") as f:
            f.write(video_file.read())

        st.video(temp_video_path)

        if st.button("🚀 Extract Frames"):
            frames_output_folder = os.path.join(tmpdir, "extracted_frames")
            frames = extract_frames(temp_video_path, output_folder=frames_output_folder, frame_skip=frame_skip)

            if frames:
                st.write("### 🖼️ Sample Extracted Frames:")
                for frame_file in frames[:5]:
                    st.image(frame_file, width=300)
                    with open(frame_file, "rb") as f:
                        st.download_button(
                            label=f"Download {os.path.basename(frame_file)}",
                            data=f,
                            file_name=os.path.basename(frame_file),
                            mime="image/jpeg"
                        )
