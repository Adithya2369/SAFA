import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# Set Up Your HuggingFace API Token
HUGGINGFACE_API_TOKEN = 'API token'
os.environ['HUGGINGFACEHUB_API_TOKEN'] = HUGGINGFACE_API_TOKEN

# Loading a Pre-Trained Model from HuggingFace Hub
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# Creating a Function to Run the Application
def run_classification(text):
    result1 = classifier(text)
    return result1

# Running the Application
input_text = "I Product quality is worst. Never buying it again"
result = run_classification(input_text)
print(f"Input: {input_text}")
print(f"Classification: {result}")