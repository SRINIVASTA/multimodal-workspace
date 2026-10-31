import streamlit as st
import base64
import io
import textwrap
import requests
from PIL import Image, ImageDraw

def get_sandbox_placeholder_image(prompt_text: str):
    """Generates a high-quality local placeholder canvas and burns the prompt text inside it."""
    img = Image.new('RGB', (800, 450), color='#1E293B') 
    d = ImageDraw.Draw(img)
    
    d.rectangle([(20, 20), (780, 430)], outline='#38BDF8', width=3) 
    d.line([(20, 20), (780, 430)], fill='#334155', width=1)
    d.line([(20, 430), (780, 20)], fill='#334155', width=1)
    
    d.text((40, 40), "🚧 LOCAL HACKATHON SANDBOX MODE PREVIEW", fill='#38BDF8')
    
    cleaned_prompt = prompt_text.strip() if prompt_text.strip() else "System idle. Awaiting configuration prompts..."
    wrapped_lines = textwrap.wrap(cleaned_prompt, width=65)
    
    y_offset = 120
    for line in wrapped_lines[:10]:
        d.text((50, y_offset), line, fill='#94A3B8')
        y_offset += 25
        
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def render_image_tab():
    st.subheader("🎨 Graphic Design & Vision Analysis Studio")
    
    # FIXED: Consumes UnifiedAIService to eliminate import layout name crashes
    from src.api.media_service import UnifiedAIService
    ai_service = UnifiedAIService()
    
    tab_gen, tab_vision = st.tabs(["✨ Text-To-Image Engine", "👁️ Vision & File Analysis"])
    
    # ---------------------------------------------------------
    # SUB-TAB 1: TEXT TO IMAGE ENGINE
    # ---------------------------------------------------------
    with tab_gen:
        col_l, col_r = st.columns(2)
        with col_l:
            st.write("#### Design Configuration Canvas")
            
            image_model = st.selectbox(
                "Select Dynamic Generation Engine:",
                [
                    "openai/gpt-image-2",
                    "openai/gpt-image-2.5-sunburst",
                    "black-forest-labs/flux-3-image"
                ],
                key="image_tab_engine_selector"
            )
            
            with st.expander("📊 Option 1: Automatic Metric Data Binding"):
                if "data_frame" in st.session_state:
                    regions = ", ".join(st.session_state.data_frame["Region"].tolist())
                    sales = ", ".join([f"${val:,}" for val in st.session_state.data_frame["Sales"].tolist()])
                    bound_prompt = f"Vector infographic layout displaying performance metrics for regions: {regions}. Left side charts map total metrics: {sales}. Flat corporate modern design style."
                    st.code(bound_prompt, language="text")

            with st.expander("📄 Option 2: Custom ReportLab PDF Image Constraints"):
                st.code("A professional engineering document header graphic template asset. Styled for landscape A4 margins. Clean geometric trace lines on an ultra-light gray backdrop.", language="text")

            img_prompt = st.text_area("Graphic Specifications Layout Prompt:", key="image_tab_raw_prompt_input")
            sandbox_mode = st.toggle("Enable Local Hackathon Sandbox Mode", value=True)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                render_clicked = st.button("Render Canvas Asset", use_container_width=True)
            with col_b2:
                feed_clicked = st.button("🔗 Inject to Doc Canvas", use_container_width=True)
                
            if render_clicked or feed_clicked:
                if not img_prompt.strip():
                    st.warning("Awaiting creative layout parameters...")
                else:
                    with st.spinner("Compiling image data stream..."):
                        try:
                            if sandbox_mode:
                                st.session_state["last_generated_img_data"] = get_sandbox_placeholder_image(img_prompt)
                                st.session_state["last_generated_img_url"] = "https://placeholder.com"
                                st.success("🎉 Asset compilation completed successfully (Sandbox Mode Profile)!")
                            else:
                                # FIXED: Utilizes unified service generation syntax cleanly
                                url = ai_service.generate_image(img_prompt, image_model)
                                st.session_state["last_generated_img_url"] = url
                                if "last_generated_img_data" in st.session_state:
                                    del st.session_state["last_generated_img_data"]
                                st.success("Asset generation sequence complete!")
                        except Exception as e:
                            st.error(f"Image System Error: {str(e)}")
                        
        with col_r:
            st.write("#### Asset Visual Canvas")
            if "last_generated_img_data" in st.session_state:
                st.image(st.session_state["last_generated_img_data"], caption="Active Visual Track Frame (Local Sandbox)", use_container_width=True)
            elif "last_generated_img_url" in st.session_state and st.session_state["last_generated_img_url"] != "https://placeholder.com":
                st.image(st.session_state["last_generated_img_url"], caption="Active Visual Track Frame (Live Remote API)", use_container_width=True)
            else:
                st.info("Awaiting creative visual mapping generations...")

            if feed_clicked and "last_generated_img_url" in st.session_state:
                st.session_state.document_draft += f"\n\n![Generated Graphic]({st.session_state['last_generated_img_url']})\n"
                st.toast("Embedded asset URL link directly into Document Editor Tab!")
    # ---------------------------------------------------------
    # SUB-TAB 2: IMAGE FILE UPLOAD & VISION ANALYSIS HUB
    # ---------------------------------------------------------
    with tab_vision:
        col_v_l, col_v_r = st.columns(2)
        with col_v_l:
            st.write("#### Select Source Context")
            
            source_mode = st.radio(
                "Vision Analysis Image Target:",
                ["Use active generated studio graphic", "Upload fresh image file from disk"],
                horizontal=True,
                key="vision_source_mode_selector"
            )
            
            file_bytes = None
            mime_type = "image/png"
            
            if source_mode == "Upload fresh image file from disk":
                uploaded_file = st.file_uploader("Choose an image file...", type=["jpg", "jpeg", "png"], key="vision_uploader")
                if uploaded_file is not None:
                    file_bytes = uploaded_file.read()
                    mime_type = uploaded_file.type
            else:
                if "last_generated_img_data" in st.session_state:
                    file_bytes = st.session_state["last_generated_img_data"]
                    st.info("🔄 Automatically binding active Local Sandbox image stream context.")
                elif "last_generated_img_url" in st.session_state and st.session_state["last_generated_img_url"] != "https://placeholder.com":
                    try:
                        res = requests.get(st.session_state["last_generated_img_url"], timeout=15)
                        if res.ok:
                            file_bytes = res.content
                            st.info("🔄 Automatically fetched and bound active Live API graphic track.")
                    except Exception:
                        pass
                
                if file_bytes is None:
                    st.warning("⚠️ No generated graphic active in the studio canvas yet. Run text-to-image synthesis first.")

            vision_model = st.selectbox(
                "Select Vision Model Engine:",
                ["google/gemini-2.5-flash", "openai/gpt-4o-mini"],
                key="vision_model_selector"
            )
            
            vision_prompt = st.text_area("Vision Analysis Directive Input:", value="Analyze this image layout matrix in detail and extract key structural insights.", key="vision_prompt_input")
            
            if st.button("🔬 Execute Multimodal Vision Analysis", use_container_width=True):
                if file_bytes is None:
                    st.error("❌ Execution aborted: No valid source pixels available.")
                else:
                    with st.spinner("Analyzing image array context..."):
                        try:
                            base64_image = base64.b64encode(file_bytes).decode("utf-8")
                            
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
            st.write("#### Analysis Preview & Output Screen")
            if source_mode == "Upload fresh image file from disk" and uploaded_file is not None:
                st.image(file_bytes, use_container_width=True, caption="Uploaded File Preview")
            elif source_mode == "Use active generated studio graphic" and file_bytes is not None:
                st.image(file_bytes, use_container_width=True, caption="Active Studio Canvas Preview")
                
            if "last_vision_analysis_output" in st.session_state:
                st.write("#### 📝 Extracted Analysis Logs")
                st.markdown(st.session_state["last_vision_analysis_output"])
                if st.button("🔗 Append Analysis to Document Tab", use_container_width=True):
                    st.session_state.document_draft += f"\n\n### Image Analysis Report\n{st.session_state['last_vision_analysis_output']}\n"
                    st.toast("Analysis text successfully appended to Tab 1 Document Editor!")
