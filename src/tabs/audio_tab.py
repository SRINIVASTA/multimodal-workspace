import streamlit as st

def render_audio_tab():
    st.subheader("🎵 Universal Multilingual Voice Synthesis & Transcription Engine")
    
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
    # SUB-TAB 2: SPEECH-TO-TEXT (STT) - Real-time On-Demand Translation
    # =========================================================================
    with tab_stt:
        st.write("### Transcribe & Real-time Translate Audio Track")
        
        uploaded_audio = st.file_uploader(
            "Upload Target Audio Track Frame:", 
            type=["mp3", "wav", "m4a", "ogg", "flac"],
            key="stt_audio_uploader"
        )
        
        # Automatic input spoken language fingerprint analysis tracking logic pass
        detected_lang_label = "Awaiting File Attachment..."
        if uploaded_audio is not None:
            if "last_file_name" not in st.session_state or st.session_state.last_file_name != uploaded_audio.name:
                with st.spinner("🧠 Scanning audio waveform patterns to identify spoken language..."):
                    try:
                        st.session_state.last_file_name = uploaded_audio.name
                        raw_bytes = uploaded_audio.getvalue()
                        det_format = uploaded_audio.name.split(".")[-1].lower()
                        if det_format == "m4a": det_format = "mp3"
                        
                        guessed_code = transcribe_service.detect_audio_language(raw_bytes, det_format)
                        st.session_state.auto_detected_lang = guessed_code
                        # Flush past transcript items upon dynamic item updates
                        st.session_state.pop("raw_extracted_transcript", None)
                    except Exception:
                        st.session_state.auto_detected_lang = "en-US"
            
            code_visual_map = {"te-IN": "Telugu (తెలుగు)", "hi-IN": "Hindi (हिन्दी)", "ta-IN": "Tamil (தமிழ்)", "en-US": "English (US)"}
            detected_lang_label = f"💡 Automatically Detected: {code_visual_map.get(st.session_state.auto_detected_lang, 'English (US)')}"
        
        st.info(f"🗣️ Spoken Audio Language (Input Tracking): **{detected_lang_label}**")
        
        if uploaded_audio is not None:
            detected_format = uploaded_audio.name.split(".")[-1].lower()
            if detected_format == "m4a": 
                detected_format = "mp3"
                
            if st.button("🔮 Step 1: Run Audio Transcription", use_container_width=True):
                with st.spinner("Extracting speech vectors..."):
                    try:
                        raw_audio_bytes = uploaded_audio.read()
                        chosen_input_lang = st.session_state.get("auto_detected_lang", "en-US")
                        
                        # Transcribe strictly to the original language first
                        transcript_raw = transcribe_service.speech_to_text(
                            audio_bytes=raw_audio_bytes,
                            audio_format=detected_format,
                            language_code=chosen_input_lang,
                            target_lang="original"
                        )
                        st.session_state["raw_extracted_transcript"] = transcript_raw
                        st.success("Audio transcribed successfully into its native language!")
                    except Exception as trans_err:
                        st.error(f"Processing Pipeline Crash: {str(trans_err)}")

        # Step 2: Live Translation UI Switch (Only renders once original text is present)
        if "raw_extracted_transcript" in st.session_state:
            st.write("---")
            st.write("### 🌍 Step 2: Live Translation Options")
            
            target_choice = st.selectbox(
                "🌐 Convert Output Text Language to:",
                ["Original (Same as Audio)", "Telugu (తెలుగు)", "Hindi (हिन्दी)", "Tamil (தமிழ்)", "English"],
                index=0,
                key="stt_output_language_selector"
            )
            
            output_code_map = {
                "Original (Same as Audio)": "original", 
                "English": "en", 
                "Telugu (తెలుగు)": "te", 
                "Hindi (हिन्दी)": "hi", 
                "Tamil (தமிழ்)": "ta"
            }
            selected_output_code = output_code_map[target_choice]
            
            # Execute on-the-fly string translation instantly without touching the audio file again
            with st.spinner("Translating text layout..."):
                display_text = transcribe_service._translate_text(
                    st.session_state["raw_extracted_transcript"], 
                    selected_output_code
                )
                
            edited_transcript = st.text_area(
                "Final Transcript / Translation Output Window:", 
                value=display_text, 
                height=180,
                key="stt_transcript_edit_area"
            )
            
            if st.button("💾 Sync Transcript to Tab 1 Document Draft", use_container_width=True):
                st.session_state.document_draft = edited_transcript
                st.toast("✅ Workspace Synced! Draft shifted to Document Engine.", icon="💾")
                st.success("Draft snapshot synchronized back into main Workspace Matrix panel successfully!")
                st.rerun()
                
            if st.button("🗑️ Clear Transcription State & File Window", use_container_width=True, key="clear_stt_btn"):
                st.session_state.pop("raw_extracted_transcript", None)
                st.session_state.pop("last_file_name", None)
                st.rerun()
