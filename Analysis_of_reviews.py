import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Update the path to the Excel file
df = pd.read_excel('uploads/TestData.xlsx')

# Extract the 'text' column and convert to a dictionary
text_column = df['Text']
text_dict = text_column.to_dict()
def perform_analysis(text_dict):
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")

    # Define the system and human messages
    system = "You are a business analyst. Based on the given reviews, write a summary report highlighting the key points."
    human_reviews = "\n".join(text_dict.values())  # Join the dictionary values
    human = "{text}"

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    # Invoke the chain with the required input
    chain = prompt | chat
    response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
    print(response.content)

perform_analysis(text_dict)