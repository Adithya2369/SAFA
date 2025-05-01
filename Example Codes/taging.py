import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from io import StringIO

def csv_text_to_dataframe(csv_text):
    from io import StringIO
    csv_data = StringIO(csv_text)
    df = pd.read_csv(csv_data)  # No header=None, because LLM gives headers
    return df

# Update the path to the Excel file
df = pd.read_excel('uploads/TestData.xlsx')

# Extract the 'text' column and convert to a dictionary
text_column = df['Text']
text_dict = text_column.to_dict()
def tag_it(text_dict):
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="llama3-70b-8192")

    # Define the system and human messages
    system = """You are an AI-powered review classification assistant. Your task is to analyze a given dictionary of client reviews and classify each review into one or more relevant categories.  
    
    ### **Instructions:**  
    {{1}} **Analyze the reviews** to identify key themes (e.g., product quality, pricing, delivery, customer experience).  
    {{2}} **Generate a concise set of 5–10 categories** that broadly cover most of the reviews.  
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
    human_reviews = "\n".join(f"{key+1}: {value}" for key, value in text_dict.items())
    human = "{text}"

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    # Invoke the chain with the required input
    chain = prompt | chat
    response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
    res = response.content
    return res
#print(tag_it(text_dict))
print(csv_text_to_dataframe(tag_it(text_dict)))