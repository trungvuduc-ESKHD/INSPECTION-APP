import streamlit as st
import pandas as pd
from src.ui.components.ui_helpers import create_styled_header

def render_container_status():
    """Render the container status form"""
    create_styled_header("Trạng thái container/Container Status")
    
    container_status_data = []
    for i, status in enumerate(st.session_state.inspection_data['containerStatus']):
        container_status_data.append([
            i + 1,
            status['feature'],
            status['isOk']
        ])
    
    container_df = pd.DataFrame(
        container_status_data,
        columns=["No", "Đặc điểm/Feature", "OK/NG"]
    )
    
    # Edit container status
    for i, status in enumerate(st.session_state.inspection_data['containerStatus']):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"<div>{i+1}. {status['feature']}</div>", unsafe_allow_html=True)
        with col2:
            current_value = status['isOk']
            options = ["OK", "NG", "N/A"]
            current_index = 2  # Default to N/A
            if current_value == True:
                current_index = 0
            elif current_value == False:
                current_index = 1
            
            new_value = st.selectbox(
                "Status", 
                options, 
                index=current_index,
                key=f"container_status_{i}",
                label_visibility="collapsed"
            )
            
            # Update the value in session state
            if new_value == "OK":
                st.session_state.inspection_data['containerStatus'][i]['isOk'] = True
            elif new_value == "NG":
                st.session_state.inspection_data['containerStatus'][i]['isOk'] = False
            else:
                st.session_state.inspection_data['containerStatus'][i]['isOk'] = None
