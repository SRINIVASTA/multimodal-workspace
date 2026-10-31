import streamlit as st

def render_audio_tab():
    st.subheader("🎵 Hyper-Realistic Voice Synthesis Engine")
    
    from src.api.client import OpenRouterClient
    from src.api.media_service import MediaService
    
    client = OpenRouterClient()
    media_service = MediaService(client)
    
    # Dynamic Voice Engine Selection Matrix
    audio_model = st.selectbox(
        "Select Dynamic Speech/Voice Engine:",
        [
            "assemblyai/tts-1",
            "openai/tts-1-hd",
            "elevenlabs/rachel"
        ],
        key="audio_dynamic_model_selector"
    )
    
    audio_source = st.radio("Select Target Audio Source:", ["Pull from Tab 1 Document Matrix", "Write Custom Isolated Script"], horizontal=True)
    
    if audio_source == "Pull from Tab 1 Document Matrix":
        audio_text = st.session_state.document_draft
        st.caption("🔒 Connected to live context editor frame inside Tab 1.")
    else:
        audio_text = st.text_area("Isolated Script Panel Input:", value="Welcome to the modular enterprise audio deployment suite.", height=150)
        
    if st.button("🗣️ Synthesize Speech Output Stream", use_container_width=True):
        with st.spinner("Compiling high-fidelity clean stream tracks..."):
            try:
                audio_bytes = media_service.text_to_speech(audio_text[:2000], model=audio_model)
                st.audio(audio_bytes, format="audio/mp3")
                st.success("Clean high-fidelity audio narration generated!")
            except Exception as e:
                st.error(f"Audio API Disconnect: {str(e)}")
