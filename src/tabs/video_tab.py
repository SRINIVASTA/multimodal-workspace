import streamlit as st
import os

def render_video_tab():
    st.subheader("🎬 Multi-Agent Asynchronous Video Generation Pipeline")
    
    from src.core.pipeline import VideoCompilationWorker
    
    # Dynamic Video Generation Foundations Model Matrix
    video_model = st.selectbox(
        "Select Dynamic Video Foundation:",
        [
            "google/veo",
            "minimax/video",
            "luma/ray"
        ],
        key="video_dynamic_model_selector"
    )
    
    # FOLDED CODE CONFIGURATIONS: Parameter asset overrides
    with st.expander("⚙️ View Folded Render Pipeline Overrides"):
        aspect_ratio = st.radio(
            "Target Aspect Ratio Profile:", 
            ["16:9 Landscape (Report Banner)", "9:16 Vertical (SaaS Ad)", "1:1 Square"], 
            horizontal=True,
            key="video_tab_aspect_ratio"
        )
        frame_rate = st.slider("Target Synthesis Framerate (FPS):", min_value=24, max_value=60, value=30, key="video_tab_fps")
        st.caption(f"🔧 Configuration Pipeline Bound: Rendering at {frame_rate} FPS using a {aspect_ratio} grid.")

    task_key = "commercial_render_prod"
    status_data = VideoCompilationWorker.get_task_status(task_key)
    
    col_ctrl, col_screen = st.columns(2)
    with col_ctrl:
        st.write("#### Operations Console Log")
        st.info(f"Target Active Foundation Vector Engine: {video_model}")
        
        if status_data["status"] == "NOT_FOUND":
            if st.button("Launch Asynchronous Media Render Workflow", use_container_width=True):
                # Generates temporary pipeline target files cleanly
                VideoCompilationWorker.start_async_compilation(
                    task_id=task_key,
                    video_path="temp_broll.mp4",
                    audio_path="temp_voiceover.mp3",
                    output_path="generated_commercial.mp4"
                )
                st.rerun()
        else:
            if st.button("Reset Pipeline Track Status Window", use_container_width=True):
                # Flushes background task statuses out of shared thread memory
                VideoCompilationWorker.clear_task(task_key)
                st.rerun()
                
    with col_screen:
        st.write("#### Core Processing Output Screen")
        if status_data["status"] == "NOT_FOUND":
            st.info("Awaiting video worker orchestration initialization execution paths...")
        elif status_data["status"] == "PROCESSING":
            st.warning(f"⏳ Background Thread Rendering Active: Processing layout frames at {status_data['progress']}%...")
            st.progress(status_data["progress"] / 100)
        elif status_data["status"] == "SUCCESS":
            st.success("🎉 Background execution worker pipeline finished compiling media assets successfully!")
            
            # Safe physical validation check on the written file
            if os.path.exists(status_data["file"]):
                st.video(status_data["file"])
            else:
                st.error("Worker pipeline reported success, but target video sequence asset was dropped from workspace disk.")
        elif status_data["status"] == "FAILED":
            st.error(f"❌ Render Engine Pipeline Failure: {status_data['error']}")
