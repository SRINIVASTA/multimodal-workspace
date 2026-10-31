import streamlit as st
import base64

def render_image_tab():
    st.subheader("🎨 Graphic Design & Vision Analysis Studio")
    
    from src.api.client import OpenRouterClient
    from src.api.media_service import MediaService
    from src.api.text_service import TextService
    
    client = OpenRouterClient()
    media_service = MediaService(client)
    text_service = TextService(client)
    
    tab_gen, tab_vision = st.tabs(["✨ Text-To-Image Engine", "👁️ Vision & File Analysis"])
    
    # ---------------------------------------------------------
    # SUB-TAB 1: TEXT TO IMAGE GENERATION WORKSPACE
    # ---------------------------------------------------------
    with tab_gen:
        col_l, col_r = st.columns(2)
        with col_l:
            st.write("#### Design Configuration Canvas")
            image_model = st.selectbox(
                "Select Dynamic Generation Engine:",
                ["black-forest-labs/flux-1-schnell", "openai/dall-e-3"],
                key="image_tab_engine_selector"
            )
            img_prompt = st.text_area("Graphic Specifications Layout Prompt:", key="image_tab_raw_prompt_input")
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                render_clicked = st.button("Render Canvas Asset", use_container_width=True)
            with col_b2:
                feed_clicked = st.button("🔗 Inject to Doc Canvas", use_container_width=True)
                
            if render_clicked or feed_clicked:
                if not img_prompt.strip():
                    st.warning("⚠️ Please provide a description layout prompt first.")
                else:
                    with st.spinner("Processing generative graphic assets..."):
                        try:
                            url = media_service.generate_image(img_prompt, image_model)
                            st.session_state["last_generated_img_url"] = url
                            
                            if feed_clicked:
                                st.session_state.document_draft += f"\n\n![Generated Graphic]({url})\n"
                                st.toast("Image canvas link cleanly injected into Tab 1!")
                        except Exception as e:
                            st.error(f"Image System Error: {str(e)}")
                        
        with col_r:
            st.write("#### Asset Visual Canvas")
            if "last_generated_img_url" in st.session_state:
                st.image(st.session_state["last_generated_img_url"], caption="Active Visual Track Frame")
            else:
                st.info("Awaiting creative visual mapping generations...")

    # ---------------------------------------------------------
    # SUB-TAB 2: ENTERPRISE IMAGE UPLOAD & VISION ANALYSIS
    # ---------------------------------------------------------
    with tab_vision:
        col_v_l, col_v_r = st.columns(2)
        with col_v_l:
            st.write("#### Upload Target Document / Image")
            uploaded_file = st.file_uploader("Choose an image file...", type=["jpg", "jpeg", "png"], key="vision_uploader")
            
            vision_model = st.selectbox(
                "Select Vision Model Engine:",
                ["google/gemini-2.5-flash", "openai/gpt-4o-mini"],
                key="vision_model_selector"
            )
            vision_prompt = st.text_area("What would you like to ask about this image?", value="Analyze this image in detail and extract key structural insights.", key="vision_prompt_input")
            
            if st.button("🔬 Execute Multimodal Vision Analysis", use_container_width=True):
                if uploaded_file is None:
                    st.warning("⚠️ Please upload a valid image file first.")
                else:
                    with st.spinner("Analyzing image array context via OpenRouter Multimodal Engine..."):
                        try:
                            # Read and convert the file into an safe base64 data string payload wrapper
                            file_bytes = uploaded_file.read()
                            base64_image = base64.b64encode(file_bytes).decode("utf-8")
                            mime_type = uploaded_file.type
                            
                            # Construct structural OpenAI-compatible vision message block array
                            vision_payload = {
                                "model": vision_model,
                                "messages": [
                                    {
                                        "role": "user",
                                        "content": [
                                            {"type": "text", "text": vision_prompt},
                                            {
                                                "type": "image_url",
                                                "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
                                            }
                                        ]
                                    }
                                ],
                                "max_tokens": 1000
                            }
                            
                            res = client.post("chat/completions", vision_payload)
                            st.session_state["last_vision_analysis_output"] = res.json()['choices'][0]['message']['content']
                            st.success("Vision analysis complete!")
                        except Exception as vision_err:
                            st.error(f"Vision Engine Processing Aborted: {str(vision_err)}")
                            
        with col_v_r:
            if uploaded_file is not None:
                st.write("#### Image Preview")
                st.image(uploaded_file, use_container_width=True)
                
            if "last_vision_analysis_output" in st.session_state:
                st.write("#### 📝 Extracted Analysis Logs")
                st.markdown(st.session_state["last_vision_analysis_output"])
                
                if st.button("🔗 Append Analysis to Document Tab", use_container_width=True):
                    st.session_state.document_draft += f"\n\n### Image Analysis Report\n{st.session_state['last_vision_analysis_output']}\n"
                    st.toast("Analysis text successfully appended to Tab 1 Document Editor!")
