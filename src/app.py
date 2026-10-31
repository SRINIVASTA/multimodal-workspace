import sys
import os

# Dynamically inject the root repository path into Python's search matrix
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.config import settings
from src.core.state import SessionStateManager
from src.core.pipeline import VideoCompilationWorker

st.set_page_config(page_title="Enterprise Multi-Modal AI Engine", layout="wide")
SessionStateManager.initialize()

st.title("⚙️ Enterprise Multi-Modal Studio")

@st.cache_resource(show_spinner=False)
def initialize_core_services():
    from src.api.client import OpenRouterClient
    from src.api.text_service import TextService
    from src.api.media_service import MediaService
    
    core_client = OpenRouterClient()
    return {
        "text": TextService(core_client),
        "media": MediaService(core_client)
    }

services = initialize_core_services()

if not settings.OPENROUTER_API_KEY:
    st.error("Authentication Error: OPENROUTER_API_KEY missing from secrets configurations.")
    st.stop()

tab_doc, tab_media = st.tabs(["🏛️ Advanced Document Engine", "🎬 Creative Asset Studio"])

with tab_doc:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Deep Research Input")
        topic = st.text_input("Target Analysis Topic:")
        if st.button("Query Web Engine"):
            with st.spinner("Executing real-time technical web crawl analysis..."):
                try:
                    st.session_state.document_draft = services["text"].generate_document(topic)
                    st.rerun()
                except Exception as e:
                    st.error("❌ OpenRouter Request Rejected:")
                    st.info(str(e))
            
    with col_r:
        st.subheader("Live Document Matrix")
        st.session_state.document_draft = st.text_area("Workspace Editor", value=st.session_state.document_draft, height=350)

@st.fragment(run_every=2.0)
def render_media_studio():
    col_img, col_aud = st.columns(2)
    
    with col_img:
        st.subheader("Image Engine Core")
        img_model = st.selectbox("Engine Selector:", ["black-forest-labs/flux-1-schnell", "openai/dall-e-3"])
        img_prompt = st.text_area("Graphic Specifications Layout Prompt:")
        if st.button("Render Canvas Asset"):
            with st.spinner("Generating creative assets..."):
                try:
                    url = services["media"].generate_image(img_prompt, img_model)
                    st.image(url)
                except Exception as e:
                    st.error("❌ Image Request Failed:")
                    st.info(str(e))

    with col_aud:
        st.subheader("Asynchronous Video Production Pipeline")
        st.info("Compile synthetic commercial structures inside decoupled background tasks.")
        
        task_key = "commercial_render_prod"
        status_data = VideoCompilationWorker.get_task_status(task_key)
        
        if status_data["status"] == "NOT_FOUND":
            if st.button("Launch Asynchronous Media Render Workflow"):
                with open("temp_broll.mp4", "wb") as f: f.write(b"Mock Video Data")
                with open("temp_voiceover.mp3", "wb") as f: f.write(b"Mock Audio Data")
                
                VideoCompilationWorker.start_async_compilation(
                    task_id=task_key,
                    video_path="temp_broll.mp4",
                    audio_path="temp_voiceover.mp3",
                    output_path="generated_commercial.mp4"
                )
                st.rerun()
                
        elif status_data["status"] == "PROCESSING":
            st.warning(f"⏳ Background Thread Rendering: Processing Action at {status_data['progress']}%...")
            st.progress(status_data["progress"] / 100)
            
        elif status_data["status"] == "SUCCESS":
            st.success("🎉 Background execution worker pipeline finished compiling media assets successfully!")
            st.video(status_data["file"])
            if st.button("Reset Compilation Window"):
                VideoCompilationWorker._tasks.pop(task_key, None)
                st.rerun()
                
        elif status_data["status"] == "FAILED":
            st.error(f"Engine Compilation Error: {status_data['error']}")
            if st.button("Retry Thread Operations"):
                VideoCompilationWorker._tasks.pop(task_key, None)
                st.rerun()

render_media_studio()
