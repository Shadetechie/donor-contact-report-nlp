import pandas as pd
import numpy as np
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. Load Raw CSV Data
df = pd.read_csv('contact_reports.csv')

# 2. Define CRM Tag Rules Dictionary
TAG_RULES = {
    'Lassonde_Entrepreneurship': ['lassonde', 'entrepreneurship', 'incubator', 'pitch', 'startup', 'startups', 'prototype'],
    'Underrepresented_Founders': ['black-owned', 'underrepresented', 'diverse', 'dei', 'women in stem', 'first-generation'],
    'HairCare_Beauty_ConsumerTech': ['hair care', 'beauty', 'wellness', 'consumer tech'],
    'Analytics_PublicHealth': ['analytics', 'data science', 'public health', 'ai', 'research assistantships'],
    'Scholarships_Fellowships': ['scholarship', 'scholarships', 'fellowship', 'endowed scholarship'],
    'Capital_Facilities': ['capital', 'building', 'campus tour', 'facility']
}

# 3. Helper Function to Extract CRM Tags
def extract_crm_tags(text):
    text_lower = str(text).lower()
    matched_tags = []
    for tag_name, keywords in TAG_RULES.items():
        if any(keyword in text_lower for keyword in keywords):
            matched_tags.append(tag_name)
    return ", ".join(matched_tags) if matched_tags else "General_Interest"

# Apply tag extraction to the entire dataset
df['Suggested_CRM_Tags'] = df['Contact_Report_Text'].apply(extract_crm_tags)

# 4. Sentiment Analysis Engine (Lexicon-Based)
POSITIVE_WORDS = set(['enthusiastic', 'impressed', 'passionate', 'warm', 'strong', 'supported', 'great', 'interested', 'consider', 'proposal'])
NEGATIVE_WORDS = set(['frustration', 'poor', 'unhappy', 'disconnected', 'hesitation', 'difficult', 'uncertainty', 'hold', 'lack', 'neutral'])

def calculate_sentiment(text):
    words = re.findall(r'\w+', str(text).lower())
    pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)

    total = pos_count + neg_count
    if total == 0:
        score = 0.0
    else:
        score = round((pos_count - neg_count) / total, 2)

    if score > 0.15:
        label = 'Positive'
    elif score < -0.15:
        label = 'Negative (At Risk)'
    else:
        label = 'Neutral'

    return pd.Series([score, label])

# Apply sentiment analysis to the entire dataset
df[['Sentiment_Score', 'Sentiment_Label']] = df['Contact_Report_Text'].apply(calculate_sentiment)

# 5. Save Enriched CSV Dataset
df.to_csv('contact_reports_enriched.csv', index=False)

# 6. Generate and Save WordCloud Visualization
all_text = " ".join(df['Contact_Report_Text'].dropna().tolist())

stopwords_list = set(['met', 'discuss', 'donor', 'expressed', 'interest', 'meeting', 'phone', 'call', 'asked', 'wants', 'would', 'receive', 'via', 'past', 'recent', 'regarding', 'also', 'stated', 'brief', 'local', 'cafe', 'virtual', 'check-in', 'to', 'the', 'in', 'and', 'for', 'a', 'of', 'on', 'with'])

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    stopwords=stopwords_list,
    colormap='viridis',
    max_words=40
).generate(all_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Donor Contact Report Keywords & Affinity Themes', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('donor_interest_wordcloud.png', dpi=300)
plt.close()

# Save image file to folder
plt.savefig('donor_interest_wordcloud.png', dpi=300)

# Add this line to pop up the image window on your screen:
plt.show()



