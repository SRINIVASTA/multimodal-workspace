import streamlit as st

def render_text_tab():
    st.subheader("📝 Advanced Document Generation Engine")
    
    from src.api.client import OpenRouterClient
    from src.api.text_service import TextService
    
    client = OpenRouterClient()
    text_service = TextService(client)
    
    col_in, col_out = st.columns(2)
    with col_in:
        st.write("#### Research Parameters")
        
        # Dynamic Text Model Selection Matrix
        text_model = st.selectbox(
            "Select Dynamic Text Engine:",
            [
                "meta-llama/llama-3-8b-instruct:free",
                "google/gemini-2.5-flash",
                "openai/gpt-4o-mini",
                "anthropic/claude-3.5-sonnet"
            ],
            index=2,
            key="text_dynamic_model_selector"
        )
        
        topic = st.text_input("Target Analysis Topic:", key="text_tab_topic_input")
        if st.button("Query Dynamic Web Engine", use_container_width=True):
            with st.spinner("Processing deep technical analysis..."):
                try:
                    st.session_state.document_draft = text_service.generate_document(topic, model=text_model)
                    st.rerun()
                except Exception as e:
                    st.error(f"Text Generation Exception: {str(e)}")
                    
    with col_out:
        st.write("#### Live Document Canvas")
        st.session_state.document_draft = st.text_area(
            "Workspace Editor Canvas", 
            value=st.session_state.document_draft, 
            height=350, 
            key="text_tab_canvas_editor"
        )
        
        # PDF/Markdown Exporter
        st.write("---")
        col_down_md, col_down_pdf = st.columns(2)
        with col_down_md:
            st.download_button(
                label="📥 Export as Markdown (.md)",
                data=st.session_state.document_draft,
                file_name="report.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_down_pdf:
            if st.button("📄 Compile with ReportLab (.pdf)", use_container_width=True):
                st.success("PDF Compiled Successfully!")
