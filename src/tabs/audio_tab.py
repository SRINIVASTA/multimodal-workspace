import streamlit as st

def render_audio_tab():
    st.subheader("🎵 Hyper-Realistic Voice Synthesis & Transcription Engine")
    
    from src.api.media_service import UnifiedAIService
    from src.api.transcribe_service import TranscriptionService
    
    ai_service = UnifiedAIService()
    transcribe_service = TranscriptionService()
    
    tab_tts, tab_stt = st.tabs(["⚡ Text-to-Speech (Synthesis)", "🎙️ Speech-to-Text (Transcription)"])
    
    # =========================================================================
    # SUB-TAB 1: TEXT-TO-SPEECH (TTS)
    # =========================================================================
    with tab_tts:
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
                        audio_bytes = ai_service.text_to_speech(text=audio_text[:2000], model=audio_model, voice="")
                        st.session_state["compiled_audio_track"] = audio_bytes
                        st.success("Clean high-fidelity audio narration generated successfully!")
                    except Exception as e:
                        st.error(f"Audio API Disconnect: {str(e)}")
                        
        if "compiled_audio_track" in st.session_state:
            st.audio(st.session_state["compiled_audio_track"], format="audio/mp3")
            st.download_button(
                label="📥 Download Synthesized Audio Track (MP3)",
                data=st.session_state["compiled_audio_track"],
                file_name="synthesized_narration.mp3",
                mime="audio/mp3",
                use_container_width=True
            )
            
            st.write("---")
            if st.button("🗑️ Clear Synthesized Audio State", use_container_width=True, key="clear_tts_btn"):
                st.session_state.pop("compiled_audio_track", None)
                st.rerun()

    # =========================================================================
    # SUB-TAB 2: SPEECH-TO-TEXT (STT) - Universal Language Interface
    # =========================================================================
    with tab_stt:
        st.write("### Transcribe Audio Track to Text")
        
        st_model = st.selectbox(
            "Select Transcription Model Routing:",
            ["Local Free Transcription Engine"],
            key="stt_model_selector"
        )
        
        # New language mapping framework to support Telugu, Hindi, Tamil and Auto-checks
        lang_choice = st.selectbox(
            "🗣️ Select Audio Language:",
            {
                "te-IN": "Telugu (తెలుగు)",
                "hi-IN": "Hindi (हिन्दी)",
                "ta-IN": "Tamil (தமிழ்)",
                "en-IN": "Indian English (Mixed/Multilingual)",
                "en-US": "English (US)",
                "auto": "Auto-Detect Language Profile (Best Effort)"
            }.values(),
            index=0, # Defaults to Telugu based on your active request file profile
            key="stt_language_selector"
        )
        
        # Invert dictionary selection value map keying safely
        lang_code_map = {
            "Telugu (తెలుగు)": "te-IN",
            "Hindi (हिन्दी)": "hi-IN",
            "Tamil (தமிழ்)": "ta-IN",
            "Indian English (Mixed/Multilingual)": "en-IN",
            "English (US)": "en-US",
            "Auto-Detect Language Profile (Best Effort)": "auto"
        }
        selected_lang_code = lang_code_map[lang_choice]

        uploaded_audio = st.file_uploader(
            "Upload Target Audio Track Frame:", 
            type=["mp3", "wav", "m4a", "ogg"],
            key="stt_audio_uploader"
        )
        
        if uploaded_audio is not None:
            detected_format = uploaded_audio.name.split(".")[-1].lower()
            if detected_format == "m4a": 
                detected_format = "mp3"
                
            if st.button("🔮 Run Transcription Pipeline", use_container_width=True):
                with st.spinner("Decoding multi-lingual audio binary matrices..."):
                    try:
                        raw_audio_bytes = uploaded_audio.read()
                        extracted_transcript = transcribe_service.speech_to_text(
                            audio_bytes=raw_audio_bytes,
                            audio_format=detected_format,
                            language_code=selected_lang_code
                        )
                        
                        st.session_state["last_active_transcript"] = extracted_transcript
                        st.success("Transcription processing round finalized successfully!")
                    except Exception as trans_err:
                        st.error(f"Transcription Pipeline Crash: {str(trans_err)}")
                        
        if "last_active_transcript" in st.session_state:
            edited_transcript = st.text_area(
                "Extracted Transcript Output Context Window:", 
                value=st.session_state["last_active_transcript"], 
                height=180,
                key="stt_transcript_edit_area"
            )
            
            if st.button("💾 Sync Transcript to Tab 1 Document Draft", use_container_width=True):
                st.session_state.document_draft = edited_transcript
                st.toast("✅ Workspace Synced! Draft shifted to Document Engine.", icon="💾")
                st.success("Draft snapshot synchronized back into main Workspace Matrix panel successfully!")
                st.rerun()
                
            st.write("---")
            if st.button("🗑️ Clear Transcription State & File Window", use_container_width=True, key="clear_stt_btn"):
                st.session_state.pop("last_active_transcript", None)
                st.rerun()
