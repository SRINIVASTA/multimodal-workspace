import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from src.utils.file_parser import extract_text_from_file

def render_text_tab():
    st.subheader("📝 Advanced Document Generation & Analysis Engine")
    
    from src.api.client import OpenRouterClient
    from src.api.text_service import TextService
    
    client = OpenRouterClient()
    text_service = TextService(client)
    
    if "text_tab_canvas_editor" not in st.session_state:
        st.session_state["text_tab_canvas_editor"] = st.session_state.document_draft
        
    if "extracted_doc_context" not in st.session_state:
        st.session_state["extracted_doc_context"] = ""

    col_in, col_out = st.columns(2)
    with col_in:
        st.write("#### Orchestration Parameters")
        
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
        
        # Mode Selection Matrix
        mode = st.radio("Choose Mode:", ["Topic Synthesis", "Analyze Uploaded Document"], horizontal=True)
        
        if mode == "Topic Synthesis":
            topic = st.text_input("Target Analysis Topic:", key="text_tab_topic_input")
            
            with st.expander("💡 View Sample Research Prompts"):
                st.code("Comprehensive analysis of global microchip supply chains in 2026", language="text")
                st.code("Corporate financial impact report detailing automated logistics frameworks", language="text")

            if st.button("Query Dynamic Web Engine", use_container_width=True):
                if not topic.strip():
                    st.warning("Please enter a research topic first.")
                else:
                    with st.spinner("Processing deep technical analysis..."):
                        try:
                            response_content = text_service.generate_document(topic, model=text_model)
                            st.session_state.document_draft = response_content
                            st.session_state["text_tab_canvas_editor"] = response_content
                            st.rerun()
                        except Exception as e:
                            st.error(f"Text Generation Exception: {str(e)}")
                            
        else:
            st.write("##### Attach Document Matrix")
            uploaded_doc = st.file_uploader(
                "Upload Report File Layer", 
                type=["txt", "pdf", "docx", "csv"], 
                key="text_tab_file_uploader"
            )
            
            if uploaded_doc is not None:
                # Cache parsed results so re-renders don't re-parse the physical layout stream
                if st.button("📥 Load & Parse Document Target", use_container_width=True):
                    with st.spinner("Decoding document blocks..."):
                        st.session_state["extracted_doc_context"] = extract_text_from_file(uploaded_doc)
                        st.success(f"Successfully processed {uploaded_doc.name}! Context indexed.")
            
            if st.session_state["extracted_doc_context"]:
                st.info("💡 Document context active in memory. Ask your question below:")
                user_question = st.text_area("Analysis Query Prompt:", placeholder="e.g., Summarize the financial vulnerabilities or extract the core trends.")
                
                if st.button("🔬 Execute Context Analysis", use_container_width=True):
                    if not user_question.strip():
                        st.warning("Please provide a query prompt instruction.")
                    else:
                        with st.spinner("Analyzing document matrix layers..."):
                            try:
                                # Packaging both the custom text query and the file context injection safely
                                complete_prompt = (
                                    f"Context data from uploaded document:\n"
                                    f"---START CONTEXT---\n{st.session_state['extracted_doc_context'][:8000]}\n---END CONTEXT---\n\n"
                                    f"User Instruction: {user_question}"
                                )
                                response_content = text_service.generate_document(complete_prompt, model=text_model)
                                st.session_state.document_draft = response_content
                                st.session_state["text_tab_canvas_editor"] = response_content
                                st.rerun()
                            except Exception as e:
                                st.error(f"Document Analysis Exception: {str(e)}")
                    
    with col_out:
        st.write("#### Live Document Canvas")
        st.session_state.document_draft = st.text_area(
            "Workspace Editor Canvas", 
            height=400, 
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
            try:
                pdf_buffer = io.BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
                styles = getSampleStyleSheet()
                body_style = ParagraphStyle('PDFBody', parent=styles['Normal'], fontSize=10, leading=14)
                
                story = []
                for line in st.session_state.document_draft.split('\n'):
                    if line.strip():
                        story.append(Paragraph(line, body_style))
                        story.append(Spacer(1, 6))
                
                doc.build(story)
                st.download_button(
                    label="📄 Download Compiled PDF",
                    data=pdf_buffer.getvalue(),
                    file_name="compiled_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as pdf_err:
                st.error(f"PDF Infrastructure Compiler Error: {str(pdf_err)}")
