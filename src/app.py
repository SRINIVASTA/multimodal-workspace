import streamlit as st
from src.config import settings
from src.core.state import SessionStateManager

# 1. APPLICATION LIFECYCLE MANAGEMENT (Executed Immediately)
st.set_page_config(page_title="Enterprise Multi-Modal AI Engine", layout="wide")
SessionStateManager.initialize()

st.title("⚙️ Enterprise Multi-Modal Studio")

# 2. CACHED SERVICE ORCHESTRATION LAYER (Runs once, blocks reload latency)
@st.cache_resource(show_spinner=False)
def initialize_core_services():
    """Initializes and caches heavy API client connections in memory."""
    from src.api.client import OpenRouterClient
    from src.api.text_service import TextService
    from src.api.media_service import MediaService
    
    core_client = OpenRouterClient()
    return {
        "text": TextService(core_client),
        "media": MediaService(core_client)
    }

# Fetch instant cached service resource structures
services = initialize_core_services()

# Validate credential parameters silently without freezing UI layout rendering
if not settings.OPENROUTER_API_KEY:
    st.error("Authentication Error: OPENROUTER_API_KEY missing from system secrets environment configuration.")
    st.stop()

# 3. INTERFACE COMPONENT TABS
tab_doc, tab_media = st.tabs(["🏛️ Advanced Document Engine", "🎬 Creative Asset Studio"])

with tab_doc:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Deep Research Input")
        topic = st.text_input("Target Analysis Topic:")
        if st.button("Query Web Engine"):
            with st.spinner("Executing real-time technical web crawl analysis..."):
                st.session_state.document_draft = services["text"].generate_document(topic)
            st.rerun()

        st.subheader("Block Modifications")
        block_input = st.text_area("Target Section Segment:")
        action = st.selectbox("Transformation Type:", ["Shorten", "Translate to Spanish", "Professional Tone"])
        if st.button("Execute Paragraph Layer Update"):
            with st.spinner("Processing selective block structure rewrite..."):
                updated = services["text"].selective_edit(block_input, action)
            st.code(updated, language="markdown")
            
    with col_r:
        st.subheader("Live Document Matrix")
        st.session_state.document_draft = st.text_area("Workspace Editor", value=st.session_state.document_draft, height=350)

# 4. ISOLATED RUNTIME RUNTIME LAYER USING ST.FRAGMENT
@st.fragment
def render_media_studio():
    """Encapsulates media modules so interactions do not trigger full application reloads."""
    col_img, col_aud = st.columns(2)
    with col_img:
        st.subheader("Image Engine Core")
        img_model = st.selectbox("Engine Selector:", ["black-forest-labs/flux-1-schnell", "openai/dall-e-3"])
        img_prompt = st.text_area("Graphic Specifications Layout Prompt:")
        if st.button("Render Canvas Asset"):
            with st.spinner("Generating creative asset assets..."):
                url = services["media"].generate_image(img_prompt, img_model)
            st.image(url)

    with col_aud:
        st.subheader("Audio Synthesis Hub")
        # Moving heavy visualization imports down to runtime instantiation triggers
        import plotly.express as px
        st.write("Dynamic dashboard analysis visualizations run smoothly isolated here.")

render_media_studio()
