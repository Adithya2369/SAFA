import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


# Functions used:
# Function to create the dictionary of all the reviews. Later can be used to pass this as an argument to other functions
def get_data():
    df = pd.read_excel('uploads/TestData.xlsx')
    # Extract the 'text' column and convert to a dictionary
    text_column = df['Text']
    text_dict = text_column.to_dict()
    return text_dict

# Function to summarize that have been retrieved from the uploaded document
def summarize_reviews(text_dict):
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mistral-saba-24b")

    # Define the system and human messages
    system = "You are an AI system designed to process and summarize text. You will receive a Python dictionary where each key represents an index, and its value is a detailed review. Your task is to process this dictionary and return a new dictionary (give only dictionary donot add any other responses) with the same keys, where each value is a concise summary of the corresponding review. The summaries should be very concise, retaining the core meaning of the original review, including key insights, sentiment, and main points. Each summary should be objective, unbiased, and free from emotional or subjective language and enclosed in double quotes as strings for further programming use."
    human_reviews = "\n".join(f"{key}: {value}" for key, value in text_dict.items())
    human = "{text}"

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    # Invoke the chain with the required input
    chain = prompt | chat
    response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
    res = response.content
    return res

# Function to analyse the summaries and provide a single summarized report of all the reviews
def perform_analysis(text_dict):
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mistral-saba-24b")

    # Define the system and human messages
    system = "You are a business analyst. Based on the given reviews, write a summary report highlighting the key points. If you feel like the data which you get is not at all related to reviews, just return this statement - 'PLEASE CROSS CHECK THE FILE YOU UPLOADED'"
    human_reviews = "\n".join(text_dict.values())  # Join the dictionary values
    human = "{text}"

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    # Invoke the chain with the required input
    chain = prompt | chat
    response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
    result = response.content
    return result


# Function to suggest improvements based on the customer feedback
def suggested_improvements(text_dict):
# Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mistral-saba-24b")

    # Define the system and human messages
    system = "You are a quality assurance consultant. Based on the given client reviews, pinpoint the key areas that require improvement. Focus on identifying issues and suggesting strategies to enhance overall customer satisfaction and product quality. If you feel like the data which you get is not at all related to reviews, just return this statement - 'PLEASE CROSS CHECK THE FILE YOU UPLOADED'"
    human_reviews = "\n".join(text_dict.values())  # Join the dictionary values
    human = "{text}"

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    # Invoke the chain with the required input
    chain = prompt | chat
    response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
    result = response.content
    return result




def Sentiment_analysis(text_dict):
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mistral-saba-24b")

    # Define the system and human messages
    system = "You are an AI system designed to analyze and classify text. You will receive a Python dictionary where each key represents an index, and its value is a detailed review. Your task is to process this dictionary and return a new dictionary (give only dictionary, do not add any other responses) with the same keys, where each value is the sentiment of the corresponding review. The sentiment should be classified as 'Positive,' 'Negative,' or 'Neutral' and enclosed in double quotes as strings for further programming use."
    human_reviews = "\n".join(f"{key}: {value}" for key, value in text_dict.items())
    human = "{text}"

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    # Invoke the chain with the required input
    chain = prompt | chat
    response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
    res = response.content
    return res