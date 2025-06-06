from google import genai
from google.genai import types
import base64
from gtts import gTTS
import pygame
import os

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
            parts=[text1]
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
        ],
        system_instruction=types.Part.from_text(text=si_text1),  # FIXED THIS LINE
    )

    # Using generate_content instead of generate_content_stream
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return response.text if response.text else ""  # Ensure text is returned

# Start conversation
a = input("Start your conversation by saying something: ")
chathistory = f"user: {a}"

# Initialize user input before the loop
userinput = ""
i = 0

while userinput.lower().strip() != "bye":
    # Generate response using current chat history
    response = generate(chathistory)

    print("AI:", response)  # Print AI response

    # Convert response to speech
    language = 'en'
    myobj = gTTS(text=response, lang=language, slow=False)

    audio_filename = f"welcome{i}.mp3"
    myobj.save(audio_filename)

    # Initialize pygame mixer and play audio
    pygame.mixer.init()
    pygame.mixer.music.load(audio_filename)
    pygame.mixer.music.play()

    # Wait for audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Cleanup the audio file
    pygame.mixer.quit()
    os.remove(audio_filename)  # Delete file after playing

    # Get user input
    userinput = input("You: ")
    
    # Update chat history with new exchange
    chathistory += f"\nAI: {response}\nuser: {userinput}"
    
    i += 1  # Increment filename counter
