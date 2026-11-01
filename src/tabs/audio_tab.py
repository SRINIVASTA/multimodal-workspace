import streamlit as st

def render_audio_tab():
    st.subheader("🎵 Hyper-Realistic Voice Synthesis & Transcription Engine")
    
    from src.api.media_service import UnifiedAIService
    ai_service = UnifiedAIService()
    
    # Split the workspace into clear task panels
    mode_selection = st.tabs(["⚡ Text-to-Speech (Synthesis)", "🎙️ Speech-to-Text (Transcription)"])
    
    # =========================================================================
    # TASK PANEL 1: TEXT TO SPEECH
    # =========================================================================
    with mode_selection[0]:
        audio_model = st.selectbox(
            "Select Free Dynamic Speech/Voice Engine:",
            ["fish-audio/s2.1-pro-free:free"],
            key="audio_dynamic_model_selector"
        )
        
        with st.expander("📝 View Folded Script Templates"):
            st.code("Good morning team. Welcome to the automated operations performance review.", language="text")

        audio_source = st.radio(
            "Select Target Audio Source:", 
            ["Pull from Tab 1 Document Matrix", "Write Custom Isolated Script"], 
            horizontal=True,
            key="tts_source_selector"
        )
        
        if audio_source == "Pull from Tab 1 Document Matrix":
            audio_text = st.session_state.document_draft
            st.caption("🔗 Connected to live context editor frame inside Tab 1.")
        else:
            audio_text = st.text_area(
                "Isolated Script Panel Input:", 
                value="Welcome to the modular enterprise audio deployment suite.", 
                height=150,
                key="audio_tab_script_input"
            )
            
        if st.button("🚀 Synthesize Speech Output Stream", use_container_width=True):
            if not audio_text.strip() or audio_text.startswith("Enter or generate primary draft"):
                st.warning("Narrative workspace contains no valid speech configuration data.")
            else:
                with st.spinner("Compiling high-fidelity clean stream tracks..."):
                    try:
                        audio_bytes = ai_service.text_to_speech(text=audio_text[:2000], model=audio_model)
                        
                        # Store audio buffer into session space for multi-element availability
                        st.session_state["compiled_audio_track"] = audio_bytes
                        st.success("Clean high-fidelity audio narration generated successfully!")
                    except Exception as e:
                        st.error(f"Audio API Disconnect: {str(e)}")
                        
        # NATIVE DOWNLOAD SUB-FRAME
        if "compiled_audio_track" in st.session_state:
            st.audio(st.session_state["compiled_audio_track"], format="audio/mp3")
            st.download_button(
                label="📥 Download Synthesized Audio Track (MP3)",
                data=st.session_state["compiled_audio_track"],
                file_name="synthesized_narration.mp3",
                mime="audio/mp3",
                use_container_width=True
            )

    # =========================================================================
    # TASK PANEL 2: SPEECH TO TEXT
    # =========================================================================
    with mode_selection[1]:
        st.write("### Transcribe Audio Track to Text")
        
        st_model = st.selectbox(
            "Select Transcription Model Routing:",
            ["openai/whisper-large-v3", "fish-audio/transcribe-1-pro"],
            key="stt_model_selector"
        )
        
        uploaded_audio = st.file_uploader(
            "Upload Target Audio Track Frame:", 
            type=["mp3", "wav", "m4a", "ogg"],
            help="Select an audio file to extract transcription strings straight into workspace workflows."
        )
        
        if uploaded_audio is not None:
            # Detect string format dynamically from file extension mapping
            detected_format = uploaded_audio.name.split(".")[-1].lower()
            if detected_format == "m4a": 
                detected_format = "mp3" # Force standard audio routing fallback
                
            if st.button("🔮 Run Transcription Pipeline", use_container_width=True):
                with st.spinner("Decoding audio binary matrices..."):
                    try:
                        raw_audio_bytes = uploaded_audio.read()
                        extracted_transcript = ai_service.speech_to_text(
                            audio_bytes=raw_audio_bytes,
                            audio_format=detected_format,
                            model=st_model
                        )
                        
                        st.success("Transcription processing round finalized successfully!")
                        st.text_area("Extracted Transcript Output Context Window:", value=extracted_transcript, height=180)
                        
                        # Inject straight back into your Tab 1 data frame state sync manager
                        if st.button("💾 Sync Transcript to Tab 1 Document Draft"):
                            st.session_state.document_draft = extracted_transcript
                            st.session_state["text_tab_canvas_editor"] = extracted_transcript
                            st.info("Draft snapshot synchronized back into main Workspace Matrix panel.")
                    except Exception as trans_err:
                        st.error(f"Transcription Pipeline Crash: {str(trans_err)}")
