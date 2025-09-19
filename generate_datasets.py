import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define Sri Lankan government departments and districts
departments = [
    'Department of Motor Traffic', 'Registrar General Department', 
    'Department of Immigration', 'Inland Revenue Department',
    'Department of Pensions', 'Department of Census and Statistics',
    'Department of Health Services', 'Department of Education',
    'Provincial Council Secretariat', 'Divisional Secretariat',
    'Municipal Council', 'Pradeshiya Sabha'
]

districts = [
    'Colombo', 'Gampaha', 'Kalutara', 'Kandy', 'Matale', 'Nuwara Eliya',
    'Galle', 'Matara', 'Hambantota', 'Jaffna', 'Kilinochhi', 'Mannar',
    'Vavuniya', 'Mullaitivu', 'Batticaloa', 'Ampara', 'Trincomalee',
    'Kurunegala', 'Puttalam', 'Anuradhapura', 'Polonnaruwa', 'Badulla',
    'Monaragala', 'Ratnapura', 'Kegalle'
]

service_types = [
    'License Renewal', 'Birth Certificate', 'Marriage Certificate',
    'Passport Application', 'Visa Processing', 'Tax Filing',
    'Pension Claims', 'Land Registration', 'Business Registration',
    'School Admission', 'Medical Certificate', 'Police Report'
]

complaint_categories = [
    'Long Queue', 'Delayed Processing', 'Rude Staff Behavior',
    'Bribery Demand', 'Incorrect Information', 'System Downtime',
    'Missing Documents', 'Overcharging', 'Protocol Violation',
    'Poor Facility Condition'
]

# Generate Citizen Complaints Dataset
def generate_complaints_data(n_records=5000):
    complaints_data = []
    
    for i in range(n_records):
        # Generate random date within last 2 years
        start_date = datetime.now() - timedelta(days=730)
        random_days = random.randint(0, 730)
        complaint_date = start_date + timedelta(days=random_days)
        
        # Resolution date (some complaints still pending)
        if random.random() > 0.15:  # 85% resolved
            resolution_days = random.randint(1, 180)
            resolution_date = complaint_date + timedelta(days=resolution_days)
            status = 'Resolved'
            resolution_time = resolution_days
        else:
            resolution_date = None
            status = 'Pending'
            resolution_time = (datetime.now() - complaint_date).days
        
        # Satisfaction score (1-5, higher for resolved complaints)
        if status == 'Resolved':
            satisfaction = random.choices([1,2,3,4,5], weights=[10,15,25,30,20])[0]
        else:
            satisfaction = random.choices([1,2,3,4,5], weights=[40,30,20,8,2])[0]
        
        complaint = {
            'complaint_id': f'C{i+1:06d}',
            'department': random.choice(departments),
            'district': random.choice(districts),
            'service_type': random.choice(service_types),
            'complaint_category': random.choice(complaint_categories),
            'complaint_date': complaint_date.strftime('%Y-%m-%d'),
            'resolution_date': resolution_date.strftime('%Y-%m-%d') if resolution_date else None,
            'resolution_time_days': resolution_time,
            'status': status,
            'satisfaction_score': satisfaction,
            'priority': random.choices(['Low', 'Medium', 'High'], weights=[50, 35, 15])[0]
        }
        complaints_data.append(complaint)
    
    return pd.DataFrame(complaints_data)

# Generate Employee Performance Dataset
def generate_employee_data(n_employees=500):
    employee_data = []
    
    for i in range(n_employees):
        dept = random.choice(departments)
        
        # Performance varies by department (some are naturally more efficient)
        if dept in ['Department of Motor Traffic', 'Registrar General Department']:
            efficiency_base = 0.7
        elif dept in ['Department of Immigration', 'Inland Revenue Department']:
            efficiency_base = 0.8
        else:
            efficiency_base = 0.75
        
        # Generate performance metrics
        cases_per_day = max(5, int(np.random.normal(25, 8)))
        avg_processing_time = max(15, int(np.random.normal(60, 20)))  # minutes
        attendance_rate = min(100, max(60, np.random.normal(efficiency_base * 100, 10)))
        violations = max(0, int(np.random.poisson(2 * (1 - efficiency_base))))
        
        employee = {
            'employee_id': f'E{i+1:05d}',
            'department': dept,
            'district': random.choice(districts),
            'cases_handled_per_day': cases_per_day,
            'avg_processing_time_minutes': avg_processing_time,
            'attendance_rate_percent': round(attendance_rate, 1),
            'protocol_violations': violations,
            'years_of_service': random.randint(1, 25),
            'efficiency_rating': round(min(5, max(1, np.random.normal(efficiency_base * 5, 0.8))), 1)
        }
        employee_data.append(employee)
    
    return pd.DataFrame(employee_data)

# Generate Social Media Sentiment Dataset
def generate_sentiment_data(n_posts=2000):
    sentiment_data = []
    
    positive_keywords = ['excellent', 'fast', 'helpful', 'efficient', 'satisfied', 'good service']
    negative_keywords = ['terrible', 'slow', 'corrupt', 'waste of time', 'frustrated', 'unprofessional']
    neutral_keywords = ['okay', 'average', 'normal', 'standard', 'typical']
    
    for i in range(n_posts):
        sentiment_label = random.choices(['Positive', 'Negative', 'Neutral'], weights=[20, 50, 30])[0]
        
        # Generate sample text based on sentiment
        if sentiment_label == 'Positive':
            sample_text = f"Service at {random.choice(departments)} was {random.choice(positive_keywords)}"
        elif sentiment_label == 'Negative':
            sample_text = f"{random.choice(departments)} service is {random.choice(negative_keywords)}"
        else:
            sample_text = f"Experience with {random.choice(departments)} was {random.choice(neutral_keywords)}"
        
        # Generate date within last year
        post_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        sentiment = {
            'post_id': f'P{i+1:06d}',
            'department': random.choice(departments),
            'district': random.choice(districts),
            'post_date': post_date.strftime('%Y-%m-%d'),
            'sentiment_label': sentiment_label,
            'sentiment_score': round(random.uniform(-1, 1), 3),
            'sample_text': sample_text,
            'platform': random.choice(['Twitter', 'Facebook', 'Instagram'])
        }
        sentiment_data.append(sentiment)
    
    return pd.DataFrame(sentiment_data)

# Generate Department Summary Dataset
def generate_department_summary():
    dept_summary = []
    
    for dept in departments:
        # Calculate some aggregate metrics
        total_complaints = random.randint(150, 500)
        resolved_complaints = int(total_complaints * random.uniform(0.7, 0.95))
        avg_resolution_time = random.randint(5, 45)
        avg_satisfaction = round(random.uniform(2.1, 4.2), 1)
        
        summary = {
            'department': dept,
            'total_complaints_last_year': total_complaints,
            'resolved_complaints': resolved_complaints,
            'pending_complaints': total_complaints - resolved_complaints,
            'avg_resolution_time_days': avg_resolution_time,
            'avg_satisfaction_score': avg_satisfaction,
            'total_employees': random.randint(20, 200),
            'efficiency_category': 'High' if avg_satisfaction > 3.5 else 'Medium' if avg_satisfaction > 2.8 else 'Low'
        }
        dept_summary.append(summary)
    
    return pd.DataFrame(dept_summary)

# Generate all datasets
print("Generating Government Service Analytics Datasets...")
print("=" * 50)

complaints_df = generate_complaints_data(5000)
print(f"✓ Generated {len(complaints_df)} complaint records")

employee_df = generate_employee_data(500)
print(f"✓ Generated {len(employee_df)} employee records")

sentiment_df = generate_sentiment_data(2000)
print(f"✓ Generated {len(sentiment_df)} social media sentiment records")

department_df = generate_department_summary()
print(f"✓ Generated {len(department_df)} department summary records")

# Save to CSV files
complaints_df.to_csv('citizen_complaints.csv', index=False)
employee_df.to_csv('employee_performance.csv', index=False)
sentiment_df.to_csv('social_media_sentiment.csv', index=False)
department_df.to_csv('department_summary.csv', index=False)

print("\nDataset files created successfully!")
print("Files: citizen_complaints.csv, employee_performance.csv, social_media_sentiment.csv, department_summary.csv")

# Display sample data
print("\n" + "="*50)
print("SAMPLE DATA PREVIEW")
print("="*50)

print("\n📊 Citizen Complaints Sample:")
print(complaints_df.head(3))

print("\n👥 Employee Performance Sample:")
print(employee_df.head(3))

print("\n📱 Social Media Sentiment Sample:")
print(sentiment_df.head(3))

print("\n🏛️ Department Summary Sample:")
print(department_df.head(3))