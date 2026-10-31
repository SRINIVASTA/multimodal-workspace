import streamlit as st

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
    
    task_key = "commercial_render_prod"
    status_data = VideoCompilationWorker.get_task_status(task_key)
    
    col_ctrl, col_screen = st.columns(2)
    with col_ctrl:
        st.write("#### Operations Console Log")
        st.info(f"Target Active Foundation Vector Engine: {video_model}")
        
        if status_data["status"] == "NOT_FOUND":
            if st.button("Launch Asynchronous Media Render Workflow", use_container_width=True):
                VideoCompilationWorker.start_async_compilation(
                    task_id=task_key,
                    video_path="temp_broll.mp4",
                    audio_path="temp_voiceover.mp3",
                    output_path="generated_commercial.mp4"
                )
                st.rerun()
        else:
            if st.button("Reset Pipeline Track Status Window", use_container_width=True):
                VideoCompilationWorker._tasks.pop(task_key, None)
                st.rerun()
                
    with col_screen:
        st.write("#### Core Processing Output Screen")
        if status_data["status"] == "NOT_FOUND":
            st.info("Awaiting video worker orchestration initialization execution paths...")
        elif status_data["status"] == "PROCESSING":
            st.warning(f"⏳ Background Thread Rendering active: Processing layout frames at {status_data['progress']}%...")
            st.progress(status_data["progress"] / 100)
        elif status_data["status"] == "SUCCESS":
            st.success("🎉 Background execution worker pipeline finished compiling media assets successfully!")
            st.video(status_data["file"])
