import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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
            if not topic.strip():
                st.warning("Please enter a research topic first.")
            else:
                with st.spinner("Processing deep technical analysis..."):
                    try:
                        st.session_state.document_draft = text_service.generate_document(topic, model=text_model)
                        st.slots = {} # Reset runtime caching slots safely
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
            # FIX: Real ReportLab Compilation Engine using memory byte buffers
            try:
                pdf_buffer = io.BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
                styles = getSampleStyleSheet()
                
                # Custom body layout flow configuration
                body_style = ParagraphStyle(
                    'PDFBody',
                    parent=styles['Normal'],
                    fontSize=10,
                    leading=14
                )
                
                story = []
                # Basic line-break structural processing loop
                for line in st.session_state.document_draft.split('\n'):
                    if line.strip():
                        story.append(Paragraph(line, body_style))
                        story.append(Spacer(1, 6))
                
                doc.build(story)
                pdf_data = pdf_buffer.getvalue()
                
                st.download_button(
                    label="📄 Download Compiled PDF",
                    data=pdf_data,
                    file_name="compiled_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as pdf_err:
                st.error(f"PDF Infrastructure Compiler Error: {str(pdf_err)}")
