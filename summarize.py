import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Update the path to the Excel file
df = pd.read_excel('uploads/TestData.xlsx')

# Extract the 'text' column and convert to a dictionary
text_column = df['Text']
text_dict = text_column.to_dict()


def summarize(text_dict):
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="llama3-70b-8192")

    # Define the system message with additional requirements
    system = """You are an AI system designed to process and summarize text. 
    You will receive a Python dictionary where each key represents an index, and its value is a detailed review.
    Your task is to process this dictionary and return the output as a CSV text (no files, only plain text).
    Each row should have:
    - "Index": same as the dictionary key,
    - "Summary": a very concise summary of the review (enclosed in double quotes),
    - "Rating": a rating from 1 to 5 depending on the review,
    - "Sentiment": either Positive, Negative, or Neutral.
    Strict Instructions:
    - Respond ONLY with raw CSV format text.
    - Do not add any extra explanations, messages, or headings.
    - Keep everything as plain CSV text.
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


# Test the updated function
print(summarize(text_dict))