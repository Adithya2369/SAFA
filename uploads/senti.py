

def Sentiment_analysis(text_dict):
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")

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