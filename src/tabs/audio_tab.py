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
    
    # FOLDED CODE PROMPTS: Pre-built modular narration scripts
    with st.expander("💡 View Folded Script Templates"):
        st.write("**Corporate Summary Briefing:**")
        st.code("Good morning team. Welcome to the automated operations performance review. Regional sales metrics indicate strong upward trajectories.", language="text")
        
        st.write("**Developer Core System Technical Log:**")
        st.code("Warning: Asynchronous media rendering pipeline initialized. Monitoring local background thread performance matrices for trace exceptions.", language="text")
        
        st.write("**Creative Commercial Spotlight:**")
        st.code("Introducing the next leap in enterprise cognitive design. Powerful. Seamless. Uncompromisingly scalable.", language="text")

    audio_source = st.radio(
        "Select Target Audio Source:", 
        ["Pull from Tab 1 Document Matrix", "Write Custom Isolated Script"], 
        horizontal=True
    )
    
    if audio_source == "Pull from Tab 1 Document Matrix":
        audio_text = st.session_state.document_draft
        st.caption("🔒 Connected to live context editor frame inside Tab 1.")
    else:
        audio_text = st.text_area(
            "Isolated Script Panel Input:", 
            value="Welcome to the modular enterprise audio deployment suite.", 
            height=150,
            key="audio_tab_script_input"
        )
        
    if st.button("🗣️ Synthesize Speech Output Stream", use_container_width=True):
        if not audio_text.strip() or audio_text.startswith("Enter or generate primary draft"):
            st.warning("Narrative workspace contains no valid speech configuration data.")
        else:
            with st.spinner("Compiling high-fidelity clean stream tracks..."):
                try:
                    # Pointing to the patched client-backed media service pipeline
                    # Restricting payload window defensively to prevent standard context limits
                    audio_bytes = media_service.text_to_speech(audio_text[:2000], model=audio_model)
                    st.audio(audio_bytes, format="audio/mp3")
                    st.success("Clean high-fidelity audio narration generated!")
                except Exception as e:
                    st.error(f"Audio API Disconnect: {str(e)}")
