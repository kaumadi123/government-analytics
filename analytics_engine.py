"""
Government Service Analytics Engine
Handles all data processing, analysis, and insight generation
Separate from UI components for better code organization
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class GovernmentServiceAnalytics:
    """
    Core analytics engine for Government Service Efficiency & Citizen Satisfaction Analysis
    """
    
    def __init__(self):
        self.complaints_df = None
        self.employee_df = None
        self.sentiment_df = None
        self.department_df = None
        self.is_data_loaded = False
        
    def load_data(self, complaints_file='citizen_complaints.csv', 
                  employee_file='employee_performance.csv',
                  sentiment_file='social_media_sentiment.csv', 
                  department_file='department_summary.csv'):
        """Load all datasets from CSV files"""
        try:
            # Load datasets
            self.complaints_df = pd.read_csv(complaints_file)
            self.employee_df = pd.read_csv(employee_file)
            self.sentiment_df = pd.read_csv(sentiment_file)
            self.department_df = pd.read_csv(department_file)
            
            # Convert date columns
            self.complaints_df['complaint_date'] = pd.to_datetime(self.complaints_df['complaint_date'])
            self.complaints_df['resolution_date'] = pd.to_datetime(self.complaints_df['resolution_date'])
            self.sentiment_df['post_date'] = pd.to_datetime(self.sentiment_df['post_date'])
            
            self.is_data_loaded = True
            return True, "Data loaded successfully"
            
        except Exception as e:
            self.is_data_loaded = False
            return False, f"Error loading data: {str(e)}"
    
    def get_kpi_metrics(self, complaints_df=None):
        """Calculate key performance indicators"""
        if complaints_df is None:
            complaints_df = self.complaints_df
            
        if complaints_df is None or len(complaints_df) == 0:
            return {
                'total_complaints': 0,
                'resolved_complaints': 0,
                'resolution_rate': 0,
                'avg_satisfaction': 0,
                'avg_resolution_time': 0
            }
        
        total_complaints = len(complaints_df)
        resolved_complaints = len(complaints_df[complaints_df['status'] == 'Resolved'])
        resolution_rate = (resolved_complaints / total_complaints) * 100 if total_complaints > 0 else 0
        avg_satisfaction = complaints_df['satisfaction_score'].mean()
        
        resolved_df = complaints_df[complaints_df['status'] == 'Resolved']
        avg_resolution_time = resolved_df['resolution_time_days'].mean() if len(resolved_df) > 0 else 0
        
        return {
            'total_complaints': total_complaints,
            'resolved_complaints': resolved_complaints,
            'resolution_rate': round(resolution_rate, 1),
            'avg_satisfaction': round(avg_satisfaction, 1) if not pd.isna(avg_satisfaction) else 0,
            'avg_resolution_time': round(avg_resolution_time, 1) if not pd.isna(avg_resolution_time) else 0
        }
    
    def analyze_department_performance(self, complaints_df=None):
        """Analyze performance by department with efficiency scoring"""
        if complaints_df is None:
            complaints_df = self.complaints_df
            
        if complaints_df is None or len(complaints_df) == 0:
            return pd.DataFrame()
        
        # Group by department and calculate metrics
        dept_analysis = complaints_df.groupby('department').agg({
            'complaint_id': 'count',
            'satisfaction_score': 'mean',
            'resolution_time_days': 'mean'
        }).reset_index()
        
        dept_analysis.columns = ['department', 'total_complaints', 'avg_satisfaction', 'avg_resolution_time']
        dept_analysis = dept_analysis.round(2)
        
        # Calculate efficiency score (composite metric)
        max_resolution_time = dept_analysis['avg_resolution_time'].max()
        if max_resolution_time > 0:
            # Satisfaction weight: 60%, Speed weight: 40%
            dept_analysis['efficiency_score'] = (
                (dept_analysis['avg_satisfaction'] / 5) * 0.6 +
                (1 - (dept_analysis['avg_resolution_time'] / max_resolution_time)) * 0.4
            )
        else:
            dept_analysis['efficiency_score'] = dept_analysis['avg_satisfaction'] / 5
        
        # Sort by efficiency score and add ranking
        dept_analysis = dept_analysis.sort_values('efficiency_score', ascending=False)
        dept_analysis['rank'] = range(1, len(dept_analysis) + 1)
        
        # Add performance categories
        dept_analysis['performance_category'] = dept_analysis['efficiency_score'].apply(
            lambda x: 'Excellent' if x > 0.8 else 'Good' if x > 0.6 else 'Needs Improvement'
        )
        
        dept_analysis['performance_emoji'] = dept_analysis['performance_category'].apply(
            lambda x: '🏆' if x == 'Excellent' else '👍' if x == 'Good' else '⚠️'
        )
        
        return dept_analysis
    
    def analyze_regional_performance(self, complaints_df=None):
        """Analyze performance by district/region"""
        if complaints_df is None:
            complaints_df = self.complaints_df
            
        if complaints_df is None or len(complaints_df) == 0:
            return pd.DataFrame()
        
        regional_analysis = complaints_df.groupby('district').agg({
            'complaint_id': 'count',
            'satisfaction_score': 'mean',
            'resolution_time_days': 'mean'
        }).reset_index()
        
        regional_analysis.columns = ['district', 'total_complaints', 'avg_satisfaction', 'avg_resolution_time']
        regional_analysis = regional_analysis.round(2)
        
        return regional_analysis
    
    def analyze_complaint_patterns(self, complaints_df=None):
        """Analyze complaint categories and patterns"""
        if complaints_df is None:
            complaints_df = self.complaints_df
            
        if complaints_df is None or len(complaints_df) == 0:
            return {}, {}, pd.DataFrame()
        
        # Complaint category distribution
        category_distribution = {}
        if 'complaint_category' in complaints_df.columns:
            category_distribution = complaints_df['complaint_category'].value_counts().to_dict()
        
        # Satisfaction score distribution
        satisfaction_distribution = complaints_df['satisfaction_score'].value_counts().sort_index().to_dict()
        
        # Monthly trends
        monthly_trends = pd.DataFrame()
        if len(complaints_df) > 0:
            complaints_df_copy = complaints_df.copy()
            complaints_df_copy['month'] = complaints_df_copy['complaint_date'].dt.to_period('M').astype(str)
            monthly_trends = complaints_df_copy.groupby('month').agg({
                'complaint_id': 'count',
                'satisfaction_score': 'mean'
            }).reset_index()
            monthly_trends.columns = ['month', 'complaint_count', 'avg_satisfaction']
            monthly_trends = monthly_trends.round(2)
        
        return category_distribution, satisfaction_distribution, monthly_trends
    
    def analyze_sentiment_data(self, sentiment_df=None):
        """Analyze social media sentiment patterns"""
        if sentiment_df is None:
            sentiment_df = self.sentiment_df
            
        if sentiment_df is None or len(sentiment_df) == 0:
            return {}, pd.DataFrame()
        
        # Overall sentiment distribution
        sentiment_distribution = sentiment_df['sentiment_label'].value_counts().to_dict()
        
        # Sentiment by department
        dept_sentiment = sentiment_df.groupby(['department', 'sentiment_label']).size().reset_index(name='count')
        
        return sentiment_distribution, dept_sentiment
    
    def generate_insights_and_recommendations(self, complaints_df=None, dept_analysis=None):
        """Generate automated insights and actionable recommendations"""
        if complaints_df is None:
            complaints_df = self.complaints_df
        if dept_analysis is None:
            dept_analysis = self.analyze_department_performance(complaints_df)
            
        insights = {
            'key_findings': [],
            'recommendations': [],
            'action_items': []
        }
        
        if complaints_df is None or len(complaints_df) == 0:
            return insights
        
        # Calculate key metrics
        kpis = self.get_kpi_metrics(complaints_df)
        
        # Key findings
        insights['key_findings'] = [
            f"Total of {kpis['total_complaints']:,} complaints processed",
            f"Average citizen satisfaction: {kpis['avg_satisfaction']}/5",
            f"Resolution rate: {kpis['resolution_rate']}%",
            f"Average resolution time: {kpis['avg_resolution_time']} days"
        ]
        
        # Add top complaint type if available
        if 'complaint_category' in complaints_df.columns and not complaints_df['complaint_category'].empty:
            top_complaint = complaints_df['complaint_category'].mode()
            if len(top_complaint) > 0:
                insights['key_findings'].append(f"Most common complaint: {top_complaint.iloc[0]}")
        
        # Add department performance insights
        if len(dept_analysis) > 0:
            best_dept = dept_analysis.iloc[0]['department']
            worst_dept = dept_analysis.iloc[-1]['department']
            insights['key_findings'].extend([
                f"Best performing department: {best_dept}",
                f"Department needing attention: {worst_dept}"
            ])
        
        # Generate recommendations based on data
        insights['recommendations'] = [
            "Implement online appointment systems to reduce queue times",
            "Conduct staff training focused on customer service excellence",
            "Digitize more services to reduce physical office visits",
            "Share best practices from top-performing departments",
            "Establish real-time performance monitoring systems",
            "Create streamlined citizen feedback collection mechanisms"
        ]
        
        # Generate action items with priorities
        action_items_data = []
        if len(dept_analysis) > 0:
            worst_dept = dept_analysis.iloc[-1]['department']
            action_items_data.append({
                'priority': 'High',
                'action': f'Address performance issues in {worst_dept}',
                'timeline': '1 month',
                'expected_impact': 'High'
            })
        
        # Add complaint-specific action if data available
        if 'complaint_category' in complaints_df.columns and not complaints_df['complaint_category'].empty:
            top_complaint = complaints_df['complaint_category'].mode()
            if len(top_complaint) > 0:
                action_items_data.append({
                    'priority': 'Medium',
                    'action': f'Implement solutions for {top_complaint.iloc[0]} issues',
                    'timeline': '2 months', 
                    'expected_impact': 'Medium'
                })
        
        # Add standard action items
        action_items_data.extend([
            {
                'priority': 'Medium',
                'action': 'Launch comprehensive staff training program',
                'timeline': '3 months',
                'expected_impact': 'High'
            },
            {
                'priority': 'Low',
                'action': 'Expand digital service offerings',
                'timeline': '6 months',
                'expected_impact': 'Medium'
            }
        ])
        
        insights['action_items'] = pd.DataFrame(action_items_data)
        
        return insights
    
    def filter_data(self, departments=None, districts=None, date_range=None):
        """Filter datasets based on user selections"""
        if not self.is_data_loaded:
            return None, None
        
        filtered_complaints = self.complaints_df.copy()
        filtered_sentiment = self.sentiment_df.copy()
        
        # Apply department filter
        if departments and len(departments) > 0:
            filtered_complaints = filtered_complaints[filtered_complaints['department'].isin(departments)]
            filtered_sentiment = filtered_sentiment[filtered_sentiment['department'].isin(departments)]
        
        # Apply district filter
        if districts and len(districts) > 0:
            filtered_complaints = filtered_complaints[filtered_complaints['district'].isin(districts)]
            filtered_sentiment = filtered_sentiment[filtered_sentiment['district'].isin(districts)]
        
        # Apply date filter
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_complaints = filtered_complaints[
                (filtered_complaints['complaint_date'] >= pd.to_datetime(start_date)) &
                (filtered_complaints['complaint_date'] <= pd.to_datetime(end_date))
            ]
            filtered_sentiment = filtered_sentiment[
                (filtered_sentiment['post_date'] >= pd.to_datetime(start_date)) &
                (filtered_sentiment['post_date'] <= pd.to_datetime(end_date))
            ]
        
        return filtered_complaints, filtered_sentiment
    
    def get_unique_values(self):
        """Get unique values for filter dropdowns"""
        if not self.is_data_loaded:
            return [], []
        
        departments = sorted(self.complaints_df['department'].unique().tolist())
        districts = sorted(self.complaints_df['district'].unique().tolist())
        
        return departments, districts
    
    def get_data_summary(self):
        """Get summary statistics about the loaded datasets"""
        if not self.is_data_loaded:
            return {}
        
        return {
            'complaints_count': len(self.complaints_df),
            'employees_count': len(self.employee_df),
            'sentiment_posts': len(self.sentiment_df),
            'departments_count': len(self.department_df),
            'date_range': {
                'start': self.complaints_df['complaint_date'].min().strftime('%Y-%m-%d'),
                'end': self.complaints_df['complaint_date'].max().strftime('%Y-%m-%d')
            }
        }

# Utility functions for testing
def test_analytics_engine():
    """Test function to verify analytics engine works correctly"""
    print("🧪 Testing Government Service Analytics Engine...")
    
    # Initialize engine
    analytics = GovernmentServiceAnalytics()
    
    # Load data
    success, message = analytics.load_data()
    print(f"Data Loading: {'✅' if success else '❌'} {message}")
    
    if success:
        # Test KPI calculation
        kpis = analytics.get_kpi_metrics()
        print(f"KPIs calculated: {kpis}")
        
        # Test department analysis
        dept_analysis = analytics.analyze_department_performance()
        print(f"Department analysis: {len(dept_analysis)} departments analyzed")
        
        # Test insights generation
        insights = analytics.generate_insights_and_recommendations()
        print(f"Insights generated: {len(insights['key_findings'])} findings, {len(insights['recommendations'])} recommendations")
        
        print("✅ Analytics engine test completed successfully!")
    else:
        print("❌ Analytics engine test failed - could not load data")

if __name__ == "__main__":
    test_analytics_engine()