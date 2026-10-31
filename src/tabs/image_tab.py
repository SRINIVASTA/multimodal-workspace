import streamlit as st
import base64
import io
import textwrap
from PIL import Image, ImageDraw, ImageFont

def get_sandbox_placeholder_image(prompt_text: str):
    """Generates a high-quality local placeholder canvas and burns the prompt text inside it."""
    # Create dark slate blueprint slate matrix background frame (800x450 landscape)
    img = Image.new('RGB', (800, 450), color='#1E293B') 
    d = ImageDraw.Draw(img)
    
    # Draw boundary alignment wireframes 
    d.rectangle([(20, 20), (780, 430)], outline='#38BDF8', width=3) 
    d.line([(20, 20), (780, 430)], fill='#334155', width=1)
    d.line([(20, 430), (780, 20)], fill='#334155', width=1)
    
    # Overlay context tracking metrics text layers
    d.text((40, 40), "🚧 LOCAL HACKATHON SANDBOX MODE PREVIEW", fill='#38BDF8')
    
    # Text-wrapping layout logic block to prevent line truncation dropouts
    cleaned_prompt = prompt_text.strip() if prompt_text.strip() else "System idle. Awaiting configuration prompts..."
    wrapped_lines = textwrap.wrap(cleaned_prompt, width=65)
    
    y_offset = 120
    for line in wrapped_lines[:10]: # Safely cap heights to fit baseline boundaries
        d.text((50, y_offset), line, fill='#94A3B8')
        y_offset += 25
        
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def render_image_tab():
    st.subheader("🎨 Graphic Design & Vision Analysis Studio")
    
    from src.api.client import OpenRouterClient
    from src.api.media_service import MediaService
    from src.api.text_service import TextService
    
    client = OpenRouterClient()
    media_service = MediaService(client)
    text_service = TextService(client)
    
    tab_gen, tab_vision = st.tabs(["✨ Text-To-Image Engine", "👁️ Vision & File Analysis"])
    
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
                else:
                    st.info("No active data frames identified.")

            with st.expander("📄 Option 2: Custom ReportLab PDF Image Constraints"):
                st.code("A professional engineering document header graphic template asset. Styled for landscape A4 margins. Clean geometric trace lines on an ultra-light gray backdrop.", language="text")

            with st.expander("🏢 Option 3: Dark-Mode Architectural Theme"):
                st.code("Hyper-realistic architectural concept rendering of a towering corporate headquarters at night. Glass cladding, deep black metal panels, sharp orange aesthetic glow layers.", language="text")

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
                                # FIXED: Passes prompt data down dynamically into the image canvas burner matrix
                                st.session_state["last_generated_img_data"] = get_sandbox_placeholder_image(img_prompt)
                                st.session_state["last_generated_img_url"] = "https://placeholder.com"
                                st.success("🎉 Asset compilation completed successfully (Sandbox Mode Profile)!")
                            else:
                                url = media_service.generate_image(img_prompt, image_model)
                                st.session_state["last_generated_img_url"] = url
                                if "last_generated_img_data" in st.session_state:
                                    del st.session_state["last_generated_img_data"]
                                st.success("Asset generation sequence complete!")
                        except Exception as e:
                            if "402" in str(e):
                                st.error("❌ OpenRouter Account lacks credits. Activate Sandbox Mode above to simulate.")
                            else:
                                st.error(f"Image System Error: {str(e)}")
                        
        with col_r:
            st.write("#### Asset Visual Canvas")
            if "last_generated_img_data" in st.session_state:
                st.image(st.session_state["last_generated_img_data"], caption="Active Visual Track Frame (Local Sandbox)", use_container_width=True)
            elif "last_generated_img_url" in st.session_state:
                st.image(st.session_state["last_generated_img_url"], caption="Active Visual Track Frame (Live Remote API)", use_container_width=True)
            else:
                st.info("Awaiting creative visual mapping generations...")

            if feed_clicked and "last_generated_img_url" in st.session_state:
                st.session_state.document_draft += f"\n\n![Generated Graphic]({st.session_state['last_generated_img_url']})\n"
                st.toast("Embedded asset URL link directly into Document Editor Tab!")

    with tab_vision:
        # Keeping vision system analytics structures bound securely...
        pass
