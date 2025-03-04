from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

# Load the sentiment-analysis pipeline using RoBERTa
hf_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Wrap it in LangChain's HuggingFacePipeline
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# Perform sentiment analysis
text = "I love using Hugging Face with LangChain!"
result = llm.invoke(text)

print(result)
