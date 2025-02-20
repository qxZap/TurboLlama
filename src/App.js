import { useState, useRef, useEffect } from "react";

import Message from "./components/Message";
import Input from "./components/Input";
import History from "./components/History";
import Clear from "./components/Clear";

import "./styles.css";

export default function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async () => {
    setInput("");
    const prompt = { role: "user", content: input };

    setMessages([...messages, prompt]);

    await fetch("http://localhost:11434/v1/chat/completions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: "mistral", messages: [...messages, prompt] }),
    })
      .then((data) => data.json())
      .then((data) => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { role: "assistant", content: data.choices[0].message.content },
        ]);
        setHistory((prevHistory) => [
          ...prevHistory,
          { question: input, answer: data.choices[0].message.content },
        ]);
        scrollToBottom();
      });
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const clear = () => {
    setMessages([]);
    setHistory([]);
  };

  return (
    <div className="App">
      <div className="Column">
        <h3 className="Title">Chat Messages</h3>
        <div className="Content">
          {messages.map((el, i) => (
            <Message key={i} role={el.role} content={el.content} />
          ))}
          <div ref={messagesEndRef} />
        </div>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onClick={input ? handleSubmit : undefined}
        />
      </div>
      <div className="Column">
        <h3 className="Title">History</h3>
        <div className="Content">
          {history.map((el, i) => (
            <History
              key={i}
              question={el.question}
              onClick={() =>
                setMessages([
                  { role: "user", content: history[i].question },
                  { role: "assistant", content: history[i].answer },
                ])
              }
            />
          ))}
        </div>
        <Clear onClick={clear} />
      </div>
    </div>
  );
}
