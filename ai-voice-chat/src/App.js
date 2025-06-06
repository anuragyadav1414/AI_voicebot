import React, { useState } from "react";

export default function VoiceChat() {
  const [conversation, setConversation] = useState([]);
  const [isRecording, setIsRecording] = useState(false);

  const handleSpeechToText = async () => {
    setIsRecording(true);

    try {
      const response = await fetch("http://localhost:5000/speech-to-text", {
        method: "POST",
      });

      const data = await response.json();
      if (data.text) {
        setConversation((prev) => [...prev, { role: "User", text: data.text }]);
        getAIResponse(data.text);
      }
    } catch (error) {
      console.error("Error processing speech:", error);
    }

    setIsRecording(false);
  };

  const getAIResponse = async (text) => {
    try {
      const response = await fetch("http://localhost:5000/generate-response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: text }),
      });

      const data = await response.json();
      if (data.audio_url) {
        setConversation((prev) => [...prev, { role: "AI", text: data.text }]);
        playAudio(data.audio_url);
      }
    } catch (error) {
      console.error("Error fetching AI response:", error);
    }
  };

  const playAudio = (audioUrl) => {
    const audio = new Audio(audioUrl);
    audio.play();
  };

  return (
    <div className="p-4 max-w-lg mx-auto">
      <h1 className="text-xl font-bold mb-4">AI Voice Chat</h1>
      <button
        className={`px-4 py-2 rounded ${isRecording ? "bg-gray-400" : "bg-blue-500 text-white"}`}
        onClick={handleSpeechToText}
        disabled={isRecording}
      >
        {isRecording ? "Listening..." : "Speak"}
      </button>

      <div className="mt-4">
        {conversation.map((msg, index) => (
          <p key={index} className={`p-2 ${msg.role === "User" ? "bg-gray-200" : "bg-green-200"}`}>
            <strong>{msg.role}: </strong> {msg.text}
          </p>
        ))}
      </div>
    </div>
  );
}
