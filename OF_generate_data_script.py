import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for consistent results
np.random.seed(42)
random.seed(42)

# Config
NUM_REPORTS = 500
START_DATE = datetime(2024, 10, 1)
END_DATE = datetime(2026, 9, 15)

# Helper for random dates across 2-year range
def generate_random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')

# Data Pools
contact_types = ['In-Person Lunch', 'Campus Tour', 'Virtual Call', 'Coffee Meeting', 'Event Reception', 'Phone Call']
Fundraiser = ['GO_101', 'GO_102', 'GO_103', 'GO_104', 'GO_105']

# Constituent ID pool (50 unique donors to create repeat interactions)
constituent_ids = [f"DONOR_{1000 + i}" for i in range(100)]

# Narrative note templates across different sentiment & interest profiles
note_components = [
    # Lassonde & Student Entrepreneurship
    {
        "text": "Met over lunch to discuss student entrepreneurship initiatives. The donor expressed strong interest in supporting Lassonde programs, specifically funding pitch competitions for underrepresented founders and black-owned student startups in hair care and consumer tech. Highly enthusiastic about mentoring undergraduate founders.",
        "capacity": 25000
    },
    {
        "text": "Toured the campus innovation hub. Donor was impressed by student prototype displays. Expressed interest in creating a seed grant pool for student-led startups in sustainable beauty and wellness products. Requested a formal proposal for $50k.",
        "capacity": 50000
    },
    # STEM & Data Analytics
    {
        "text": "Virtual catch-up regarding the new Business Analytics fellowship fund. Donor shared their background in healthcare data analytics and wants to sponsor capstone projects focusing on public health resource allocation. Warm interaction overall.",
        "capacity": 15000
    },
    {
        "text": "Coffee meeting to review annual giving options. Donor asked how AI and data science are being integrated into the curriculum. Would consider a major gift if tied directly to undergraduate research assistantships.",
        "capacity": 30000
    },
    # DEI & Scholarships
    {
        "text": "Met at alumni event reception. Donor spoke passionately about first-generation student scholarships and leadership development programs. Interested in endowing an annual scholarship for women in STEM.",
        "capacity": 100000
    },
    {
        "text": "Phone call to discuss endowed giving. Constituent wants to ensure funding directly benefits diverse student entrepreneurs and underrepresented founders entering local startup accelerators.",
        "capacity": 20000
    },
    # Mixed / Neutral Sentiment
    {
        "text": "Met to discuss campus capital updates. Donor feels slightly disconnected from the university's recent strategic direction. Not interested in general annual fund, but might consider targeted gifts to student incubators if leadership provides clearer ROI metrics.",
        "capacity": 10000
    },
    {
        "text": "Brief phone check-in. Constituent was busy and neutral regarding current campaign priorities. Asked to receive updates via email instead of in-person visits until next spring.",
        "capacity": 5000
    },
    # Hesitant / Negative Sentiment (Pipeline Risk)
    {
        "text": "Difficult meeting at local cafe. Donor expressed frustration over recent event organization and poor communication regarding past gift allocation. Stated they are putting further contributions on hold until receiving an audit of their endowed scholarship fund.",
        "capacity": 50000
    },
    {
        "text": "Virtual call to discuss renewal. Donor cited economic uncertainty and expressed hesitation to commit to a multi-year pledge this fiscal year. Unhappy with lack of personal updates from the college dean.",
        "capacity": 15000
    }
]

# Generate 100 records
records = []
for i in range(1, NUM_REPORTS + 1):
    report_id = f"REP_{2000 + i}"
    constituent_id = random.choice(constituent_ids)
    Fundraiser = random.choice(Fundraiser)
    contact_date = generate_random_date(START_DATE, END_DATE)
    contact_type = random.choice(contact_types)

    # Pick note archetype and add minor natural variance
    archetype = random.choice(note_components)
    note_text = archetype["text"]

    # Randomly vary capacity based on archetype baseline
    capacity_variance = random.choice([0.8, 1.0, 1.2, 1.5])
    est_capacity = int(archetype["capacity"] * capacity_variance)

    records.append({
        'Report_ID': report_id,
        'Constituent_ID': constituent_id,
        'Fundraiser_ID': Fundraiser,
        'Contact_Date': contact_date,
        'Contact_Type': contact_type,
        'Contact_Report_Text': note_text,
        'Est_Gift_Capacity': est_capacity
    })

# Convert to DataFrame
df = pd.DataFrame(records)

# Sort chronologically by date
df['Contact_Date'] = pd.to_datetime(df['Contact_Date'])
df = df.sort_values(by='Contact_Date').reset_index(drop=True)

# Export to CSV
file_name = 'contact_reports.csv'
df.to_csv(file_name, index=False)
print(f"Successfully generated {len(df)} synthetic contact reports saved to '{file_name}'.")

# Preview first 3 rows
print("\nSample Output:")
print(df[['Report_ID', 'Constituent_ID', 'Contact_Date', 'Contact_Type', 'Est_Gift_Capacity']].head(3))
