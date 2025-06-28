import streamlit as st
from src.ui.tabs.general_tab import render_general_tab
from src.ui.tabs.quality_tab import render_quality_tab
from src.ui.tabs.weight_tab import render_weight_tab
from src.ui.tabs.defects_tab import render_defects_tab
from src.ui.tabs.camera_tab import render_camera_tab

def render_tabs():
    """Render the main application tabs"""
    # Main tabs
    tab_list = ["Thông tin/General", "Chất lượng/Quality", "Khối lượng/Weight", "Lỗi/Defects", "Camera"]
    tabs = st.tabs(tab_list)

    # Render the content for each tab
    with tabs[0]:
        render_general_tab()

    with tabs[1]:
        render_quality_tab()

    with tabs[2]:
        render_weight_tab()

    with tabs[3]:
        render_defects_tab()

    with tabs[4]:
        render_camera_tab()
