from google import genai
from google.genai import types
import base64

def generate(prompt):
    client = genai.Client(
        vertexai=True,
        project="chayan-development",
        location="us-central1",
    )

    text1 = types.Part.from_text(text=prompt)
    si_text1 = """hii act like you are my old friend and talk to me. dont give too long responses and too many questions at once. keep the tone of conversation friendly. Dont mention the fact that you are an ai you can use some general lies to continue the conversation. i will give you previous conversation history between me and you, so that you can give relevant and contextual replies. i will symbolise myself as user and you as AI. You don't write your response as AI:, simply just write your response"""

    model = "gemini-2.0-flash-001"
    contents = [
        types.Content(
            role="user",
            parts=[
                text1
            ]
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="OFF"
        )],
        system_instruction=[types.Part.from_text(text=si_text1)],
    )

    output = ""  # Initialize output variable
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text:  # Check if there's text in the chunk
            output += chunk.text  # Append text to output variable

    return output  # Return the collected text

a=input("start your conversation by saying something: ")
chathistory=f"user: {a}"
# Initialize userinput before the loop
userinput = ""
while userinput.lower().strip() != "bye":  # Add .lower() and .strip() for better input handling
    # Generate response using current chat history
    response = generate(chathistory)
    print("AI:", response)
    
    # Get user input
    userinput = input("You: ")
    
    # Update chat history with new exchange
    chathistory += f"\nAI: {response}\nuser: {userinput}"

# print(generate(chathistory))
# print(out)
# aioutput
# userinput=input("Your response here:")
# generate(chathistory + aioutput + userinput)