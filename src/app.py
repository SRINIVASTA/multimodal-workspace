import sys
import os

# Dynamically inject the root repository path into Python's search matrix
# This prevents the ModuleNotFoundError on Streamlit Cloud deployment architectures
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.config import settings
from src.core.state import SessionStateManager
from src.core.pipeline import VideoCompilationWorker

st.set_page_config(page_title="Enterprise Multi-Modal AI Engine", layout="wide")
SessionStateManager.initialize()

st.title("⚙️ Enterprise Multi-Modal Studio")

def initialize_core_services():
    """Initializes core engine client handlers dynamically on each run loop."""
    from src.api.client import OpenRouterClient
    from src.api.text_service import TextService
    from src.api.media_service import MediaService
    
    core_client = OpenRouterClient()
    return {
        "text": TextService(core_client),
        "media": MediaService(core_client)
    }

# Read fresh live service instances straight from disk
services = initialize_core_services()

if not settings.OPENROUTER_API_KEY:
    st.error("Authentication Error: OPENROUTER_API_KEY missing from secrets configurations.")
    st.stop()

tab_doc, tab_media = st.tabs(["🏛️ Advanced Document Engine", "🎬 Creative Asset Studio"])

with tab_doc:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Deep Research Input")
        
        text_model = st.selectbox(
            "Select Text AI Engine:",
            [
                "meta-llama/llama-3-8b-instruct:free",
                "google/gemini-2.5-flash",
                "openai/gpt-4o-mini"
            ],
            index=2
        )
        
        topic = st.text_input("Target Analysis Topic:")
        if st.button("Query Web Engine"):
            with st.spinner("Executing real-time technical web crawl analysis..."):
                try:
                    st.session_state.document_draft = services["text"].generate_document(topic, model=text_model)
                    st.rerun()
                except Exception as e:
                    st.error("❌ OpenRouter Request Rejected:")
                    st.info(str(e))
            
    with col_r:
        st.subheader("Live Document Matrix")
        st.session_state.document_draft = st.text_area("Workspace Editor", value=st.session_state.document_draft, height=350)
        
        # 📥 ENTERPRISE EXPORT PIPELINE
        st.write("---")
        col_down_md, col_down_pdf = st.columns(2)
        
        with col_down_md:
            st.download_button(
                label="📥 Export Document as Markdown (.md)",
                data=st.session_state.document_draft,
                file_name="generated_report.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        with col_down_pdf:
            if st.button("📄 Compile Document to PDF (.pdf)", use_container_width=True):
                with st.spinner("Compiling layout frames using ReportLab..."):
                    try:
                        from reportlab.lib.pagesizes import letter
                        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                        
                        pdf_path = "generated_report.pdf"
                        doc = SimpleDocTemplate(pdf_path, pagesize=letter, title="AI Studio Export")
                        story = []
                        styles = getSampleStyleSheet()
                        
                        body_style = ParagraphStyle(
                            'PDFBody',
                            parent=styles['Normal'],
                            fontSize=10,
                            leading=14,
                            spaceAfter=8
                        )
                        
                        for line in st.session_state.document_draft.split('\n'):
                            clean_line = line.strip()
                            if not clean_line:
                                story.append(Spacer(1, 10))
                                continue
                            
                            clean_line = clean_line.replace("#", "").replace("**", "").replace("*", "")
                            story.append(Paragraph(clean_line, body_style))
                        
                        story.append(Spacer(1, 20))
                        disclaimer_style = ParagraphStyle('Disclaimer', parent=body_style, fontSize=8, leading=10)
                        story.append(Paragraph("<i>This is for informational purposes only. For medical advice or diagnosis, consult a professional. AI responses may include mistakes.</i>", disclaimer_style))
                        
                        doc.build(story)
                        
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(
                                label="🚀 Download Ready PDF File",
                                data=pdf_file.read(),
                                file_name="ai_studio_report.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        st.success("PDF ready for download!")
                    except Exception as pdf_err:
                        st.error(f"PDF Compiler Error: {str(pdf_err)}")

# 2. FIXED LAYER: We draw the structure inside Tab 2 explicitly to guarantee visibility
with tab_media:
    col_img, col_aud = st.columns(2)
    
    with col_img:
        st.subheader("Image Engine Core")
        img_model = st.selectbox("Engine Selector:", ["black-forest-labs/flux-1-schnell", "openai/dall-e-3"])
        img_prompt = st.text_area("Graphic Specifications Layout Prompt:")
        
        col_img_btn1, col_img_btn2 = st.columns(2)
        with col_img_btn1:
            render_clicked = st.button("Render Canvas Asset", use_container_width=True)
        with col_img_btn2:
            feed_clicked = st.button("🔗 Inject Image to Canvas", use_container_width=True)
            
        if render_clicked or feed_clicked:
            with st.spinner("Generating creative assets..."):
                try:
                    url = services["media"].generate_image(img_prompt, img_model)
                    st.image(url, caption="Generated Asset Frame")
                    if feed_clicked:
                        st.session_state.document_draft += f"\n\n![Generated Marketing Graphic]({url})\n"
                        st.success("Asset injected! Refresh tab 1 to view line items.")
                except Exception as e:
                    st.error(f"❌ Image Engine Request Failed: {str(e)}")

    with col_aud:
        st.subheader("Audio Synthesis & Video Production")
        st.write("#### 🎵 AssemblyAI Text-To-Speech Interface")
        
        if st.button("🗣️ Read Document Aloud Automatically", use_container_width=True):
            with st.spinner("Synthesizing narration from Document Canvas text..."):
                try:
                    narration_text = st.session_state.document_draft[:2000]
                    audio_bytes = services["media"].text_to_speech(narration_text, model="assemblyai/tts-1")
                    st.audio(audio_bytes, format="audio/mp3")
                    st.success("Audio stream successfully compiled!")
                except Exception as audio_err:
                    st.error(f"TTS Connection Exception: {str(audio_err)}")
        
        st.write("---")
        st.write("#### 🎬 Asynchronous Video Production Pipeline")
        st.info("Compile synthetic commercial structures inside decoupled background tasks.")
        
        # Isolated runtime check inside a safe block for background threading tracking
        task_key = "commercial_render_prod"
        status_data = VideoCompilationWorker.get_task_status(task_key)
        
        if status_data["status"] == "NOT_FOUND":
            if st.button("Launch Asynchronous Media Render Workflow", use_container_width=True):
                # Ensure placeholder streams are present on server
                with open("temp_broll.mp4", "wb") as f: f.write(b"Placeholder Video Stream")
                with open("temp_voiceover.mp3", "wb") as f: f.write(b"Placeholder Audio Stream")
                
                VideoCompilationWorker.start_async_compilation(
                    task_id=task_key,
                    video_path="temp_broll.mp4",
                    audio_path="temp_voiceover.mp3",
                    output_path="generated_commercial.mp4"
                )
                st.rerun()
                
        elif status_data["status"] == "PROCESSING":
            st.warning("⏳ Background Thread Rendering active...")
            
        elif status_data["status"] == "SUCCESS":
            st.success("🎉 Background worker pipeline finished compiling media assets!")
            st.video(status_data["file"])
            if st.button("Reset Compilation Window", use_container_width=True):
                VideoCompilationWorker._tasks.pop(task_key, None)
                st.rerun()
                
        elif status_data["status"] == "FAILED":
            st.error(f"Engine Compilation Error: {status_data['error']}")
            if st.button("Retry Thread Operations", use_container_width=True):
                VideoCompilationWorker._tasks.pop(task_key, None)
                st.rerun()
