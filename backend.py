from google import genai
from google.genai import types
import base64
from gtts import gTTS
import pygame
import os
import speech_recognition as sr

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
   
    try:
        text = recognizer.recognize_google(audio)
        print("✅ You said:", text)
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, could not understand the audio.")
        return ""  # Return an empty string so the conversation doesn't break
    except sr.RequestError:
        print("❌ Could not request results, check your internet connection.")
        return ""

def generate(prompt):
    client = genai.Client(
        vertexai=True,
        project="chayan-development",
        location="us-central1",
    )

    text1 = types.Part.from_text(text=prompt)
    system_instruction = """hii act like you are my old friend and talk to me. don't give too long responses and too many questions at once. Keep the tone of conversation friendly. Don't mention that you are an AI. You can use some general lies to continue the conversation. I will give you previous conversation history between me and you so that you can give relevant and contextual replies. I will symbolize myself as user and you as AI. You don't write your response as AI:, simply just write your response"""

    model = "gemini-2.0-flash-001"
    contents = [types.Content(role="user", parts=[text1])]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=512,
        response_modalities=["TEXT"],
        system_instruction=types.Part.from_text(text=system_instruction),
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return response.text if response.text else ""

# 🌟 Start Conversation
userinput = input("🗣 Start your conversation: ")
chathistory = f"user: {userinput}"
i = 0

while userinput.lower().strip() != "bye":
    # 🧠 Generate AI response
    response = generate(chathistory)
    print("🤖 AI:", response)  

    # 🗣 Convert AI response to speech
    myobj = gTTS(text=response, lang="en", slow=False)
    audio_filename = f"response_{i}.mp3"
    myobj.save(audio_filename)

    # 🎵 Play the response audio
    pygame.mixer.init()
    pygame.mixer.music.load(audio_filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # 🧹 Cleanup
    pygame.mixer.quit()
    os.remove(audio_filename)

    # 🎤 Get user input via speech recognition
    userinput = speech_to_text()
    
    if userinput.strip():  # Prevent adding empty input
        chathistory += f"\nAI: {response}\nuser: {userinput}"

    i += 1  # Increment filename counter
