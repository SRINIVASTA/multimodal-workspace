import streamlit as st

def render_audio_tab():
    st.subheader("🎵 Hyper-Realistic Voice Synthesis Engine")
    
    # Import and bind identical backend unified service client
    from src.api.media_service import UnifiedAIService
    ai_service = UnifiedAIService()
    
    # Dynamic Voice Engine Selection Matrix (Free & Streams Native MP3)
    audio_model = st.selectbox(
        "Select Dynamic Speech/Voice Engine:",
        [
            "fish-audio/s2.1-pro-free:free"
        ],
        key="audio_dynamic_model_selector"
    )
    
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
                    # Fires request securely to the refactored, endpoint-safe audio node route
                    audio_bytes = ai_service.text_to_speech(text=audio_text[:2000], model=audio_model)
                    
                    st.audio(audio_bytes, format="audio/mp3")
                    st.success("Clean high-fidelity audio narration generated successfully!")
                except Exception as e:
                    st.error(f"Audio API Disconnect: {str(e)}")
