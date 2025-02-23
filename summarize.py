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
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")

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
print(summarize(text_dict))
# # Convert the response into a dictionary
# summarized_reviews = eval(response.content)  # Assuming the response is in Python dictionary format
#
# # Add the summarized reviews as a new column to the DataFrame
# df['Summarized Review'] = df.index.map(summarized_reviews)
#
# # Save the updated DataFrame back to the Excel file
# df.to_excel('processed/TestData_updated.xlsx', index=False)