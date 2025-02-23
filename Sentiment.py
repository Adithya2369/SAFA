#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip show transformers
from transformers import pipeline


# In[ ]:


# Load RoBERTa-based sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")


# In[ ]:


# Load Excel file
file_path = 'customer_reviews_feedback.xlsx'  # Replace with your Excel file path
df = pd.read_excel(file_path)

# Check if the 'text' column exists
if 'text' not in df.columns:
    raise ValueError("The column 'text' is not found in the provided Excel file.")


# In[ ]:


# Dictionary to store sentiment scores
sentiment_dict = {}

# Maximum token length for the RoBERTa model
max_length = 512

# Analyze sentiment and store results
sentiment_results = []

for idx, text in enumerate(df['text']):
    if isinstance(text, str) and text.strip():
        # Truncate text if it's too long for the model
        truncated_text = text[:max_length]
        result = sentiment_pipeline(truncated_text)[0]
        label = result['label'].lower()
        if label == 'negative':
            sentiment_results.append('Negative')
        elif label == 'positive':
            sentiment_results.append('Positive')
        else:
            sentiment_results.append('Neutral')
        sentiment_dict[idx] = {
            'positive': result['score'] if label == 'positive' else 0.0,
            'negative': result['score'] if label == 'negative' else 0.0,
            'neutral': result['score'] if label == 'neutral' else 0.0,
            'compound': result['score']
        }
    else:
        sentiment_results.append('No Data')  # Handle empty or non-string entries
        sentiment_dict[idx] = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0, 'compound': 0.0}


# In[ ]:


# Add new column to DataFrame
df['Sentiment'] = sentiment_results

# Save the updated DataFrame to a new Excel file
output_file_path = 'output_with_sentiment.xlsx'  # Replace with your desired output file path
df.to_excel(output_file_path, index=False)

print(f"Sentiment analysis complete. Results saved to '{output_file_path}'.")


# In[ ]:




