import streamlit as st

def render_image_tab():
    st.subheader("🎨 Graphic Design & Asset Studio")
    
    from src.api.client import OpenRouterClient
    from src.api.media_service import MediaService
    
    client = OpenRouterClient()
    media_service = MediaService(client)
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("#### Design Configuration Canvas")
        
        image_model = st.selectbox(
            "Select Dynamic Generation Engine:",
            [
                "black-forest-labs/flux-1-schnell",
                "openai/dall-e-3",
                "stabilityai/stable-diffusion-3"
            ],
            key="image_dynamic_model_selector"
        )
        
        img_prompt = st.text_area("Graphic Specifications Layout Prompt:", key="image_tab_prompt_input")
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            render_clicked = st.button("Render Canvas Asset", use_container_width=True)
        with col_b2:
            feed_clicked = st.button("🔗 Inject to Doc Canvas", use_container_width=True)
            
        if render_clicked or feed_clicked:
            # DEFENSIVE VALIDATION LAYER: Catch blank fields locally
            if not img_prompt.strip():
                st.warning("⚠️ Request Aborted: Please provide a description in the Graphic Specifications Layout Prompt field first.")
            else:
                with st.spinner("Processing generative graphic assets..."):
                    try:
                        url = media_service.generate_image(img_prompt, image_model)
                        st.session_state["last_generated_img_url"] = url
                        
                        if feed_clicked:
                            st.session_state.document_draft += f"\n\n![Generated Graphic]({url})\n"
                            st.toast("Image canvas link cleanly injected into Tab 1 database!")
                    except Exception as e:
                        st.error(f"Image System Error: {str(e)}")
                    
    with col_r:
        st.write("#### Asset Visual Canvas")
        if "last_generated_img_url" in st.session_state:
            st.image(st.session_state["last_generated_img_url"], caption="Active Visual Track Frame")
        else:
            st.info("Awaiting creative visual mapping generations...")
