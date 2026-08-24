import { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState(
    "Connecting to MemoraAI backend..."
  );

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/health")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }

        return response.json();
      })
      .then((data) => {
        setMessage(`${data.status} - ${data.service}`);
      })
      .catch((error) => {
        console.error("Backend connection error:", error);
        setMessage("Backend connection failed");
      });
  }, []);

  return (
    <div>
      <h1>MemoraAI</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;