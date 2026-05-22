import React, { useState, useRef } from "react";

function App() {
  const [recording, setRecording] = useState(false);
  const [processing, setProcessing] = useState(false);

  const [messages, setMessages] = useState([]);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const currentAudioRef = useRef(null);

  // START RECORDING
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      const mediaRecorder = new MediaRecorder(stream);

      mediaRecorderRef.current = mediaRecorder;

      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/wav",
        });

        const formData = new FormData();

        formData.append("file", audioBlob, "recording.wav");

        setProcessing(true);

        try {
          const response = await fetch(
            "http://127.0.0.1:8000/process-audio",
            {
              method: "POST",
              body: formData,
            }
          );

          const data = await response.json();

          setMessages((prev) => [
            ...prev,
            {
              user: data.user_text,
              ai: data.ai_response,
            },
          ]);
        } catch (error) {
          console.error("Error:", error);
        }

        setProcessing(false);
      };

      mediaRecorder.start();

      setRecording(true);
    } catch (error) {
      console.error("Microphone error:", error);
    }
  };

  // STOP RECORDING
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();

      setRecording(false);
    }
  };

  // PLAY AI AUDIO
  const playAudio = async (text) => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/text-to-speech",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: text,
          }),
        }
      );

      const audioBlob = await response.blob();

      const audioUrl = URL.createObjectURL(audioBlob);

      const audio = new Audio(audioUrl);

      currentAudioRef.current = audio;

      audio.play();
    } catch (error) {
      console.error("Audio play error:", error);
    }
  };

  // STOP AUDIO
  const stopAudio = () => {
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();

      currentAudioRef.current.currentTime = 0;
    }
  };

  return (
    <div
      style={{
        backgroundColor: "#071133",
        minHeight: "100vh",
        color: "white",
        fontFamily: "Arial",
      }}
    >
      {/* HEADER */}
      <div
        style={{
          textAlign: "center",
          paddingTop: "20px",
        }}
      >
        <h1>Voice AI Healthcare Agent</h1>
        <p style={{ color: "white" }}>
          Multilingual Voice-Based Healthcare Assistant
        </p>
      </div>

      {/* RECORDING SECTION */}
      <div
        style={{
          position: "sticky",
          top: 0,
          backgroundColor: "#071133",
          zIndex: 1000,
          padding: "20px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: "15px",
          flexWrap: "wrap",
          borderBottom: "1px solid #1e2d5c",
        }}
      >
        {/* START BUTTON */}
        {!recording && !processing && (
          <button
            onClick={startRecording}
            style={{
              padding: "15px 30px",
              backgroundColor: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "10px",
              fontSize: "18px",
              cursor: "pointer",
            }}
          >
            Start Recording
          </button>
        )}
        {!recording && !processing && messages.length > 0 && (
          <button
            onClick={() => setMessages([])}
            style={{
              backgroundColor: "#444",
              color: "white",
              border: "none",
              padding: "10px 20px",
              borderRadius: "8px",
              marginLeft: "10px",
              cursor: "pointer",
            }}
          >
            Clear Chat
          </button>
        )}

        {/* STOP BUTTON */}
        {recording && (
          <button
            onClick={stopRecording}
            style={{
              padding: "15px 30px",
              backgroundColor: "red",
              color: "white",
              border: "none",
              borderRadius: "10px",
              fontSize: "18px",
              cursor: "pointer",
            }}
          >
            Stop Recording
          </button>
        )}

        {/* RECORDING TEXT */}
        {recording && (
          <p
            style={{
              marginTop: "15px",
              fontSize: "18px",
            }}
          >
            Recording audio...
          </p>
        )}

        {/* PROCESSING TEXT */}
        {processing && (
          <p
            style={{
              marginTop: "15px",
              fontSize: "18px",
            }}
          >
            Processing audio...
          </p>
        )}
      </div>

      {/* CHAT CONTAINER */}
      <div
        style={{
          maxWidth: "900px",
          margin: "20px auto",
          height: "70vh",
          overflowY: "auto",
          padding: "10px",
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              marginBottom: "25px",
            }}
          >
            {/* USER MESSAGE */}
            <div
              style={{
                backgroundColor: "#2563eb",
                padding: "15px",
                borderRadius: "12px",
                marginBottom: "10px",
              }}
            >
              <strong>You:</strong> {msg.user}
            </div>

            {/* AI MESSAGE */}
            <div
              style={{
                backgroundColor: "#1e293b",
                padding: "15px",
                borderRadius: "12px",
              }}
            >
              <strong>AI:</strong> {msg.ai}
            </div>

            {/* AUDIO BUTTONS */}
            <div
              style={{
                marginTop: "10px",
                display: "flex",
                gap: "10px",
              }}
            >
              <button
                onClick={() => playAudio(msg.ai)}
                style={{
                  backgroundColor: "#16a34a",
                  color: "white",
                  border: "none",
                  padding: "10px 15px",
                  borderRadius: "8px",
                  cursor: "pointer",
                }}
              >
                Play Voice
              </button>

              <button
                onClick={stopAudio}
                style={{
                  backgroundColor: "#dc2626",
                  color: "white",
                  border: "none",
                  padding: "10px 15px",
                  borderRadius: "8px",
                  cursor: "pointer",
                }}
              >
                Stop Voice
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;