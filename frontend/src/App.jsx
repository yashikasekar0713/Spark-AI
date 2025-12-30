import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askBackend = async () => {
    setLoading(true);
    setAnswer("");

    const res = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    setAnswer(data.answer);
    setLoading(false);
  };

  return (
    <div style={{ padding: 40, maxWidth: 700, margin: "auto", fontFamily: "Arial" }}>
      <h2>Startup Funding Assistant</h2>

      <textarea
        rows={4}
        style={{ width: "100%", padding: 10 }}
        placeholder="Ask about the report..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <br /><br />

      <button onClick={askBackend} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      <div
        style={{
          marginTop: 20,
          background: "#f3f3f3",
          padding: 20,
          borderRadius: 6,
          color: "#000"
        }}
      >
        <b>Answer:</b>
        <p>{answer}</p>
      </div>
    </div>
  );
}

export default App;
