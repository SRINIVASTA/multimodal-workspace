import streamlit as st
import pandas as pd
from typing import Dict

class SessionStateManager:
    @staticmethod
    def initialize():
        if "save_points" not in st.session_state:
            st.session_state.save_points = {}
        if "document_draft" not in st.session_state:
            st.session_state.document_draft = "Enter or generate primary draft contents..."
        if "data_frame" not in st.session_state:
            st.session_state.data_frame = pd.DataFrame({
                "Region": ["North America", "EMEA", "APAC"],
                "Sales": [550000, 420000, 610000]
            })

    @staticmethod
    def commit_snapshot(name: str, layout_content: str):
        st.session_state.save_points[name] = layout_content

    @staticmethod
    def rollback_snapshot(name: str):
        st.session_state.document_draft = st.session_state.save_points[name]
