### the code works but the output did not meet my expectations

import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Update the path to the Excel file
df = pd.read_excel('uploads/TestData.xlsx')

# Extract the 'text' column and convert to a dictionary
text_column = df['Text']
text_dict = text_column.to_dict()

# Initialize the ChatGroq model
chat = ChatGroq(temperature=0.3, groq_api_key="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", model_name="mixtral-8x7b-32768")

# Define the system and human messages
system = """You are an AI-powered review classification assistant. Your task is to analyze a given dictionary of client reviews and classify each review into one or more relevant categories.  

### **Instructions:**  
{{1}} **Analyze the reviews** to identify key themes (e.g., product quality, pricing, delivery, customer experience).  
{{2}} **Generate a concise set of 5–10 categories** that broadly cover most of the reviews.  
   - Categories should be **general enough** to apply to multiple reviews.  
   - Avoid creating redundant or highly specific categories.  
{{3}} **Classify each review into one or more relevant categories.**  
   - A review can belong to **multiple categories** if it discusses different aspects.  
   - If a review does not fit any clear category, assign it to `"Other"`.  
{{4}} **Return the output as a dictionary** where:  
   - The **keys are the original review indices** from the input.  
   - The **values are single strings** containing the assigned categories, separated by commas.  

### **Output Format:**  
Return a dictionary where:  
- The keys match the original review identifiers.  
- The values are single strings of assigned categories, separated by commas.  

Do **not** provide explanations, extra text, or formatting—just return the dictionary.

"""
human_reviews = "\n".join(f"{key}: {value}" for key, value in text_dict.items())
human = "{text}"

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

# Invoke the chain with the required input
chain = prompt | chat
response = chain.invoke({"text": f"Here are the client reviews:\n{human_reviews}"})
print(response.content)


# Convert the response into a dictionary
#tags = eval(response.content)  # Assuming the response is in Python dictionary format

# Add the summarized reviews as a new column to the DataFrame
#df['tags'] = df.index.map(tags)

# Save the updated DataFrame back to the Excel file
#df.to_excel('processed/TestData_updated_tags.xlsx', index=False)
'''
For example, if the input review dictionary is:  
python:
{
    {{1}}: "The apples were fresh and tasted great!",
    {{2}}: "Delivery was late, and the packaging was damaged.",
    {{3}}: "Too expensive for the quality offered."
    {{4}}: "The oranges were good but the delivery did not meet my expectations"
}
output should be:
{
    {{1}}: "Product Quality",
    {{2}}: "Delivery, Packaging",
    {{3}}: "Pricing"
    {{4}}: "Product Quality, Delivery"
}'''