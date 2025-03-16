import google.generativeai as genai
from google.generativeai import types

# Initialize the client with your API key
client = genai.Client(api_key="AIzaSyBC0qbLDuWXwrmNahgu5U_4l3bnnhlAQxQ")  # Replace with your actual API key

# Use your fine-tuned model
model = "tunedModels/customerfeedbackanalyzer-r79aagjknmx5"

# Config for response generation
generate_content_config = types.GenerateContentConfig(
    temperature=1,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
    response_mime_type="text/plain",
)


def chat():
    print("Chatbot started. Type 'exit' to stop.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot session ended.")
            break

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)],
            ),
        ]

        print("Bot:", end=" ", flush=True)

        for chunk in client.models.generate_content_stream(
                model=model, contents=contents, config=generate_content_config
        ):
            print(chunk.text, end="", flush=True)

        print()  # Newline after response


if __name__ == "__main__":
    chat()
