import streamlit as st
import plotly.express as px
from src.config import settings
from src.api.client import OpenRouterClient
from src.api.text_service import TextService
from src.api.media_service import MediaService
from src.core.state import SessionStateManager
from src.core.pipeline import VideoCompilationWorker

# Initialize system resources
st.set_page_config(page_title="Enterprise Multi-Modal AI Engine", layout="wide")
SessionStateManager.initialize()

client = OpenRouterClient()
text_service = TextService(client)
media_service = MediaService(client)

st.title("⚙️ Enterprise Multi-Modal Studio")
settings.OPENROUTER_API_KEY = st.sidebar.text_input("OpenRouter Key", type="password", value=settings.OPENROUTER_API_KEY)

if not settings.OPENROUTER_API_KEY:
    st.warning("Please supply an active OpenRouter credential structure inside the configuration pane.")
    st.stop()

# Layout structural tabs
tab_doc, tab_media = st.tabs(["🏛️ Advanced Document Engine", "🎬 Creative Asset Studio"])

with tab_doc:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Deep Research Input")
        topic = st.text_input("Target Analysis Topic:")
        if st.button("Query Web Engine"):
            st.session_state.document_draft = text_service.generate_document(topic)
            st.rerun()

        st.subheader("Block Modifications")
        block_input = st.text_area("Target Section Segment:")
        action = st.selectbox("Transformation Type:", ["Shorten", "Translate to Spanish", "Professional Tone"])
        if st.button("Execute Paragraph Layer Update"):
            updated = text_service.selective_edit(block_input, action)
            st.code(updated, language="markdown")
            
    with col_r:
        st.subheader("Live Document Matrix")
        st.session_state.document_draft = st.text_area("Workspace Editor", value=st.session_state.document_draft, height=350)

with tab_media:
    col_img, col_aud = st.columns(2)
    with col_img:
        st.subheader("Image Engine Core")
        img_model = st.selectbox("Engine Selector:", ["black-forest-labs/flux-1-schnell", "openai/dall-e-3"])
        img_prompt = st.text_area("Graphic Specifications Layout Prompt:")
        if st.button("Render Canvas Asset"):
            url = media_service.generate_image(img_prompt, img_model)
            st.image(url)
