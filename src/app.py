import sys
import os

# Dynamically inject the root repository path into Python's search matrix
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.config import settings
from src.core.state import SessionStateManager
from src.tabs.text_tab import render_text_tab
from src.tabs.image_tab import render_image_tab
from src.tabs.audio_tab import render_audio_tab
from src.tabs.video_tab import render_video_tab

st.set_page_config(page_title="Enterprise Multi-Modal AI Studio", layout="wide")
SessionStateManager.initialize()

st.title("⚙️ Enterprise Multi-Modal Studio")

if not settings.OPENROUTER_API_KEY:
    st.error("Authentication Error: OPENROUTER_API_KEY missing from secrets configurations.")
    st.stop()

# Modular Tab Splitting Infrastructure
tab_text, tab_image, tab_audio, tab_video = st.tabs([
    "📝 1. Document Engine", 
    "🎨 2. Image Studio", 
    "🎵 3. Voice Synthesis", 
    "🎬 4. Video Pipeline"
])

with tab_text:
    render_text_tab()

with tab_image:
    render_image_tab()

with tab_audio:
    render_audio_tab()

with tab_video:
    render_video_tab()
