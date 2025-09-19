"""
Government Service Analytics Dashboard UI
Handles all user interface components and visualizations
Uses the analytics_engine.py for data processing
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from analytics_engine import GovernmentServiceAnalytics


class DashboardUI:
    """
    Dashboard user interface class
    Handles all UI components, visualizations, and user interactions
    """

    def __init__(self):
        self.analytics = GovernmentServiceAnalytics()
        self.setup_page_config()
        self.setup_custom_css()

    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Government Service Analytics Dashboard",
            page_icon="🏛️",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def setup_custom_css(self):
        """Setup custom CSS styling with improved text visibility"""
        st.markdown(
            """
        <style>
            .main-header {
                font-size: 2.5rem;
                color: #1f4e79;
                text-align: center;
                margin-bottom: 2rem;
                font-weight: bold;
            }
            .metric-card {
                background-color: #f0f2f6;
                padding: 1rem;
                border-radius: 0.5rem;
                border-left: 5px solid #1f4e79;
            }
            .insight-box {
                background-color: #e8f4f8;
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 1rem 0;
            }
            .stMetric {
                background-color: white;
                padding: 1rem;
                border-radius: 0.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            /* Improve metric text visibility */
            .stMetric > div {
                background-color: white !important;
            }
            .stMetric label {
                font-size: 0.9rem !important;
                color: #262730 !important;
                font-weight: 600 !important;
            }
            .stMetric .metric-value {
                font-size: 1.8rem !important;
                font-weight: 700 !important;
                color: #262730 !important;
            }
            .stMetric .metric-delta {
                font-size: 0.8rem !important;
                font-weight: 500 !important;
            }
            /* Ensure delta text is visible */
            [data-testid="metric-container"] {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px;
                margin: 4px 0;
            }
            [data-testid="metric-container"] > div > div {
                color: #262730 !important;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

    def render_header(self):
        """Render dashboard header"""
        st.markdown(
            '<h1 class="main-header">🏛️ Government Service Efficiency & Citizen Satisfaction Analytics</h1>',
            unsafe_allow_html=True,
        )
        st.markdown("**Dashboard for Sri Lankan Government Service Performance Analysis**")
        st.markdown("---")

    def render_data_loading_section(self):
        """Handle data loading with user feedback"""
        success, message = self.analytics.load_data()

        if not success:
            st.error(f"❌ {message}")
            st.info("Please ensure all CSV files are in the same directory as this script:")
            st.code(
                """
            Required files:
            • citizen_complaints.csv
            • employee_performance.csv  
            • social_media_sentiment.csv
            • department_summary.csv
            """
            )
            st.stop()

        # Show data summary
        data_summary = self.analytics.get_data_summary()
        with st.expander("📊 Dataset Overview", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Complaints", f"{data_summary['complaints_count']:,}")
            with col2:
                st.metric("Employees", f"{data_summary['employees_count']:,}")
            with col3:
                st.metric("Social Posts", f"{data_summary['sentiment_posts']:,}")
            with col4:
                st.metric("Departments", f"{data_summary['departments_count']:,}")

        return True

    def render_sidebar_filters(self):
        """Render sidebar filters and return selected values (REMOVED DATE RANGE)"""
        st.sidebar.header("🔍 Filters")

        # Get unique values for filters
        departments, districts = self.analytics.get_unique_values()

        # Department filter with default selection
        selected_departments = st.sidebar.multiselect(
            "Select Departments:",
            options=departments,
            default=departments,
            help="Filter data by specific government departments"
        )

        # District filter with default selection
        selected_districts = st.sidebar.multiselect(
            "Select Districts:",
            options=districts,
            default=districts,
            help="Filter data by specific districts/regions"
        )

        return selected_departments, selected_districts

    def render_kpi_section(self, complaints_df):
        """Render KPI metrics with improved visibility and formatting"""
        kpis = self.analytics.get_kpi_metrics(complaints_df)

        st.subheader("📈 Key Performance Indicators")
        
        # Use 4 columns with better spacing
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Total complaints with clear resolved count
            resolved_count = kpis.get('resolved_complaints', 0)
            st.metric(
                label="📋 Total Complaints",
                value=f"{kpis['total_complaints']:,}",
                delta=f"{resolved_count:,} resolved"
            )
        
        with col2:
            # Resolution rate with clear target status
            resolution_rate = kpis.get('resolution_rate', 0)
            target_met = resolution_rate >= 85
            if target_met:
                delta_text = "✅ Meets target"
                delta_color = "normal"
            else:
                delta_text = "❌ Below target"
                delta_color = "inverse"
            
            st.metric(
                label="✅ Resolution Rate",
                value=f"{resolution_rate:.1f}%",
                delta=delta_text,
                delta_color=delta_color
            )
        
        with col3:
            # Satisfaction with clear rating
            satisfaction = kpis.get('avg_satisfaction', 0)
            if satisfaction >= 4:
                rating = "Excellent"
                delta_color = "normal"
            elif satisfaction >= 3:
                rating = "Good"
                delta_color = "normal"
            else:
                rating = "Poor"
                delta_color = "inverse"
            
            st.metric(
                label="😊 Satisfaction",
                value=f"{satisfaction:.1f}/5",
                delta=f"{rating} rating",
                delta_color=delta_color
            )
        
        with col4:
            # Resolution time with clear target comparison
            resolution_time = kpis.get('avg_resolution_time', 0)
            target_met = resolution_time <= 15
            if target_met:
                delta_text = "✅ Within target"
                delta_color = "normal"
            else:
                delta_text = "⚠️ Exceeds target"
                delta_color = "inverse"
            
            st.metric(
                label="⏱️ Resolution Time",
                value=f"{resolution_time:.0f} days",
                delta=delta_text,
                delta_color=delta_color
            )

    def render_department_section(self, complaints_df):
        """Render department performance section"""
        st.subheader("🏢 Department Performance Analysis")

        dept_analysis = self.analytics.analyze_department_performance(complaints_df)

        if dept_analysis.empty:
            st.warning("No department data available with current filters.")
            return

        # Show department rankings table
        st.markdown("### 🏆 Department Performance Rankings")
        
        # Format the display table
        display_df = dept_analysis.copy()
        display_df = display_df.rename(columns={
            'rank': 'Rank',
            'department': 'Department',
            'avg_satisfaction': 'Satisfaction (1-5)',
            'avg_resolution_time': 'Resolution Time (Days)',
            'total_complaints': 'Total Complaints',
            'efficiency_score': 'Efficiency Score',
            'performance_category': 'Performance'
        })
        
        # Round efficiency score for display
        display_df['Efficiency Score'] = display_df['Efficiency Score'].round(3)
        
        st.dataframe(
            display_df[['Rank', 'Department', 'Satisfaction (1-5)', 'Resolution Time (Days)', 
                       'Total Complaints', 'Efficiency Score', 'Performance']],
            use_container_width=True,
            hide_index=True
        )

        # Visualization charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Satisfaction bar chart
            fig_satisfaction = px.bar(
                dept_analysis,
                x="avg_satisfaction",
                y="department",
                orientation='h',
                color="avg_satisfaction",
                color_continuous_scale='RdYlGn',
                title="Average Satisfaction by Department",
                text="avg_satisfaction"
            )
            fig_satisfaction.update_layout(yaxis={'categoryorder': 'total ascending'})
            fig_satisfaction.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            st.plotly_chart(fig_satisfaction, use_container_width=True)

        with col2:
            # Efficiency score chart
            fig_efficiency = px.bar(
                dept_analysis,
                x="efficiency_score",
                y="department",
                orientation='h',
                color="performance_category",
                title="Department Efficiency Scores",
                text="efficiency_score"
            )
            fig_efficiency.update_layout(yaxis={'categoryorder': 'total ascending'})
            fig_efficiency.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            st.plotly_chart(fig_efficiency, use_container_width=True)

    def render_complaint_patterns(self, complaints_df):
        """Render complaint patterns section"""
        st.subheader("📌 Complaint Analysis & Trends")

        category_distribution, satisfaction_distribution, monthly_trends = (
            self.analytics.analyze_complaint_patterns(complaints_df)
        )

        col1, col2 = st.columns(2)
        
        with col1:
            # Complaint categories pie chart
            if category_distribution:
                fig = px.pie(
                    names=list(category_distribution.keys()),
                    values=list(category_distribution.values()),
                    title="Distribution of Complaint Categories"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No complaint category data available")
        
        with col2:
            # Satisfaction distribution
            if satisfaction_distribution:
                fig = px.bar(
                    x=list(satisfaction_distribution.keys()),
                    y=list(satisfaction_distribution.values()),
                    title="Satisfaction Score Distribution",
                    labels={'x': 'Satisfaction Score', 'y': 'Number of Complaints'},
                    color=list(satisfaction_distribution.values()),
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No satisfaction data available")

        # Monthly trends
        if not monthly_trends.empty and len(monthly_trends) > 1:
            st.subheader("📅 Monthly Trends")
            
            fig = px.line(
                monthly_trends,
                x="month",
                y="complaint_count",
                title="Monthly Complaint Volume",
                markers=True,
                line_shape='spline'
            )
            fig.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

    def render_sentiment_section(self, sentiment_df):
        """Render sentiment analysis section"""
        st.subheader("💬 Social Media Sentiment Analysis")

        if sentiment_df.empty:
            st.warning("No social media sentiment data available with current filters.")
            return

        sentiment_distribution, dept_sentiment = self.analytics.analyze_sentiment_data(sentiment_df)

        col1, col2 = st.columns(2)
        
        with col1:
            # Overall sentiment distribution
            if sentiment_distribution:
                colors = {'Positive': '#2E8B57', 'Negative': '#DC143C', 'Neutral': '#FFD700'}
                fig = px.pie(
                    names=list(sentiment_distribution.keys()),
                    values=list(sentiment_distribution.values()),
                    title="Overall Sentiment Distribution",
                    color=list(sentiment_distribution.keys()),
                    color_discrete_map=colors
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Department-wise sentiment
            if not dept_sentiment.empty:
                colors = {'Positive': '#2E8B57', 'Negative': '#DC143C', 'Neutral': '#FFD700'}
                fig = px.bar(
                    dept_sentiment,
                    x="department",
                    y="count",
                    color="sentiment_label",
                    title="Sentiment by Department",
                    color_discrete_map=colors,
                    barmode='stack'
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

        # Sentiment summary metrics
        if sentiment_distribution:
            total_posts = sum(sentiment_distribution.values())
            positive_rate = (sentiment_distribution.get('Positive', 0) / total_posts) * 100
            negative_rate = (sentiment_distribution.get('Negative', 0) / total_posts) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📱 Total Posts", f"{total_posts:,}")
            with col2:
                st.metric("👍 Positive Rate", f"{positive_rate:.1f}%")
            with col3:
                st.metric("👎 Negative Rate", f"{negative_rate:.1f}%")

    def render_insights_section(self, complaints_df):
        """Render insights and recommendations section"""
        st.subheader("💡 Key Insights & Recommendations")

        insights = self.analytics.generate_insights_and_recommendations(complaints_df)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔍 Key Findings")
            for finding in insights["key_findings"]:
                st.markdown(f"• {finding}")

        with col2:
            st.markdown("### 🎯 Recommendations")
            for rec in insights["recommendations"]:
                st.markdown(f"• {rec}")

        # Action items table
        if isinstance(insights["action_items"], pd.DataFrame) and not insights["action_items"].empty:
            st.markdown("### 📋 Priority Action Items")
            
            # Add priority emojis for better visualization
            action_items_display = insights["action_items"].copy()
            priority_emojis = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
            action_items_display['Priority'] = action_items_display['priority'].map(priority_emojis) + ' ' + action_items_display['priority']
            
            # Rename columns for display
            action_items_display = action_items_display.rename(columns={
                'action': 'Action',
                'timeline': 'Timeline',
                'expected_impact': 'Expected Impact'
            })[['Priority', 'Action', 'Timeline', 'Expected Impact']]
            
            st.dataframe(action_items_display, use_container_width=True, hide_index=True)

    def render_sidebar_data_info(self, filtered_complaints, filtered_sentiment):
        """Render filtered data information in sidebar"""
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Filtered Data Summary")
        st.sidebar.markdown(f"**Complaints:** {len(filtered_complaints):,}")
        st.sidebar.markdown(f"**Social Media Posts:** {len(filtered_sentiment):,}")
        
        if len(filtered_complaints) > 0:
            resolution_rate = (len(filtered_complaints[filtered_complaints['status'] == 'Resolved']) / len(filtered_complaints)) * 100
            st.sidebar.markdown(f"**Resolution Rate:** {resolution_rate:.1f}%")

    def run(self):
        """Run the full dashboard"""
        self.render_header()

        if not self.render_data_loading_section():
            return

        # Get filters (REMOVED DATE RANGE)
        departments, districts = self.render_sidebar_filters()

        # Filter data (REMOVED DATE RANGE PARAMETER)
        complaints_df, sentiment_df = self.analytics.filter_data(
            departments=departments,
            districts=districts,
            date_range=None
        )

        # Show filtered data info in sidebar
        self.render_sidebar_data_info(complaints_df, sentiment_df)

        # Main dashboard sections
        self.render_kpi_section(complaints_df)
        st.markdown("---")
        
        self.render_department_section(complaints_df)
        st.markdown("---")
        
        # REMOVED: self.render_regional_section(complaints_df)
        
        self.render_complaint_patterns(complaints_df)
        st.markdown("---")
        
        self.render_sentiment_section(sentiment_df)
        st.markdown("---")
        
        self.render_insights_section(complaints_df)

        # Footer
        st.markdown("---")
        st.markdown("**Dashboard created for Government Service Analytics Assignment**")
        st.markdown("*Data is simulated for demonstration purposes*")


def main():
    """Main function to run the dashboard"""
    dashboard = DashboardUI()
    dashboard.run()


if __name__ == "__main__":
    main()