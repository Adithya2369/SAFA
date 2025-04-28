import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from io import StringIO

# Functions used:
# Function to create the dictionary of all the reviews. Later can be used to pass this as an argument to other functions
def get_data():
    df = pd.read_excel('uploads/TestData.xlsx')
    # Extract the 'text' column and convert to a dictionary
    text_column = df['Text']
    text_dict = text_column.to_dict()
    return text_dict

def csv_text_to_dataframe(csv_text):
    # Use StringIO to treat the text like a file
    csv_data = StringIO(csv_text)
    # Define the column names manually
    df = pd.read_csv(csv_data) #, header=None, names=["ID", "Review", "Rating", "Sentiment"])
    return df

def summarize(text_dict):
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="llama3-70b-8192")

    # Define the system message with additional requirements
    system = """You are an AI system designed to process and summarize text.
    You will receive a Python dictionary where each key represents an index, and its value is a detailed review.
    Your task is to process this dictionary and return the output as CSV text (no files, only plain text).
    CSV Requirements:
    - The header must be exactly: Index,Review,Rating,Sentiment (spellings must match exactly).
    - Each row should have:
        - "Index": same as the dictionary key,
        - "Review": a very concise summary of the review (enclosed in double quotes),
        - "Rating": an integer from 1 to 5 based on the review,
        - "Sentiment": either Positive, Negative, or Neutral.
    Strict Instructions:
    - Respond ONLY with raw CSV text.
    - Do NOT add any explanations, titles, or extra formatting.
    - Ensure the column names match exactly: Index,Review,Rating,Sentiment.
    The summaries must be objective, unbiased, and free from emotional language."""
    # Join the reviews into one string
    human_reviews = "\n".join(f"{key + 1}: {value}" for key, value in text_dict.items())
    human = "{text}"

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    # Invoke the chain with the required input
    chain = prompt | chat
    response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
    res = response.content

    return res


def tag_it(text_dict):
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key="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",
                    model_name="llama3-70b-8192")

    # Define the system and human messages
    system = """You are an AI-powered review classification assistant. Your task is to analyze a given dictionary of client reviews and classify each review into one or more relevant categories.  

    ### Instructions:
    {{1}} Analyze the reviews to identify key themes (e.g., product quality, pricing, delivery, customer experience).  
    {{2}} Generate a concise set of 5–10 categories that broadly cover most of the reviews.  
       - Categories should be **general enough** to apply to multiple reviews.  
       - Avoid creating redundant or highly specific categories.  
    {{3}} Classify each review into one or more relevant categories.  
       - A review can belong to **multiple categories** if it discusses different aspects.  
       - If a review does not fit any clear category, assign it to `"Other"`.  
    {{4}} Return the output as a CSV text (no files, only plain text):  
        Each row should have:
        - "Index": same as the dictionary key,  
        - "Tags": containing the assigned categories, separated by commas and in double quotes"".    
    Do **not** provide explanations, extra text, or formatting—just return the csv text only, not even the text like "here is the required information or something like that".
    """
    human_reviews = "\n".join(f"{key + 1}: {value}" for key, value in text_dict.items())
    human = "{text}"

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    # Invoke the chain with the required input
    chain = prompt | chat
    response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
    res = response.content
    return res

def count_sentiments(df):
    positive_count = (df['Sentiment'] == 'Positive').sum()
    negative_count = (df['Sentiment'] == 'Negative').sum()
    neutral_count = (df['Sentiment'] == 'Neutral').sum()
    gen_rating_mean = df['Rating'].mean()
    return positive_count, negative_count, neutral_count, gen_rating_mean

def actual_rating(df):
    act_rating_mean = df['Rating'].mean()
    return act_rating_mean
print("actual rating = ", actual_rating(df))

# # Function to summarize that have been retrieved from the uploaded document
# def summarize_reviews(text_dict):
#     # Initialize the ChatGroq model
#     chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mistral-saba-24b")
#
#     # Define the system and human messages
#     system = "You are an AI system designed to process and summarize text. You will receive a Python dictionary where each key represents an index, and its value is a detailed review. Your task is to process this dictionary and return a new dictionary (give only dictionary donot add any other responses) with the same keys, where each value is a concise summary of the corresponding review. The summaries should be very concise, retaining the core meaning of the original review, including key insights, sentiment, and main points. Each summary should be objective, unbiased, and free from emotional or subjective language and enclosed in double quotes as strings for further programming use."
#     human_reviews = "\n".join(f"{key}: {value}" for key, value in text_dict.items())
#     human = "{text}"
#
#     # Create the prompt template
#     prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
#
#     # Invoke the chain with the required input
#     chain = prompt | chat
#     response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
#     res = response.content
#     return res

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




# def Sentiment_analysis(text_dict):
#     # Initialize the ChatGroq model
#     chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mistral-saba-24b")
#
#     # Define the system and human messages
#     system = "You are an AI system designed to analyze and classify text. You will receive a Python dictionary where each key represents an index, and its value is a detailed review. Your task is to process this dictionary and return a new dictionary (give only dictionary, do not add any other responses) with the same keys, where each value is the sentiment of the corresponding review. The sentiment should be classified as 'Positive,' 'Negative,' or 'Neutral' and enclosed in double quotes as strings for further programming use."
#     human_reviews = "\n".join(f"{key}: {value}" for key, value in text_dict.items())
#     human = "{text}"
#
#     # Create the prompt template
#     prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
#
#     # Invoke the chain with the required input
#     chain = prompt | chat
#     response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
#     res = response.content
#     return res