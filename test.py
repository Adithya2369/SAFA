import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from io import StringIO

# Update the path to the Excel file
df = pd.read_excel('uploads/TestData.xlsx')
# Extract the 'text' column and convert to a dictionary
text_column = df['Text']
text_dict = text_column.to_dict()

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

df1 = csv_text_to_dataframe(summarize(text_dict))
df2 = csv_text_to_dataframe(tag_it(text_dict))

merged_df = df1.merge(df2, on="Index", how="left")
print(merged_df)
print(count_sentiments(merged_df))
