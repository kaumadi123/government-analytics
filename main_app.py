"""
Government Service Analytics Dashboard - Main Application
Entry point that connects the analytics engine with the dashboard UI
"""

import streamlit as st
import sys
import os


st.set_page_config(
    page_title="Gov Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme (better for metrics)
st.markdown("""
    <style>
        [data-testid="stMetricValue"] {
            color: black;
        }
    </style>
""", unsafe_allow_html=True)


# Add current directory to path to import local modules
sys.path.append(os.path.dirname(__file__))

try:
    from dashboard_ui import DashboardUI
    from analytics_engine import GovernmentServiceAnalytics
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.error("Please ensure both 'analytics_engine.py' and 'dashboard_ui.py' are in the same directory as this file.")
    st.stop()

def main():
    """
    Main application entry point
    """
    try:
        # Initialize and run the dashboard
        dashboard = DashboardUI()
        dashboard.run()
        
    except Exception as e:
        st.error(f"❌ Application Error: {e}")
        st.error("Please check that all required files are present and CSV data files are available.")
        
        with st.expander("🔧 Troubleshooting"):
            st.markdown("""
            **Required Files:**
            - `analytics_engine.py` - Core analytics processing
            - `dashboard_ui.py` - User interface components  
            - `main_app.py` - This main application file
            - `citizen_complaints.csv` - Complaints dataset
            - `employee_performance.csv` - Employee performance dataset
            - `social_media_sentiment.csv` - Sentiment analysis dataset
            - `department_summary.csv` - Department summary dataset
            
            **Common Issues:**
            1. **Missing CSV files**: Ensure all 4 CSV files are in the same directory
            2. **Import errors**: Check that all Python files are in the same directory
            3. **Package errors**: Run `pip install streamlit pandas plotly` to install dependencies
            """)

if __name__ == "__main__":
    main()